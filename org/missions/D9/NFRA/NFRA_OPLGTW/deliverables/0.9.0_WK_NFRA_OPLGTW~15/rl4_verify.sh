#!/usr/bin/env bash
# OG-rl-4 PHASE B verify (row W15-S18, filed as Z-W15-S30): usage  rl4_verify.sh before|after <state.json>
# `before` saves the host's BEFORE reads and the three route read codes (run before the act); the state file holds names, 16-hex
# process-env hash prefixes and status codes -- keep it OUT of the repository (e.g. <worktree>/.scratch/rl4_before.json).
# `after` runs the host reads and every comparison (rl4_verify.py), then rl4.AC1.sh, tr.AC1.sh and ht.AC2.sh.
# Run `after` IMMEDIATELY after safe-ec2-deploy.sh returns. Any FAIL below: roll back (ANNOUNCE_OG-rl-4.md), re-verify, close ROLLED BACK.
# Env: OG_REL_TREE (default /c/tmp/og-rel9) supplies the shipped sender table whose first address the mail listing read uses.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~15}"
REL="${OG_REL_TREE:-/c/tmp/og-rel9}"
export OG_RL4_MAIL_SENDER="$(tr -d '\r' < "$REL/infra/aws/ec2/opal-gateway/deploy/mail_sender_table.txt" | grep -m1 . | tr 'A-Z' 'a-z')"
[ -n "$OG_RL4_MAIL_SENDER" ] || { echo "ERROR: no sender in the shipped table at $REL"; exit 2; }
python "$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/rl4_verify.py" || echo "$HERE/rl4_verify.py")" "$1" "$2"; rc=$?
[ "$1" = "after" ] || exit $rc
ROOT="$(cd "$HERE" && git rev-parse --show-toplevel)"
cd "$ROOT" || exit 9
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
echo "--- rl4.AC1.sh ---"; out1=$(bash "$C/r14/checks/rl4.AC1.sh" 2>&1); rc1=$?; printf '%s\n' "$out1"
echo "--- tr.AC1.sh ---"; out2=$(bash "$C/trnspt/checks/tr.AC1.sh" 2>&1); rc2=$?; printf '%s\n' "$out2"
echo "--- ht.AC2.sh ---"; out3=$(bash "$C/hxteams/checks/ht.AC2.sh" 2>&1); rc3=$?; printf '%s\n' "$out3"
# tr.AC1.sh arm 4 hard-codes ".env 48 keys" (stale since OG-rl-3 made it 50; row Z-W15-S32): its arms 1-3 must be OK and its host line
# must read the same capability-ON shape at 50 keys; that is graded here instead of the script's own rc (the script is the issuer's, unedited).
tr_ok=no
if [ "$rc2" = 0 ]; then tr_ok=yes
elif [ "$(printf '%s\n' "$out2" | grep -c '^arm [123] .*: OK$')" = 3 ] && printf '%s\n' "$out2" | grep -qE '^HOST env_keys 50 taxsma_keys 2 identity_empty False bearer_empty False$'; then tr_ok=yes-with-stale-arm-4; fi
echo "rl4_verify: host/route checks rc=$rc; rl4.AC1 rc=$rc1; tr.AC1 rc=$rc2 (graded $tr_ok); ht.AC2 rc=$rc3"
[ "$rc" = 0 ] && [ "$rc1" = 0 ] && [ "$tr_ok" != no ] && [ "$rc3" = 0 ]
