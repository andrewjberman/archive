#!/usr/bin/env bash
# OG-rl-11 PHASE B post-deploy reads, run IMMEDIATELY after r25_verify.sh after (never run by the Phase A worker against an installed release).
# usage: bash r25_postdeploy.sh <40-hex deployed sha> <state.json written by r25_verify.sh before>      (run from the release-owning worktree root; HOST RUNS ONE AT A TIME, row Z-W28-S9)
# Writes, through the INSTALLED code (never a staged copy), in this directory:
#   RL11_SEND.json    {"body", "ssm_command_id", "instance_id"}  RL11S_DIGEST attested   (rl11.AC2)
#   RL11_SCOPES.json  same shape, RL11C_DIGEST attested                                  (rl11.AC3)
#   RL11_FLOOR.json   the two standing properties re-read: the r24 portal login and the r23 real-holder read (query + download) on the installed code
# The known execution id (the 2026-10-07 ~01:26Z run) is read read-only from the portal's execution table at run time and passed to the host ONLY inside the SSM parameters
# (the runner redacts it from the output); it is never written to the repository.
set -u
SHA="$1"; STATE="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"; export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~28}"
TB=$(python -c "import json,sys;print(len(json.load(open(sys.argv[1],encoding='utf-8'))['tools']))" "$STATE" | tr -d '\r')
EXEC_JSON=$(python - <<'PY'
import boto3, json
from boto3.dynamodb.conditions import Key
t = boto3.resource("dynamodb", region_name="us-east-1").Table("opal-data-refresh-executions")
items, kw = [], dict(KeyConditionExpression=Key("PK").eq("EXECUTION"), ProjectionExpression="SK, startedAt")
while True:
    r = t.query(**kw); items += r["Items"]
    if "LastEvaluatedKey" not in r: break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
w = [i for i in items if i.get("startedAt", "")[:16] in ("2026-10-07T01:26", "2026-10-07T01:25", "2026-10-07T01:27")]
assert len(w) == 1, "expected exactly one execution record near 01:26Z, found %d" % len(w)
print(json.dumps({"R25_EXEC_ID": w[0]["SK"]}))
PY
)
[ -n "$EXEC_JSON" ] || { echo "no execution id read"; exit 9; }
export R25_JSON_DIR="$HERE"
echo "=== RL11_SEND (installed code) ==="
R25_SECRET_ENV="$EXEC_JSON" R25_JSON_SPECS='[["RL11S_BODY","RL11S_DIGEST","RL11_SEND.json"]]' python "$HERE/r25_ssm_prog.py" "$HERE/r25_send_host.py.txt" "$HERE/r25_phaseB_send.out" "after $SHA $TB" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcS=${PIPESTATUS[0]}
echo "=== RL11_SCOPES (installed code) ==="
R25_JSON_SPECS='[["RL11C_BODY","RL11C_DIGEST","RL11_SCOPES.json"]]' python "$HERE/r25_ssm_prog.py" "$HERE/r25_scopes_host.py.txt" "$HERE/r25_phaseB_scopes.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcC=${PIPESTATUS[0]}
echo "=== FLOOR 1: the portal login (installed code) ==="
R25_JSON_SPECS='[["RL10_BODY","RL10_DIGEST","r25_phaseB_login_body.json"]]' python "$HERE/r25_ssm_prog.py" "$HERE/r25_login_host.py.txt" "$HERE/r25_phaseB_login.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcL=${PIPESTATUS[0]}
echo "=== FLOOR 2: the real holder, query + download (installed code; POLICY# reads only) ==="
T="$HERE/../../../../../../../.scratch/r25_real_json"; mkdir -p "$T"
python "$HERE/r25_ssm.py" real after "$HERE/r25_phaseB_real.out" "$SHA" --json "$T" 2>&1 | grep -v "warnings.warn\|IncompleteField" | tail -14; rcR=${PIPESTATUS[0]}
python - "$HERE" "$T" "$SHA" <<'PY'
import json, sys
here, t, sha = sys.argv[1:4]
lg = json.load(open(here + "/r25_phaseB_login_body.json", encoding="utf-8"))
dl = json.load(open(t + "/GA1_DOWNLOAD.json", encoding="utf-8"))
qy = json.load(open(t + "/GA1_QUERY.json", encoding="utf-8"))
def held(b, k):
    h = b["body"]["held_check"]
    return {"path": k, "outcome": b["body"][k], "returned": h["returned"], "distinct_returned": h["distinct_returned"], "held": h["held_cusips_in_dim_position"], "unheld_returned": h["unheld_returned"]}
body = {"served_release": sha, "installed_code": True,
        "portal_login": lg["body"]["login"], "portal_login_ssm": lg["ssm_command_id"],
        "real_holder": [held(qy, "dim_asset_query"), held(dl, "dim_asset_download")],
        "real_holder_ssm": {"query": qy["ssm_command_id"], "download": dl["ssm_command_id"]}, "grants_written": 0}
body["floor_ok"] = (body["portal_login"] == "OK" and all(r["outcome"] == "OK" and r["returned"] == r["distinct_returned"] == r["held"] and r["unheld_returned"] == 0 for r in body["real_holder"]))
json.dump({"body": body, "instance_id": lg["instance_id"]}, open(here + "/RL11_FLOOR.json", "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
print("RL11_FLOOR floor_ok=%s portal_login=%s real_holder=%s" % (body["floor_ok"], body["portal_login"], [(r["path"], r["returned"], r["distinct_returned"], r["held"], r["unheld_returned"]) for r in body["real_holder"]]))
PY
echo "post-deploy reads rc: send=$rcS scopes=$rcC login=$rcL real=$rcR"
[ "$rcS" = 0 ] && [ "$rcC" = 0 ] && [ "$rcL" = 0 ] && [ "$rcR" = 0 ]
