#!/usr/bin/env bash
# MX-v-7 AC1: the thread re-run record carries, for blackdiamond_list_fees, one figure + as_of returned by the SERVED tool
# equal to the same field read from the source object by VersionId, with the VersionId and the denominator printed (item 4).
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~22/THREAD_RERUN_round6.json"
out=$(python - "$F" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("record absent or unreadable: %s" % e)
    sys.exit(1)
r = d.get("blackdiamond_list_fees") or {}
keys = ("served_figure", "source_figure", "served_as_of", "source_as_of", "source_version_id", "denominator")
miss = [k for k in keys if r.get(k) in (None, "")]
eq = (not miss) and str(r["served_figure"]) == str(r["source_figure"]) and str(r["served_as_of"]) == str(r["source_as_of"])
print("fields missing=%s; figure %s == %s; as_of %s == %s; VersionId %s; denominator %s" % (
    miss, r.get("served_figure"), r.get("source_figure"), r.get("served_as_of"), r.get("source_as_of"),
    r.get("source_version_id"), r.get("denominator")))
sys.exit(0 if eq else 1)
EOF
); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
