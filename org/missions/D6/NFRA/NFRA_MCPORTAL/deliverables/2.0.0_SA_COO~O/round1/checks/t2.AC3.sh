#!/usr/bin/env bash
# MP-t-2 AC3 (the IAM shape, static): the writer's Terraform is fmt-clean, names the function by the builder's output
# verbatim, grants lambda:InvokeFunction (the gateway role's ONE new permission), and grants the gateway role no
# sts:AssumeRole: every sts:AssumeRole in the file sits in a trust policy naming lambda.amazonaws.com.
. "$(dirname "$0")/_root.sh"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
e=$(mp_writer_entry); tf=$(printf '%s\n' "$e" | sed -n 4p)
[ -n "$tf" ] && [ -f "$tf" ] || { echo "tf_file absent"; echo "RESULT: FAIL"; exit 1; }
timeout 60 terraform fmt -check "$tf" >/dev/null 2>&1; fmt=$?
named=$(grep -cF "\"$nm\"" "$tf"); inv=$(grep -c 'lambda:InvokeFunction' "$tf")
r=$(python - "$tf" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
# each AssumeRole occurrence must have lambda.amazonaws.com within the same 400-char window (a Lambda trust policy)
bad = sum(1 for m in re.finditer(r"sts:AssumeRole", s) if "lambda.amazonaws.com" not in s[max(0, m.start()-400):m.end()+400])
print(bad)
EOF
)
echo "fmt rc=$fmt; builder name literal occurrences=$named; lambda:InvokeFunction=$inv; sts:AssumeRole outside a Lambda trust policy=$r"
if [ "$fmt" = 0 ] && [ "$named" -ge 1 ] && [ "$inv" -ge 1 ] && [ "$r" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
