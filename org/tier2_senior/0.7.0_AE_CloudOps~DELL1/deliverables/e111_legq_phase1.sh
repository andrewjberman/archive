#!/usr/bin/env bash
# Leg Q phase 1 (TO-SC-e111b): window read -> start the runner -> SSM online -> FIRST command = systemctl stop.
set -uo pipefail
ROOT=/c/dev/ajb_workspace; D=$ROOT/org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables; AWS=$ROOT/.tools/aws; INST=i-01003b035d2988dfb
cd "$ROOT"
echo "== window read $(date -u +%Y-%m-%dT%H:%M:%SZ)"
st=$($AWS ec2 describe-instances --instance-ids $INST --query 'Reservations[0].Instances[0].State.Name' --output text)
n=$($AWS ec2 describe-instances --filters "Name=tag:Name,Values=*gold-layer-runner*" "Name=instance-state-name,Values=pending,running,stopping" --query 'length(Reservations[].Instances[])' --output text)
echo "runner state=$st; pending/running/stopping=$n"
[ "$st" = "stopped" ] && [ "$n" = "0" ] || { echo "STOP: runner not stopped"; exit 11; }
if $AWS s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "STOP: trigger-pending waits"; exit 12; else echo "gold/trigger-pending.json: absent (404 read)"; fi
echo "served E_18: $($AWS s3api head-object --bucket opal-data-bd --key code/gold/E_18.detect_new_securities.py --query '[ETag,VersionId]' --output text)"
echo "accounts_dimension_latest.parquet (pre-start): $($AWS s3api head-object --bucket opal-data-bd --key gold/dimensions/accounts_dimension_latest.parquet --query '[ETag,VersionId,LastModified]' --output text)"
echo "== start-instances $(date -u +%H:%M:%SZ)"
$AWS ec2 start-instances --instance-ids $INST --query 'StartingInstances[0].[InstanceId,CurrentState.Name]' --output text
python -I "$D/e111_ssm.py" online $INST 420 || { echo "STOP: agent never came online"; exit 13; }
echo "== FIRST SSM command: stop gold-layer-runner"
python -I "$D/e111_ssm.py" send $INST "e111b leg Q: stop boot wrapper (DELL1)" "$D/e111_cmd_stop.sh" "$D/e111_legq_stop.json"
echo "== exit $?"
