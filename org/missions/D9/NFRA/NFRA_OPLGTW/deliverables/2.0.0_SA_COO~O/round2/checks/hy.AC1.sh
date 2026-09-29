#!/usr/bin/env bash
# OPLGTW OG-h-1 AC1: every tracked gateway file with one of the seven W2-S8 extensions resolves eol=lf, and none is
# stored CRLF in the index.
. "$(dirname "$0")/_root.sh"
files=$(git ls-files "$GW" | grep -E '\.(service|txt|yaml|json|md|html|jsonl)$')
n=$(printf '%s\n' "$files" | grep -c .)
notlf=$(printf '%s\n' "$files" | grep . | git check-attr --stdin eol | grep -vc ': eol: lf$')
crlf=$(printf '%s\n' "$files" | grep . | xargs git ls-files --eol -- | grep -c '^i/crlf')
printf '%s\n' "$files" | grep . | git check-attr --stdin eol | grep -v ': eol: lf$' | sed 's/^/  no rule: /' | head -20
echo "gateway files with the 7 extensions=$n; attr eol=lf on $([ "$notlf" = 0 ] && echo all || echo "all but $notlf"); stored CRLF $crlf"
if [ "$n" -ge 1 ] && [ "$notlf" = 0 ] && [ "$crlf" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
