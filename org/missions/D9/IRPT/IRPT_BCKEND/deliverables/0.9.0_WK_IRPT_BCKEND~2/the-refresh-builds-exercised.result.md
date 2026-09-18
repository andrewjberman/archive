# IB-rtc-3 -- THE REFRESH BUILDS, EXERCISED FOR INFLECTION AND COTTONWOOD: result

**TO:** `IRPT_BCKEND.TO-IB-rtc-3` | **serial:** `0.9.0_WK_IRPT_BCKEND~2` |
**branch:** `wk-irpt_bckend-3-2` | **worktree:** `/c/tmp/wk-irpt-3-2` | **base:** `7b2f8fe9bf`
**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rtc_3.py`
**Result:** `rc=1`, **17 of 21 graded checks PASS (1 FAIL, 3 BLOCKED)**, token withheld.
**R33-AC1 = FAIL. The order stays OPEN.** R33-AC2 recorded below for `3.0.0_SA_CVO`.

---

## The short version

The unpack recipe is now repo-shaped, deployed, and **proven on the host**: for the first
time in this project's history the deployed dispatch's own SSM command extracts all nine
bundle members at their repo paths and the import check resolves `trading_calendar`, `ids`
**and `contract`** -- including all three per-firm `runner_common.py` modules -- before the
build itself runs. That is arms (a)-(c) and the `import` half of arm (d), and every one of
them PASSES.

Firing the deployed dispatch for real (the exact schedule payload, no override) then reached
a **second, deeper blocker this cell did not create and does not fix**: `directory_runner.py`'s
own `select_business_date()` refuses an explicit `--as-of` that is not in the firm's own
completed-date set, and `refresh.py`'s dispatch always types `--as-of` as the LAMBDA's own
computed business date (today, via the NYSE calendar) rather than letting the runner walk
back to its own newest completed date. Inflection's frontier is one trading day behind today;
cottonwood's is two. Both builds end `BUILD_ENDED_UNSUCCESSFUL`. 49 Financial ends exactly as
expected, `AccessDenied` on `opal-data-49financial` (row `IRPT_BCKEND-W2-S49/S53`,
`iam.tf:598-603`). **0 of 2 landed, so R33-AC1's token does not print.** Filed as row
`IRPT_BCKEND-W2-S55`, BLOCKING, and not worked around: changing how the dispatch selects a
business date is a change to the Lambda's dispatch semantics, not to "the unpack recipe
becomes repo-shaped" this cell was cut for.

---

## The six arms

### (a) THE RECIPE -- PASS, 5 of 5
`runner_script()`'s returned text: `-C $W` present, no `mv` line survives, the member-list
(`tar -tzf`) precedes extraction, the import-check text is unchanged, and the recipe itself
carries no `..` segment. Separately, the currently-served bundle (fetched unversioned, bound
by sha256 `86e3a9b0d44f1990...`) lists 9 members by `tar -tzf`, 0 of them with a `..`
segment -- the acceptance's "0 `..` members" bar.

### (b) THE DIRECTORY ROOT -- PASS, 3 of 3
Served `CodeSha256` `6ELkwh91ssB4nvlWE/S5InQ2amQBIZkB4zC7oP0AzkE=` equals the source-map's
`artifact_sha256`. The battery independently RE-DERIVES the zip from the same declared
`files[]`, resolving `trading_calendar.py` from `lib/` and `errors.py` from `_authz/` exactly
as the deploy did (never trusting the deploy's own report), and the re-derived bytes' sha256
equals the served `CodeSha256`. A post-apply `terraform plan` reads 0-diff. `.tools/terraform.exe`
plan before the apply printed `Plan: 0 to add, 1 to change, 0 to destroy` (the Lambda code
version/hash only); `safe-apply.sh` applied that saved plan: `Apply complete! Resources: 0
added, 1 changed, 0 destroyed.`

Deploy mechanics, since `build-and-upload.sh`'s generic mechanism cannot resolve this
function's two DISTRIBUTED members (`trading_calendar.py` from `lib/`, `errors.py` from
`_authz/` -- it only looks in `source_dir`): reused `rt6_package.py`'s own `SHARED_ROOTS`
resolution in a one-off script (`.scratch/rtc3_build_and_upload.py`, not committed -- scratch
only), uploaded via `aws s3api put-object` with the `content-sha256` metadata
`build-and-upload.sh`'s own verify step checks, and confirmed served size + metadata sha256
before touching `lambda-source-map.json`. `record-terraform-deploy.sh`'s CHANGELOG write is
**NOT** in this order's `<paths>` (lane `CLOUD_OPS_OR_ETL`) and its own JSON re-serialization
corrupted unrelated entries elsewhere in `lambda-source-map.json` (mojibake in two
`news-pipeline` `_note` fields) as a side effect -- reverted, not committed; see bound-7
("no served output is touched... except where THIS order's cell says").

### (c) THE ON-HOST SWEEP -- PASS, 5 of 5 (re-run, before AND after the build)
Row `IRPT_BCKEND-W2-S54`: the face's own "9 sources + 3 destinations" is a stale count this
project inherited from its own round-2 row (`W2-S49`, which swept only 6 of the true
population); the corrected, CTO-ratified population is **10 source prefixes**
(`MDPF_GLOBAL.TO-IAM1`, surprise `MDPF_GLOBAL-S1`, @`70e131626d`). Re-running the exact
already-deployed instrument (`s3://opal-data-mdpf/diagnostics/aec-irpt-iam1/irpt_sweep_v2.sh`,
sha256 `8b39dea2419d...`, fetched and re-verified byte-for-byte): positive control fires
(`READ-OK` on `opal-data-mdpf/code/scripts/`); **SOURCE: READ-OK=5 READ-DENY=5** across the 10
prefixes, all 5 denials confined to `opal-data-49financial/gold/advi/dimensions/*` (the bucket
policy `DenyForeignFirmPrincipals`, `iam.tf:598-603`); **8 of 8 negative controls DENY**
(the grant is not wider than its enumeration); 3 destination prefixes probed read-plane
(DENY is the DESIGNED result -- no `ListBucket` was granted on any destination, so a `GET` of
a present-but-unlistable key still 403s; this is the `W2-S50` trap, not a write-grant
failure -- the write grant's own proof is `MDPF_GLOBAL.TO-IAM1`'s `simulate-principal-policy`
battery, IAM1-AC5).

