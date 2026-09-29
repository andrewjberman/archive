"""AMGT_RESAPP round 49, AMGT-xx-4 AC1 -- the redeploy landed: `opal-amgt-scoped-api` CodeSha256 differs from the base the halves signed
(`uv0oTSMaW3gDvq0H/pn64hORUYCYFAzWN7OsjC2x+Ng=`, AMGT_HARVST HVST-i-4's act of 21:57:59Z) and LastUpdateStatus is Successful.
AMENDMENT 1: the cut named round 48's lg6NJ2JL..., which i-4 had already replaced, so this read passed BEFORE the act (0.7.0_AE_CloudOps~A, msg 26747).
usage: python <this>"""
import sys

import boto3

PRIOR = "uv0oTSMaW3gDvq0H/pn64hORUYCYFAzWN7OsjC2x+Ng="


def main():
    c = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
    print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (
        c["CodeSha256"], c.get("LastUpdateStatus"), c.get("LastModified"), PRIOR))
    ok = c["CodeSha256"] != PRIOR and c.get("LastUpdateStatus") == "Successful"
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
