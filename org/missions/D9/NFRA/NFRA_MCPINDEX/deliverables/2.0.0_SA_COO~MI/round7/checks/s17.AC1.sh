#!/usr/bin/env bash
# MX-s-17 AC1 (Z-W24-S3 disarm read): BOTH held documents (opal-bd-transaction-download, opal-bd-realized-download), at
# DEFAULT and at $LATEST, name code/silver/merge-daily-incremental.py and NO s3://opal-data-bd/scripts/ path.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; n=0; ok=0
for d in transaction realized; do for v in '$DEFAULT' '$LATEST'; do n=$((n+1))
  c=$(timeout 30 "$AWS" ssm get-document --name "opal-bd-$d-download" --document-version "$v" --query Content --output text 2>&1 | tr -d '\r')
  new=$(printf '%s' "$c" | grep -c 'code/silver/merge-daily-incremental.py'); old=$(printf '%s' "$c" | grep -c 's3://opal-data-bd/scripts/')
  if [ "$new" -ge 1 ] && [ "$old" = 0 ]; then ok=$((ok+1)); tag=OK; else tag=STALE; fi
  echo "$tag: opal-bd-$d-download $v code/silver refs=$new scripts/ refs=$old"
done; done
echo "documents repointed $ok of $n (2 documents x DEFAULT,LATEST)"
rc=1; [ "$ok" = "$n" ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