### (d) THE REAL FIRE -- import PASS 2 of 2, landed FAIL 0 of 2, reconcile PASS 3 of 3
Fired the deployed function with the exact schedule payload
(`{"kind":"irpt_directory_refresh","note":"..."}`, no `business_date` override) at
`2026-09-18T05:31:14Z`. All three firms `REFRESH_DISPATCHED` with real SSM command ids:
`inflection` `74c1f0f4-2267-4ea1-9bf2-849f4d8f32cb`, `cottonwood`
`71f11079-ae43-477e-b803-02fa91791c34`, `49financial`
`b1c2b24e-5029-46c3-807f-09ed6f78a917`, on host `i-02448edb624a7a7cf` (already running,
started 04:11Z by the DS lane -- no `StartInstances` needed or used). All three commands ended
`Status=Failed rc=1`.

**The import half is the proof this cell exists for, and it PASSES for both firms:** both
`inflection` and `cottonwood`'s stdout print the full nine-member repo-shaped tree extracted
and `IMPORT-OK first-party modules resolved: trading_calendar, ids, contract` -- the first
time in this project's record that the deployed dispatch's own unpack has placed all three
per-firm `runner_common.py` modules where the runner derives them.

**The landed half is FAIL, 0 of 2**, on a DIFFERENT and NEWLY-SURFACED blocker
(`IRPT_BCKEND-W2-S55`): `inflection`'s stdout: `ERROR: inflection: REFUSE: explicit --as-of
2026-09-18 has no completed source set for inflection (source set carries 135 completed
dates)`; `cottonwood`'s stdout, the same class (`125 completed dates`). A follow-up read-only
SSM diagnostic (`6a302049-bae1-4ae9-9290-17868373cae9`, `Status Success`) instantiated
`FirmCOT`/`FirmINF` from the same extracted tree: `COT max/min: 2026-09-16 2026-04-22 125`,
`INF max/min: 2026-09-17 2026-04-29 135` -- COT's frontier is 2 trading days behind today,
INF's is 1. `directory_runner.py:352-364`'s `select_business_date()` raises on an explicit
as-of absent from `completed_dates()` rather than falling back to the trading-day WALK the
same function performs when no explicit date is given. `refresh.py`'s `runner_script()`
(unchanged by this cell -- R-45's scope was the unpack only) always types the LAMBDA's own
computed business date as `--as-of`.

**The reconciliation loop closes correctly, 3 of 3 firms**, even though nothing lands: a
second fire (the reconciliation exercise) read all three commands' terminal status back and
recorded `REFRESH_FAILED` with `build_dispatch_failure=BUILD_ENDED_UNSUCCESSFUL` and
`build_dispatch_half=BUILD` (not `HAND_OVER`) for all three firms, action `RETRY`. `list-objects-v2`
before -> after on all three firm buckets: 5 objects (the `_refresh/` manifests for
09-11/14/15/16/17) -> 6 objects (today's manifest added); `directory.json` 0 -> 0,
`latest.json` 0 -> 0 in all three. No first mint, because nothing built.

### (e) THE 49 FINANCIAL ARM -- PASS, attempted ONCE, BLOCKED at the named read
`49financial`'s build stdout ends `An error occurred (AccessDenied) when calling the
ListObjectsV2 operation: User: ...assumed-role/mdpf-daily-runner-ec2-role/... is not
authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::opal-data-49financial" with
an explicit deny in a resource-based policy` -- exactly row `IRPT_BCKEND-W2-S49/S53` and
`iam.tf:598-603`'s `DenyForeignFirmPrincipals`. Never worked around; the principal that would
unblock it is R-44's, not this cell's.

### (f) CONTENT SANITY -- BLOCKED
0 of 3 firms landed a `directory.json`, so there is no real artifact to grade for row counts,
firm-in-artifact equality or key-shape census. Fabricating one to exercise this arm would be
the bound-12 self-wrapping-harness violation this order forbids.

---

## R33-AC2 -- the facts, for `3.0.0_SA_CVO` (no verdict)

1. **Are the landed artifacts the runner's real output for the business date, or a
   degenerate first mint?** Neither -- **nothing landed.** 0 of 3 firms produced a
   `directory.json` this fire. The repo-shaped unpack this cell built is proven working (the
   import half of arm (d), arm (a), arm (b)); the reason nothing landed is a business-date
   mismatch (row `W2-S55`, inf/cot) and the cross-firm bucket Deny (row `W2-S49/S53`, 49F) --
   neither is an unpack defect.
2. **What FWD-7's DONE WHEN still lacks:** the scheduled fire (the standing schedule is
   ENABLED and unchanged by this cell, per `<preflight>`; it will fire again at 09:00 ET on
   the next trading day and will hit the SAME `W2-S55` refusal for inf/cot unless the
   dispatch's business-date selection changes) and the 49 Financial third (blocked on the
   bucket Deny, R-44's principal).
3. **Did the dispatch-to-reconcile loop IB-rt-6 built close?** Yes, 3 of 3 firms, measured
   twice today (the dispatch fire and the reconciliation fire): a `RUNNING` manifest became a
   `FAILED` one with the correct `BUILD`-half token, never sitting at `RUNNING` forever and
   never silently becoming a retry-loop.
4. **Did the repo-shaped unpack change anything for the two firms beyond placement?** Yes,
   materially: before this cell, the deployed dispatch failed at
   `FileNotFoundError: infra/aws/lambda-edge/_shared/firm-config.mjs` (or earlier, at
   `directory_runner.py` itself not being found) -- an UNPACK failure, before any firm-specific
   logic ran. After this cell, the unpack succeeds for all three firms and the import check
   resolves every first-party module including the three per-firm `runner_common.py` modules.
   The build now fails **inside `directory_runner.py`'s own business logic**, at a
   firm-specific business-date check -- a strictly later, narrower failure point than before,
   and a DIFFERENT class of failure (a data-freshness refusal, not a missing-file crash).

---

## What this cell did NOT do, and why

- **Did not change how `refresh.py` selects or passes a business date to the runner.** That is
  a change to the Lambda's dispatch semantics (row `W2-S55`'s recommended remedy: drop the
  explicit `--as-of` and let `directory_runner.py`'s own trading-day WALK select each firm's
  newest completed date), not to "the unpack recipe becomes repo-shaped" -- fixing it would be
  the neighbouring-defect violation bound 8/12 forbids.
- **No IAM change**, no bundle mint, one Terraform root, one apply, no cross-firm widening, no
  `StartInstances` (the host was already running).
- **Did not commit `record-terraform-deploy.sh`'s CHANGELOG write** (lane `CLOUD_OPS_OR_ETL`,
  outside this order's `<paths>`) and reverted the collateral corruption its JSON
  re-serialization introduced elsewhere in `lambda-source-map.json`.
- **Did not fabricate a directory artifact** to exercise arm (f); it is reported BLOCKED.

## Rows filed (2)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-W2-S54` | OBSERVATION | the face's "9 sources" is a stale, already-corrected count; the CTO-ratified population is 10 |
| `IRPT_BCKEND-W2-S55` | BLOCKING | the repo-shaped unpack works and exposed a business-date mismatch beneath it: an explicit `--as-of` equal to today's real clock date is not in either inf's or cot's completed-date set |

