#!/usr/bin/env bash
# MX-f-1r AC2: the guarded comprehension holds exactly the 5 daily platinum keys it held before 3d7fb62105 -- the two
# weekly silver entries (no as_of_field / frontier_page_trading_days) are excluded, and nothing else moved.
# Needs AC1's init in the same tree. Run from the worktree root.
M=infra/aws/terraform/bd-pipeline
want='["bd_platinum_cumulative_chart","bd_platinum_dashboard","bd_platinum_header_metrics","bd_platinum_leaderboard","bd_platinum_partner_analytics"]'
got=$(echo 'jsonencode(sort(keys(local.bd_served_vintage_keys)))' | terraform -chdir="$M" console 2>&1 | tr -d '\r' | tail -1)
got=$(printf '%s' "$got" | python -c "import sys,json; s=sys.stdin.read().strip(); s=json.loads(s) if s.startswith('\"') else s; print(s)")
echo "keys=$got"
echo "want=$want"
if [ "$got" = "$want" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
