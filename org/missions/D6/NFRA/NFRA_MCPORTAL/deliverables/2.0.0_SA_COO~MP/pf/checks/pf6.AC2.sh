#!/usr/bin/env bash
# MP-pf-6 AC2 (the one real read, SERVED; a MEASUREMENT criterion, not an equality one): the worker's run file deliverables/0.9.0_WK_NFRA_MCPORTAL~36/r2_run.json is well formed and non-vacuous.
# It carries {"ssm_status","ssm_command","scan_n","history_n","history_items","history_pages","history_unparsed_items","only_scan_n","only_history_n","equal","vacuous"} with:
#   ssm_status "Success"; scan_n >= 1 and history_n >= 1 (both denominators printed, neither empty); history_pages >= 1; history_unparsed_items 0 (no history row dropped from the set);
#   and the comparison is consistent with its own counts: equal == (only_scan_n == 0 and only_history_n == 0 and not vacuous).
# The verdict `equal` is REPORTED, never required here: today the grant writer's table holds one REFUSED attempt by a placeholder principal and the grant store holds one real principal, so the sets differ and that is the finding.
. "$(dirname "$0")/../../pc/checks/_root.sh"
R="${MP_PF6_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~36/r2_run.json}"
v=$(python - "$R" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s) ok=no" % type(e).__name__); sys.exit()
g = lambda k: d.get(k)
isint = lambda k: isinstance(g(k), int) and not isinstance(g(k), bool)
need = all(k in d for k in ("ssm_status", "ssm_command", "scan_n", "history_n", "history_items", "history_pages", "history_unparsed_items", "only_scan_n", "only_history_n", "equal", "vacuous"))
cons = need and all(isint(k) for k in ("scan_n", "history_n", "history_pages", "history_unparsed_items", "only_scan_n", "only_history_n")) \
    and g("equal") == (g("only_scan_n") == 0 and g("only_history_n") == 0 and not g("vacuous"))
ok = need and cons and g("ssm_status") == "Success" and g("scan_n") >= 1 and g("history_n") >= 1 and g("history_pages") >= 1 and g("history_unparsed_items") == 0
print("run=read ssm=%s scan_n=%s history_n=%s history_items=%s pages=%s unparsed=%s only_scan=%s only_history=%s equal=%s vacuous=%s consistent=%s ok=%s" % (
    g("ssm_status"), g("scan_n"), g("history_n"), g("history_items"), g("history_pages"), g("history_unparsed_items"), g("only_scan_n"), g("only_history_n"), g("equal"), g("vacuous"), "yes" if cons else "no", "yes" if ok else "no"))
PY
)
echo "$v"
if printf '%s' "$v" | grep -q ' ok=yes$'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
