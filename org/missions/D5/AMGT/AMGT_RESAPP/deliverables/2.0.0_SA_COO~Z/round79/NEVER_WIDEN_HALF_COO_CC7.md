# AMGT_RESAPP round 79 -- AMGT-cc-7 never-widen half (COO), 2.0.0_SA_COO~Z, 2026-10-08

**SIGNED** (the signature block is the last section; the issuer's calls on the eleven open points are the section THE ISSUER'S CALLS).

Measured and drafted by a subagent of `2.0.0_SA_COO~Z` on 2026-10-08, 12:55Z to 13:50Z. Nothing was built, deployed, applied or
uploaded. No `terraform`, `pip`, `safe-apply` or download ran, and the snapshot event was not sent. Every number was measured
in that session unless its line says INFERRED or CITED. The issuer reads this whole, rules on the section OPEN POINTS FOR THE
ISSUER, and signs.

**THE PIN: `63f0605039e3a95eae1868b8d4917fef40052447`** (the drain of the adapter cell cc-6). Every `git show <pin>:<path>` read
and the whole CONTENT-DIFF below are at this one commit.

**HEAD has moved; no packaged file has.** HEAD was `bf4829e697` when the session started and `43a0ba8cc1` at 13:31Z: six commits
after the pin (`bf4829e697`, `fd1c038a53`, `0894b4d98d`, `325bd4e0f8`, `609c015f18`, `43a0ba8cc1`; logs, a ledger and records by
`2.0.0_SA_COO~D`, `2.0.0_SA_COO~Z`, `2.0.0_SA_COO~RV`, `3.0.0_SA_CVO~RV`, `1.0.0_SA_CTO~Z`). `git diff --name-status <pin> HEAD`
over the 136 packaged paths, the folder `infra/aws/terraform/harvest/` and the module `modules/yang-lambda/`: 0 lines, read at
13:31Z and again 13:45Z.

**BUT A MERGE THAT MOVES TWO PACKAGED FILES IS IN PROGRESS IN THE SHARED TREE.** At 13:45Z the shared tree holds another
seat's uncommitted merge (`.git/MERGE_HEAD` `bf1b297689`, a commit of `2.0.0_SA_COO~G1`; laid into the tree at 13:27:23Z by
the file times; 1,010 staged files; who runs it was not read). Staged against HEAD on the packaged paths:
`lib/opal_naming.py` (+12 / -0: a second switch in the naming census and a `--all-roots` flag) and
`infra/logic/registry/exemptions.json` (+6 / -24). Neither is on this half's lists as it will then read. When that merge
commits, HEAD differs from the pin on those two packaged files. This draft touched nothing of it.

**The GO names the pin exactly, and the build is from a DETACHED worktree at the pin, or this half is measured again at the
commit the GO names.** A build at the merged trunk would carry two files this half did not read. The pin is a sound build commit: the six drains in the orders' last `<status>` lines
(`0433c23f27`, `bdd1a55638`, `beee52785a`, `f6b844fadd`, `646167b6df`, `63f0605039`), the six cell commits, the four
AMGT_HARVST commits of the CHANGED table and the round-78 trunk merge `f6cff376d1` are its ancestors, 17 of 17 checked
(negative control: HEAD is not an ancestor of the pin, rc 1). The
round-78 pin `fbb643923e` is NOT an ancestor (rc 1): it was a scratch build commit, never merged, as its own half says.

## READ FIRST: SIX FINDINGS THE ISSUER RULES ON

1. **AC3 as written will exit 1 after a correct deploy.** `round77/checks/r77_served_shape.py` clause C5 finds the segment
   block by walking the `/thesis` body for the first object that holds `rows`, `source` and `reason`. From this round the new
   key `segment_table` holds all three and is met before `segment_breakdown`. Measured: the check reads **YES on the deployed
   function now and NO on the tree** (C5 only). The served `segment_breakdown` did not change. Section EARLIER-ROUND PINS.
2. **AC2's c59 reads NO today and can read NO after a correct deploy.** It compares the stored snapshot with a view worked out
   on the executor's box. It reads YES only after the snapshot leg wrote, and only while no store has moved since. Section
   EARLIER-ROUND PINS.
3. **ONE apply carries no order between the grant and the code** (no dependency edge in the `.tf`). The window is real and
   touches no served route while the stored snapshot is under 24 hours old. That ends at **2026-10-09T12:30Z**. Section BOTH
   BRANCHES OF THE SNAPSHOT LEG.
4. **The artifact gains FOUR files, not three, and SIX files of other projects ride it.** `collector_record.py` (round 78's
   bb-16) enters through the new reader's import. Section THE CONTENT-DIFF.
5. **The stored snapshot shrinks from 4,758,475 B to about 1,063,343 B.** The retired read record
   `reads.seeking_alpha_bronze` is 3,740,991 B of today's object. Not a loss of rows: 302 rows before and after.
6. **The shared tree is about to leave the pin on two packaged files** (the merge in progress named above). The build is at
   the pin regardless; the criteria run on the shared tree. OPEN POINT 11.

## THE ACT

For `opal-amgt-scoped-api`, under ONE NEVER-2 entry and this pair. Executor `0.7.0_AE_CloudOps~A`. Order:
`task-orders/AMGT_RESAPP.TO-AMGT-cc-7.the-code-redeploy.md`. Three legs, recorded apart:

1. **Grant leg.** The role's inline policy gains ONE read-only prefix in two limbs.
2. **Code leg.** ONE artifact built from a DETACHED worktree at EXACTLY the pin, then ONE `safe-apply` on
   `infra/aws/terraform/harvest/`, the plan graded UNTARGETED. It moves exactly two resources. `memory_size` stays 1769.
3. **Snapshot leg.** ONE direct invoke with exactly `{"amgt_scheduled_action": "refresh_freshness_snapshot"}`.

## THE BASE, read live in this session -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=` (round 78 bb-18, built at `fbb643923e`), CodeSize 42,001,525, MemorySize 1769, timeout 29, runtime python3.11, LastModified 2026-10-08T07:19:32Z, LastUpdateStatus Successful, one layer `opal-amgt-print-deps:1` (read 12:56Z and again 13:31Z, equal) | the prior artifact through the module, one `safe-apply` |
| the artifact object `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip` | VersionId `5EzlvQKaRhlENyrD6osK7pRdpfUkDTxi`, 42,001,525 B, `content-sha256` metadata `+s6R0/rc...`, LastModified 2026-10-08T07:15:07Z | copy-object of that VersionId onto the key (or `upload_verified` of the kept zip), then the `safe-apply`; never an S3 delete |
| the deployed package on this box | `C:/tmp/bb18-r78-fbb643923e.zip`, 42,001,525 B, 388 entries, 133,718,098 B unzipped. Its sha256 in base64 is `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=`, EQUAL to the live CodeSha256 (one local hash, one `get-function-configuration` read) | it IS the rollback artifact and the build's `AMGT_DEPLOYED_ZIP`: not deleted, moved or renamed by this act |
| the older package on this box | `C:/tmp/ba20-r77-14a36147bd.zip`, 41,981,131 B, sha256 in base64 `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=` (hashed) | not this act's rollback; kept |
| the role's inline policy | role `opal-amgt-scoped-api-role`, policy `opal-amgt-scoped-api-grants`: 7 statements, 33 object-read resources, 33 list prefixes, `job_record` 0 times. sha256 over sorted-keys compact JSON `6270e453570b8ea923b9a4471bbcf4d0660e73fabe8ffe920502be4442c64adb`. Saved whole: `round79/reads/ROLE_POLICY_BEFORE_20261008.json` (read 12:58Z) | the prior policy text through the `.tf` (the one list entry removed), the same `safe-apply` |
| the /freshness snapshot object | `s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`, 4,758,475 B, LastModified 2026-10-08T12:30:50Z, VersionId `05UOLBhjOKcpe7DoqAM5mOvSDP1l0m5z`, `generated_at` `2026-10-08T12:30Z`, 302 rows, 95 covered (the scheduled write of today) | copy-object from that VersionId; NEVER an S3 delete |
| the gateway route list, memory, schedule, every other IAM line | not moved: one `.tf` file differs between `fbb643923e` and the pin, by one list entry (section TERRAFORM) | none needed; a plan that shows one is a STOP |
| open NEVER-2 entries on this function | none in any live worktree's HEAD that is open in the world (section OPEN DEPLOYS) | -- |

The snapshot's VersionId moves at every scheduled write (weekdays 12:30Z). The executor reads `head-object` again immediately
before the event and records THAT VersionId as the rollback key.

**The code and the snapshot roll back TOGETHER.** A rollback of the code leaves a snapshot written by the new code: the old
code serves its moved Seeking Alpha stamps until the next scheduled write. So a rollback of the code is followed by the
copy-object of the snapshot's prior VersionId.

## THE THREE LEGS

### Leg 1: the grant

