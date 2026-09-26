#!/usr/bin/env bash
# MX-s-2 AC1 (a PRODUCTION schedule, fired): an EventBridge rule or Scheduler schedule whose name contains
# "assets-dim" exists and is ENABLED, and opal-data-bd silver/bd_assets_dim.parquet was last written AFTER this order's
# issue (2026-09-25T23:00:00Z) -- the builder ran (one ad-hoc QA fire is allowed; the schedule stays the acceptance).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; ISSUED="2026-09-25T23:00:00"
r=$(timeout 60 "$AWS" events list-rules --query "Rules[?contains(Name,'assets-dim')].[Name,State]" --output text 2>/dev/null | tr -d '\r')
s=$(timeout 60 "$AWS" scheduler list-schedules --query "Schedules[?contains(Name,'assets-dim')].[Name,State]" --output text 2>/dev/null | tr -d '\r')
en=$(printf '%s\n%s\n' "$r" "$s" | grep -c 'ENABLED')
lm=$(timeout 60 "$AWS" s3api head-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet --query LastModified --output text 2>/dev/null | tr -d '\r')
fresh=$(python -c "import sys;print('yes' if sys.argv[1][:19] > sys.argv[2] else 'no')" "$lm" "$ISSUED" 2>/dev/null)
echo "schedules/rules named *assets-dim* ENABLED=$en ($(printf '%s %s' "$r" "$s" | tr '\n\t' '  ' | cut -c1-160)); bd_assets_dim.parquet LastModified=${lm:-NONE} after issue=$fresh"
if [ "$en" -ge 1 ] && [ "$fresh" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
