"""AMGT_RESAPP round 42, AMGT-rq-2 AC1 -- the deployed code MOVED: opal-amgt-scoped-api's CodeSha256 differs from round 40's
B2 deploy (pmH20bb+L1Kcejf4MKS4tVt+tCIPgeHwSZAsTe+nXZo=) and the last update is Successful. A read.
usage (repo root): python <this>"""
import sys

import boto3

PRIOR = "pmH20bb+L1Kcejf4MKS4tVt+tCIPgeHwSZAsTe+nXZo="
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
sha, status = cfg.get("CodeSha256"), cfg.get("LastUpdateStatus")
print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (sha, status, cfg.get("LastModified"), PRIOR))
sys.exit(0 if sha and sha != PRIOR and status == "Successful" else 1)
