#!/usr/bin/env bash
# OPLGTW OG-ab-1 AC2: the tool-classification census over app/tools.py (static, tool_class_census.py) lists
# copy_site_file_to_s3 as a registered tool and reports 0 UNCLASSIFIED registered tools -- the gateway would otherwise
# fail-close the new tool to confirm_required.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks"
out=$(timeout 60 python "$(native "$D/tool_class_census.py")" "$(native "$PWD")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | grep -iE 'denominator|classified|UNCLASSIFIED' | head -8
reg=$(grep -cE 'def copy_site_file_to_s3\(' "$GW/app/tools.py")
unc=$(printf '%s\n' "$out" | grep -ciE '^ *UNCLASSIFIED[: ].*copy_site_file_to_s3|^ *copy_site_file_to_s3$')
zero=$(printf '%s\n' "$out" | grep -ciE 'unclassified[^0-9]*\b0\b')
echo "copy_site_file_to_s3 registered in tools.py: $reg (want 1); listed unclassified: $unc (want 0); census reports 0 unclassified: $([ "$zero" -ge 1 ] && echo yes || echo no)"
[ "$reg" = 1 ] && [ "$unc" = 0 ] && [ "$zero" -ge 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
