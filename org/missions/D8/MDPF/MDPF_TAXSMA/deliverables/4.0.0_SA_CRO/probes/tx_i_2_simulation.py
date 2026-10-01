"""TX-i-2 policy SIMULATION (not exercise). One resource per call; firm bucket policy passed where it applies."""
import datetime
import json
import boto3

ACCT = "313476888478"
iam = boto3.client("iam")
s3 = boto3.client("s3")
RP = "arn:aws:iam::%s:role/opal-assets-mdpf-egress-publisher-role" % ACCT
POL49 = s3.get_bucket_policy(Bucket="opal-data-49financial")["Policy"]


def sim(action, resource, prefix=None, pol=None):
    ctx = [{"ContextKeyName": "aws:PrincipalArn", "ContextKeyValues": [RP], "ContextKeyType": "string"}]
    if prefix is not None:
        ctx.append({"ContextKeyName": "s3:prefix", "ContextKeyValues": [prefix], "ContextKeyType": "string"})
    kw = {"PolicySourceArn": RP, "ActionNames": [action], "ResourceArns": [resource], "ContextEntries": ctx}
    if pol:
        kw.update(ResourcePolicy=pol, CallerArn=RP, ResourceOwner="arn:aws:iam::%s:root" % ACCT)
    try:
        return iam.simulate_principal_policy(**kw)["EvaluationResults"][0]["EvalDecision"]
    except Exception as e:  # noqa: BLE001
        for k in ("ResourcePolicy", "CallerArn", "ResourceOwner"):
            kw.pop(k, None)
        return iam.simulate_principal_policy(**kw)["EvaluationResults"][0]["EvalDecision"] + \
            " (identity policy only: %s)" % type(e).__name__


rows = [
    ("Tax control get", "s3:GetObject", "arn:aws:s3:::opal-data-mdpf/mdpf/global/state/taxsma_control/current.json", None, None, "allowed"),
    ("Tax control put", "s3:PutObject", "arn:aws:s3:::opal-data-mdpf/mdpf/global/state/taxsma_control/current.json", None, None, "DENY"),
    ("another opal-data-mdpf key get", "s3:GetObject", "arn:aws:s3:::opal-data-mdpf/mdpf/feeds/x/y/2026-09-30.parquet", None, None, "DENY"),
    ("49financial taxsma_assets get", "s3:GetObject", "arn:aws:s3:::opal-data-49financial/mdpf/49financial/gold/taxsma_assets/date=2026-09-30/data.parquet", None, POL49, "DENY"),
    ("49financial dispositions get", "s3:GetObject", "arn:aws:s3:::opal-data-49financial/mdpf/49financial/state/taxsma_membership/dispositions.json", None, POL49, "DENY"),
    ("workbook Silver get", "s3:GetObject", "arn:aws:s3:::opal-data-assets/gateway/global/silver/taxsma_workbook/date=2026-09-30/a-b.parquet", None, None, "DENY"),
    ("workbook Bronze get", "s3:GetObject", "arn:aws:s3:::opal-data-assets/gateway/global/bronze/taxsma_workbook/date=20260930/a-b.json", None, None, "DENY"),
    ("capability secret get", "secretsmanager:GetSecretValue", "arn:aws:secretsmanager:us-east-1:%s:secret:gateway/global/taxsma-workbook-token-AbCdEf" % ACCT, None, None, "DENY"),
    ("EXISTING canonical Gold get (control)", "s3:GetObject", "arn:aws:s3:::opal-data-assets/portal/gold/mdpf/49financial/category-views/2026-09-29.json", None, None, "allowed"),
    ("EXISTING served put (control)", "s3:PutObject", "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/49financial/category-views.json", None, None, "allowed"),
]
print("SIMULATION (iam simulate-principal-policy), %s, %d rows, one resource per call"
      % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), len(rows)))
bad = 0
for label, action, res, prefix, pol, expected in rows:
    got = sim(action, res, prefix, pol)
    ok = got.startswith("allowed") if expected == "allowed" else not got.startswith("allowed")
    bad += 0 if ok else 1
    print("%-4s %-40s %-30s -> %s" % ("OK" if ok else "FAIL", label, action, got))
print("rows as expected: %d of %d" % (len(rows) - bad, len(rows)))
names = iam.list_role_policies(RoleName=RP.split("/")[-1])["PolicyNames"]
print("inline policies on the role (%d): %s" % (len(names), ", ".join(sorted(names))))
doc = iam.get_role_policy(RoleName=RP.split("/")[-1], PolicyName="mdpf-publisher-taxsma-control-read-policy")["PolicyDocument"]
print("new policy:", json.dumps(doc["Statement"]))
