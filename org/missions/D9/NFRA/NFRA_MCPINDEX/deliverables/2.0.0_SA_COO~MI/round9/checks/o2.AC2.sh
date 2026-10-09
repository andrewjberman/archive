#!/usr/bin/env bash
# MX-o-2 AC2 (FWD-19, contracts 1 and 3), BOTH branches of the census verdict:
#   SERVED -> the three named tests in tests/test_ops_billing.py pass offline (fixture-field rows, the C4 envelope,
#             C7 isolation) and no other test in that file fails;
#   GAP    -> no reader was built: app/integrations/ops_billing/ is absent.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
C="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json"
v=$(python -c "import json,sys; print(json.load(open(sys.argv[1],encoding='utf-8')).get('verdict'))" "$(native "$(pwd)/$C")" 2>&1 | tr -d '\r')
echo "census verdict: $v"
rc=1
if [ "$v" = SERVED ]; then
  pytest_named tests/test_ops_billing.py \
    test_billing_rows_carry_exactly_the_fixture_fields \
    test_billing_answer_states_scope_as_of_completeness \
    test_billing_refuses_a_cross_firm_read
  rc=$?
elif [ "$v" = GAP ]; then
  if [ -e "$GW/app/integrations/ops_billing" ]; then echo "GAP branch but the reader folder exists"; else echo "GAP branch: no reader built"; rc=0; fi
fi
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
