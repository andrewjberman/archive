#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t1.AC1.sh (2.0.0_SA_COO~AI). ONE amendment: the nested opal_ai is read at $OA_NESTED_PIN (the move's drain commit), never at its HEAD.
# OA-t-1 AC1 (built): the slice-first layout and the moved product files are COMMITTED in the nested opal_ai repo, and the
# files moved without edit are byte-equal (git blob id) to their parent copies at the cut.
# Amended per the CTO's ruling I-4 (D-1): refs/census/ does NOT move in round 1, so opal_ai must carry none of it.
. "$(dirname "$0")/_root.sh"
S="org/tier0_utility/0.0.3_BG_BBGTerminal"
NEW="README.md opal/README.md template/README.md clients/README.md docs/README.md opal/agent/prompt.md
opal/agent/refs/BLOOMBERG_GUARDRAILS.md opal/agent/refs/BUCKET_ALLOWLIST.yaml opal/agent/refs/PORTAL_RETRIEVAL.md
opal/agent/refs/RELAUNCH.md opal/agent/refs/REQUEST_CATALOG.md opal/agent/refs/TEAMS_DUTY.md opal/agent/refs/THREAD_MEMORY.md
opal/agent/tools/portal_lookup.py opal/agent/skills/bbg-teams-assist/SKILL.md"
# new-path:old-path pairs moved WITHOUT edit (PORTAL_RETRIEVAL.md, prompt.md and SKILL.md are edited by the cell)
EQ="BLOOMBERG_GUARDRAILS.md BUCKET_ALLOWLIST.yaml RELAUNCH.md REQUEST_CATALOG.md TEAMS_DUTY.md THREAD_MEMORY.md"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent at $(pwd)/opal_ai"; echo "RESULT: FAIL"; exit 1; }
git -C opal_ai cat-file -e "${OA_NESTED_PIN}^{commit}" 2>/dev/null || { echo "opal_ai pin $OA_NESTED_PIN unresolved (run: git -C opal_ai fetch origin)"; echo "RESULT: FAIL"; exit 1; }
tree=$(git -C opal_ai ls-tree -r --name-only "$OA_NESTED_PIN" 2>/dev/null)
n=0; p=0; miss=""
for f in $NEW; do n=$((n+1)); if printf '%s\n' "$tree" | grep -qxF "$f"; then p=$((p+1)); else miss="$miss $f"; fi; done
m=0; e=0; diff=""
for r in $EQ; do
  m=$((m+1))
  a=$(git -C opal_ai rev-parse -q --verify "$OA_NESTED_PIN:opal/agent/refs/$r" 2>/dev/null)
  b=$(git rev-parse -q --verify "$OA_BASE:$S/refs/$r" 2>/dev/null)
  if [ -n "$a" ] && [ "$a" = "$b" ]; then e=$((e+1)); else diff="$diff refs/$r"; fi
done
m=$((m+1))
a=$(git -C opal_ai rev-parse -q --verify "$OA_NESTED_PIN:opal/agent/tools/portal_lookup.py" 2>/dev/null)
b=$(git rev-parse -q --verify "$OA_BASE:$S/tools/portal_lookup.py" 2>/dev/null)
if [ -n "$a" ] && [ "$a" = "$b" ]; then e=$((e+1)); else diff="$diff tools/portal_lookup.py"; fi
c=$(printf '%s\n' "$tree" | grep -c '^opal/agent/refs/census/')
echo "present $p of $n; content-equal $e of $m; census files in opal_ai: $c"
[ -n "$miss" ] && echo "missing:$miss"
[ -n "$diff" ] && echo "not byte-equal:$diff"
if [ "$p" = "$n" ] && [ "$e" = "$m" ] && [ "$c" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
