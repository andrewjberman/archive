"""AMGT_RESAPP round 49, AMGT-xx-4 AC1 -- the redeploy landed: `opal-amgt-scoped-api` CodeSha256 differs from round 48's served
`lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s=` and LastUpdateStatus is Successful.
usage: python <this>"""
import sys

import boto3

PRIOR = "lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s="


def main():
    c = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
    print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (
        c["CodeSha256"], c.get("LastUpdateStatus"), c.get("LastModified"), PRIOR))
    ok = c["CodeSha256"] != PRIOR and c.get("LastUpdateStatus") == "Successful"
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
