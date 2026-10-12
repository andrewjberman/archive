"""ADVI_FIRMBKTS round 4: the edge router's own request lines since the edge leg, by bucket and key class (issuer
2.0.0_SA_COO~B1). READ-ONLY (logs describe-log-groups, filter-log-events). It prints COUNTS only: never an identifier.

  python r4_routerlogs.py --since 2026-10-12T15:15:10Z [--regions us-east-1,us-east-2,us-west-2]
For every region it finds the log groups whose name starts /aws/lambda/us-east-1.shared-advisor-router (the router; the
response guard shares the prefix and is filtered out by its own name) and counts the "Firm routing:" lines by
`firmId`/`bucket` and by the key class (the first four path segments with any id-like segment replaced by <id>).
Last line: ROUTER LINES: <n> since <ts>; 49financial on opal-data-49financial <a>, on another bucket <b>.
"""
import argparse
import collections
import datetime
import json
import re
import shutil
import subprocess
import sys

AWS = shutil.which("aws") or shutil.which("aws.cmd") or "aws"
PREFIX = "/aws/lambda/us-east-1.shared-advisor-router"
LINE = re.compile(r"Firm routing: firmId=(\S+) bucket=(\S+) uri=(\S+)")


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=110)
    if r.returncode:
        return None
    return json.loads(r.stdout or "{}")


def klass(uri):
    segs = [s for s in uri.split("/") if s]
    out = []
    for s in segs[:5]:
        out.append("<id>" if re.fullmatch(r"[A-Za-z0-9_-]{16,}|[0-9]{5,}", s) or s.endswith(".json") else s)
    return "/" + "/".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True)
    ap.add_argument("--regions", default="us-east-1,us-east-2,us-west-2")
    a = ap.parse_args()
    since = int(datetime.datetime.strptime(a.since, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc).timestamp() * 1000)
    by_bucket = collections.Counter()
    by_class = collections.Counter()
    total = 0
    for region in a.regions.split(","):
        gs = aws("logs", "describe-log-groups", "--log-group-name-prefix", PREFIX, "--region", region)
        names = [g["logGroupName"] for g in (gs or {}).get("logGroups", [])
                 if not g["logGroupName"].endswith("-response")]
        print("region %s: router log groups %d" % (region, len(names)))
        for g in names:
            tok = None
            while True:
                args = ["logs", "filter-log-events", "--log-group-name", g, "--region", region,
                        "--start-time", str(since), "--filter-pattern", '"Firm routing"']
                if tok:
                    args += ["--next-token", tok]
                d = aws(*args)
                if d is None:
                    print("  read failed for %s" % g)
                    break
                for e in d.get("events", []):
                    m = LINE.search(e.get("message", ""))
                    if m:
                        total += 1
                        by_bucket[(m.group(1), m.group(2))] += 1
                        by_class[(m.group(2), klass(m.group(3)))] += 1
                tok = d.get("nextToken")
                if not tok:
                    break
    for (firm, bucket), n in sorted(by_bucket.items()):
        print("  firm %-14s bucket %-28s %d" % (firm, bucket, n))
    for (bucket, k), n in sorted(by_class.items(), key=lambda x: -x[1])[:14]:
        print("  %-28s %-48s %d" % (bucket, k, n))
    on = sum(n for (f, b), n in by_bucket.items() if f == "49financial" and b == "opal-data-49financial")
    off = sum(n for (f, b), n in by_bucket.items() if f == "49financial" and b != "opal-data-49financial")
    print("ROUTER LINES: %d since %s; 49financial on opal-data-49financial %d, on another bucket %d" % (total, a.since, on, off))
    return 0 if off == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
