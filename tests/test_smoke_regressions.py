import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from curate_catalog import classify
from discovery_policy import inferred_track, relevance_reason
from incremental_scan import run_incremental, load_registry


class SmokeRegressions(unittest.TestCase):
    def test_names_do_not_infer_ios_or_unity_by_substring(self):
        self.assertEqual(inferred_track({"name": "TOSIOS", "description": "browser shooter", "language": "TypeScript"}), "browser")
        self.assertEqual(inferred_track({"name": "community-game", "description": "a browser game", "language": "TypeScript"}), "browser")

    def test_fivem_minigames_and_readme_only_phaser_tools_survive(self):
        self.assertIsNone(relevance_reason({"name": "eye_minigames", "description": "70 FiveM minigames", "topics": []}))
        self.assertIsNone(relevance_reason({"name": "camera-helper", "description": "Camera helpers", "topics": [], "discovery_track": "phaser"}))
        self.assertEqual(classify({"full_name": "britzl/defold-input", "description": "Simplify input mapping and gesture detection"})[0], "tool")

    def test_previous_scan_state_is_corrected_and_irrelevant_lead_restored(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_item = {"full_name": "halftheopposite/TOSIOS", "url": "https://github.com/halftheopposite/TOSIOS",
                        "description": "Browser shooter", "engine": "PixiJS", "language": "TypeScript",
                        "license": "mit", "size_kb": 100, "stars": 2, "homepage": "", "reasons": [],
                        "score": 5, "discovery_track": "ios"}
            mini_repo = {"id": 55, "full_name": "invalid0190/eye_minigames", "name": "eye_minigames",
                         "html_url": "https://github.com/invalid0190/eye_minigames", "description": "70 FiveM minigames",
                         "language": "Lua", "topics": [], "size": 100, "stargazers_count": 1,
                         "license": None, "default_branch": "main", "homepage": "", "pushed_at": ""}
            registry = root / "registry.json"
            registry.write_text(json.dumps({"version": 1, "seen": {"22": {"item": old_item}}, "pending": {},
                                            "query_cursors": {}, "irrelevant": {"55": {"repo": mini_repo, "reason": "old rule"}}}))
            args = SimpleNamespace(registry=str(registry), output=str(root / "results"),
                                   cache=str(root / "cache"), inspect=1, per_query=5, pages=1)
            def fake_inspect(api, repo):
                return {**old_item, "full_name": repo["full_name"], "url": repo["html_url"],
                        "description": repo["description"], "engine": "Unknown"}
            with patch("incremental_scan.inspect", side_effect=fake_inspect):
                stats = run_incremental(args, api=object(), searches=[])
            state = load_registry(registry)
            self.assertEqual(stats["irrelevant_restored"], 1)
            self.assertEqual(stats["irrelevant_total"], 0)
            self.assertEqual(state["seen"]["22"]["item"]["discovery_track"], "browser")
            self.assertEqual(stats["total_catalog"], 2)


if __name__ == "__main__":
    unittest.main()
