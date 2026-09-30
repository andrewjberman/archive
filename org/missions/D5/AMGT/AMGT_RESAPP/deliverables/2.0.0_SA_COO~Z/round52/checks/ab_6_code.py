"""AMGT_RESAPP round 52, AMGT-ab-6 -- the ONE build landed: the deployed `opal-amgt-scoped-api` CodeSha256 differs from the base the halves
sign (`zHpr7FhS+irmKofIuKNqTkQm2hj7x2fvS1rrX1ohkfQ=`, zz-8's act) and LastUpdateStatus is Successful.
usage: python <this>   (from the repo root; lambda:GetFunctionConfiguration only)"""
import sys

import boto3

PRIOR = "zHpr7FhS+irmKofIuKNqTkQm2hj7x2fvS1rrX1ohkfQ="


def main():
    c = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
    print("deployed CodeSha256 %s LastModified %s LastUpdateStatus %s (base %s)" % (
        c["CodeSha256"], c["LastModified"], c.get("LastUpdateStatus"), PRIOR))
    ok = c["CodeSha256"] != PRIOR and c.get("LastUpdateStatus") == "Successful"
    print("THE ONE BUILD LANDED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
