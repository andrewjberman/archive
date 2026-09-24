#!/usr/bin/env bash
# OA-w-1 AC3 (refusal, difference control): with the MAIN tree's opal_ai uninitialised, `provision --nested opal_ai=<ref>`
# refuses rc 2 with a line naming opal_ai as uninitialised and creates NOTHING. At the base the flag does not exist, so
# the refusal is "unknown argument" -- same rc, different reason -- and this check FAILS there by the reason, not the rc.
. "$(dirname "$0")/_root.sh"
M=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
T="${TMPDIR:-/tmp}/oa_w1_ac3_$$"
out=$(timeout 100 bash .tools/wk-provision.sh provision NFRA_OPALAI 97 --path "$T" --nested opal_ai=DEV 2>&1); rc=$?
created=no; [ -e "$T" ] && created=yes
if [ "$created" = yes ]; then
  git worktree remove --force "$T" >/dev/null 2>&1
  git branch -D wk-NFRA_OPALAI-97 >/dev/null 2>&1
fi
init=no; [ -e "$M/opal_ai/.git" ] && init=yes
line=$(printf '%s\n' "$out" | grep -m1 'REFUSED' || echo "(no REFUSED line)")
echo "main-tree opal_ai initialised=$init; rc=$rc; created=$created; $line"
if [ "$init" = no ] && [ "$rc" = 2 ] && [ "$created" = no ] \
   && printf '%s\n' "$out" | grep -Eq 'REFUSED:.*opal_ai.*uninitiali[sz]ed'; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
