#!/usr/bin/env bash
# OPLGTW OG-md-1 AC1 (PRD v1.9, C7): the headless mail route admits and lists by sender DOMAIN. Seven named tests in
# tests/test_mail_route_domain.py, offline (Graph faked): (01) a message from a listed domain, from an address NOT on
# the sender table, is LISTED by `sender_domain` and FETCHED by id; (02) an unlisted domain is refused 403 before any
# Graph call; (03) `sub.<listed domain>` and `<x><listed domain>` (a suffix) are refused: the match is whole and
# case-insensitive; (04) a request with BOTH `sender` and `sender_domain`, or NEITHER, is refused 400; (05) a page
# token minted for one domain is refused 400 when presented with another domain, and a sender token is refused for a
# domain request; (06) with the domain table empty or unset every `sender_domain` request is refused 403 and nothing
# is admitted by domain, while the sender table still admits its addresses; (07) a domain listing drops every row
# whose own sender is not at the requested domain, counts the drops in the audit record, puts a HASH of the domain
# and never the domain or an address in that record, and returns v1.4's five row fields exactly.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r31_md1_audit_$$.jsonl"
pytest_named tests/test_mail_route_domain.py test_ogmd1_ac01 test_ogmd1_ac02 test_ogmd1_ac03 test_ogmd1_ac04 test_ogmd1_ac05 test_ogmd1_ac06 test_ogmd1_ac07; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
