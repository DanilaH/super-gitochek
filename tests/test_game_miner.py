import base64
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from game_miner import GitHub, inspect, preliminary, render_html, scan


class FakeGitHub:
    def get(self, route, params=None):
        if "/git/trees/" in route:
            return {"truncated": False, "tree": [
                {"type": "blob", "path": "package.json"},
                {"type": "blob", "path": "index.html"},
                {"type": "blob", "path": "src/Game.ts"},
                {"type": "blob", "path": "assets/hero.png"},
            ]}
        if "/contents/package.json" in route:
            manifest = json.dumps({"dependencies": {"phaser": "^3.0.0"}}).encode()
            return {"encoding": "base64", "content": base64.b64encode(manifest).decode()}
        raise AssertionError(route)


class GameMinerTest(unittest.TestCase):
    def setUp(self):
        self.repo = {
            "id": 1, "name": "fishing-game", "full_name": "alice/fishing-game",
            "description": "small arcade fishing game", "language": "TypeScript",
            "license": {"key": "mit"}, "size": 400, "stargazers_count": 3,
            "default_branch": "main", "html_url": "https://github.com/alice/fishing-game",
            "topics": ["phaser"], "pushed_at": "2026-09-01T00:00:00Z",
        }

    def test_game_outscores_framework(self):
        library = {**self.repo, "name": "game-engine-template", "description": "game engine framework"}
        self.assertGreater(preliminary(self.repo), preliminary(library))

    def test_detects_engine_and_unverified_assets(self):
        result = inspect(FakeGitHub(), self.repo)
        self.assertEqual(result["engine"], "Phaser")
        self.assertEqual(result["license"], "mit")
        self.assertEqual(result["assets_status"], "unverified")
        self.assertEqual(result["media_files"], 1)

    def test_html_escapes_untrusted_description(self):
        result = inspect(FakeGitHub(), {**self.repo, "description": '<script>alert(1)</script>'})
        page = render_html([result])
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_unknown_license_not_cleared(self):
        result = inspect(FakeGitHub(), {**self.repo, "license": None})
        self.assertEqual(result["license_status"], "manual-license-review")
        self.assertEqual(result["assets_status"], "unverified")

    def test_tree_truncation_reported(self):
        class Truncated(FakeGitHub):
            def get(self, route, params=None):
                if "/git/trees/" in route:
                    return {"truncated": True, "tree": []}
                return super().get(route, params)
        result = inspect(Truncated(), self.repo)
        self.assertTrue(result["tree_truncated"])


if __name__ == "__main__":
    unittest.main()
