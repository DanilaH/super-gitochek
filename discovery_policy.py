"""Broader game discovery; metadata never verifies gameplay, portability or rights."""
from __future__ import annotations
import re
from collections import defaultdict, deque
from game_miner import SEARCHES, preliminary

# Preserve old query strings and pagination; GitHub repo sizes are in KB.
SEARCH_TRACKS = [(q, "phaser" if "phaser" in q else "godot" if "godot" in q else "browser", 30000) for q in SEARCHES]
# Small live A/B on 2026-09-20: matching names/descriptions surfaced playable-code
# leads drowned out by unrelated README matches. Keep README queries too: they
# surface mini-game collections that are not named for individual mechanics.
SEARCH_TRACKS += [
    ("phaser incremental game in:name,description", "phaser", 30000),
    ("phaser fishing game in:name,description", "phaser", 30000),
    ("phaser mining game in:name,description", "phaser", 30000),
]
SEARCH_TRACKS += [
    ("phaser plugin language:TypeScript in:name,description", "phaser", 30000),
    ("phaser plugin language:JavaScript in:name,description", "phaser", 30000),
    ("topic:unity2d game language:C#", "unity", 200000),
    ("unity 2d game language:C# in:name,description", "unity", 200000),
    ("unity clicker game in:name,description", "unity", 200000),
    ("topic:unity-game language:C#", "unity", 200000),
    ("topic:android-game language:Kotlin", "android", 75000),
    ("android game language:Kotlin in:name,description", "android", 75000),
    ("libgdx game language:Java in:name,description", "android", 75000),
    ("spritekit game language:Swift in:name,description", "ios", 75000),
    ("ios game language:Swift in:name,description", "ios", 75000),
    ("cocos2d game language:C++ in:name,description", "native", 120000),
    ("cocos creator game language:TypeScript in:name,description", "native", 120000),
    ("defold game language:Lua in:name,description", "native", 75000),
    ("love2d game language:Lua in:name,description", "native", 75000),
    ("monogame game language:C# in:name,description", "native", 120000),
    ("raylib game language:C++ in:name,description", "native", 120000),
    ("pygame game language:Python in:name,description", "native", 75000),
]
GAME_RELEVANCE = re.compile(r"\b(?:games?|gaming|gamedev|phaser|godot|unity(?:2d|3d)?|cocos2d?|libgdx|love2d|defold|monogame|spritekit|raylib|pygame|pixi(?:js)?|gamepad|arcade|clicker|incremental|idle|plinko|slot|rogueli(?:ke|te)|survivors?|platformer|puzzle|rpg|shooter|metroidvania|mini.?games?|gameplay|level editor|game engine|game framework|gamification)\b", re.I)
UNRELATED = re.compile(r"\b(?:rxjs|devsecops|accessibility|harness engineering|discord quest auto|lottery prediction|bukkit|spigot|minecraft mod|minecraft plugin|bot that automatically plays|world of warcraft fishing bot)\b", re.I)
MECHANICS = {
    "progression/upgrades": re.compile(r"\b(?:incremental|idle|clicker|upgrade|progression|level.?up)\b", re.I),
    "loot/random rewards": re.compile(r"\b(?:loot|drop|gacha|plinko|slot|chest|crate|pack opening)\b", re.I),
    "collecting/discovery": re.compile(r"\b(?:collect|fishing|mining|digging|discover|exploration)\b", re.I),
    "action/movement": re.compile(r"\b(?:shooter|parkour|dash|platformer|survivors?|bullet.?hell|combat)\b", re.I),
    "puzzle/strategy": re.compile(r"\b(?:puzzle|merge|2048|strategy|turn.?based|deckbuilder)\b", re.I),
}
TRACK_ORDER = ("phaser", "browser", "unity", "android", "ios", "native", "godot", "unspecified")


