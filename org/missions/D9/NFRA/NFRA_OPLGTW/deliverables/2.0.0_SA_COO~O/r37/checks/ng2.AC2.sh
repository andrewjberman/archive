#!/usr/bin/env bash
# OPLGTW OG-ng-2 AC2 (round-37, XA-20261016T034740Z-28da): the full-add naming gate in ENFORCE over every client module AND app/portal_json_served.py prints no REFUSE:
# the ten lines (8 bd49f, 2 etfs) the gate refused are graded RULED from their name_rulings.json rows.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D=$(mktemp -d); : > "$D/all.diff"
files="$(ls "$GW"/app/client_*.py 2>/dev/null) $GW/app/portal_json_served.py"
for f in $files; do [ -f "$f" ] || { echo "missing $f"; echo "RESULT: FAIL"; exit 1; }; done
for f in $files; do git diff --no-index --no-color /dev/null "$f" >> "$D/all.diff" 2>/dev/null; done
printf 'org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/x.json\n' > "$D/paths.txt"
for f in $files; do printf '%s\n' "$f" >> "$D/paths.txt"; done
timeout 115 python .tools/naming-gate.py --diff "$D/all.diff" --staged-paths "$D/paths.txt" --enforce > "$D/gate.out" 2>&1; grc=$?
refuse=$(grep -c "NAMING REFUSE" "$D/gate.out"); ruled=$(grep -c "NAMING RULED" "$D/gate.out"); graded=$(grep -oE 'NAMING-GATE: [A-Z]+ [0-9]+ graded' "$D/gate.out" | tail -1)
echo "full-add naming gate over the client modules and portal_json_served in ENFORCE: rc=$grc; REFUSE verdicts $refuse (want 0); RULED verdicts $ruled (want 10); $graded"
[ "$grc" = 0 ] && [ "$refuse" = 0 ] && [ "$ruled" -ge 10 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
