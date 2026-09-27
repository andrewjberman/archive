#!/usr/bin/env bash
# MX-s-7 AC1: every open() inside the recorder's python heredocs names encoding='utf-8'.
# Denominator: all open( calls between <<'PYEOF' and PYEOF in record-terraform-deploy.sh.
f=${RTD_FILE:-infra/aws/lambda/ci/record-terraform-deploy.sh}
[ -f "$f" ] || { echo "ERROR: $f missing -- RESULT: FAIL"; exit 1; }
blocks=$(awk "/<<'PYEOF'/{on=1;next} /^PYEOF\$/{on=0} on" "$f")
total=$(printf '%s\n' "$blocks" | grep -c 'open(')
bare=$(printf '%s\n' "$blocks" | grep 'open(' | grep -vc "encoding=['\"]utf-8['\"]")
echo "python open() calls=$total bare=$bare"
if [ "$total" -ge 3 ] && [ "$bare" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
