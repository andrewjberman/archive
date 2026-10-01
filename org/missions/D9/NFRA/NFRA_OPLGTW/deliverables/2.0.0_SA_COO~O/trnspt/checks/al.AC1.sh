#!/usr/bin/env bash
# OPLGTW OG-al-1 AC1: hx-capability.tf declares exactly ONE aws_lb_listener_rule on the https listener, forward-only to
# the gateway target group, path patterns exactly /hx/mail/* and /hx/transcripts/*, and no other resource.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
timeout 60 python "$(native "$H/_al.py")" tf 2>&1 | tr -d '\r'
