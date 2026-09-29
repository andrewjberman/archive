#!/usr/bin/env bash
# MX-s-14 AC1 (the SSM document that RUNS, not the repo copy): opal-bd-transaction-download is read at $LATEST -- the
# version its trigger executes (row Z-S48) -- and DefaultVersion equals LatestVersion; that content runs the REST
# transaction pull (pull_bd_transaction_rest), and neither the Playwright download (download-daily-transaction.ts) nor
# any portal credential (BD_PASSWORD).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; D=opal-bd-transaction-download
v=$(timeout 60 "$AWS" ssm describe-document --name $D --query 'Document.[DefaultVersion,LatestVersion]' --output text 2>&1 | tr -d '\r')
dv=$(printf '%s' "$v" | awk '{print $1}'); lv=$(printf '%s' "$v" | awk '{print $2}')
c=$(timeout 60 "$AWS" ssm get-document --name $D --document-version '$LATEST' --query Content --output text 2>&1 | tr -d '\r')
[ -n "$c" ] || { echo "get-document returned nothing -- RESULT: FAIL"; exit 1; }
rest=$(printf '%s' "$c" | grep -c 'pull_bd_transaction_rest')
pw=$(printf '%s' "$c" | grep -c 'download-daily-transaction.ts')
pwd_=$(printf '%s' "$c" | grep -c 'BD_PASSWORD')
echo "document $D: DefaultVersion=$dv LatestVersion=$lv; at \$LATEST: rest-pull refs=$rest playwright refs=$pw BD_PASSWORD refs=$pwd_"
if [ -n "$dv" ] && [ "$dv" = "$lv" ] && [ "$rest" -ge 1 ] && [ "$pw" = 0 ] && [ "$pwd_" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
