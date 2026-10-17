"""Read-only REHEARSAL of packet Act 3 (no change): does the simulator honor the bucket fence by principal ARN?
A control principal that matches role/*-inf-* (an existing builder-named role) is simulated with the planned four-statement gold PutObject statement as an
input policy and the live opal-data-inflection bucket policy as the resource policy; the runner role (name does not match) is the negative arm.
Decisions only."""
import json
import subprocess
import sys
from pathlib import Path

AWS = str(Path("C:/dev/ajb_workspace/.tools/aws.cmd"))
BUCKET = "opal-data-inflection"
KEY = "arn:aws:s3:::opal-data-inflection/irpt/inflection/gold/account_transaction/date=2026-10-16/data.parquet"


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or r.stdout)[-160:]
    return json.loads(r.stdout or "null"), None


cand = sys.argv[1:]
bp, err = aws("s3api", "get-bucket-policy", "--bucket", BUCKET)
if bp is None:
    raise SystemExit("bucket policy read failed: " + str(err))
policy = bp["Policy"]
planned = json.dumps({"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": [KEY.rsplit("/date=", 1)[0] + "/*"]}]})
for name in cand:
    role, err = aws("iam", "get-role", "--role-name", name)
    if role is None:
        print(name, "| role read:", "absent" if "NoSuchEntity" in str(err) else err)
        continue
    arn = role["Role"]["Arn"]
    for with_rp in (False, True):
        cmd = ["iam", "simulate-principal-policy", "--policy-source-arn", arn, "--action-names", "s3:PutObject", "--resource-arns", KEY, "--policy-input-list", planned]
        if with_rp:
            cmd += ["--resource-policy", policy]
        res, err = aws(*cmd)
        if res is None:
            print(name, "| simulate failed:", err)
            continue
        e = res["EvaluationResults"][0]
        print("%s | resource policy %s -> %s | matched: %s" % (name, "INCLUDED" if with_rp else "not included", e["EvalDecision"], [m["SourcePolicyId"] for m in e.get("MatchedStatements", [])][:4]))
