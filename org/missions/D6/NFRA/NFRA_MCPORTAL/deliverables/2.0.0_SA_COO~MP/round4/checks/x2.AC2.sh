#!/usr/bin/env bash
# MP-x-2 AC2 (the sidebar): PAGES' labels are Andrew's brief order with "Control Plane" appended last, and the whole
# mcportal suite (`bun test`, sidebar test included) exits 0 with 0 fail.
. "$(dirname "$0")/_root.sh"
[ -f mcportal/src/shell/pages.ts ] || { echo "pages.ts absent"; echo "RESULT: FAIL"; exit 1; }
labels=$(grep -oE "label: '[^']+'" mcportal/src/shell/pages.ts | sed -E "s/label: '([^']+)'/\1/" | paste -sd'|' -)
want="Home|Operations Report|User Management|User Analytics|MCP Server|Health Check|Cost Management|Infosec|Control Plane"
out=$(cd mcportal && NO_COLOR=1 timeout 150 bun test 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
echo "labels: $labels"; echo "bun test rc=$rc; fail=${fails:-?}"
if [ "$labels" = "$want" ] && [ "$rc" = 0 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
