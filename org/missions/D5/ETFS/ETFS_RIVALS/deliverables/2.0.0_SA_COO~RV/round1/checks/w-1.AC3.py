"""RIV-w-1 AC3 -- comp-iam instrument: the gateway's new read policy, simulated by IAM itself.

Page objects GET: allowed. List with s3:prefix = the page prefix: allowed. GET on issuer bronze, PUT or DELETE on a
page object, List with another prefix: denied. The policy is read from the JSON file the Terraform loads."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    import boto3

    root = c.setup_path()
    pol_p = root / "infra" / "aws" / "terraform" / "opal-gateway" / "rivalfunds-iam.policy.json"
    tf_p = root / "infra" / "aws" / "terraform" / "opal-gateway" / "rivalfunds-iam.tf"
    v.check(pol_p.exists() and tf_p.exists(), "policy JSON and its Terraform exist")
    if not pol_p.exists():
        return
    v.check("rivalfunds-iam.policy.json" in tf_p.read_text(encoding="utf-8"), "the Terraform loads that policy file")
    doc = pol_p.read_text(encoding="utf-8")
    page = c.address("rivalfunds", "etfs", "platinum", "page", "date=2026-09-29", "index.html")
    bronze = c.address("issuer-site", "etfs", "bronze", "holdings", "date=2026-09-29", "x.txt")
    bucket = page.split("/")[2]
    page_prefix = page.split("/", 3)[3].rsplit("date=", 1)[0]
    arn = lambda u: "arn:aws:s3:::" + u[len("s3://"):]  # noqa: E731
    iam = boto3.client("iam")

    def sim(action, resource, ctx=None):
        kw = {"PolicyInputList": [doc], "ActionNames": [action], "ResourceArns": [resource]}
        if ctx:
            kw["ContextEntries"] = [{"ContextKeyName": "s3:prefix", "ContextKeyValues": [ctx], "ContextKeyType": "string"}]
        return iam.simulate_custom_policy(**kw)["EvaluationResults"][0]["EvalDecision"]

    cases = [
        ("s3:GetObject", arn(page), None, "allowed"),
        ("s3:ListBucket", f"arn:aws:s3:::{bucket}", page_prefix, "allowed"),
        ("s3:GetObject", arn(bronze), None, "denied"),
        ("s3:PutObject", arn(page), None, "denied"),
        ("s3:DeleteObject", arn(page), None, "denied"),
        ("s3:ListBucket", f"arn:aws:s3:::{bucket}", "issuer-site/", "denied"),
    ]
    for action, res, ctx, want in cases:
        got = sim(action, res, ctx)
        ok = (got == "allowed") if want == "allowed" else (got != "allowed")
        v.check(ok, f"{action} {res}{' prefix=' + ctx if ctx else ''}: {got} (want {want})")
    stmts = json.loads(doc).get("Statement", [])
    acts = {a for s in stmts for a in ([s["Action"]] if isinstance(s.get("Action"), str) else s.get("Action", []))}
    v.check(acts <= {"s3:GetObject", "s3:ListBucket"}, f"the policy grants only GetObject/ListBucket ({sorted(acts)})")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
