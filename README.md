# GitHub Game Miner

Discover public games, Phaser plugins, starters and technical experiments for study. These are **unverified candidates**, not proven playable games or permission to republish code and assets.

## Run in GitHub Actions

Open **[Actions → Game Miner](https://github.com/DanilaH/super-gitochek/actions/workflows/game-miner.yml) → Run workflow** on `main`. Start with `inspect=30`, `per_query=30`, `pages=1`. Download `game-miner-catalog` from the completed run and open `index.html` locally. **Open `new.html` to see only newly inspected projects**; `new.json` and `new.csv` contain the same new-only subset.

### How incremental discovery works

Manual scans preserve `data/discovery-registry.json` in the repository, committed by GitHub Actions. It keeps GitHub repository IDs (stable across renames), all inspected catalog entries, a pending queue and the next search page for each query. Each scan advances its search pages, skips inspection of previously seen IDs, and inspects up to `inspect` new candidates from the queue. Uninspected candidates are not discarded. The full catalog accumulates across runs, including plugins, starters and games with extra dependencies. `results/scan_stats.json` reports new inspections, pending candidates and already-inspected search hits.

The first incremental run initializes the registry and may rediscover projects in earlier, pre-registry artifacts once. Thereafter previously inspected IDs are skipped. This prevents repeating the **expensive inspection**, not all GitHub search requests: search pages still need to be fetched to discover new results. The page cursor is best-effort because GitHub search rankings change. Previously inspected projects are **not automatically re-inspected after updates**; that can be added later.

The registry is versioned and persists independently of GitHub's temporary Actions caches and 7-day downloadable artifacts. If Actions cannot push to `main`, check the repository's Actions workflow token write permissions and branch protection; the scan job requires `contents: write`. Pushes and pull requests run only offline tests, not the API scan.

## Run locally

Python 3.10+, standard library only. Set `GITHUB_TOKEN` for higher API limits, if available.

```bash
python3 incremental_scan.py --inspect 30 --per-query 30 --registry data/discovery-registry.json --output results
python3 -m unittest discover -s tests -v
python3 game_miner.py download owner/repository
```

The original `game_miner.py scan` is still available for standalone, non-incremental experiments; its 12-hour HTTP cache lives under `.github-cache/` and is **not** the persistent seen registry. Downloads are commit-pinned ZIP archives and are never extracted or executed automatically.

## Catalog and safety

The artifact includes cumulative `candidates.json`, `candidates.csv` and `index.html`, plus `new.*`, `scan_stats.json`, `raw_candidates.json`, and category pages for games, tools/plugins, starters, games with external dependencies and other discoveries. All candidates are preserved, with heuristic labels rather than deleted.

Metadata and file-tree inspection do not verify gameplay, build success, originality, licenses or commercial viability. GitHub's code license does not necessarily cover graphics, audio, fonts, trademarks or third-party assets. Review provenance and licenses before any reuse, and inspect untrusted install/build scripts in an isolated environment.
