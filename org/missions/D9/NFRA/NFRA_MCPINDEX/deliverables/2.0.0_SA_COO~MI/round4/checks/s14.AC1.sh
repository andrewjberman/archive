#!/usr/bin/env bash
# MX-s-14 AC1 (as amended A1: strip, keep the merge): opal-bd-transaction-download read at $LATEST -- the version its
# trigger runs (row Z-S48) -- with DefaultVersion == LatestVersion carries no Playwright download
# (download-daily-transaction.ts) and no portal credential (BD_PASSWORD), and still runs the silver merge
# (merge-daily-incremental).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; D=opal-bd-transaction-download
v=$(timeout 60 "$AWS" ssm describe-document --name $D --query 'Document.[DefaultVersion,LatestVersion]' --output text 2>&1 | tr -d '\r')
dv=$(printf '%s' "$v" | awk '{print $1}'); lv=$(printf '%s' "$v" | awk '{print $2}')
c=$(timeout 60 "$AWS" ssm get-document --name $D --document-version '$LATEST' --query Content --output text 2>&1 | tr -d '\r')
[ -n "$c" ] || { echo "get-document returned nothing -- RESULT: FAIL"; exit 1; }
pw=$(printf '%s' "$c" | grep -c 'download-daily-transaction.ts'); pwd_=$(printf '%s' "$c" | grep -c 'BD_PASSWORD'); mg=$(printf '%s' "$c" | grep -c 'merge-daily-incremental')
echo "document $D: DefaultVersion=$dv LatestVersion=$lv; at \$LATEST: playwright refs=$pw BD_PASSWORD refs=$pwd_ merge refs=$mg"
if [ -n "$dv" ] && [ "$dv" = "$lv" ] && [ "$pw" = 0 ] && [ "$pwd_" = 0 ] && [ "$mg" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
