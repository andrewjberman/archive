"""CT-a-1 AMENDMENT 15 item 2, the stop-condition read: which statement refuses the Dell users' s3:PutObject on the Cottonwood, Inflection and Black Diamond code prefixes?
Reads LIVE with iam:SimulatePrincipalPolicy (read-only; no object is touched, no secret read). Prints the decision and the matched policy per user and key."""
import boto3
iam = boto3.client("iam", region_name="us-east-1")
res = ["arn:aws:s3:::opal-data-bd/code/bronze/cot_bronze_ingest.py","arn:aws:s3:::opal-data-bd/code/silver/cot_silver_merge.py","arn:aws:s3:::opal-data-bd/code/gold/gold_dispatch.sh",
 "arn:aws:s3:::opal-data-bd/code/gold/09_generate_partner_analytics.py","arn:aws:s3:::opal-data-bd/code/gold/lib/advisor_nna_attribution.py","arn:aws:s3:::opal-data-bd/code/canonical-schwab-runner/run-canonical.sh",
 "arn:aws:s3:::opal-data-bd/code/bronze/templates/fees.json",
 "arn:aws:s3:::opal-data-cot/code/gold/gold_dispatch.sh","arn:aws:s3:::opal-data-cot/code/gold/x.py","arn:aws:s3:::opal-data-cot/code/bronze/cot_bronze_ingest.py","arn:aws:s3:::opal-data-cot/code/silver/cot_silver_merge.py",
 "arn:aws:s3:::opal-data-inf/code/exporter/inf-jwt-fetch.sh","arn:aws:s3:::opal-data-inf/code/exporter/stepwise/a.sh","arn:aws:s3:::opal-data-inf/code/gold/x.py"]
for u in ("cloudops-dell1-agent-user","cloudops-dell2-agent-user"):
    for act in ("s3:PutObject",):
        r = iam.simulate_principal_policy(PolicySourceArn="arn:aws:iam::313476888478:user/"+u, ActionNames=[act], ResourceArns=res)
        for e in r["EvaluationResults"]:
            for x in e.get("ResourceSpecificResults", []):
                print(u.split("-")[1], x["EvalResourceName"].split(":::")[1], x["EvalResourceDecision"], [m["SourcePolicyId"] for m in x.get("MatchedStatements", [])])
