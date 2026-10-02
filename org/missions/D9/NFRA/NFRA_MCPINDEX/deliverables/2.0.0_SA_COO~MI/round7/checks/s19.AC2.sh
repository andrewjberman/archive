#!/usr/bin/env bash
# MX-s-19 AC2 (acceptance, CTO item 1(v)): on the first Mon AND Tue run dates after the retirement (2026-10-05,
# 2026-10-06 -- BD's late-posting empty window), a BRONZE_COMPLETE sentinel exists and the SCHEDULED bd-silver-merge run
# for that run_date logged a transactions SUMMARY with failures=0, with silver/transactions/<date>.parquet landing that run.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; n=0; ok=0
for D in 2026-10-05 2026-10-06; do n=$((n+1))
  s=$(timeout 30 "$AWS" s3api head-object --bucket opal-data-bd --key "bronze/$D/_BRONZE_COMPLETE.json" --query LastModified --output text 2>&1 | tr -d '\r')
  st=$(python -c "import datetime;print(int(datetime.datetime.fromisoformat('${D}T00:00:00+00:00').timestamp()*1000))")
  lg=$(timeout 60 "$AWS" logs filter-log-events --log-group-name /aws/lambda/bd-silver-merge --start-time "$st" --end-time $((st+86400000)) --query 'events[].message' --output text 2>&1 | tr -d '\r' | tr '\t' '\n')
  tx=$(printf '%s\n' "$lg" | awk '/Incremental Merge \[transactions\]/{f=1} f&&/SUMMARY/{print; exit}')
  pq=$(timeout 60 "$AWS" s3api list-objects-v2 --bucket opal-data-bd --prefix silver/transactions/ --query 'Contents[].LastModified' --output text 2>&1 | tr -d '\r' | tr '\t' '\n' | awk -v a="${D}T00:00:00" -v b="${D}T03:00:00" '$0>=a && $0<b {n++} END {print n+0}')
  good=0; case "$s" in 20*) case "$tx" in *'failures=0'*) case "$pq" in [1-9]*) good=1;; esac;; esac;; esac
  [ "$good" = 1 ] && ok=$((ok+1))
  echo "$D: sentinel=${s:-ABSENT}; transactions summary=[${tx:-NONE}]; transactions partitions written ${D} 00:00-03:00Z=${pq:-UNREAD}"
done
echo "empty-window acceptance dates passing $ok of $n"
rc=1; [ "$ok" = "$n" ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
