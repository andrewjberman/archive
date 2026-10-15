#!/usr/bin/env bash
# TO-SC-e102b legs P and D in ONE shell (COO half condition 2/3): window read -> pre census -> leg P -> deploy -> post census.
# Any failed step aborts before the next; the deploy is never reached on a failed window read or leg P.
set -euo pipefail
ROOT=/c/dev/ajb_workspace
D=$ROOT/org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables
AWS=$ROOT/.tools/aws
RUNNER=i-01003b035d2988dfb
cd "$ROOT"
echo "== window read $(date -u +%Y-%m-%dT%H:%M:%SZ)"
st=$($AWS ec2 describe-instances --instance-ids $RUNNER --query 'Reservations[0].Instances[0].State.Name' --output text)
n=$($AWS ec2 describe-instances --filters "Name=tag:Name,Values=*gold-layer-runner*" "Name=instance-state-name,Values=pending,running,stopping" --query 'length(Reservations[].Instances[])' --output text)
echo "runner $RUNNER state=$st; gold-layer-runner instances pending/running/stopping=$n"
[ "$st" = "stopped" ] && [ "$n" = "0" ] || { echo "STOP: runner not stopped"; exit 11; }
if $AWS s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "STOP: gold/trigger-pending.json waits"; exit 12; else echo "gold/trigger-pending.json: absent (404 read)"; fi
served=$($AWS s3api head-object --bucket opal-data-bd --key code/gold/C_06.client_mix_timeseries.py --query '[ETag,VersionId]' --output text)
echo "served C_06: $served"
case "$served" in *f847d8d105025ffbee94b1aa5092faf6*jGO15I3AZTATLbGxE3_36dKm86wuggDK*) : ;; *) echo "STOP: served C_06 is not the base"; exit 13;; esac
echo "== pre census"; python -I "$D/e102_census.py" snap "$D/E102_CODEGOLD_PRE_20261015.json"
echo "== leg P"; python -I "$D/e102_legp.py" legp "$D/E102_LEGP_20261014.json" "$D/E102_LEGP_mix_daily_summary_BODY.json"
echo "== window re-read before the ship $(date -u +%Y-%m-%dT%H:%M:%SZ)"
st2=$($AWS ec2 describe-instances --instance-ids $RUNNER --query 'Reservations[0].Instances[0].[State.Name,LaunchTime]' --output text); echo "runner: $st2"
case "$st2" in stopped*) : ;; *) echo "STOP: runner not stopped at ship"; exit 14;; esac
if $AWS s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "STOP: trigger-pending waits"; exit 15; fi
echo "== leg D: safe-deploy"
bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py 2>&1 | tee "$D/e102_safe_deploy.out"
echo "== post census"; python -I "$D/e102_census.py" snap "$D/E102_CODEGOLD_POST_20261015.json"
python -I "$D/e102_census.py" cmp "$D/E102_CODEGOLD_PRE_20261015.json" "$D/E102_CODEGOLD_POST_20261015.json"
echo "== served now"; $AWS s3api head-object --bucket opal-data-bd --key code/gold/C_06.client_mix_timeseries.py --query '{E:ETag,V:VersionId,L:LastModified,S:ContentLength}' --output json
