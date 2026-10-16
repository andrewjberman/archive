#!/usr/bin/env bash
# drain.sh <n> <id> <slug> <what>: wait for a clear shared tree, safe-merge the worker branch, resolve by id-union if needed.
S="C:/Users/OPALBL~1/AppData/Local/Temp/claude/C--Users-Opal-Bloomberg-Desktop-ajb-workspace/b0503755-bb6d-429f-ab74-832301c56fa5/scratchpad"; O="$S/merge_out.txt"
n=$1; id=$2; slug=$3; what=$4; T=org/missions/D9/NFRA/NFRA_OPLGTW/task-orders; OR=$T/NFRA_OPLGTW.TO-OG-$id.$slug.md
M="drain(NFRA_OPLGTW.TO-OG-$id): merge worker 0.9.0_WK_NFRA_OPLGTW~$n -- $what, instance VALID"
for try in 1 2 3 4; do
  for w in $(seq 1 12); do if git rev-parse -q --verify MERGE_HEAD >/dev/null || [ -n "$(git diff --cached --name-only)" ]; then sleep 20; else break; fi; done
  bash .tools/safe-merge.sh wk-NFRA_OPLGTW-$n -m "$M" > "$O" 2>&1; rc=$?
  if git rev-parse -q --verify MERGE_HEAD >/dev/null && grep -q "wk-NFRA_OPLGTW-$n" .git/safe-merge-conflict.branch 2>/dev/null; then python "$S/resolve_merge.py" $OR complete >/dev/null; bash .tools/safe-merge.sh --continue -m "$M" > "$O" 2>&1; rc=$?; fi
  if grep -q "MERGED and committed" "$O" || git log --oneline -30 | grep -q "TO-OG-$id): merge worker"; then echo "$id try $try: merged"; git log --oneline -30 | grep "TO-OG-$id): merge worker" | head -1 | cut -c1-80; exit 0; fi
  echo "$id try $try: rc=$rc $(grep -E 'REFUSED' "$O" | head -1 | cut -c1-150)"
done
exit 1
