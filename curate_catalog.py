#!/usr/bin/env python3
"""Categorize discovery results without discarding games, plugins or technical projects.

Categories are metadata hints, not playability or licensing verification.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re

from game_miner import render_html

PLUGIN = re.compile(r"\b(?:plugins?|ads integration|web workers|software library|integration library|game engine|game framework|sdk)\b", re.I)
STARTER = re.compile(r"\b(?:boilerplate|bootstrap project|starter kit|project template|code examples)\b", re.I)
SERVER_RUNTIME = re.compile(r"\ballows? you to run\b.*\bon node\b", re.I)
FRAMEWORK_PORT = re.compile(r"\b(?:make|making)\s+phaser\s+works?\s+with\b", re.I)
SERVER_DEPENDENCY = re.compile(r"\b(?:websockets?|socket\.io|dedicated server|requires? a backend)\b", re.I)
WEB3_DEPENDENCY = re.compile(r"\b(?:ERC-?721|NFT|crypto payout|smart contract)\b", re.I)
HARDWARE_SIMULATOR = re.compile(r"\b(?:arduino|microcontroller|cpu emulator)\b.*\b(?:simulator|emulator)\b", re.I)


def classify(item: dict) -> tuple[str, str]:
    name = (item.get("full_name") or "").split("/")[-1]
    desc = item.get("description") or ""
    if HARDWARE_SIMULATOR.search(desc):
        return "other", "hardware simulator; not a game, but preserved for review"
    if SERVER_RUNTIME.search(desc) or FRAMEWORK_PORT.search(desc):
        return "tool", "game-engine runtime or platform port, not a standalone game"
    if PLUGIN.search(name) or PLUGIN.search(desc) or re.search(r"(?:^|[-_.])plugins?(?:$|[-_.])", name, re.I):
        return "tool", "plugin or game development tool; compatibility not verified"
    if STARTER.search(desc) or re.search(r"(?:^|[-_.])(?:templates?|boilerplates?|starters?)(?:$|[-_.])", name, re.I):
        return "starter", "project starter or instructional example, not necessarily a complete game"
    if SERVER_DEPENDENCY.search(desc) or WEB3_DEPENDENCY.search(desc):
        return "complex_game", "game with external server or Web3 dependency; standalone adaptation unverified"
    return "game", "candidate game; gameplay and build not verified"


def exclusion_reason(item: dict) -> str | None:
    """Compatibility shim: no discoveries are discarded merely for not being games."""
    return None


def _render(items: list[dict]) -> str:
    display = [{**item, "description": f"[{item['category']}] {item.get('description') or ''}"} for item in items]
    return render_html(display)


def curate(folder: Path) -> tuple[int, int]:
    source = folder / "candidates.json"
    items = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("candidates.json must contain a list")
    groups = {"game": [], "tool": [], "starter": [], "complex_game": [], "other": []}
    categorized = []
    for item in items:
        category, note = classify(item)
        entry = {**item, "category": category, "review_note": note}
        categorized.append(entry)
        groups[category].append(entry)
    (folder / "raw_candidates.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "excluded.json").write_text("[]\n", encoding="utf-8")
    source.write_text(json.dumps(categorized, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = folder / "candidates.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        fieldnames = list(csv.DictReader(f).fieldnames or ())
    if not fieldnames:
        raise ValueError("Cannot find columns in candidates.csv")
    fieldnames = list(dict.fromkeys([*fieldnames, "category", "review_note"]))
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in fieldnames} for item in categorized)
    labels = {"game": "Games", "tool": "Plugins and tools", "starter": "Starters and examples", "complex_game": "Games requiring integrations", "other": "Other discoveries"}
    navigation = ' · '.join(f'<a href="{key}.html">{label} ({len(groups[key])})</a>' for key, label in labels.items())
    index = _render(categorized).replace("<h1>Game Miner</h1>", f"<h1>Game Miner</h1><nav>{navigation}</nav>", 1)
    (folder / "index.html").write_text(index, encoding="utf-8")
    for category, subset in groups.items():
        (folder / f"{category}.html").write_text(_render(subset), encoding="utf-8")
        (folder / f"{category}.json").write_text(json.dumps(subset, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Catalog: " + ", ".join(f"{k}={len(v)}" for k, v in groups.items()) + f"; preserved={len(categorized)}")
    return len(categorized), 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Categorize game and Phaser tooling discoveries without discarding them")
    parser.add_argument("folder", nargs="?", default="results")
    args = parser.parse_args()
    curate(Path(args.folder))


if __name__ == "__main__":
    main()
