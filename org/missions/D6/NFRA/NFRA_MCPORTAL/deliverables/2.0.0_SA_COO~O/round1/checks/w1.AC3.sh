#!/usr/bin/env bash
# MP-w-1 AC3 (built): the shell's sidebar test passes -- `bun test src/shell/sidebar.test.ts` runs the test named
# "sidebar lists the pages in the brief's order" and it passes, with no failure.
. "$(dirname "$0")/_root.sh"
[ -f mcportal/src/shell/sidebar.test.ts ] || { echo "mcportal/src/shell/sidebar.test.ts absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd mcportal && timeout 110 bun test src/shell/sidebar.test.ts 2>&1 | tr -d '\r'); rc=$?
named=$(printf '%s\n' "$out" | grep -c "sidebar lists the pages in the brief's order")
fails=$(printf '%s\n' "$out" | grep -oE '[0-9]+ fail' | head -1 | awk '{print $1}')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named test lines=$named; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$named" -ge 1 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
