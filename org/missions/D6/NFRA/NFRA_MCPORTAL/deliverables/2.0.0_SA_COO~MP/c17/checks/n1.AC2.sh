#!/usr/bin/env bash
# MP-n-1 AC2 (PRD v0.6 C17, integration_refused): a planted refusal that a LATER rc == 0 integrate superseded reads
# "not recorded"; a planted refusal newer than every integrate reads {at, note}.
. "$(dirname "$0")/../../cp2/checks/_root.sh"
timeout 110 python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/c17/checks/_n1_harness.py ac2