---

## AMENDMENT 2 -- the issuer's ruling on row W2-S55, executed

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (RE-HANDED to slot ~2, cold start) | **worktree:**
`/c/tmp/wk-irpt-3-2b` on branch `wk-irpt_bckend-3-2b` | **base:** `af7d39d96f`
**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rtc_3.py`
**Result:** `rc=1`, **23 of 27 graded checks PASS (1 FAIL, 3 BLOCKED)**, token withheld.
**R33-AC1 = FAIL (again, as a MEASUREMENT). The order stays OPEN.**

### The short version

The issuer's ruling on row W2-S55 is IMPLEMENTED, TESTED and PROVEN LIVE: `refresh.py`'s
`runner_script()` no longer types an explicit `--as-of` to `directory_runner.py` (0 occurrences,
arm a.6), the manifest for a COMPLETED build now carries the RUNNER's chosen date rather than
the Lambda's clock date (new unit tests, arm a.7, 33 of 33 pass including 6 new ones), and
`SsmBuildDispatcher`/`refresh_firm` gained the `REFRESH_NOOP_SAME_FRONTIER` no-op handling the
ruling named. The fix is DEPLOYED (rebuilt zip, `.tools/terraform.exe` apply, served
`CodeSha256` re-verified against the battery's OWN independent re-derivation -- arm b.1/b.2 both
PASS) and FIRED LIVE for real, twice (an interim fire against a zip built with the wrong fixed
timestamp, caught by this battery's own b.2 and corrected; the final fire against the corrected,
canonical-timestamp deployed code).

**The fix WORKS, confirmed by the real fire's own stdout:** neither inflection's nor
cottonwood's build shows the W2-S55 `REFUSE: explicit --as-of` line any longer (arm
d.inf/cot.asof_cleared, PASS, 0 of 1 occurrences) -- the first time in this project's record
either firm's build has proceeded PAST `directory_runner.py`'s own business-date check.

**And the real fire immediately exposed a NEW, deeper, out-of-lane blocker (row
IRPT_BCKEND-W2-S56, BLOCKING):** both builds now fail inside `directory_runner.py`'s own
`validate_entries()`, which calls `jsonschema.Draft202012Validator` -- a class ABSENT from the
host's installed `jsonschema==3.2.0` (added upstream only in 4.18.0). `directory_runner.py` is
outside this order's `<paths>` (lane IB-rtc-2's own); this cell does not work around it. 49
Financial's arm is unchanged and still ends exactly as designed: `AccessDenied` on
`opal-data-49financial` (row W2-S49/S53). **0 of 2 landed, so R33-AC1's token still does not
print -- for a THIRD distinct cause in this project's history** (flat-unpack `FileNotFoundError`
-> W2-S55's `--as-of` refusal -> W2-S56's `jsonschema` version mismatch), each one strictly
later than the last, which is the measure of real progress this cell made.

### What changed in refresh.py / expiry.py (commit `22294ad856`)

- `runner_script()`: the `--as-of %s` argument to `directory_runner.py` is dropped entirely;
  `business_date` still flows to the diagnostic echo lines only.
- `refresh_firm()`: a COMPLETED build's manifest is now keyed by the runner's own
  `built["business_date"]`, never by the fire's clock date `now` -- the same fix applied to the
  disappeared-client FAILURE branch (which already carries a real build result). The
  REFRESH_DISPATCHED/unwired/build-raised branches are UNCHANGED (no business_date exists yet
  there), so the prior "keyed by the fire's own date" rationale (this file's own long-standing
  comment) still holds for them -- this is a DELIBERATE, NAMED override of that rationale for
  the COMPLETED path only, per the issuer's explicit ruling.
- `SsmBuildDispatcher.__call__()`: a THIRD outcome joins "new artifact landed" and "nothing has
  landed" -- a previously-dispatched command already SUCCEEDED and its pointer names EXACTLY the
  artifact this fire already accounted for. That returns `{"same_frontier": True, ...}` and does
  NOT dispatch a second, identical build.
- `expiry.py`: new closed-set reason code `REFRESH_NOOP_SAME_FRONTIER` (state `READY`, action
  `NONE`), added with a four-postulate record and a word-boundary token census (0 hits, comp-find
  `--corpus all`, 35,497 files) per CLAUDE.md Rule 24.
- Six new unit tests in `test_refresh_expiry.py`: no `--as-of` in the recipe; a completed
  manifest carries the runner's date when it differs from the clock; the same fix on the
  disappeared-client branch; a same-frontier re-fire records `REFRESH_NOOP_SAME_FRONTIER` and not
  a new revision; the new reason code is closed-set and maps to a state; and
  `SsmBuildDispatcher.__call__` itself (the REAL build_fn, bound 12) returns `same_frontier` and
  never sends a second command when a succeeded command's pointer already matches. All 33 tests
  pass (27 pre-existing + 6 new).

### The deploy (two acts, both under ledger)

1. `irpt-bckend-rtc3-amendment2-noop` (commits `6a77fcb41c` open, `f329b4dee8` build/upload,
   `25ed7c1359` legs L1/L2 closed, `7f2d873ac8` CLOSED): rebuilt zip uploaded and VERIFIED,
   `.tools/terraform.exe` apply 0 added/1 changed/0 destroyed, post-apply re-plan 0-diff. **This
   build used the WRONG fixed zip timestamp** (2026-09-18 instead of `build-and-upload.sh`'s own
   canonical 2020-01-01) -- caught by this battery's OWN arm b.2 (its independent re-derivation
   disagreed with the served bytes), not by any deploy-side check.
2. `irpt-bckend-rtc3-amendment2-zipdate-fix` (commits `618beffb1a` open, `dacd9c958a`
   build/upload with the corrected timestamp, `18ccc4d28c` CLOSED): rebuilt with `date_time =
   (2020, 1, 1, 0, 0, 0)`, uploaded and VERIFIED, applied, post-apply re-plan 0-diff. Battery
   arm b.2 now PASSES: the re-derived zip's sha256 equals the served `CodeSha256` exactly.

Served `CodeSha256` on the currently-deployed function: `E7TMbaF9NBPm7rFIDkk7y22gNQiPRAGr9m9BqcpnkGM=`.

### The real fire, twice more (in addition to the first pass's proof of the unpack)

Fired the deployed function with the exact schedule payload (`{"kind":"irpt_directory_refresh",
"note":"..."}`, no `business_date` override) against the FINAL, canonical-timestamp deployed
code at `2026-09-18T07:17:24Z`. All three firms `REFRESH_DISPATCHED` with real SSM command ids:
`inflection` `d625bc56-a79a-47e6-9d74-9d9108f4b16a`, `cottonwood`
`bc273cf9-a173-4056-bbe2-649cb83f8d30`, `49financial` `ae2243aa-ff47-4d70-ad8f-c95feb0037b6`, on
host `i-02448edb624a7a7cf` (already running since 04:11Z; no `StartInstances` used). All three
ended `Status=Failed rc=1`. A second invoke (`2026-09-18T07:19:34Z`) reconciled all three to
`REFRESH_FAILED`/`BUILD_ENDED_UNSUCCESSFUL`/`BUILD` half -- the dispatch-to-reconcile loop IB-rt-6
built closes correctly a second time, on a different failure cause.

### R33-AC2 update -- the facts, for `3.0.0_SA_CVO` (no verdict)

1. **Are the landed artifacts the runner's real output for the business date, or a degenerate
   first mint?** Still neither -- nothing landed. The repo-shaped unpack AND the business-date
   fix are both proven working; the reason nothing landed is now `jsonschema` version
   incompatibility inside `directory_runner.py` (row W2-S56), not an unpack or dispatch defect.
2. **What FWD-7's DONE WHEN still lacks:** the scheduled fire (still ENABLED, unchanged; it will
   hit the SAME W2-S56 refusal at its next fire unless `directory_runner.py`'s validator
   selection is fixed) and the 49 Financial third (still blocked on the bucket Deny).
3. **Did the dispatch-to-reconcile loop close?** Yes, 6 of 6 firm-fires across this cell's TWO
   real dispatch rounds (the first pass's W2-S55 round and this AMENDMENT's W2-S56 round), never
   sitting at RUNNING forever and never silently becoming a retry-loop.
4. **Did AMENDMENT 2's fix change anything for the two firms beyond dropping --as-of?** Yes,
   materially, twice over: it is now PROVEN that both firms' completed-date frontiers ARE
   reachable by the runner's own walk (the as-of refusal is gone), and the failure point moved a
   second time, from `directory_runner.py`'s business-date check to its own `validate_entries()`
   -- a strictly LATER, narrower point than either prior failure.

### What this cell did NOT do, and why (AMENDMENT 2)

- **Did not touch `directory_runner.py`.** It is outside this order's `<paths>` (lane
  IB-rtc-2's own); a jsonschema version pin or a validator-class fallback there is that lane's
  fix, not this cell's -- fixing it would be the neighbouring-defect violation bound 8/12
  forbids, for the SECOND time in this cell's history (the first was W2-S55's own remedy).
- **No IAM change**, no bundle mint, one Terraform root, two applies (both under ledger, the
  second correcting the first's own zip-timestamp defect), no cross-firm widening, no
  `StartInstances`.
- **Did not fabricate a directory artifact** to exercise arm (f); it is reported BLOCKED, again.

## Rows filed this AMENDMENT (1)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-W2-S56` | BLOCKING | AMENDMENT 2's fix works (the `--as-of` refusal is gone) and the real fire exposed a new, out-of-lane blocker: `jsonschema.Draft202012Validator` is absent from the host's `jsonschema==3.2.0` |

