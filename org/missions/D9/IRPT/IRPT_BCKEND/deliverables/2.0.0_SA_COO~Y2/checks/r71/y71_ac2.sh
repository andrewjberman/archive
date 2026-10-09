#!/usr/bin/env bash
# IRPT_BCKEND round 71 Y71-1-AC2: BUILD_ONLY the irpt-ycharts-generate zip, then grade its symbol closure (row IRPT_BCKEND-D2-S16).
# Prints the build's import-closure line and the closure verdict; the last line is "symbol_closure PASS|FAIL".
set -u
root=$(git rev-parse --show-toplevel)
cd "$root" || exit 2
BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate 2>&1 | grep -E 'import-closure|BUILD_ONLY:'
zip=/tmp/lambda-artifact-irpt-ycharts-generate.zip
if command -v cygpath >/dev/null 2>&1; then zip=$(cygpath -w "$zip"); fi
python "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r71/symbol_closure.py" "$zip"
