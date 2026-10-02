"""RIV-rd-1 AC2 (RFW-U09, raw-code: no system code on the face): every stored market-reading key in an AI account reads
as its label WHOLE -- a multi-word key and a bare family name included -- with the stored key kept as the label's title
tooltip; and the vintage line names tables in words, the table code in a tooltip.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base).
The label regex `_READING` (render.py:1072) takes `<family>/[A-Za-z0-9_]+`, so:
  - a multi-word key is labelled by its first word and the rest prints after the label: 'the news sentiment for
    "middle" east oil = -0.2227', 'the sentiment of the trending topic "U".S. Threatens Diesel Export Ban' (195 such
    spans over 10 keys on the served 10-02 page, in Cited rows and "Inputs as of");
  - a bare family name is never labelled: 'Weak fear_greed readings suggest ...' (4 on the served page);
  - `_vintage_line` (render.py:1146-1160) prints the raw table names 'buying_trend' and 'holding_contribution'.
INTERFACE: `render._ai_card(ctx, f)`; labels from `ai_accounts.reading_label` (or a render-side map with the same
words). A replaced key is an element whose `title` is the stored key exactly (the claim survives); a bare family name
reads in words ("Fear & Greed") with a title carrying the stored name; the `data-vintage` element names each table in
words with the table code in a title, the revision tooltips unchanged.

Pure, offline fixture: one TXUE PASS account. Text: "fear_greed/fear_greed_index sat at 28.09. The fund kept adding.";
Inferred: "Weak fear_greed readings suggest the backdrop was unsupportive."; cited rows: market_context
keyword_sentiment/middle east oil = -0.2227, market_context trending_topics/U.S. Threatens Diesel Export Ban = -0.6,
holding_contribution TXUE|YTD|INTU_US_Equity = 0.0125 (revision 20261002T110325Z-1e965e151a22), buying_trend
TXUE|INTU_US_Equity = 3000 (revision 20261002T110403Z-2164be9a1d84); input vintages for the two multi-word keys and
fear_greed/fear_greed_index. The page serves holding_contribution 20261002T194820Z-e3c4c5906249 and buying_trend
20261002T194900Z-5fd3f83ad4f8, so the vintage line shows.
  - the card text (attributes excluded, the dialog and the closed sources box included) carries 0 raw reading codes:
    no '<family>/' and no bare 'fear_greed' / 'trending_topics' / 'keyword_sentiment' / 'harvest_chatter', and the
    Inferred item reads "Fear & Greed" with a title carrying 'fear_greed';
  - each multi-word key reads whole: the text carries 'middle east oil' and 'U.S. Threatens Diesel Export Ban' and
    neither '"middle" east' nor '"U".S.'; elements titled exactly 'keyword_sentiment/middle east oil' and
    'trending_topics/U.S. Threatens Diesel Export Ban' exist; none titled 'keyword_sentiment/middle' or
    'trending_topics/U';
  - the vintage line's text carries no 'holding_contribution' / 'buying_trend' (no '<word>_<word>' code) while a title
    in it still carries each table name;
  - control: 'fear_greed/fear_greed_index' still reads "Fear & Greed index" under a title of exactly that key; the
    figures 28.09, -0.2227 and -0.6 read; the four revision ids survive as titles in the vintage line; the row's stored
    text is unchanged.
FAIL at base: the first three limbs; the control PASSes."""

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

MIDDLE = "keyword_sentiment/middle east oil"
USDIESEL = "trending_topics/U.S. Threatens Diesel Export Ban"
TEXT = "fear_greed/fear_greed_index sat at 28.09. The fund kept adding."
INFERRED = "Weak fear_greed readings suggest the backdrop was unsupportive."
HC_W, BT_W = "20261002T110325Z-1e965e151a22", "20261002T110403Z-2164be9a1d84"
HC_S, BT_S = "20261002T194820Z-e3c4c5906249", "20261002T194900Z-5fd3f83ad4f8"
RAW = re.compile(r"\b(?:fear_greed|rsi|trending_topics|keyword_sentiment|harvest_chatter)/"
                 r"|\b(?:fear_greed|trending_topics|keyword_sentiment|harvest_chatter)\b")


