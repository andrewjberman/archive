#!/usr/bin/env bash
# MP-n-1 AC1 (PRD v0.6 C17, the bounded read): a planted store at 1x (5 days) and 10x (50 days) of history, with the trunk
# head moved inside the 48 h window and no refusal, gives EQUAL get_object counts for a cold _compute.
. "$(dirname "$0")/../../cp2/checks/_root.sh"
timeout 110 python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/c17/checks/_n1_harness.py ac1
