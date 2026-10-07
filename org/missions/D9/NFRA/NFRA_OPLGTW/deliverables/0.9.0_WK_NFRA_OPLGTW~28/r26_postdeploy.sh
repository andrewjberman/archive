#!/usr/bin/env bash
# OG-rl-12 PHASE B post-deploy reads, run IMMEDIATELY after r26_verify.sh after (never run by the Phase A worker against an installed release).
# usage: bash r26_postdeploy.sh <40-hex deployed sha> <state.json written by r26_verify.sh before>      (run from the release-owning worktree root; HOST RUNS ONE AT A TIME, row Z-W28-S9)
# Writes, through the INSTALLED code (never a staged copy), in this directory:
#   RL12_ALLOW.json  {"body", "ssm_command_id", "instance_id"}  RL12_DIGEST attested   (rl12.AC2)
#   RL12_FLOOR.json  the standing floor re-read -- the portal login and the real holder (query + download) on the installed code -- plus status_id_refused and status_id_accepted,
#                    plus (AMENDMENT A3) chart_404, chart_400, day_page_unchanged, audit_page_unchanged: the four route arms r26_verify.sh after wrote to r26_phaseB_route.json
# overlay_rows_before is COUNTED from the allowlist blob at the live sha (the file the host held before the deploy), by the loader's own rule (a line with >= 2 tokens before any '#').
# The known execution id (the 2026-10-07 ~01:26Z run) is read read-only from the portal's execution table at run time and passed to the host ONLY inside the SSM parameters
# (the runner redacts it from the output); it is never written to the repository.
set -u
SHA="$1"; STATE="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"; export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~28}"
LIVE=240ac2fe5abde944f15358ab563cb4b2ab63f09f
TB=$(python -c "import json,sys;print(len(json.load(open(sys.argv[1],encoding='utf-8'))['tools']))" "$STATE" | tr -d '\r')
ROWS_BEFORE=$(git show "$LIVE:infra/aws/ec2/opal-gateway/identity_tool_allowlist.txt" | python -c "import sys;print(sum(1 for l in sys.stdin.buffer.read().decode('utf-8').splitlines() if len(l.split('#',1)[0].split())>=2))" | tr -d '\r')
echo "tools before (state) $TB; overlay rows before (live blob) $ROWS_BEFORE"
EXEC_JSON=$(python "$HERE/r26_exec_id.py" 2>&1 | grep '^{')
[ -n "$EXEC_JSON" ] || { echo "no execution id read"; exit 9; }
export R26_JSON_DIR="$HERE"
echo "=== RL12_ALLOW (installed code) ==="
R26_JSON_SPECS='[["RL12_BODY","RL12_DIGEST","RL12_ALLOW.json"]]' python "$HERE/r26_ssm_prog.py" "$HERE/r26_allow_host.py.txt" "$HERE/r26_phaseB_allow.out" "after $SHA $ROWS_BEFORE" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcA=${PIPESTATUS[0]}
echo "=== STATUS ID ARMS: one refused id, one accepted id (installed code) ==="
R26_SECRET_ENV="$EXEC_JSON" R26_JSON_SPECS='[["RL12ID_BODY","RL12ID_DIGEST","r26_phaseB_status_body.json"]]' python "$HERE/r26_ssm_prog.py" "$HERE/r26_status_host.py.txt" "$HERE/r26_phaseB_status.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcS=${PIPESTATUS[0]}
echo "=== FLOOR 1: the portal login (installed code) ==="
R26_JSON_SPECS='[["RL10_BODY","RL10_DIGEST","r26_phaseB_login_body.json"]]' python "$HERE/r26_ssm_prog.py" "$HERE/r26_login_host.py.txt" "$HERE/r26_phaseB_login.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcL=${PIPESTATUS[0]}
echo "=== FLOOR 2: the real holder, query + download (installed code; POLICY# reads only) ==="
T="$HERE/../../../../../../../.scratch/r26_real_json"; mkdir -p "$T"
python "$HERE/r26_ssm.py" real after "$HERE/r26_phaseB_real.out" "$SHA" --json "$T" 2>&1 | grep -v "warnings.warn\|IncompleteField" | tail -14; rcR=${PIPESTATUS[0]}
python - "$HERE" "$T" "$SHA" <<'PY'
import json, sys
here, t, sha = sys.argv[1:4]
lg = json.load(open(here + "/r26_phaseB_login_body.json", encoding="utf-8"))
st = json.load(open(here + "/r26_phaseB_status_body.json", encoding="utf-8"))
rt = json.load(open(here + "/r26_phaseB_route.json", encoding="utf-8"))["body"]       # written by r26_verify.sh after, from the installed release code
dl = json.load(open(t + "/GA1_DOWNLOAD.json", encoding="utf-8"))
qy = json.load(open(t + "/GA1_QUERY.json", encoding="utf-8"))
def held(b, k):
    h = b["body"]["held_check"]
    return {"path": k, "outcome": b["body"][k], "returned": h["returned"], "distinct_returned": h["distinct_returned"], "held": h["held_cusips_in_dim_position"], "unheld_returned": h["unheld_returned"]}
