"""AMGT_RESAPP round 121 (cb-2): prepare the issuer's read of the CEO profile on the RUNNING Security Analysis page.

  python r121_running_page_read.py build [outdir]     build the forced-corrupt fixture and print the three ui-smoke commands
  python r121_running_page_read.py check <log>...    grade ui-smoke text logs (not used before the promote)

Read-only against the live API. `build` invokes GET /api/scoped/amgt/security/TSM_US_Equity/thesis on opal-amgt-scoped-api once, copies the
body, replaces its `management` object's CEO fields with a CORRUPT served shape (`ceo_public_profile` the string `corrupt`; `ceo_profile_reading`
`{reading: UNREADABLE_OBJECT, reading_basis: "the object is not a dict", reason: null, urls_returned: null}`) and writes
`<outdir>/corrupt_TSM_US_thesis_fixture.json` as `{"TSM_US_Equity/thesis": <body>}` for `node scripts/ui-smoke.mjs --fixtures`. The three reads
the CTO named (round-120 analysis section 4): TSM US (the live body: NOT_WRITTEN) shows `No CEO profile has been written for this company yet.`;
the forced corrupt fixture shows `The CEO profile could not be read.`; HD US (the live body: SEARCHED_NOTHING_FOUND) shows its searched sentence.
The screenshots are READ by the issuer; this script writes no screenshot and grades nothing by itself.
"""
import base64
import json
import os
import sys

import boto3

FN = "opal-amgt-scoped-api"
LAM = boto3.client("lambda", region_name="us-east-1")


def thesis(key):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        raise SystemExit("ERROR: thesis %s status %s" % (key, r.get("statusCode")))
    raw = base64.b64decode(r["body"]) if r.get("isBase64Encoded") else r["body"].encode("utf-8")
    return json.loads(raw.decode("utf-8"))


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    body = thesis("TSM_US_Equity")
    mg = body.get("management") or {}
    before = (mg.get("ceo_profile_reading") or {}).get("reading")
    mg["ceo_public_profile"] = "corrupt"
    mg["ceo_profile_reading"] = {"reading": "UNREADABLE_OBJECT", "reading_basis": "the object is not a dict", "reason": None, "urls_returned": None}
    body["management"] = mg
    path = os.path.join(outdir, "corrupt_TSM_US_thesis_fixture.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"TSM_US_Equity/thesis": body}, f)
    print("FIXTURE: %s (live reading before the change: %s; after: UNREADABLE_OBJECT; size %d bytes)" % (path, before, os.path.getsize(path)))
    # MEASURED at the first run (2026-10-18 17:4xZ): with the stubbed auth session the live API answers no data (the page shows `The identity
    # header could not be loaded` and skeleton rows), so the live JS bundle is fed the SERVED /thesis body of each name through --fixtures instead.
    for key in ("TSM_US_Equity", "HD_US_Equity"):
        with open(os.path.join(outdir, "live_%s_thesis_fixture.json" % key), "w", encoding="utf-8") as f:
            json.dump({"%s/thesis" % key: thesis(key)}, f)
    print("COMMANDS (from C:/Dev/ajb_workspace/portal, route WITHOUT a leading slash; the live bundle at https://opalinvest.dev, the served /thesis body through --fixtures):")
    for stem, key, fx in (("tsm_live", "TSM_US_Equity", "live_TSM_US_Equity_thesis_fixture.json"), ("hd_live", "HD_US_Equity", "live_HD_US_Equity_thesis_fixture.json"), ("tsm_corrupt", "TSM_US_Equity", "corrupt_TSM_US_thesis_fixture.json")):
        print('  node scripts/ui-smoke.mjs security-analysis/%s %s/%s.png --origin https://opalinvest.dev --fixtures %s/%s --click "Exec Management"' % (key, outdir, stem, outdir, fx))
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("build", "check"):
        print(__doc__)
        return 2
    if sys.argv[1] == "build":
        return build(sys.argv[2] if len(sys.argv) > 2 else "C:/dev/ui-walk-evidence/r121-page")
    print("check: not implemented before the promote; the issuer reads the screenshots")
    return 0


if __name__ == "__main__":
    sys.exit(main())
