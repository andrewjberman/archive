#!/usr/bin/env bash
# OG-rl-7 PHASE A: pull the gateway audit lake (s3://opal-mcp-audit/audit/dt=<day>/) for a day range into a scratch dir (read-only on S3).
# usage: r19_lake_pull.sh <first day> <last day> <scratch dir>   (days YYYY-MM-DD, inclusive; UTC partitions)
first="$1"; last="$2"; dest="$3"
mkdir -p "$dest"
d="$first"
n=0
while [ "$d" != "$(date -u -d "$last + 1 day" +%F)" ]; do
  aws s3 sync "s3://opal-mcp-audit/audit/dt=$d/" "$dest/dt=$d/" --region us-east-1 --only-show-errors || echo "SYNC_FAIL $d"
  n=$((n+1)); d=$(date -u -d "$d + 1 day" +%F)
done
echo "DAYS_PULLED $n"
