"""Regression tests for search depth and cursor/page-size compatibility."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from incremental_scan import load_registry, run_incremental


class FakeGitHub:
    def __init__(self):
        self.calls = []

    def get(self, route, params=None):
        assert route == "/search/repositories"
        page, per_query = params["page"], params["per_page"]
        self.calls.append((page, per_query))
        # Stable IDs across page-size changes, as in a stable search result.
        return {"items": [make_repo((page - 1) * per_query + i)
                          for i in range(1, per_query + 1)],
                "incomplete_results": False}


def make_repo(number):
    return {"id": number, "full_name": f"alice/game-{number}", "name": f"game-{number}",
            "html_url": f"https://github.com/alice/game-{number}", "description": "Phaser game",
            "language": "JavaScript", "size": 150, "stargazers_count": 2,
            "fork": False, "archived": False, "disabled": False, "license": {"key": "mit"},
            "topics": ["phaser"], "default_branch": "main", "homepage": "", "pushed_at": "2026-01-01"}


def inspected(repo):
    return {"full_name": repo["full_name"], "url": repo["html_url"],
            "description": repo["description"], "engine": "Phaser", "language": "JavaScript",
            "license": "mit", "license_status": "manual", "assets_status": "unverified",
            "score": 75, "size_kb": 150, "stars": 2, "last_push": "2026-01-01",
            "homepage": "", "reasons": [], "review_status": "candidate"}


class SearchCursorTests(unittest.TestCase):
    def args(self, root, per_query, inspect=20):
        return SimpleNamespace(registry=str(root / "registry.json"), output=str(root / "results"),
                               cache=str(root / "cache"), inspect=inspect, per_query=per_query, pages=1)

    def test_reaches_page_eleven_without_wrapping_at_ten(self):
        with TemporaryDirectory() as directory:
            root, api = Path(directory), FakeGitHub()
            args = self.args(root, per_query=1, inspect=1)
            with patch("incremental_scan.inspect", side_effect=lambda api, value: inspected(value)):
                for _ in range(11):
                    run_incremental(args, api=api, searches=["phaser incremental game"])
            self.assertEqual(api.calls, [(i, 1) for i in range(1, 12)])
            self.assertEqual(len(load_registry(Path(args.registry))["seen"]), 11)
            query_stats = json.loads((root / "results" / "search_query_stats.json").read_text())
            self.assertEqual(query_stats[0]["new_unique_queued"], 1)
            self.assertEqual(query_stats[0]["pages_fetched"], 1)

    def test_page_size_change_restarts_safely_without_reinspection(self):
        with TemporaryDirectory() as directory:
            root, api = Path(directory), FakeGitHub()
            args = self.args(root, per_query=2)
            with patch("incremental_scan.inspect", side_effect=lambda api, value: inspected(value)) as fake_inspect:
                run_incremental(args, api=api, searches=["phaser incremental game"])
                args.per_query = 3
                run_incremental(args, api=api, searches=["phaser incremental game"])
            self.assertEqual(api.calls, [(1, 2), (1, 3)])
            self.assertEqual(fake_inspect.call_count, 3)
            state = load_registry(Path(args.registry))
            self.assertEqual(len(state["seen"]), 3)
            self.assertEqual(state["query_page_sizes"]["phaser incremental game"], 3)
            query_stats = json.loads((root / "results" / "search_query_stats.json").read_text())
            self.assertEqual(query_stats[0]["already_inspected_hits"], 2)
            self.assertEqual(query_stats[0]["new_unique_queued"], 1)

    def test_legacy_registry_without_page_size_is_restarted_safely(self):
        with TemporaryDirectory() as directory:
            root, api = Path(directory), FakeGitHub()
            args = self.args(root, per_query=4)
            root.joinpath("registry.json").write_text(json.dumps({
                "version": 1, "seen": {}, "pending": {},
                "query_cursors": {"phaser incremental game": 7}, "irrelevant": {}}))
            with patch("incremental_scan.inspect", side_effect=lambda api, value: inspected(value)):
                run_incremental(args, api=api, searches=["phaser incremental game"])
            self.assertEqual(api.calls, [(1, 4)])
            self.assertEqual(load_registry(Path(args.registry))["query_page_sizes"]["phaser incremental game"], 4)


if __name__ == "__main__":
    unittest.main()
