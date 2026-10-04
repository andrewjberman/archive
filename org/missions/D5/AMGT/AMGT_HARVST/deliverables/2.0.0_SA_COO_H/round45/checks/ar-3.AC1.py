"""Round 45 HVST-ar-3 AC1 (issuer READ, FWD-9 / row Z-S82, CTO msg 29207): the served timeline is clipped at
STORE_START (2026-01-01).

Runs the SERVED code path (`scoped_amgt._serve_timeline_body`, the body of both wired timeline routes) for
every name gold carries, against live gold read once and memoised (the same `_timeline_snapshot_rows` the
Lambda calls). Read-only: no write, no vendor call, no Lambda invoke.

Prints the pre-2026 rows gold holds per table and the names they fall on, then:
  range route, `from=2013-01-01`: any served series day, event first/last day, marker date or word-cloud
    window start before 2026-01-01 is a LEAK;
  day route: every pre-2026 event first_day and every pre-2026 mention day of those names must NOT serve
    data (an error body), else a LEAK.
`AC1 RESULT: PASS` iff 0 leaks and every name was served without an error body on the range route.
"""

import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
sys.path.insert(0, ROOT)

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import timeline_api  # noqa: E402

FLOOR = datetime.date(2026, 1, 1)
OUT = os.path.join(os.path.dirname(HERE), "ar-3.served_clip.json")


def _d(v):
    if v is None:
        return None
    if isinstance(v, datetime.datetime):
        return v.astimezone(datetime.timezone.utc).date() if v.tzinfo else v.date()
    if isinstance(v, datetime.date):
        return v
    return datetime.date.fromisoformat(str(v)[:10])


def main():
    real = scoped_amgt._timeline_snapshot_rows
    cache = {}

    def memo(table, columns=None, security_key=None):
        if table not in cache:
            cache[table] = list(real(table))
        rows = cache[table]
        if security_key is not None:
            rows = [r for r in rows if r.get("security_key") == security_key]
        return rows

    scoped_amgt._timeline_snapshot_rows = memo
    daily = memo("chatter_daily")
    events = memo("chatter_event")
    mention = memo("article_security_mention")
    names = sorted({r.get("security_key") for r in daily if r.get("security_key")})

    pre_event = [r for r in events if _d(r.get("first_day")) and _d(r.get("first_day")) < FLOOR]
    pre_mention = [r for r in mention if r.get("published_utc") is not None and pg._day_of(r["published_utc"]) < FLOOR]
    pre_daily = [r for r in daily if _d(r.get("day")) and _d(r.get("day")) < FLOOR]
    print("gold rows: chatter_daily %d (pre-2026 %d), chatter_event %d (pre-2026 %d on %d names), "
          "article_security_mention %d (pre-2026 %d on %d names)"
          % (len(daily), len(pre_daily), len(events), len(pre_event), len({r.get("security_key") for r in pre_event}),
             len(mention), len(pre_mention), len({r.get("security_key") for r in pre_mention})))

    leaks = []
    errors = []
    served_events = 0
    for key in names:
        resp = scoped_amgt._serve_timeline_body(key, None, {"from": "2013-01-01"}, timeline_api)
        body = json.loads(resp["body"]) if isinstance(resp.get("body"), str) else resp.get("body")
        if timeline_api.is_error_body(body):
            errors.append("%s range route: %s" % (key, body.get("error_code")))
            continue
        for s in body.get("series") or []:
            if _d(s.get("date")) is None or _d(s.get("date")) < FLOOR:
                leaks.append("%s series date %s" % (key, s.get("date")))
        for e in body.get("events") or []:
            served_events += 1
            for f in ("first_day", "last_day"):
                if e.get(f) and _d(e.get(f)) < FLOOR:
                    leaks.append("%s event %s %s %s" % (key, e.get("event_id"), f, e.get(f)))
        for m in body.get("markers") or []:
            if _d(m.get("date")) is None or _d(m.get("date")) < FLOOR:
                leaks.append("%s marker %s %s" % (key, m.get("kind"), m.get("date")))
        wc = body.get("word_cloud") or {}
        if wc.get("window") and _d(wc["window"].get("from")) < FLOOR:
            leaks.append("%s word_cloud window from %s" % (key, wc["window"].get("from")))

    probe_days = sorted({(r.get("security_key"), _d(r.get("first_day"))) for r in pre_event}
                        | {(r.get("security_key"), pg._day_of(r["published_utc"])) for r in pre_mention
                           if r.get("security_key") in {e.get("security_key") for e in pre_event}})
    day_served = 0
    for key, day in probe_days:
        resp = scoped_amgt._serve_timeline_body(key, day.isoformat(), {}, timeline_api)
        body = json.loads(resp["body"]) if isinstance(resp.get("body"), str) else resp.get("body")
        if not timeline_api.is_error_body(body):
            day_served += 1
            leaks.append("%s day route served %s with %d articles" % (key, day, len(body.get("articles") or [])))

    record = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "names": len(names),
              "pre2026": {"chatter_daily": len(pre_daily), "chatter_event": len(pre_event),
                          "chatter_event_names": sorted({r.get("security_key") for r in pre_event}),
                          "article_security_mention": len(pre_mention),
                          "article_security_mention_names": len({r.get("security_key") for r in pre_mention})},
              "range_route_events_served": served_events, "day_route_probes": len(probe_days),
              "day_route_probes_served": day_served, "leaks": leaks, "errors": errors}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, default=str)
    print("names served on the range route: %d; errors %d; events served %d" % (len(names) - len(errors), len(errors), served_events))
    print("pre-2026 event names: %s" % ", ".join(record["pre2026"]["chatter_event_names"]))
    print("day-route probes on pre-2026 days: %d; served with data: %d" % (len(probe_days), day_served))
    print("LEAKS: %d" % len(leaks))
    for x in (leaks + errors)[:40]:
        print("  " + x)
    print("RECORD: %s" % OUT)
    ok = not leaks and not errors and names
    print("AC1 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
