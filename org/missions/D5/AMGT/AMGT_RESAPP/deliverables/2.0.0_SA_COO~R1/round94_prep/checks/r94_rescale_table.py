"""AMGT_RESAPP round-94 PREP -- the rescale rule's regression table: over every stored analysis object, it moves SAP (0 -> 3 points on one scale) and nothing else.

  PYTHONPATH=<repo root> python r94_rescale_table.py            (S3 GETs of the stored objects; nothing is written)

For each `filings/v1/<key>/<accession>.analysis.json` (listed, not typed) the production path
`analyze.reverify_stored_thesis_driver(key, accession, dry_run=True)` computes EXPECTED on the checkout's code; STORED is the object's own
`thesis_driver.points` (round 93's ss-4 left SAP at 0 points, ASML at 0 and BABA at 2).
    T1 SAP_GY_Equity: expected 3 points on ONE scale, the series unit's: 2023 = 13.745, 2024 = 18.078, 2025 = 21.05, each carrying `stated_scale` and
       `rescaled_to` `billion`.
    T2 control: every OTHER analysis object's expected points equal its stored points (11 of 11): the rule moves no other name.
    T3 denominators printed: objects listed, names changed, names equal.
Verdict: R94 RESCALE TABLE: YES|NO (exit 0|1). At the base (2026-10-11) T1 FAILs (expected 0 points, held whole) and T2 PASSes.
"""
import json
import re
import sys

import boto3

from lib.research.filings import analyze

BUCKET = "opal-data-harvest"
S3 = boto3.client("s3", region_name="us-east-1")


def triples(points):
    return sorted((str(p.get("period")), str(p.get("value")), json.dumps(p.get("span"))) for p in points or [])


def main():
    pairs = []
    for page in S3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="filings/v1/"):
        for o in page.get("Contents", []):
            m = re.match(r"^filings/v1/([^/]+)/([^/]+)\.analysis\.json$", o["Key"])
            if m:
                pairs.append((m.group(1), m.group(2), o["Key"]))
    changed, equal, sap_points = [], [], None
    for key, accession, okey in sorted(pairs):
        stored = json.loads(S3.get_object(Bucket=BUCKET, Key=okey)["Body"].read())
        doc, _k, _r = analyze.reverify_stored_thesis_driver(key, accession, client=S3, dry_run=True)
        exp = triples((doc.get("thesis_driver") or {}).get("points"))
        sto = triples((stored.get("thesis_driver") or {}).get("points"))
        line = "   %-16s stored %d | expected %d%s" % (key, len(sto), len(exp), "" if exp == sto else "  CHANGED")
        print(line)
        if key == "SAP_GY_Equity":
            sap_points = {p["period"]: p for p in (doc.get("thesis_driver") or {}).get("points") or []}
        if exp == sto:
            equal.append(key)
        else:
            changed.append(key)
    points = (sap_points or {})
    t1 = (sorted(points) == ["2023", "2024", "2025"]
          and {p: round(float(v["value"]), 6) for p, v in points.items()} == {"2023": 13.745, "2024": 18.078, "2025": 21.05}
          and all(v.get("stated_scale") and v.get("rescaled_to") == "billion" for v in points.values()))
    others_changed = [k for k in changed if k != "SAP_GY_Equity"]
    t2 = not others_changed
    print("   objects %d | changed %d %s | equal %d" % (len(pairs), len(changed), sorted(changed), len(equal)))
    for ok, label in ((t1, "T1 SAP_GY_Equity expects 3 points on the unit's scale (13.745, 18.078, 21.05), each with its stated scale"),
                      (t2, "T2 control: no other analysis object's expected points move (%s)" % (others_changed or "none"))):
        print("%s %s" % ("PASS" if ok else "FAIL", label))
    ok = t1 and t2
    print("R94 RESCALE TABLE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
