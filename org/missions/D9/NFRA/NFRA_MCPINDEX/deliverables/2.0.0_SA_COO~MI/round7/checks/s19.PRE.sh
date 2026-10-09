#!/usr/bin/env bash
# MX-s-19 PRE (amendment A5): the PHASE B precondition as ONE read, run on the A2 dates BEFORE the rule disable.
# For each run date (default the A2 dates 2026-10-12 and 2026-10-13; pass others as args): (1) the runner logged
# 'OK: bronze sentinel emitted for <D>' AND head-object finds bronze/<D>/_BRONZE_COMPLETE.json (the log line alone is not
# sound: pre-MX-s-18 code printed it on 2026-10-05 while the object was never written, 404); (2) the SCHEDULED bd-silver-merge run for <D>
# logged a transactions SUMMARY and a realized SUMMARY, both failures=0; (3) silver/transactions/ and silver/realized/
# each carry an object written <D> 00:00-03:00Z. (2)+(3) are the Z-W24-S8 discriminator: the Lambda, not the 21:54Z
# document, refreshes the newest LastModified the gold dispatch's freshness gate reads. All reads are AWS-only; no
# Black Diamond call, no invocation.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; n=0; ok=0
[ "$#" -gt 0 ] || set -- 2026-10-12 2026-10-13
for D in "$@"; do n=$((n+1))
  st=$(python -c "import datetime;print(int(datetime.datetime.fromisoformat('${D}T00:00:00+00:00').timestamp()*1000))")
  rl=$(timeout 60 "$AWS" logs filter-log-events --log-group-name /aws/lambda/bd-49f-runner --start-time "$st" --end-time $((st+10800000)) --filter-pattern '"bronze sentinel emitted"' --query 'events[].message' --output text 2>&1 | tr -d '\r' | tr '\t' '\n' | grep -c "OK: bronze sentinel emitted for $D")
  so=$(timeout 30 "$AWS" s3api head-object --bucket opal-data-bd --key "bronze/$D/_BRONZE_COMPLETE.json" --query LastModified --output text 2>&1 | tr -d '\r')
  lg=$(timeout 60 "$AWS" logs filter-log-events --log-group-name /aws/lambda/bd-silver-merge --start-time "$st" --end-time $((st+10800000)) --query 'events[].message' --output text 2>&1 | tr -d '\r' | tr '\t' '\n')
  tx=$(printf '%s\n' "$lg" | awk '/Incremental Merge \[transactions\]/{f=1} f&&/^SUMMARY/{print; exit}')
  re=$(printf '%s\n' "$lg" | awk '/Realized Incremental Merge/{f=1} f&&/^SUMMARY/{print; exit}')
  cnt() { timeout 60 "$AWS" s3api list-objects-v2 --bucket opal-data-bd --prefix "silver/$1/" --query 'Contents[].LastModified' --output text 2>&1 | tr -d '\r' | tr '\t' '\n' | awk -v a="${D}T00:00:00" -v b="${D}T03:00:00" '$0>=a && $0<b {n++} END {print n+0}'; }
  pt=$(cnt transactions); pr=$(cnt realized)
  good=0
  [ "$rl" -ge 1 ] && case "$so" in 20*) true;; *) false;; esac && case "$tx" in *'failures=0'*) case "$re" in *'failures=0'*) [ "$pt" -ge 1 ] && [ "$pr" -ge 1 ] && good=1;; esac;; esac
  [ "$good" = 1 ] && ok=$((ok+1))
  echo "$D: sentinel OK lines=$rl, object=${so:-UNREAD}; transactions=[${tx:-NONE}]; realized=[${re:-NONE}]; silver objects written 00:00-03:00Z: transactions=$pt realized=$pr"
done
echo "precondition dates passing $ok of $n"
rc=1; [ "$ok" = "$n" ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
