# Never-widen packet R45 REFRESH 3 -- ONE gold Lambda release over live `oNgy4rnr`, FOUR members pinned on today's bytes, and what it changes for 49 Financial's method row 2 beyond R45

Author `0.9.0_WK_IRPT_DASHBD~101` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-126` (cell DB-b-126, round 68). Ordered by `1.0.0_SA_CTO~DELL2`'s ROUND-68 ANALYSIS, section 2 item 2 and section 4 item 3, answering rows `IRPT_DASHBD-D2-W88-S1` and `IRPT_DASHBD-D2-W88-S3` (both ARMED).
This cell writes this packet and its records only. **Nothing was built, uploaded, applied or edited** under `data/`, `infra/` or `portal/`. `s3_writes: 0`: no S3 put, copy or delete, no Lambda, Terraform or IAM act, no deploy, no push. Both halves below are UNSIGNED. Records, same folder: `R45_REFRESH3.json` (the criterion's record), `R45_REFRESH3_DELTA0.json` (tables, run identities, manifest comparison, the method-row dry runs), and `method_scripts/` (the five small scripts this cell wrote, kept as `.txt`). Harness reused UNCHANGED from `deliverables/0.9.0_WK_IRPT_DASHBD~92/`, sha256 prefixes read today: `refresh_delta0_run.py` `1dfddd6d771c`, `manifest_capture.py` `c0a47876bf0b`, `manifest_compare.py` `8cbdc1e08d88`. Client-data rule kept: the kit, the parquet outputs, the raw manifest capture and the logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~101/`; this packet holds counts, hashes and booleans only.

## READ FIRST

1. **Four members, all pinned today** (section "Members"). One of them moved after REFRESH_2: `account_return_daily.py`, through FOUR commits (`91e3ec5a47` DB-b-118, `3438a03703` DB-b-118 AMENDMENT 1, `ac6a174677` DB-b-120, `17304421c8` DB-b-122), not the one commit the issuing order names. The other three are byte-equal to REFRESH_2's pins.
2. **`sources.json` rides the release at pin `f043506a7c`**, the same bytes as REFRESH_2's; its 49 Financial source `schwab_08335338` declares `"method_version": 2` at `sources.json:23`. That is the disarm of row W88-S1.
3. **Kit day 2026-10-08, run today on the four candidate members: the five output tables are byte-equal to the live-pinned run (5 of 5), and `method_version` is equal on 6,901 of 6,901 returns rows.** The returns manifest states `method_version` 2, `valuation_source` `custodian_reported`, `fee_treatment` `gross_of_advisory_fees`, `price_basis` `custodian_closing_price`: none `absent`. That is the disarm of row W88-S3 for the backfill call site.
4. **THE NEW SECTION (read it hardest): a release at these pins puts NINE new columns, not two, into 49 Financial's method row 2 -- but only when the producer's own `main()` later runs with upload; the Lambda this release replaces never writes that row.** The two the issuing order names (`income_basis_claim`, `income_basis_reason`) are the last two; seven more (`tolerance_claim`, `large_flow_share_claim`, `plausibility_band_low_claim`, `plausibility_band_high_claim`, `comparability_max_excluded_weight_claim`, `threshold_claims_source`, `tieout_tolerance_proposed_claim`) came with DB-b-118 and DB-b-120 and have never been named in a 49 Financial pair. Rows `IRPT_DASHBD-D2-W101-S1` and `-S2` file the two differences from the order.

## Supersedes

This packet replaces `deliverables/0.9.0_WK_IRPT_DASHBD~92/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2.md` (sha256 `863f98a21e34d5ad5e65875dc8a718c4998d036c01da365dbfa53864c0e13758`), which the COO half (`deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_R45_RELEASE_REFRESH2_COO_HALF.md`) signed and the CTO's half of which is VOID (analysis section 2 item 2). Any half signed on REFRESH_2, REFRESH, or the one-member packet is void for the apply. The COO half's four conditions carry forward, restated under "Conditions".

## Members (the release's files, each pinned at the commit that LAST CHANGED it on trunk today)

