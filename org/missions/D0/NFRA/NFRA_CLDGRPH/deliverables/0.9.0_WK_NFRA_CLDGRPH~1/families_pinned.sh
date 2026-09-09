#!/usr/bin/env bash
# E2-AC1 -- SEVEN OF SEVEN ACTIVE globgrph FAMILIES REFERENCE THE IMAGE BY DIGEST.
# Reads the LIVE applied plane: ecs describe-task-definition on each family's latest
# ACTIVE revision, and tests containerDefinitions[0].image for '@sha256:'.
# The denominator is the SEVEN named globgrph families that pull the shared
# opal-globgrph-derive-runner image (R13's population). globgrph-nessie and
# globgrph-trino are NOT in this population -- they run OTHER images.
# ASCII only. Git Bash 3.6.7 safe. The aws shim emits CRLF -- stripped before any test.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT/.tools/aws"

FAMILIES="globgrph-comp-learns-producer globgrph-cse-producer globgrph-fedobs-producer globgrph-resource-summaries-producer globgrph-derive-runner globgrph-projection-worker globgrph-serving"

total=0
pinned=0
for f in $FAMILIES; do
  total=$((total + 1))
  row="$("$AWS" ecs describe-task-definition --task-definition "$f" \
        --query 'taskDefinition.[revision,status,containerDefinitions[0].image]' \
        --output text 2>&1 | tr -d '\r')"
  rev="$(printf '%s\n' "$row" | awk '{print $1}')"
  st="$(printf '%s\n' "$row" | awk '{print $2}')"
  img="$(printf '%s\n' "$row" | awk '{print $3}')"
  case "$img" in
    *@sha256:*) verdict="BY-DIGEST"; pinned=$((pinned + 1)) ;;
    *)          verdict="BY-TAG-OR-UNREAD" ;;
  esac
  echo "FAMILY=$f REVISION=$rev STATUS=$st IMAGE=$img -> $verdict"
done

echo "NOT-IN-THIS-POPULATION: globgrph-nessie, globgrph-trino (other images, no opal-globgrph-derive-runner reference)"
echo "PINNED_BY_DIGEST=$pinned of $total"
