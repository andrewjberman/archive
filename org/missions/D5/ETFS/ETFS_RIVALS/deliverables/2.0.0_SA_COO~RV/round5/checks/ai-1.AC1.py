"""RIV-ai-1 AC1 (FWD-17 inputs, amendment A1) -- every market reading carries its stored name and its date; a stale reading
carries no series; an absent source is a `missing` reading, never skipped.

Pure, offline: `market_context.read_context(day, getter=..., lister=...)` over fixture bytes in the REAL shapes of the four
portal JSON files (measured 2026-10-02 READ-ONLY), day 2026-10-02:
  fear-greed  current.last_update 2026-10-01 (components keyed by stored name, each {score, historical})   -> fresh
  rsi-summary last_updated 2026-09-30                                                                   -> fresh (2 trading days)
  trending    data_as_of 2026-10-01                                                                     -> fresh
  keywords    generated_at 2026-09-20                                                                   -> stale
  harvest     the lister returns no partition                                                           -> missing
  - fear_greed readings name `stock_price_strength` and `stock_price_breadth` (stored names), as_of 2026-10-01, fresh, with a series;
  - the rsi equities reading is fresh with as_of 2026-09-30; the keyword_sentiment reading is stale with series None;
  - a harvest_chatter reading exists with status missing and a reason;
  - control: every reading's status is in {fresh, stale, missing} and every source the contract names appears."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-02"
P = "s3://opal-data-portal-v2/"
COMP = ("market_momentum_sp500", "stock_price_strength", "stock_price_breadth", "put_call_options", "market_volatility_vix",
        "safe_haven_demand", "junk_bond_demand")


def files():
    hist = [{"date": d, "value": v, "rating": "fear"} for d, v in (("2026-10-01", -8.24), ("2026-09-30", -7.68))]
    fg = {"current": {"value": 28.09, "description": "fear", "last_update": "2026-10-01T21:13:15+00:00", "previous_close": 30.83,
                      "components": {k: {"score": 0.4, "rating": "fear", "name": k, "historical": hist} for k in COMP}},
          "historical": [{"date": "2026-10-01", "value": 28.09, "description": "fear"}, {"date": "2026-09-30", "value": 30.26, "description": "fear"}],
          "generated_at": "2026-10-01T21:30:41+00:00"}
    ac = {"value": 48.2, "status": "neutral", "change_7d": 1.0, "change_14d": 2.0, "change_30d": 3.0, "change_90d": 4.0,
          "change_1y": 5.0, "change_3y": 6.0}
    rsi = {"generated_at": "2026-10-01T21:30:34Z", "data_as_of": "2026-09-30", "last_updated": "2026-09-30",
           "rsi_summary": {"equities": ac, "fixedIncome": ac, "commodities": ac}}
    item = {"topic": "rates", "subtext": "", "context": "", "article_count": 12, "sentiment_bull_bear": 0.3}
    tr = {"generated_at": "2026-10-01T21:21:48+00:00", "data_as_of": "2026-10-01", "date": "2026-10-01", "bullish": [item], "bearish": [item]}
    kw = {"generated_at": "2026-09-20T21:18:11+00:00", "days_back": 7, "keywords": [{"keyword": "tariffs", "sentiment": -0.2, "count": 9, "rank": 1}]}
    return {P + "json/sentiment/fear-greed-index.json": fg, P + "json-tiered/market-overview/rsi-summary.json": rsi,
            P + "json/trending/latest.json": tr, P + "json/sentiment/keyword-sentiments.json": kw}


def run(v):
    c.setup_path()
    from rivalfunds import market_context as mc

    fx = files()
    out = mc.read_context(DAY, getter=lambda uri: json.dumps(fx[uri]).encode() if uri in fx else None, lister=lambda prefix: [])
    for r in out:
        print(" ", r.get("source"), r.get("name"), r.get("as_of"), r.get("status"), "series" if r.get("series") else "-")
    by = {(r.get("source"), r.get("name")): r for r in out}
    s, b = by.get(("fear_greed", "stock_price_strength")), by.get(("fear_greed", "stock_price_breadth"))
    v.check(s is not None and b is not None and all(str(x["as_of"])[:10] == "2026-10-01" and x["status"] == "fresh" and x["series"]
                                                     for x in (s, b)),
            "fear_greed names stock_price_strength and stock_price_breadth, as_of 2026-10-01, fresh, with a series")
    eq = [r for r in out if r.get("source") == "rsi" and "equit" in str(r.get("name")).lower()]
    kw = [r for r in out if r.get("source") == "keyword_sentiment"]
    v.check(len(eq) == 1 and eq[0]["status"] == "fresh" and str(eq[0]["as_of"])[:10] == "2026-09-30"
            and kw and all(r["status"] == "stale" and not r.get("series") for r in kw),
            "rsi equities fresh at 2026-09-30; keyword_sentiment stale with no series")
    hv = [r for r in out if r.get("source") == "harvest_chatter"]
    v.check(len(hv) >= 1 and all(r["status"] == "missing" and r.get("reason") for r in hv),
            "harvest_chatter with no partition is a missing reading with a reason")
    srcs = {r.get("source") for r in out}
    v.check({r.get("status") for r in out} <= {"fresh", "stale", "missing"}
            and {"fear_greed", "rsi", "trending_topics", "keyword_sentiment", "harvest_chatter"} <= srcs,
            "control: every status is in the enum and every contract source appears")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
