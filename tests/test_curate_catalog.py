import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curate_catalog import classify, curate, exclusion_reason


class CatalogCurationTest(unittest.TestCase):
    def test_phaser_plugins_retained(self):
        for name, desc in [
            ("azerion/phaser-ads", "A Phaser plugin for providing nice ads integration"),
            ("azerion/phaser-web-workers", "A simple Phaser plugin that allows you to easily integrate Web Workers"),
            ("geckosio/phaser-on-nodejs", "Allows you to run Phaser 3 game on Node.js"),
            ("littlee/wechat-small-game-phaser", "make phaser works with wechat small game"),
        ]:
            self.assertEqual(classify({"full_name": name, "description": desc})[0], "tool")
            self.assertIsNone(exclusion_reason({"full_name": name, "description": desc}))

    def test_starter_retained(self):
        self.assertEqual(classify({"full_name": "leandr0ck/phaser-es6-webpack", "description": "A bootstrap project for creating games with Phaser"})[0], "starter")

    def test_complex_games_and_unrelated_retained(self):
        self.assertEqual(classify({"full_name": "jojoee/blocker", "description": "Multiplayer online game using Phaser + WebSocket"})[0], "complex_game")
        self.assertEqual(classify({"full_name": "wokwi/avr8js", "description": "Arduino simulator"})[0], "other")
        self.assertEqual(classify({"full_name": "ganlvtech/phaser-catch-the-cat", "description": "An HTML5 game powered by Phaser 3"})[0], "game")

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
            self.assertEqual(curate(root), (2, 0))
            self.assertEqual(len(json.loads((root / "raw_candidates.json").read_text())), 2)
            self.assertEqual(len(json.loads((root / "candidates.json").read_text())), 2)
            self.assertEqual(json.loads((root / "excluded.json").read_text()), [])
            self.assertEqual(len(json.loads((root / "tool.json").read_text())), 1)
            self.assertIn("alice/fishing-game", (root / "index.html").read_text())
            self.assertIn("alice/my-plugin", (root / "index.html").read_text())
            self.assertIn("my-plugin", (root / "tool.html").read_text())
            self.assertIn('href="tool.html"', (root / "index.html").read_text())
            with (root / "candidates.csv").open(encoding="utf-8-sig", newline="") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 2)
            self.assertEqual({row["category"] for row in rows}, {"game", "tool"})


if __name__ == "__main__":
    unittest.main()
