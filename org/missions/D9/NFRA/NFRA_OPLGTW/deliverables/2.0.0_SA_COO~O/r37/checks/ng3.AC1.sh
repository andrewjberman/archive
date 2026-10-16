#!/usr/bin/env bash
# OPLGTW OG-ng-3 AC1 (round-37, row Z-S161): the full-add naming gate in ENFORCE over EVERY app module the OG-ap-23 release takes whole prints no REFUSE.
# (ng2.AC2 graded only the client modules and portal_json_served; the applier's release commit grades all of them.)
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D=$(mktemp -d); : > "$D/all.diff"
A="$GW/app"
files="$(ls $A/client_*.py) $A/portal_json_served.py $A/portal_served.py $A/etfs_silver.py $A/etfs_rivals.py $A/etfs_rivals_flow.py $A/mdpf_classification.py $A/admin_gateway_breakdown.py $A/admin_people.py"
for f in $files; do [ -f "$f" ] || { echo "missing $f"; echo "RESULT: FAIL"; exit 1; }; done
n=0; for f in $files; do git diff --no-index --no-color /dev/null "$f" >> "$D/all.diff" 2>/dev/null; n=$((n+1)); done
printf 'org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/x.json\n' > "$D/paths.txt"
for f in $files; do printf '%s\n' "$f" >> "$D/paths.txt"; done
timeout 115 python .tools/naming-gate.py --diff "$D/all.diff" --staged-paths "$D/paths.txt" --enforce > "$D/gate.out" 2>&1; grc=$?
refuse=$(grep -c "NAMING REFUSE" "$D/gate.out"); ruled=$(grep -c "NAMING RULED" "$D/gate.out"); graded=$(grep -oE 'NAMING-GATE: [A-Z]+ [0-9]+ graded' "$D/gate.out" | tail -1)
echo "full-add naming gate over $n release modules in ENFORCE: rc=$grc; REFUSE verdicts $refuse (want 0); RULED verdicts $ruled; $graded"
[ "$grc" = 0 ] && [ "$refuse" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
