#!/usr/bin/env bash
# OPLGTW OG-h-1 AC1 (amended A1): every tracked gateway file with one of the seven W2-S8 extensions, except the one
# named exception, resolves eol=lf and none is stored CRLF; the exception resolves text unset (-text).
. "$(dirname "$0")/_root.sh"
EXC="infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
files=$(git ls-files "$GW" | grep -E '\.(service|txt|yaml|json|md|html|jsonl)$' | grep -vxF "$EXC")
n=$(printf '%s\n' "$files" | grep -c .)
notlf=$(printf '%s\n' "$files" | grep . | git check-attr --stdin eol | grep -vc ': eol: lf$')
crlf=$(printf '%s\n' "$files" | grep . | xargs git ls-files --eol -- | grep -c '^i/crlf')
printf '%s\n' "$files" | grep . | git check-attr --stdin eol | grep -v ': eol: lf$' | sed 's/^/  no rule: /' | head -20
exc=no; git check-attr text -- "$EXC" | grep -q ': text: unset$' && exc=yes
echo "gateway files with the 7 extensions outside the exception=$n; attr eol=lf on $([ "$notlf" = 0 ] && echo 'all outside the exception' || echo "all but $notlf"); exception -text=$exc; stored CRLF outside the exception $crlf"
if [ "$n" -ge 1 ] && [ "$notlf" = 0 ] && [ "$exc" = yes ] && [ "$crlf" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
