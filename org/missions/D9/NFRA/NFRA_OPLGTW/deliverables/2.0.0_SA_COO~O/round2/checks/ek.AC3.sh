#!/usr/bin/env bash
# OPLGTW OG-e-1 AC3: the operator writer exposes the one-shot deny-backfill mode with its five named flags.
R="$(git rev-parse --show-toplevel)"; cd "$R/infra/aws/ec2/opal-gateway" || exit 9
h=$(timeout 60 python ops/schwab_entitlement_admin.py deny-backfill --help 2>&1); rc=$?
miss=0; for f in --tid --oid --email --approver --source-authorization; do printf '%s' "$h" | grep -q -- "$f" || miss=$((miss+1)); done
echo "deny-backfill --help rc=$rc flags missing=$miss of 5"
if [ "$rc" -eq 0 ] && [ "$miss" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
