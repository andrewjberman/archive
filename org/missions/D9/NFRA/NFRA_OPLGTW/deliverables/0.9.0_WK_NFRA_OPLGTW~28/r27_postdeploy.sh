#!/usr/bin/env bash
# OG-rl-13 PHASE B post-deploy reads, run IMMEDIATELY after r27_verify.sh after (never run by the Phase A worker against an installed release).
# usage: bash r27_postdeploy.sh <40-hex deployed sha> <state.json written by r27_verify.sh before>      (run from the release-owning worktree root; HOST RUNS ONE AT A TIME, row Z-W28-S9)
# Writes, through the INSTALLED code (never a staged copy), in this directory:
#   RL13_READ.json   {"body", "ssm_command_id", "instance_id"}  RL13_DIGEST attested   (rl13.AC2): the wrapper exercise, displayed_date, the rivalfunds audit args and bytes
#   RL13_FLOOR.json  the standing floor re-read -- the portal login and the real holder (query + download) on the installed code -- plus status_id_refused (slash), status_id_refused_dot,
#                    status_id_accepted, plus the four route arms r27_verify.sh after wrote to r27_phaseB_route.json (chart_404, chart_400, day_page_unchanged, audit_page_unchanged)
# The known execution id (the 2026-10-07 ~01:26Z run) is read read-only from the portal's execution table at run time and passed to the host ONLY inside the SSM parameters
# (the runner redacts it from the output); it is never written to the repository.
set -u
SHA="$1"; STATE="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"; export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~28}"
LIVE=feddb372443adbcf139febab35b69f109e49b664
EXEC_JSON=$(python "$HERE/r27_exec_id.py" 2>&1 | grep '^{')
[ -n "$EXEC_JSON" ] || { echo "no execution id read"; exit 9; }
export R27_JSON_DIR="$HERE"
echo "=== RL13_READ (installed code: the wrapper exercise, the status tool's displayed_date, the rivalfunds audit args) ==="
python "$HERE/r27_run_read.py" after "$SHA" "$HERE/r27_phaseB_read.out" --json 2>&1; rcA=${PIPESTATUS[0]}
echo "=== STATUS ID ARMS: one refused id, one accepted id (installed code) ==="
R27_SECRET_ENV="$EXEC_JSON" R27_JSON_SPECS='[["RL13ID_BODY","RL13ID_DIGEST","r27_phaseB_status_body.json"]]' python "$HERE/r27_ssm_prog.py" "$HERE/r27_status_host.py.txt" "$HERE/r27_phaseB_status.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcS=${PIPESTATUS[0]}
echo "=== FLOOR 1: the portal login (installed code) ==="
R27_JSON_SPECS='[["RL10_BODY","RL10_DIGEST","r27_phaseB_login_body.json"]]' python "$HERE/r27_ssm_prog.py" "$HERE/r27_login_host.py.txt" "$HERE/r27_phaseB_login.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcL=${PIPESTATUS[0]}
echo "=== FLOOR 2: the real holder, query + download (installed code; POLICY# reads only) ==="
T="$HERE/../../../../../../../.scratch/r27_real_json"; mkdir -p "$T"
python "$HERE/r27_ssm.py" real after "$HERE/r27_phaseB_real.out" "$SHA" --json "$T" 2>&1 | grep -v "warnings.warn\|IncompleteField" | tail -14; rcR=${PIPESTATUS[0]}
python - "$HERE" "$T" "$SHA" <<'PY'
import json, sys
here, t, sha = sys.argv[1:4]
lg = json.load(open(here + "/r27_phaseB_login_body.json", encoding="utf-8"))
st = json.load(open(here + "/r27_phaseB_status_body.json", encoding="utf-8"))
rt = json.load(open(here + "/r27_phaseB_route.json", encoding="utf-8"))["body"]       # written by r27_verify.sh after, from the installed release code
dl = json.load(open(t + "/GA1_DOWNLOAD.json", encoding="utf-8"))
qy = json.load(open(t + "/GA1_QUERY.json", encoding="utf-8"))
def held(b, k):
    h = b["body"]["held_check"]
    return {"path": k, "outcome": b["body"][k], "returned": h["returned"], "distinct_returned": h["distinct_returned"], "held": h["held_cusips_in_dim_position"], "unheld_returned": h["unheld_returned"]}
body = {"served_release": sha, "installed_code": True,
        "portal_login": lg["body"]["login"], "portal_login_ssm": lg["ssm_command_id"],
        "real_holder": [held(qy, "dim_asset_query"), held(dl, "dim_asset_download")],
        "real_holder_ssm": {"query": qy["ssm_command_id"], "download": dl["ssm_command_id"]},
        "status_id_refused": st["body"]["status_id_refused"], "status_id_refused_dot": st["body"]["status_id_refused_dot"], "status_id_accepted": st["body"]["status_id_accepted"], "status_id_ssm": st["ssm_command_id"], "grants_written": 0,
        "chart_404": {"ok": rt["chart_404"], "status": rt["chart_404_status"], "body_names_no_chart": rt["chart_404_body_named"]},
        "chart_400": {"ok": rt["chart_400"], "status": rt["chart_400_status"]},
        "day_page_unchanged": {"ok": rt["day_page_unchanged"], "status": rt["day_status"], "bytes": rt["day_bytes"], "sha16": rt["day_sha16"]},
        "audit_page_unchanged": {"ok": rt["audit_page_unchanged"], "status": rt["audit_status"], "bytes": rt["audit_bytes"], "sha16": rt["audit_sha16"]}}
body["route_ok"] = all(body[k]["ok"] is True for k in ("chart_404", "chart_400", "day_page_unchanged", "audit_page_unchanged"))
body["floor_ok"] = (body["portal_login"] == "OK" and all(r["outcome"] == "OK" and r["returned"] == r["distinct_returned"] == r["held"] and r["unheld_returned"] == 0 for r in body["real_holder"]))
body["status_id_ok"] = (body["status_id_refused"]["outcome"] == "refused" and body["status_id_refused"]["http_requests"] == 0
                        and body["status_id_refused_dot"]["outcome"] == "refused" and body["status_id_refused_dot"]["http_requests"] == 0
                        and body["status_id_accepted"]["outcome"] == "OK" and body["status_id_accepted"]["status_value"] in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"))
json.dump({"body": body, "instance_id": lg["instance_id"]}, open(here + "/RL13_FLOOR.json", "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
print("RL13_FLOOR route_ok=%s floor_ok=%s status_id_ok=%s portal_login=%s real_holder=%s refused=%s accepted=%s" % (body["route_ok"], body["floor_ok"], body["status_id_ok"], body["portal_login"],
      [(r["path"], r["returned"], r["distinct_returned"], r["held"], r["unheld_returned"]) for r in body["real_holder"]], body["status_id_refused"]["outcome"], body["status_id_accepted"]["outcome"]))
PY
echo "post-deploy reads rc: allow=$rcA status=$rcS login=$rcL real=$rcR"
[ "$rcA" = 0 ] && [ "$rcS" = 0 ] && [ "$rcL" = 0 ] && [ "$rcR" = 0 ]
