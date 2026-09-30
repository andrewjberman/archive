#!/usr/bin/env bash
# MS-dn-1 AC4 (NEVER-2 -- a fourth mechanical criterion, reason: the Deny is a hard-stop WORLD act and its ledger close
# is the change-management half the other three do not read): the entry for slug nfra-mcpmsp-r2-gateway-firm-deny is
# committed at HEAD, sentinel gone, not listed OPEN/HELD.
. "$(dirname "$0")/_root.sh"
if ledger_closed nfra-mcpmsp-r2-gateway-firm-deny; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
