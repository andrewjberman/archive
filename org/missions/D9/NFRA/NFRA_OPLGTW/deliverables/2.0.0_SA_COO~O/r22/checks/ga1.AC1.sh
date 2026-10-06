#!/usr/bin/env bash
# OPLGTW OG-ga-1 AC1 (STORE): the one in-force dim_asset grant carries download_filtered at a new revision; its other
# scope dimensions and every other principal's in-force grant are unchanged against the worker's before-record.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
B="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/GA1_BEFORE.json"
python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r22/checks/ga1_state.py")" --grade "$(native "$B")"
