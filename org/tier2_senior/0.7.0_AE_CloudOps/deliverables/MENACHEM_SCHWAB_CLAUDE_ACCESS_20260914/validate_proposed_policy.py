"""Read-only IAM simulation of the proposed source-reader policy; creates no AWS resources."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import boto3

HERE = Path(__file__).resolve().parent
policy = json.loads((HERE / "reader-role-policy.proposed.json").read_text())
session = boto3.Session()
account = session.client("sts").get_caller_identity()["Account"]
if account != "313476888478":
    raise SystemExit("Wrong AWS account; simulation stopped")
iam = session.client("iam")
bucket = "arn:aws:s3:::opal-data-assets"
cases = []
def add(name, action, resource, expected, prefix=None, additive=False):
    cases.append(dict(name=name, action=action, resource=resource, expected=expected,
                      prefix=prefix, additive_allow_all_s3=additive))
for master in ("08242234", "08335338"):
    for dataset in ("dim_position", "dim_balance", "dim_asset"):
        prefix = f"schwab/{master}/silver/{dataset}/"
        add(f"read-{master}-{dataset}", "s3:GetObject", bucket + "/" + prefix + "date=2026-09-11/data.parquet", "allowed")
        add(f"list-{master}-{dataset}", "s3:ListBucket", bucket, "allowed", prefix)
add("pinned-version", "s3:GetObjectVersion", bucket + "/schwab/08335338/silver/dim_position/date=2026-09-11/data.parquet", "allowed")
for label, suffix in [
    ("account-pii", "schwab/08242234/silver/fact_acc/date=2026-09-11/data.parquet"),
    ("raw", "schwab/08335338/bronze/vendor.zip"),
    ("third-master", "schwab/99999999/silver/dim_position/date=2026-09-11/data.parquet"),
    ("lookalike-dataset", "schwab/08242234/silver/dim_position_extra/data.parquet"),
    ("config", "config/settings.json"),
    ("other-source", "blackdiamond/49f/gold/data.parquet"),
]:
    add(label, "s3:GetObject", bucket + "/" + suffix, "explicitDeny", additive=True)
for label, prefix in [("root-list", ""), ("master-list", "schwab/08242234/"), ("missing-prefix", None),
                      ("other-prefix", "config/"), ("lookalike-list", "schwab/08335338/silver/dim_asset_extra/")]:
    add(label, "s3:ListBucket", bucket, "explicitDeny", prefix, additive=True)
add("other-bucket-read", "s3:GetObject", "arn:aws:s3:::opal-data-portal-v2/json/file.json", "explicitDeny", additive=True)
add("other-bucket-list", "s3:ListBucket", "arn:aws:s3:::opal-data-portal-v2", "explicitDeny",
    "schwab/08242234/silver/dim_position/", True)
key = bucket + "/schwab/08242234/silver/dim_position/date=2026-09-11/data.parquet"
for action in ("s3:PutObject", "s3:DeleteObject", "s3:DeleteObjectVersion", "s3:PutObjectAcl",
               "s3:PutObjectTagging", "s3:RestoreObject", "s3:AbortMultipartUpload"):
    add(action, action, key, "explicitDeny", additive=True)
for action in ("s3:PutBucketPolicy", "s3:PutBucketAcl", "s3:PutBucketVersioning", "s3:PutLifecycleConfiguration",
               "s3:DeleteBucket", "s3:ListBucketVersions"):
    add(action, action, bucket, "explicitDeny", additive=True)
add("no-role-chain", "sts:AssumeRole", "arn:aws:iam::313476888478:role/other-role", "explicitDeny")
add("no-iam-change", "iam:AttachRolePolicy", "arn:aws:iam::313476888478:role/other-role", "explicitDeny")

def run(case):
    policies = [json.dumps(policy)]
    if case["additive_allow_all_s3"]:
        policies.append(json.dumps({"Version": "2012-10-17", "Statement": [{
            "Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}))
    args = dict(PolicyInputList=policies, ActionNames=[case["action"]], ResourceArns=[case["resource"]])
    if case["prefix"] is not None:
        args["ContextEntries"] = [{"ContextKeyName": "s3:prefix", "ContextKeyType": "string",
                                   "ContextKeyValues": [case["prefix"]]}]
    try:
        result = iam.simulate_custom_policy(**args)["EvaluationResults"][0]
        return dict(case, decision=result["EvalDecision"],
                    missing_context=result.get("MissingContextValues", []),
                    passed=result["EvalDecision"] == case["expected"])
    except Exception as exc:
        return dict(case, error=str(exc), passed=False)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(run, cases))
report = {
    "measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "method": "IAM SimulateCustomPolicy, one action and resource per request; supplied policies only",
    "account": account, "total": len(results), "passed": sum(c["passed"] for c in results),
    "limitations": [
        "MODEL ONLY: no policy attached and no actual S3 write or delete attempted.",
        "Does not prove runtime authentication, application filters, role trust, SCPs, boundaries, or live resource policies.",
        "Negative S3 cases include a deliberately broad additive s3:* allow to check explicit-deny fences.",
        "Live end-to-end tests with dedicated test principals remain a rollout acceptance requirement."
    ],
    "cases": results
}
(HERE / "iam-simulation-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"total": report["total"], "passed": report["passed"],
                  "failures": [r for r in results if not r["passed"]]}, indent=2))
raise SystemExit(0 if report["total"] == report["passed"] else 1)