def relevance_reason(repo: dict) -> str | None:
    """Only strong off-topic metadata is skipped; ambiguous projects stay reviewable."""
    name = repo.get("name") or repo.get("full_name") or ""
    description = repo.get("description") or ""
    topics = " ".join(repo.get("topics") or [])
    text = f"{name} {description} {topics}"
    if UNRELATED.search(text) and not re.search(r"\b(?:phaser|godot|unity|cocos2d?|libgdx|defold)\b", topics, re.I):
        return "explicit unrelated software/tutorial/bot; metadata retained for reconsideration"
    if repo.get("discovery_track") == "phaser":
        return None  # Phaser match may be in README only; keep a possible plugin.
    if GAME_RELEVANCE.search(text):
        return None
    if not name.strip() or (not description and not topics):
        return None
    return "no game-development evidence in repository name, description or topics"


def inferred_track(repo: dict) -> str:
    if repo.get("discovery_track") in TRACK_ORDER:
        return repo["discovery_track"]
    text = " ".join((repo.get("name") or "", repo.get("description") or "", " ".join(repo.get("topics") or []))).lower()
    language = (repo.get("language") or "").lower()
    if re.search(r"\bunity(?:2d|3d)?\b", text):
        return "unity"
    if re.search(r"\bphaser\b", text):
        return "phaser"
    if re.search(r"\bgodot\b", text) or language == "gdscript":
        return "godot"
    if re.search(r"\b(?:android|libgdx)\b", text) or language in ("kotlin", "java"):
        return "android"
    if re.search(r"\b(?:ios|spritekit)\b", text) or language == "swift":
        return "ios"
    if any(token in text for token in ("monogame", "love2d", "defold", "raylib", "cocos", "pygame")):
        return "native"
    if language in ("typescript", "javascript", "html"):
        return "browser"
    return "unspecified"


def inspection_order(pending: dict, limit: int) -> list[str]:
    """Round-robin by track so the Phaser backlog cannot starve mobile/native games."""
    queues: dict[str, deque[str]] = defaultdict(deque)
    for key, repo in sorted(pending.items(), key=lambda kv: preliminary(kv[1]), reverse=True):
        queues[inferred_track(repo)].append(key)
    chosen = []
    while len(chosen) < limit and any(queues.values()):
        for track in TRACK_ORDER:
            if queues[track] and len(chosen) < limit:
                chosen.append(queues[track].popleft())
    return chosen


def enrich(item: dict, repo: dict) -> dict:
    """Independent, explicitly unverified mechanics and rewrite-cost hints."""
    track = inferred_track(repo)
    engine = item.get("engine") or "Unknown"
    # A search-query match is weaker evidence than detected files/dependencies.
    # In particular, a TypeScript PixiJS shooter must not be labeled iOS.
    detected_tracks = {"Phaser": "phaser", "PixiJS": "browser", "Browser/JS": "browser",
                       "Three.js": "browser", "Godot": "godot", "Unity": "unity"}
    track = detected_tracks.get(engine, track)
    if engine == "Unknown" and track == "unity" and re.search(r"\bunity(?:2d|3d)?\b", (" ".join(repo.get("topics") or []) + " " + (repo.get("description") or "")), re.I):
        engine = "Unity (metadata only)"
    title = f"{repo.get('name') or ''} {repo.get('description') or ''}"
    mechanics = [tag for tag, pattern in MECHANICS.items() if pattern.search(title)]
    if engine in ("Phaser", "PixiJS", "Browser/JS", "Three.js"):
        effort, reason = "potentially lower", "browser-oriented code; inspect actual dependencies and game scope"
    elif track == "unity" or engine.startswith("Unity"):
        effort, reason = "potentially higher", "Unity runtime and asset pipeline likely require a rewrite for Phaser"
    elif track in ("android", "ios", "native"):
        effort, reason = "potentially higher", "native platform APIs and rendering may require a rewrite"
    elif engine == "Godot" or track == "godot":
        effort, reason = "variable", "Godot supports web export; Phaser rewrite is still separate work"
    else:
        effort, reason = "unknown", "platform and dependency evidence insufficient"
    return {**item, "engine": engine, "discovery_track": track,
            "mechanic_signals": mechanics,
            "idea_review": "mechanic lead; evaluate gameplay" if mechanics else "no specific mechanic inferred; inspect manually",
            "porting_effort_hint": effort, "porting_reason": reason,
            "effort_and_idea_unverified": True}
