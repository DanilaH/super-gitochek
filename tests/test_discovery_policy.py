import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from discovery_policy import SEARCH_TRACKS, enrich, inspection_order, relevance_reason
from incremental_scan import load_registry, run_incremental


def repo(identifier, name, description, *, language="JavaScript", topics=(), track=None, size=150):
    result = {
        "id": identifier, "full_name": f"user/{name}", "name": name,
        "html_url": f"https://github.com/user/{name}", "description": description,
        "language": language, "size": size, "stargazers_count": 1,
        "fork": False, "archived": False, "disabled": False,
        "license": {"key": "mit"}, "topics": list(topics),
        "default_branch": "main", "homepage": "", "pushed_at": "2026-09-01",
    }
    if track:
        result["discovery_track"] = track
    return result


def inspected(candidate):
    return {"full_name": candidate["full_name"], "url": candidate["html_url"],
            "description": candidate["description"], "engine": "Unknown",
            "language": candidate["language"], "license": "mit", "license_status": "manual",
            "assets_status": "unverified", "score": 10, "size_kb": candidate["size"], "stars": 1,
            "last_push": "", "homepage": "", "reasons": [], "review_status": "candidate"}


class FakeGitHub:
    def get(self, route, params=None):
        return {"items": [], "incomplete_results": False}


class DiscoveryPolicyTests(unittest.TestCase):
    def test_existing_queries_retained_and_native_search_uses_bigger_limits(self):
        from game_miner import SEARCHES
        self.assertEqual([q for q, _, _ in SEARCH_TRACKS[:len(SEARCHES)]], SEARCHES)
        self.assertTrue(any(track == "unity" and budget >= 200000 for _, track, budget in SEARCH_TRACKS))
        self.assertTrue(any("spritekit" in query and track == "ios" for query, track, _ in SEARCH_TRACKS))
        self.assertTrue({"unity", "android", "ios", "native", "phaser"}.issubset({track for _, track, _ in SEARCH_TRACKS}))

    def test_precheck_skips_noise_but_preserves_plugins_and_tutorials(self):
        self.assertIsNotNone(relevance_reason(repo(1, "learn-rxjs", "Clear examples of RxJS")))
        self.assertIsNotNone(relevance_reason(repo(2, "desloppify", "Agent harness for code")))
        self.assertIsNone(relevance_reason(repo(3, "phaser-web-workers", "Phaser plugin with web workers")))
        self.assertIsNone(relevance_reason(repo(4, "unity-2d", "", language="C#", topics=["unity2d"])))
        self.assertIsNone(relevance_reason(repo(5, "a-game", "", topics=[])))
        self.assertIsNone(relevance_reason(repo(6, "learn-phaser", "Phaser tutorial")))

    def test_idea_and_rewrite_hints_are_independent_and_unverified(self):
        unity = repo(1, "fishing-game", "Unity fishing and loot game", language="C#", track="unity")
        result = enrich(inspected(unity), unity)
        self.assertEqual(result["porting_effort_hint"], "potentially higher")
        self.assertIn("loot/random rewards", result["mechanic_signals"])
        self.assertIn("collecting/discovery", result["mechanic_signals"])
        self.assertTrue(result["effort_and_idea_unverified"])
        self.assertEqual(result["engine"], "Unity (metadata only)")
        browser = repo(2, "phaser-mining", "Mining game", topics=["phaser"])
        self.assertEqual(enrich({**inspected(browser), "engine": "Phaser"}, browser)["porting_effort_hint"], "potentially lower")

    def test_native_projects_not_starved_by_existing_phaser_queue(self):
        pending = {str(i): repo(i, f"phaser-game-{i}", "Phaser game", topics=["phaser"], track="phaser") for i in range(10)}
        pending["99"] = repo(99, "native-plinko", "Plinko game", language="Swift", track="ios")
        pending["100"] = repo(100, "unity-game", "Unity game", language="C#", track="unity")
        selected = inspection_order(pending, 4)
        self.assertIn("99", selected)
        self.assertIn("100", selected)

    def test_old_registry_migrates_without_losing_queue_or_cursors(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.json"
            registry.write_text(json.dumps({"version": 1, "seen": {}, "pending": {
                "1": repo(1, "learn-rxjs", "RxJS tutorial"),
                "2": repo(2, "phaser-tool", "Phaser plugin", topics=["phaser"]),
            }, "query_cursors": {"old query": 4}}))
            args = SimpleNamespace(registry=str(registry), output=str(root / "results"),
                                   cache=str(root / "cache"), inspect=2, per_query=5, pages=1)
            with patch("incremental_scan.inspect", side_effect=lambda api, value: inspected(value)) as spy:
                stats = run_incremental(args, api=FakeGitHub(), searches=[])
            self.assertEqual(spy.call_count, 1)
            self.assertEqual(stats["irrelevant_total"], 1)
            self.assertEqual(stats["total_catalog"], 1)
            state = load_registry(registry)
            self.assertIn("1", state["irrelevant"])
            self.assertEqual(state["query_cursors"]["old query"], 4)
            self.assertIn("phaser-tool", (root / "results" / "new.html").read_text())
            self.assertTrue((root / "results" / "phaser.html").exists())


if __name__ == "__main__":
    unittest.main()
