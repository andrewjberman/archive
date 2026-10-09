#!/usr/bin/env bash
# OA-f-15 AC2 (row Z-S67): Andrew's sender gate reaches the Analyst UNCHANGED. The step-0b block of the opal_ai skill
# (from the line starting **0b. SENDER GATE up to, not including, the line starting **1. ACK) is byte-equal to the same
# block of the workspace skill at the pin ${OA_F15_WS_PIN:-33837fdea8} (Andrew-direct 2026-10-09 ~03:3xZ, ef8c4e57a1 +
# AMENDMENT 1 0c9fbd0876). Control: the block is non-empty on both sides.
. "$(dirname "$0")/_root.sh"
REF="${OA_F15_REF:-HEAD}"; PIN="${OA_F15_WS_PIN:-33837fdea8}"
blk() { awk '/^\*\*0b\. SENDER GATE/{p=1} /^\*\*1\. ACK/{p=0} p'; }
ws=$(git show "$PIN:.claude/skills/bbg-teams-assist/SKILL.md" 2>/dev/null | tr -d '\r' | blk)
oa=$(git -C opal_ai show "$REF:opal/agent/skills/bbg-teams-assist/SKILL.md" 2>/dev/null | tr -d '\r' | blk)
wl=$(printf '%s' "$ws" | grep -c .); ol=$(printf '%s' "$oa" | grep -c .)
eq=no; [ -n "$ws" ] && [ "$ws" = "$oa" ] && eq=yes
echo "sender-gate block: workspace@$PIN lines=$wl, opal_ai@$REF lines=$ol, byte-equal (CR-stripped)=$eq"
if [ "$wl" -gt 0 ] && [ "$eq" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
