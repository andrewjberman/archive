"""RIV-ai-1 AC2 (the seam against the REAL sources) -- read_context over live S3, READ-ONLY, with the default getter and lister.

Run date in ET. Expect:
  - fear_greed readings for `stock_price_strength` and `stock_price_breadth`, each with an `as_of`;
  - three rsi readings (equities, fixed income, commodities), each with an `as_of`;
  - at least one trending_topics reading with an `as_of`;
  - a harvest_chatter reading (any status) and a keyword_sentiment reading;
  - control: every status is in {fresh, stale, missing}, and every non-missing reading's `location` is an s3:// URI."""
import datetime as dt
import pathlib
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import market_context as mc

    day = dt.datetime.now(ZoneInfo("America/New_York")).date().isoformat()
    out = mc.read_context(day)
    print(f"day {day}: {len(out)} readings")
    for r in out:
        print(" ", r.get("source"), r.get("name"), r.get("as_of"), r.get("status"), str(r.get("location"))[:70])
    by = {(r.get("source"), r.get("name")): r for r in out}
    fg = [by.get(("fear_greed", k)) for k in ("stock_price_strength", "stock_price_breadth")]
    v.check(all(x is not None and x.get("as_of") for x in fg), "fear_greed strength and breadth read, each dated")
    rsi = [r for r in out if r.get("source") == "rsi"]
    tt = [r for r in out if r.get("source") == "trending_topics"]
    v.check(len(rsi) == 3 and all(r.get("as_of") for r in rsi) and tt and all(r.get("as_of") for r in tt),
            "three rsi readings and the trending topics, each dated")
    srcs = {r.get("source") for r in out}
    v.check({"harvest_chatter", "keyword_sentiment"} <= srcs, "harvest_chatter and keyword_sentiment readings present")
    v.check({r.get("status") for r in out} <= {"fresh", "stale", "missing"}
            and all(str(r.get("location", "")).startswith("s3://") for r in out if r.get("status") != "missing"),
            "control: statuses in the enum; every read reading's location is an s3:// URI")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