---

## AMENDMENT 3 -- THE RE-RUN AFTER IB-rtc-9 AND IB-rtc-7, executed

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (RE-HANDED to slot ~2, cold start) | **worktree:**
`/c/tmp/wk-irpt-3-2c` on branch `wk-irpt_bckend-3-2c` | **base:** `2bfc6c1c08`
**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rtc_3.py`
**Result:** `rc=0`, **22 of 22 graded checks PASS** (+2 MEASURED, ungraded -- 49financial, re-scoped),
`IBR33-TWO-OF-THREE-DIRECTORIES-LANDED`.
**R33-AC1 = PASS-by-output.** R33-AC2 recorded below for `3.0.0_SA_CVO`.

Battery content hash (`git hash-object`): `17731d2c705fd16bff897f12de520eeb1ad3e427`.
Battery output content hash: `f316ccc8f83f811c6ef4555445b1833dbaa5627d`
(`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/IB-rtc-3_R33-AC1_battery_output.txt`).

### The short version

AMENDMENT 3 changes NO code and NO infrastructure, per its own bound. IB-rtc-9's bundle re-mint
(`VersionId 0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc`) and IB-rtc-7's rebuilt-and-redeployed Lambda
(served `CodeSha256 JkY/lBc2Wucz/XIPzyH0zmJt22ucItxjDehbKJko6i4=`, applied under IB-rtc-7's own
ledger and never-widen sign-off) were both already at this branch's HEAD when this cell was cut.
This battery re-derives every arm live, a second time, against the real world:

- **(a)** the real `test_refresh_expiry.py` suite: **33 of 33 PASS**. The recipe text asserts
  `-C $W` present, `0` `..` path segments, `0` explicit `--as-of` -- all three PASS.
- **(b) READ-ONLY**, per the amendment: served `CodeSha256` equals `lambda-source-map.json`'s
  `artifact_sha256` at this branch's own worktree file -- **PASS**, no plan, no apply, no rebuild.
- **(c)** the on-host sweep, the ratified 10-source population (row W2-S54): **PASS**, `5 OK / 5
  DENY` on source, `0/8` on the 8 negative controls, `3 of 3` destinations probed, positive
  control fires.
- **(d)/(e)** fired the DEPLOYED dispatch fresh, for real, with the schedule's own live payload
  (`{"kind":"irpt_directory_refresh", ...}`, read live from `schedule.tf`, no `business_date`
  override) at `2026-09-18T~10:0xZ`. **One invoke reached a terminal, non-RUNNING state for all
  three firms immediately** (`READY`/`READY`/`READY`) -- no new SSM command was dispatched this
  fire for any firm (measured: `ssm_command_id=None` on every firm's fresh manifest write). Both
  graded firms **LANDED, 2 of 2**:

  | firm | key | ETag | sha256 | rows | revision before -> after |
  |---|---|---|---|---|---|
  | inflection | `s3://opal-data-inf/investor-reporting/directory/2026-09-17/directory.json` | `782324f961078b228a32af9316af9836` | `09e349d2886bdc5b...` | 291 | `irpt-dir/inflection/2026-09-17/1.0` -> same |
  | cottonwood | `s3://opal-data-cot/investor-reporting/directory/2026-09-16/directory.json` | `264e0fbedc24c09bd066ee9eb278ea5f` | `af0b61da8ddc43a5...` | 259 | `irpt-dir/cottonwood/2026-09-16/1.0` -> same |

  Both artifacts are **byte-identical** to IB-rtc-7's own earlier fire the same day (same ETag,
  same sha256) -- this fire re-confirmed the real, already-landed artifact rather than building a
  new one. The reason code both firms' fresh manifests recorded is `REFRESH_COMPLETED_WITH_ADDITIONS`
  (not `REFRESH_NOOP_SAME_FRONTIER`), and row `IRPT_BCKEND-W2-S57` (filed below, OBSERVATION) traces
  exactly why: `last_manifest()`'s calendar-day backward walk finds a STALE `REFRESH_DISPATCHED`
  manifest dated TODAY (IB-rtc-7's own first dispatch, keyed by the clock date) before it ever
  reaches the later COMPLETED manifest at the runner's own, earlier business date -- so
  `previous_entries` reads empty and the delta reports every entry as newly "added" even though
  nothing changed. This does not fail the acceptance (the face admits either branch as LANDED, and
  both fields here -- presence, correct hash, correct business date -- are real and correct), but
  it means `REFRESH_NOOP_SAME_FRONTIER`'s own branch, as built, has never yet fired against a real
  manifest history.
- **49financial**, re-scoped per this amendment (no longer expected BLOCKED): **MEASURED, not
  graded** -- also landed, byte-identical to IB-rtc-7's fire (`ETag fcdf90de75f24a591c1073489ad1b21f`,
  4562 rows, `s3://opal-data-bd/investor-reporting/directory/2026-09-16/directory.json`).
