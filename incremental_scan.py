#!/usr/bin/env python3
"""Incremental game discovery: persist inspected IDs and advance search pages."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

from curate_catalog import curate
from game_miner import GitHub, SEARCHES, inspect, preliminary, render_html

CSV_COLUMNS = [
    "full_name", "url", "description", "engine", "language", "license",
    "license_status", "assets_status", "score", "size_kb", "stars",
    "last_push", "homepage", "review_status", "category", "review_note",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "seen": {}, "pending": {}, "query_cursors": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not all(isinstance(data.get(field), dict) for field in ("seen", "pending", "query_cursors")):
        raise ValueError("Invalid discovery registry schema; refusing to overwrite it")
    return data


def repo_key(repo: dict) -> str:
    """GitHub numeric IDs remain stable if the repository gets renamed."""
    return str(repo["id"]) if repo.get("id") is not None else "name:" + repo["full_name"].lower()


def compact_repo(repo: dict) -> dict:
    fields = (
        "id", "full_name", "name", "html_url", "description", "language", "size",
        "stargazers_count", "fork", "archived", "disabled", "license", "topics",
        "default_branch", "homepage", "pushed_at",
    )
    return {key: repo.get(key) for key in fields}


def write_csv(path: Path, items: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in CSV_COLUMNS} for item in items)


def run_incremental(args: argparse.Namespace, *, api: GitHub | None = None, searches: list[str] | None = None) -> dict:
    registry_path = Path(args.registry)
    state = load_registry(registry_path)
    seen: dict = state["seen"]
    pending: dict = state["pending"]
    cursors: dict = state["query_cursors"]
    # Search responses must be fresh enough to discover changes; inspected repos are persisted separately.
    api = api or GitHub(os.getenv("GITHUB_TOKEN"), Path(args.cache), refresh=True)
    queries = SEARCHES if searches is None else searches
    new_discoveries = 0
    already_inspected = 0
    max_page = max(1, min(10, 1000 // args.per_query))
    for index, base_query in enumerate(queries, 1):
        query = f"{base_query} is:public fork:false archived:false size:<30000"
        page = int(cursors.get(base_query, 1))
        if page < 1 or page > max_page:
            page = 1
        for _ in range(args.pages):
            data = api.get("/search/repositories", {"q": query, "per_page": args.per_query, "page": page})
            hits = data.get("items", [])
            if data.get("incomplete_results"):
                print(f"WARNING: incomplete search {index}; will retry page {page}", file=sys.stderr)
                break
            for repo in hits:
                key = repo_key(repo)
                if key in seen:
                    already_inspected += 1
                elif key not in pending:
                    pending[key] = compact_repo(repo)
                    new_discoveries += 1
                else:
                    pending[key] = compact_repo(repo)
            print(f"Search {index}/{len(queries)} page {page}: {len(hits)} hits; {len(pending)} queued; {len(seen)} inspected", file=sys.stderr)
            page = page + 1 if len(hits) == args.per_query and page < max_page else 1
            cursors[base_query] = page
            if len(hits) < args.per_query or page == 1:
                break

    now = utc_now()
    new_keys = []
    for key in sorted(pending, key=lambda k: preliminary(pending[k]), reverse=True)[:args.inspect]:
        repo = pending[key]
        try:
            item = inspect(api, repo)
        except (RuntimeError, ValueError, KeyError, TypeError) as exc:
            print(f"Inspection deferred {repo.get('full_name')}: {exc}", file=sys.stderr)
            continue  # API failures are retried; neither ignored nor marked seen.
        seen[key] = {"repo_id": repo.get("id"), "first_seen": now, "inspected_at": now, "item": item}
        del pending[key]
        new_keys.append(key)

    target = Path(args.output)
    target.mkdir(parents=True, exist_ok=True)
    all_items = sorted((entry["item"] for entry in seen.values()), key=lambda item: item["score"], reverse=True)
    (target / "candidates.json").write_text(json.dumps(all_items, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(target / "candidates.csv", all_items)
    (target / "index.html").write_text(render_html(all_items), encoding="utf-8")
    curate(target)  # preserves plugins, starters and complex games under separate categories
    categorized = json.loads((target / "candidates.json").read_text(encoding="utf-8"))
    by_name = {item["full_name"].lower(): item for item in categorized}
    for entry in seen.values():
        entry["item"] = by_name[entry["item"]["full_name"].lower()]
    new_items = sorted((seen[key]["item"] for key in new_keys), key=lambda item: item["score"], reverse=True)
    (target / "new.json").write_text(json.dumps(new_items, ensure_ascii=False, indent=2), encoding="utf-8")
    (target / "new.html").write_text(render_html(new_items), encoding="utf-8")
    write_csv(target / "new.csv", new_items)
    stats = {
        "new_discoveries_queued": new_discoveries,
        "already_inspected_search_hits": already_inspected,
        "newly_inspected": len(new_items),
        "pending": len(pending),
        "total_catalog": len(seen),
    }
    (target / "scan_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    state["last_run"] = now
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = registry_path.with_suffix(registry_path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(registry_path)
    print("Incremental scan: " + ", ".join(f"{name}={value}" for name, value in stats.items()))
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Incremental GitHub game discovery with persistent registry")
    parser.add_argument("--registry", default="data/discovery-registry.json")
    parser.add_argument("--output", default="results")
    parser.add_argument("--cache", default=".github-cache")
    parser.add_argument("--inspect", type=int, default=30)
    parser.add_argument("--per-query", type=int, default=30)
    parser.add_argument("--pages", type=int, default=1)
    args = parser.parse_args()
    if not (1 <= args.inspect <= 500 and 1 <= args.per_query <= 100 and 1 <= args.pages <= 10):
        parser.error("Use --inspect 1..500, --per-query 1..100, --pages 1..10")
    run_incremental(args)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
