#!/usr/bin/env bash
# OPLGTW OG-dc-2 AC1 (row Z-S57, CTO R26): .tools/m365-mcp-kit/ holds README.md ONLY -- measured with git ls-files
# (which sees dotfiles and nested dirs; dc1.AC1's '*' glob did not, which is how .mcp.json and .claude/ survived) -- no
# kit file names the old Lokka entry, and README.md still carries the hosted reconnect command.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
K=".tools/m365-mcp-kit"
files=$(git ls-files "$K"; git ls-files --others --exclude-standard "$K")
n=$(printf '%s\n' "$files" | grep -c .)
only=no; [ "$n" = 1 ] && [ "$(printf '%s' "$files" | tr -d '\r\n')" = "$K/README.md" ] && only=yes
lokka=$(printf '%s\n' "$files" | grep . | while read -r f; do grep -lF 'Lokka' "$f" 2>/dev/null; done | grep -c .)
cmd=$(grep -cF 'claude mcp add --transport http -s user opalgateway https://mcp.opalinvest.dev/mcp' "$K/README.md" 2>/dev/null); cmd=${cmd:-0}
echo "kit files $n (README.md only: $only); files naming Lokka $lokka; README hosted command lines $cmd"
[ "$only" = yes ] && [ "$lokka" = 0 ] && [ "$cmd" -ge 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
