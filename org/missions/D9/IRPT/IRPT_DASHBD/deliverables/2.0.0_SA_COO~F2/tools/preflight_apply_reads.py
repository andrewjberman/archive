"""IRPT_DASHBD (F-SHIP, ~F2): the READ-ONLY pre-flight of the two apply orders (TO-DB-f-2702 Inflection, TO-DB-f-2703 Cottonwood).

  python <this file>      run from the repository root, before each GO

It runs, once, the AWS calls of the checkers p139_infapply and p139_cotapply against the live world and prints counts, names and hash prefixes only: the live state each packet's section 3 states
(Inflection: the role's 13 inline policies and none new, the four code keys' version counts, the runner state, the target prefix; Cottonwood: the function's code hash and limits, the five
statements, the schedule, the artifact key's latest version, the new prefix and the returns prefix). It proves the checkers' command syntax and parsing work (first run 2026-10-17, all calls
answered) and shows the issuer a drift before it sends a GO. It writes nothing.
"""
import sys

from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r139"))
import p139_infapply as inf  # noqa: E402
import p139_cotapply as cot  # noqa: E402

R = str(ROOT)
names = inf.aws_json(R, ["iam", "list-role-policies", "--role-name", inf.ROLE])["PolicyNames"]
print("inf: role inline policies", len(names), "new ones", len([n for n in names if n not in inf.OTHER_POLICIES]))
for k, key in inf.KEYS.items():
    v = inf.aws_json(R, ["s3api", "list-object-versions", "--bucket", inf.CODE_BUCKET, "--prefix", key, "--max-items", "5"])
    print("inf: versions of", k, len([x for x in (v or {}).get("Versions", []) if x["Key"] == key]))
st = inf.aws_json(R, ["ec2", "describe-instances", "--instance-ids", inf.INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
print("inf: runner", st)
r = inf.aws_json(R, ["s3api", "list-objects-v2", "--bucket", inf.GOLD_BUCKET, "--prefix", inf.GOLD_PREFIX, "--delimiter", "/"]) or {}
print("inf: target partitions", len(r.get("CommonPrefixes", [])))

c = cot.aws_json(R, ["lambda", "get-function-configuration", "--function-name", cot.FUNCTION])
print("cot: function", c["CodeSha256"][:12], c["MemorySize"], c["Timeout"], len(c.get("Layers", [])), bool((c.get("Environment") or {}).get("Variables")))
pol = cot.aws_json(R, ["iam", "get-role-policy", "--role-name", cot.ROLE, "--policy-name", cot.POLICY])["PolicyDocument"]["Statement"]
print("cot: statements", sorted(s["Sid"] for s in pol) == sorted(cot.OLD_SIDS), [cot.statement_hash(s)[:8] for s in pol][:2])
s = cot.aws_json(R, ["scheduler", "get-schedule", "--name", cot.SCHEDULE])
print("cot: schedule", s["State"], s["ScheduleExpression"])
v = cot.aws_json(R, ["s3api", "list-object-versions", "--bucket", cot.ARTIFACT_BUCKET, "--prefix", cot.ARTIFACT_KEY, "--max-items", "3"])
print("cot: latest version", [x["VersionId"][:8] for x in v.get("Versions", []) if x["Key"] == cot.ARTIFACT_KEY and x.get("IsLatest")])
r = cot.aws_json(R, ["s3api", "list-objects-v2", "--bucket", cot.BUCKET, "--prefix", cot.TX_PREFIX, "--delimiter", "/"]) or {}
print("cot: new prefix partitions", len(r.get("CommonPrefixes", [])))
rp = cot.aws_json(R, ["s3api", "list-objects-v2", "--bucket", cot.BUCKET, "--prefix", cot.RETURNS_PREFIX, "--delimiter", "/"]) or {}
print("cot: returns partitions", len(rp.get("CommonPrefixes", [])))
