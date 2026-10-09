#!/usr/bin/env bash
# OPLGTW OG-ap-1 AC3 (the converter leg, CTO half on OG-tm-1 @4149c01c23): the live opal-assets-silver-schwab Lambda runs
# the artifact rebuilt from the repinned source (CodeSha256 AzrzJS+91y57ylRdqGccFPGqWaqAGLFn/jhItkAQCzE=), and the
# opal-data-assets bucket notification configuration reads back 12 rules in all (11 before + silver-schwab-08403355),
# with exactly one rule on the prefix schwab/08403355/bronze/.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
WANT="AzrzJS+91y57ylRdqGccFPGqWaqAGLFn/jhItkAQCzE="
sha=$(.tools/aws lambda get-function-configuration --function-name opal-assets-silver-schwab --region us-east-1 --query CodeSha256 --output text | tr -d '\r'); rc1=$?
counts=$(.tools/aws s3api get-bucket-notification-configuration --bucket opal-data-assets --region us-east-1 --output json | tr -d '\r' | python -c "
import json,sys
d=json.load(sys.stdin)
allr=[r for k in ('LambdaFunctionConfigurations','QueueConfigurations','TopicConfigurations') for r in d.get(k,[])]
def pre(r):
    for f in (r.get('Filter',{}).get('Key',{}).get('FilterRules',[])):
        if f.get('Name','').lower()=='prefix': return f.get('Value')
print(len(allr), sum(1 for r in allr if pre(r)=='schwab/08403355/bronze/'))"); rc2=$?
total=${counts% *}; new=${counts#* }
echo "converter CodeSha256=$sha (aws rc=$rc1), want $WANT"
echo "bucket notification rules: $total (want 12); on schwab/08403355/bronze/: $new (want 1) (rc=$rc2)"
[ "$rc1" = 0 ] && [ "$sha" = "$WANT" ] && [ "$rc2" = 0 ] && [ "$total" = 12 ] && [ "$new" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
