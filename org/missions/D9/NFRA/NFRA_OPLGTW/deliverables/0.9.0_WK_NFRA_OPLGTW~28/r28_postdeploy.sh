#!/usr/bin/env bash
# OG-rl-14 PHASE B post-deploy reads, run IMMEDIATELY after r28_verify.sh after (never run by the Phase A worker against an installed release).
# usage: bash r28_postdeploy.sh <40-hex deployed sha> <state.json written by r28_verify.sh before>      (run from the release-owning worktree root; HOST RUNS ONE AT A TIME, row Z-W28-S9)
# Needs, taken by the Phase B worker around the deploy (R42, the page-time read):  python r28_pagetime.py before r28_pagetime_before.out   IMMEDIATELY BEFORE the deploy command,
#                                                                                   python r28_pagetime.py after  r28_pagetime_after.out    IMMEDIATELY AFTER it returns.
# Writes, through the INSTALLED code (never a staged copy), in this directory:
#   RL14_READ.json   {"body", "ssm_command_id", "instance_id"}  RL14_DIGEST attested (rl14.AC2): the audit-lake key builder through _emit on a FAKE S3 client (no lake object written), tools, consent
#   RL14_FLOOR.json  the standing floor re-read: the portal login; the real holder on both paths (query + download); status_id_refused (slash), status_id_refused_dot, status_id_accepted, and the status
#                    tool's displayed_date against the manifest's generated_at; the four route arms r28_verify.sh after wrote to r28_phaseB_route.json; the rivalfunds pages by the page-time read
#                    (BEFORE and AFTER, each with LastModified); then the audit-lake read `lake_record` (the first rivalfunds_view record written after the r27 deploy, 2026-10-07T16:57:30Z, or `none yet`).
# The known execution id is read read-only from the portal's execution table at run time and passed to the host ONLY inside the SSM parameters (the runner redacts it from the output); never written to the repository.
# NOTE (Phase A, stated): the real-holder run (r28_ssm.py real) reads the issuer's OFF-REPO holder file under %LOCALAPPDATA%/opal/og-salt/ga1/ (a principal identifier) and passes it only in the SSM parameters. Phase A did NOT run it (the
# order says the BEFORE/REHEARSAL needs no principal identifier); it is a Phase B floor read, as in r25-r27.
set -u
SHA="$1"; STATE="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"; export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~28}"
EXEC_JSON=$(python "$HERE/r28_exec_id.py" 2>&1 | grep '^{')
[ -n "$EXEC_JSON" ] || { echo "no execution id read"; exit 9; }
echo "=== RL14_READ (installed code: the audit-lake key builder on a fake S3 client; tools; consent) ==="
python "$HERE/r28_run_lake.py" after "$SHA" "$HERE/r28_phaseB_read.out" --json 2>&1; rcA=${PIPESTATUS[0]}
echo "=== STATUS ID ARMS + displayed_date: one refused id, one accepted id (installed code) ==="
R28_SECRET_ENV="$EXEC_JSON" R28_JSON_DIR="$HERE" R28_JSON_SPECS='[["RL14ID_BODY","RL14ID_DIGEST","r28_phaseB_status_body.json"]]' python "$HERE/r28_ssm_prog.py" "$HERE/r28_status_host.py.txt" "$HERE/r28_phaseB_status.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcS=${PIPESTATUS[0]}
echo "=== FLOOR 1: the portal login (installed code) ==="
R28_JSON_DIR="$HERE" R28_JSON_SPECS='[["RL10_BODY","RL10_DIGEST","r28_phaseB_login_body.json"]]' python "$HERE/r28_ssm_prog.py" "$HERE/r28_login_host.py.txt" "$HERE/r28_phaseB_login.out" "after $SHA" 2>&1 | grep -v "warnings.warn\|IncompleteField"; rcL=${PIPESTATUS[0]}
echo "=== FLOOR 2: the real holder, query + download (installed code; POLICY# reads only) ==="
T="$HERE/../../../../../../../.scratch/r28_real_json"; mkdir -p "$T"
python "$HERE/r28_ssm.py" real after "$HERE/r28_phaseB_real.out" "$SHA" --json "$T" 2>&1 | grep -v "warnings.warn\|IncompleteField" | tail -14; rcR=${PIPESTATUS[0]}
python - "$HERE" "$T" "$SHA" <<'PY'
import json, re, sys
here, t, sha = sys.argv[1:4]
lg = json.load(open(here + "/r28_phaseB_login_body.json", encoding="utf-8"))
st = json.load(open(here + "/r28_phaseB_status_body.json", encoding="utf-8"))
rt = json.load(open(here + "/r28_phaseB_route.json", encoding="utf-8"))["body"]       # written by r28_verify.sh after, from the installed release code
dl = json.load(open(t + "/GA1_DOWNLOAD.json", encoding="utf-8"))
qy = json.load(open(t + "/GA1_QUERY.json", encoding="utf-8"))
sb = st["body"]
def held(b, k):
    h = b["body"]["held_check"]
    return {"path": k, "outcome": b["body"][k], "returned": h["returned"], "distinct_returned": h["distinct_returned"], "held": h["held_cusips_in_dim_position"], "unheld_returned": h["unheld_returned"]}
