"""AMGT_RESAPP round 43, AMGT-rr-3 AC1 -- the deployed code MOVED from round 42's rq-2 deploy
(FOF+dRXoW1KFFzD0moLigsMB2LMmIjwhwURq7FkCzbw=) and the last update is Successful. A read.
usage (repo root): python <this>"""
import sys

import boto3

PRIOR = "FOF+dRXoW1KFFzD0moLigsMB2LMmIjwhwURq7FkCzbw="
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
sha, status = cfg.get("CodeSha256"), cfg.get("LastUpdateStatus")
print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (sha, status, cfg.get("LastModified"), PRIOR))
sys.exit(0 if sha and sha != PRIOR and status == "Successful" else 1)
