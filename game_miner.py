#!/usr/bin/env python3
"""Find small public game projects through GitHub's REST API; never execute them."""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com"
API_VERSION = "2022-11-28"
SEARCHES = [
    "topic:phaser game language:TypeScript",
    "topic:phaser game language:JavaScript",
    "phaser incremental game in:name,description,readme",
    "phaser fishing game in:name,description,readme",
    "phaser mining game in:name,description,readme",
    "phaser arcade game in:name,description,readme",
    "html5 idle game language:JavaScript in:name,description,readme",
    "clicker game language:TypeScript in:name,description,readme",
    "browser game language:TypeScript in:name,description,readme",
    "topic:godot-game language:GDScript",
    "godot incremental game in:name,description,readme",
]
PERMISSIVE = {"mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc", "0bsd", "unlicense", "cc0-1.0", "zlib"}
GAME_WORDS = re.compile(r"\b(game|games|arcade|idle|clicker|incremental|fishing|mining|shooter|survivor|platformer|puzzle|roguelike|collect|simulator)\b", re.I)
FRAMEWORK_WORDS = re.compile(r"\b(engine|framework|boilerplate|template|awesome|tutorials|examples|collection|library|starter)\b", re.I)
REPO_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class GitHub:
    def __init__(self, token: str | None = None, cache_dir: Path | None = None, refresh: bool = False):
        self.token = token
        self.cache_dir = cache_dir or Path(".github-cache")
        self.refresh = refresh
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.last_search = 0.0

    def get(self, route: str, params: dict | None = None) -> dict:
        url = API + route + ("?" + urlencode(params) if params else "")
        cache_file = self.cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")
        if not self.refresh and cache_file.exists() and time.time() - cache_file.stat().st_mtime < 12 * 3600:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        if route.startswith("/search/"):
            delay = 2.2 if self.token else 6.5
            time.sleep(max(0.0, delay - (time.monotonic() - self.last_search)))
            self.last_search = time.monotonic()
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "game-miner-cli", "X-GitHub-Api-Version": API_VERSION}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        for attempt in range(3):
            try:
                with urlopen(Request(url, headers=headers), timeout=25) as res:
                    data = json.load(res)
                cache_file.write_text(json.dumps(data), encoding="utf-8")
                return data
            except HTTPError as error:
                if error.code in (403, 429) and attempt < 2:
                    retry_after = error.headers.get("Retry-After")
                    remaining = error.headers.get("X-RateLimit-Remaining")
                    if retry_after:
                        wait = min(120, max(1, int(retry_after)))
                    elif remaining == "0":
                        wait = max(1, int(error.headers.get("X-RateLimit-Reset", "0")) - int(time.time()) + 1)
                        if wait > 120:
                            raise RuntimeError(f"GitHub API rate limit; retry in ~{wait}s") from error
                    else:
                        wait = 60 * (attempt + 1)
                    print(f"GitHub HTTP {error.code}; waiting {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                detail = error.read(400).decode("utf-8", "replace")
                raise RuntimeError(f"GitHub API HTTP {error.code} at {route}: {detail}") from error
            except URLError as error:
                if attempt == 2:
                    raise RuntimeError(f"Network error: {error}") from error
                time.sleep(2 ** attempt)
        raise RuntimeError("Unable to retrieve GitHub data")


def preliminary(repo: dict) -> int:
    title = (repo.get("name") or "") + " " + (repo.get("description") or "")
    score = 0
    if GAME_WORDS.search(title):
        score += 20
    if FRAMEWORK_WORDS.search(title):
        score -= 30
    if (repo.get("language") or "").lower() in {"typescript", "javascript", "html", "gdscript"}:
        score += 12
    size = repo.get("size") or 0
    if 20 <= size <= 5000:
        score += 16
    elif size > 30000 or size < 5:
        score -= 20
    if (repo.get("stargazers_count") or 0) >= 2:
        score += 4
    if repo.get("fork") or repo.get("archived") or repo.get("disabled"):
        score -= 50
    if ((repo.get("license") or {}).get("key") or "").lower() in PERMISSIVE:
        score += 8
    return score


def inspect(api: GitHub, repo: dict) -> dict:
    name = repo["full_name"]
    owner, project = name.split("/", 1)
    branch = quote(repo["default_branch"], safe="")
    tree = api.get(f"/repos/{owner}/{project}/git/trees/{branch}", {"recursive": "1"})
    paths = [node.get("path", "") for node in tree.get("tree", []) if node.get("type") == "blob"]
    lower_paths = [p.lower() for p in paths]
    root = {p for p in lower_paths if "/" not in p}
    deps = ""
    if "package.json" in root:
        try:
            package = api.get(f"/repos/{owner}/{project}/contents/package.json")
            if package.get("encoding") == "base64":
                decoded = base64.b64decode(package["content"]).decode("utf-8", "replace")
                parsed = json.loads(decoded)
                deps = " ".join(list(parsed.get("dependencies", {})) + list(parsed.get("devDependencies", {}))).lower()
        except (RuntimeError, ValueError, KeyError, TypeError):
            pass
    engine = "Unknown"
    if "phaser" in deps or any("phaser" in topic for topic in repo.get("topics", [])):
        engine = "Phaser"
    elif "pixi.js" in deps or "pixi.js-legacy" in deps:
        engine = "PixiJS"
    elif "project.godot" in root:
        engine = "Godot"
    elif "unity" in deps or any(p.startswith("assets/") and p.endswith(".unity") for p in lower_paths):
        engine = "Unity"
    elif "three" in deps:
        engine = "Three.js"
    elif "package.json" in root or "index.html" in root:
        engine = "Browser/JS"
    artwork = sum(p.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".aseprite", ".ogg", ".mp3", ".wav")) for p in lower_paths)
    license_key = ((repo.get("license") or {}).get("key") or "unknown").lower()
    license_status = "permissive-code-license; verify full terms and assets" if license_key in PERMISSIVE else "manual-license-review"
    reasons = []
    score = preliminary(repo)
    if engine in ("Phaser", "PixiJS", "Browser/JS"):
        score += 16
        reasons.append("browser-oriented source")
    elif engine == "Godot":
        score += 9
        reasons.append("Godot project; check web export")
    elif engine == "Unity":
        score -= 20
        reasons.append("Unity project; higher adaptation effort")
    else:
        reasons.append("engine not confirmed")
    if artwork:
        score += 6
        reasons.append(f"{artwork} possible media files")
    if any(p.startswith(("dist/", "build/")) for p in lower_paths):
        reasons.append("built files present; source still requires checking")
    if "index.html" in root or "project.godot" in root:
        score += 7
        reasons.append("entry/project file present")
    if "package.json" in root and deps:
        reasons.append("root package manifest readable")
    if tree.get("truncated"):
        score -= 12
        reasons.append("file tree truncated: inspection incomplete")
    if license_key not in PERMISSIVE:
        score -= 15
        reasons.append("license needs manual review")
    if not GAME_WORDS.search((repo.get("name") or "") + " " + (repo.get("description") or "")):
        reasons.append("game status unverified")
    return {
        "full_name": name, "url": repo["html_url"], "description": repo.get("description") or "",
        "engine": engine, "language": repo.get("language") or "Unknown", "license": license_key,
        "license_status": license_status, "assets_status": "unverified",
        "score": score, "size_kb": repo.get("size") or 0,
        "stars": repo.get("stargazers_count") or 0, "last_push": repo.get("pushed_at"),
        "default_branch": repo["default_branch"], "homepage": repo.get("homepage") or "",
        "files_seen": len(paths), "media_files": artwork, "tree_truncated": bool(tree.get("truncated")),
        "reasons": reasons, "review_status": "candidate-only; build, gameplay and legal reuse unverified",
    }


