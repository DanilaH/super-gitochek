#!/usr/bin/env python3
"""Curate a Game Miner scan without losing the unfiltered discovery data.

Only rejects clear tool/template/server-only signals. Still does NOT verify gameplay,
license terms, or permission to redistribute bundled assets.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re

from game_miner import render_html

NON_GAME_NAMES = re.compile(r"(?:^|[-_.])(plugins?|templates?|boilerplates?|starters?|sdks?|examples?)(?:$|[-_.])", re.I)
NON_GAME_DESCRIPTIONS = re.compile(
    r"\b(?:plugin|plugins|boilerplate|bootstrap project|starter kit|project template|"
    r"game engine|game framework|software library|code examples|ads integration|"
    r"integration library|provides? (?:an? )?(?:api|sdk|library))\b", re.I
)
SERVER_ONLY = re.compile(r"\ballows? you to run\b.*\bon node\b", re.I)
SERVER_DEPENDENCY = re.compile(r"\b(?:multiplayer|online)\b.*\b(?:socket\.io|websockets?|dedicated server|backend)\b", re.I)


def exclusion_reason(item: dict) -> str | None:
    name = item.get("full_name", "").split("/")[-1]
    description = item.get("description") or ""
    if NON_GAME_NAMES.search(name):
        return "repository name identifies a tool, template, plugin or example"
    if NON_GAME_DESCRIPTIONS.search(description):
        return "description identifies a tool, template, plugin or example"
    if SERVER_ONLY.search(description):
        return "server-side game runtime, not a standalone game"
    if SERVER_DEPENDENCY.search(description):
        return "multiplayer game explicitly requiring backend or sockets"
    return None


def curate(folder: Path) -> tuple[int, int]:
    source = folder / "candidates.json"
    items = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("candidates.json must contain a list")
    kept, excluded = [], []
    for item in items:
        reason = exclusion_reason(item)
        if reason:
            excluded.append({**item, "exclusion_reason": reason})
        else:
            kept.append(item)
    (folder / "raw_candidates.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "excluded.json").write_text(json.dumps(excluded, ensure_ascii=False, indent=2), encoding="utf-8")
    source.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = folder / "candidates.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        fieldnames = list(csv.DictReader(f).fieldnames or ())
    if not fieldnames:
        raise ValueError("Cannot find columns in candidates.csv")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in fieldnames} for item in kept)
    (folder / "index.html").write_text(render_html(kept), encoding="utf-8")
    print(f"Curated: {len(kept)} candidates; excluded {len(excluded)} clear non-game projects (preserved in excluded.json)")
    return len(kept), len(excluded)


def main() -> None:
    parser = argparse.ArgumentParser(description="Exclude obvious non-games from the generated catalog")
    parser.add_argument("folder", nargs="?", default="results")
    args = parser.parse_args()
    curate(Path(args.folder))


if __name__ == "__main__":
    main()
