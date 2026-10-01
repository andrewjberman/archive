#!/usr/bin/env bash
# MS-a-1 AC1 (NEVER-2 / PRD C12): the apply's ledger entry for slug nfra-mcpmsp-r1-firm-role is COMMITTED at HEAD, its
# sentinel is gone, and deploy_ledger.py's OPEN/HELD scan does not list it.
. "$(dirname "$0")/_root.sh"
if ledger_closed nfra-mcpmsp-r1-firm-role; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
