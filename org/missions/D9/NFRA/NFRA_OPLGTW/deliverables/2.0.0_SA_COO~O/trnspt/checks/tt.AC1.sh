#!/usr/bin/env bash
# OPLGTW OG-tt-1 AC1: taxsma-capability.tf declares exactly ONE aws_lb_listener_rule on the https listener, forward-only
# to the gateway target group, path pattern EXACTLY /ms/taxsma-workbook (no /ms/* wildcard), and no other resource.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
timeout 60 python "$(native "$H/_tt.py")" tf 2>&1 | tr -d '\r'
