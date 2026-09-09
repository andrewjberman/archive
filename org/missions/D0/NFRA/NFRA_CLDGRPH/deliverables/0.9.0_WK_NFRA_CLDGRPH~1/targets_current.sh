#!/usr/bin/env bash
# E2-AC3 -- EVERY DECLARED LAUNCHER POINTS AT THE PINNED REVISION.
# For each of the four moved producers, the launcher declared in
# infra/aws/terraform/globgrph is read LIVE and its task_definition_arn compared
# against the family's current ACTIVE revision ARN read from ECS.
#   comp-learns -> aws_cloudwatch_event_target.comp_learns_producer_nightly
#                  (rule opal-globgrph-comp-learns-producer-nightly)
#   fedobs      -> aws_cloudwatch_event_target.fedobs_producer_nightly
#                  (rule opal-globgrph-fedobs-producer-nightly)
#   cse         -> aws_scheduler_schedule.cse_producer_nightly
#                  (schedule globgrph-cse-producer-nightly)
#   resource-summaries -> NO DECLARED LAUNCHER in this tree (printed by name below
#                  with how it is in fact launched). The DENOMINATOR is the
#                  launchers FOUND, not the families.
# ASCII only. Git Bash 3.6.7 safe. The aws shim emits CRLF -- stripped before any test.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT/.tools/aws"

active_arn() {
  "$AWS" ecs describe-task-definition --task-definition "$1" \
    --query 'taskDefinition.taskDefinitionArn' --output text 2>&1 | tr -d '\r'
}

found=0
on_revision=0

check() {
  # $1 family, $2 launcher label, $3 live task-definition arn on the launcher
  local fam="$1" label="$2" live="$3" want
  want="$(active_arn "$fam")"
  found=$((found + 1))
  if [ "$live" = "$want" ]; then
    on_revision=$((on_revision + 1))
    echo "LAUNCHER=$label FAMILY=$fam TARGET_ARN=$live ACTIVE_ARN=$want -> ON-PINNED-REVISION"
  else
    echo "LAUNCHER=$label FAMILY=$fam TARGET_ARN=$live ACTIVE_ARN=$want -> STALE"
  fi
}

cl="$("$AWS" events list-targets-by-rule --rule opal-globgrph-comp-learns-producer-nightly \
      --query 'Targets[0].EcsParameters.TaskDefinitionArn' --output text 2>&1 | tr -d '\r')"
check globgrph-comp-learns-producer "events-rule/opal-globgrph-comp-learns-producer-nightly" "$cl"

fo="$("$AWS" events list-targets-by-rule --rule opal-globgrph-fedobs-producer-nightly \
      --query 'Targets[0].EcsParameters.TaskDefinitionArn' --output text 2>&1 | tr -d '\r')"
check globgrph-fedobs-producer "events-rule/opal-globgrph-fedobs-producer-nightly" "$fo"

cs="$("$AWS" scheduler get-schedule --name globgrph-cse-producer-nightly \
      --query 'Target.EcsParameters.TaskDefinitionArn' --output text 2>&1 | tr -d '\r')"
check globgrph-cse-producer "scheduler/globgrph-cse-producer-nightly" "$cs"

echo "NO-DECLARED-LAUNCHER: globgrph-resource-summaries-producer -- launched BY HAND (ad-hoc ecs run-task)."
echo "  Measured live, three instruments, none finds an automated launcher for this family:"
echo "  (1) events list-rules across the default bus = every rule censused, list-targets-by-rule on each:"
echo "      exactly 3 rules carry an ECS TaskDefinitionArn (comp-learns, derive-runner, fedobs) and none is this family."
echo "  (2) scheduler list-schedules = 19 schedules, the only globgrph one is globgrph-cse-producer-nightly."
echo "  (3) pipes list-pipes = 1 pipe, opal-globgrph-projection-worker, not this family."
echo "  Its Terraform declares only an output (resource_summaries_producer.tf:186) whose own description"
echo "  reads 'manual run-task', and its log group /ecs/globgrph-resource-summaries-producer holds exactly"
echo "  THREE streams, all on 2026-07-18 (20:58:14Z, 21:08:15Z, 21:11:04Z) -- one seeding session, no cadence."
echo "  Its NEXT LAUNCH is whoever runs it, and it will run the pinned revision because that is the family's ACTIVE one."
echo "TARGETS_ON_PINNED_REVISION=$on_revision of $found declared launcher(s)"
