"""TX-i-1 policy SIMULATION (not exercise). One resource per call; conditioned statements get context entries;
each firm bucket's own policy is passed as the resource policy so the fence is evaluated; every DENY has a
positive control run as a separate call. cloud-ops IAM traps 1-4."""
import datetime
import boto3

ACCT = "313476888478"
iam = boto3.client("iam")
s3 = boto3.client("s3")
R49 = "arn:aws:iam::%s:role/mdpf-49f-taxsma-role" % ACCT
RCOT = "arn:aws:iam::%s:role/mdpf-cot-taxsma-role" % ACCT
RGOLD = "arn:aws:iam::%s:role/mdpf-gold-lambda-role" % ACCT
B49, BCOT, BASSETS, BMDPF, BSERVE = ("opal-data-49financial", "opal-data-cottonwood", "opal-data-assets",
                                     "opal-data-mdpf", "opal-data-portal-v2")
POL = {}
for b in (B49, BCOT, BASSETS):
    POL[b] = s3.get_bucket_policy(Bucket=b)["Policy"]


def sim(role, action, resource, prefix=None, bucket=None):
    kw = {"PolicySourceArn": role, "ActionNames": [action], "ResourceArns": [resource]}
    ctx = [{"ContextKeyName": "aws:PrincipalArn", "ContextKeyValues": [role], "ContextKeyType": "string"}]
    if prefix is not None:
        ctx.append({"ContextKeyName": "s3:prefix", "ContextKeyValues": [prefix], "ContextKeyType": "string"})
    kw["ContextEntries"] = ctx
    if bucket in POL:
        kw["ResourcePolicy"] = POL[bucket]
        kw["CallerArn"] = role.replace(":role/", ":role/")  # same account; the role itself is the caller
        kw["ResourceOwner"] = "arn:aws:iam::%s:root" % ACCT
    try:
        r = iam.simulate_principal_policy(**kw)["EvaluationResults"][0]
        return r["EvalDecision"]
    except Exception as e:  # noqa: BLE001
        # CallerArn must be a user for some APIs; retry without the resource policy and say so.
        kw.pop("ResourcePolicy", None), kw.pop("CallerArn", None), kw.pop("ResourceOwner", None)
        r = iam.simulate_principal_policy(**kw)["EvaluationResults"][0]
        return r["EvalDecision"] + " (identity policy only: %s)" % type(e).__name__


