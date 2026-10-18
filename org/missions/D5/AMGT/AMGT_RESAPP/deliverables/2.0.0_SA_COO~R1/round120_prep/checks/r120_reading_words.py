"""AMGT_RESAPP round 120 (ca-5, the CTO half's condition 3): per name, the served CEO reading word and whether the profile is null.

  python r120_reading_words.py [outfile.json]

Read-only. Invokes GET /api/scoped/amgt/security/<key>/thesis on opal-amgt-scoped-api for the eight names the CVO reads and prints, per name:
`management.ceo_public_profile` (null | dict | other) and `management.ceo_profile_reading.reading`. Run once BEFORE the act and once AFTER; the
CTO half's condition 3 reads the two outputs: a word that moves for a name whose profile is NOT null is a rollback. It grades nothing by itself.
"""
import json
import sys

import boto3

FN = "opal-amgt-scoped-api"
NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]
LAM = boto3.client("lambda", region_name="us-east-1")


def read(key):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        return {"key": key, "status": r.get("statusCode")}
    body = json.loads(r["body"])
    mgmt = body.get("management") or {}
    prof = mgmt.get("ceo_public_profile")
    reading = mgmt.get("ceo_profile_reading") or {}
    kind = "null" if prof is None else ("dict" if isinstance(prof, dict) else type(prof).__name__)
    return {"key": key, "status": 200, "profile": kind, "reading": reading.get("reading"), "reading_basis": reading.get("reading_basis")}


def main():
    rows = [read(k) for k in NAMES]
    for r in rows:
        print("%-20s status=%s profile=%-5s reading=%-26s basis=%s" % (r["key"], r["status"], r.get("profile"), r.get("reading"), (r.get("reading_basis") or "")[:60]))
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1)
    print("READING WORDS: %d of %d names read (status 200)" % (sum(1 for r in rows if r["status"] == 200), len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
