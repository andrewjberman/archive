"""Regressions for the actual session handoff and previously contaminated bodies."""

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ft_rest_fetch as ft
import harvest_rest_loop as loop
import sa_rest_fetch as sa
import wsj_rest_fetch as wsj


class RestContractTests(unittest.TestCase):
    def test_fresh_sa_bundle_does_not_read_parked_session(self):
        bundle = {
            "captured_at": "test",
            "all_cookies": [
                {
                    "name": "user_id",
                    "value": "synthetic-test-value",
                    "domain": ".seekingalpha.com",
                }
            ],
        }
        with patch.object(
            sa, "_secret", side_effect=AssertionError("unexpected secret read")
        ):
            session, captured = sa.build_session(use_proxy=False, bundle=bundle)
            self.assertEqual(captured, "test")
            self.assertEqual(session.cookies.get("user_id"), "synthetic-test-value")
            session.close()

    def test_ft_nested_byline_does_not_truncate_article(self):
        html = '<title>Example</title><div data-component="article-body"><div><div>Byline</div></div>'
        html += '<article data-component="article-content-body"><p>First paragraph.</p><p>Second paragraph.</p>'
        html += "<script>privateNoise()</script><style>badCSS</style></article></div>"
        article = ft.parse_article(html, "test")
        self.assertEqual(article["text"], "First paragraph.\n\nSecond paragraph.")

    def test_ft_subscription_shell_is_not_an_article(self):
        with self.assertRaises(ft.ReHarvestRequired):
            ft.parse_article(
                "<title>Article</title><p>Subscribe</p><script>hugePayload</script>",
                "test",
            )

    def test_wsj_nested_css_and_outside_paragraphs_are_excluded(self):
        article = wsj.parse_article(
            '<p>Navigation noise</p><article><div class="crawler"><section>'
            "<p>Real text<style>long CSS text</style></p></section></div></article>",
            "test",
        )
        self.assertEqual(article["text"], "Real text")
        self.assertEqual(article["completeness"], "requires_review")

    def test_sa_related_links_do_not_invent_relevance(self):
        article = loop.clean_sa(
            {
                "attributes": {
                    "content": '<p>Unrelated story.</p><div id="more-links"><p>Boeing</p></div>'
                }
            }
        )
        self.assertNotIn("Boeing", article["text"])

    def test_changed_saved_body_cannot_pass_old_review(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            attempts, reviews = [], {}
            for i in range(5):
                key = f"article-{i}.json"
                digest = hashlib.sha256(f"original {i}".encode()).hexdigest()
                attempts.append(
                    {
                        "review_key": key,
                        "content_status": "candidate",
                        "url": key,
                        "body_sha256": digest,
                    }
                )
                reviews[key] = {
                    "complete": True,
                    "relevant": True,
                    "body_sha256": digest,
                }
                loop.write(out / key, {"text": f"changed {i}"})
            loop.write(out / "review.json", reviews)
            state = {
                "rounds": [
                    {
                        "round": 1,
                        "ticker": "BA",
                        "results": {"sa": {"attempts": attempts}},
                    }
                ]
            }
            loop.reconcile(state, out)
            self.assertFalse(state["rounds"][0]["results"]["sa"]["passed"])
            self.assertFalse(state["target_measured"])


if __name__ == "__main__":
    unittest.main()