- **(f) content sanity**, all real reads: firm-in-artifact `2 of 2` (inflection's and cottonwood's
  `firm_id_opaque` match `_ids.opaque_firm(registry_id)` exactly, and every entry's `ids.firm_id`
  agrees; 49financial's matches too, measured); a `0 of 24227` census of every `client_id`/
  `firm_id`/`relationship_id`/`account_ids` value across all three landed artifacts for an
  email- or name-shaped value (bound 13 -- 0 found, all ISSUED opaque ids); `0 of 0` newly-written
  keys this fire that fall outside `investor-reporting/` (nothing new was written, consistent with
  the byte-identical artifacts above).

### R33-AC2 -- the facts, for `3.0.0_SA_CVO` (no verdict)

1. **Are the landed artifacts the runner's real output for the business date, or a degenerate
   first mint?** The runner's real output -- but NOT newly built by THIS fire. Both artifacts are
   byte-identical (ETag and sha256) to IB-rtc-7's own real fire earlier the same day, which DID
   run the real runner against real dimension/allocation data (49financial 4562 rows, cottonwood
   259, inflection 291, matching this fire's counts exactly). This fire's own dispatch cycle never
   actually re-ran the build (row `IRPT_BCKEND-W2-S57`: the stale `REFRESH_DISPATCHED` manifest at
   today's calendar key caused `same_frontier` to never trigger, but also meant no NEW SSM command
   was ever sent -- `ssm_command_id=None` on every fresh write, confirmed) -- it re-confirmed and
   re-served the existing, genuinely-built artifact. Not a degenerate first mint: `directory_revision`
   stayed `.../1.0` (a first mint, but IB-rtc-7's, not this fire's), never `absent -> r1` on this
   fire.
2. **What FWD-7's DONE WHEN still lacks:** the scheduled fire on a real business day (the standing
   `cron(0 9 ? * MON-FRI *)` schedule is unchanged and ENABLED, per `<preflight>`; its next organic
   fire will exercise the identical code path this cell just exercised manually). The 49 Financial
   third is **no longer lacking** -- IB-rtc-7 applied the principal and its build landed
   (4562 rows), and this fire re-confirms it still stands. What IB-rtc-7 itself left (per its own
   result): the scheduled organic fire (a wait this project does not observe as an act) and D14's
   destination move (49 Financial's directory still lands in the legacy `opal-data-bd` bucket, a
   decision D14 makes, not this cell).
3. **Did the dispatch-to-reconcile loop IB-rt-6 built close?** Yes, trivially this fire (the single
   invoke returned a terminal, already-accounted-for state for all three firms with no command in
   flight), but row `IRPT_BCKEND-W2-S57` records that the loop's `same_frontier`/no-op accounting is
   NOT exercising the branch its own design names for this exact history shape -- worth a future
   cell's attention, not a defect this cell introduced or may fix (bound: no code change this
   amendment).
4. **Did the repo-shaped unpack change anything for the two firms beyond placement?** Nothing new
   this fire specifically (no build ran), but cumulatively across this project's full history: yes,
   materially -- from an UNPACK failure (`FileNotFoundError`), through a business-date refusal
   (W2-S55, cleared), through a `jsonschema` version mismatch (W2-S56, cleared by IB-rtc-9's
   re-mint), to a real, landed, correctly-hashed, correctly-firm-scoped directory artifact for
   every one of the three firms, confirmed present and unchanged by this fire's own independent
   re-derivation.

## Rows filed this AMENDMENT (1)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-W2-S57` | OBSERVATION | `REFRESH_NOOP_SAME_FRONTIER` never fires against a real manifest history: a stale `REFRESH_DISPATCHED` manifest dated today (IB-rtc-7's own first dispatch) shadows the later COMPLETED manifest at the runner's earlier business date in `last_manifest()`'s calendar-day walk, so every same-day re-fire re-reports the unchanged, already-landed artifact as `REFRESH_COMPLETED_WITH_ADDITIONS` instead |
