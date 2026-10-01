"""RIV-f-4 AC1 (analysis ruling 7) -- the page headline: the top-level word means "page published"; the headline states the count
and names each lagging fund with its reason.

Offline page fixture (test_p2's: TXUE bloomberg, BASG issuer, three days, G5 replayed). The page is published for 2026-09-30 with a
planted content_repeat failure on TXUE (one of two funds lags):
  - the manifest's top-level `status` reads `published` (today: `not-updated`);
  - the page text before the first fund block states "<funds_updated> of <funds_total> funds current" (the manifest's own counts;
    the fixture's universe has 13 funds) and names TXUE with its reason (content_repeat);
  - control: the TXUE block still reads data-status="not-updated" and the BASG block data-status="updated" (failed figures never
    publish: FWD-9)."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import homes, publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    spec, s, _ = c.page_fixture()
    r = publish_page.handler_entry(tp2._ev(spec, plant_failure="content_repeat", plant_fund="TXUE"))
    html = s.get(homes.page("2026-09-30", "index.html")).decode("utf-8")
    man = json.loads(s.get(homes.page("2026-09-30", "manifest.json")))
    head = html.split("<article", 1)[0]
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", head))
    print("run status:", r.get("status"), "| manifest status:", man.get("status"))
    print("headline text:", text[-300:].strip())
    v.check(man.get("status") == "published", "the manifest's top-level status reads published")
    want = f"{man.get('funds_updated')} of {man.get('funds_total')} funds current"
    v.check(want in text and "TXUE" in text and "content_repeat" in text,
            f"the headline states '{want}' (the manifest's own counts) and names TXUE with its reason")
    tx, ba = tp2._block(html, "TXUE"), tp2._block(html, "BASG")
    v.check('data-status="not-updated"' in tx and 'data-status="updated"' in ba,
            "control: TXUE's block stays not-updated, BASG's updated (failed figures never publish)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
