#!/usr/bin/env bash
# MP-f-1 AC2 (R-8's bound): the running gateway's own default is NOT moved -- app/config.py at HEAD still reads
# AUDIT_PATH from the environment with the ./audit.jsonl default (the host's env sets it; the fix lives in the tests).
# Read at HEAD with git show, never the working-tree path.
. "$(dirname "$0")/_root.sh"
F="infra/aws/ec2/opal-gateway/app/config.py"
n=$(git show "HEAD:$F" 2>&1 | grep -cF 'AUDIT_PATH: str = os.environ.get("AUDIT_PATH", "./audit.jsonl")')
lines=$(git show "HEAD:$F" 2>&1 | wc -l)
echo "$F at HEAD: $lines lines; AUDIT_PATH default line present=$n"
if [ "$n" = 1 ] && [ "$lines" -gt 100 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
