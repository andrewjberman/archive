"""RIV-ui-4 AC2 (RFW-U09, raw-code: no system code on the face): a stored market-reading name in an account's text or
lists ('fear_greed/fear_greed_index') is DISPLAYED as its label ('Fear & Greed index'), with the stored name kept as the
label's title tooltip so the claim survives. The stored text is not rewritten.
INTERFACE: `render._ai_card(ctx, f)`; labels from `ai_accounts.reading_label` (or a render-side map with the same
words); each replaced name is an element whose `title` is the stored name exactly.

Pure, offline fixture: one TXUE PASS account whose text reads "fear_greed/fear_greed_index sat at 28.09, with
fear_greed/stock_price_strength at 0.4 and rsi/equities at 61.2." and whose Observed list holds
"fear_greed/stock_price_breadth was 0.2"; no cited rows, no input vintages.
  - the card text (attributes excluded) carries 0 stored reading names (<source>/<name> for the five sources);
  - it carries the labels: "Fear & Greed index", "stock price strength", "stock price breadth", "equities RSI";
  - an element titled "fear_greed/fear_greed_index" and one titled "rsi/equities" exist (the claim survives);
  - control: the figures 28.09, 0.4, 61.2 and 0.2 still read, and the row's stored text is unchanged after the
    render."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

RAW = re.compile(r"\b(?:fear_greed|rsi|trending_topics|keyword_sentiment|harvest_chatter)/[A-Za-z0-9_]+")
TEXT = (
    "fear_greed/fear_greed_index sat at 28.09, with fear_greed/stock_price_strength at 0.4 and rsi/equities at 61.2. "
    "The fund kept adding."
)


def run(v):
    c.setup_path()
    from rivalfunds import render

    acct = u.account("TXUE", "activity_30d", TEXT, observed=["fear_greed/stock_price_breadth was 0.2"])
    html = render._ai_card(
        {"day": "2026-10-02", "a1": {"research_hypotheses": [acct]}}, {"fund": "TXUE", "role": "rival"}
    )
    root = u.parse(html)
    t = u.text(root)
    print("card text:", t[:400])
    raw = RAW.findall(t)
    v.check(not raw, f"0 stored reading names in the account text (found {raw})")
    labels = ("fear & greed index", "stock price strength", "stock price breadth", "equities rsi")
    miss = [x for x in labels if x not in t.lower()]
    v.check(not miss, f"each reading reads by its label (missing {miss})")
    titled = {n.attrs.get("title") for n in root.all("title")}
    v.check(
        {"fear_greed/fear_greed_index", "rsi/equities"} <= titled,
        f"the stored name survives as the label's title tooltip (titles: {sorted(x for x in titled if x)[:6]})",
    )
    figs = [x for x in ("28.09", "0.4", "61.2", "0.2") if not re.search(r"(?<![\d.])" + re.escape(x) + r"(?![\d])", t)]
    v.check(
        not figs and acct["text"] == TEXT,
        f"control: the figures read and the stored text is unchanged (missing {figs})",
    )


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
