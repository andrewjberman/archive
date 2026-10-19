# IB-cw-5 notes, worker 0.9.0_WK_IRPT_BCKEND~461

**The change.** `infra/aws/lambda/investor-reporting/directory/refresh.py` gains one pure helper,
`rekeyed_keys(previous_entries, current_entries)`, placed above `disappeared_entries`. A previous key the current build
lacks is RETAINED when every previous entry of that key names at least one account id and the union of those account ids
is a subset of the account ids of ONE single current entry; the helper returns the retained keys, sorted and unique. It
reuses `_entry_key`. `disappeared_entries` now leaves a retained key out, so `resolve_disappeared` neither holds nor
carries it, whatever the source (a `None` source included). `compute_delta` takes its `disappeared` set minus the
retained keys; `prev`, `cur` and every other count are untouched, and the delta gains no key. A key with an account in
no current entry, a key whose accounts are split over two current entries, and a key with an account-less previous entry
still disappear and are held or carried exactly as before. `refresh_firm`, `last_manifest`, the dispatcher and the
`TO-IB-cw-2` failure handling are not touched. The diff against HEAD is 37 added lines and 3 replaced lines in
`refresh.py`. No AWS call, no S3 access, no deploy, no push; invented keys and account ids only.

**The new test file.** `infra/aws/lambda/investor-reporting/directory/tests/test_refresh_retained_key.py` carries the eight
named tests (AC1). All eight pass.

**Test counts for the directory folder** (`python -m pytest infra/aws/lambda/investor-reporting/directory/tests -q
--color=no -p no:cacheprovider --continue-on-collection-errors`, run from the worktree root):

- Before the change: 32 failed, 194 passed, 6 errors.
- After the change: 32 failed, 202 passed, 6 errors. The 8 new passes are the eight named tests.
- The failing and error set is IDENTICAL before and after (38 ids, compared line for line). The 38 ids, with the
  directory path omitted:

```
ERROR test_search_readers_overage.py::test_B1_served_Entry_handle__over_age
ERROR test_search_readers_overage.py::test_B1_served_Entry_handle__plain
ERROR test_search_readers_overage.py::test_B2_enforce_Enforcer_serve__over_age
ERROR test_search_readers_overage.py::test_B2_enforce_Enforcer_serve__plain
ERROR test_search_readers_overage.py::test_control_the_plain_fixture_is_a_list_and_the_over_age_one_is_the_envelope
ERROR test_search_readers_overage.py::test_control_the_two_wire_answers_differ_only_where_the_envelope_says
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[directory]
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[entitlement]
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[principal]
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[query]
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[revoke]
FAILED test_bootstrap_browse.py::test_cursor_cannot_survive_context_change[size]
FAILED test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable
FAILED test_bootstrap_browse.py::test_partial_and_foreign_documents_are_withheld
FAILED test_bootstrap_browse.py::test_uir07_browse_q_puts_the_exact_full_name_match_first_across_the_cursor[Thiessen, Anna]
FAILED test_bootstrap_browse.py::test_uir07_browse_q_puts_the_exact_full_name_match_first_across_the_cursor[anna thiessen]
FAILED test_bootstrap_browse.py::test_uir07_browse_q_puts_the_exact_full_name_match_first_across_the_cursor[thiessen anna]
FAILED test_bootstrap_browse.py::test_uir07_browse_without_a_full_match_keeps_the_directory_order
FAILED test_custody_owner.py::test_real_custody_access_and_projected_organization_reader[None]
FAILED test_entry.py::test_search_honours_limit_from_the_2_0_event_shape_wider_match_truncated
FAILED test_entry.py::test_search_honours_q_from_the_2_0_event_shape_exact_one_match
FAILED test_entry.py::test_the_pre_fix_mutant_ignores_q_and_limit_on_the_same_fixture
FAILED test_opal_context.py::test_actual_global_and_selected_partner_preserve_distinct_firms
FAILED test_opal_context.py::test_selected_browse_cursor_cannot_cross_firm_or_principal
FAILED test_read_once.py::test_a_rotated_pointer_is_seen_by_the_very_next_request
FAILED test_read_once.py::test_the_directory_is_read_once_per_request_and_never_across_requests
FAILED test_read_once.py::test_the_revision_hash_and_the_browse_order_are_computed_once_per_version
FAILED test_read_once.py::test_the_same_version_is_parsed_once_across_requests_and_a_new_version_is_not
FAILED test_search_overage.py::test_a_directory_with_no_as_of_is_unchanged
FAILED test_search_overage.py::test_an_in_age_directory_serves_as_before[2026-10-07-2026-10-05]
FAILED test_search_overage.py::test_an_in_age_directory_serves_as_before[2026-10-07-2026-10-06]
FAILED test_search_overage.py::test_an_over_age_directory_answers_the_declared_expiry[2026-10-07-2026-09-30-5]
FAILED test_search_overage.py::test_an_over_age_directory_answers_the_declared_expiry[2026-10-07-2026-10-02-3]
FAILED test_search_overage.py::test_an_unknown_age_is_never_served_as_fresh
FAILED test_search_overage.py::test_the_boundary_is_max_age_trading_days_exactly
FAILED test_search_overage_public_status.py::test_calendar_unavailable_status_is_public_too
FAILED test_search_overage_public_status.py::test_over_age_status_has_only_public_members
FAILED test_search_overage_public_status.py::test_over_age_status_still_states_the_expiry
```

These fail at base for reasons outside this order and are not touched by it.

**Line endings.** `refresh.py` and the sibling tests are LF at HEAD (byte-counted); the edit keeps LF. The
investigation file is LF and is appended in append mode (see the commit's numstat).

**Surprises.** Two rows are filed in `INVESTIGATION_v1.md`: the sparse worktree lacks `org/surprise_channel`, so the row
schema was read from the base checkout; and AC2 can only pass after the commit, because it compares `HEAD` with
`HEAD~1`.
