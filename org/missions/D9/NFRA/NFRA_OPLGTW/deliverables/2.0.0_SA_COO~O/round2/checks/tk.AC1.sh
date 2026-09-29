#!/usr/bin/env bash
# OPLGTW OG-t-1 AC1 (R-3 (a) and (f), rulings Q1/Q2 @5676f4a48a): tier.py reads no email set; no call site passes an email
# to resolve_tier; config declares the two principal rosters; and the NAMED out-of-scope files -- the email sets
# resolve_tier does not read, plus the machine/bearer path (app/ms_ingest.py) -- are touched by NO commit of the build
# worker (author 0.9.0_WK_NFRA_OPLGTW~12). Author-scoped, so it reads the same in the worker's worktree and on CLOUD.
. "$(dirname "$0")/_root.sh"
A="${OG_T1_AUTHOR:-0.9.0_WK_NFRA_OPLGTW~12}"
emails=$(grep -cE 'MASTER_ADMIN_EMAILS|WRITE_CAPABLE_EMAILS' "$GW/app/tier.py")
RX='resolve_tier[(][[:space:]]*(email|display|wanted)[[:space:]]*[,)]|def resolve_tier[(][[:space:]]*email'
calls=$(cat "$GW"/app/*.py "$GW"/app/integrations/*.py | grep -cE "$RX")
RC='^[[:space:]]+(MASTER_ADMIN_PRINCIPALS|WRITE_CAPABLE_PRINCIPALS)[[:space:]]*:'
cfg=$(grep -cE "$RC" "$GW/app/config.py")
OOS="$GW/app/owner_gate.py $GW/app/sprint_view.py $GW/identity_tool_allowlist.txt $GW/app/identity_scope.py $GW/app/query_v0.py $GW/app/data_entitlement.py $GW/app/ms_ingest.py"
moved=0; named=0
for f in $OOS; do
  named=$((named+1))
  n=$(git log --format=%H --author="$A <" HEAD -- "$f" | grep -c .)
  if [ "$n" != 0 ]; then moved=$((moved+1)); echo "out-of-scope file touched by $A: $f ($n commit(s))"; fi
done
echo "email sets read by tier.py=$emails; email-keyed resolve_tier call sites=$calls; principal rosters declared=$cfg of 2; out-of-scope named=$named moved=$moved"
if [ "$emails" = 0 ] && [ "$calls" = 0 ] && [ "$cfg" = 2 ] && [ "$moved" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
