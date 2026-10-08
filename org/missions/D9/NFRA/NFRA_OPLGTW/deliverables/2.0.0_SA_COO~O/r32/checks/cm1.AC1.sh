#!/usr/bin/env bash
# OPLGTW OG-cm-1 AC1 (PRD v2.0 item 4, FWD-12, acceptance A23): a grant may set calendar_months (1 to 13) in place of
# calendar_days. Five named tests in tests/test_grant_calendar_months.py, offline (S3 and the state store faked):
#   (01) a rolling grant with calendar_months=13: the window is the latest qualified complete business date back to the
#        same calendar day 13 months earlier, month-end clamped (latest 2026-03-31 -> first 2025-02-28), and two
#        qualified dates a year apart are both available;
#   (02) exactly one of calendar_days / calendar_months: a grant carrying both is refused, and calendar_months 0 or 14
#        is refused, at the grant write AND at the read;
#   (03) a date inside a 13-month window with no qualified completion record is reported in not_available, never filled
#        from another date, dataset or master;
#   (04) a grant with calendar_days (or neither) answers exactly as before this cell: the same window, the same dates;
#   (05) the A14 query and export caps are unchanged: the contract's `limits` equal the cut's, and a 13-month request
#        that would exceed them is refused by the existing cap, not served.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_cm1_audit_$$.jsonl"
pytest_named tests/test_grant_calendar_months.py test_ogcm1_ac01 test_ogcm1_ac02 test_ogcm1_ac03 test_ogcm1_ac04 test_ogcm1_ac05; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
