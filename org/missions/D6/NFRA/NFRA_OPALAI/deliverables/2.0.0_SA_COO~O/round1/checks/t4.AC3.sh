#!/usr/bin/env bash
# OA-t-4 AC3 (the move, parent side): .claude/skills/teams-assist/teams-watch.py is gone at HEAD, the moved watch is
# committed in opal_ai, and no code/config file at HEAD still names the old path (the operator's /teams-assist
# SKILL.md now names opal_ai/opal/agent/teams_watch/teams-watch.py).
. "$(dirname "$0")/_root.sh"
gone=yes; git cat-file -e "HEAD:.claude/skills/teams-assist/teams-watch.py" 2>/dev/null && gone=no
there=no; git -C opal_ai cat-file -e "HEAD:opal/agent/teams_watch/teams-watch.py" 2>/dev/null && there=yes
hits=$(git grep -l -F 'teams-assist/teams-watch.py' HEAD -- .claude/ .tools/ org/mcp/ '*.ps1' 2>/dev/null | sed 's/^HEAD://')
nh=$(printf '%s' "$hits" | grep -c .)
newref=$(git show "HEAD:.claude/skills/teams-assist/SKILL.md" 2>/dev/null | grep -c 'opal_ai/opal/agent/teams_watch/teams-watch.py')
echo "old path gone at HEAD=$gone; moved watch committed in opal_ai=$there; code/config files naming the old path=$nh; /teams-assist SKILL.md names the new path=$newref"
[ "$nh" != 0 ] && printf '%s\n' "$hits" | sed 's/^/  ref: /'
if [ "$gone" = yes ] && [ "$there" = yes ] && [ "$nh" = 0 ] && [ "$newref" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