Base: worktree `0db7244334` cut from `box/dell2`; for each member `git log -1 --format=%H -- <file>` on `HEAD` and on `box/dell2` (`27c28a6497`) return the same commit. sha256 is of `git show <pin>:<file>`, and equals the file at HEAD. Pins resolved by content (blob sha256 printed from `git show`), not by filename or ancestry.

| # | Member | Pin (last change) | sha256 at the pin | REFRESH_2 pin / sha256 | Since REFRESH_2 |
|---|---|---|---|---|---|
| 1 | `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `080dc90d92542d96817ae79f4f8a72a85dd9de09` (DB-b-115) | `d95f42d54aacd7efa6d054b12d3901e49b109427f910ff7a60ef6dcc7d36a116` | `080dc90d92` / `d95f42d54aac...` | unchanged |
| 2 | `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `17304421c87c2c0369b05a742887b873ba30693d` (DB-b-122) | `a9832cf35678d2bc2e1ef89fc74c3f5ed551b42b6c62ffca01f06ec438afbfb0` | `354214c55f` / `14a6b91f5021...` | **MOVED**: 4 commits, 1 file, +131 / -5 lines, every hunk in the method-row machinery (constants `:107-131`, a new claims block `:1889-1980`, `emit_method_row` `:1981-2057`) plus 3 lines in `main()` `:2131-2133` |
| 3 | `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `19ba6fe341da80c906d0a1ff7a0db0253fdd2115` (DB-b-110) | `c5364a9f81f0105ce675c28991fa6691e52f264cbf8a3ff5fc0e64c29fa73d2f` | `19ba6fe341` / `c5364a9f81f0...` | unchanged |
| 4 | `data/assets/scripts/gold/irpt_reporting/sources.json` | `f043506a7c3f5a7d997e6e4096ba094435e419a5` (ADVI_COTBKF CB-au-1) | `b8f40af776589a1d3dc00c5d63f1e93508b812215c71d6baa5bf899a7f42fc3b` | `f043506a7c` / `b8f40af77658...` | unchanged |

What changed in member 2 since REFRESH_2 (the four commits): `91e3ec5a47` DB-b-118 (a claim per guard threshold value, six columns), `3438a03703` DB-b-118 AMENDMENT 1 (the method row's table typed explicitly, so an all-absent row lands typed nulls), `ac6a174677` DB-b-120 (`tieout_tolerance_proposed` takes a claim, one column), `17304421c8` DB-b-122 (income per row: row 2 `cash_when_received` / `held`, row 3 none / `absent` with a reason; two columns). None touches `emit_day`, `build_manifest`, or any day computation; the kit comparison below is the measurement of that.

**Not members (stay at their source-map pins).** The source-map entry for `irpt-49f-reporting-gold-lambda` (`infra/aws/lambda/ci/lambda-source-map.json`) is byte-equal to its content at REFRESH_2's head (`5e022934e8`): 18 `staged_from` pins, each pin blob's sha256 equals its recorded sha256 (18 of 18). Of the 18 at HEAD, **10 equal HEAD, 3 are members (rows 2-4 above), and 5 differ from HEAD and STAY at their pins**: `lib/opal_naming.py` (pin `e15671f611`, sha256 `9d301e1c0fe6...`; HEAD last change `f41e5a1811`), `infra/logic/registry/systems.json` (pin `530ef17ff8`, `70cfd07e4555...`; HEAD `826364c980`), `infra/logic/registry/scopes.json` (pin `5f962296ae`, `13947f7f2b35...`; HEAD `3a5e564561`), `infra/logic/registry/reporting_policies.json` (pin `0c35aeeaa8`, `dc0eccfde861...`; HEAD `103902e75d`), and `MEASURED_THRESHOLDS_R1.json` (pin `6be02af162` of the deleted `0.4.0_DS_ClientPlatform~S` path, sha256 `551920f0c364...`). **Since REFRESH_2 this list grew by one: `systems.json` (a two-line registry edit, `826364c980`).** It is not shipped; the release stays on its pin. (10 + 3 + 5 = 18.)

**Trunk has moved since this worktree was cut, and one move touches the handler's folder:** `box/dell2` carries `aaeb1866ff` (DB-b-125), a tracked `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json` with a claim per threshold (sha256 `69e0a889a7e6...`). The source map does not point at it; the release stages the pinned `551920f0c364...` blob, as REFRESH_2's did. It matters here for one reason: the VALUES of the five threshold claims in row 2 depend on which thresholds file a later `main()` is given (section "New section", table 2).

## `sources.json` that rides the release (row W88-S1's disarm)

- Pin `f043506a7c3f5a7d997e6e4096ba094435e419a5`, sha256 `b8f40af776589a1d3dc00c5d63f1e93508b812215c71d6baa5bf899a7f42fc3b`. Same blob as REFRESH_2's.
- **It declares `method_version` for the 49 Financial source at `sources.json:23`: `"method_version": 2`**, inside the entry `schwab_08335338` (opens `:6`). `declared_sources` (`account_return_daily.py:319-325`) returns every top-level key whose value is an object and whose name is not underscore-prefixed; run today on these bytes it returns exactly `['schwab_08335338']`, and `method_version_of` of that entry returns 2, `firm_scope` gives `49financial`.
- `_commonwealth_delivery` (opens `:123`; `method_version` 3 at `:125`) rides in the same bytes and is **not** a declared source (underscore-prefixed), so no 49 Financial path reads it. No commit holds the 49 Financial method fields without it (REFRESH_2, open question 1, restated). A pin without that entry is not available.
- Diff against the live pin `efeb21df71`: unchanged since REFRESH_2 (six keys added to the custody entry, one new underscore-prefixed top-level entry, nothing changed or removed).

## Kit comparison on the kit day REFRESH_2 used (2026-10-08), DRY

**Method, same as REFRESH_2 (its harness, unchanged).** A kit `kit_new6` in the Lambda layout, outside the repo: all four members at the pins above, every other member as pinned (checked: the 15 non-member staged files equal both their recorded sha256 and the pinned blob, 0 mismatches; the 3 staged members and `handler.py` equal HEAD). `refresh_delta0_run.py` calls `handler.local()` for the one day in one process: S3 GETs only; the lots status write goes to a counting stub (1 stub put, 0 S3 writes). The LIVE outputs are DB-b-113's live-pinned run, REUSED as REFRESH_2 reused them: re-hashed today, 5 of 5 equal to the committed `sha256_live`. The new run is also equal to REFRESH_2's new run on 5 of 5 tables, so the inputs for the kit day have not moved since REFRESH_2 read them.

| Table | Rows | sha256 live-pinned | sha256 four members at today's pins | Equal |
|---|---|---|---|---|
| returns | 6,901 | `9e5d6e92760d0ae2...` | `9e5d6e92760d0ae2...` | yes |
| class | 25,057 | `2028f91d7e2a652f...` | `2028f91d7e2a652f...` | yes |
| account_activity_daily | 6,901 | `f81aaa0b4f33691c...` | `f81aaa0b4f33691c...` | yes |
| account_lot_realized | 35,834 | `651421e336953941...` | `651421e336953941...` | yes |
| account_lot_unrealized_daily | 542,546 | `9e2df0d8f7fb0579...` | `9e2df0d8f7fb0579...` | yes |

Full hashes in `R45_REFRESH3_DELTA0.json`. Thresholds sha256 `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` in both. Run identity (new): `handler.py d95f42d54aac`, `account_return_daily.py a9832cf35678`, `account_activity_lots.py c5364a9f81f0`, `sources.json b8f40af77658`, `account_class_daily.py 2def366fb5de` (as live). Wall 972.6 s.

**`method_version`, row by row.** The returns parquet has the column. Live and new carry the same column list; their (`account_id`, `business_date`) keys align row by row; `method_version` is 2 in both on every row, none null: **6,901 of 6,901 rows equal. `kit.equal` is true.**

**Reads made.** The two kit runs (the harness run and the manifest capture below) read served inputs with the handler's own S3 GET and LIST calls, as REFRESH_2's did, under the same harness; the calls are not individually logged by that harness, so no per-call count is stated. No write verb reached S3: the capture client raises on any write verb other than a captured `put_object`, and the data writer is stubbed.

## Manifest comparison (candidate against live; row W88-S3's disarm)

**Method, same as REFRESH_2.** `manifest_capture.py` runs the kit's OWN `handler.run_backfill()` for the one landed day 2026-10-08 against a guard client that delegates reads and CAPTURES every `put_object` (never sent), with the data write stubbed; the candidate put **5 objects** (returns, class, three lots manifests). The live side is REFRESH_2's capture of the live kit (`capture_live.json`, the live kit's bytes are unchanged and were not re-run), compared with `manifest_compare.py` unchanged. The status record is captured by calling the kit's own `record_lots_status` with a forced refusal. **Denominator: 6 objects, 91 field comparisons: 87 EQUAL, 3 ADDED, 1 CHANGED (a derived key count), 0 REMOVED.** Identical to REFRESH_2's counts.

**The four fields as the candidate's returns manifest writes them:**

| Field | Live manifest | Candidate | Verdict |
|---|---|---|---|
| `method_version` | 2 | **2** | EQUAL (not `absent`) |
| `valuation_source` | no such key | `custodian_reported` | ADDED |
| `fee_treatment` | no such key | `gross_of_advisory_fees` | ADDED |
| `price_basis` | no such key | `custodian_closing_price` | ADDED |
| (key count, derived) | 16 | 19 | CHANGED: exactly the three ADDED |

Everything else in the returns manifest is EQUAL (`method` sentence byte-equal, `rows`, both censuses, `thresholds`, `address`, `asof`, `schema_version`); the class and three lots manifests and the status record are field-for-field EQUAL. The DB-b-118/120/122 changes therefore touch no manifest the handler writes. **Reader read of the three ADDED keys:** `deliverables/0.9.0_WK_IRPT_DASHBD~94/RETURNS_MANIFEST_READERS.json`, 10 readers counted, verdict `NO_STRICT_READER` (all 10 read named keys and ACCEPT an unknown key); its stated limit (an unlisted reader is not seen) stands.
Limits stated: the data write is stubbed on both sides, so `landed` reads equal by construction (the data bytes are carried by the table hashes); the scheduled call site `handler.py:624` was not exercised, only the backfill site `:581` (same expression over the same `src`). W88-S3 is read here for the backfill site; the scheduled site stays the acceptance read at the first fire after release.

## NEW SECTION -- what a release at these pins changes for 49 Financial's served objects BEYOND R45's original scope

Required by the CTO half on DB-b-122, condition 5 (`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_METHOD_ROW3_INCOME_CTO_HALF.md`): the producer change "alters what a later emit writes for 49 Financial's method row 2 ... a release under its own pair, and that pair names row 2's new columns and who reads them."

### 1. Which served object, and does THIS release move it?

The object: `s3://opal-data-49financial/irpt/49financial/gold/dim_return_method/method_version=2` (the producer's own dry run returns this `address` for the 49 Financial entry; `lib/opal_naming.py address()` output, not typed here). It holds two keys, `data.parquet` (one row) and `manifest.json` (the row plus `thresholds`), written by `emit_method_row` (`account_return_daily.py:2053-2054`).

