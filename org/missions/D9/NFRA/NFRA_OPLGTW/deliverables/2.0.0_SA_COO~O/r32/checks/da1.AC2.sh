#!/usr/bin/env bash
# OPLGTW OG-da-1 AC2: the LIVE opal-data-refresh-api Lambda runs box/sitez HEAD's lambda_function.py byte for byte
# (da1_live.py). Today live = HEAD, so this reads PASS at the cut; it FAILs from the moment the cell's code lands until the
# deploy carries it, then PASSes again on the new bytes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
timeout 110 python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/da1_live.py")" opal-data-refresh-api "$(native "$PWD")" | tr -d '\r'
