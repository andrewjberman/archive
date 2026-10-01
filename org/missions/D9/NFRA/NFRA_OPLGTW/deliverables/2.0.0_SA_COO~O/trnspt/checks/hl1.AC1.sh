#!/usr/bin/env bash
# OPLGTW OG-hl-1 AC1 (PRD v1.4 C7 mail listing): the 12 named tests of tests/test_mail_listing.py, Graph and the token
# broker stubbed -- the listing route's rules (sender-bound, minimal rows, caps, opaque bound page token, ordering, empty
# window) and the sender-table file kept equal to NFRA_TRNSPT's criterion.py.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
pytest_named tests/test_mail_listing.py \
  test_list_requires_mail_bearer_only test_list_offtable_sender_403_before_graph test_list_empty_table_403 \
  test_list_window_bounds_400 test_list_page_size_bounds_400 test_list_rows_minimal_keys \
  test_list_drops_row_whose_own_sender_offtable test_list_orders_and_pages_without_repeat \
  test_list_page_token_bound_to_sender_and_window test_list_rejects_graph_url_token \
  test_list_empty_window_200_zero_rows test_sender_table_file_equals_criterion; r=$?
restore_audit
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
