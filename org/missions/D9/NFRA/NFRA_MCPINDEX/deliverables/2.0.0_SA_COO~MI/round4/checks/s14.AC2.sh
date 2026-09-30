#!/usr/bin/env bash
# MX-s-14 AC2 (the one producer, re-enabled on the ported document): EventBridge bd-transaction-pipeline-trigger reads
# ENABLED on cron(53 21 ? * MON-FRI *) with exactly 1 target, the bd-transactions-trigger Lambda. (MX-i-5 disables it
# first; this cell re-enables it only in its PHASE B.)
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; R=bd-transaction-pipeline-trigger
st=$(timeout 40 "$AWS" events describe-rule --name $R --query '[State,ScheduleExpression]' --output text 2>&1 | tr -d '\r')
state=$(printf '%s' "$st" | awk '{print $1}'); cron=$(printf '%s' "$st" | cut -f2)
tg=$(timeout 40 "$AWS" events list-targets-by-rule --rule $R --query 'Targets[].Arn' --output text 2>&1 | tr -d '\r')
ntg=$(printf '%s\n' "$tg" | tr '\t' '\n' | grep -c 'arn:'); hit=$(printf '%s' "$tg" | grep -c 'function:bd-transactions-trigger')
echo "rule state=$state schedule=$cron targets=$ntg targets bd-transactions-trigger=$([ "$hit" -ge 1 ] && echo yes || echo no)"
if [ "$state" = ENABLED ] && [ "$cron" = 'cron(53 21 ? * MON-FRI *)' ] && [ "$ntg" = 1 ] && [ "$hit" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