def render_html(items: list[dict]) -> str:
    cards = []
    for item in items:
        url = html.escape(item["url"], quote=True)
        title = html.escape(item["full_name"])
        desc = html.escape(item["description"])
        why = " · ".join(html.escape(reason) for reason in item["reasons"])
        fields = f'{html.escape(item["engine"])} · {html.escape(item["language"])} · {item["size_kb"]:,} KB · {item["stars"]} stars'
        license_tag = html.escape(item["license"])
        demo = item["homepage"]
        demo_link = f' <a href="{html.escape(demo, quote=True)}" target="_blank" rel="noopener noreferrer">Project homepage ↗</a>' if demo.startswith(("https://", "http://")) else ""
        cards.append(f'<article data-search="{html.escape((item["full_name"] + " " + item["description"] + " " + item["engine"]).lower(), quote=True)}">'
                     f'<div class="top"><strong>{title}</strong><span>Fit heuristic: {item["score"]}</span></div>'
                     f'<p>{desc}</p><small>{fields}</small><p><b>Code license: {license_tag}</b> · Assets unverified</p>'
                     f'<p class="why">{why}</p><a href="{url}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>{demo_link}</article>')
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Game Miner candidates</title>
<style>body{font:16px system-ui,sans-serif;background:#10151d;color:#ecf1f7;max-width:1100px;margin:32px auto;padding:0 16px}h1{letter-spacing:-.04em}p{line-height:1.5}input{box-sizing:border-box;width:100%;padding:14px;margin:10px 0 24px;border:1px solid #455065;border-radius:10px;background:#1b2532;color:white;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:14px}article{border:1px solid #324153;background:#1b2532;border-radius:14px;padding:18px;overflow-wrap:anywhere}.top{display:flex;justify-content:space-between;gap:10px}.top span{white-space:nowrap;color:#9bd3bd;font-size:12px}small,.why,.note{color:#aab9cc}a{color:#a4ceff;margin-right:12px}article[hidden]{display:none}</style>
<h1>Game Miner</h1><p class="note">Discovery candidates only. Scores are experimental fit heuristics, not quality or legal clearance. Never run untrusted projects outside an isolated environment. Check code and all asset rights before reuse.</p>
<input id="q" type="search" placeholder="Filter by game, description or engine" aria-label="Filter candidates"><div class="grid">""" + "\n".join(cards) + """</div><script>const q=document.getElementById('q');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>"""


def scan(args: argparse.Namespace) -> None:
    api = GitHub(os.getenv("GITHUB_TOKEN"), Path(args.cache), args.refresh)
    found: dict[int, dict] = {}
    for index, base_query in enumerate(SEARCHES, 1):
        query = f"{base_query} is:public fork:false archived:false size:<30000"
        for page in range(1, args.pages + 1):
            data = api.get("/search/repositories", {"q": query, "per_page": args.per_query, "page": page})
            for repo in data.get("items", []):
                found[repo["id"]] = repo
            print(f"Search {index}/{len(SEARCHES)} page {page}: {len(data.get('items', []))} hits; {len(found)} unique", file=sys.stderr)
            if data.get("incomplete_results"):
                print("WARNING: Search timed out; incomplete_results=true", file=sys.stderr)
            if len(data.get("items", [])) < args.per_query:
                break
    ranked = sorted(found.values(), key=preliminary, reverse=True)
    items = []
    for repo in ranked[:args.inspect]:
        try:
            items.append(inspect(api, repo))
        except RuntimeError as exc:
            print(f"Inspection skipped {repo['full_name']}: {exc}", file=sys.stderr)
    items.sort(key=lambda item: item["score"], reverse=True)
    target = Path(args.output)
    target.mkdir(parents=True, exist_ok=True)
    (target / "candidates.json").write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    with (target / "candidates.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["full_name", "url", "description", "engine", "language", "license", "license_status", "assets_status", "score", "size_kb", "stars", "last_push", "homepage", "review_status"])
        writer.writeheader()
        for item in items:
            writer.writerow({key: item.get(key, "") for key in writer.fieldnames})
    (target / "index.html").write_text(render_html(items), encoding="utf-8")
    print(f"Saved {len(items)} inspected candidates to {target.resolve()}")


def download(args: argparse.Namespace) -> None:
    if not REPO_NAME.fullmatch(args.repo) or args.repo.startswith("-"):
        raise ValueError("Repository must be owner/name")
    api = GitHub(os.getenv("GITHUB_TOKEN"), Path(args.cache), args.refresh)
    owner, project = args.repo.split("/", 1)
    repo = api.get(f"/repos/{owner}/{project}")
    if repo.get("private"):
        raise ValueError("This tool only downloads public repositories")
    branch = quote(repo["default_branch"], safe="")
    commit = api.get(f"/repos/{owner}/{project}/commits/{branch}")["sha"]
    url = f"https://api.github.com/repos/{owner}/{project}/zipball/{commit}"
    request = Request(url, headers={"User-Agent": "game-miner-cli", "Accept": "application/vnd.github+json"})
    dest = Path(args.output)
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / f"{owner}--{project}--{commit[:12]}.zip"
    max_bytes = args.max_mb * 1024 * 1024
    downloaded = 0
    try:
        with urlopen(request, timeout=60) as src, archive.open("wb") as dst:
            while block := src.read(1024 * 1024):
                downloaded += len(block)
                if downloaded > max_bytes:
                    raise ValueError(f"Archive exceeds {args.max_mb} MB cap")
                dst.write(block)
        if archive.read_bytes()[:4] != b"PK\x03\x04":
            raise ValueError("Server did not return a ZIP file")
    except Exception:
        archive.unlink(missing_ok=True)
        raise
    print(f"Saved {archive.resolve()} ({downloaded:,} bytes). No files were executed or extracted.")
    print("Review LICENSE, asset rights, dependencies and scripts before running or distributing.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover public game source code with GitHub REST API")
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("scan", help="Search and create a local candidate catalog")
    search.add_argument("--inspect", type=int, default=40, help="Candidates to inspect (default: 40)")
    search.add_argument("--per-query", type=int, default=30, help="Results per page (1..100)")
    search.add_argument("--pages", type=int, default=1, help="Pages per search (1..10)")
    search.add_argument("--output", default="results")
    search.add_argument("--cache", default=".github-cache")
    search.add_argument("--refresh", action="store_true", help="Ignore 12-hour API cache")
    grab = sub.add_parser("download", help="Download a public repository ZIP pinned to a commit")
    grab.add_argument("repo", help="owner/name")
    grab.add_argument("--output", default="downloads")
    grab.add_argument("--max-mb", type=int, default=100)
    grab.add_argument("--cache", default=".github-cache")
    grab.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.command == "scan":
        if not (1 <= args.per_query <= 100 and 1 <= args.pages <= 10 and 1 <= args.inspect <= 500):
            parser.error("Use --per-query 1..100, --pages 1..10 and --inspect 1..500")
        scan(args)
    else:
        if not 1 <= args.max_mb <= 1000:
            parser.error("Use --max-mb 1..1000")
        download(args)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, URLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