- **BEFORE (measured 12:58Z).** `.tools/aws iam get-role-policy --role-name opal-amgt-scoped-api-role --policy-name
  opal-amgt-scoped-api-grants --output json`. The role holds exactly one inline policy (`list-role-policies`), one attached
  managed policy `AWSLambdaBasicExecutionRole` (`list-attached-role-policies`), no permissions boundary, and trusts
  `lambda.amazonaws.com` only (`get-role`).
  - Statements, 7: `ReadRankedAxesAndPoints`, `ReadThePoolPrefixesTheAdapterReads`, `ListOnlyThePoolPrefixesTheAdapterReads`,
    `WriteOnlyTheFirmsOwnStarMarkers`, `ReadTheServedEtfClassificationLabels`, `ReadTheScannerSp500UniverseForCoveredNoBlock`,
    `ReadAndWriteTheFreshnessSnapshotObjectOnly`.
  - `ReadThePoolPrefixesTheAdapterReads`: action `s3:GetObject`, **33 resources**.
  - `ListOnlyThePoolPrefixesTheAdapterReads`: action `s3:ListBucket` on `arn:aws:s3:::opal-data-harvest`, **33 `s3:prefix`
    values**.
  - Both limbs equal, in order, the 33 entries of `scoped_amgt_pool_prefixes` at `fbb643923e` with `*` appended (live equals
    the last applied text).
  - Lines under any `state/` tier: one in each limb, `amgt/harvest/state/filing_attempt/*`. Lines naming Seeking Alpha: three
    in each limb (`bronze/*`, `silver/*`, `silver/article/*`).
  - sha256 `6270e453570b8ea923b9a4471bbcf4d0660e73fabe8ffe920502be4442c64adb`, EQUAL to the figure GROUP_E measured at 10:37Z.
- **AFTER (the executor reads it with the same command, after the apply, and saves it whole).** 7 statements with the same
  seven Sids and the same actions; **34 resources and 34 prefixes**. The one added line in each limb, last in its list:
  - `arn:aws:s3:::opal-data-harvest/seeking-alpha/harvest/state/job_record/*`
  - `seeking-alpha/harvest/state/job_record/*`
  The other 33 of each are byte-equal to BEFORE and in the same order; the five other statements are byte-equal; the attached
  policy list is unchanged.
  - **Expected sha256, same canonical form: `77c69f83597649427ce979e1b4dd9084bde2fcd820bf0e014c3651a8ac9f0857`.** INFERRED: the
    BEFORE document with the two lists replaced by the pin's 34 `.tf` entries in file order. A different digest with the counts
    34 and 34 is read line by line before it is called a failure (AWS may return a list in another order).
