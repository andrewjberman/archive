#!/usr/bin/env bash
# org/missions/D0/NFRA/NFRA_DEVPLN/deliverables/2.0.0_SA_COO~DV/checks/check_devpln_settlement.sh -- NFRA_DEVPLN cell DP-s-1 independent denominator (issuer-authored; the worker only runs it).
# Reads the settlement list the tool wrote and compares its two headline counts with the portal repo, read directly.
# Usage: check_devpln_settlement.sh <list-file> <portal-repo-path>
# Last line: SETTLEMENT-COUNTS-MATCH dev_ahead=<n> prod_ahead=<m>   |   SETTLEMENT-COUNTS-MISMATCH list=<..> repo=<..>
set -u
LIST="${1:-}"; REPO="${2:-portal}"
[ -f "$LIST" ] || { echo "SETTLEMENT-COUNTS-MISMATCH list=absent repo=-"; exit 1; }
d=$(git -C "$REPO" rev-list --count origin/PROD..origin/DEV 2>&1) || { echo "SETTLEMENT-COUNTS-MISMATCH list=- repo=unreadable:$d"; exit 1; }
p=$(git -C "$REPO" rev-list --count origin/DEV..origin/PROD 2>&1) || { echo "SETTLEMENT-COUNTS-MISMATCH list=- repo=unreadable:$p"; exit 1; }
ld=$(grep -o -E 'dev_ahead=[0-9]+' "$LIST" | head -1 | cut -d= -f2)
lp=$(grep -o -E 'prod_ahead=[0-9]+' "$LIST" | head -1 | cut -d= -f2)
if [ "$ld" = "$d" ] && [ "$lp" = "$p" ]; then
  echo "SETTLEMENT-COUNTS-MATCH dev_ahead=$d prod_ahead=$p"; exit 0
fi
echo "SETTLEMENT-COUNTS-MISMATCH list=dev:${ld:-none},prod:${lp:-none} repo=dev:$d,prod:$p"; exit 1
