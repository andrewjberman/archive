# SESSION LOG -- AMGT_RESAPP.TO-AMGT-rk-19 (adapter half) -- 0.9.0_WK_AMGT_RESAPP~27

Worktree: `.claude/worktrees/wk-amgt-13-27-chainB`, branch `wk-amgt-13-27-chainB`, HEAD at start `67168eba8c`.

1. First act: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-27-chainB`; `test -d org && test -d .tools` -> both present, `TREE-OK`. All six `<paths>` entries confirmed present.

2. Read the task order file at its own path and confirmed it matches the worker face verbatim.

3. Read `thesis_driver_chart()` (`lib/research/api/scoped_amgt.py:1953-2013` at HEAD) and its caller `read_thesis_bundle()` (`:1897-1949`).

4. Traced the driver's schema forward: `lib/research/filings/analyze.py` (raw driver + points schema, `resolve_driver()` :640-676), `lib/research/filings/drafting_build.py` (`build_drafting_document()` :211-247, copies `analysis.get("thesis_driver")` verbatim :239), `read_drafted_sections()`/`_read_drafting_document()` (`scoped_amgt.py` :1387-1445, :1581-1637) -- confirmed the bundle's `thesis_driver` traces to `drafting/v1/<key>.json`, NOT `filings/v1/.../analysis.json` directly.

5. Read the sibling producer order (`AMGT_RESAPP.TO-AMGT-rk-19.filings-producer-verification.md`, issued to `0.9.0_WK_AMGT_RESAPP~26`) to learn the corrected schema shape (`points[].span`, `points[].passage_id`, `held_uncited`, `resolution`).

6. Live read, `s3://opal-data-harvest/filings/v1/BA_US_Equity/000162828026004357.analysis.json`: `thesis_driver.points` carries 3 entries, each with `span` and `passage_id`, `held_uncited: []`, `resolution: "cited"` -- the producer half HAS drained (this differs from an earlier attempt at this same order on a different worktree/branch, `wk-amgt-13-27`, commit `2577f1db86`, which found the producer half undrained at its own polling time; time has since moved and the fix has landed).

7. Live read, `s3://opal-data-harvest/drafting/v1/BA_US_Equity.json` (the object `read_drafted_sections()` actually reads, confirmed via `DRAFTING_BUCKET`/`DRAFTING_PREFIX` defaults and no Terraform override in `scoped-amgt-api.tf`): the SAME 3 points, but with NEITHER `span` NOR `passage_id` NOR a `held_uncited` key -- the pre-fix shape, never rebuilt by the producer order (whose own `<paths>` scopes its pool write to the `filings/v1` key only) or by anything else in this round's plan. Filed as row `AMGT_RESAPP-Z-W27-S3`.

8. Snapshotted `lib/research/api/scoped_amgt.py` to `.scratch/scoped_amgt.py.orig` (blob `3cb02df1ea`) before editing.

9. Implemented the second branch inside `thesis_driver_chart()`'s `matched is None` arm: fires only when `>= 2` of `thesis_driver.points` carry a `span` (the verified marker) AND `resolution` is not `None`/`"held"`/`"absent"`; serves `status: "SERVED"`, `source: "filing"`, each point's `period`/`value`/`unit`/`span`/`passage_id`; otherwise stays `ABSENT` printing `held_uncited_count` vs the raw emitted `points` count. Added `points_count: 0` to the two pre-existing early-return branches so `points_count` is always a printed integer, never an implicit `None`.

10. `python -m py_compile lib/research/api/scoped_amgt.py` -> `COMPILE-OK`.

11. Local sanity check, 6 synthetic `thesis_driver` shapes fed directly to the patched `thesis_driver_chart()` (no I/O): (1) stale/pre-fix shape (points, no span) -> ABSENT, points_count 0; (2) verified shape, 3 spanned points, resolution cited -> SERVED, source filing, points_count 3; (3) only 1 spanned point -> ABSENT (needs >=2), held_uncited_count 2; (4) resolution "held" with 2 spanned points -> ABSENT (never serve on a held/absent driver); (5) `thesis_driver=None` -> ABSENT, points_count 0; (6) exact-mnemonic hit (unchanged first branch) -> SERVED, source "model-block fiscal_year_line_item". All six matched the design.

