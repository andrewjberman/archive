#!/usr/bin/env bash
# AMGT_RESAPP round-89 PREP -- AMGT-nn-7's close arm: the dossier METHOD in the DEPLOYED package, and the no-regression pair.
#   bash r89_deployed_close.sh [--want amgt-corpus-dossier/11]       (run from the repo root; PYTHONPATH is set here)
# 1. r87_dossier.py --want <METHOD>: the deployed package's dossier.py METHOD_VERSION (also prints CodeSha256, LastModified);
# 2. r87_withheld.py --crit AC1: no FAILED description carries a sentence, every drafted name answers (mm-4 AC2);
# 3. r84_listing.py --crit AC1 --where deployed: typed ASML still resolves, Micro still lists, the rest byte-equal (mm-4 AC3).
# Verdict: R89 DEPLOYED CLOSE: YES|NO (exit 0|1). At the base (live /10, 2026-10-11): NO on step 1 only.
set -u
WANT="amgt-corpus-dossier/11"
if [ "${1:-}" = "--want" ]; then WANT="${2:-$WANT}"; fi
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREP="$(cd "$HERE/.." && pwd)"
DELIV="$(cd "$PREP/.." && pwd)"
ROOT="$(git rev-parse --show-toplevel)"
export PYTHONPATH="$ROOT"
cd "$ROOT" || exit 2
python "$DELIV/round87_prep/checks/r87_dossier.py" --want "$WANT" | tail -6; D=${PIPESTATUS[0]}
python "$DELIV/round87_prep/checks/r87_withheld.py" --crit AC1 | tail -4; W=${PIPESTATUS[0]}
python "$DELIV/round84_prep/checks/r84_listing.py" --crit AC1 --where deployed | tail -5; L=${PIPESTATUS[0]}
echo "   dossier rc=$D | withheld rc=$W | listing rc=$L"
if [ "$D" = "0" ] && [ "$W" = "0" ] && [ "$L" = "0" ]; then echo "R89 DEPLOYED CLOSE: YES"; exit 0; fi
echo "R89 DEPLOYED CLOSE: NO"; exit 1
