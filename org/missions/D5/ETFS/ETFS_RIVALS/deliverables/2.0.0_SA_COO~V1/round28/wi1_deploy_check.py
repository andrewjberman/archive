"""TO-APPLY-WI1 AC1 -- the lookup deploy is live as the pair bounds it (read-only boto3).

    python wi1_deploy_check.py [<deploy tree, default C:/tmp/rv-wi1-dell1>]

(1) the five functions' CodeSha256 equal the zips built in <tree>/.runtime/rivalfunds-build/zips/, Active/Successful/3008;
(2) the daily Lambda's environment KEY set is exactly {RIVALFUNDS_AI_ENABLE, RIVALFUNDS_OPENAI_SECRET, RIVALFUNDS_SERP_SECRET,
    BD_SERP_ZONE}, RIVALFUNDS_SERP_SECRET equals the one ARN and BD_SERP_ZONE equals serp_opal (neither is a secret value);
    the other four functions carry no environment;
(3) the daily role's inline policy (role and policy names from the tree's generated.auto.tfvars.json) carries exactly two
    secretsmanager statements, one of them GetSecretValue on exactly the ARN, no wildcard.
A failed read is a failure. Exit 0 = PASS, 1 = FAIL.
"""
import base64
import hashlib
import json
import pathlib
import sys
import urllib.parse

import boto3

TREE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "C:/tmp/rv-wi1-dell1")
ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:find-insure/bright-data/api-key-7ojPkd"
DAILY = "etfs-rivalfunds-daily-lambda"
FUNCS = [DAILY, "etfs-rivalfunds-fetch-holdings-lambda", "rivalfunds-build-silver-lambda",
         "rivalfunds-build-canonical-shape-lambda", "rivalfunds-publish-page-lambda"]
lam, iam = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam")
zdir = TREE / ".runtime" / "rivalfunds-build" / "zips"
built = {base64.b64encode(hashlib.sha256(z.read_bytes()).digest()).decode(): z.name
         for z in (sorted(zdir.glob("*.zip")) if zdir.is_dir() else [])}
fails = []
print(f"deploy tree {TREE}: {len(built)} built zip(s)")
for fn in FUNCS:
    try:
        c = lam.get_function_configuration(FunctionName=fn)
    except Exception as ex:  # noqa: BLE001
        fails.append(f"(1) {fn}: READ FAILED {type(ex).__name__}")
        continue
    env = (c.get("Environment") or {}).get("Variables", {})
    print(f"{fn}: CodeSha256 {c['CodeSha256'][:12]} built-zip {built.get(c['CodeSha256'], 'NONE')} "
          f"{c['State']}/{c['LastUpdateStatus']}/{c['MemorySize']} env-keys {sorted(env)}")
    if c["CodeSha256"] not in built or (c["State"], c["LastUpdateStatus"], c["MemorySize"]) != ("Active", "Successful", 3008):
        fails.append(f"(1) {fn}: not a built package, or not Active/Successful/3008")
    if fn == DAILY:
        want = {"RIVALFUNDS_AI_ENABLE", "RIVALFUNDS_OPENAI_SECRET", "RIVALFUNDS_SERP_SECRET", "BD_SERP_ZONE"}
        if set(env) != want or env.get("RIVALFUNDS_SERP_SECRET") != ARN or env.get("BD_SERP_ZONE") != "serp_opal":
            fails.append("(2) the daily environment is not the four keys with the ARN and serp_opal")
    elif env:
        fails.append(f"(2) {fn} carries an environment")
try:
    tf = json.loads((TREE / "infra/aws/terraform/etfs-rivalfunds/generated.auto.tfvars.json").read_text(encoding="utf-8"))
    d = tf["lambdas"][DAILY]
    doc = iam.get_role_policy(RoleName=d["role_name"], PolicyName=d["policy_name"])["PolicyDocument"]
    doc = json.loads(urllib.parse.unquote(doc)) if isinstance(doc, str) else doc
    sm = [st for st in doc["Statement"] if any(str(a).startswith("secretsmanager:") for a in
                                                (st["Action"] if isinstance(st["Action"], list) else [st["Action"]]))]
    res = [st["Resource"] if isinstance(st["Resource"], list) else [st["Resource"]] for st in sm]
    print(f"daily role {d['role_name']} policy {d['policy_name']}: secretsmanager statements {len(sm)} resources {res}")
    if len(sm) != 2 or [ARN] not in res:
        fails.append("(3) the daily role does not carry exactly two secretsmanager statements, one on exactly the ARN")
except Exception as ex:  # noqa: BLE001
    fails.append(f"(3) READ FAILED {type(ex).__name__}: {ex}")
for f in fails:
    print("FAIL:", f)
print(f"WI1 DEPLOY RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