12. Re-ran the patched `thesis_driver_chart()` against the two LIVE driver objects read in steps 6-7: the CORRECTED `filings/v1` driver -> SERVED, source filing, points_count 3 (matches AC2's exact expectation); the STALE `drafting/v1` driver (the one actually served) -> ABSENT, points_count 0, held_uncited_count 0 -- confirms the code is correct and the gap is purely the unrebuilt cache object (row S3), not the adapter logic.

13. Ran AC1's and AC2's literal `<invocation>` blocks, byte-for-byte, against the LIVE deployed `opal-amgt-scoped-api` (unmodified this session; `CodeSha256 zHmPoWu9jZqUUqlK9zwvfoZk/aFg+rOoOLbuJwHGRHA=`, `LastModified 2026-09-17T03:27:57Z`): both returned `statusCode 401`, body `{"refused": true, "reason": "missing edge-injected X-Firm-Id: request did not pass auth-validator-edge"}` -- neither invocation's `headers` carries the `x-firm-id` header `lib/research/api/scoped_amgt.py:3021` `_firm_id()` requires, so neither reaches `thesis_driver_chart()` at all. Filed as row `AMGT_RESAPP-Z-W27-S4`.

14. Searched `git log --all` for any `sign()`/`co-sign()` commit naming `rk-19` for round 13: zero. The only precedent never-widen pairs in this project (`rk-2`, `rk-6`, `rk-7`) are each authored by `2.0.0_SA_COO~Z` (COO half) and `1.0.0_SA_CTO~Z` (CTO half) themselves, never by a worker. Per CLAUDE.md's hard stop ("NEVER move served output without never-widen sign-off (CTO+COO)") and the standing rule that no agent message authorizes waiving a hard stop, this worker did NOT redeploy the Lambda. Filed as row `AMGT_RESAPP-Z-W27-S5`. No change-management ledger entry was opened, because no live deploy act was performed to open one against.

15. Filed rows `AMGT_RESAPP-Z-W27-S3`, `S4`, `S5` by textual splice inside the one fenced JSON array in `INVESTIGATION_v1.md` (326 -> 329 items, verified by re-parsing the fenced block); `python .tools/surprise-row-gate.py <path>` -> `OK: 1 file(s), all new rows carry their step-7/step-10 fields.`

16. AC1 and AC2 both graded FAIL per the REFUSAL CLAUSE: run literal, byte-for-byte, actual output recorded, not repaired/widened. `<status>` is not flipped to `complete` (the order stays open, blocked on rows S3/S4/S5).

17. Wrote this SESSION_LOG and the proof-of-spec instance; ran `python .tools/proof-of-spec-check.py <instance> AC1,AC2`.

## RESUMED SESSION (same worktree, 2026-09-17 ~18:5x-19:3xZ) -- the co-sign now exists

18. Re-grounded: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-27-chainB`, HEAD unchanged at `0e974a48e7`; `test -d org && test -d .tools` -> `TREE-OK`. Read the CTO half at `org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND13_RK19_ADAPTER_SECOND_JOIN_CTO_HALF.md` @`e3fc4495cf` verbatim (`git show`), confirmed row S5's prior blocker (no co-sign at HEAD) is resolved. Confirmed no separate COO-half ledger file exists yet for this act (`git log --all --grep`); the dispatching instruction from `2.0.0_SA_COO~Z` carries the COO half's own required content (live pre-act anchor to be measured fresh, pre/post census, rollback, ledger open/close) inline.

19. Opened the change-management ledger BEFORE any live act: `python .tools/deploy_ledger.py open --slug amgt-rk19-adapter-thesis-driver-second-join-20260917 --lambda opal-amgt-scoped-api --window-hours 4` -> `OK: OPENED ... 1 legs`.

20. Read the LIVE pre-act state fresh: `boto3.client('lambda').get_function_configuration(FunctionName='opal-amgt-scoped-api')` -> `CodeSha256 zHmPoWu9jZqUUqlK9zwvfoZk/aFg+rOoOLbuJwHGRHA=`, `LastModified 2026-09-17T03:27:57.000+0000`, `CodeSize 781832`, one layer (`opal-amgt-print-deps:1`), `MemorySize 512`, `Timeout 29`, `Environment` two vars unchanged.

21. Pre-deploy census: `scoped_amgt_route_table()` -> 16 routes total, 13 GET; invoked all 13 live (rawPath+`x-firm-id: bd`+`requestContext.http.method GET`, `BA_US_Equity`/`trending`/`chatter` substituted for path params) -> 13 of 13 `200`. Also read pre-deploy `BA_US_Equity/thesis` body: `thesis_driver_chart` `status ABSENT` (old code, no second branch).

22. Ran `bash infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`: transitive-closure package (47 code entries, 7 data members, 6 vendored packages), ISOLATED runtime 3/3 arms OK, uploaded to `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip`, local sha256 `zuWM8IZziIL4u/0n2sXeeF+ZdW7hTKoHrtDHTHOqrzQ=`, `head-object` confirms `VersionId DZ_9GSNC5kbJoKC6AvdG17ZQo85JB7z6`.

23. `terraform -chdir=infra/aws/terraform/harvest init -reconfigure`, then `plan -target=module.scoped_amgt_api.aws_lambda_function.this` first FAILED on an unrelated resource (`chatter-axis-schedule.tf:124`, `filebase64sha256(local.chatter_axis_zip)` on a missing `.build/chatter-axis-producer.zip` this worktree never built) -- resolved by running `python infra/aws/terraform/harvest/lambda_src/build_zip.py` (gitignored, untracked output only). Filed as part of row `AMGT_RESAPP-Z-W27-S6`. Re-ran the targeted plan: `Plan: 0 to add, 1 to change, 0 to destroy`, naming only `module.scoped_amgt_api.aws_lambda_function.this` (`source_code_hash`, `s3_object_version`, `last_modified` -- matches the CTO half's discriminator exactly).

24. `HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/harvest apply -target=module.scoped_amgt_api.aws_lambda_function.this -auto-approve -no-color` (first attempt without `HALT_ACK` blocked on a routine, non-STOP-class HALT-GATE of 182 base-inbox messages; grepped the full output for `rk-19`/`scoped-amgt`/`AMGT_RESAPP` -> zero hits, none relevant; re-ran with the tool's own documented `HALT_ACK=1` escape). naming-apply-gate/naming-plan-gate both WARN-only on pre-existing resource names (none an addition). `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`

25. Read the LIVE post-act state: `CodeSha256 zuWM8IZziIL4u/0n2sXeeF+ZdW7hTKoHrtDHTHOqrzQ=` (matches the uploaded artifact exactly), `LastModified 2026-09-17T19:23:42.000+0000`, `CodeSize 782668`, layer/memory/timeout/environment unchanged.

26. Post-deploy census, same 13 GET routes, same shape: 13 of 13 `200`; `LOST=[]`, `GAINED=[]` against the pre-deploy census.

27. Re-ran AC1 (corrected header shape, already at HEAD): `statusCode 200`, `points_count 0`, `status ABSENT`, `reason "no thesis_driver on a served D-1 document"` -- matches AC1 exactly. PASS.

28. Re-ran AC2 (corrected header shape): `statusCode 200`, `status ABSENT`, `points_count 0`, `held_uncited_count 0` -- does NOT match AC2's `points_count 3, source "filing"`. Re-read `sa._read_drafting_document('BA_US_Equity')` in this same session: `thesis_driver.points` still 3 entries, none carrying `span`/`passage_id` -- byte-identical to row S3's prior grounding; the drafting/v1 cache was never rebuilt (explicitly out of scope, CTO half section 4 item 6) and this session did not touch it. AC2 genuinely FAILS; the deploy itself is correct.

29. Targeted 0-diff replan: `terraform plan -target=module.scoped_amgt_api.aws_lambda_function.this` -> `No changes. Your infrastructure matches the configuration.`

30. Closed the ledger leg with the full proof string (apply delta, hash transition, replan, live config, census, AC1/AC2 outcome), then `python .tools/deploy_ledger.py close --slug ...` -> `OK: CLOSED ... all 1 legs proven; sentinel removed`.

31. Filed row `AMGT_RESAPP-Z-W27-S6` (confirms S3 on the live post-deploy plane; also names the unrelated `.build/` precondition from step 23). Updated this session's proof-of-spec instance (AC1 PASS, AC2 FAIL-genuine) and this log.

32. `<status>` is NOT flipped to `complete`: AC2 fails, genuinely, for a reason (drafting/v1 cache staleness) this act's own co-sign explicitly places out of scope. The order stays OPEN.
