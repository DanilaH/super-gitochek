"""Observed regressions from the first cross-engine GitHub Actions scan."""
import unittest

from curate_catalog import classify
from discovery_policy import enrich


class CrossEngineRegressions(unittest.TestCase):
    def test_tosios_is_browser_even_when_github_search_labels_it_ios(self):
        repo = {
            "name": "TOSIOS",
            "full_name": "halftheopposite/TOSIOS",
            "description": "The Open-Source IO Shooter is an open-source multiplayer game in the browser",
            "language": "TypeScript", "topics": ["pixijs", "game", "multiplayer"],
            "discovery_track": "ios",
        }
        item = enrich({"engine": "PixiJS", "full_name": repo["full_name"]}, repo)
        self.assertEqual(item["discovery_track"], "browser")
        self.assertEqual(item["porting_effort_hint"], "potentially lower")

    def test_defold_input_is_a_tool_not_a_complete_game(self):
        item = {
            "full_name": "britzl/defold-input",
            "description": "Simplify input related operations such as gesture detection, input mapping and clicking/dragging game objects",
        }
        self.assertEqual(classify(item)[0], "tool")


if __name__ == "__main__":
    unittest.main()
