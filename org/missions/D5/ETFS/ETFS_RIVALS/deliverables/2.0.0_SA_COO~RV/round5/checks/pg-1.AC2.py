"""RIV-pg-1 AC2 (FWD-18 "a section with missing data says so in its own place"; comp-adversary declared: a benchmark never
shows an AI section) -- the components render from the A1 tables and an absent one says so.

Offline: `_a1_page.publish` (TXUE has all four tables; BASG has none; SCHY carries a PLANTED AI account; the census names S9).
  - TXUE's MTD panel names `Name S1` and its table carries data-ranked="2" data-missing="1"; TXUE has a trend and an AI block;
  - BASG's MTD panel carries the `rf-missing` notice;
  - the benchmark SCHY shows no AI block, even with an account planted for it;
  - control: the census block names the missing input S9."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _a1_page as ap  # noqa: E402
import _common as c  # noqa: E402


def _panel(html, fund, period):
    m = re.search(rf'data-rank-fund="{fund}"\s+data-rank-period="{period}"(.*?)(?=data-rank-fund=|data-trend-fund=|data-ai-fund=|<details\b[^>]*id="audit"|\Z)',
                  html, re.S)
    return m.group(1) if m else ""


def run(v):
    c.setup_path()
    _, html = ap.publish()
    tx = _panel(html, "TXUE", "MTD")
    print("TXUE MTD panel:", len(tx), "chars;", re.findall(r'data-ranked="\d+"|data-missing="\d+"', tx)[:4])
    v.check("Name S1" in tx and 'data-ranked="2"' in tx and 'data-missing="1"' in tx
            and 'data-trend-fund="TXUE"' in html and 'data-ai-fund="TXUE"' in html,
            "TXUE: the ranking names Name S1 with ranked 2 and missing 1; trend and AI blocks present")
    ba = _panel(html, "BASG", "MTD")
    v.check("rf-missing" in ba, "BASG's MTD ranking, with no table, says so in place")
    v.check('data-ai-fund="SCHY"' not in html, "the benchmark SCHY shows no AI block even with a planted account")
    v.check('data-input-missing="S9"' in html, "control: the census names the missing input S9")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
