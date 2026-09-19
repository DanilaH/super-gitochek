# GitHub Game Miner

Discover small public game repositories for study and adaptation. Results are **unverified candidates**, not proof that a game runs or that any code/assets may be republished.

## GitHub Actions: run a scan

Open **[Actions → Game Miner](https://github.com/DanilaH/super-gitochek/actions/workflows/game-miner.yml) → Run workflow**, choose the `main` branch and start with `inspect=30`, `per_query=30`, `pages=1`. On completion, open that run and download its `game-miner-catalog` artifact. Unzip and open `index.html` locally to browse the catalog.

The artifact contains `candidates.json`, `candidates.csv`, and `index.html`, plus `raw_candidates.json` (all inspected candidates before curation) and `excluded.json` (items filtered out, with reasons). A small heuristic filter removes obvious plugins, templates, hardware simulators, explicitly socket-dependent multiplayer, framework ports and projects tied to NFT/crypto services. Its decisions are reversible via `excluded.json` and should not be treated as definitive.

**Pushes and pull requests run only fast offline tests.** Expensive API scans run only when manually requested, using the workflow's temporary `GITHUB_TOKEN`; no personal access token or custom secret is needed.

## Run locally

Python 3.10+ with no third-party dependencies. Optional `GITHUB_TOKEN` provides higher API limits.

```bash
python3 game_miner.py scan --inspect 30 --per-query 30 --output results
python3 curate_catalog.py results
python3 -m unittest discover -s tests -v
python3 game_miner.py download owner/repository
```

Downloads are commit-pinned ZIP files. This tool never extracts or executes downloaded code. Do not blindly run `npm install` or build scripts from untrusted repositories on your host computer; use an isolated environment after inspection.

## Interpretation and limits

The ranking estimates adaptation fit from GitHub metadata, repository file trees, and the root `package.json`. It does **not** assess actual gameplay, build success, novelty, originality, or market demand. GitHub's license key is only a preliminary hint. A permissive code license may not cover graphics, sound, fonts, logos or bundled third-party content. Review the original licenses and asset provenance before commercial reuse.

Next step: sandboxed build and browser screenshots for selected, manually reviewed projects; keep that pipeline separate from basic discovery.
