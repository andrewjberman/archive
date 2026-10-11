#!/usr/bin/env bash
# AMGT_RESAPP round-89 PREP -- AMGT-nn-7's behaviour arm: the DEPLOYED function serves nn-2 and nn-3.
#   bash r89_peers_deployed.sh        (run from the repo root; PYTHONPATH is set here)
# Runs r89_peer_identity.py and r89_subject_cap.py with --where deployed (a Lambda invoke of opal-amgt-scoped-api) and prints
# both verdict lines. Verdict: R89 PEERS DEPLOYED: YES|NO (exit 0|1). At the base (live KlosR/ap8O, 2026-10-11): NO.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git rev-parse --show-toplevel)"
export PYTHONPATH="$ROOT"
cd "$ROOT" || exit 2
RC=0
python "$HERE/r89_peer_identity.py" --where deployed | tail -8; R1=${PIPESTATUS[0]}
python "$HERE/r89_subject_cap.py" --where deployed | tail -6; R2=${PIPESTATUS[0]}
echo "   peer identity rc=$R1 | subject cap rc=$R2"
if [ "$R1" = "0" ] && [ "$R2" = "0" ]; then echo "R89 PEERS DEPLOYED: YES"; exit 0; fi
echo "R89 PEERS DEPLOYED: NO"; exit 1
