"""HARVST round 41 -- the post-act reads the CTO halves name (@8e0fed682a), on what RESAPP SERVES. Read-only:
lambda:Invoke of `opal-amgt-scoped-api` with the same event shape as round38's timeline read and RESAPP round64's checks.

  --after an-2   (1) the chatter route still serves `tone` null beside `tone_reason` on every row (it reads no tone field
                 yet); (2) BA's timeline day view serves its articles on BA's busiest day in the newest mention snapshot.
  --after an-3   on BA, AMD and VLO (RESAPP FWD-37 c11): every event the timeline serves has a coverage_event marker on its
                 first_day labelled with its lead headline, and EVERY coverage_event marker's day view serves >0 articles.
Writes `round41/post_act_<an>_<stamp>.json`. Verdict line: `POST-ACT <an>: PASS|FAIL`.
"""
import argparse
import collections
import datetime
import json
import os
import subprocess
import sys

import boto3

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
FUNCTION, REGION = "opal-amgt-scoped-api", "us-east-1"
PREFIX = "/api/scoped/amgt"
NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity")


def call(lam, path, query=None):
    ev = {"rawPath": path, "headers": {"x-firm-id": "opal"}, "queryStringParameters": query,
          "requestContext": {"http": {"method": "GET", "path": path}}}
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode("utf-8"))
    parsed = json.loads(r["Payload"].read())
    try:
        body = json.loads(parsed.get("body") or "null")
    except ValueError:
        body = None
    return parsed.get("statusCode"), body, r.get("FunctionError")


def articles(body):
    return (body or {}).get("articles") or (body or {}).get("items") or []


def after_an2(lam, out):
    ok = []
    st, b, fe = call(lam, PREFIX + "/lead-panel/timeseries/collected/chatter")
    rows = (b or {}).get("rows") or []
    bad = [r.get("security_key") for r in rows if not (r.get("tone") is None and r.get("tone_reason"))]
    reasons = sorted({r.get("tone_reason") for r in rows})
    out["chatter"] = {"status": st, "function_error": fe, "rows": len(rows), "rows_without_null_tone_and_reason": len(bad),
                      "tone_reasons": reasons}
    ok.append(st == 200 and rows and not bad)
    print("%s (1) chatter: status %s rows %d, rows without null tone + reason %d, reasons %s"
          % ("PASS" if ok[-1] else "FAIL", st, len(rows), len(bad), reasons))
    from lib.research.harvest import publication_gold as pg
    per_day = collections.Counter(str(r.get("published_utc"))[:10] for r in pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
                                  if r.get("security_key") == "BA_US_Equity")
    day, gold_n = per_day.most_common(1)[0]
    st, b, fe = call(lam, "%s/security/BA_US_Equity/timeline/day/%s" % (PREFIX, day))
    arts = articles(b)
    out["ba_day"] = {"day": day, "gold_mention_rows": gold_n, "status": st, "function_error": fe, "articles": len(arts),
                     "publishers": dict(collections.Counter(a.get("publisher") for a in arts if isinstance(a, dict)))}
    ok.append(st == 200 and len(arts) > 0)
    print("%s (2) BA day %s: status %s, %d articles served (%d gold mention rows that day), publishers %s"
          % ("PASS" if ok[-1] else "FAIL", day, st, len(arts), gold_n, out["ba_day"]["publishers"]))
    return all(ok)


def after_an3(lam, out):
    ok = []
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    out["names"] = {}
    for key in NAMES:
        st, tl, fe = call(lam, "%s/security/%s/timeline" % (PREFIX, key), {"from": "2026-01-01", "to": today})
        tl = tl or {}
        mk = tl.get("markers") if isinstance(tl.get("markers"), list) else []
        events = tl.get("events") or []
        cov = [m for m in mk if m.get("kind") == "coverage_event"]
        cov_set = {(m.get("date"), m.get("label")) for m in cov}
        missing = [e.get("first_day") for e in events if (e.get("first_day"), e.get("lead_headline")) not in cov_set]
        empty_days = []
        for d in sorted({m.get("date") for m in cov}):
            dst, db, _ = call(lam, "%s/security/%s/timeline/day/%s" % (PREFIX, key, d))
            if dst != 200 or not articles(db):
                empty_days.append([d, dst])
        out["names"][key] = {"status": st, "function_error": fe, "events": len(events), "coverage_markers": len(cov),
                             "events_without_marker": missing, "marker_days_not_opening": empty_days}
        ok.append(st == 200 and not missing and not empty_days)
        print("%s %s: status %s, %d events, %d coverage markers, events without a marker %d, marker days that do not open %d"
              % ("PASS" if ok[-1] else "FAIL", key, st, len(events), len(cov), len(missing), len(empty_days)))
    return all(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--after", choices=("an-2", "an-3"), required=True)
    a = ap.parse_args()
    lam = boto3.client("lambda", region_name=REGION)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = {"after": a.after, "read_at": stamp, "function": FUNCTION}
    passed = after_an2(lam, out) if a.after == "an-2" else after_an3(lam, out)
    out["verdict"] = "PASS" if passed else "FAIL"
    path = os.path.join(HERE, "post_act_%s_%s.json" % (a.after, stamp))
    json.dump(out, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    print("POST-ACT %s: %s" % (a.after, out["verdict"]))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
