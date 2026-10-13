# IRPT_ANLREQ round 20 -- the status rule into all eight `served.py` packagers, with the current `ops/status.py` into `irpt-status` -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-13. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Asked for by the CTO's round-19 analysis section 1 (row D2-W54-S5: ONE `served.py` into all eight, both pin groups together), round-20 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_20_20261013.md`, rows W55-S25 and the enrichment list), and msg 6882 (the binding the rule ends).

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened (and, where it says so, re-ran); INFERRED = said so.

## 1. What moves

- **`_authz/served.py`** (commit `564e60483858a3cc5c51ffea6aed0f76ff291abe`, blob sha256 `30c0eb88ec38...`) into the eight functions that package it: it carries (a) the AR-y-172 status rule -- an INTERNAL caller (Opal's own principal class) who selects ANOTHER firm is admitted only when the `opal-users-v2` row exists and its `status` is exactly `active`; no row, or any other status (`disabled`, absent), is refused `FIRM_BINDING`; an active row binds as before; service subjects are unchanged -- and (b) the AR-y-184 caller-class log line.
- **`ops/status.py`** (commit `e93258c650b369df46e22210d94add7cbb0d1749`) into `irpt-status` only: the difference from the deployed one is the `CORRECTION_WORDS` literal alone (AST equal without it; 4 words -> 28), so the status envelope shows words for the 24 finding codes the upload door now returns (row `W55-S25`, accepted by the CTO as a named limit until this pair).
- **Writers of `served.py` into a served package: N = 8** (RECORD `AR-y-185`, recounted from `lambda-source-map.json`: 8 of 235 map entries; the resident does not reach it). Each of the eight is read below; no other member of any package moves.

## 2. Start state, per function (MEASURED: `get-function`, zip downloaded and hashed; the S3 versions listed 2026-10-13 ~11:0xZ)

| function | live CodeSha256 | S3 latest version (= live object) | base commit (BUILD_ONLY guard: 8 mentions) | release patch (git hash-object) | EXPECTED CodeSha256 | moves |
|---|---|---|---|---|---|---|
| `irpt-directory-search` | `TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=` | `sk08zsHKMXATPSxY1lGWOPBHDA3mUZLa` (2026-10-12T13:50:48Z, 193621 bytes) | `e274a0e60c` | `irpt-directory-search.release.diff` (`731d34f7ec`) | `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=` | served.py |
| `irpt-narrative` | `0+/PHOb/xGvYNBrz/j4Ltk5k85clmAo96BOJzi9n3ZY=` | `vfMfQUz1j8R1ke05lBe2jNX6yAjWbIOz` (2026-10-12T13:54:58Z, 220364 bytes) | `5d8b0390ed` | `irpt-narrative.release.diff` (`91a941971d`) | `vBzPCvn9lUEZzmDFGK+9g9ICnF8h7N8Z/hccjw2qoBg=` | served.py |
| `irpt-export-render` | `dCzMEt04dtBAlvkj+2rZMGZaU30kY+7leZxN00dbxH8=` | `kxJxKiFuGVIu8UpXBif2tzRxZY_cwNcS` (2026-10-12T13:51:02Z, 418605 bytes) | `e274a0e60c` | `irpt-export-render.release.diff` (`d1b67fe334`) | `K74JEIjw0NKmy4YfEo7Sb7LcRxEII+/yaYtaKJ3qnD8=` | served.py |
| `irpt-holdings` | `SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=` | `hfQkgY1LcwrlvQCRQrJJlUJ2TLeah6op` (2026-10-13T11:24:26Z, 299273 bytes) | `e274a0e60c` | `irpt-holdings.release.diff` (`52b8a1118e`) | `d1HwIxeAvr2V1RibOmjT8UQBOd7NdzFqi4LPEKxjZPw=` | served.py |
| `irpt-49f-reporting-read-lambda` | `IhlTVtU9yYVskJ3PUOcoOKp1HnE2WAW5V8X31IwKkTc=` | `2iKVUY7CiWJvX2WaCmY8hd7OTf48Uupy` (2026-10-06T01:28:35Z, 277334 bytes) | `e274a0e60c` | `irpt-49f-reporting-read-lambda.release.diff` (`ebbaf2443c`) | `WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0=` | served.py |
| `irpt-performance-adapter` | `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=` | `oI.PAFCtZLh1MQJR6sh1UZY0O0A.YAfe` (2026-10-12T22:30:22Z, 446422 bytes) | `5d8b0390ed` | `irpt-performance-adapter.release.diff` (`53d1bdc588`) | `NdwQsZ4YsijmDKfv1ElBDuSJzCsNKVv/80/xeT7y7bg=` | served.py |
| `irpt-status` | `JmOhV/ep4mR1mt2NKKqyUlohgO3mlDw1GEM4eAWYKdw=` | `c7FKfNVu49nUZj6tEQbKx43ZGNg_gyGU` (2026-10-12T13:52:10Z, 361441 bytes) | `5d8b0390ed` | `irpt-status.release2.diff` (`09ffe5db3c`) | `vlGh380QUKvBMOhJn0GJGgDi1/WLI9qTaSP2uETmdP4=` | served.py and ops/status.py |
| `irpt-ycharts-generate` | `bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=` | `hgfB7ucwFdyO.uwz4GiwtC24IDlOmN7n` (2026-10-13T06:23:42Z, 620712 bytes) | `4067c2dd5b` | `irpt-ycharts-generate.release.diff` (`3b85d26d1f`) | `hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg=` | served.py |

Each release differs from its live package in the members named in the last column and in NOTHING else (members compared one by one; RECORD `AR-y-212`, `-213`, `-217`, drained @6703116dd4, @97896cf32d, @a709345527). Each BASE was proved by a holds-only build: the map at the base with no patch builds the live CodeSha256 byte for byte (8 of 8). For `irpt-ycharts-generate` that is trunk `4067c2dd5b`, which carries release 19's rows. Every base carries the guard of `build-and-upload.sh` (BUILD_ONLY mentions: 8 at `5d8b0390ed`, `e274a0e60c` and `4067c2dd5b`).

## 3. Artifacts, pins, rollback

- **Build, per function:** a throwaway worktree OUTSIDE the product tree, DETACHED at the function's base commit, the function's release patch applied (uncommitted), then `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <fn>` -> the printed CodeSha256 must equal the EXPECTED column; any other digest: ABORT that function before any upload. **Never run the script without `BUILD_ONLY=1` for the check, and never at a commit whose copy lacks the guard (row `D2-S69`: at pre-guard commits the script uploads).** Then the same script WITHOUT `BUILD_ONLY` from the same worktree uploads the new object version; read it back (sha256 equal to the build).
- **Patches:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~61/r20/` (group A, `~61`), `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~64/r20/` (group B, `~64`), and `irpt-status.release2.diff` under `~66/r20/` for `irpt-status`; each is a git diff of `infra/aws/lambda/ci/lambda-source-map.json` only; check each file's `git hash-object` against the table.
- **Terraform:** per function a scoped plan (`-target module.<module>.aws_lambda_function.this`, the function's `tf_resource` in the map): `Plan: 0 to add, 1 to change, 0 to destroy`, differing attributes `last_modified`, `s3_object_version`, `source_code_hash` only, environment equal (as act 4's L4 printed for the same eight functions); `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`. Eight units, sequential, about 75 s each (act 4: first unit start 14:03:43Z, last unit end 14:13:46Z).
- **ROLLBACK, per function (independent):** copy the S3 version in the table's column 3 onto the key, scoped plan and `safe-apply`, read CodeSha256 back equal to column 2. The versions in column 3 are the live objects at the time of writing; step 0 re-reads them and a changed latest version is a STOP (someone wrote). Nothing is deleted.
- **Source map, in the close commit and not before:** the eight release diffs applied to the trunk map (only `served.py` rows, and the `ops/status.py` row of `irpt-status`), plus each function's `artifact_*` and `last_deployed_*` record; on any conflict beyond those rows the applier stops.
- **Ledger:** one entry `irpt-status-rule-all-eight-20261013`, nine legs as act 4's (L1 verify, L2 before sample, L3 builds, L4 plans, L5 applies, L6 after sample, L7 first hour, L8 after-reads, L9 map record).

## 4. Blast radius -- who is refused after this

- **People who meet a refusal:** an internal caller (Opal's own staff principal class, home firm `opal-capital`) that SELECTS a firm other than its own through any of the eight functions, and whose `opal-users-v2` row is absent, `disabled` or has no `status`. Measured population (RECORD `TO-RUN-C173`, `C173_INTERNAL_CALLERS_CENSUS.json`, read 2026-10-12T23:35:00Z, 86 items): 56 profile rows, 33 external, 23 internal -- 21 `active` (5 Dev, 14 with no user type, 2 service) and 2 `disabled` (1 Dev, 1 with no user type). So two named rows would be refused if they selected another firm. **NOT countable: internal callers with NO users row** (part (b): no log line carries the caller). The AR-y-184 line (`INTERNAL-CALLER-CLASS class=<row_present|row_absent|row_non_active> outcome=<admitted|refused>`, no identity) measures that after the release: after-read A4.
- **narrative's no-selection path (row `W65-S4`):** narrative's entry also calls the rule for an internal caller who selects NO firm; a users row without a `status` raises inside that call and narrative hands roster None (class UNKNOWN) -- fail-closed, and a change from today's roster. A row with `status` `active` is unchanged.
- **What changes in the envelope of `irpt-status`:** for the 24 codes of the upload door the envelope adds a `CORRECT` action with the finding's words (the action already exists for 4 codes). The portal's status reader admits `CORRECT` at PROD `37aa1247ee` and DEV `f644605182` (RECORD: `contracts/public-status.ts:41` lists it among the six closed actions; test `iv-e-123.correction-words`); the words are a free string. MEASURED by this seat by reading the source at both commits; not run.
- **No client-facing page changes; no portal file changes.** Andrew's word is not needed.
- Reach: the eight functions are read-only or request-driven; none writes a served output through this change (the rule only refuses).

## 5. Order and after-reads

**Step 0 (the applier, within the hour before the first unit):** R0a this file and both halves signed on one blob; ledger opened, every live worktree's open entries read and the denominator printed; R0b each function's CodeSha256 equals the table's column 2, each key's latest version equals column 3 AND that object, downloaded and hashed, equals the CodeSha256 (any difference: STOP that function; the rollback target must be the live bytes); R0c the guard check for each base commit.
**Sequence:** the eight units in the table's order (`irpt-status` and `irpt-ycharts-generate` last), each: build and compare -> upload -> scoped plan -> `safe-apply` -> A1/A2. The rule is per function and no stored state crosses functions, so a half-done sequence is a safe state; the window is short on purpose (act 4: about 10 minutes).
- **A1:** CodeSha256 reads the EXPECTED value. **A2:** the downloaded live zip equals the previous package in every member but the named ones.
- **A3 (the act-4 sampler):** `SAMPLE_BEFORE` then `SAMPLE_AFTER` -- 14 records, a granted and a refused viewer for each side-effect-free function, status and body sha256 only (ADVI_FIRMBKTS deliverables, `r4_sample_eq.py`; its viewers are an active internal profile and a partner row): EQUAL 14 of 14. If the sampler cannot run in the applier's seat, A3 reads ABSENT with the reason and A1/A2 stand.
- **A4 (the rule, measured after):** the first hour's CloudWatch lines `INTERNAL-CALLER-CLASS` of the eight log groups, counted by class and outcome with the denominator (functions read, minutes, lines) -- this is the part (b) number; a `row_absent` or `row_non_active` count above zero is REPORTED to the CTO with the class and the function, never with an identity.
- **A5:** the `irpt-status` envelope for one of the 24 codes (any stored request in that state, or an offline call of the packaged `build_status_envelope`) shows a `CORRECT` action with words.

## 6. Both branches

- **All reads as expected:** close the ledger, the map record, disarm `D2-W54-S5`, `D2-W55-S1` (limits stated) and `D2-W55-S25`.
- **A function's A1 or A2 false, or its plan shows more than the three attributes:** ROLL THAT FUNCTION BACK (above), stop the sequence, close ROLLED_BACK for the unit and file a row; functions already done stay (independent).
- **A person is refused who should not be (a report, or A4's counts):** record the function, the class and the time (no identity); roll nothing back for one report; bring it to the CTO. The remedy for a wrongly-refused person is their row's status, not this release.

## 7. Limits named

- **Callers with no users row cannot be counted before the release** (C173 part (b)); A4 counts them after.
- **narrative's no-selection roster (W65-S4)** and **the rule's own limits (W55-S1):** the log line is absent on a lookup exception and on an unregistered firm; its `outcome=` is the selection gate's verdict.
- **Tests:** only the list below was run, against the shipped `served.py` (the trunk head carries the same blob):
- `irpt-directory-search`: 216 passed, 4 failed (test_read_once, fail identically with the old bytes; after AR-y-216).
- `irpt-narrative`: 69 passed, 0 failed (after AR-y-216; 56 and 13 failed before it).
- `irpt-export-render`: 313 passed, 0 failed (after AR-y-216).
- `irpt-holdings`: 182 passed, 0 failed.
- `irpt-49f-reporting-read-lambda`: 21 passed, 0 failed.
- `irpt-performance-adapter`: 277 passed, 1 failed (the fallback-calendar test, fails identically with the old bytes).
- `irpt-status`: 313 passed, 22 skipped, 0 failed (with status.py moved; the live bytes: 310 passed, 3 failed).
- `irpt-ycharts-generate`: 10 of 11 arms (the failing arm g_schema_valid also fails with the old bytes); pytest cannot collect (fitz missing).
- **Not read by this seat:** the eight functions' configuration beyond CodeSha256, the deployed portal bundles, any real internal caller.
- **ycharts-generate** was released at `bNPCG2Oe...` on 2026-10-13 (release 19); this pair builds on that package (base `4067c2dd5b`).

## 8. Owed before any apply order is cut

1. The CTO half on this file's blob.
2. The applier (this seat proposes `0.7.0_AE_CloudOps~AQ2`, a fresh lane that applied the holdings restore; the CTO half may name another).
3. Nothing from Andrew.
