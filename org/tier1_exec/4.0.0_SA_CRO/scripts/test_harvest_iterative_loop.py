"""Offline regression checks for input handling and the measured-success gate."""

import io
import json
import unittest
from unittest.mock import MagicMock, Mock, patch
from PIL import Image
import harvest_iterative_loop as loop
import press_and_hold_lib as hold


class HoldRegression(unittest.TestCase):
    def test_checkmark_releases_mouse(self):
        png = io.BytesIO()
        Image.new("RGB", (40, 20)).save(png, format="PNG")
        page = Mock()
        page.screenshot.return_value = png.getvalue()
        with (
            patch.object(hold, "_crop_scores", side_effect=[(10, 5), (20, 30)]),
            patch.object(hold.time, "sleep"),
        ):
            hold.press_and_hold_adaptive(
                page,
                20,
                10,
                {"x": 0, "y": 0, "width": 40, "height": 20},
                lambda message: None,
            )
        self.assertEqual(page.mouse.down.call_count, 1)
        self.assertEqual(page.mouse.up.call_count, 1)

    def test_gradual_drain_releases_and_represses(self):
        png = io.BytesIO()
        Image.new("RGB", (40, 20)).save(png, format="PNG")
        page = Mock()
        page.screenshot.return_value = png.getvalue()
        ticks = iter(i / 10 for i in range(100))
        with (
            patch.object(
                hold,
                "_crop_scores",
                side_effect=[
                    (5, 0),
                    (20, 0),
                    (30, 0),
                    (27, 0),
                    (24, 0),
                    (5, 0),
                    (5, 0),
                    (5, 0),
                ],
            ),
            patch.object(hold.time, "sleep"),
            patch.object(hold.time, "monotonic", side_effect=lambda: next(ticks)),
            patch.object(hold, "Path", return_value=MagicMock()),
        ):
            hold.press_and_hold_adaptive(
                page,
                20,
                10,
                {"x": 0, "y": 0, "width": 40, "height": 20},
                lambda message: None,
                max_hold_s=1.5,
                trace_dir="unused-mocked",
                release_on_pixel_peak=False,
            )
        self.assertEqual(page.mouse.down.call_count, 2)
        self.assertEqual(page.mouse.up.call_count, 2)


class SuccessGate(unittest.TestCase):
    def fixture(self, tickers=("BA", "COST", "HD")):
        rows = []
        reviews = {}
        for n, ticker in enumerate(tickers, 1):
            row = {"round": n, "ticker": ticker, "results": {}}
            for pub in loop.ORDER:
                attempts = []
                for i in range(5):
                    key = f"{n}/{pub}/{i}"
                    digest = f"hash-{n}-{pub}-{i}"
                    attempts.append(
                        {
                            "review_key": key,
                            "url": f"https://example.test/{key}",
                            "body_sha256": digest,
                            "content_status": "candidate",
                        }
                    )
                    reviews[key] = {
                        "complete": True,
                        "relevant": True,
                        "body_sha256": digest,
                    }
                row["results"][pub] = {"attempts": attempts}
            rows.append(row)
        return {"rounds": rows}, reviews

    def reconcile(self, state, reviews):
        out = Mock()
        path = Mock()
        out.__truediv__ = Mock(return_value=path)
        path.__truediv__ = Mock(return_value=path)
        path.exists.return_value = True
        path.read_text.return_value = json.dumps(reviews)
        with patch.object(loop, "write"):
            return loop.reconcile(state, out)

    def test_three_distinct_tickers_pass(self):
        state, reviews = self.fixture()
        result = self.reconcile(state, reviews)
        self.assertTrue(result["target_measured"])
        self.assertEqual(result["joint_streak"], 3)

    def test_unreviewed_body_does_not_count(self):
        state, reviews = self.fixture()
        reviews.pop("3/sa/0")
        result = self.reconcile(state, reviews)
        self.assertFalse(result["target_measured"])
        self.assertEqual(result["streaks"]["sa"], 0)
        self.assertEqual(result["streaks"]["ft"], 3)

    def test_changed_body_invalidates_review(self):
        state, reviews = self.fixture()
        reviews["3/sa/0"]["body_sha256"] = "stale"
        self.assertFalse(self.reconcile(state, reviews)["target_measured"])

    def test_duplicate_body_cannot_supply_fifth_article(self):
        state, reviews = self.fixture()
        a = state["rounds"][-1]["results"]["sa"]["attempts"]
        a[4]["body_sha256"] = a[3]["body_sha256"]
        reviews["3/sa/4"]["body_sha256"] = a[3]["body_sha256"]
        self.assertFalse(self.reconcile(state, reviews)["target_measured"])

    def test_repeating_ticker_is_not_three_different_tickers(self):
        state, reviews = self.fixture(("BA", "COST", "BA"))
        self.assertFalse(self.reconcile(state, reviews)["target_measured"])

    def test_publishers_can_qualify_in_different_consecutive_windows(self):
        state, reviews = self.fixture(("BA", "COST", "HD", "INTU", "VLO"))
        for pub, failed_rounds in {
            "sa": [1, 2],
            "ft": [4, 5],
            "wsj": [1, 5],
            "bbg": [1, 2],
        }.items():
            for n in failed_rounds:
                reviews.pop(f"{n}/{pub}/0")
        result = self.reconcile(state, reviews)
        self.assertTrue(result["target_measured"])
        self.assertEqual(result["joint_streak"], 0)


if __name__ == "__main__":
    unittest.main()
