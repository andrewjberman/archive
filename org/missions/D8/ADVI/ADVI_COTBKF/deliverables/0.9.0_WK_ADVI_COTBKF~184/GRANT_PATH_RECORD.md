# CB-cp-1 grant path argument -- record (round 94, 0.9.0_WK_ADVI_COTBKF~184)

- Module: `data/assets/scripts/silver/cotbkf_crm_match_job.py`, commit `275c698a5f`.
- `--grant PATH` is optional and validated before it is opened. Refusals: `GRANT_PATH_ABSOLUTE`,
  `GRANT_PATH_OUTSIDE_DELIVERABLES`, `GRANT_PATH_NAME`, `GRANT_PATH_MISSING`. Without the argument the job reads the
  round-88 record, as before.
- The run record gains `grant_file` and `grant_sha256`.
- Tests: six `test_grant_path_*` added; the nineteen existing tests are unchanged (the test file shows added lines only).
- No argument names a key, a bucket or a role. The key still comes only from the grant record.
- Stub records only. No S3, no AWS, no CRM value. The account-id scan failed closed (the pinned set is absent).

Machine-readable form: `GRANT_PATH_RECORD.json` beside this file.
