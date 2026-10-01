#!/usr/bin/env bash
# MS-dn-1 AC2 (LIVE, the Deny): simulate on the gateway role opal-gateway-role, one call per resource --
# opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json and .../platinum/mdpf/cottonwood/aum-metrics.json read
# explicitDeny (a firm key), while opal-data-portal-v2/json/benchmarks/etf_returns.json (a global key) stays allowed.
. "$(dirname "$0")/_root.sh"
A=$(acct); G="arn:aws:iam::${A}:role/${GW_ROLE}"
i=$(sim "$G" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json")
c=$(sim "$G" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json")
g=$(sim "$G" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/json/benchmarks/etf_returns.json")
echo "gateway role $GW_ROLE: inflection firm key=${i:-NONE} cottonwood firm key=${c:-NONE} global key=${g:-NONE}"
if [ "$i" = explicitDeny ] && [ "$c" = explicitDeny ] && [ "$g" = allowed ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
