#!/usr/bin/env bash
# OPLGTW OG-tg-1 AC1 (PRD v2.3 item 4; Andrew ~03:2xZ and ~03:3xZ, CTO msgs 32320, 32327, 32339): six named tests in
# tests/test_opal_users_gate.py, offline (Graph faked):
#   (01) poll_addressed_teams_messages returns each message's sender UPN and tenant id (from Graph from.user) for EVERY
#        caller, beside today's fields;
#   (02) read_chat_messages returns the same two fields for every caller;
#   (03) for the Bloomberg concierge principal ONLY, Teams reads (poll, chat, channel) DROP a message whose sender UPN is not
#        @opalinvest.com, and drop one whose identity cannot be read (unreadable = external); display names are never used;
#   (04) for that principal, send_chat_message and send_channel_message REFUSE a chat or channel with any member whose UPN
#        is not @opalinvest.com (or is unreadable), and admit one whose members are all @opalinvest.com;
#   (05) another caller (an unscoped staff principal) gets unfiltered reads and unrestricted sends: the gate is that
#        principal's only;
#   (06) the concierge is UNSCOPED: identity_scope.check returns None for it on a tool outside the old seed, and the two old
#        overlay rows are gone.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_tg1_audit_$$.jsonl"
pytest_named tests/test_opal_users_gate.py test_ogtg1_ac01 test_ogtg1_ac02 test_ogtg1_ac03 test_ogtg1_ac04 test_ogtg1_ac05 test_ogtg1_ac06; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
