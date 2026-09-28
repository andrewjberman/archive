#!/usr/bin/env bash
# MX-s-10 AC2 (the schedule is ported, not replaced): EventBridge rule bd-asset-dim-pipeline-trigger is ENABLED on
# cron(10 22 ? * MON-FRI *) and its target is the bd-asset-dim-trigger Lambda. One producer before and after.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
st=$(timeout 60 "$AWS" events describe-rule --name bd-asset-dim-pipeline-trigger --query '[State,ScheduleExpression]' --output text 2>&1 | tr -d '\r')
tg=$(timeout 60 "$AWS" events list-targets-by-rule --rule bd-asset-dim-pipeline-trigger --query 'Targets[].Arn' --output text 2>&1 | tr -d '\r')
state=$(printf '%s' "$st" | awk '{print $1}'); cron=$(printf '%s' "$st" | cut -f2)
ok_t=no; printf '%s' "$tg" | grep -q ':function:bd-asset-dim-trigger' && ok_t=yes
ntg=$(printf '%s' "$tg" | wc -w | tr -d ' ')
echo "rule state=$state schedule=$cron targets=$ntg targets bd-asset-dim-trigger=$ok_t"
if [ "$state" = ENABLED ] && [ "$cron" = 'cron(10 22 ? * MON-FRI *)' ] && [ "$ok_t" = yes ] && [ "$ntg" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
