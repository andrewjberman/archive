#!/usr/bin/env bash
# OPLGTW OG-sf-1 AC2 (R54): the census. Every function tools.py decorates with @mcp.tool is counted (the denominator)
# and classified against SAFE_TOOLS, DESTRUCTIVE_OPS and TOOL_WRITE_CLASS by the issuer's own static reader
# (tool_class_census.py, ast only). PASS when opal_asker_query is in SAFE_TOOLS and the worker's census record lists
# exactly the same unclassified set and denominator as the issuer's reader.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~37/tool_class_census.json"
timeout 60 python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/tool_class_census.py")" \
  "$(native "$PWD")" --worker-record "$(native "$REC")" | tr -d '\r'