def fixture():
    cited = [{"table": "market_context", "key": MIDDLE, "revision": "2026-10-01T21:18:11Z", "value": -0.2227},
             {"table": "market_context", "key": USDIESEL, "revision": "2026-10-01", "value": -0.6},
             {"table": "market_context", "key": "fear_greed/fear_greed_index", "revision": "2026-10-01",
              "value": 28.09},
             {"table": "holding_contribution", "key": "TXUE|YTD|INTU_US_Equity", "revision": HC_W, "value": 0.0125},
             {"table": "buying_trend", "key": "TXUE|INTU_US_Equity", "revision": BT_W, "value": 3000.0}]
    vint = {MIDDLE: "2026-10-01T21:18:11Z", USDIESEL: "2026-10-01", "fear_greed/fear_greed_index": "2026-10-01"}
    acct = u.account("TXUE", "activity_30d", TEXT, cited=cited, inferred=[INFERRED], vintages=vint)
    a1 = {"research_hypotheses": [acct],
          "holding_contribution": [{"fund_id": "TXUE", "revision": HC_S}],
          "buying_trend": [{"fund_id": "TXUE", "revision": BT_S}]}
    return acct, {"day": "2026-10-02", "a1": a1}


def run(v):
    c.setup_path()
    from rivalfunds import render

    acct, ctx = fixture()
    before = json.dumps(acct, sort_keys=True)
    root = u.parse(render._ai_card(ctx, {"fund": "TXUE", "role": "rival"}))
    t = u.text(root)
    titles = [n.attrs.get("title", "") for n in root.all("title")]
    print("card text:", t[:900])
    raw = RAW.findall(t)
    li = [n for n in root.tags("li") if "readings suggest" in u.text(n)]
    li_ok = bool(li) and all("fear & greed" in u.text(n).lower()
                             and any("fear_greed" in m.attrs.get("title", "") for m in n.all("title")) for n in li)
    print("raw codes in text:", raw[:8], "| inferred items:", [u.text(n) for n in li])
    v.check(not raw and li_ok,
            f"0 raw reading codes in the card text, the bare family reads 'Fear & Greed' under a title "
            f"(found {raw[:6]})")
    whole = ("middle east oil" in t and "U.S. Threatens Diesel Export Ban" in t
             and '"middle" east' not in t and '"U".S.' not in t)
    split = sorted({x for x in titles if x in ("keyword_sentiment/middle", "trending_topics/U")})
    print("titles:", sorted(set(titles))[:14])
    v.check(whole and MIDDLE in titles and USDIESEL in titles and not split,
            f"each multi-word key reads whole under a title of the whole key (first-word titles: {split})")
    vin = root.all("data-vintage")
    vt = u.text(vin[0]) if vin else ""
    vtitles = " ".join(n.attrs.get("title", "") for n in vin[0].all("title")) if vin else ""
    print("vintage line:", repr(vt))
    codes = re.findall(r"\b[a-z]+_[a-z_]+\b", vt)
    v.check(bool(vin) and not codes and "holding_contribution" in vtitles and "buying_trend" in vtitles,
            f"the vintage line names its tables in words, the table code in a title (codes in text: {codes})")
    fg = [n for n in root.all("title", "fear_greed/fear_greed_index") if "fear & greed index" in u.text(n).lower()]
    figs = [x for x in ("28.09", "-0.2227", "-0.6") if not re.search(r"(?<![\d.])" + re.escape(x) + r"(?!\d)", t)]
    revs = [r for r in (HC_W, BT_W, HC_S, BT_S) if r not in vtitles]
    v.check(bool(fg) and not figs and not revs and json.dumps(acct, sort_keys=True) == before,
            f"control: single-word labels, figures, revision tooltips and the stored row unchanged (missing figures "
            f"{figs}, revisions {revs})")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
