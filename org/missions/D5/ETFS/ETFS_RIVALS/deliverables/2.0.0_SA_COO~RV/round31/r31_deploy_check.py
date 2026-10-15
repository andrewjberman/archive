"""TO-APPLY-R31 AC1 -- the round-31 code is live as the pair bounds it (read-only boto3 and zip reads).

    python r31_deploy_check.py <deploy tree>      (the applier's tree at the round-31 pin 34b2ab6351, e.g. C:/tmp/rv-r31-dell1)

(1) the five functions' CodeSha256 equal the zips built in <tree>/.runtime/rivalfunds-build/zips/, Active/Successful/3008;
(2) NOTHING ELSE MOVED: the daily Lambda's environment KEY set is exactly {RIVALFUNDS_AI_ENABLE, RIVALFUNDS_OPENAI_SECRET,
    RIVALFUNDS_SERP_SECRET, BD_SERP_ZONE}, RIVALFUNDS_SERP_SECRET equals the one ARN and BD_SERP_ZONE equals serp_opal; the other
    four carry no environment; the daily role's inline policy still has exactly two secretsmanager statements, one on exactly the ARN;
(3) the built zips carry the pin's bytes: each of rivalfunds/{dramatic_move,render,ai_accounts,ai_client,gold_trade_schedule,price_series}.py, in every zip that holds it, hashes
    (git blob id) to the pin's blob, and at least one zip holds each.
A failed read is a failure. Exit 0 = PASS, 1 = FAIL.
"""
import base64
import hashlib
import json
import pathlib
import sys
import urllib.parse
import zipfile

import boto3

TREE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "C:/tmp/rv-r31-dell1")
ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:find-insure/bright-data/api-key-7ojPkd"
DAILY = "etfs-rivalfunds-daily-lambda"
FUNCS = [DAILY, "etfs-rivalfunds-fetch-holdings-lambda", "rivalfunds-build-silver-lambda",
         "rivalfunds-build-canonical-shape-lambda", "rivalfunds-publish-page-lambda"]
BLOBS = {  # the pin 34b2ab6351 (= ea0e5025ac + the four round-31 files at the merged HEAD's bytes): git blob ids
    "rivalfunds/dramatic_move.py": "37397a1057439b90aa2a9b759beb159375e91673",        # unchanged since the round-29 pin
    "rivalfunds/render.py": "fda4ab160bb72d1f6e5b20ddf3a9df37997354fa",                # unchanged since the round-30 pin (RIV-xa-2)
    "rivalfunds/ai_accounts.py": "917e2fa12e0b2cde80d4d29d7ab864d1a9ef9fb6",           # RIV-yb-1 (the default model, the clients' temperature rule)
    "rivalfunds/ai_client.py": "2b45ec0ac8c423ae6801c1370b8045f26fa52941",              # RIV-yb-1 (the Lambda client's request)
    "rivalfunds/gold_trade_schedule.py": "928331c8de7fde907d1cdf7a66f42a4be95ac51a",   # RIV-ya-1 (G5 precedence)
    "rivalfunds/price_series.py": "4c932a816434a702648f13da0c6530d02e11d3fa",          # RIV-ya-1 (chart precedence)
}


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


lam, iam = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam")
zdir = TREE / ".runtime" / "rivalfunds-build" / "zips"
zips = sorted(zdir.glob("*.zip")) if zdir.is_dir() else []
built = {base64.b64encode(hashlib.sha256(z.read_bytes()).digest()).decode(): z.name for z in zips}
fails = []
print(f"deploy tree {TREE}: {len(zips)} built zip(s)")
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
        if set(env) != want or env.get("RIVALFUNDS_SERP_SECRET") != ARN or env.get("BD_SERP_ZONE") != "serp_opal":  # no RIVALFUNDS_AI_MODEL key is added: the model rides the code default
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
        fails.append("(2) the daily role does not carry exactly two secretsmanager statements, one on exactly the ARN")
except Exception as ex:  # noqa: BLE001
    fails.append(f"(2) ROLE READ FAILED {type(ex).__name__}: {ex}")
for member, want_blob in BLOBS.items():
    held, wrong = 0, []
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            if member in zf.namelist():
                held += 1
                if blob_id(zf.read(member)) != want_blob:
                    wrong.append(z.name)
    print(f"{member}: held by {held} of {len(zips)} zip(s), {len(wrong)} not the pin's bytes")
    if not held or wrong:
        fails.append(f"(3) {member}: held by {held} zip(s), wrong bytes in {wrong}")
for f in fails:
    print("FAIL:", f)
print(f"R31 DEPLOY RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
