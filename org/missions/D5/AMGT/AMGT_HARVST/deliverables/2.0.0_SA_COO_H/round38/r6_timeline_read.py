"""Rebuild #6, CTO half @5eb4e11b3d condition (3): read the SERVED RESAPP timeline day route on one ft-bearing name
(after the act it serves 0 ft articles) beside one non-ft name (its day body is unchanged). Read-only: lambda:Invoke
of `opal-amgt-scoped-api`, the same event shape as RESAPP round62/checks/timeline_day.py.

  --what pick --out <json>    choose the ft-bearing (security, day) and the non-ft (security, day) from the served
                              mention snapshot (a non-ft name has 0 ft rows; its day has articles)
  --what read --pick <json> --out <json>
                              invoke the day route for both; record per-article publisher counts and the body sha256
  --what compare --before <json> --after <json>
                              PASS when the ft-bearing day serves 0 ft (and served >0 before), and the non-ft day
                              body sha256 is unchanged
"""
import argparse
import collections
import hashlib
import json
import subprocess
import sys

import boto3

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
FUNCTION, REGION = "opal-amgt-scoped-api", "us-east-1"


def event(path):
    return {"rawPath": path, "headers": {"x-firm-id": "opal"},
            "requestContext": {"http": {"method": "GET", "path": path}}, "queryStringParameters": None}


def day_path(key, day):
    return "/api/scoped/amgt/security/%s/timeline/day/%s" % (key, day)


def invoke(lam, path):
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event(path)).encode("utf-8"))
    parsed = json.loads(r["Payload"].read())
    body = parsed.get("body") or ""
    try:
        doc = json.loads(body)
    except ValueError:
        doc = {}
    arts = doc.get("articles") or doc.get("items") or []
    pubs = collections.Counter(a.get("publisher") for a in arts if isinstance(a, dict))
    return {"path": path, "status": parsed.get("statusCode"), "function_error": r.get("FunctionError"),
            "articles": len(arts), "publishers": dict(pubs), "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()}


def pick():
    from lib.research.harvest import publication_gold as pg
    rows = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    day = lambda r: str(r.get("published_utc"))[:10]  # noqa: E731
    ft_rows = [r for r in rows if r.get("publisher") == "ft"]
    ft_keys = {r["security_key"] for r in ft_rows}
    ft = next(((r["security_key"], day(r)) for r in ft_rows if r["security_key"] == "BA_US_Equity"),
              (ft_rows[0]["security_key"], day(ft_rows[0])))
    per = collections.Counter((r["security_key"], day(r)) for r in rows if r["security_key"] not in ft_keys)
    non = per.most_common(1)[0][0]
    return {"ft_bearing": {"security_key": ft[0], "day": ft[1]}, "non_ft": {"security_key": non[0], "day": non[1]},
            "ft_securities": len(ft_keys)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pick", "read", "compare"), required=True)
    ap.add_argument("--pick")
    ap.add_argument("--out")
    ap.add_argument("--before")
    ap.add_argument("--after")
    a = ap.parse_args()
    if a.what == "pick":
        p = pick()
        json.dump(p, open(a.out, "w", encoding="utf-8"), indent=1)
        print("PICK", p)
        return 0
    if a.what == "read":
        p = json.load(open(a.pick, encoding="utf-8"))
        lam = boto3.client("lambda", region_name=REGION)
        out = {k: invoke(lam, day_path(p[k]["security_key"], p[k]["day"])) for k in ("ft_bearing", "non_ft")}
        json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1)
        for k, v in out.items():
            print("READ %s %s status=%s articles=%d publishers=%s sha=%s" % (k, v["path"], v["status"], v["articles"],
                                                                              v["publishers"], v["body_sha256"][:16]))
        return 0
    b, af = json.load(open(a.before, encoding="utf-8")), json.load(open(a.after, encoding="utf-8"))
    fails = []
    if not b["ft_bearing"]["publishers"].get("ft"):
        fails.append("the ft-bearing day served 0 ft BEFORE (the control cannot see the quarantine)")
    if af["ft_bearing"]["publishers"].get("ft"):
        fails.append("the ft-bearing day still serves %d ft articles" % af["ft_bearing"]["publishers"]["ft"])
    if af["ft_bearing"]["status"] != 200 or af["non_ft"]["status"] != 200:
        fails.append("status after %s/%s" % (af["ft_bearing"]["status"], af["non_ft"]["status"]))
    if b["non_ft"]["body_sha256"] != af["non_ft"]["body_sha256"]:
        fails.append("the non-ft day body changed")
    print("FT-BEARING before %s after %s; NON-FT sha before %s after %s" % (
        b["ft_bearing"]["publishers"], af["ft_bearing"]["publishers"], b["non_ft"]["body_sha256"][:16],
        af["non_ft"]["body_sha256"][:16]))
    print("TIMELINE READ: %s (%d failure(s))" % ("PASS" if not fails else "FAIL", len(fails)))
    for f in fails:
        print("  FAIL: " + f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