def pagetime(fn):
    tx = open(here + "/" + fn, encoding="utf-8").read()
    m = re.search(r"^R28_PAGETIME_JSON (\{.*\})$", tx, re.M)
    return json.loads(m.group(1)) if m else None
pb, pa = pagetime("r28_pagetime_before.out"), pagetime("r28_pagetime_after.out")
pages = {"before": pb, "after": pa, "changed_with_lastmodified_unmoved": None}
if pb and pa:
    bm = dict(((o["day"], o["object"]), o) for o in pb["objects"])
    bad = []
    for o in pa["objects"]:
        b = bm.get((o["day"], o["object"]))
        if b and (b.get("size") != o.get("size") or b.get("sha16") != o.get("sha16")) and b.get("last_modified") == o.get("last_modified"):
            bad.append("%s %s" % (o["day"], o["object"]))
    pages["changed_with_lastmodified_unmoved"] = bad
body = {"served_release": sha, "installed_code": True,
        "portal_login": lg["body"]["login"], "portal_login_ssm": lg["ssm_command_id"],
        "real_holder": [held(qy, "dim_asset_query"), held(dl, "dim_asset_download")],
        "real_holder_ssm": {"query": qy["ssm_command_id"], "download": dl["ssm_command_id"]},
        "status_id_refused": sb["status_id_refused"], "status_id_refused_dot": sb["status_id_refused_dot"], "status_id_accepted": sb["status_id_accepted"], "status_id_ssm": st["ssm_command_id"],
        "displayed_date": sb.get("displayed_date"), "manifest_generated_at": sb.get("manifest_generated_at"),
        "displayed_date_equals_manifest_generated_at": sb.get("displayed_date_equals_manifest_generated_at"), "grants_written": 0,
        "chart_404": {"ok": rt["chart_404"], "status": rt["chart_404_status"], "body_names_no_chart": rt["chart_404_body_named"]},
        "chart_400": {"ok": rt["chart_400"], "status": rt["chart_400_status"]},
        "day_page_unchanged": {"ok": rt["day_page_unchanged"], "status": rt["day_status"], "bytes": rt["day_bytes"], "sha16": rt["day_sha16"]},
        "audit_page_unchanged": {"ok": rt["audit_page_unchanged"], "status": rt["audit_status"], "bytes": rt["audit_bytes"], "sha16": rt["audit_sha16"]},
        "pages_page_time": pages}
body["route_ok"] = all(body[k]["ok"] is True for k in ("chart_404", "chart_400", "day_page_unchanged", "audit_page_unchanged"))
body["floor_ok"] = (body["portal_login"] == "OK" and all(r["outcome"] == "OK" and r["returned"] == r["distinct_returned"] == r["held"] and r["unheld_returned"] == 0 for r in body["real_holder"]))
body["status_id_ok"] = (body["status_id_refused"]["outcome"] == "refused" and body["status_id_refused"]["http_requests"] == 0
                        and body["status_id_refused_dot"]["outcome"] == "refused" and body["status_id_refused_dot"]["http_requests"] == 0
                        and body["status_id_accepted"]["outcome"] == "OK" and body["status_id_accepted"]["status_value"] in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED")
                        and body["displayed_date_equals_manifest_generated_at"] is True)
body["page_time_ok"] = bool(pb and pa) and pages["changed_with_lastmodified_unmoved"] == []
json.dump({"body": body, "instance_id": lg["instance_id"]}, open(here + "/RL14_FLOOR.json", "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
print("RL14_FLOOR route_ok=%s floor_ok=%s status_id_ok=%s page_time_ok=%s portal_login=%s real_holder=%s refused=%s accepted=%s displayed_date_equal=%s" % (body["route_ok"], body["floor_ok"], body["status_id_ok"], body["page_time_ok"], body["portal_login"],
      [(r["path"], r["returned"], r["distinct_returned"], r["held"], r["unheld_returned"]) for r in body["real_holder"]], body["status_id_refused"]["outcome"], body["status_id_accepted"]["outcome"], body["displayed_date_equals_manifest_generated_at"]))
PY
rcF=$?
echo "=== AUDIT-LAKE READ (read-only list + get; nothing written): the first rivalfunds_view record after the r27 deploy ==="
python "$HERE/r28_lake_read.py" 2026-10-07T16:57:30Z "$HERE/r28_phaseB_lake_read.out" --merge "$HERE/RL14_FLOOR.json"; rcK=$?
echo "post-deploy reads rc: read=$rcA status=$rcS login=$rcL real=$rcR floor_fold=$rcF lake_read=$rcK"
[ "$rcA" = 0 ] && [ "$rcS" = 0 ] && [ "$rcL" = 0 ] && [ "$rcR" = 0 ] && [ "$rcF" = 0 ] && [ "$rcK" = 0 ]
