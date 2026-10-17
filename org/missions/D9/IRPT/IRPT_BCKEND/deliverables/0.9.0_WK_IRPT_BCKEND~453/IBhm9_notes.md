# IB-hm-9 notes -- the dispatch half of the per-firm HMAC list (0.9.0_WK_IRPT_BCKEND~453)

Order: `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-hm-9.dispatch-passes-the-hmac-arguments.md`.
Worktree: `C:/dev/wk-IRPT_BCKEND-453`, branch `wk-IRPT_BCKEND-453`, base `6c413115b9`.

## The change

`infra/aws/lambda/investor-reporting/directory/refresh.py` now hands the runner's three HMAC arguments to each
firm's build. Three module-level helpers read `IRPT_HMAC_SECRET_ID`, `IRPT_HMAC_ROLE_ARN` and
`IRPT_HMAC_LIST_URI_MAP` (a JSON object of firm id to list URI) from the Lambda environment. Each value is
validated: the secret id must fullmatch the order's character class, the role ARN must start with the IAM
prefix, contain `:role/` and use only the ARN characters already allowed, and the list URI must fullmatch the
S3 shape with no `..` and no trailing slash. A value that fails is dropped, so the firm builds with no HMAC
arguments. `_hmac_args_for(firm_id)` returns the six tokens only when all three are valid for that firm.
`runner_script` takes an optional `hmac_args`, shell-quotes each token and places them before `2>&1`; with none,
the build line and the whole script are unchanged. `SsmBuildDispatcher.dispatch` passes the tokens and trails
`hmac list stage armed for the <firm> build` (firm id only). No literal secret, ARN, bucket or S3 address
is in the module; the S3 pattern is written with escaped slashes, as a shape rather than an address.

The six tests in `infra/aws/lambda/investor-reporting/directory/tests/test_refresh_hmac_args.py` use invented
values only and pass (6 passed, three runs).

## Counts, directory folder (`python -m pytest infra/aws/lambda/investor-reporting/directory/tests -q`)

- Before: 95 passed, 5 failed, 15 errors.
- After: 101 passed, 5 failed, 15 errors (95 plus the six new tests).
- The failing and error sets are identical, 20 lines each (`diff` empty).

## Criteria

- IBHM9-AC1 and AC2: PASS before the commit; output in `IBhm9_criteria_output.txt`.
- IBHM9-AC3: reads HEAD~1..HEAD, so it runs after the one commit. Its result is in the worker report, not in
  this file or the instance, and the proof instance records it as UNCOMPUTABLE-BY-CONSTRUCTION with that named later run.

## Held and surprised

- The status flip of TO-IB-hm-9 to complete is HELD. AC3's allowlist admits no path for the order file, so
  a flip in the one commit would fail AC3. Row `IRPT_BCKEND-D2-W453-S1` in `INVESTIGATION_v1.md`. The order stays
  `pending` for the issuer.
- Row `IRPT_BCKEND-D2-W453-S2`: the check's AC1 success line says "ten" over a six-name tuple. Cosmetic.
