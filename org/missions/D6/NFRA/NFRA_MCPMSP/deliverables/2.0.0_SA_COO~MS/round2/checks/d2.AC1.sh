#!/usr/bin/env bash
# MS-d-2 AC1 (NEVER-2): the release's ledger entry for slug nfra-mcpmsp-r2-gateway-release is committed at HEAD,
# sentinel gone, not listed OPEN/HELD.
. "$(dirname "$0")/_root.sh"
if ledger_closed nfra-mcpmsp-r2-gateway-release; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
