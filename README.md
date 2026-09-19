# GitHub Game Miner

Find public games **and** Phaser plugins, tools, templates, and experiments for studying mechanics. Unity, Android, iOS, and native desktop projects are valid leads even when porting them to Phaser would require a rewrite. Discoveries are **not verified builds, playable games, or permission to republish code or assets**.

## Run in GitHub Actions

Open [Actions → Game Miner](https://github.com/DanilaH/super-gitochek/actions/workflows/game-miner.yml) → **Run workflow** on `main`; start with `inspect=30`, `per_query=30`, `pages=1`. Download the `game-miner-catalog` artifact from the completed run. Open `index.html` for all inspected projects and `new.html` for only the projects inspected in that run. `new.json` and `new.csv` contain the same subset. **Pushes and pull requests run tests only; they do not trigger a costly GitHub search.**

### Search breadth, queue and cache

The original Phaser/browser/Godot searches remain, with their existing pagination cursors intact. Additional searches cover **Phaser plugins; Unity 2D/C#; Android Kotlin and Java/libGDX; iOS Swift/SpriteKit; Cocos, Defold, LÖVE, MonoGame, raylib, and Pygame**. GitHub repository `size` is in KB: Unity searches allow up to 200,000 KB, whereas the old browser queries retain their 30,000 KB cap. These are search bounds, not download or build operations; very large repos or unindexed projects may still be missed.

`data/discovery-registry.json` persists GitHub IDs, previously inspected entries, queued candidates, and each query's next page. Searches can overlap, but an ID is not inspected twice. The inspection budget is shared round-robin across Phaser, browser, Unity, Android, iOS, native and Godot leads so a large Phaser backlog does not starve new platforms. Failed inspections remain queued. Previously inspected repos are not automatically refreshed on new commits; GitHub search pagination is best-effort because rankings can change.

To avoid spending inspection API calls on unrelated hits, a **conservative metadata-only precheck** moves clear non-game results (for example, an RxJS tutorial or unrelated automation bot) into `irrelevant.json` and the registry's reversible `irrelevant` map. It does not delete them. Ambiguous titles, game tutorials, Phaser plugins and other game-development tools remain eligible. This is a heuristic and can make mistakes; move a false positive back from `irrelevant` to `pending` in the registry if needed.

### How to read the findings

The catalog preserves category pages (`game.html`, `tool.html`, `starter.html`, `complex_game.html`, `other.html`) and adds separate platform pages (`phaser.html`, `unity.html`, `android.html`, `ios.html`, `native.html`, etc.). Each new finding has **two separate, unverified signals**: `mechanic_signals` / `idea_review` from repository names and descriptions, and `porting_effort_hint` / `porting_reason` from engine or platform clues. These are *not* gameplay quality scores or reliable development estimates. A Unity project can be interesting as a mechanic reference yet costly to port. Existing `score` is the older browser-adaptation heuristic, so do not treat it as an idea-quality rank.

`scan_stats.json` reports newly inspected and queued projects and prefiltered unrelated items. All inspected games, plugins, starters and complex projects remain in the cumulative catalog. The artifact also contains `irrelevant.json` for reconsideration. GitHub Actions commits the persistent registry to `main` after a successful scan; if this fails, check Actions token write permissions and branch protection. Artifacts expire after seven days but the registry remains committed.

## Local usage

Requires Python 3.10+ and the standard library. Optional `GITHUB_TOKEN` provides higher GitHub API limits.

```bash
python3 incremental_scan.py --inspect 30 --per-query 30 --registry data/discovery-registry.json --output results
python3 -m unittest discover -s tests -v
python3 game_miner.py download owner/repository
```

The standalone `game_miner.py scan` retains its older browser-focused search behavior; use `incremental_scan.py` for the expanded platform search and persistent registry. Downloads are commit-pinned ZIPs and are **never extracted or executed automatically**. Before adapting or commercially releasing any project, verify the actual license text, graphics/audio/font rights, trademarks, asset provenance, build scripts and real gameplay in an isolated environment. Discovery alone says nothing about commercial demand.
