# CB-cl-1 record safety: CRM job run record

Module: `data/assets/scripts/silver/cotbkf_crm_match_job.py` at blob `44c23f5effd76f628ab94f35eea8b9d943e40a98`
(commit `afbd09f46e`). Tests: `data/assets/scripts/silver/tests/test_cotbkf_crm_match_job.py` (commit `afbd09f46e`).

Shape of the run record after the change, by key name:

- `header_columns`: per member, `columns` (a count), `roles` (role name to count), `first_line_is_header` (a bool).
- `columns_used`: a list of `member:role` strings, plus one `blackdiamond:bd` entry for the holdings.
- `skipped_members`: a count of CSV members whose first line is not a header. The job declares no schema for any
  member, so such a member is skipped and its text is never read.

Refusal: `_write_record` raises `RECORD_CARRIES_MEMBER_TEXT` and writes nothing when a record string matches a hashed
cell read from the zip.

Results on stub zips: `-k record_safety` gives 6 passed, 5 deselected. The whole file gives 11 passed. The
account-id scan failed closed because the pinned account set is absent on this box.

No CRM value, name or account number appears in this note.
