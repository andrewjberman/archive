#!/usr/bin/env bash
# AMGT_RESAPP round 41, AMGT-rp-1 AC3 -- THE HARNESS CAN FAIL: round 40's difference control, re-run unchanged. The harness the
# sweep uses reads round 38's stale body (17 extras) as NOT OK. A control: it PASSES at the base. usage: bash <this>
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
bash org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/ro-1.AC2.sh
