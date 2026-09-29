# NFRA_OPALAI.TO-OA-e-10 -- session log -- 0.9.0_WK_NFRA_OPALAI~16

Worktree `C:/tmp/oa-16`, branch `wk-NFRA_OPALAI-16`.

1. Read the `/login` path (server.py login(), the :199 access arm, callback()), token_broker (cache owners) and the
   callers of `get_token(<email>)`. The email-keyed cache is written only by `redeem_consent`.
2. Census over SSM on i-07dccb1615503ac99 (journalctl counts, cache file names, `.env` key hashes): LOGIN_USES 0
   over 2026-07-14..2026-09-28; DEPENDENTS 1 (one identity on /otp/* and /ms/*) -> BRANCH NARROW.
3. Built the NARROW branch in server.py; new tests/test_login_retire.py; test_email_deny.py untouched.
4. AC1 PASS, AC3 PASS. AC2 FAIL as written: e10.AC2.sh matches `tests/...` and pytest prints `tests\...` on this
   Windows device; the tests themselves passed (2 passed, 3 runs). Filed BLOCKING row Z-W16-S4. Order left open.
5. Mutant: guard removed -> both new tests fail; restored byte-for-byte.
6. Issuer answered row Z-W16-S4 (matcher amended, 3ebf12c48f). Re-ran AC1-AC3: all PASS (AC2 named passed=1). Proof
   re-validated rc=0; `<status>` flipped to complete.