body = {"served_release": sha, "installed_code": True,
        "portal_login": lg["body"]["login"], "portal_login_ssm": lg["ssm_command_id"],
        "real_holder": [held(qy, "dim_asset_query"), held(dl, "dim_asset_download")],
        "real_holder_ssm": {"query": qy["ssm_command_id"], "download": dl["ssm_command_id"]},
        "status_id_refused": st["body"]["status_id_refused"], "status_id_accepted": st["body"]["status_id_accepted"], "status_id_ssm": st["ssm_command_id"], "grants_written": 0,
        "chart_404": {"ok": rt["chart_404"], "status": rt["chart_404_status"], "body_names_no_chart": rt["chart_404_body_named"]},
        "chart_400": {"ok": rt["chart_400"], "status": rt["chart_400_status"]},
        "day_page_unchanged": {"ok": rt["day_page_unchanged"], "status": rt["day_status"], "bytes": rt["day_bytes"], "sha16": rt["day_sha16"]},
        "audit_page_unchanged": {"ok": rt["audit_page_unchanged"], "status": rt["audit_status"], "bytes": rt["audit_bytes"], "sha16": rt["audit_sha16"]}}
body["route_ok"] = all(body[k]["ok"] is True for k in ("chart_404", "chart_400", "day_page_unchanged", "audit_page_unchanged"))
body["floor_ok"] = (body["portal_login"] == "OK" and all(r["outcome"] == "OK" and r["returned"] == r["distinct_returned"] == r["held"] and r["unheld_returned"] == 0 for r in body["real_holder"]))
body["status_id_ok"] = (body["status_id_refused"]["outcome"] == "refused" and body["status_id_refused"]["http_requests"] == 0
                        and body["status_id_accepted"]["outcome"] == "OK" and body["status_id_accepted"]["status_value"] in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"))
json.dump({"body": body, "instance_id": lg["instance_id"]}, open(here + "/RL12_FLOOR.json", "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
print("RL12_FLOOR route_ok=%s floor_ok=%s status_id_ok=%s portal_login=%s real_holder=%s refused=%s accepted=%s" % (body["route_ok"], body["floor_ok"], body["status_id_ok"], body["portal_login"],
      [(r["path"], r["returned"], r["distinct_returned"], r["held"], r["unheld_returned"]) for r in body["real_holder"]], body["status_id_refused"]["outcome"], body["status_id_accepted"]["outcome"]))
PY
echo "post-deploy reads rc: allow=$rcA status=$rcS login=$rcL real=$rcR"
[ "$rcA" = 0 ] && [ "$rcS" = 0 ] && [ "$rcL" = 0 ] && [ "$rcR" = 0 ]
