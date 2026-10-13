#!/usr/bin/env bash
# OPLGTW OG-bd-2 AC2: the never-widen ask for the gateway release that ships the deny exists, and names the admitted class
# master_admin, the still-denied unlinked caller fc9aed2e22, and the rollback.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~60/NEVER_WIDEN_ASK_OG-bd-2.md"
[ -f "$F" ] || { echo "ask absent"; echo "RESULT: FAIL"; exit 1; }
a=$(grep -c 'master_admin' "$F"); b=$(grep -c 'fc9aed2e22' "$F"); c=$(grep -ci 'rollback' "$F")
echo "ask: master_admin lines $a; fc9aed2e22 lines $b; rollback lines $c"
[ "$a" -ge 1 ] && [ "$b" -ge 1 ] && [ "$c" -ge 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