**The Lambda release moves neither key.** Three independent readings, all of source, none of the live role:
- `handler.py:12-16` states it omits `emit_method_row`, and the census of `emit_method_row` call sites (below) lists no call in the handler.
- The role's Terraform grants `s3:PutObject` only on the five gold prefixes: `infra/aws/terraform/investor-reporting/reporting-gold/iam.tf:88-95` ("and not the dim_return_method prefix"), `locals.tf:94-95`. (The live IAM role was not read; this is the Terraform source.)
- The kit capture put 5 objects, none of them a method row.

**The method row moves only on a later, separate act: the producer's own `main()` with `--upload`** (full emit `account_return_daily.py:2213`, or `--method-row-only` `:2159`). Whether anything or anyone schedules or runs that for 49 Financial is **NOT_ESTABLISHED**: the schedule in `infra/aws/terraform/investor-reporting/reporting-gold/schedule.tf:85` fires the Lambda, which does not call it, and no other trigger of the producer's CLI was found in the files read; a manual run cannot be seen from the tree. And whether the row-2 object exists in the bucket today is NOT_ESTABLISHED: no S3 listing is granted to this order.

### 2. The columns row 2 gains (the producer's dry run, `upload=False`, three code states, the same 49 Financial entry)

Row 2 at the live-pinned producer (`ba544b6064`) and at REFRESH_2's pin (`354214c55f`) is the SAME 22 columns. At today's pin it is **31: 9 ADDED, 0 REMOVED, 0 CHANGED among the 22 existing columns except `measured_at`**, which every emit re-stamps. Address printed above. Table schema: `income_basis`, the claim columns and the reason are `string`; `tieout_tolerance_proposed` `double`.

