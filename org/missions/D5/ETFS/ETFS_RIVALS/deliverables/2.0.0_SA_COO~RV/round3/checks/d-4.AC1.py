"""RIV-d-4 AC1 (live, READ-ONLY) -- the SERVED page for the act's page day shows both Opal funds beside their rivals
with data (FWD-1), its freshness reasons count trading days, and its publish marker exists and names any not-updated fund.

Reads d4_live.json `page_day`, then s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=<page_day>/{index.html,
manifest.json} and the publish_page marker the record names (`publish_marker`)."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def run(v):
    rec = L.record()
    day = rec.get("page_day")
    base = f"rivalfunds/etfs/platinum/page/date={day}/"
    html = L.get(base + "index.html").decode("utf-8")
    m = json.loads(L.get(base + "manifest.json"))
    print("page day", day, "funds_updated", m.get("funds_updated"), "of", m.get("funds_total"))
    for f in ("IDVZ", "PFOE"):
        blk = re.search(rf'data-fund="{f}"(.*?)(?=data-fund="|\Z)', html, re.S)
        body = blk.group(1) if blk else ""
        v.check("data-calendar" in body and 'data-source="home_producer"' in body, f"{f}: served with calendar + home_producer badge")
    v.check("home-producer reader: next round" not in html.lower(), "no 'home-producer reader: next round' placeholder served")
    reasons = [x.get("reason", "") for e in (m.get("funds") or {}).values() for x in e.get("checks", [])
               if x.get("check") == "report_date_freshness"]
    v.check(len(reasons) > 0 and all("trading day" in r for r in reasons), f"{len(reasons)} freshness reasons count trading days")
    mk = rec.get("publish_marker")
    body = json.loads(L.get(mk[len("s3://opal-data-etfs/"):])) if mk else {}
    flagged = {k.split("/")[-1] for k, e in (m.get("funds") or {}).items()
               if any(x.get("status") == "FAIL" for x in e.get("checks", []))}
    v.check(bool(mk) and flagged <= set(map(str, (body.get("not_updated") or {}).keys())),
            f"publish marker {mk} names every not-updated fund ({sorted(flagged)})")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
