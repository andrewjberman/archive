#!/usr/bin/env bash
# OA-f-3 AC1 (built, row Z-S37): at opal_ai ${OA_NESTED_REF:-HEAD}, provision-account.ps1's New-LocalUser -Description
# literal is 48 characters or fewer (New-LocalUser's own limit), and against the cut fd8ab8a57f the change is exactly ONE
# line removed and ONE added in that file, with no other file changed. The CTO's condition on the scratch-copy G-ACCT
# run compares that same one line (msg 26231).
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/provision/provision-account.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
out=$(git -C opal_ai show "$REF:$F" 2>/dev/null | python -c '
import re, sys
t = sys.stdin.read()
m = re.search(r"-Description\s+\x27([^\x27]*)\x27", t)
print("desc_len=%s" % (len(m.group(1)) if m else "none"))
' 2>&1 | tr -d '\r')
ns=$(git -C opal_ai diff --numstat "$OA_NESTED_PIN" "$REF" -- "$F" 2>/dev/null | awk '{print $1" "$2}')
others=$(git -C opal_ai diff --name-only "$OA_NESTED_PIN" "$REF" 2>/dev/null | grep -v -x -F "$F" | grep -c .)
echo "opal_ai $REF: $out; numstat added/removed vs $OA_NESTED_PIN=[${ns:-0 0}]; other files changed=$others"
len=$(printf '%s' "$out" | sed -n 's/^desc_len=\([0-9][0-9]*\)$/\1/p')
if [ -n "$len" ] && [ "$len" -le 48 ] && [ "$ns" = "1 1" ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
