#!/usr/bin/env bash
# MS-ir-2 AC2 (LIVE, the new role and grant): simulate, one call per resource -- the internal reader role
# gateway-global-internal-reader-role reads opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json (a firm key)
# ALLOWED and opal-data-portal-v2/json/benchmarks/etf_returns.json (a global key) ALLOWED; the gateway role
# opal-gateway-role may sts:AssumeRole on it (ALLOWED).
. "$(dirname "$0")/_root.sh"
nm=$(opal_name gateway global internal-reader role); A=$(acct); R="arn:aws:iam::${A}:role/${nm}"; G="arn:aws:iam::${A}:role/${GW_ROLE}"
f=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json")
g=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/json/benchmarks/etf_returns.json")
a=$(sim "$G" sts:AssumeRole "$R")
echo "role $nm: firm-key=${f:-NONE} global-key=${g:-NONE}; gateway AssumeRole=${a:-NONE}"
if [ "$f" = allowed ] && [ "$g" = allowed ] && [ "$a" = allowed ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
