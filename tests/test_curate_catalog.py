import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curate_catalog import exclusion_reason, curate


class CatalogCurationTest(unittest.TestCase):
    def test_phaser_plugin_excluded(self):
        self.assertIsNotNone(exclusion_reason({"full_name": "azerion/phaser-ads", "description": "A Phaser plugin for providing nice ads integration"}))

    def test_bootstrap_excluded(self):
        self.assertIsNotNone(exclusion_reason({"full_name": "leandr0ck/phaser-es6-webpack", "description": "A bootstrap project for creating games with Phaser"}))

    def test_server_only_excluded(self):
        self.assertIsNotNone(exclusion_reason({"full_name": "geckosio/phaser-on-nodejs", "description": "Allows you to run Phaser 3 game on Node.js"}))

    def test_multiplayer_backend_excluded(self):
        self.assertIsNotNone(exclusion_reason({"full_name": "jojoee/blocker", "description": "Multiplayer online game using Phaser + WebSocket"}))

    def test_real_game_and_unknown_license_preserved(self):
        self.assertIsNone(exclusion_reason({"full_name": "ganlvtech/phaser-catch-the-cat", "description": "An HTML5 game powered by Phaser 3", "license": "unknown"}))

    def test_csv_html_and_raw_preservation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            entries = [
                {"full_name": "alice/fishing-game", "url": "https://github.com/alice/fishing-game", "description": "Fishing game", "engine": "Phaser", "language": "TypeScript", "size_kb": 300, "stars": 1, "license": "mit", "homepage": "", "reasons": [], "score": 80},
                {"full_name": "alice/my-plugin", "url": "https://github.com/alice/my-plugin", "description": "Phaser plugin", "engine": "Phaser", "language": "TypeScript", "size_kb": 100, "stars": 1, "license": "mit", "homepage": "", "reasons": [], "score": 60},
            ]
            (root / "candidates.json").write_text(json.dumps(entries), encoding="utf-8")
            with (root / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["full_name", "description"])
                writer.writeheader()
                writer.writerows({k: e[k] for k in writer.fieldnames} for e in entries)
            self.assertEqual(curate(root), (1, 1))
            self.assertEqual(len(json.loads((root / "raw_candidates.json").read_text())), 2)
            self.assertEqual(len(json.loads((root / "candidates.json").read_text())), 1)
            self.assertEqual(len(json.loads((root / "excluded.json").read_text())), 1)
            self.assertIn("alice/fishing-game", (root / "index.html").read_text())
            self.assertNotIn("my-plugin", (root / "index.html").read_text())
            with (root / "candidates.csv").open(encoding="utf-8-sig", newline="") as file:
                self.assertEqual(len(list(csv.DictReader(file))), 1)


if __name__ == "__main__":
    unittest.main()
