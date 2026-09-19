#!/usr/bin/env python3
"""Incremental discovery: preserve seen projects, queue and search cursors."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

from curate_catalog import _render, curate
from game_miner import GitHub, inspect
from discovery_policy import SEARCH_TRACKS, enrich, inspection_order, relevance_reason

CSV_COLUMNS = [
    "full_name", "url", "description", "engine", "language", "license",
    "license_status", "assets_status", "score", "size_kb", "stars",
    "last_push", "homepage", "review_status", "category", "review_note",
    "discovery_track", "mechanic_signals", "idea_review", "porting_effort_hint", "porting_reason",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "seen": {}, "pending": {}, "query_cursors": {}, "irrelevant": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not all(isinstance(data.get(field), dict) for field in ("seen", "pending", "query_cursors")):
        raise ValueError("Invalid discovery registry schema; refusing to overwrite it")
    if not isinstance(data.setdefault("irrelevant", {}), dict):
        raise ValueError("Invalid irrelevant registry; refusing to overwrite it")
    return data


def repo_key(repo: dict) -> str:
    """GitHub numeric IDs survive repository renames."""
    return str(repo["id"]) if repo.get("id") is not None else "name:" + repo["full_name"].lower()


def compact_repo(repo: dict) -> dict:
    fields = (
        "id", "full_name", "name", "html_url", "description", "language", "size",
        "stargazers_count", "fork", "archived", "disabled", "license", "topics",
        "default_branch", "homepage", "pushed_at", "discovery_track",
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
    irrelevant: dict = state["irrelevant"]
    api = api or GitHub(os.getenv("GITHUB_TOKEN"), Path(args.cache), refresh=True)
    queries = SEARCH_TRACKS if searches is None else [(q, "unspecified", 30000) for q in searches]
    new_discoveries = 0
    already_inspected = 0
    new_irrelevant = 0
    restored = 0
    # Updated heuristics may rescue entries previously considered unrelated.
    for key, entry in list(irrelevant.items()):
        if relevance_reason(entry["repo"]) is None:
            pending.setdefault(key, entry["repo"])
            del irrelevant[key]
            restored += 1
    for entry in seen.values():
        item = entry["item"]
        # Real engine evidence overrides a search-track guess (TOSIOS is not iOS).
        if item.get("engine") in ("Phaser", "PixiJS", "Browser/JS", "Three.js", "Godot", "Unity"):
            detected = item["engine"]
            item["discovery_track"] = ("phaser" if detected == "Phaser" else
                                       "godot" if detected == "Godot" else
                                       "unity" if detected == "Unity" else "browser")
    # Revisit old pending items using the current conservative metadata precheck.
    for key, repo in list(pending.items()):
        reason = relevance_reason(repo)
        if reason:
            irrelevant[key] = {"repo": repo, "reason": reason}
            del pending[key]
            new_irrelevant += 1
    max_page = max(1, min(10, 1000 // args.per_query))
    for index, (base_query, track, size_limit) in enumerate(queries, 1):
        query = f"{base_query} is:public fork:false archived:false size:<{size_limit}"
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
                elif key in irrelevant:
                    continue
                else:
                    candidate = compact_repo({**repo, "discovery_track": track})
                    reason = relevance_reason(candidate)
                    if reason:
                        irrelevant[key] = {"repo": candidate, "reason": reason}
                        pending.pop(key, None)
                        new_irrelevant += 1
                    else:
                        if key not in pending:
                            new_discoveries += 1
                        if key in pending and track == "unspecified":
                            candidate["discovery_track"] = pending[key].get("discovery_track")
                        pending[key] = candidate
            print(f"Search {index}/{len(queries)} page {page}: {len(hits)} hits; {len(pending)} queued; {len(seen)} inspected", file=sys.stderr)
            page = page + 1 if len(hits) == args.per_query and page < max_page else 1
            cursors[base_query] = page
            if len(hits) < args.per_query or page == 1:
                break

    now = utc_now()
    new_keys = []
    for key in inspection_order(pending, args.inspect):
        repo = pending[key]
        try:
            item = enrich(inspect(api, repo), repo)
        except (RuntimeError, ValueError, KeyError, TypeError) as exc:
            print(f"Inspection deferred {repo.get('full_name')}: {exc}", file=sys.stderr)
            continue
        seen[key] = {"repo_id": repo.get("id"), "first_seen": now, "inspected_at": now, "item": item}
        del pending[key]
        new_keys.append(key)

    target = Path(args.output)
    target.mkdir(parents=True, exist_ok=True)
    all_items = sorted((entry["item"] for entry in seen.values()), key=lambda item: item["score"], reverse=True)
    (target / "candidates.json").write_text(json.dumps(all_items, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(target / "candidates.csv", all_items)
    curate(target)  # preserves games, plugins, starters and complex projects
    categorized = json.loads((target / "candidates.json").read_text(encoding="utf-8"))
    by_name = {item["full_name"].lower(): item for item in categorized}
    for entry in seen.values():
        entry["item"] = by_name[entry["item"]["full_name"].lower()]
    new_items = sorted((seen[key]["item"] for key in new_keys), key=lambda item: item["score"], reverse=True)
    (target / "new.json").write_text(json.dumps(new_items, ensure_ascii=False, indent=2), encoding="utf-8")
    (target / "new.html").write_text(_render(new_items), encoding="utf-8")
    write_csv(target / "new.csv", new_items)
    (target / "irrelevant.json").write_text(json.dumps(irrelevant, indent=2, ensure_ascii=False), encoding="utf-8")
    stats = {
        "new_discoveries_queued": new_discoveries,
        "already_inspected_search_hits": already_inspected,
        "newly_inspected": len(new_items),
        "pending": len(pending),
        "irrelevant_new": new_irrelevant,
        "irrelevant_restored": restored,
        "irrelevant_total": len(irrelevant),
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
