#!/usr/bin/env bash
# OPLGTW OG-ad-1 AC1 (round-37, PRD v3.14 @f2b066d9ad, PRD v3.1 Ruling 2, CVO half refusal Z-S162): the five client_* tools are the DATA-GRANT class and master_admin-only for an unprofiled principal.
#  - app.data_entitlement: each of the five is in DATA_GRANT_TOOLS AND in TIER_ADMITTED_TOOLS, and in none of NATIVE_TOOLS; each is still CLASSIFIED (classify() is not None), so none is tool_unclassified;
#  - decide(): an unprofiled principal that is not master_admin (tier STANDARD_EMPLOYEE, then READ_ONLY) is DENIED each of the five; the master_admin tier passes each.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(cd "$GW" && python - <<'PYEOF'
import sys
sys.path.insert(0, ".")
from app import data_entitlement as de
from app.tier import Tier
five = ["client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"]
in_dg = sum(1 for t in five if t in de.DATA_GRANT_TOOLS)
in_ti = sum(1 for t in five if t in de.TIER_ADMITTED_TOOLS)
in_nat = sum(1 for t in five if t in de.NATIVE_TOOLS)
classified = sum(1 for t in five if de.classify(t) is not None)
unprof = de.Access(False, None, None, frozenset())
den_std = sum(1 for t in five if de.decide(t, unprof, Tier.STANDARD_EMPLOYEE) is not None)
den_ro = sum(1 for t in five if de.decide(t, unprof, Tier.READ_ONLY) is not None)
adm_ok = sum(1 for t in five if de.decide(t, unprof, Tier.MASTER_ADMIN) is None)
print("data-grant class: in DATA_GRANT_TOOLS %d of 5; in TIER_ADMITTED_TOOLS %d of 5; in NATIVE_TOOLS %d (want 0); classified %d of 5" % (in_dg, in_ti, in_nat, classified))
print("decide(): unprofiled standard_employee denied %d of 5; unprofiled read_only denied %d of 5; unprofiled master_admin passes %d of 5" % (den_std, den_ro, adm_ok))
print("OK" if in_dg == 5 and in_ti == 5 and in_nat == 0 and classified == 5 and den_std == 5 and den_ro == 5 and adm_ok == 5 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
