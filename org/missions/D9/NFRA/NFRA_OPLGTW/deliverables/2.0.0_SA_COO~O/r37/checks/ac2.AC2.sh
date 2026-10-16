#!/usr/bin/env bash
# OPLGTW OG-ac-2 AC2 (round-37, the etf-classifications increment): the worker's probe (RE-RUN here) read the REAL table by one ticker and refused a non-Opal principal with zero reads,
# the tool is defined in app/mdpf_classification.py, and the module reads the table with GetItem only (no Scan, Query, BatchGetItem or write call anywhere in it).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113"
MOD="infra/aws/ec2/opal-gateway/app/mdpf_classification.py"
[ -f "$MOD" ] && [ -f "$W/probe_ac2.py" ] || { echo "module or probe absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$MOD")" <<'PYEOF'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
defd = 1 if re.search(r"def\s+mdpf_get_security_classification\s*\(", src) else 0
bad = re.findall(r"\.(scan|query|batch_get_item|batch_write_item|put_item|update_item|delete_item|transact_write_items|transact_get_items)\s*\(", src)
get = len(re.findall(r"\.get_item\s*\(", src))
print("module: tool defined %d of 1; get_item calls %d (want 1 or more); scan/query/batch/write calls %d (want 0)" % (defd, get, len(bad)))
print("OK" if defd == 1 and get >= 1 and not bad else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
out=$(timeout 115 python "$W/probe_ac2.py" 2>&1 | tr -d '\r'); printf '%s\n' "$out" | grep -E "^probe cls:" | tail -n 3
a=$(printf '%s\n' "$out" | grep -cE "^probe cls: mdpf_get_security_classification answered True as_of [0-9]{4}-[0-9]{2}-[0-9]{2} non_opal_refused True reads_on_refusal 0")
b=$(printf '%s\n' "$out" | grep -cE "^probe cls: absent_ticker answered True absent_reason set True")
echo "probe: real row answered $a of 1; absent ticker answered with absent_reason $b of 1"
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$a" = 1 ] && [ "$b" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
