"""AMGT_RESAPP round 50, AMGT-yy-5 AC1 -- the ONE build landed: `opal-amgt-scoped-api` CodeSha256 differs from the base read at the cut
(`Um3BOJ+jcVc3B79VuFCn4RyD5VYu+IzCpe3BQOP/p7A=`, xx-4's act of 22:29:10Z) and LastUpdateStatus is Successful. The executor re-reads the
base immediately before the build; a moved base is a STOP and a re-sign (CTO round-49 ruling 2).
usage: python <this>"""
import sys

import boto3

PRIOR = "Um3BOJ+jcVc3B79VuFCn4RyD5VYu+IzCpe3BQOP/p7A="


def main():
    c = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
    print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (
        c["CodeSha256"], c.get("LastUpdateStatus"), c.get("LastModified"), PRIOR))
    ok = c["CodeSha256"] != PRIOR and c.get("LastUpdateStatus") == "Successful"
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
