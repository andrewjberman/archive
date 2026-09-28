"""AMGT_RESAPP round 46, AMGT-uu-4 AC1 -- the deployed code MOVED from round 45's tt-2 deploy
(vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew=) and the last update is Successful. A read.
usage (repo root): python <this>"""
import sys

import boto3

PRIOR = "vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew="
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
sha, status = cfg.get("CodeSha256"), cfg.get("LastUpdateStatus")
print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (sha, status, cfg.get("LastModified"), PRIOR))
sys.exit(0 if sha and sha != PRIOR and status == "Successful" else 1)
