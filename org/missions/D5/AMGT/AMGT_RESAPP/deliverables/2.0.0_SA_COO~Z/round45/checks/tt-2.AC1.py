"""AMGT_RESAPP round 45, AMGT-tt-2 AC1 -- the deployed code MOVED from round 44's rs-2 deploy
(LK9h47juBfZPaAyfztAxDe9z65W2ZtEw6H2IJ/DcO4s=) and the last update is Successful. A read.
usage (repo root): python <this>"""
import sys

import boto3

PRIOR = "LK9h47juBfZPaAyfztAxDe9z65W2ZtEw6H2IJ/DcO4s="
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
sha, status = cfg.get("CodeSha256"), cfg.get("LastUpdateStatus")
print("CodeSha256=%s LastUpdateStatus=%s LastModified=%s (prior %s)" % (sha, status, cfg.get("LastModified"), PRIOR))
sys.exit(0 if sha and sha != PRIOR and status == "Successful" else 1)
