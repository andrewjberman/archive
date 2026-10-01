#!/usr/bin/env bash
# OPLGTW OG-pr-1 AC1 (CTO ruling R3 / C11): gateway-read-secrets.tf names exactly the three secrets
# gateway/transcripts/bearer, gateway/mail/bearer and gateway/principals/rosters by metadata-only data sources and
# grants opal-gateway-role exactly secretsmanager:GetSecretValue on exactly their three ARNs; no secret version.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
timeout 60 python "$(native "$H/_pr.py")" tf 2>&1 | tr -d '\r'
