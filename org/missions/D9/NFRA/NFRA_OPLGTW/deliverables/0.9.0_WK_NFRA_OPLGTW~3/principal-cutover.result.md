# NFRA_OPLGTW.TO-OG-a-2: principal cutover result (second run, order as amended @adc6874dea)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3c` (worktree `/c/tmp/wk-oplgtw-1-3c`, cut from
`CLOUD` at `3f94e0a024`) | **Commits (LOCAL, this run):** `318e119c4f` fixtures + AC13 probe; `840de8bd66` rows
W3-S13, W3-S14; and the commit carrying this file and the rebuilt proof instance. First run: `d02e73c272` code,
`5f47166b4b` rows, `fed567f54e` proof. Nothing was pushed, merged or deployed.

## Read this first: the order stays OPEN (OGA2-AC12 FAIL, refused as written; row W3-S13 BLOCKING, ARMED)

12 of 13 criteria pass by output. **OGA2-AC12 does not:** the three granted modules read `3 failed, 28 passed`
(they read `16 failed, 15 passed` before the amendment's grant).

- **Why they fail:** each of the 3 fails on an untouched assertion that compares a validated token's `sub` to an
  email. The three assertions are `test_oauth_durable.py:710`, `test_jwt_cve_lock.py:117` and
  `test_schwab_audit.py:342` @`318e119c4f`.
- **Why a fixture cannot fix them:** OGA2-AC1 requires `sub = <tid>/<oid>` with no `@`, and `validate_access_token`
  refuses any other `sub`. So no fixture yields an email subject. Each test already reaches its assertion holding a
  token the gateway accepted.
- **Why the worker stopped there:** the grant is fixture-only ("no assertion is removed, weakened or re-targeted").
  Passing these three means re-targeting each one, to the principal key or to the email claim. The worker left all
  three as written.
- **What would disarm it:** an issuer amendment that permits that one-expression re-target. OGA2-AC13 cannot tell
  such a re-target from none, because the assert counts would not move.

The proof instance validates (checker rc 0). Per the order, a VALID instance with a FAIL row is not a met order, so
`<status>` is left `pending`.

## What changed this run (`318e119c4f`, fixture-only)

| file | change |
|---|---|
| `tests/test_oauth_durable.py` | The LocalIssuer's ID token carries a `tid` (the harness tenant) and an `oid` fixed per email. The fixture patches `token_broker.redeem_code_for_principal` with `LocalIssuer.redeem_principal`, which verifies the token and returns `make_principal(tid, oid, email)`, and sets `TENANT_ID` to the harness tenant. The email-only `redeem_code_for_email` patch is gone. |
| `tests/test_jwt_cve_lock.py` | The control test takes a `family_store` fixture (moto DynamoDB, fake credentials, harness tenant, revocation files in `tmp_path`) and mints its token from a refresh family: register, pending authorization, code, PKCE S256 exchange. |
| `tests/test_schwab_audit.py` | `test_ogo1_ac06` mints its token the same way, inside its existing `mock_aws`. |
| `probes/og_a2.py` (deliverables) | The AC13 probe. It counts assert statements per module by AST, from git objects at HEAD and at `3f94e0a024`. A failed or empty git read is a FAIL, never a zero. |

No assert, `self.assert*` or `pytest.raises` line was added, removed or edited. `git diff -U0` over the three files
shows 107 changed lines, and 0 of them name an assertion. The app modules and `tests/test_principal_cutover.py` are
byte-identical to `d02e73c272` (`git diff --quiet` rc 0). The commit gate read `OK ... 4 of 4 file(s)`.

## Criteria (each invocation run verbatim at `318e119c4f`, and AC13 again at `840de8bd66`)

| id | verdict | deciding output |
|---|---|---|
| OGA2-AC1 .. AC11 | PASS-by-output, 11 of 11 | `1 passed` each, rc 0. The denominator lines are byte-identical to the first run's (11 of 11) |
| OGA2-AC12 | **FAIL** (refused as written) | `3 failed, 28 passed in 17.08s`, rc 1. FAILED: `test_oauth_durable.py::test_oga1_ac13`, `test_jwt_cve_lock.py::test_control_valid_token_accepted`, `test_schwab_audit.py::test_ogo1_ac06` |
| OGA2-AC13 | PASS-by-output | `VERDICT: PASS-OGA2-AC13`. HEAD == base: 123/123, 6/6, 63/63 (58 assert + 5 pytest.raises); modules equal 3 of 3 |

## Controls

- **Mutant:** AC13's own verdict path, run in-process with the HEAD copy of `test_jwt_cve_lock.py` minus one `assert`
  line. Result: `VERDICT: FAIL-OGA2-AC13 test_jwt_cve_lock.py HEAD=5 base=6`, rc 1. FIRED-AS-EXPECTED. The first
  run's code mutant (the family status check removed, so AC6 failed) still describes the unchanged code.
- **Determinism:**
  - AC13: 3 runs, with identical per-module lines.
  - AC12: 2 runs, with the same 3 FAILED ids and the same summary line.
  - AC1..AC11: 11 of 11 denominator lines are identical to the first run's.
  - STABLE.

## Checker

`py -3.12 .tools/proof-of-spec-check.py <instance> OGA2-AC1,...,OGA2-AC13` -> `VALID (rc=0)`, violations 0.

- **Artifacts:** 11 of 11 are content-resolved at their pins.
- **Surprises:** 8 of 8 entries resolve to a channel row.
- **Invocations:** 13 of 13 match the criterion text.

The first check read `INVALID (rc=1)`. It found two defects in the instance itself: AC12 carried no
`status_reason`, and one `introduces` token was not literal text at its pin. Both were corrected, and nothing else
changed.

## Rows filed this run (`840de8bd66`)

| id | class | hazard | subject |
|---|---|---|---|
| NFRA_OPLGTW-W3-S13 | BLOCKING | ARMED (2.0.0_SA_COO~O) | Under the fixture-only grant OGA2-AC12 cannot pass: 3 untouched `sub == <email>` assertions against OGA2-AC1's `<tid>/<oid>` |
| NFRA_OPLGTW-W3-S14 | OBSERVATION | INERT | `test_jwt_cve_lock.py`'s `__main__` smoke calls the control test without its new fixture; pytest is unaffected (INFERRED from source, not run) |

W3-S7 (the first run's BLOCKING row) is disarmed in part by the amendment: 13 of its 16 failures now pass. The
remaining 3 are W3-S13. Rows W3-S8 .. W3-S12 stand as filed.

## Side effects outside the grant

- The untracked `audit.jsonl` at the worktree root (a default `AUDIT_PATH` side effect of the test runs) is not
  committed. The tracked `infra/aws/ec2/opal-gateway/audit.jsonl` is unmodified (`git status` clean for it).
- `.venv-og/` and `.scratch/` are not committed.
