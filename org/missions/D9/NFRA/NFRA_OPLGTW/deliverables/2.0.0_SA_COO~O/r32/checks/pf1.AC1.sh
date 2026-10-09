#!/usr/bin/env bash
# OPLGTW OG-pf-1 AC1 (CTO ruling msg 32383): a profile confines only the DATA-GRANT tool family. Four named tests in
# tests/test_data_entitlement_family.py, offline (state store faked):
#   (01) a profiled principal whose grant names the Schwab tools (Andrew's v2.2 width) is allowed every NON-data tool and
#        every REST route the guard covers, and its granted Schwab tools;
#   (02) an UNPROFILED principal is still denied every Schwab tool and every Black Diamond data tool (C2 fail-closed);
#   (03) Alyssa's profile (the live shape: restricted, its grant's datasets, masters, operations) gets exactly the same
#        DATA-tool answers as before this cell, tool for tool; a data tool outside her grant is still denied;
#   (04) the data family is named in ONE place and holds the five schwab_* tools and the Black Diamond data tools; a tool
#        in neither the family nor any other classification is still `tool_unclassified` for every principal.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_pf1_audit_$$.jsonl"
pytest_named tests/test_data_entitlement_family.py test_ogpf1_ac01 test_ogpf1_ac02 test_ogpf1_ac03 test_ogpf1_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
