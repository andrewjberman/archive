#!/usr/bin/env bash
# MS-ir-1 AC2 (the seam: Terraform's own plan against the live account, read-only, unlocked, private data dir): a plan
# targeted at every resource of mcpmsp_internal_reader.tf reads "Plan: N to add, 0 to change, 0 to destroy" with N >= 3
# and shows the builder's role name gateway-global-internal-reader-role.
. "$(dirname "$0")/_root.sh"
F="$TF_DIR/mcpmsp_internal_reader.tf"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
targets=$(python -c "import re,sys;t=open(sys.argv[1],encoding='utf-8').read();print(' '.join('-target=%s.%s'%m for m in re.findall(r'^resource\s+\"([^\"]+)\"\s+\"([^\"]+)\"',t,re.M)))" "$F" | tr -d '\r')
[ -n "$targets" ] || { echo "no resource blocks"; echo "RESULT: FAIL"; exit 1; }
nm=$(opal_name gateway global internal-reader role)
PD=$(tf_private) ; [ -n "$PD" ] || { echo "no initialised .terraform in the main tree"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$TF_DIR" && TF_DATA_DIR="$PD" timeout 110 terraform plan -lock=false -input=false -no-color -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER $targets 2>&1 | tr -d '\r')
rm -rf "$PD"
line=$(printf '%s\n' "$out" | grep -m1 -E '^Plan: [0-9]+ to add' || printf '%s\n' "$out" | grep -m1 -E 'No changes|Error' || echo "(no plan line)")
named=$(printf '%s\n' "$out" | grep -cE "name +(=|\+) +\"$nm\"|\+ name += \"$nm\"")
echo "targets: $targets"; echo "plan: $line; planned role name $nm seen=$named"
add=$(printf '%s' "$line" | sed -nE 's/^Plan: ([0-9]+) to add, ([0-9]+) to change, ([0-9]+) to destroy.*/\1 \2 \3/p'); set -- $add
if [ -n "$add" ] && [ "$1" -ge 3 ] && [ "$2" = 0 ] && [ "$3" = 0 ] && [ "$named" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
