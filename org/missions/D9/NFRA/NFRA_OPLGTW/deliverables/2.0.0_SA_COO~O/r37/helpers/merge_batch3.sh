#!/usr/bin/env bash
# merge_batch.sh: verify each worker's checks as issuer, sync its branch with status complete, commit the staged order file, drain it.
S="C:/Users/OPALBL~1/AppData/Local/Temp/claude/C--Users-Opal-Bloomberg-Desktop-ajb-workspace/b0503755-bb6d-429f-ab74-832301c56fa5/scratchpad/sync_branch.py"
ROOT="C:/Users/Opal Bloomberg/Desktop/ajb_workspace"
R=org/missions/D9/NFRA/NFRA_OPLGTW
C="$ROOT/$R/deliverables/2.0.0_SA_COO~O/r37/checks"
PROT=$R/deliverables/2.0.0_SA_COO~O/r37/G2_ADAPTER_PROTOCOL.md
MSG=C:/tmp/merge_batch_msg.txt
cat > $MSG <<'E'
sync(NFRA_OPLGTW round 37, 2.0.0_SA_COO~O): the order file at trunk text with the worker's status (complete) before the drain

Verified by the issuer in the worker's worktree: both criteria PASS, proof instance VALID.
Push state: LOCAL (not pushed; box-sync pushes).

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
E
# "<slot> <short> <cell-id-for-drain> <slug> <what>"
while IFS='|' read -r n short id slug what; do
  [ -z "$n" ] && continue
  W="C:/tmp/wk-oplgtw-$n"
  ORDER=$R/task-orders/NFRA_OPLGTW.TO-OG-$id.$slug.md
  cd "$W" || { echo "$id: no worktree"; continue; }
  git checkout HEAD -- $PROT 2>/dev/null
  a1=$(bash "$C/$short.AC1.sh" 2>&1 | tail -1); a2=$(timeout 118 bash "$C/$short.AC2.sh" 2>&1 | tail -1)
  echo "$id verify: AC1 $a1 | AC2 $a2"
  if [ "$a1" != "RESULT: PASS" ] || [ "$a2" != "RESULT: PASS" ]; then echo "$id: NOT MERGED (a check failed)"; continue; fi
  python "$S" $ORDER complete > /tmp/sync_$n.out 2>&1
  if [ -n "$(git diff --cached --name-only | grep -v '^portal$')" ]; then
    timeout 110 bash .tools/safe-commit.sh --author "2.0.0_SA_COO~O <2.0.0_SA_COO~O@opal.agent>" -F $MSG -- $ORDER > /tmp/sync_commit_$n.out 2>&1
  fi
  git checkout HEAD -- $PROT 2>/dev/null
  cd "$ROOT" || exit 1
  bash C:/tmp/drain.sh $n $id $slug "$what" 2>&1 | tail -n 2
done <<'LIST'
107|cl5|cl-5|client-smartx|the SmartX adapter (row filter by advisor_id through the roster name join, A2) behind the five client tools, AC1 8 of 8, AC2 PASS live
108|cl6|cl-6|client-commonwealth|the Commonwealth adapter (closed delivery) behind the five client tools, AC1 7 of 7, AC2 PASS live
LIST
