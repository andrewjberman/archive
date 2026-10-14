#!/usr/bin/env bash
# MP-pd-6 AC1 (U2, enable and SEE a live payload; decomposition PD.4, PD.6): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~29/pd6_run.json carries {"settings_path","backup_path","blast_radius","rollback_proven_on_copy",
# "rollback_bytes_equal","snapshot_path","waited_seconds"}, and the checker reads the WORLD itself, never the run file's word:
#   - the live settings file parses as JSON and its `statusLine` command names claude-usage-statusline.py;
#   - every key of the backup (the settings as they were) is still present in the live file with an equal value, `statusLine` aside;
#   - the rollback was proven on a COPY: the run file says so, and re-applying the stated rollback (delete the one `statusLine` key)
#     to a copy of the live file gives a JSON object whose bytes-as-data equal the backup;
#   - the snapshot file the live status line wrote parses (schema 1) with rate_limits_claim measured, or absent WITH a reason;
#   - blast_radius is a non-empty statement.
. "$(dirname "$0")/_root.sh"
RUN="${MP_PD6_RUN:-$PDD/0.9.0_WK_NFRA_MCPORTAL~29/pd6_run.json}"
v=$(python - "$RUN" <<'PY'
import json, os, sys
def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)
try:
    r = load(sys.argv[1])
except Exception as e:
    print("run=unreadable(%s)" % type(e).__name__); print("PASSCOND no"); sys.exit()
out = {}
try:
    live = load(r["settings_path"]); bak = load(r["backup_path"])
    sl = live.get("statusLine")
    cmd = json.dumps(sl) if sl is not None else ""
    out["live_statusline_names_script"] = "yes" if "claude-usage-statusline.py" in cmd else "no"
    out["backup_keys_preserved"] = "yes" if all(k in live and live[k] == v for k, v in bak.items() if k != "statusLine") else "no"
    cp = dict(live); cp.pop("statusLine", None)
    exp = dict(bak); exp.pop("statusLine", None)
    out["rollback_on_copy_equals_backup"] = "yes" if cp == exp else "no"
except Exception as e:
    out["settings"] = "unreadable(%s)" % type(e).__name__
try:
    s = load(r["snapshot_path"])
    ok = s.get("schema") == 1 and (s.get("rate_limits_claim") == "measured" or (s.get("rate_limits_claim") == "absent" and s.get("reason")))
    out["snapshot"] = "%s/%s" % (s.get("rate_limits_claim"), "ok" if ok else "bad")
except Exception as e:
    out["snapshot"] = "unreadable(%s)" % type(e).__name__
out["blast_radius_stated"] = "yes" if str(r.get("blast_radius") or "").strip() else "no"
out["run_claims_rollback_proven"] = "yes" if r.get("rollback_proven_on_copy") is True and r.get("rollback_bytes_equal") is True else "no"
print("run=read " + " ".join("%s=%s" % kv for kv in out.items()))
good = (out.get("live_statusline_names_script") == "yes" and out.get("backup_keys_preserved") == "yes"
        and out.get("rollback_on_copy_equals_backup") == "yes" and out.get("snapshot", "").endswith("/ok")
        and out.get("blast_radius_stated") == "yes" and out.get("run_claims_rollback_proven") == "yes")
print("PASSCOND " + ("yes" if good else "no"))
PY
)
printf '%s\n' "$v" | grep -v '^PASSCOND'
if printf '%s' "$v" | grep -q '^PASSCOND yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