- **The prefix is builder output, not a typed string (rule 30).** Run on a `git archive` export of the pin:
  - `lib.opal_naming.address("seeking-alpha", lookup("harvest")["long"], "state", "job_record", "date=1970-01-01")` printed
    `s3://opal-data-harvest/seeking-alpha/harvest/state/job_record/date=1970-01-01`; with the partition cut:
    `seeking-alpha/harvest/state/job_record/`.
  - The generated constant `lib/research/api/_harvest_prefixes.py` `SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX` reads
    `seeking-alpha/harvest/state/job_record/`: **EQUAL**.
  - The reader's own call, `collector_read.job_record_location()`, returned `('opal-data-harvest',
    'seeking-alpha/harvest/state/job_record/')`: **EQUAL**, on the export and again on the packaged file set.
  - The `.tf` entry at the pin (`scoped-amgt-api.tf`, the last entry of `scoped_amgt_pool_prefixes`) is that string.
- **STOP list.** Any statement added or removed. Any action added. A count other than 34 and 34. An added line other than the
  two above. The tier root `seeking-alpha/harvest/state/*` in either limb. Any change in the five other statements or in the
  attached policy list. The negative arm reading anything but implicitDeny (section THE NEGATIVE ARM).
- **ROLLBACK per key.** The policy document: the saved BEFORE text, restored by removing the one list entry from the `.tf`
  and applying. An unused read-only grant left in place harms no route; it is still removed if the act rolls back.

### Leg 2: the code

- **BEFORE.** CodeSha256 `+s6R0/rc...`, artifact VersionId `5EzlvQKa...` (THE BASE).
- **AFTER.** A new CodeSha256 that DIFFERS from `+s6R0/rc...` AND EQUALS the kept zip's sha256 in base64. A new artifact
  VersionId. MemorySize 1769, timeout 29, runtime and layer unchanged.
- **STOP list.**
  - The build's gate does not exit 0, or either pip step cannot resolve from the wheel folder.
  - `r78_bb23.py --compare-zip <the kept zip>` with `R78_BB23_DEPLOYED_ZIP=C:/tmp/bb18-r78-fbb643923e.zip` reads anything but
    `EQUAL: YES`, 147 of 147.
  - The CONTENT-DIFF the build prints is not CHANGED 12, ADDED 4, REMOVED 0 with exactly the files of the two tables below.
  - Any vendored file reads CHANGED or ADDED (0 expected this round; see THE BUILD'S TERMS item 3).
  - A hookup of the section THE HOOKUPS BY NAME is missing from the built package.
  - The plan shows any resource other than the two named in TERRAFORM, or any attribute beyond those listed there.
  - The new CodeSha256 equals the old one (a 0-diff deploy).
- **ROLLBACK per key.** The function: the prior artifact (VersionId `5EzlvQKa...` copied onto the key, or `upload_verified`
  of `C:/tmp/bb18-r78-fbb643923e.zip`) through the module, one `safe-apply`, with the `.tf` list entry removed in the same
  apply. Then the snapshot's prior VersionId is copied back.

### Leg 3: the snapshot

- **BEFORE.** VersionId `05UOLBhj...` (or the one the executor reads immediately before the event), 302 rows, written by the
  old code: no row carries `seeking_alpha`; 3 rows carry the pilot's stamp of 2026-09-11.
- **AFTER, branch A (the read completes).** A new VersionId at the SAME key, 302 rows, 95 covered. Section BOTH BRANCHES.
- **AFTER, branch B (the read does not complete).** The event answers 500, NOTHING is written, the VersionId is unchanged.
- **STOP list.** Branch B: report what the event printed and stop before AC1; it is NOT a rollback of the code by itself (the
  order's rule). A new VersionId at any other key. A row count other than 302. More than one event sent (but see OPEN POINT 3).
- **ROLLBACK per key.** copy-object from the BEFORE VersionId. Never a delete.

## THE HOOKUPS BY NAME (CTO round-78 analysis R1), each read at the pin in `lib/research/api/scoped_amgt.py`

| # | hookup | where at the pin | what the route gains |
|---|---|---|---|
| 1 | `segment_served.serve_segment_table` | `read_thesis_bundle` (defined `:3630`); import inside the function `:3742`; call `:3743`: `bundle["segment_table"] = segment_served.serve_segment_table(resolved_key or security_key, fiscal_year_figures, header_figures, client=_pool_client())` | `/thesis` gains the key `segment_table`. It reads through `segment_table.read_segment_table` (cc-1's walk) and `segment_period.label_periods` |
| 2 | `dossier_sections.dossier_sections` | module import `:135`; call in the `bundle` literal of `read_thesis_bundle` `:3694` | `/thesis` gains the key `dossier_sections`, a list of five. No new store read |
| 3 | `collector_read.seeking_alpha_by_security` (with `collector_read.compact_stamp`) | `read_coverage_freshness` (defined `:5792`); import inside the function `:5800`; the ONE call `:5829`; the stamp `:5833`; `per_vendor["seekingalpha"]` `:5836`; the row field `:5891` | each /freshness row gains `seeking_alpha`. `denominators.seeking_alpha_bronze_objects_listed` and `reads.seeking_alpha_bronze` are retired; `denominators.seeking_alpha_job_record_objects_listed` (`:5908`), `denominators.seeking_alpha_states` (`:5909`) and `reads.seeking_alpha_job_record` (`:5918`) replace them. The listing of `seeking-alpha/harvest/bronze/` is no longer made |
| 4 | `page_body.PAGE_ROW_FIELDS` | `lib/research/freshness/page_body.py:10`, last entry `"seeking_alpha"` | `/freshness?view=page` rows carry `seeking_alpha` |
| 5 | `top_band.INPUT_SOURCES["seekingalpha"]` | `lib/research/api/top_band.py:34`: the read record is `seeking_alpha_job_record` | on `/overlay` and `/thesis` a failed read of the records is served as `failed`, not as `never read` |
| 6 | wording, `inputs_statement._uses` | `lib/research/api/inputs_statement.py:33`: `"the segment breakdown"` | the filings row of `/thesis` `input_provenance` says "the segment breakdown" where it said "the segment table" |
| 7 | wording, `top_band.INPUT_SOURCES["pack"]` | `lib/research/api/top_band.py:36`: `"the analysis built for this name"` (CTO msg 31722, CITED) | the pack row's `source` on `/overlay` and `/thesis` |

**A hookup missing from the built package is a STOP.** Measured on the packaged file set (136 files of the pin at their zip
names, imported with the repo root off the path, 13:09Z to 13:26Z):

- All 95 covered names' `/thesis` answer 200. `segment_table`: 76 served, 19 none (10 "No Bloomberg segment table has been
  stored for this name yet.", 9 "Bloomberg's stored table for this name has no revenue by business line."). `dossier_sections`:
  5 entries on 95 of 95; names by sections served: 42 with none, 26 with one, 10 with two, 12 with three, 2 with four, 3 with
  five.
- The pack row's source reads "the analysis built for this name" on 95 of 95. The filings row says "the segment breakdown" on
  10 of 95 and "the segment table" on 0.
- `read_coverage_freshness()`: 302 rows, complete, 6.8 seconds. `seeking_alpha_states` `{read 12, checked 13, no_record 70,
  unreadable 0}`; 112 records listed in 111 folders, 25 bodies read, 0 failed, 0 rejected, 0 capped.
- Seconds per `/thesis` on this box: minimum 3.0, median 4.3, maximum 23.1 (which request took 23.1 was not recorded).

### GROUP_D section 8, verified against the pin and restated

- **Added, verified.** `/thesis` `segment_table`: `status`, `rows`, `operating_income_rows`, `periods` (each `period`, `label`,
  `fiscal_year`, `top_level_sum`, `note`), `period_note`, `currency`, `units`, `currency_note`, `reason`, `source`. `/thesis`
  `dossier_sections`: five entries, each `field`, `heading`, `status`, `text`, `reason`, `citation`. `/freshness` and the
  stored snapshot: `rows[].seeking_alpha` (None on a row that is not covered: 207 of 207; else `state`, `sentence`,
  `last_read`, `newest_job_finished_at`, `newest_job_status`: 95 of 95), the two denominators, and the read record of 14 keys.
- **Retired, verified:** the two keys named in row 3. No file under `portal/src` reads either (CITED from GROUP_D; not
  re-searched).
- **Existing values that MOVE, measured (the stored snapshot against the pin's view):**
  - `rows[].per_input.seekingalpha` on **12 rows today** (GROUP_D counted 11; LLY_US now reads `20261008T110328Z`). Three leave
    the pilot's date: BABA_US `20260911T040221Z` to `20261006T231547Z`, BA_US `20260911T040304Z` to `20261007T013347Z`, COST_US
    `20260911T040346Z` to `20261007T112736Z`. Nine leave `NEVER`: 992_HK, AMD_US, ASML_NA, BP/_LN, GOOGL_US, HAL_US, HD_US,
    HSBA_LN, LLY_US.
  - `rows[].last_refreshed` where that stamp is the row's greatest, and on the page view the rule's outputs that follow
    (`inputs.seekingalpha`, `stale_inputs`, `stale`, `keyed_date`, `stale_reason`). The count was not isolated: a Bloomberg pull
    moved 65 rows' `pack`, `per_input.bloomberg` and `last_refreshed` between the 12:30Z snapshot and the 13:09Z read.
  - `/overlay` and `/thesis`: the Seeking Alpha row of `input_provenance` (`last_run`, `outcome`, `reason`) for the same rows.
  - `/overlay` and `/thesis`: the pack row's `source`, on every name (wording 7). GROUP_D's list predates this ruling.
  - `/thesis`: the filings row's `used_for` and `reason` (wording 6), for a name whose filing breakdown has rows.
- **GROUP_D's list of changed files is short by two round-79 files:** `lib/research/api/_harvest_prefixes.py` (cc-5) and
  `lib/research/freshness/collector_record.py` (bb-16's module, packaged for the first time). The tables below are the list.

## THE CONTENT-DIFF, measured at the pin against deployed `+s6R0/rc`

**How it was measured (no build ran).** The build script's own seed, closure and data-member code (lines 169 to 441 of
`build-and-upload-scoped-amgt.sh` at the pin, executed unchanged) was run over a `git archive` export of the pin. Its answer:
`CLOSURE: 118 entr(ies) at the fixed point after 5 pass(es) -- 43 seeded (1 handler + 42 .py under 5 seed package dir(s)), 75
added by closure`, plus 18 data members. Those 136 files were compared by content with the same paths in the deployed zip.

- The deployed zip: 388 entries = 132 repo-sourced + 256 vendored (147 under the four deployed folders, 109 from the five pure
  wheels).
- **Repo-sourced files, 136 at the pin: IDENTICAL 120, CHANGED 12, ADDED 4, REMOVED 0.** No file differs by line endings only
  (0); 5 members carry CRLF at the pin and the same 5 do in the deployed zip.
- **What `content_diff.py` should print at the build (INFERRED from the counts above):** `files 392, IDENTICAL 376, CHANGED 12,
  ADDED 4, REMOVED 0, against +s6R0/rc...`.
- Cross-check against git: `git diff --name-status fbb643923e <pin>` over the 136 paths lists 15 (12 M, 3 A). The sixteenth,
  `collector_record.py`, did not change in git: it existed at `fbb643923e` and was not packaged.
- IDENTICAL, named because round 78 moved them: the handler `lambda_function.py`, `lib/research/corpus/dossier.py`
  (`METHOD_VERSION` `"amgt-corpus-dossier/7"`), `lib/trading_calendar.py`, `lib/research/freshness/build_view.py`,
  `snapshot.py`, `stale_rule.py`, `lib/research/api/segment_period.py`. So this act moves no dossier value and adds no
  trading-calendar branch.

### CHANGED, 12 files

| file | lines +/- | who changed it | what |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | +22 / -4 | cc-6 `6f2bc69f8f` (`0.9.0_WK_AMGT_RESAPP~313`) | the adapter: hookups 1, 2 and 3 |
| `lib/research/api/inputs_statement.py` | +1 / -1 | cc-6 `6f2bc69f8f` | wording 6 |
| `lib/research/api/top_band.py` | +2 / -2 | cc-6 `6f2bc69f8f` | hookup 5 and wording 7 |
| `lib/research/freshness/page_body.py` | +1 / -1 | cc-6 `6f2bc69f8f` | hookup 4 |
| `lib/research/api/segment_table.py` | +21 / -16 | cc-1 `ceb7da64f0` (`~308`) | the reader walks the folder newest first, one body at a time, up to 20, and stops at the first table |
| `lib/research/api/_harvest_prefixes.py` | +3 / -2 | cc-5 `ddc917a52d` (`~312`) | the regenerated stamp (`REGISTRY_HASH` `0b67ab69...` to `fff9a273...`) and the one new constant; the four old prefix values are unchanged |
| **`lib/research/harvest/publication_gold.py`** | +79 / -2 | **AMGT_HARVST**: `c5eea8fc73`, `7690b9d3e0`, `0574db3e2f` (`0.9.0_WK_AMGT_HARVST~110`), `d055a9a8fa` (`~117`) | the gold BUILD's mention matcher: anchored ticker forms, the bare-name rule, the capitalised-headline rule |
| **`lib/opal_naming.py`** | +69 / -4 | **LGIC_BLANKFIX / NFRA_CTLPLN**: `cc0c2b4b5c` (`0.9.0_WK_NFRA_CTLPLN~6`), `c17998e4fb`, `736a8f8a06` (`0.9.0_WK_LGIC_BLANKFIX~1`) | a closed key set for exemption rows in `validate()`, an interval form for the cadence slot, a function-name rule in the census |
| **`org/standards/NAMING_SCHEMA.json`** | +6 / -3 | `f701d5da50`, `eb29bf7f37` (`4.0.0_SA_CRO`) | v1.15 to v1.17 |
| **`infra/logic/registry/systems.json`** | +95 / -95 | `11f54fba67`, `c09b1ad769` (`4.0.0_SA_CRO`) | service words reclassified; 41 owner fields confirmed |
| **`infra/logic/registry/resources.json`** | +0 / -6 | `17ae4222c7` (`4.0.0_SA_CRO`) | one layer row removed |
| **`infra/logic/registry/exemptions.json`** | +36 / -0 | `d5516cb074` (`4.0.0_SA_CRO`) | three scoped exemption rows |

### ADDED, 4 files

| file | cell | how it enters the artifact |
|---|---|---|
| `lib/research/api/segment_served.py` | cc-2 `f43467023f` (`~309`) | seed dir `lib/research/api`; imported by the adapter inside `read_thesis_bundle` |
| `lib/research/api/dossier_sections.py` | cc-4 `a76f6e121b` (`~311`) | seed dir; imported by the adapter at module scope |
| `lib/research/freshness/collector_read.py` | cc-3 `c68dde3c71` (`~310`) | closure: `scoped_amgt.py` imports it inside `read_coverage_freshness` |
| `lib/research/freshness/collector_record.py` | round 78 bb-16 (unchanged since) | closure: `collector_read.py` imports it at module scope |

- **Size (INFERRED: pin repo files + the deployed zip's vendored files, the layer figure from the script):** 3,645,147 B +
  130,126,155 B = 133,771,302 B, + layer 121,743,633 B = **255,514,935 B against 262,144,000 B (97.5%, 6,629,065 B spare)**. The
  deployed package is 133,718,098 B unzipped, so the round adds 53,204 B.
- **Any file outside the two tables is a STOP.**

### SIX FILES FROM OTHER PROJECTS RIDE THIS ARTIFACT (6 of 12 CHANGED; 0 of 4 ADDED)

Each is read here for what it can change on a served route.

1. **The five files of the round-78 trunk merge** (`lib/opal_naming.py`, `NAMING_SCHEMA.json`, `systems.json`,
   `resources.json`, `exemptions.json`). The round-78 CTO half's C1 and the drain packet's item 5 left them to this half.
   - Measured: at the pin all five equal `f6cff376d1`'s (0 diff lines), and their line counts equal the table in round 78's
     half. The deployed zip holds the `fbb643923e` versions. So the live code is behind by exactly these five and no more.
   - **Two of the five must ride together.** The pin's `opal_naming._Vocab` reads `schema["cadence"]["interval_form"]`; the
     deployed schema (v1.15) has no such key and the pin's (v1.17) has. Both are in this artifact. A build that took one
     without the other would raise when the vocabulary is built.
   - `REGISTRY_FILES` names an eighth file, `legacy_addresses.json`, which the build does not package (as in round 78); the
     module reads its absence as None.
   - **Exercised on the packaged file set** (seven registry files present, the eighth absent): the registry loads;
     `snapshot.snapshot_address()` reads `s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`,
     EQUAL to the key the live function writes today; `collector_read.job_record_location()` reads the builder's prefix; the
     four old generated prefixes are unchanged. So the snapshot event writes the same key.
   - `validate()`, `grade()`, `name()`, `legacy_address()` and the census are called by 0 of the 118 code members outside
     `opal_naming.py` (two text reads of the packaged set: `opal_naming.` and the alias `naming.` before each of those names).
2. **`lib/research/harvest/publication_gold.py` (AMGT_HARVST).** Every changed line is inside `_security_mentions` or is one of
   its two new helpers. `_security_mentions` is called at `publication_gold.py:444` only, in the gold build. The routes call
   `_latest_gold_snapshot_rows_cached` and `_day_of` (`scoped_amgt.py:5385`, `:6505`, `:6507`, `:6549`, `:6669`;
   `monthly_chatter.py:205`), which did not change. No served value moves by this file; the gold tables move when AMGT_HARVST
   rebuilds them, under that project's own pair.

## DATA FILES

- `DATA_MEMBERS` at the pin: 18, the same 18 arcnames as the deployed zip.
- `lib/research/freshness/seeking_alpha_job_record.schema.json` is NOT packaged, and no packaged module opens it:
  `collector_record.py` and `collector_read.py` were read whole and name it in docstrings only.
- `rot_signal.json`: as round 78 ruled. Not packaged; no route opens it.

## BUILT AND NOT SERVED: nothing new; three leftovers named

- The two modules round 78 packaged with no reader are now read: `segment_table.py` and `segment_period.py` are imported by
  `segment_served.py:12`. `collector_record.py` is imported by `collector_read.py:15`.
- Left with no caller, on purpose (cc-6 hookup 3g): `_seeking_alpha_bronze_stamps` (`scoped_amgt.py:5675`), its table tuple
  and `SEEKING_ALPHA_BRONZE_PREFIX`. The role keeps its read grant on `seeking-alpha/harvest/bronze/`; no route lists it now.
- The generated constant `SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX` has no runtime reader: the reader calls the builder.

## THE BUILD'S TERMS (carried from round 78; the build scripts did not change)

`build-and-upload-scoped-amgt.sh`, `vendor_from_deployed.py`, `content_diff.py` and `upload_verified.sh`: 0 diff lines between
`fbb643923e` and the pin. The script's lines read at the pin: 127 (the gate), 134 to 140 (the deployed zip and its hash), 154
to 156 and 592 to 593 (the two pip downloads), 761 (`content_diff.py`). The script was not run.

1. **`AMGT_DEPLOYED_ZIP=C:/tmp/bb18-r78-fbb643923e.zip`.** Its hash equals the live CodeSha256 (THE BASE). The build reads the
   live hash again and stops on a mismatch.
2. **`PIP_NO_INDEX=1`, `PIP_FIND_LINKS=C:/tmp/bb18-wheels`, `PIP_LOG=<a file the executor attaches>`.** The folder holds six
   files; **6 of 6 sha256 equal** `round78/BB18_WHEEL_FOLDER_SHA256_20261008.txt` (re-hashed 12:55Z). `python` here is 3.14.7,
   which the sixth wheel (`cp314 win_amd64`) fits.
3. **No vendored file is expected to read CHANGED.** The five pure wheels' members after the script's prune: 109, byte-equal to
   the deployed zip's 109 pure-wheel files, **109 of 109**. Round 78's exception for three `RECORD` files no longer applies:
   the deployed zip was built from these wheels. Any vendored CHANGED or ADDED line is a STOP.
4. **The gate.** `gen_harvest_prefixes.py --check` run on the `git archive` export of the pin: `OK: ... matches fresh
   lib.opal_naming output byte for byte (registry hash fff9a273...)`, exit 0.
5. **`content_diff.py` downloads the deployed package from AWS** at the build. The CTO ruled in round 78 that it stays (CITED:
   `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_R78_BB18_REDEPLOY_20261007.md`, "It stays", one term: the
   downloaded bytes hash to the live CodeSha256 and the record states it beside the kept zip's).
6. **The built zip is kept.** Build `--build-only <a kept path>` and upload THAT file. After the apply its sha256 in base64
   equals the new live CodeSha256 and it is the next build's `AMGT_DEPLOYED_ZIP`. `C:/tmp/bb18-r78-fbb643923e.zip` is ALSO
   kept: it is this act's rollback artifact, and the deployed zip again after a rollback.

## TERRAFORM: two resources may move, and no plan was run

`git diff --stat fbb643923e <pin> -- infra/aws/terraform/harvest/`: 2 files changed, 11 insertions, 3 deletions.

| file | commit | a `.tf` file? |
|---|---|---|
| `scoped-amgt-api.tf` (+7) | cc-5 `ddc917a52d` | **yes: ONE list entry and six comment lines**, at the end of `scoped_amgt_pool_prefixes` |
| `gen_harvest_prefixes.py` (+4 / -3) | cc-5 `ddc917a52d` | no |

The module `modules/yang-lambda/` did not change. A new module `modules/opal_name/` appeared between the two commits; this
root names it 0 times.

**The expected UNTARGETED plan: exactly two in-place updates and nothing else.**

1. `aws_iam_role_policy.scoped_amgt_api_grants` (`scoped-amgt-api.tf:298`): the policy document gains one resource in
   `ReadThePoolPrefixesTheAdapterReads` and one `s3:prefix` value in `ListOnlyThePoolPrefixesTheAdapterReads`.
2. `module.scoped_amgt_api.aws_lambda_function.this` (`scoped-amgt-api.tf:453`, `modules/yang-lambda/main.tf:23`):
   `source_code_hash` (`+s6R0/rc...` to the kept zip's), `s3_object_version` (`5EzlvQKa...` to the new one) and
   `last_modified`. It appears only after the new artifact is uploaded: the module reads the artifact object's `version_id`
   and its `content-sha256` metadata.

Anything else is a STOP before the apply. **No plan was run in this session.** Standing drift in this root would show as a
third resource, or as an attribute of one of the two beyond those listed: a route or integration, the schedule or its role,
the layer version, a table, a bucket, the function's memory, timeout, environment or tags. The live policy equals the last
applied text (Leg 1), which is the one drift read this session made.

## THE NEGATIVE ARM (CTO msg 31672 and its confirmation msg 31706, CITED)

**The question.** After the apply, is the grant exactly the builder's table prefix and nothing wider under
`seeking-alpha/harvest/state/`?

**Why a simulation.** The role trusts `lambda.amazonaws.com` only, so the executor cannot read AS the role without new code or
a new permission. `iam simulate-principal-policy` evaluates the role's own policies and is a read. What it does not see was
measured: the bucket `opal-data-harvest` has no bucket policy (`NoSuchBucketPolicy`) and the role has no permissions boundary.
An organisation-level policy was not read.

**The sibling.** The state tier holds ONE child today, `job_record/`, and no object of its own (one delimiter listing). So
the arm uses two addresses that need no object to exist: the tier root itself, and a sibling table the BUILDER names:
`address("seeking-alpha", "harvest", "state", "filing_attempt", "date=1970-01-01")` printed
`s3://opal-data-harvest/seeking-alpha/harvest/state/filing_attempt/date=1970-01-01`.

**The commands** (each run from the repo root; one resource per call; `R=arn:aws:iam::313476888478:role/opal-amgt-scoped-api-role`,
`B=arn:aws:s3:::opal-data-harvest`, `Q='EvaluationResults[].[EvalActionName,EvalResourceName,EvalDecision]'`):

```
# C0 control, a prefix granted before and after
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:GetObject --resource-arns "$B/seeking-alpha/harvest/bronze/probe.json" --query "$Q" --output text
# C1 control
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:ListBucket --resource-arns "$B" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=seeking-alpha/harvest/bronze/,ContextKeyType=string" --query "$Q" --output text
# P1 positive arm, the object read
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:GetObject --resource-arns "$B/seeking-alpha/harvest/state/job_record/security_key=PROBE_US_Equity/probe.json" --query "$Q" --output text
# P2 positive arm, the listing
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:ListBucket --resource-arns "$B" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=seeking-alpha/harvest/state/job_record/,ContextKeyType=string" --query "$Q" --output text
# N1 NEGATIVE ARM, an object under the sibling table
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:GetObject --resource-arns "$B/seeking-alpha/harvest/state/filing_attempt/date=1970-01-01/probe.json" --query "$Q" --output text
# N2 NEGATIVE ARM, a listing of the tier root (the arm that tells narrow from wide)
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:ListBucket --resource-arns "$B" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=seeking-alpha/harvest/state/,ContextKeyType=string" --query "$Q" --output text
# N3 NEGATIVE ARM, a listing of the sibling table
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:ListBucket --resource-arns "$B" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=seeking-alpha/harvest/state/filing_attempt/,ContextKeyType=string" --query "$Q" --output text
# N4 the grant is read-only
.tools/aws iam simulate-principal-policy --policy-source-arn $R --action-names s3:PutObject s3:DeleteObject --resource-arns "$B/seeking-alpha/harvest/state/job_record/security_key=PROBE_US_Equity/probe.json" --query "$Q" --output text
```

The repo's hook routes a raw IAM read to `comp-iam`; each command carries a trailing `# rail-checked: <why>` marker, as this
session's did (`comp-iam` reconciles text against live and does not answer one action on one resource).

| arm | BEFORE, run 2026-10-08T13:01:34Z (rc 0 on all eight) | the pass AFTER the apply |
|---|---|---|
| C0 GetObject under `seeking-alpha/harvest/bronze/` | allowed | allowed |
| C1 ListBucket, prefix `seeking-alpha/harvest/bronze/` | allowed | allowed |
| P1 GetObject under `job_record/` | implicitDeny | **allowed** |
| P2 ListBucket, prefix `seeking-alpha/harvest/state/job_record/` | implicitDeny | **allowed** |
| N1 GetObject under the sibling `filing_attempt/` | implicitDeny | **implicitDeny** |
| N2 ListBucket, prefix `seeking-alpha/harvest/state/` | implicitDeny | **implicitDeny** |
| N3 ListBucket, prefix `seeking-alpha/harvest/state/filing_attempt/` | implicitDeny | **implicitDeny** |
| N4 PutObject and DeleteObject under `job_record/` | implicitDeny, implicitDeny | **implicitDeny, implicitDeny** |

- The pair discriminates because P1 and P2 move and N1 to N4 do not. C0 and C1 show a deny is the policy's answer and not a
  failed call. An `allowed` on N1, N2 or N3 means the grant is the tier and not the table: STOP and roll the grant back.
- **The positive arm in the world** (the simulation is not the function): the snapshot written in branch A carries
  `reads.seeking_alpha_job_record.read_completed` true with `objects_listed` 112 or more and `bodies_failed` empty.
- **The negative arm has no arm in the world.** The function never reads a sibling prefix, so a refused read by the function
  itself cannot be produced without code. The simulation is the whole of it. Stated, not hidden.
- Also simulated at 13:14Z, for the segment hookup: GetObject under `bloomberg/harvest/bronze/segments/` and ListBucket with
  that folder's prefix both read `allowed` today. Hookups 1 and 2 need no grant.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The role's inline policy: N = 1 writer,** `aws_iam_role_policy.scoped_amgt_api_grants` in this root. The live text
  equals the last applied text.
- **The snapshot object: N = 1 writer,** `write_freshness_snapshot` (`lib/research/freshness/snapshot.py:52`), reached only
  through `refresh_freshness_snapshot` (`scoped_amgt.py:5969`), reached only through the scheduled action (`:6813` to `:6834`).
  - Counted by a text read of every `.py` in the repo for the two names followed by `(`: 9 hits in 4 files. Outside the
    test file (4) and this round's check (1) they are the two definitions and the two calls, `scoped_amgt.py:5976` and
    `:6828`.
  - It has TWO triggers: the schedule `amgt-global-freshness-snapshot-daily`, `cron(30 12 ? * MON-FRI *)` UTC
    (`freshness-snapshot-schedule.tf:101` to `:118`), and a direct invoke by hand (this act's one event). The object's four
    newest versions match that: 2026-10-08T12:30:50Z and 2026-10-07T12:30:47Z (scheduled), 2026-10-08T07:24:00Z and
    2026-10-07T04:51:31Z (the events of rounds 78 and 77).
  - The role holds PutObject on that one key only. Whether another principal can write the key was not read.
  - Its key is `lib.opal_naming.address()` output, from a file this act changes: computed on the packaged file set and EQUAL.
- **The job records the new read consumes: not this project's.** AMGT_HARVST's collector writes them; this role cannot (N4).
- **Served bodies:** the section THE HOOKUPS BY NAME.

## BOTH BRANCHES OF THE SNAPSHOT LEG, read from the producer's own rule at the pin

**The rule.**
- `refresh_freshness_snapshot` (`scoped_amgt.py:5969`) calls `write_freshness_snapshot` and never raises.
- `write_freshness_snapshot` (`snapshot.py:52`) builds the view and asks `_freshness_complete`; if that is false it returns
  `written: False` with the reason "a store read did not finish, so the snapshot was left as it was", and makes NO put.
- `_freshness_complete` (`scoped_amgt.py:5930`) is false when `denominators.covered_read_error` is set or when ANY record
  under `reads` carries `read_completed` false. Hookup 3 puts the reader's record there.
- The reader (`collector_read.py`) never raises. A failed address, a failed listing, or ONE record body whose fetch raises
  gives `read_completed` false (`:190`). A body that is not JSON or is off contract is `rejected`, not failed, and does not
  stop the write. It reads at most 5 records per covered name, 16 at a time, with no retry.
- The scheduled action answers 200 with `object`, `generated_at`, `rows`, `etag` when written, and 500 with `error` and
  `object` when not (`:6828` to `:6834`).

**Branch A: the read completes.**
- The event answers 200 with `rows` 302. A new VersionId at the same key.
- Expected content (measured on the packaged file set at 13:09Z; the counts move as the collector runs): 95 covered rows
  with `seeking_alpha`, 207 uncovered rows with None; `seeking_alpha_states` near `{read 12, checked 13, no_record 70,
  unreadable 0}` summing to 95; `seeking_alpha_job_record_objects_listed` 112 or more; no row dated 2026-09-11. The object is
  about 1,063,343 B.
- The page then shows a Seeking Alpha state and sentence on every covered row once a page cell draws it; 992_HK_Equity reads
  stale on a 2026-09-22 stamp; BABA_US, BA_US and COST_US no longer read stale on the pilot's date.
- The executor reads the stamp, then runs AC1. **The function holds a view for 60 seconds** (`FRESHNESS_TTL`,
  `served_cache.POINTER_TTL = 60.0`): a container that answered a freshness, overlay or thesis request inside the last minute
  still serves the old snapshot. `r79_cc6.py` prints the stamp of the view that answered; if it is the old one, wait 65
  seconds and run again. That is not a failure.

**Branch B: the read does not complete** (the grant has not reached the function, or one record body failed to fetch).
- The event answers 500 with "a store read did not finish, so the snapshot was left as it was". NOTHING is written. The old
  snapshot keeps serving.
- The page shows what it shows now: no Seeking Alpha state on any row, the pilot's 2026-09-11 on three rows. The thesis
  already serves `segment_table`, `dossier_sections` and the two wordings: none of them needs the snapshot.
- The executor reports the event's body, runs P1 and P2 of the negative-arm table, and stops before AC1. If P1 and P2 read
  `allowed`, one record body failed: OPEN POINT 3 asks whether one more event may be sent.

**The window between the code and the snapshot, in either branch.** Measured on the packaged file set against the live
snapshot: the new code serves the OLD snapshot without error. `/freshness?view=page` answers 200 with 95 rows, 0 carrying
`seeking_alpha`; BA_US's `/thesis` Seeking Alpha row still reads `20260911T040304Z`, `landed`. The old snapshot has no
`reads.seeking_alpha_job_record`, which `top_band` reads as "the store answered".

**THE MOST IMPORTANT BRANCH: the code lands and the grant does not.**
- **Is the window real in ONE apply? Yes.** The module takes the role's ARN (`role_arn = aws_iam_role.scoped_amgt_api.arn`,
  `scoped-amgt-api.tf:457`) and the file holds 0 `depends_on` lines, so Terraform holds no order between the policy and the
  function. Either can land first, and either can fail alone. IAM changes also take seconds to reach a caller (INFERRED:
  AWS's stated behaviour, not measured).
- **On served routes, at once: nothing.** The job records are read by `read_coverage_freshness` only. Its callers are the
  snapshot build (`snapshot.py:47`) and the fallback of `serve_coverage_freshness` (`scoped_amgt.py:5959`), which runs only
  when no stored snapshot under 24 hours old can be read. Hookups 1, 2, 4, 6 and 7 serve normally.
- **The snapshot event and every scheduled fire: branch B.** No snapshot is written by the new code.
- **When the stored snapshot passes 24 hours.** Its stamp is `2026-10-08T12:30Z`; `read_freshness_snapshot` refuses it when
  its age exceeds 24.0 hours, so from **2026-10-09T12:30Z** it is not served (a later scheduled write by the OLD code, if the
  act runs after one, moves that time). From then EVERY `/freshness`, `/overlay` and `/thesis` request builds the view. The
  view is incomplete, and an incomplete view is never held (`:5964`), so the next request builds it again. One build took 6.8
  seconds on this box with the read succeeding and 9.9 seconds at GROUP_D's draft (CITED); the function's ceiling is 29 seconds.
  Every covered row then reads `seeking_alpha.state` `unreadable`, and the Seeking Alpha row of the statement of inputs reads
  `failed`.
- **What the executor does.** A half-landed apply is not left (NEVER-2). Read the policy; if it is still the BEFORE text,
  apply again (the plan then shows the policy alone). If the grant cannot land before the snapshot's 24 hours end, roll the
  code back. The reverse half (the grant lands, the code does not) harms no route: finish or roll back.
- **A property that stays after a good deploy.** A scheduled fire whose record read fails writes nothing, and the snapshot
  it would have replaced is 24 hours old at that minute. Requests then build the view; when the read succeeds the view is
  complete and held for 60 seconds per container. The same was true of every other store the view lists; this round adds
  one listing and up to 475 record reads to the set that must all succeed. The schedule runs on weekdays, so from Saturday
  12:30Z to Monday 12:30Z the route runs on that fallback today already (INFERRED from the cron and the 24-hour rule).

## EARLIER-ROUND PINS (order AC2 and AC3): what each reads, BEFORE and AFTER

BEFORE is `--where deployed` against the live function `+s6R0/rc`, run in this session (GET-shaped invokes, read only). The
AFTER prediction is `--where local` on the shared tree. Every local run in the table ended by 13:19Z, before the other seat's
merge was laid into the tree at 13:27:23Z; the tree's packaged files equalled the pin then (0 dirty paths read at 13:12Z).
One run came after it: the second c59 deployed run (13:28Z), whose local half read a tree with the two staged files.

| check | BEFORE (deployed) | predicted AFTER (local on the tree) | can a round-79 change move it? |
|---|---|---|---|
| `r76_served.py --cell c62` | YES: 95 names, 93 items (13:07Z) | YES: 95 names, 93 items | no: it reads `top_band` only |
| `r76_served.py --cell c63` | YES: 0 entries disagreeing (13:09Z) | YES: 0 entries disagreeing | it reads each `/overlay` `input_provenance.last_run` against the same function's `/freshness` row. Both come from one view, so the moved Seeking Alpha values agree in either branch. It requires only that `source` is not empty: the reworded pack source passes |
| `r75_served.py --cell c59` | **NO**: C1 0 of 302 rows equal; C2 PASS (33 cold of 40, all inside the 2,000 ms bar); C3 PASS 1,853 ms (13:28Z, nothing else running) | local C1 YES, 302 of 302 (the builder against the view, both on the tree) | **YES. See below** |
| `r78_deployed.py` (3 lines) | YES 3 of 3 (13:10Z) | line 1 local YES, 6 of 6. Lines 2 and 3 have no local mode; the packaged-set read of all 95 `/thesis` answers 200 on 95 of 95 | no: line 1 reads the six round-78 hookups; line 2 reads `segment_breakdown.reason` BY KEY; line 3 reads the model block and the drafted sections. None reads the phrase, the pack source or a retired field |
| `r77_served_shape.py` | YES, 6 of 6 clauses (13:06Z) | **NO: C5 FAILS** (13:06Z) | **YES. See below** |

**`r77_served_shape.py` clause C5 WILL READ NO after a correct deploy. This is the most important finding of the half.**
- The check's `_segments()` walks the `/thesis` body and returns the first object holding `rows`, `source` and `reason`. It
  takes the last-added keys first. `segment_table` holds those three keys in every status (`segment_served.py`) and is added
  directly after `segment_breakdown` (95 of 95 bodies on the packaged file set), so the walk now returns `segment_table`.
- Measured on the tree: `ASML NA: ... segment rows 12 reason 'None'` and `BA: ... segment rows 0`, `FAIL C5`, `R77 SERVED
  SHAPE: NO`, exit 1. On the deployed function now: `ASML NA ... segment rows 0 reason "The filing text kept here is about
  the company's share capital ..."` and `BA: ... segment rows 11`, PASS.
- **No served value regressed.** Read by key on the packaged file set: `segment_breakdown` has 0 rows for ASML_NA and 11 for
  BA_US, as before. The 12 and the 0 are the Bloomberg table's (`segment_table` served for ASML_NA; none stored for BA_US).
- **What the half must state:** AC3's second command exits 1 after the deploy for this reason and no other, unless the check
  is amended first. OPEN POINT 1.
- cc-6's AC2 did not catch it: it runs `r78_bb17.py --crit AC1`, which does not run this check.

**`r75_served.py --cell c59` reads NO now and is time-sensitive after.**
- Its deployed C1 compares the rows the function serves from the stored snapshot with a view worked out on the executor's
  box at that minute, on every field but `rot`.
- Now: 0 of 302 equal, because the tree's view carries `seeking_alpha` on every row and the stored snapshot does not. The
  order's issuer notes cite AC2's pins "as round 78's bb-18 read them"; that reading predates cc-6's drain.
- After branch A: equal only if no store moved between the snapshot event and the check. Two stores move on their own. A
  Bloomberg pull changed `pack`, `per_input.bloomberg` and `last_refreshed` on 65 rows between the 12:30Z snapshot and a
  13:09Z read (stamps `20261008T1300..Z` onward). The collector's records move at any hour: the rows reading `read` went from
  11 at GROUP_D's draft (about 10:5xZ) to 12 at 13:09Z, and today's newest last-read stamps are 02:45Z, 03:05Z, 03:23Z, 11:03Z.
- After branch B: NO, 0 of 302. The order stops before AC1 in that branch, so AC2 is not reached.
- The executor's tree must hold the pin's packaged files when it runs c59. The shared tree will not once the merge in
  progress lands (two packaged files). OPEN POINT 11.
- C3 is an end-to-end time on the executor's box with a bar of 2,000 ms: 1,853 ms alone and 2,442 ms while this session ran
  other checks beside it (the function's own duration was 244 ms and 158 ms in those two runs, so the rest is the box and the
  4.7 MB body). The served body shrinks after branch A.
- OPEN POINT 2.

## EXPECTED OUTCOMES (both branches)

| check | before (`+s6R0/rc`) | expected after | if not |
|---|---|---|---|
| the build's gate | exit 0 on the pin export | exit 0 | STOP before packaging |
| `--compare-zip` | -- | EQUAL: YES, 147 of 147 | STOP before the upload |
| the CONTENT-DIFF the build prints | -- | CHANGED 12, ADDED 4, REMOVED 0, exactly the two tables; 0 vendored lines | STOP before the upload |
| the plan | -- | exactly the two in-place updates of TERRAFORM | STOP before the apply |
| the policy | 33 and 33, sha `6270e453...` | 34 and 34, the two added lines, sha `77c69f83...` (INFERRED) | STOP; roll the grant back |
| the negative arm | P1, P2, N1 to N4 implicitDeny; C0, C1 allowed | P1, P2 allowed; N1 to N4 implicitDeny; C0, C1 allowed | N allowed: STOP and roll back. P denied: wait and read again before the event |
| new CodeSha256 | `+s6R0/rc...` | differs AND equals the kept zip's | unchanged: a 0-diff deploy, STOP |
| the snapshot event | VersionId `05UOLBhj...`, 4,758,475 B, 302 rows | branch A: 200, a new VersionId, 302 rows, about 1,063,343 B. Branch B: 500, nothing written | branch B: report and stop before AC1 |
| AC1 `r79_deployed.py` (the one line of the section below) | NO: H1 to H4, H5a to H5d and K1 all FAIL (13:07Z) | YES 1 of 1, after branch A and the 60-second hold | rollback trigger |
| AC2 c62, c63 | YES, YES | YES, YES | rollback trigger |
| AC2 c59 | NO (C1) | YES only as OPEN POINT 2 states | per OPEN POINT 2; UNMEASURED (exit 2) is reported, not a rollback |
| AC3 `r78_deployed.py` | YES 3 of 3 | YES 3 of 3 | rollback trigger |
| AC3 `r77_served_shape.py` | YES | **NO at C5 unless the check is amended** (OPEN POINT 1) | per OPEN POINT 1 |
| cold read (leadpanel `after`) | -- | reported; the adapter gains one module-scope import of a small pure module (`dossier_sections`: `copy`, `re`) | not a rollback |

**Not proven by this act:**
- The gateway: every check invokes the function directly. The walk (cc-8) is the first read through the edge.
- The two wordings and hookup 5 have no deployed check (next section).
- `/thesis` time in the function with the new listing and up to 20 segment bodies: local figures only.

## THE LINES OF `round79/checks/r79_deployed_cells.txt` (PROPOSED; the file is not written by this draft)

The format is round 78's: one shell command per line, run from the repo root with `PYTHONPATH` set to it; `#` lines are
comments; a command passes on exit 0; an empty list reads NO CELLS LISTED (exit 2). `r79_deployed.py` allows 1,500 s a line.

Of the seven `r79_cc*.py` checks, ONE accepts `--where deployed` (read from each script's argparse): `r79_cc6.py`.
`r79_cc1.py`, `r79_cc2.py`, `r79_cc3.py` and `r79_cc4.py` take `--where local` only; `r79_cc5.py` takes no `--where` (it reads
text); `r79_cc8.py` is the walk's.

```
# AMGT_RESAPP round 79 -- the deployed checks AMGT-cc-7's AC1 runs (r79_deployed.py). ONE line; filled by the issuer at the signing of the COO half.
# It FAILS against the deployed BASE +s6R0/rc (H1-H4, H5a-H5d, K1; 2026-10-08 13:07Z). H5 and K1 read the stored snapshot: run it AFTER the snapshot event, and 65 s after it.
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc6.py --crit AC1 --where deployed
```

- **The line grades every served hookup of the round:** H1 and H2 the segment table (cc-2, through cc-1's walk: AMD_US,
  8766_JP, HD_US), H3 and H4 the five sections (cc-4: ASML_NA, AMD_US), H5a to H5d the Seeking Alpha column on the page view
  (cc-3 and hookup 4), K1 the default body's added and retired fields.
- **Should `r79_cc2.py`, `r79_cc3.py`, `r79_cc4.py` be listed? No.** None has a deployed mode; listed as they are they would
  grade the tree, not the function, and a tree check in a deployed list reads YES before the deploy. Their served arms are
  H1 to H5 of the one line.
- **The count the GO states: 1.**
- The line's names are pinned to today's stores (GROUP_D section 7): HD_US_Equity holds no segment folder, AMD_US_Equity holds
  notes with none of the five sections, 95 covered names. `--where deployed` does not accept `unreadable`.
- **Served changes with no line:** wording 6, wording 7 and hookup 5. The issuer reads the first two by hand after the apply:
  `/thesis` for `HD_US_Equity`, `input_provenance`: the filings row's `used_for` holds "the segment breakdown" and the pack
  row's `source` is "the analysis built for this name" (both measured on the packaged file set). Hookup 5 shows only when
  the record read fails; its only exercise is cc-6's plant test.
- The breadth read (every covered `/thesis` answers 200) is AC3's `r78_deployed.py` lines 2 and 3.

## OPEN DEPLOYS (every live worktree read, 13:10Z)

`git worktree list --porcelain`: **83 worktrees, 83 answered `ls-tree`, 0 errors, 0 with an empty folder.** Entries per tree: 17
to 26 (1,653 in all); **68 distinct entry files in the union, 88 distinct blobs.** Every one of the 88 blobs was text-read for
`opal-amgt-scoped-api`, `terraform/harvest`, `scoped_amgt`, `scoped-amgt`, `cc-7` and `bb-18`. The shared tree's HEAD holds 20
entries (24 files on disk, `.unindexed_red_state.json` among them, read with `ls -a`).

| entry | where | what it is to this act |
|---|---|---|
| `amgt-resapp-r77-ba20.json` | 2 stale worktrees; absent from the shared tree's HEAD | names this function. World-done: the live CodeSha256 is a LATER build (`+s6R0/rc`, round 78). Nothing to re-execute |
| `amgt-resapp-r76-az5.json`, `amgt-resapp-r74-ax5.json` | 1 stale worktree each; absent from the shared tree's HEAD | name this function. Superseded by two and four later deploys of it |
| `amgt-resapp-r78-bb18.json` | 0 trees | opened at `98d018e6bf`, closed and removed at `20905e0ff1` (`0.7.0_AE_CloudOps~A`) |
| `amgt-corpus-r40-ap10d.json`, `amgt-corpus-r40-ap10d2.json`, `harvst-gold-rebuild8-m-20261007.json` | 7, 2 and 3 trees; none in the shared tree's HEAD | other projects' acts whose text cites round 78's bb-18. Not this function's entries |
| `harvst-sa-job-record-m-20261007.json` | 10 trees; not in the shared tree's HEAD | AMGT_HARVST's writer of the records this round reads. It names none of the six tokens. Its closing commit was not read |
| `amgt-corpus-r40-ap10m.json` | the shared tree and 18 others | AMGT_CORPUS's induction re-pin; names none of the six tokens |
| `amgt-resapp-r56-af6-price-cutover.json` | 16 stale trees | a box-side act for the price producer, not this function |

**No entry in any tree names `cc-7`, and none is open in the world on `opal-amgt-scoped-api` or on
`infra/aws/terraform/harvest/`.** The executor reads the trees again before acting.

## SOURCE MAP (row AMGT_RESAPP-Z-S370)

`infra/aws/lambda/ci/lambda-source-map.json`, entry `functions.opal-amgt-scoped-api`, key `_artifact_note`, reads today:

> "NOT YET UPLOADED. No artifact exists at the key above and no terraform apply has been run: AMGT-rf-2 is a source-plane cell
> and its issuer ruled explicitly that no world act is to be taken."

That is false: the artifact exists (VersionId `5EzlvQKa...`) and the function has been applied many times. After this act it
should say what is true and stays true, for example:

> "UPLOADED AND APPLIED. The artifact at the key above is built by infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh
> (the closure of lambda_function.py plus vendored packages, never source_dir alone) and applied through safe-apply on
> infra/aws/terraform/harvest/. The live hash is read with lambda get-function-configuration, never from this note. Last
> corrected by AMGT_RESAPP round 79, cell AMGT-cc-7."

The note should name no hash and no VersionId: both change at every deploy, and a stale value in a note is how this row arose.
The same entry's `_note` says the function serves "the eleven" routes; the handler's docstring at the pin says sixteen
(`scoped_amgt.py:6840`). That is a second stale figure in the entry, outside the order's sentence.

## OPEN POINTS FOR THE ISSUER

1. **`r77_served_shape.py` C5 will read NO, so AC3 exits 1 after a correct deploy.**
   Recommendation: amend the check before the GO. `_segments()` returns `bundle.get("segment_breakdown")` when that key is an
   object, and walks only when it is absent. Dry-run it both ways before signing: deployed base YES, local YES. The issuer
   amends its own criterion and says in the commit which gate limb graded it. The alternative, a sentence in the pair saying
   "AC3's second command reads NO at C5 only", leaves a criterion whose exit is 1 on success; not recommended.
2. **`r75 c59` C1 is a race against two stores after the deploy.**
   Recommendation: the pair says c59 is run within minutes of the snapshot event, with nothing else running on the box, and
   not while a Bloomberg pull is writing (today 13:00Z to about 13:15Z). A C1 difference confined to rows whose store object
   is newer than the snapshot's `generated_at` is not a rollback trigger: the executor prints the differing rows and their
   stamps and stops for the issuer.
3. **May the executor send the event a second time?** The order says once. One failed record body in 25 (up to 475) leaves
   branch B with the grant in place, and a c59 race is cured by a fresh snapshot.
   Recommendation: the pair allows ONE more event, only when P1 and P2 read `allowed`, each event's body and VersionId
   recorded. Each event is one write of one key by its one writer.
4. **ONE apply, or the grant first?** One apply is what the order says and it carries the window of BOTH BRANCHES. The grant
   can go first with no targeting: apply BEFORE the upload (the plan then shows the policy alone), read the AFTER and the
   negative arm, then upload and apply again (the plan then shows the function alone). That costs a second apply and an
   amendment to the order.
   Recommendation: keep ONE apply, on three conditions the pair states. (a) The apply completes with the stored snapshot
   under 24 hours old and hours to spare (it does until 2026-10-09T12:30Z, and again after each scheduled write). (b) The
   policy's AFTER read and the negative-arm table come BEFORE the snapshot event. (c) A half-landed apply is finished or
   rolled back before the snapshot's 24 hours end. If the CTO half wants no window at all, the grant goes first as above.
5. **The deployed list is ONE line and the GO states 1.** Recommendation: as proposed, with the two hand reads of the
   wordings in the issuer's one real run.
6. **The 60-second hold.** Recommendation: the GO tells the executor to wait 65 seconds after the event before AC1, and to
   read the stamp H5 prints.
7. **Six riders from other projects.** Recommendation: ACCEPT on the measurements above, and name them in the message that
   carries this half so the CTO half covers them: the five trunk-merge files (the round-78 C1 debt, now paid) and
   `publication_gold.py`.
8. **One failed record body refuses the whole snapshot, with no retry.** It is the rule as built and as cc-3's order wrote it.
   Recommendation: accept for this round; file a surprise row for the round-80 analysis (a reader that retries a body once,
   or a snapshot that records the failed names and is still written, is a design change and not this act's).
9. **The source-map note.** Recommendation: the text of the section SOURCE MAP, with no hash in it; the route count in `_note`
   is a separate row.
10. **The order's preflight line on `comp-iam`** says no `simulate-principal-policy` call was made at the cut. This session
    made ten (the table above and the two segment reads). Recommendation: cite this half in the GO in place of that line.
11. **The criteria run from the shared tree, and the shared tree is about to leave the pin.** AC1 to AC3 start with `cd "$(git
    rev-parse --show-toplevel)"` and several import `lib` from there (c59 works out a whole view on it). After the merge in
    progress lands, `lib/opal_naming.py` and `exemptions.json` there differ from the pin and from the deployed package.
    Recommendation: the issuer reads the landed diff of those two files before the GO. If it is the staged one (the census
    and its command line, and exemption rows; no line of `address()`, `key()` or `lookup()`), the pair says so in one
    sentence and the criteria run on the shared tree as written. If it is anything else, c59 is run from a tree at the pin.
    The two files ride a LATER redeploy under their own measurement, as round 78's five did.

## NOT MEASURED

- **The build itself.** No zip was made. The closure is the script's own code run over the pin's files; the vendored half,
  the verify, the isolated-runtime step and the size step were not run. The size line and the `files 392` line are INFERRED.
- **pip under `PIP_NO_INDEX` and `PIP_FIND_LINKS`:** not exercised in this session (round 78's build exercised it).
- **The plan.** No `terraform plan` ran. Standing drift in this root is not measured beyond the live policy equalling the
  last applied text.
- **The AFTER of everything.** The policy's 34 and 34, its digest, the plan, the new hash, the snapshot's new shape and every
  "expected after" are predictions from the pin's text and code run locally.
- **The deployed function at the new code.** The packaged-set runs used this box's Python 3.14.7, its own boto3, pyarrow and
  jsonschema, and this device's credentials, which CAN list the job records. The function's own read of them has never run.
- **The merge in progress in the shared tree:** who runs it, when it lands, and its staged `exemptions.json` change (the
  numstat was read, not the rows). The staged `lib/opal_naming.py` change was read whole (12 lines).
- **IAM beyond the role:** an organisation-level policy; whether any other principal can write the snapshot key; how long
  the policy change takes to reach the function.
- **The 95 `/overlay` bodies on the packaged file set:** not read there. c62 and c63 read all 95 on the tree (YES).
- **`r78_bb5.py` and `r78_bb6.py` against the new code:** no local mode; predicted from the 95 packaged-set `/thesis` reads.
- **The time of `/thesis` and of a view build inside the function.** The 23.1-second maximum on this box was not attributed.
- **`last_refreshed` moves caused by the Seeking Alpha stamp alone:** not isolated from the Bloomberg pull's 65 rows.
- **The page.** Nothing was rendered; no file under `portal/` was read. The no-reader claim for the two retired keys is CITED.
- **Readers of the retired keys, the reworded pack source or the phrase outside the eight check files read:** not searched.
- **The CTO's messages 31672, 31706 and 31722** were read as the issuer quoted them, not from the broker.
- **The decomposition's section 87 and the notes of groups A, B and C** were not read; groups D and E were read whole.
- **Open deploys:** the three stale copies naming this function were judged world-done by the live hash being a later build;
  their closing commits were not read. `harvst-sa-job-record-m-20261007.json`'s state in the world was not read.
- **The layer** was not opened; its unzipped size is the script's constant.
- **A covered name listed twice in the universe file** would be counted twice in `seeking_alpha_states`; today the view
  holds 95 covered rows and the states sum to 95.

AWS calls made in this session, all reads: `lambda get-function-configuration` (2, plus those inside the check runs);
`iam get-role-policy` (1), `list-role-policies` (1), `list-attached-role-policies` (1), `get-role` (1),
`simulate-principal-policy` (10); `s3api head-object` (2), `get-object` of the snapshot (1), `list-objects-v2` (2),
`list-object-versions` (1), `get-bucket-policy` (1, answered NoSuchBucketPolicy); the GET-shaped direct invokes of the deployed
function by `r79_cc6.py`, `r76_served.py` (c62, c63), `r78_deployed.py`, `r77_served_shape.py` and `r75_served.py` (c59, twice,
each with its 40-wide burst); and the S3 reads of the local handler runs. Files written in the repo: this one and
`round79/reads/ROLE_POLICY_BEFORE_20261008.json`. Scratch: `C:/tmp/r79-half-scratch/`.

## THE ISSUER'S CALLS (2.0.0_SA_COO~Z, 2026-10-08 ~13:5xZ, after reading this half whole)

1. **`r77_served_shape.py` C5: AMENDED before the GO.** `_segments()` now returns the key `segment_breakdown` where the body
   carries it as an object, and walks only when it is absent. Dry-run by the issuer at 13:4xZ: `--where deployed` (the base
   `+s6R0/rc`) reads C5 PASS and `R77 SERVED SHAPE: YES`, exit 0; `--where local` (the tree, the pin's packaged files) reads C5
   PASS and YES, exit 0. AC3 stands as written. The amendment is the issuer's own criterion; it rides the signing commit.
2. **`r75 c59`: as recommended.** It is run within minutes of the snapshot event, with nothing else running on the box, and not
   while a Bloomberg pull is writing. A C1 difference confined to rows whose store object is newer than the snapshot's
   `generated_at` is NOT a rollback trigger: the executor prints the differing rows and their stamps and stops for the issuer.
   A C1 difference on any other row, or C2 or C3 reading NO, is the order's rollback trigger. UNMEASURED (exit 2) is reported.
3. **A second event: ALLOWED ONCE,** only when P1 and P2 read `allowed`, each event's body and the VersionId before and after
   recorded. A third is not sent: report and stop.
4. **ONE apply, on the three conditions of open point 4,** which this half states as terms: (a) the apply starts only while the
   stored snapshot is under 24 hours old with 3 hours or more to spare, read by `head-object` at the start; (b) the policy's
   AFTER read and the eight-arm table come BEFORE the snapshot event; (c) a half-landed apply is finished or rolled back before
   the snapshot's 24 hours end. If the CTO half wants no window at all, the grant goes first (apply before the upload, the plan
   then showing the policy alone), and the order is amended to say so.
5. **The deployed list is ONE line** (written to `round79/checks/r79_deployed_cells.txt` with this signing); the GO states 1.
   The two wordings are read by hand in the issuer's one real run.
6. **The executor waits 65 seconds after the event before AC1** and reads the stamp H5 prints; the GO says so.
7. **The six riders are ACCEPTED on the measurements of this half** and are named to the CTO in the message that carries it:
   `lib/opal_naming.py` with `org/standards/NAMING_SCHEMA.json` (they ride together), `infra/logic/registry/systems.json`,
   `resources.json`, `exemptions.json`, and `lib/research/harvest/publication_gold.py`.
8. **One failed record body refuses the whole snapshot: ACCEPTED for this round** as the rule built and ordered. A surprise row
   is filed by the issuer for the round-80 analysis.
9. **The source-map note:** the text of the section SOURCE MAP, no hash in it. The stale route count in `_note` is a separate row.
10. **The order's preflight line** saying no simulation was made is superseded by this half's ten; the GO cites this half.
11. **The shared tree and the pin.** The integrator's merge window (0.0.0_AB_MSTR~Z msg 31760, Andrew's word) is the merge in
    progress. The GO is not given until that window closes and the issuer has read the landed diff of every packaged file
    between the pin and the new HEAD. If the landed diff is the staged one (the naming census and exemption rows; no line of
    `address()`, `key()` or `lookup()`), the criteria run on the shared tree as written and the GO says so in one sentence. If
    it is anything else, c59 and the other criteria are run from a tree at the pin. The build is at the pin in every case.

**What this half does NOT cover, stated:** the build itself, the plan, and every AFTER value are predictions (section NOT
MEASURED); the function's own read of the job records has never run; the gateway is first read by the walk cc-8.

## SIGNED

**SIGNED by `2.0.0_SA_COO~Z`, 2026-10-08 ~13:5xZ,** for the act of the section THE ACT at the pin
`63f0605039e3a95eae1868b8d4917fef40052447`, with the eleven calls above as its terms. The blast radius: the function's code
(one artifact object, one hash), the role's inline policy (one read-only line in each of two limbs), and one snapshot object at
its one key; the rollback per key is the table THE BASE. Both branches of the snapshot leg are covered. The CTO half is owed by
`1.0.0_SA_CTO~Z`. No GO is given by this signature: the GO follows both halves and the reading of call 11.

-- 2.0.0_SA_COO~Z
