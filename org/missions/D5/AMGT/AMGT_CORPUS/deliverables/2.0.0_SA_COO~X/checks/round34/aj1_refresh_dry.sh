#!/usr/bin/env bash
# AMGT_CORPUS round 34, CRPS-aj-1 AC2 -- the refresh stage's dry run against its REAL neighbour, the served model-block store
# (S3 list/get only; a dry run opens no Bloomberg session). The issuer's file.
#   PASS: rc 0; first line `refresh population registered <N> with_block <K>` with K >= 94 and K <= N; a line
#         `refresh fields header <h> hist <t> forecast <f>` with h+t+f >= 118 (66 base + 49 V3 + 3 name/earnings);
#         last line ends `pulled 0 bloomberg_calls 0`.
#   -> one line: `AJ1-REFRESH-DRY PASS|FAIL <reason>`
set -u
TOP=$(git rev-parse --show-toplevel) || { echo "AJ1-REFRESH-DRY FAIL no-repo"; exit 1; }
OUT=$(cd "$TOP" && PYTHONPATH="$TOP" timeout 110 python integrations/bloomberg/research/model_block_pull.py refresh --dry-run 2>&1)
RC=$?
FIRST=$(printf '%s\n' "$OUT" | grep -E '^refresh population ' | head -1)
FIELDS=$(printf '%s\n' "$OUT" | grep -E '^refresh fields ' | head -1)
LAST=$(printf '%s\n' "$OUT" | tail -1)
N=$(printf '%s' "$FIRST" | sed -n 's/^refresh population registered \([0-9]*\) with_block \([0-9]*\).*/\1/p')
K=$(printf '%s' "$FIRST" | sed -n 's/^refresh population registered \([0-9]*\) with_block \([0-9]*\).*/\2/p')
SUM=$(printf '%s' "$FIELDS" | sed -n 's/^refresh fields header \([0-9]*\) hist \([0-9]*\) forecast \([0-9]*\).*/\1 \2 \3/p' | awk '{print $1+$2+$3}')
if [ "$RC" -ne 0 ]; then echo "AJ1-REFRESH-DRY FAIL rc=$RC last=[$LAST]"; exit 1; fi
if [ -z "$N" ] || [ -z "$K" ]; then echo "AJ1-REFRESH-DRY FAIL no-population-line first=[$FIRST]"; exit 1; fi
if [ "$K" -lt 94 ] || [ "$K" -gt "$N" ]; then echo "AJ1-REFRESH-DRY FAIL registered=$N with_block=$K"; exit 1; fi
if [ -z "$SUM" ] || [ "$SUM" -lt 118 ]; then echo "AJ1-REFRESH-DRY FAIL fields=[$FIELDS]"; exit 1; fi
case "$LAST" in *"pulled 0 bloomberg_calls 0") ;; *) echo "AJ1-REFRESH-DRY FAIL last=[$LAST]"; exit 1;; esac
echo "AJ1-REFRESH-DRY PASS registered=$N with_block=$K fields=$SUM last=[$LAST]"
