# GitHub Game Miner

Find small public game repositories for study, reskin experiments and adaptation. The catalog is a **candidate list**, not a list of confirmed playable games or permission to republish their code and assets.

## Run locally

Python 3.10+; standard library only. Optionally set `GITHUB_TOKEN` in your environment for higher GitHub API limits.

```bash
python3 game_miner.py scan --inspect 30 --per-query 20 --output results
python3 -m unittest discover -s tests -v
python3 game_miner.py download owner/repository
```

Open `results/index.html`; JSON and CSV exports are in the same folder. Downloads are commit-pinned ZIP archives, **never extracted or executed** by the tool.

## GitHub Actions

Open **Actions → Game Miner → Run workflow**. Adjust candidate count and per-query results, then download the `game-miner-catalog` artifact with `index.html`, `candidates.json` and `candidates.csv`. A quick test job runs on pushes and pull requests. The scan uses the workflow's temporary `GITHUB_TOKEN`; you do not need to create a personal access token.

## Important limits

Results are based on GitHub metadata, file trees and the root `package.json`; gameplay and build success are not verified. An open-source code license **does not automatically license graphics, audio, fonts or third-party materials**. Review complete licensing, provenance, trademarks and dependencies before commercial reuse. Never execute third-party build or install scripts directly on your machine without inspecting them; use an isolated environment for future build/playability checks.
