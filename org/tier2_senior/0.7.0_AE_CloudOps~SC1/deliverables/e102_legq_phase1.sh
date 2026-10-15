#!/usr/bin/env bash
# Leg Q' phase 1 for run N: window read -> accounts-dimension version -> start the runner -> SSM online -> FIRST command = systemctl stop.
# Usage: e102_legq_phase1.sh <N>
set -uo pipefail
N=${1:?run number}
ROOT=/c/dev/ajb_workspace
D=$ROOT/org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables
AWS=$ROOT/.tools/aws
INST=i-01003b035d2988dfb
cd "$ROOT"
echo "== window read $(date -u +%Y-%m-%dT%H:%M:%SZ)"
st=$($AWS ec2 describe-instances --instance-ids $INST --query 'Reservations[0].Instances[0].State.Name' --output text)
n=$($AWS ec2 describe-instances --filters "Name=tag:Name,Values=*gold-layer-runner*" "Name=instance-state-name,Values=pending,running,stopping" --query 'length(Reservations[].Instances[])' --output text)
echo "runner state=$st; pending/running/stopping=$n"
[ "$st" = "stopped" ] && [ "$n" = "0" ] || { echo "STOP: runner not stopped (someone else launched it; wait, do not start)"; exit 11; }
if $AWS s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "STOP: trigger-pending waits"; exit 12; else echo "gold/trigger-pending.json: absent (404 read)"; fi
echo "served C_06: $($AWS s3api head-object --bucket opal-data-bd --key code/gold/C_06.client_mix_timeseries.py --query '[ETag,VersionId]' --output text)"
echo "accounts_dimension_latest.parquet (pre-start): $($AWS s3api head-object --bucket opal-data-bd --key gold/dimensions/accounts_dimension_latest.parquet --query '[ETag,VersionId,LastModified]' --output text)"
echo "== start-instances $(date -u +%H:%M:%SZ)"
$AWS ec2 start-instances --instance-ids $INST --query 'StartingInstances[0].[InstanceId,CurrentState.Name]' --output text
python -I "$D/e102_ssm.py" online $INST 420 || { echo "STOP: agent never came online"; exit 13; }
echo "== FIRST SSM command: stop gold-layer-runner"
python -I "$D/e102_ssm.py" send $INST "e102 leg Q' run $N: stop boot wrapper (SC1)" "$D/e102_cmd_stop.sh" "$D/e102_legq_run${N}_stop.json"
echo "== exit $?"
