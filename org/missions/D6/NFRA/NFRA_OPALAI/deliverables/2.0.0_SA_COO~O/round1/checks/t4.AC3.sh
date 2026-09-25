#!/usr/bin/env bash
# OA-t-4 AC3 (AMENDED to the CTO's ruling I-3, ROUND1_ANALYSIS_INPUTS.md @c1717499bf): the Analyst's watch is committed in
# opal_ai as its own program, and the OPERATOR plane's copy stays -- .claude/skills/teams-assist/teams-watch.py and the
# operator's /teams-assist SKILL.md are byte-equal (git blob) to the cut, because the D7 intake runner and Andrew's
# catch-up read the operator's Claude credentials through it, which the runtime never does.
. "$(dirname "$0")/_root.sh"
there=no; git -C opal_ai cat-file -e "HEAD:opal/agent/teams_watch/teams-watch.py" 2>/dev/null && there=yes
eq() { a=$(git rev-parse -q --verify "HEAD:$1" 2>/dev/null); b=$(git rev-parse -q --verify "$OA_BASE:$1" 2>/dev/null); [ -n "$a" ] && [ "$a" = "$b" ] && echo yes || echo no; }
w=$(eq .claude/skills/teams-assist/teams-watch.py); k=$(eq .claude/skills/teams-assist/SKILL.md)
echo "moved watch committed in opal_ai=$there; operator teams-watch.py byte-equal to the cut=$w; operator /teams-assist SKILL.md byte-equal to the cut=$k"
if [ "$there" = yes ] && [ "$w" = yes ] && [ "$k" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
