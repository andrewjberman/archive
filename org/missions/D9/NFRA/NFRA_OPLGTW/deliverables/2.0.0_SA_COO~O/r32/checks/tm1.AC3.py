"""OPLGTW OG-tm-1 AC3 (FWD-13, gateway side): the two gateway Schwab roles reach 08403355 exactly as they reach the others.

IAM policy simulation against the LIVE roles (iam:SimulatePrincipalPolicy):
  - gateway-schwab-read-role: s3:GetObject ALLOWED on schwab/08403355/silver/<each of the four served datasets>/x;
  - gateway-schwab-catalog-read-role: s3:GetObject ALLOWED on schwab/08403355/meta/complete/date=2026-01-02.json;
  - negative control (difference): both roles DENIED s3:GetObject on schwab/08403355/bronze/x and on
    schwab/08403355/silver/fact_acc/x, as they are for 08335338 (read in the same run, same decision expected).
"""
import sys

import boto3

ACCOUNT = "313476888478"
NEW, CTL = "08403355", "08335338"
SERVED = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def decide(iam, role, key):
    r = iam.simulate_principal_policy(PolicySourceArn="arn:aws:iam::%s:role/%s" % (ACCOUNT, role),
                                      ActionNames=["s3:GetObject"],
                                      ResourceArns=["arn:aws:s3:::opal-data-assets/" + key])
    return r["EvaluationResults"][0]["EvalDecision"]


def main():
    iam = boto3.client("iam")
    ok = True
    checks = []
    for ds in SERVED:
        checks.append(("gateway-schwab-read-role", "schwab/%s/silver/%s/date=2026-01-02/data.parquet" % (NEW, ds), "allowed"))
    checks.append(("gateway-schwab-catalog-read-role", "schwab/%s/meta/complete/date=2026-01-02.json" % NEW, "allowed"))
    for m in (NEW, CTL):
        for role in ("gateway-schwab-read-role", "gateway-schwab-catalog-read-role"):
            checks.append((role, "schwab/%s/bronze/x" % m, "denied"))
            checks.append((role, "schwab/%s/silver/fact_acc/date=2026-01-02/data.parquet" % m, "denied"))
    for role, key, want in checks:
        got = decide(iam, role, key)
        good = (got == "allowed") == (want == "allowed")
        print("%s %s s3:GetObject %s -> %s (want %s)" % ("OK  " if good else "FAIL", role, key, got, want))
        ok = ok and good
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
