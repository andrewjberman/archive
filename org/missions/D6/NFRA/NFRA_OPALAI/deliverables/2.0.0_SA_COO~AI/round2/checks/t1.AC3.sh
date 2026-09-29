#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t1.AC3.sh (2.0.0_SA_COO~AI). ONE amendment: the moved prompt is read at $OA_NESTED_PIN, never at the nested HEAD.
# OA-t-1 AC3 (C7 + C11 on the moved prompt): the "## Hard lines" section is byte-equal to the parent copy at the cut;
# the runtime prompt names none of the workspace launch acts (register_agent, /watcher, secretsmanager) that the cut's
# copy names; the identity gate (whoami) is kept; and a RUNTIME MECHANISM MAP covers all 8 APPROVED catalog rows,
# each row either naming opal_asker_query or carrying the plain C11 phrase "not available from the Analyst yet".
. "$(dirname "$0")/_root.sh"
S="org/tier0_utility/0.0.3_BG_BBGTerminal"
old=$(git show "$OA_BASE:$S/prompt.md" 2>/dev/null)
new=$(git -C opal_ai show "$OA_NESTED_PIN:opal/agent/prompt.md" 2>/dev/null)
[ -n "$new" ] || { echo "opal_ai $OA_NESTED_PIN:opal/agent/prompt.md absent (fetch the pin: git -C opal_ai fetch origin)"; echo "RESULT: FAIL"; exit 1; }
sect() { printf '%s\n' "$1" | awk '/^## Hard lines/{f=1} f&&/^## /&&!/^## Hard lines/{exit} f'; }
hl_old=$(sect "$old" | git hash-object --stdin); hl_new=$(sect "$new" | git hash-object --stdin)
hl=no; [ -n "$(sect "$old")" ] && [ "$hl_old" = "$hl_new" ] && hl=yes
lo=$(printf '%s\n' "$old" | grep -cE 'register_agent|/watcher|secretsmanager')
ln=$(printf '%s\n' "$new" | grep -cE 'register_agent|/watcher|secretsmanager')
wh=$(printf '%s\n' "$new" | grep -c 'whoami')
map=$(printf '%s\n' "$new" | awk '/^## RUNTIME MECHANISM MAP/{f=1;next} f&&/^## /{exit} f')
rows=0; ok=0
for i in 1 2 3 4 5 6 7 8; do
  r=$(printf '%s\n' "$map" | grep -E "^\| *$i *\|" | head -1)
  [ -n "$r" ] && rows=$((rows+1))
  printf '%s' "$r" | grep -Eq 'opal_asker_query|not available from the Analyst yet' && ok=$((ok+1))
done
r7=$(printf '%s\n' "$map" | grep -E '^\| *7 *\|' | grep -c 'not available from the Analyst yet')
echo "hard-lines byte-equal=$hl; launch acts named: cut=$lo runtime=$ln; whoami mentions=$wh; map rows $rows of 8, resolved $ok of 8; row 7 declined=$r7"
if [ "$hl" = yes ] && [ "$lo" -gt 0 ] && [ "$ln" = 0 ] && [ "$wh" -gt 0 ] && [ "$rows" = 8 ] && [ "$ok" = 8 ] && [ "$r7" = 1 ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
