#!/usr/bin/env bash
# MP-pd-1 AC1 (R1 / Z-W24-S2; decomposition PD.1): the worker's run file deliverables/0.9.0_WK_NFRA_MCPORTAL~25/pd1_run.json
# carries {"caller_arn","principals","tools_compared","per_principal":[{"who","store_tools","page_tools"}]}:
#   - the store was read under the OPERATOR ROLE: caller_arn contains "assumed-role/opal-gateway-access-admin/";
#   - every principal's data-grant tools read from the grant store equal the data-grant tools the served /people view lists
#     for that principal (sorted lists equal), and at least one principal holds at least one tool;
#   - the printed denominators equal the recount: principals == len(per_principal), tools_compared == sum of the store lists.
. "$(dirname "$0")/_root.sh"
RUN="${MP_PD1_RUN:-$PDD/0.9.0_WK_NFRA_MCPORTAL~25/pd1_run.json}"
v=$(python - "$RUN" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s)" % type(e).__name__); sys.exit()
pp = d.get("per_principal") or []
role = "yes" if "assumed-role/opal-gateway-access-admin/" in str(d.get("caller_arn") or "") else "no"
eq = sum(1 for r in pp if isinstance(r, dict) and sorted(r.get("store_tools") or []) == sorted(r.get("page_tools") or []))
held = sum(len(r.get("store_tools") or []) for r in pp if isinstance(r, dict))
den = "yes" if d.get("principals") == len(pp) and d.get("tools_compared") == held else "no"
print("run=read operator_role:%s principals=%d equal=%d of %d tools_compared=%s held_by_recount=%d denominators_match:%s" % (
    role, len(pp), eq, len(pp), d.get("tools_compared"), held, den))
print("PASSCOND " + ("yes" if role == "yes" and pp and eq == len(pp) and held >= 1 and den == "yes" else "no"))
PY
)
printf '%s\n' "$v" | grep -v '^PASSCOND'
if printf '%s' "$v" | grep -q '^PASSCOND yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
