#!/usr/bin/env bash
# OPLGTW OG-rr-2 AC2 (round-37, CTO ruling @8b9adcbd8d s3 cell 2: "before cell 2 merges, re-run the full-add gate over the repo, and print the number of names whose grade moved (expected 0)"):
# the full-add naming gate over EVERY app module the OG-ap-23 release took whole, run with the gate as it was before this cell (the pinned blob) and with the gate as it is now:
# the per-line verdict lists are equal (names whose grade moved 0) and the new gate prints no REFUSE in ENFORCE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
PIN=ecd2aad5d0
D=$(mktemp -d); : > "$D/all.diff"
OLD=".tools/_naming_gate_pre_rr2_$$.py"
trap 'rm -f "$OLD"' EXIT
git show "$PIN:.tools/naming-gate.py" > "$OLD" || { echo "cannot read the pinned gate $PIN"; echo "RESULT: FAIL"; exit 1; }
A="$GW/app"
files="$(ls $A/client_*.py) $A/portal_json_served.py $A/portal_served.py $A/etfs_silver.py $A/etfs_rivals.py $A/etfs_rivals_flow.py $A/mdpf_classification.py $A/admin_gateway_breakdown.py $A/admin_people.py"
for f in $files; do [ -f "$f" ] || { echo "missing $f"; echo "RESULT: FAIL"; exit 1; }; done
n=0; for f in $files; do git diff --no-index --no-color /dev/null "$f" >> "$D/all.diff" 2>/dev/null; n=$((n+1)); done
printf 'org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/x.json\n' > "$D/paths.txt"
for f in $files; do printf '%s\n' "$f" >> "$D/paths.txt"; done
timeout 115 python "$OLD" --diff "$D/all.diff" --staged-paths "$D/paths.txt" --enforce > "$D/old.out" 2>&1; orc=$?
timeout 115 python .tools/naming-gate.py --diff "$D/all.diff" --staged-paths "$D/paths.txt" --enforce > "$D/new.out" 2>&1; nrc=$?
grep -E '^NAMING (REFUSE|RULED|WARN|OK|PASS|NEW)' "$D/old.out" | sort > "$D/old.v"
grep -E '^NAMING (REFUSE|RULED|WARN|OK|PASS|NEW)' "$D/new.out" | sort > "$D/new.v"
vold=$(wc -l < "$D/old.v" | tr -d ' '); vnew=$(wc -l < "$D/new.v" | tr -d ' ')
moved=$(comm -3 "$D/old.v" "$D/new.v" | wc -l | tr -d ' ')
refuse=$(grep -c "NAMING REFUSE" "$D/new.out")
echo "full-add re-grade over $n release modules: old gate rc=$orc, new gate rc=$nrc; verdict lines old $vold, new $vnew; verdict lines that differ (names whose grade moved) $moved (want 0); new-gate REFUSE verdicts $refuse (want 0)"
[ "$orc" = 0 ] && [ "$nrc" = 0 ] && [ "$vold" -ge 1 ] && [ "$moved" = 0 ] && [ "$refuse" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
