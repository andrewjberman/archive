# CB-co-1 (round 93): the CRM job's key and session name come from the grant record

Module: `data/assets/scripts/silver/cotbkf_crm_match_job.py` at blob `a573cb7ef2` (commit `1f1b8972ef`, branch `wk-ADVI_COTBKF-183`).

- The module constant `KEY` is removed. `grant_key(grant)` returns `(bucket, key)` from the grant's single `policy_resources` entry, or raises `GrantKeyRefused` with a short code.
- The restricted prefix is derived from `opal_naming.key(...)`, not typed.
- An optional grant `session_name` must match `cotbkf-crm-match-[0-9]{1,6}` exactly; absent, `SESSION_NAME` is used.
- `gate` returns a reason and never raises on a malformed grant. `run_job` takes the grant; `main` takes no key.
- Eight `test_grant_key_*` tests added. The eleven existing tests are unchanged (test file diff: 133 added, 0 removed).
- No S3 or AWS call. No CRM value, account number or real key in any file.
