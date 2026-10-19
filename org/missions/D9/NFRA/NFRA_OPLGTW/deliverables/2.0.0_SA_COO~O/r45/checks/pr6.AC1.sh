#!/usr/bin/env bash
# OPLGTW OG-pr-6 AC1 (round 45; row Z-S402): a failed audit-lake put is AUDIBLE and the local floor write is UNCHANGED.
#  (a) the three named tests in tests/test_og_pr6.py pass together: test_failed_put_increments_counter_and_writes_one_line, test_second_line_after_60s_carries_the_running_count, test_floor_line_written_when_the_put_fails;
#  (b) the floor-write lines of app/audit.py `_emit` (from `def _emit` through the line `fh.write(line + "\n")`) are byte-equal to the base blob b40d48c1be77731dac4a0a45fb359bb1eee5b0c0 (git rev-parse HEAD:infra/aws/ec2/opal-gateway/app/audit.py at the issuance).
# Override (dry-run controls only): PR6_BASE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="${PR6_BASE_OVERRIDE:-b40d48c1be77731dac4a0a45fb359bb1eee5b0c0}"
F="${PR6_AUDIT_OVERRIDE:-$GW/app/audit.py}"
IDS="tests/test_og_pr6.py::test_failed_put_increments_counter_and_writes_one_line tests/test_og_pr6.py::test_second_line_after_60s_carries_the_running_count tests/test_og_pr6.py::test_floor_line_written_when_the_put_fails"
out=$(cd "$GW" && timeout 110 python -m pytest -q -p no:cacheprovider --color=no $IDS 2>&1 | tr -d '\r'); rc=$?
last=$(printf '%s\n' "$out" | tail -1)
p=$(printf '%s\n' "$last" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); f=$(printf '%s\n' "$last" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
restore_audit
git cat-file -e "$BASE" 2>/dev/null || { echo "base blob $BASE not in this repository"; echo "RESULT: FAIL"; exit 1; }
git cat-file -p "$BASE" > "${TMPDIR:-/tmp}/pr6_base_audit.py"
res=$(python -I - "$(native "${TMPDIR:-/tmp}/pr6_base_audit.py")" "$(native "$F")" <<'PYEOF'
import sys
def floor(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    i = next((k for k, l in enumerate(lines) if l.startswith("def _emit(")), None)
    if i is None:
        return None
    j = next((k for k in range(i, len(lines)) if 'fh.write(line + "\\n")' in lines[k]), None)
    return None if j is None else lines[i:j + 1]
a = floor(sys.argv[1]); b = floor(sys.argv[2])
print("floor lines of _emit equal to the base blob: %s (%s lines)" % ("yes" if a is not None and a == b else "NO", "none" if b is None else len(b)))
print("OK" if a is not None and a == b else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "the three named tests: passed ${p:-0} of 3; failed ${f:-0}; pytest rc=$rc"
printf '%s\n' "$res" | sed '$d'
[ "$rc" = 0 ] && [ "${p:-0}" = 3 ] && [ "${f:-0}" = 0 ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