| # | New column | Type | Row 2 value in the dry run | Commit |
|---|---|---|---|---|
| 1 | `income_basis_claim` | string | `held` | 17304421c8 DB-b-122 |
| 2 | `income_basis_reason` | string | null (a reason is stated only under `absent`; row 2's income IS stated) | 17304421c8 DB-b-122 |
| 3 | `tolerance_claim` | string | `held` (staged thresholds file, no claims) | 91e3ec5a47 DB-b-118 |
| 4 | `large_flow_share_claim` | string | `held` | 91e3ec5a47 |
| 5 | `plausibility_band_low_claim` | string | `held` | 91e3ec5a47 |
| 6 | `plausibility_band_high_claim` | string | `held` | 91e3ec5a47 |
| 7 | `comparability_max_excluded_weight_claim` | string | `held` | 91e3ec5a47 |
| 8 | `threshold_claims_source` | string | `defaulted_no_claims` | 91e3ec5a47 |
| 9 | `tieout_tolerance_proposed_claim` | string | `absent` (no `--tieout` given) | ac6a174677 DB-b-120 |

The existing column `income_basis` keeps `cash_when_received` on row 2 (it becomes null only on row 3, the Cottonwood row, which this producer does not write for 49 Financial). Values for rows 3-9 depend on the INPUT a later `main()` is given, not on the release. Table 2b, the same dry run with the DB-b-125 tracked thresholds file (`aaeb1866ff`, not in this release's pins): `tolerance_claim` `measured`, `large_flow_share_claim` `measured`, `plausibility_band_low_claim` `held`, `plausibility_band_high_claim` `held`, `comparability_max_excluded_weight_claim` `inferred`, `threshold_claims_source` `stated`; the income pair and the tie-out claim are unchanged. The pair does not choose between them: it signs that the columns appear and what they can read.

`main()` also gains a refusal at `:2131-2133` (a malformed `threshold_claims` object is refused before any computation). That is a behaviour change of any later `main()` run, and is part of this change.

### 3. EVERY reader of that method row (N = 25 files read; the count stands on the denominators printed here)

Denominator: `comp-find -i --files "\bdim_return_method\b"` over the repo (corpus=all), 317 hit(s) across 70,369 file(s) scanned: bands DEF 3 files, SURFACED 17 files (the 3 DEF are among them), TEST 3 files, plus CONFIG and DOC (data and prose: the contract, records and orders: not readers of the object, set aside); `comp-find --files "\bemit_method_row\b"`, 142 hit(s) across 70,366 file(s): adds 5 first-party files not in the first list (4 tests and the round-66 check). `TABLE_METHOD`: 4 hits, nothing new. **Union of first-party code, test and check files: 17 + 3 + 5 = 25**, each opened.

**N = 25 rules read. Result: 0 of the 25 read the served 49 Financial row-2 object's columns.** What each one does, with what an unknown (new) column does to it:

| Class | Files (file:line) | What it does | An unknown / new column |
|---|---|---|---|
| A. The writer (1) | `gold/irpt_reporting/account_return_daily.py:1981` (`emit_method_row`; callers `:2159`, `:2213`) | builds and writes the row and manifest; no guard of its own on overwrite | it IS the source of the nine |
| B. Same function, another scope (2) | `silver/commonwealth_account_return_daily.py:714` (dry), `:879` (upload; `SCOPE` is the Cottonwood registry row `:119`, `ENTRY` is `_commonwealth_delivery` `:129`); check `.../checks/r67/p67_round67.py:23` (the Cottonwood prefix) | writes / verifies the Cottonwood row 3 only; cannot reach 49 Financial | not applicable to row 2; row 3 is under its own pair |
| C. Names it, reads nothing (7) | `reporting-gold/handler.py:12,215` (docstring); `reporting-gold/iam.tf:88`, `locals.tf:95` (no-write comment); `reporting-publish/iam.tf:40`, `locals.tf:16,48,54` (read grant to the prefix, `locals.tf:54`); `checks/r22/p22_release_prep.py:88` (asserts the write set omits it); `checks/r60/p60_round60.py:3` (docstring) | the publisher is GRANTED read of the prefix but `reporting-publish/publisher.py` never opens a method row: its only `method_version` source is the return rows (`:173-176`, `:205`) | no code runs; a grant is not a read |
| D. Reads the emitted row by NAME (5) | tests `test_account_equity_value.py:81-89`, `test_short_income_and_tolerance.py:85-91`, `test_method_version_from_source.py:68-74`, `silver/tests/test_commonwealth_ard_mint_claims.py:190-192` (address only); check `checks/r66/p66_round66.py:62,79-90` (`COLS_050`: asserts the earlier 29 columns are present) | indexes named keys / compares an address | ACCEPTS (an extra column is not looked at) |
| E. Pins the COLUMN SET of the emitted row (6) | tests `test_threshold_claims.py:157-174` (the added set must equal exactly the columns listed), `test_tieout_claim.py:115`, `test_method_row3_income.py:28-66,100-116` (row 2's 28 prior columns pinned; the added set pinned); checks `p62_round62.py:113-117`, `p64_round64.py:61-65`, `P/checks/r10/p10_1_ac1_method_contract_matches_row.py:29-50` (row keys must EQUAL the contract's columns) | compares the row's key set with a fixed set / the contract | **REJECTS an unlisted column**: at HEAD the tests pass with the nine (168 passed per the DB-b-122 record, read not re-run) and the contract is at 0.6.0 with the nine; three of the checks are pinned to older contract versions and read `FAIL` today for that pin (run today: `p10` "contract_version is '0.6.0', not 0.3.0", `p62` AC3 "want 0.4.0", `p64` AC1 "want 0.5.0"), so they are already superseded by DB-b-122's cut; they are project verifiers, not on the deploy path (no deploy gate that runs them was read) |
| F. Reads the SERVED method row object (4) | `P/checks/r1/p1_1_ac1_gold_under_contract.py:134,141-146` and `p1_1_ac2_guard_seam.py:181-186`, `p1_3_ac2_method_winner_written.py:119` (all `method_version=1` only, named columns); `P/p2_window/p2_prewindow_versions.py:15` (lists object versions of the prefix, reads no column) | reads `method_version=1` (not row 2) by named columns / lists versions | ACCEPTS; none reads `method_version=2` |

(1 + 2 + 7 + 5 + 6 + 4 = 25.) Zero is a value: **no code in the 25 reads a column of the served 49 Financial row-2 object**, and the only code that rejects a new column compares the PRODUCER's emitted row to a contract and a test pin, both already moved to 0.6.0. Stated limits: a reader outside the repo (a notebook, an object read by key, `mcportal/`, an empty directory in this worktree) is not seen; the p62/p64/p10 FAILs are measured today and are not caused by this release.

### 4. Blast radius per key, and rollback per key

| Key | Moved by the Lambda release | Moved by a later `main()` upload | Rollback |
|---|---|---|---|
| `.../dim_return_method/method_version=2/data.parquet` | no | overwritten: 1 row, 22 -> 31 columns; the 21 existing values equal for the same input, `measured_at` re-stamped | the prior S3 version of the key, restored by `copy-object` from the version id READ at that moment, if the bucket is versioned (`p2_prewindow_versions.py:5` calls it versioned; NOT read by this cell); else the captured body |
| `.../dim_return_method/method_version=2/manifest.json` | no | overwritten: the same row plus `thresholds`, the nine keys added | same |
| every other 49 Financial object (the 6,650-day `account_return_daily` keys, the class and lots tables, the status record) | only by a backfill or fire, with the 3 ADDED manifest keys on the returns manifest | no | per "Rollback" below |

The CTO half on DB-b-122 required, for its own Cottonwood act, capture-first and no deletes (its conditions 1 and 6). A later row-2 act would need the same: capture both keys' bodies, sha256, size and ETag first, read `get-bucket-versioning`, and never delete. This packet states that need; it does not sign it.

## Radius

No new key, read or grant: no Terraform root file is edited. Writers on the handler's path, counted again at these bytes: **4 `put_object` sites serving 6 objects**: `account_return_daily.py:1883` (the returns manifest, `emit_day` `:1871`), `account_class_daily.py:593`, `account_activity_lots.py:1352` (three tables) and `handler.py:485` (the lots status record, ONE writer rule `record_lots_status`, two callers); the data parquet writes go through the shared `lib/stream_parquet.py:136`. `emit_method_row`'s put (`account_return_daily.py:2054`) is **not** on the handler's path. The status object is unchanged in bytes (`handler.py` is REFRESH_2's), and the kit run wrote it on neither side. Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`; `memory_size` already 3008). Any other count is a STOP.

## Branch A and Branch B (handler and lots bytes are REFRESH_2's)

`handler.py` and `account_activity_lots.py` are byte-equal to REFRESH_2's, so its Branch A (a backfill lands a stated day and the status record drops it: `handler.py:546-590`, `record_lots_status` `:458-489`, absent object writes nothing) and Branch B (a backfill refuses a day and states it: `account_activity_lots.py:317-327`, `handler.py:396-398`, `:437-438`, `:485`; returns and class still land; limit stated: a refused backfill day is not owed again by the catch-up) stand as written there; their line citations hold on identical bytes. This cell did not re-derive them.

## Rollback

Per key, back to `oNgy4rnr`:
- **Lambda function:** the prior function is the live one (below); artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in `opal-313476888478-lambda-artifacts`, base S3 version **`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`**. Route: `copy-object` of that version onto the same key, re-record the source-map entry, targeted `safe-apply` (`aws lambda update-function-code` is barred).
- **Per member (four pins restored):** `handler.py`: no source-map pin; rollback build commit `072d27a4a1` (sha256 `212b6f7682bf...`); `account_return_daily.py`: pin `ba544b60646d9b96e8bf126b4a47064dba0c70f5` (`9935f5c7bcd7...`); `account_activity_lots.py`: pin `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c` (`caf7655586b9...`); `sources.json`: pin `efeb21df7147955a64f79a4f7b7ff2cc5d3d9426` (`5dd1f367d4d0...`). The S3 version copy puts the old bytes back; the pins are the source map's record of what the artifact holds.
- **Status key** `irpt/49financial/gold/account_activity_daily/_status/lots_not_computed.json`: not written by the kit run on either side; the apply cell reads the prefix first; a write by a fire or backfill is reversed by `copy-object` of its prior version; with no prior version, removal is an S3 delete, a human-confirmed act. 0 served readers.
- **Day partitions and manifests** a released backfill rewrites: prior versions restored by `copy-object` from the version id read at that moment; a new `date=` key with no prior object is removed only after Andrew's word. A returns manifest rewritten after the release carries the three ADDED keys; restoring the prior version removes them.
- **Method row 2 keys:** see the new section, table 4.

## Memory headroom

Live MemorySize **3008 MB**, 85 percent line **2,556.8 MB**; this packet asks for no change. Local process RSS (a laptop `handler.local()` run; NOT the Lambda's figure): live-pinned members **1,691.1 MB** (`lots_read` 1,691.1; DB-b-113's run), REFRESH_2's candidate 1,458.6, **today's candidate 1,434.5 MB** (`lots_read` 1,238.0; the capture ran concurrently, so RSS is per process but the machine was shared). The Lambda's own figure for the new bytes is still ARGUED, not measured: no Lambda run exists on them; the live code last measured 1,672 MB at 3008 MB (65.4 percent of the line). The first scheduled fire after release remains the acceptance read.

## What is live today (read, not assumed)

ONE `get-function-configuration` of `irpt-49f-reporting-gold-lambda` at 2026-10-11T15:10:51Z (shim `.tools/aws`, rc 0): **CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`**, LastModified `2026-10-09T17:32:02.000+0000`, State Active, LastUpdateStatus Successful, **MemorySize 3008**, Timeout 900. ONE `head-object` of `investor-reporting/irpt-reporting-gold-lambda.zip` (the latest, no version id passed) at 15:10:57Z, rc 0: **VersionId `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`**, LastModified `2026-10-09T14:29:21+00:00`, 218,641 bytes, ETag `04b4e6be86b368990d5ce81ee178ccbc`, metadata `content-sha256` equal to the CodeSha256. All unchanged from REFRESH_2's reads. The live state is `oNgy4rnr`, the R44 build; the R45 release is not applied.

## Open questions for the halves

This worker decides none of these.
1. **Is `sources.json` (with `_commonwealth_delivery`) in the release?** Same question and same reading as REFRESH_2's question 1: unread by every 49 Financial path, carried in the bytes.
2. **Are the three ADDED returns-manifest keys inside the never-widen?** Same as REFRESH_2's question 2; the reader count is 10 with `NO_STRICT_READER`.
3. **NEW. Does the pair cover the nine new columns on row 2, or only the release?** The Lambda release moves no method-row key; the nine reach a served object only through a later `main()` upload, which is its own act. The halves may (a) sign the release alone and name the row-2 columns as a precondition of any later `main()` upload, or (b) sign both. The order named two columns; the measured set is nine.
4. **NEW. Which thresholds file does a later `main()` run be given?** It decides five of the nine values (table 2 and 2b).

## Conditions carried from the COO half on REFRESH_2 (restated at these pins)

1. The apply builds from the four PINS above, never from HEAD; it re-reads every pin's sha256 against this packet; a member whose bytes are not the packet's, or any member OTHER than the four differing from live's bytes, is a STOP before upload. (The five non-member pins stay.)
2. The Lambda's memory on the new bytes is argued: the apply's first act after upload is ONE dry-run invoke of the 2026-10-08 backfill, read against 2,556.8 MB and 85 percent of the 900 s timeout (765 s). OVER on either: roll back to `oNgy4rnr` by its S3 version and restore the four pins.
3. The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr` (row D2-W78-S1, the R44 acceptance). If that fire reads OVER, R44's rollback comes first and this packet is re-cut over that base.
4. The scheduled call site (`handler.py:624`) is read at the first fire after release for the three added keys and `method_version` 2 before the ledger closes.
5. NEW. No run of the producer's `main()` with upload against 49 Financial is made under this pair unless the halves cover it (open question 3).

Apply preconditions as REFRESH_2's: ledger first, pinned to this packet's sha256; read every live worktree's `.open_deploys/`; re-read live as `oNgy4rnr` and MemorySize 3008 before upload, else STOP; upload member census against live is exactly the four; one `.tools/safe-apply.sh`; post-apply plan `No changes`; no ad-hoc invoke beyond condition 2's one dry run. **Until both halves are signed on this packet's sha256, no apply is made.**

## COO half

Status: UNSIGNED. Reads and signs: the four members and their pins, the `sources.json` that rides, the kit comparison and manifest fields, the new section (nine columns, 25 readers, per-key radius and rollback), the carried conditions. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED. Reads and signs: the new section against DB-b-122's condition 5, both branches by reference, the manifest widening (three keys), and open question 3. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
