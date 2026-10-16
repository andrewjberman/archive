#!/usr/bin/env python3
"""MDPF_CANON round 11 -- read the newest served gold object of each of the 16 scope/type pairs and write them as a D4-shaped
response file, so grade_d4_v2.py --allow-append can grade the first SCHEDULED fire the way it graded the dry run.

  python fetch_served_as_response.py --out <response.json> [--min-date 2026-10-16]

Read-only (list + get on opal-data-assets/portal/gold/mdpf/<scope>/<type>/). Prints, per pair, the key chosen and its
LastModified; the denominator is the number of keys listed per prefix. Output file goes OUTSIDE the repo (client-scale
bytes). ASCII only.
"""
import argparse
import json
import subprocess
import sys

BUCKET = "opal-data-assets"
SCOPES = ("global", "49financial", "inflection", "cottonwood")
TYPES = ("account-distribution", "aggregate-aua-timeseries", "aum-metrics", "category-views")
AWS = "C:/dev/ajb_workspace/.tools/aws.cmd"


def aws(*a):
    p = subprocess.run([AWS, *a], capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        raise SystemExit("aws failed rc=%d: %s" % (p.returncode, p.stderr[-300:]))
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-date", default="2026-10-16")
    a = ap.parse_args()
    bodies = {}
    for s in SCOPES:
        for t in TYPES:
            pre = "portal/gold/mdpf/%s/%s/" % (s, t)
            out = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", pre, "--output", "json")
            doc = json.loads(out) if out.strip() else {}
            items = doc.get("Contents") or []
            truncated = doc.get("IsTruncated")
            keys = sorted(i["Key"] for i in items if i["Key"].endswith(".json"))
            if truncated:
                raise SystemExit("listing truncated at %s: paginate before trusting a newest key" % pre)
            if not keys:
                raise SystemExit("no keys under " + pre)
            key = keys[-1]
            lm = [i["LastModified"] for i in items if i["Key"] == key][0]
            day = key.rsplit("/", 1)[1].replace(".json", "")
            print("  %-12s %-26s keys=%-4d newest=%s LastModified=%s%s" % (s, t, len(keys), day, lm, "" if day >= a.min_date else "  <-- OLDER THAN --min-date"))
            body = aws("s3", "cp", "s3://%s/%s" % (BUCKET, key), "-", "--only-show-errors")
            bodies[key] = {"body": body, "sha256": "-"}
    json.dump({"status": "green", "errors": [], "a4_objects_built": 16, "source": "served-s3", "bodies": bodies},
              open(a.out, "w", encoding="utf-8"))
    print("wrote", a.out, "bodies=%d" % len(bodies))
    return 0


if __name__ == "__main__":
    sys.exit(main())
