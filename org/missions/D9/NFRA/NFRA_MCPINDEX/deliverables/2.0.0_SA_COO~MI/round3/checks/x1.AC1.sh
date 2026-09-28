#!/usr/bin/env bash
# MX-x-1 AC1 (row Z-S22): record-terraform-deploy.sh carries no device-specific user-home path (it DERIVES its tools).
. "$(dirname "$0")/_root.sh"
F=infra/aws/lambda/ci/record-terraform-deploy.sh
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
n=$(grep -cE '(/c/Users/|[Cc]:[/\\]Users[/\\]|/home/[A-Za-z]|/Users/[A-Za-z])' "$F")
echo "user-home literal paths in $F: $n"
if [ "$n" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
