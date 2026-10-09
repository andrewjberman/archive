#!/usr/bin/env bash
# OA-f-15 AC1 (row Z-S67/Z-S68): the Analyst's copies carry the post-move Teams fixes, at opal_ai ${OA_F15_REF:-HEAD}.
# - every Teams arm pin under opal/agent names the opalbloomberg oid; no `--identity opalbloomberg` is left anywhere;
# - the skill's arm line is bounded: `timeout 1770 python opal/agent/teams_watch/teams-watch.py ...`;
# - the skill has a step 0b SENDER GATE placed before step 1 (ACK);
# - only the skill and RELAUNCH.md differ from c9983bd2ac.
. "$(dirname "$0")/_root.sh"
REF="${OA_F15_REF:-HEAD}"; BASE="c9983bd2ac"
S="opal/agent/skills/bbg-teams-assist/SKILL.md"; R="opal/agent/refs/RELAUNCH.md"; OID="517aa5ee-b4d0-425a-b493-5a22ff77ac4f"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
sk=$(git -C opal_ai show "$REF:$S" 2>/dev/null) || { echo "skill absent at $REF"; echo "RESULT: FAIL"; exit 1; }
rl=$(git -C opal_ai show "$REF:$R" 2>/dev/null) || { echo "RELAUNCH absent at $REF"; echo "RESULT: FAIL"; exit 1; }
old=$(git -C opal_ai grep -c -F -e '--identity opalbloomberg' "$REF" -- opal/agent | awk -F: '{s+=$NF} END{print s+0}')
skoid=$(printf '%s' "$sk" | grep -c -F -e "--identity $OID")
rloid=$(printf '%s' "$rl" | grep -c -F -e "--identity $OID")
bound=$(printf '%s' "$sk" | grep -c -E "^timeout 1770 python opal/agent/teams_watch/teams-watch\.py --server opal-gateway-bbg --identity $OID")
g=$(printf '%s\n' "$sk" | grep -n -E '^\*\*0b\. SENDER GATE' | head -1 | cut -d: -f1); a=$(printf '%s\n' "$sk" | grep -n -E '^\*\*1\. ACK' | head -1 | cut -d: -f1)
order=no; [ -n "$g" ] && [ -n "$a" ] && [ "$g" -lt "$a" ] && order=yes
other=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -e "$S" -e "$R" | grep -c .)
echo "opal_ai $REF: name pins left=$old; skill oid pins=$skoid; RELAUNCH oid pins=$rloid; bounded skill arm line=$bound; sender gate before ACK=$order; other files changed vs $BASE=$other"
if [ "$old" = 0 ] && [ "$skoid" -ge 2 ] && [ "$rloid" -ge 1 ] && [ "$bound" = 1 ] && [ "$order" = yes ] && [ "$other" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
