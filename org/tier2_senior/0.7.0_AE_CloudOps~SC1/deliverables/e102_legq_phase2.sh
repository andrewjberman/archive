#!/usr/bin/env bash
# Leg Q' phase 2 for run N: BEFORE snapshot -> mix daily summary VersionId read IMMEDIATELY before the run (CTO C1) + body saved -> the single.
# Usage: e102_legq_phase2.sh <N>      (the stop command of phase 1 has already run)
set -uo pipefail
N=${1:?run number}
ROOT=/c/dev/ajb_workspace
D=$ROOT/org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables
EV=/c/Users/Test/legq_evidence_20261015          # off-repo: key names carry client/account ids
AWS=$ROOT/.tools/aws
INST=i-01003b035d2988dfb
mkdir -p "$EV"; cd "$ROOT"
echo "== instance $(date -u +%H:%M:%SZ): $($AWS ec2 describe-instances --instance-ids $INST --query 'Reservations[0].Instances[0].State.Name' --output text)"
echo "== BEFORE snapshot (run $N)"
python -I "$D/e97_legq_snapshot.py" snap "$EV/E102_RUN${N}_BEFORE.json" || exit 30
echo "== (a) mix daily summary VersionId read immediately before run $N"
line=$(python -I "$D/e102_legp.py" version); echo "$line"
VID=$(printf '%s' "$line" | sed -n 's/.*VersionId=\([^ ]*\) .*/\1/p')
[ -n "$VID" ] || { echo "STOP: no VersionId parsed"; exit 31; }
$AWS s3api get-object --bucket opal-data-49financial --key advi/49financial/platinum/views/mix_daily_summary.json --version-id "$VID" "$D/E102_RUN${N}_PRE_mix_daily_summary_BODY.json" --query '{E:ETag,V:VersionId,S:ContentLength}' --output json
printf '%s\n' "$line" > "$D/E102_RUN${N}_PRE_VERSIONID.txt"
echo "== instance still up? $(date -u +%H:%M:%SZ): $($AWS ec2 describe-instances --instance-ids $INST --query 'Reservations[0].Instances[0].State.Name' --output text)"
echo "== SECOND SSM command: the single"
python -I "$D/e102_ssm.py" send $INST "e102 leg Q' run $N: BD_PLATINUM_MODE=canonical --single C_06 (SC1)" "$D/e102_cmd_single.sh" "$D/e102_legq_run${N}_single.json"
echo "== exit $?  $(date -u +%H:%M:%SZ)"
