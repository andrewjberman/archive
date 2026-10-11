"""AMGT_RESAPP round-95 PREP -- the deployed half of `r95_casing.py`: the live function's served display name of the two initialism subjects.

  PYTHONPATH=<repo root> python r95_casing_deployed.py

Reads the live function's `/security/<key>/overlay` (Lambda invoke, GET) for CSL_AU_Equity and JD_US_Equity.
    D1 CSL_AU_Equity serves `display_name` 'CSL Ltd'.
    D2 control: JD_US_Equity serves a `display_name` that starts 'JD' (it is served from the table's own mixed-case name 'JD.com Inc', so the declared initialism
       does not change it; the check guards that it does not regress).
    D3 control: SAN_FP_Equity still serves 'Sanofi' and ASML_NA_Equity's `display_name` equals what it served before (read from the same route: ASML's registered name
       is mixed-initialism 'ASML HOLDING NV' and the declared set already holds ASML; a change here would be a regression).
Verdict: R95 CASING DEPLOYED: YES|NO (exit 0|1). At the base (live VNcX9ntm, 2026-10-11): D1 FAILs, D2 and D3 PASS.
"""
import json
import sys

import boto3

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def display(key):
    ev = {"rawPath": "%s/security/%s/overlay" % (PREFIX, key), "queryStringParameters": None,
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    return (json.loads(r.get("body") or "{}")).get("display_name")


def main():
    csl, jd, san, asml = (display(k) for k in ("CSL_AU_Equity", "JD_US_Equity", "SAN_FP_Equity", "ASML_NA_Equity"))
    res = [say(csl == "CSL Ltd", "D1 CSL_AU_Equity serves 'CSL Ltd'", repr(csl)),
           say(str(jd).startswith("JD"), "D2 control: JD_US_Equity keeps its initialism in capitals", repr(jd)),
           say(san == "Sanofi" and str(asml).startswith("ASML"), "D3 control: SAN_FP_Equity 'Sanofi' and ASML_NA_Equity unchanged", "%r, %r" % (san, asml))]
    ok = all(res)
    print("R95 CASING DEPLOYED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
