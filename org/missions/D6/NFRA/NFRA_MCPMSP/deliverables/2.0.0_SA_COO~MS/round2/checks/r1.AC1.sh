#!/usr/bin/env bash
# MS-r-1 AC1 (R-5, the built behaviour): infra/aws/ec2/opal-gateway/tests/run_release_suites.sh, given
# tests/test_mcpmsp_asker_firm.py (a suite that writes 2 audit lines, measured at the cut) with --noconftest (the temp-audit fixture ABSENT, as in a narrow release tree), runs it
# with AUDIT_PATH pointed at a temp file: the run ends 0 failed, and the TRACKED
# infra/aws/ec2/opal-gateway/audit.jsonl is byte-unchanged afterwards (git diff --quiet on it) -- the dirt that stopped
# round 1's release prompt cannot recur.
. "$(dirname "$0")/_root.sh"
S="$G/tests/run_release_suites.sh"
[ -f "$S" ] || { echo "$S absent"; echo "RESULT: FAIL"; exit 1; }
before=$(git hash-object "$G/audit.jsonl" 2>/dev/null)
out=$(cd "$G" && timeout 100 bash tests/run_release_suites.sh --noconftest tests/test_mcpmsp_asker_firm.py 2>&1 | tr -d '\r')
after=$(git hash-object "$G/audit.jsonl" 2>/dev/null)
tail=$(printf '%s\n' "$out" | grep -E '[0-9]+ (passed|failed)' | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
same=no; [ -n "$before" ] && [ "$before" = "$after" ] && git diff --quiet -- "$G/audit.jsonl" && same=yes
echo "suite: ${tail:-NONE}; tracked audit.jsonl unchanged=$same"
if [ "$failed" = 0 ] && [ "$passed" -ge 1 ] && [ "$same" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