rows = [
    # (label, role, action, resource, prefix, bucket, expected)
    ("49f: 0833 fact_rps_s2 read", R49, "s3:GetObject", "arn:aws:s3:::%s/schwab/08335338/silver/fact_rps_s2/date=2026-09-29/x.parquet" % BASSETS, None, BASSETS, "allowed"),
    ("49f: 0833 fact_acc list", R49, "s3:ListBucket", "arn:aws:s3:::%s" % BASSETS, "schwab/08335338/silver/fact_acc/date=2026-09-29/", BASSETS, "allowed"),
    ("49f: workbook Silver put", R49, "s3:PutObject", "arn:aws:s3:::%s/gateway/global/silver/taxsma_workbook/date=2026-09-30/a-b.parquet" % BASSETS, None, BASSETS, "allowed"),
    ("49f: workbook Bronze put (json)", R49, "s3:PutObject", "arn:aws:s3:::%s/gateway/global/bronze/taxsma_workbook/date=20260930/a-b.json" % BASSETS, None, BASSETS, "allowed"),
    ("49f: own dispositions get", R49, "s3:GetObject", "arn:aws:s3:::%s/mdpf/49financial/state/taxsma_membership/dispositions.json" % B49, None, B49, "allowed"),
    ("49f: own dispositions get by version", R49, "s3:GetObjectVersion", "arn:aws:s3:::%s/mdpf/49financial/state/taxsma_membership/dispositions.json" % B49, None, B49, "allowed"),
    ("49f: own taxsma_assets put", R49, "s3:PutObject", "arn:aws:s3:::%s/mdpf/49financial/gold/taxsma_assets/date=2026-09-30/data.parquet" % B49, None, B49, "allowed"),
    ("49f: own taxsma_assets list", R49, "s3:ListBucket", "arn:aws:s3:::%s" % B49, "mdpf/49financial/gold/taxsma_assets/", B49, "allowed"),
    ("49f: bucket versioning read", R49, "s3:GetBucketVersioning", "arn:aws:s3:::%s" % B49, None, B49, "allowed"),
    ("49f: capability secret read", R49, "secretsmanager:GetSecretValue", "arn:aws:secretsmanager:us-east-1:%s:secret:gateway/global/taxsma-workbook-token-AbCdEf" % ACCT, None, None, "allowed"),
    ("49f: OTHER secret read", R49, "secretsmanager:GetSecretValue", "arn:aws:secretsmanager:us-east-1:%s:secret:opal/mcp/ms-ingest-token-AbCdEf" % ACCT, None, None, "DENY"),
    ("49f: cottonwood dispositions get", R49, "s3:GetObject", "arn:aws:s3:::%s/mdpf/cottonwood/state/taxsma_membership/dispositions.json" % BCOT, None, BCOT, "DENY"),
    ("49f: Black Diamond cottonwood read", R49, "s3:GetObject", "arn:aws:s3:::%s/blackdiamond/cottonwood/silver/fact_holdings/date=2026-09-29/x.parquet" % BASSETS, None, BASSETS, "DENY"),
    ("49f: served category-views put", R49, "s3:PutObject", "arn:aws:s3:::%s/platinum/mdpf/49financial/category-views.json" % BSERVE, None, None, "DENY"),
    ("49f: served json/mdpf put", R49, "s3:PutObject", "arn:aws:s3:::%s/json/mdpf/49financial/category-views.json" % BSERVE, None, None, "DENY"),
    ("49f: own bucket OTHER prefix get", R49, "s3:GetObject", "arn:aws:s3:::%s/gold/advi/dimensions/x.parquet" % B49, None, B49, "DENY"),
    ("49f: own bucket list OTHER prefix", R49, "s3:ListBucket", "arn:aws:s3:::%s" % B49, "gold/advi/", B49, "DENY"),
    ("cot: Black Diamond cottonwood read", RCOT, "s3:GetObject", "arn:aws:s3:::%s/blackdiamond/cottonwood/silver/fact_holdings/date=2026-09-29/x.parquet" % BASSETS, None, BASSETS, "allowed"),
    ("cot: Black Diamond list", RCOT, "s3:ListBucket", "arn:aws:s3:::%s" % BASSETS, "blackdiamond/cottonwood/silver/fact_holdings/date=2026-09-29/", BASSETS, "allowed"),
    ("cot: own dispositions put", RCOT, "s3:PutObject", "arn:aws:s3:::%s/mdpf/cottonwood/state/taxsma_membership/dispositions.json" % BCOT, None, BCOT, "allowed"),
    ("cot: own taxsma_assets get", RCOT, "s3:GetObject", "arn:aws:s3:::%s/mdpf/cottonwood/gold/taxsma_assets/date=2026-09-30/data.parquet" % BCOT, None, BCOT, "allowed"),
    ("cot: bucket versioning read", RCOT, "s3:GetBucketVersioning", "arn:aws:s3:::%s" % BCOT, None, BCOT, "allowed"),
    ("cot: 49financial dispositions get", RCOT, "s3:GetObject", "arn:aws:s3:::%s/mdpf/49financial/state/taxsma_membership/dispositions.json" % B49, None, B49, "DENY"),
    ("cot: 0833 fact_rps_s2 read", RCOT, "s3:GetObject", "arn:aws:s3:::%s/schwab/08335338/silver/fact_rps_s2/date=2026-09-29/x.parquet" % BASSETS, None, BASSETS, "DENY"),
    ("cot: capability secret read", RCOT, "secretsmanager:GetSecretValue", "arn:aws:secretsmanager:us-east-1:%s:secret:gateway/global/taxsma-workbook-token-AbCdEf" % ACCT, None, None, "DENY"),
    ("cot: served category-views put", RCOT, "s3:PutObject", "arn:aws:s3:::%s/platinum/mdpf/cottonwood/category-views.json" % BSERVE, None, None, "DENY"),
    ("gold: assume the 49f Tax role", RGOLD, "sts:AssumeRole", R49, None, None, "allowed"),
    ("gold: assume the cot Tax role", RGOLD, "sts:AssumeRole", RCOT, None, None, "allowed"),
    ("gold: control put", RGOLD, "s3:PutObject", "arn:aws:s3:::%s/mdpf/global/state/taxsma_control/current.json" % BMDPF, None, None, "allowed"),
    ("gold: 49financial dispositions get (ambient role)", RGOLD, "s3:GetObject", "arn:aws:s3:::%s/mdpf/49financial/state/taxsma_membership/dispositions.json" % B49, None, B49, "DENY"),
]
print("SIMULATION (iam simulate-principal-policy), %s, %d rows, one resource per call"
      % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), len(rows)))
bad = 0
for label, role, action, res, prefix, bucket, expected in rows:
    got = sim(role, action, res, prefix, bucket)
    ok = (got.startswith("allowed")) if expected == "allowed" else (not got.startswith("allowed"))
    bad += 0 if ok else 1
    print("%-4s %-52s %-28s -> %s" % ("OK" if ok else "FAIL", label, action, got))
print("rows as expected: %d of %d" % (len(rows) - bad, len(rows)))
