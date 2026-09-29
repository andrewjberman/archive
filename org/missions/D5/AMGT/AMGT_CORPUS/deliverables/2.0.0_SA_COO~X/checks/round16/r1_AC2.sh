#!/usr/bin/env bash
# AMGT_CORPUS round 16 -- check as a file (spine v3.19 L6): r1_AC2. Run from the repo root under the worker's timeout.
# The registration script's PLAN (registers nothing): the task name is the builder's, the action runs the pinned
# commit's detached checkout and never the shared tree.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
top=$(pwd -W 2>/dev/null || pwd)
want=$(python -c "from lib import opal_naming as n; print(n.name('amgt', None, 'induction', 'daily'))")
sha=$(git rev-parse HEAD)
f=lib/research/corpus/schedule_induction.ps1
[ -f "$f" ] || { echo "r1 plan MISSING $f"; exit 0; }
out=$(powershell -NoProfile -ExecutionPolicy Bypass -File "$f" -Plan -Commit "$sha" 2>&1 | tr -d '\r')
name=$(echo "$out" | sed -n 's/^PLAN task \([^ ]*\).*/\1/p' | head -1)
wd=$(echo "$out" | sed -n 's/^PLAN workdir \(.*\)$/\1/p' | head -1)
cm=$(echo "$out" | sed -n 's/^PLAN commit \([0-9a-f]*\).*/\1/p' | head -1)
shared=no; case "$(echo "$wd" | tr 'A-Z\' 'a-z/')" in "$(echo "$top" | tr 'A-Z\' 'a-z/')"|"") shared=yes;; esac
echo "r1 plan task_is_builder_name $([ "$name" = "$want" ] && echo True || echo False) commit_pinned $([ "$cm" = "$sha" ] && echo True || echo False) workdir_is_shared_tree $([ "$shared" = yes ] && echo True || echo False) registered_now $(echo "$out" | grep -c '^REGISTERED')"
