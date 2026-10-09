"""AMGT_RESAPP round-87 PREP -- a FAILED description is never served (CTO~DELL1 round-86 analysis R1) and NU's is empty (R2).

  python r87_withheld.py --crit AC1|NU [--where deployed|local] [--keys K1,K2,...]

Reads each name's served /thesis `drafted_sections[company_description]` (--where deployed: the live function, read only; local: the
handler in this checkout, which reads the stored drafts) and prints, per name, the section's own `description_verdict_state` and its
served sentence count.
    AC1 W1 no served company_description whose own verdict is FAILED carries a sentence (the FAILED ones are printed);
        W2 every name answered 200 with a company_description section present (denominator printed).
    NU  N1 NU_US_Equity serves 0 company_description sentences (R2).
Verdict: R87 WITHHELD <crit>: YES|NO (exit 0|1). At the base (live HZoC2x, 2026-10-09 ~18:4xZ): AC1 NO (NU FAILED with 1 sentence);
NU NO (1 sentence).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

# the five names with a stored draft (AMD and NVDA serve no drafted company_description section; read 2026-10-09)
KEYS = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity")
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
SECTION = "company_description"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _thesis(key, where):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "NU"])
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    ap.add_argument("--keys", default=",".join(KEYS))
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    keys = [k.strip() for k in a.keys.split(",") if k.strip()]
    failed_served, missing, nu_count = [], [], None
    for key in keys:
        code, body = _thesis(key, a.where)
        secs = [s for s in body.get("drafted_sections") or [] if s.get("section_id") == SECTION]
        if code != 200 or not secs:
            missing.append(key)
            print("   %-15s status %s, %s section present: %s" % (key, code, SECTION, bool(secs)))
            continue
        sec = secs[0]
        n = len(sec.get("sentences") or [])
        state = sec.get("description_verdict_state")
        if state == "FAILED" and n:
            failed_served.append(key)
        if key == "NU_US_Equity":
            nu_count = n
        print("   %-15s status %s verdict %-12s served sentences %d" % (key, code, state, n))
    if a.crit == "AC1":
        w1 = say(not failed_served, "W1 no served FAILED description carries a sentence: offending %s" % failed_served)
        w2 = say(not missing, "W2 every name answered with a %s section: %d of %d (missing %s)" % (
            SECTION, len(keys) - len(missing), len(keys), missing))
        ok = w1 and w2
    else:
        ok = say(nu_count == 0, "N1 NU_US_Equity serves 0 %s sentences: read %s" % (SECTION, nu_count))
    print("R87 WITHHELD %s: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
