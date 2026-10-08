#!/usr/bin/env bash
# OG-rl-14 PHASE B steps 9-10 driver (the issuer's GO): BEFORE page reads -> cache size/files BEFORE -> deploy start time -> the deploy -> end time -> cache size/files AFTER -> R45 count -> AFTER page reads.
# Reads only (python os.walk/os.stat, .tools/aws S3 HEAD/GET) apart from the one deploy command. It judges nothing; the worker reads the outputs afterwards.
# usage: bash r28c_phaseB_drive.sh        (from anywhere; the deploy runs from /c/tmp/og-rel24)
set -u
W="/c/tmp/wk-oplgtw-r26-28/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
REL=/c/tmp/og-rel24
T="$W/r28c_phaseB_times.txt"
: > "$T"
export PYTHONDONTWRITEBYTECODE=1
echo "=== BEFORE page reads (R42) ===" >> "$T"
python "$W/r28_pagetime.py" before "$W/r28_pagetime_before.out" > "$W/r28c_pagetime_before.stdout" 2>&1; echo "pagetime_before rc=$?" >> "$T"
python "$W/r28c_bun_cache_size.py" before > "$W/r28c_cache_before.out" 2>&1; echo "cache_size_before rc=$?" >> "$T"
START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "deploy_started_utc=$START" >> "$T"
cd "$REL" || exit 9
unset OPAL_AGENT_SERIAL
DEPLOY_BASE_REF=510c8cfed2c852946e3e57fb4dd1c0467e2f3a52 HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~28 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh > "$W/r28c_phaseB_deploy.out" 2>&1
RC=$?
END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "deploy_rc=$RC" >> "$T"
echo "deploy_returned_utc=$END" >> "$T"
python "$W/r28c_bun_cache_size.py" after > "$W/r28c_cache_after.out" 2>&1; echo "cache_size_after rc=$?" >> "$T"
python "$W/r28_bun_cache_count.py" "$START" "$W/r28c_cache_count_raw.json" > "$W/r28c_cache_count.out" 2>&1; echo "cache_count rc=$?" >> "$T"
python "$W/r28_pagetime.py" after "$W/r28_pagetime_after.out" > "$W/r28c_pagetime_after.stdout" 2>&1; echo "pagetime_after rc=$?" >> "$T"
echo "DRIVE_DONE" >> "$T"
