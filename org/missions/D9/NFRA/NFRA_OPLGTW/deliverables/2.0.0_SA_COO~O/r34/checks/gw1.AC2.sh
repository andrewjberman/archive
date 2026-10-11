#!/usr/bin/env bash
# OPLGTW OG-gw-1 AC2 (round-34 E2): the TARGETED plan, saved at W/gw1_plan.txt with its exit code in W/gw1_plan.rc, read at
# rc=0, shows exactly "1 to change" and nothing else, and the one changed address is aws_lambda_function.mcportal_grant_writer.
# A summary line at rc!=0 is not a verdict, because a failed data source drops rows.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~56"
[ -f "$W/gw1_plan.txt" ] && [ -f "$W/gw1_plan.rc" ] || { echo "plan or rc file absent"; echo "RESULT: FAIL"; exit 1; }
rc=$(tr -d '\r\n ' < "$W/gw1_plan.rc"); plan=$(tr -d '\r' < "$W/gw1_plan.txt")
summ=$(printf '%s\n' "$plan" | grep -E '^Plan: ' | tail -1)
addrs=$(printf '%s\n' "$plan" | grep -E '^\s*# [a-z_.\[\]"0-9-]+ will be' | sed -E 's/^\s*# ([^ ]+) will be.*/\1/' | sort -u)
n=$(printf '%s\n' "$addrs" | grep -c .)
echo "plan rc=$rc; summary: $summ; changed addresses $n: $(printf '%s ' $addrs)"
[ "$rc" = 0 ] && [ "$summ" = "Plan: 0 to add, 1 to change, 0 to destroy." ] && [ "$n" = 1 ] \
  && [ "$addrs" = "aws_lambda_function.mcportal_grant_writer" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
