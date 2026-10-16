#!/usr/bin/env bash
# MP-pf-7 AC2 (the one real read, SERVED; Z-C-S40 closed or found open): the worker's run file deliverables/0.9.0_WK_NFRA_MCPORTAL~37/r3_run.json is well formed, non-vacuous and EQUAL.
# It carries {"sim_scan","sim_operator_role_scan","raw_complete","raw_pages","raw_count","raw_scanned","raw_n","page_n","only_page_n","only_raw_n","equal","vacuous","ssm_status","ssm_command"} with:
#   sim_scan "allowed" (the raw read was admitted) and sim_operator_role_scan a deny (the negative control: the simulator discriminates);
#   raw_complete true, raw_pages >= 1, raw_count == raw_scanned (no filter) and both >= 1; raw_n >= 1 and page_n >= 1 (both denominators printed, neither empty); ssm_status "Success";
#   and equal == (only_page_n == 0 and only_raw_n == 0 and not vacuous) AND equal true: the People view's principal set is exactly the set of principals the table holds a grant item for, read by a different credential with no app code.
# A false `equal` is the finding (the page misses a holder, or lists a non-holder), not a defect of the cell.
. "$(dirname "$0")/../../pc/checks/_root.sh"
R="${MP_PF7_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~37/r3_run.json}"
v=$(python - "$R" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s) ok=no" % type(e).__name__); sys.exit()
g = lambda k: d.get(k)
isint = lambda k: isinstance(g(k), int) and not isinstance(g(k), bool)
keys = ("sim_scan", "sim_operator_role_scan", "raw_complete", "raw_pages", "raw_count", "raw_scanned", "raw_n", "page_n", "only_page_n", "only_raw_n", "equal", "vacuous", "ssm_status", "ssm_command")
need = all(k in d for k in keys)
ints = need and all(isint(k) for k in ("raw_pages", "raw_count", "raw_scanned", "raw_n", "page_n", "only_page_n", "only_raw_n"))
cons = ints and g("equal") == (g("only_page_n") == 0 and g("only_raw_n") == 0 and not g("vacuous"))
ctl = need and str(g("sim_operator_role_scan")) in ("implicitDeny", "explicitDeny")
ok = need and cons and ctl and g("sim_scan") == "allowed" and g("raw_complete") is True and g("raw_pages") >= 1 and g("raw_count") == g("raw_scanned") and g("raw_count") >= 1 \
    and g("raw_n") >= 1 and g("page_n") >= 1 and g("ssm_status") == "Success" and g("equal") is True
print("run=read sim_scan=%s control=%s raw_complete=%s pages=%s count=%s scanned=%s raw_n=%s page_n=%s only_page=%s only_raw=%s equal=%s vacuous=%s ssm=%s consistent=%s ok=%s" % (
    g("sim_scan"), g("sim_operator_role_scan"), g("raw_complete"), g("raw_pages"), g("raw_count"), g("raw_scanned"), g("raw_n"), g("page_n"), g("only_page_n"), g("only_raw_n"), g("equal"), g("vacuous"), g("ssm_status"), "yes" if cons else "no", "yes" if ok else "no"))
PY
)
echo "$v"
if printf '%s' "$v" | grep -q ' ok=yes$'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
