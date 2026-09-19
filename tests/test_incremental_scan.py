import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from incremental_scan import load_registry, run_incremental


class FakeGitHub:
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def get(self, route, params=None):
        assert route == "/search/repositories"
        page = params["page"]
        self.calls.append(page)
        return {"items": self.pages.get(page, []), "incomplete_results": False}


def repo(id, name):
    return {"id": id, "full_name": f"alice/{name}", "name": name, "html_url": f"https://github.com/alice/{name}",
            "description": "Phaser game", "language": "JavaScript", "size": 150, "stargazers_count": 2,
            "fork": False, "archived": False, "disabled": False, "license": {"key": "mit"},
            "topics": ["phaser"], "default_branch": "main", "homepage": "", "pushed_at": "2026-01-01"}


def inspected(value):
    return {"full_name": value["full_name"], "url": value["html_url"], "description": value["description"],
            "engine": "Phaser", "language": "JavaScript", "license": "mit", "license_status": "manual",
            "assets_status": "unverified", "score": 75, "size_kb": 150, "stars": 2,
            "last_push": "2026-01-01", "homepage": "", "reasons": [], "review_status": "candidate"}


class IncrementalScanTests(unittest.TestCase):
    def test_next_run_advances_page_and_never_reinspects_seen_ids(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            args = SimpleNamespace(registry=str(root / "data" / "registry.json"), output=str(root / "results"),
                                   cache=str(root / "cache"), inspect=2, per_query=2, pages=1)
            api = FakeGitHub({1: [repo(1, "game-a"), repo(2, "game-b")], 2: [repo(2, "game-b"), repo(3, "phaser-plugin")]})
            inspected_names = []
            def fake_inspect(api, value):
                inspected_names.append(value["full_name"])
                return inspected(value)
            with patch("incremental_scan.inspect", side_effect=fake_inspect):
                first = run_incremental(args, api=api, searches=["phaser game"])
                self.assertEqual(first["newly_inspected"], 2)
                second = run_incremental(args, api=api, searches=["phaser game"])
            self.assertEqual(api.calls, [1, 2])
            self.assertEqual(inspected_names, ["alice/game-a", "alice/game-b", "alice/phaser-plugin"])
            self.assertEqual(second["newly_inspected"], 1)
            self.assertEqual(second["total_catalog"], 3)
            state = load_registry(Path(args.registry))
            self.assertEqual(len(state["seen"]), 3)
            self.assertEqual(state["query_cursors"]["phaser game"], 3)
            new = json.loads((root / "results" / "new.json").read_text())
            self.assertEqual([item["full_name"] for item in new], ["alice/phaser-plugin"])
            self.assertEqual(new[0]["category"], "tool")
            self.assertEqual(len(json.loads((root / "results" / "candidates.json").read_text())), 3)

    def test_pending_survives_inspection_budget_and_new_can_be_empty(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            args = SimpleNamespace(registry=str(root / "state.json"), output=str(root / "results"),
                                   cache=str(root / "cache"), inspect=1, per_query=3, pages=1)
            api = FakeGitHub({1: [repo(1, "game-a"), repo(2, "game-b"), repo(3, "game-c")]})
            with patch("incremental_scan.inspect", side_effect=lambda api, value: inspected(value)) as patched:
                a = run_incremental(args, api=api, searches=["phaser game"])
                b = run_incremental(args, api=api, searches=[])
                c = run_incremental(args, api=api, searches=[])
                d = run_incremental(args, api=api, searches=[])
            self.assertEqual((a["pending"], b["pending"], c["pending"], d["pending"]), (2, 1, 0, 0))
            self.assertEqual(d["newly_inspected"], 0)
            self.assertEqual(patched.call_count, 3)
            self.assertEqual(json.loads((root / "results" / "new.json").read_text()), [])
            self.assertEqual(d["total_catalog"], 3)

    def test_bad_registry_refused(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "state.json"
            path.write_text('{"version": 4, "seen": {}, "pending": {}, "query_cursors": {}}')
            with self.assertRaises(ValueError):
                load_registry(path)


if __name__ == "__main__":
    unittest.main()
