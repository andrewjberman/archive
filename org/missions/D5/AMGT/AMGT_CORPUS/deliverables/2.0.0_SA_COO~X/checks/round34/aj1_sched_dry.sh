#!/usr/bin/env bash
# AMGT_CORPUS round 34, CRPS-aj-1 AC3 -- the scheduled entry the amgt-induction-daily task runs carries the refresh step AFTER
# the admit step and BEFORE its closing line. The issuer's file.
# NOTE (row AMGT_CORPUS-Z-S84): in --mode dry-run the admit step reads rc 1 at the base, because induction_run's dry run
# poisons boto3 and admit's S3 read trips it. This check grades the step's PLACEMENT and its announce line, not its rc.
#   PASS: lines `induction_scheduled step model_block_admit rc <a>`, then `induction_scheduled step model_block_refresh rc <r>`,
#         then `induction_scheduled mode dry-run as_of <date> rc <n> log <path>`, in that order.
#   -> one line: `AJ1-SCHED-DRY PASS|FAIL <reason>`
set -u
TOP=$(git rev-parse --show-toplevel) || { echo "AJ1-SCHED-DRY FAIL no-repo"; exit 1; }
OUT=$(cd "$TOP" && timeout 110 python -m lib.research.corpus.induction_scheduled --mode dry-run 2>&1)
A=$(printf '%s\n' "$OUT" | grep -n -E '^induction_scheduled step model_block_admit rc [0-9]+$' | head -1 | cut -d: -f1)
R=$(printf '%s\n' "$OUT" | grep -n -E '^induction_scheduled step model_block_refresh rc [0-9]+$' | head -1 | cut -d: -f1)
C=$(printf '%s\n' "$OUT" | grep -n -E '^induction_scheduled mode dry-run as_of [0-9-]+ rc [0-9]+ log ' | tail -1 | cut -d: -f1)
if [ -z "$A" ] || [ -z "$R" ] || [ -z "$C" ]; then echo "AJ1-SCHED-DRY FAIL admit_line=${A:-none} refresh_line=${R:-none} closing_line=${C:-none}"; exit 1; fi
if [ "$A" -lt "$R" ] && [ "$R" -lt "$C" ]; then
  echo "AJ1-SCHED-DRY PASS order admit:$A refresh:$R closing:$C [$(printf '%s\n' "$OUT" | grep -E '^induction_scheduled step model_block_refresh')]"
else
  echo "AJ1-SCHED-DRY FAIL order admit:$A refresh:$R closing:$C"; exit 1
fi
