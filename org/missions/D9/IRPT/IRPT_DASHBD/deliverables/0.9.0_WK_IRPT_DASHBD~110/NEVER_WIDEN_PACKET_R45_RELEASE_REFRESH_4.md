# Never-widen packet R45 REFRESH 4 -- the same ONE gold Lambda release over live `oNgy4rnr`, on today's producer: a returns manifest written after it holds SIX threshold keys, not the whole file

Author `0.9.0_WK_IRPT_DASHBD~110` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-137` (cell DB-b-137, round 71). Ordered by `1.0.0_SA_CTO~DELL2`'s ruling msg 5375 item 3 on DB-b-131's read, answering rows `IRPT_DASHBD-D2-W100-S3`, `-W101-S1`, `-W101-S2`.
This cell writes this packet and its records only. **Nothing was built, uploaded, applied or edited** under `data/`, `infra/` or `portal/`. `s3_writes: 0`: no S3 put, copy or delete, no Lambda, Terraform or IAM act, no `upload=True` call, no deploy, no push. Both halves below are UNSIGNED. Records, same folder: `R45_REFRESH4.json` (the criterion's record), `R45_REFRESH4_DELTA0.json` (tables, run identity, manifest comparison, producer dry reads) and `method_scripts/` (three small scripts, kept as `.txt`). Harness reused UNCHANGED from `deliverables/0.9.0_WK_IRPT_DASHBD~92/`: `refresh_delta0_run.py`, `manifest_capture.py`, `manifest_compare.py` (REFRESH_3 used the same three). Client-data rule kept: the kit, the parquet outputs, the raw manifest capture and the logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~110/`; this packet holds counts, key names, hashes and booleans only.

## READ FIRST

1. **Four members, all pinned today; ONE moved since REFRESH_3.** `account_return_daily.py` moved from `17304421c8` to `739dbb240f` through THREE commits. The other three members are byte-equal to REFRESH_3's pins.
2. **A daily returns manifest written after the release carries a `thresholds` object of SIX keys** (`tolerance`, `large_flow_share`, `plausibility_band_low`, `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims`), measured on the kit's own captured manifest. The live package's file has 24 top-level keys; the live-pinned kit's manifest holds all 24. 19 keys stop being served; 3 of those 19 carry a run of 8 or more digits (two are the account-number-shaped ones row W100-S3 names; the third is a decimal in a sentence).
3. **Kit day 2026-10-08, run today on the four candidate members: the five output tables are byte-equal to the live-pinned run (5 of 5), and `method_version` is equal on 6,901 of 6,901 returns rows.** Manifest comparison, 6 objects, 91 field comparisons: 86 EQUAL, 3 ADDED (the R45 keys), 2 CHANGED (the derived key count, and `thresholds` 24 to 6 keys), 0 REMOVED.
4. **The method row 2 conclusion of REFRESH_3 still holds at these pins:** the Lambda this release replaces cannot write it. A later producer `main()` upload would write row 2 with the same 31 columns as REFRESH_3 named, and a `manifest.json` whose `thresholds` holds the same six keys.
5. **This release rewrites no manifest already served.** Every manifest written before it keeps the whole object. Removing a prior version is a delete and Andrew's act.
6. **One open question is new and the halves must answer it: which thresholds file rides the package** (section "The thresholds file in the package"). This worker chooses neither.

## Supersedes

This packet replaces `deliverables/0.9.0_WK_IRPT_DASHBD~101/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_3.md` (sha256 `e01f9c40ea9fdeaefea1f47c4620c9edce541ba5f1b917240e037d64c8e40e2d`) for the apply. **REFRESH_3's halves stand until REFRESH_4's are signed** (the order's instruction); a half signed on REFRESH_3 or earlier does not cover the apply once REFRESH_4's pair exists. The carried conditions are restated under "Conditions".

## Members (the release's files, each pinned at the commit that LAST CHANGED it on trunk today)

Base: worktree cut at `4f00757f67`; for each member `git log -1 --format=%H -- <file>` on `HEAD` and on `box/dell2` (`5b9b6acb7b`) return the same commit (HEAD is an ancestor of `box/dell2`). sha256 is of `git show <pin>:<file>` and equals the file at HEAD. The record `R45_REFRESH4.json` carries the same table, and its pins are re-hashed by the criterion's check with `git show`.

| # | Member | Pin (last change) | sha256 at the pin | REFRESH_3 pin | Since REFRESH_3 |
|---|---|---|---|---|---|
| 1 | `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `080dc90d92542d96817ae79f4f8a72a85dd9de09` (DB-b-115) | `d95f42d54aacd7efa6d054b12d3901e49b109427f910ff7a60ef6dcc7d36a116` | `080dc90d92` | unchanged |
| 2 | `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `739dbb240f19b6dd2c08ce982c44c9b7c17ca322` (DB-b-134) | `73361b54df395ae4a0de39d149e4ca822144dd9f0003d0fef6f98d786374383a` | `17304421c8` / `a9832cf35678...` | **MOVED**: 3 commits, 1 file, +24 / -5 lines (below) |
| 3 | `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `19ba6fe341da80c906d0a1ff7a0db0253fdd2115` (DB-b-110) | `c5364a9f81f0105ce675c28991fa6691e52f264cbf8a3ff5fc0e64c29fa73d2f` | `19ba6fe341` | unchanged |
| 4 | `data/assets/scripts/gold/irpt_reporting/sources.json` | `f043506a7c3f5a7d997e6e4096ba094435e419a5` (ADVI_COTBKF CB-au-1) | `b8f40af776589a1d3dc00c5d63f1e93508b812215c71d6baa5bf899a7f42fc3b` | `f043506a7c` | unchanged |

**What changed in member 2 since REFRESH_3** (`git diff 17304421c8 739dbb240f`, read today):
- `24dd85716d` DB-b-128: the method row 3 income reason is reworded (`METHOD_ROWS[3]["income_basis_reason"]` and a comment). Row 3 is the positions-based method; the 49 Financial entry names row 2, so no 49 Financial object carries it.
- `ddbd882a4f` DB-b-132: a new `served_thresholds(thresholds)` (`:1942`); `build_manifest` writes `"thresholds": served_thresholds(thresholds)` (`:1871`, was `thresholds`) and `emit_method_row` writes `{**row, "thresholds": served_thresholds(thresholds)}` (`:2074`, was `thresholds`). It builds a NEW dict of the five `THRESHOLD_VALUES` (each as given) and `threshold_claims` (the five claims as `threshold_claims_of` resolves them, so an input with no claims serves the defaulted ones), and nothing else; `None` stays `None`. Both manifest writers use it.
- `739dbb240f` DB-b-134: `method_version_of` (`:1829-1835`) gains a refusal for an entry that names a method row whose `valuation_source` is not `custodian_reported` yet declares no `valuation_source`. Read at the 49 Financial entry: row 2 is `custodian_reported`, so the branch is not taken; the kit run below returns `method_version` 2 on 6,901 of 6,901 rows.
- None of the three touches `emit_day`, a day computation, or `main()`'s control flow; the kit comparison measures that.

**Not members (stay at their source-map pins).** The source-map entry for `irpt-49f-reporting-gold-lambda` in `infra/aws/lambda/ci/lambda-source-map.json` (last change `6f2182e539`): 18 `staged_from` pins, each pin blob's sha256 equals its recorded sha256 (18 of 18; the 3 member entries record the OLD pins, as in REFRESH_3). Of the 18 at HEAD, **9 equal HEAD, 3 are members (rows 2-4 above), and 6 differ from HEAD and STAY at their pins**: `lib/opal_naming.py` (pin `e15671f611`; HEAD last change `b81373cbcc`), `infra/logic/registry/systems.json` (pin `530ef17ff8`; HEAD `826364c980`), `infra/logic/registry/scopes.json` (pin `5f962296ae`; HEAD `3a5e564561`), `infra/logic/registry/reporting_policies.json` (pin `0c35aeeaa8`; HEAD `103902e75d`), `infra/logic/registry/exemptions.json` (pin `2a809c975e`; HEAD `3a6d8aa89d`), and the thresholds file (pin `6be02af162` of the deleted `0.4.0_DS_ClientPlatform~S` path, sha256 `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177`). **Since REFRESH_3 this list grew by one: `exemptions.json` moved at HEAD (`3a6d8aa89d`), and `opal_naming.py` moved again.** None is shipped; the release stays on its pins. (9 + 3 + 6 = 18.) Whether the thresholds file stays on its pin is the new open question below.

## `sources.json` that rides the release (row W88-S1's disarm, unchanged)

Pin `f043506a7c`, sha256 `b8f40af77658...`: the same blob as REFRESH_3's. Run today on these bytes, `declared_sources` returns exactly one source (the 49 Financial entry), `method_version_of` of it returns 2. The underscore-prefixed Cottonwood entry rides in the same bytes and is not a declared source (REFRESH_3, open question 1, restated below).

## Kit comparison on the kit day REFRESH_3 used (2026-10-08), DRY

**Method, same as REFRESH_3 (its harness, unchanged).** A kit `kit_new7` in the Lambda layout, outside the repo, built by `method_scripts/build_kit.py.txt`: all four members at the pins above and every other staged file at its source-map pin (checked: 15 non-member staged files equal both their recorded sha256 and the pinned blob, 0 mismatches; the 3 staged members and `handler.py` equal HEAD). The kit differs from REFRESH_3's `kit_new6` in ONE file, `account_return_daily.py` (all 19 files compared). `refresh_delta0_run.py` calls `handler.local()` for the one day in one process: S3 GETs only; the lots status write goes to a counting stub (1 stub put, 0 S3 writes). The LIVE outputs are DB-b-113's live-pinned run, REUSED as REFRESH_3 reused them: re-hashed today, 5 of 5 equal to REFRESH_3's committed `sha256_live`. The new run is also equal to REFRESH_3's new run on 5 of 5 tables.

| Table | Rows | sha256 live-pinned | sha256 four members at today's pins | Equal |
|---|---|---|---|---|
| returns | 6,901 | `9e5d6e92760d0ae2...` | `9e5d6e92760d0ae2...` | yes |
| class | 25,057 | `2028f91d7e2a652f...` | `2028f91d7e2a652f...` | yes |
| account_activity_daily | 6,901 | `f81aaa0b4f33691c...` | `f81aaa0b4f33691c...` | yes |
| account_lot_realized | 35,834 | `651421e336953941...` | `651421e336953941...` | yes |
| account_lot_unrealized_daily | 542,546 | `9e2df0d8f7fb0579...` | `9e2df0d8f7fb0579...` | yes |

Full hashes in `R45_REFRESH4_DELTA0.json`. **`kit` = {ran: true, tables: 5, tables_equal_to_live_pinned: 5}**, with the pinned 24-key thresholds file (sha256 `551920f0c364...`) staged in the kit. Run identity (new): `handler.py d95f42d54aac`, `account_return_daily.py 73361b54df39`, `account_activity_lots.py c5364a9f81f0`, `sources.json b8f40af77658`, `account_class_daily.py 2def366fb5de` (as live). Wall 956.1 s (the manifest capture ran at the same time).

**`method_version`, row by row.** The returns parquet carries the column; live and new have the same column list, their (`account_id`, `business_date`) keys align row by row, and `method_version` is 2 on every row, none null: **6,901 of 6,901 rows equal.**

**Reads made.** The kit run and the manifest capture read the served inputs for the kit day with the handler's own S3 GET and LIST calls, as REFRESH_3's did; the harness does not log them one by one, so no per-call count is stated. No write verb reached S3: the capture client raises on any write verb other than a captured `put_object`, and the data writer is stubbed. The order's BOUNDS limit AWS reads to a function read; the kit's GETs are read as inside the cell's item 2 ("exactly as REFRESH_3 ran it"). Row `IRPT_DASHBD-D2-W110-S1` files that reading.

## What changes for served objects, per key class, beyond REFRESH_3

### (a) The daily returns manifest: the `thresholds` object

Measured on the kit's OWN captured returns manifest (`manifest_capture.py` runs the kit's `handler.run_backfill()` for the one landed day against a guard client that captures `put_object` and sends nothing; 5 objects captured: returns, class, three lots manifests).

`manifest_thresholds_keys` = `tolerance`, `large_flow_share`, `plausibility_band_low`, `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims` (six; `threshold_claims` is an object of five claims, one per value).

| Fact (counts, names, booleans) | Live-pinned manifest | Candidate manifest |
|---|---|---|
| `thresholds` top-level keys | 24 | **6** |
| the five values equal to live's | n/a | yes, 5 of 5 |
| claims served, with the pinned file | none | all five `held` (the pinned file states no claims: `threshold_claims_source` resolves to `defaulted_no_claims`) |
| top-level manifest keys | 16 | 19 (the 3 R45 additions: `valuation_source`, `fee_treatment`, `price_basis`) |
| a run of 8 or more digits anywhere in `thresholds` | 3 keys carry one | none |
| other manifest fields (`rows`, both censuses, `method`, `address`, `asof`, `first_data_date`, `method_version`, `landed`, `schema_version`, ...) | | EQUAL |

### (b) Nothing else in the returns manifest moves except what REFRESH_3 already named

Comparison, 6 objects, 91 field comparisons: **86 EQUAL, 3 ADDED, 2 CHANGED, 0 REMOVED.** The 3 ADDED are REFRESH_3's. The 2 CHANGED are the derived key count (16 to 19) and `thresholds` (24 keys to 6). The class and three lots manifests and the status record are field-for-field EQUAL. REFRESH_3 read 87 EQUAL, 3 ADDED, 1 CHANGED; the difference is exactly `thresholds`.

**Readers of the dropped keys.** `deliverables/0.9.0_WK_IRPT_DASHBD~94/RETURNS_MANIFEST_READERS.json` counted 10 readers of the returns manifest, each reading a NAMED top-level key (`first_data_date`, `method_version`, `rows`, `method`) and accepting an unknown one; none of the 10 reads `thresholds`. A search of `data/assets/scripts` and `infra/aws/lambda` (native Grep, Python files, patterns `["thresholds"]`, `.get("thresholds"`) finds no reader of a served manifest's `thresholds` object: the hits are the producer's own input, the Cottonwood adapter's input and tests of the producer's own output. Limits stated: `portal/`, `mcportal/`, notebooks and an object read by key from outside the repo were not searched; the 10-reader census's own stated limit (an unlisted reader is not seen) stands.

### (c) The data tables

`kit` {ran: true, tables: 5, tables_equal_to_live_pinned: 5, reason: n/a}. Table above. The release changes no data table byte on the kit day.

## The method row (item 3)

**The release still cannot write 49 Financial's method row 2.** Three readings, all source, none of the live role:
- `handler.py` carries zero `emit_method_row(` calls (counted today on the kit's handler, 0; the one mention is the docstring at `:12-16`, which states the handler "omits the one `emit_method_row` call"), and `handler.py` is member 1 at an unchanged pin.
- The producer's `emit_method_row` callers are in its own `main()` (`:2178` for `--method-row-only`, `:2232` for the full emit) and in the Cottonwood adapter (its own scope); the Lambda calls neither.
- The role's Terraform grants `s3:PutObject` only on the five gold prefixes and "not the dim_return_method prefix" (`infra/aws/terraform/investor-reporting/reporting-gold/iam.tf:88-95`, `locals.tf:94-95`; the live IAM role was not read, as in REFRESH_3). The kit capture put 5 objects, none a method row.

**What a LATER producer `main()` upload would now write to the method manifest** (`.../dim_return_method/method_version=2/manifest.json`): the 31-column row REFRESH_3 named (dry run today with `upload=False`: 31 columns, the same list, address the producer prints for the 49 Financial entry; income pair `cash_when_received` / `held` / no reason) plus a `thresholds` object of **the same six keys** as (a), where it wrote the whole file at REFRESH_3's pin. `data.parquet` is unchanged from REFRESH_3's description (the five threshold values and their claims are columns of the row; no other threshold key is). The claims in the row depend on the thresholds file given: with the pinned package file all five `held` and `threshold_claims_source` `defaulted_no_claims`; with the tracked file `measured`, `measured`, `held`, `held`, `inferred` and `stated`. REFRESH_3's condition 5 stands: no `main()` upload under this pair unless the halves cover it.

## The thresholds file in the package (item 4) -- OPEN QUESTION 5, chosen by neither this worker nor this packet

REFRESH_3's condition 1 keeps the PINNED 24-key file (`551920f0c364...`, source-map entry 6) in the package. With DB-b-132 a manifest no longer copies the file whole, so the choice no longer decides what is served beyond the six keys; it still decides the claims and what the package carries.

| | A. Keep the pinned file (REFRESH_3's condition 1) | B. Ship the tracked file with a claim per threshold |
|---|---|---|
| File | `551920f0c364...` at pin `6be02af162` of the deleted path; 24 top-level keys | `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`, last change `aaeb1866ff`, sha256 `69e0a889a7e639336d3c01105804e05173ab49528b5882d38cf6aa94a09bad0f`; 6 top-level keys |
| Five values | as live | equal to the pinned file's on 5 of 5 (read today through `served_thresholds`) |
| Claims a returns manifest serves | all five `held` (defaulted, no claims stated) | `measured`, `measured`, `held`, `held`, `inferred` |
| The other 19 keys | staged in the package, not served | not in the package at all |
| Members | four (this packet) | five: a 5th member, and the source map's entry 6 changes (`repo_path`, `pin`, `sha256`; `packaged_as` unchanged) -- a file the apply must then re-pin |
| Measured here | the kit comparison above (tables 5 of 5, manifest six keys) | the dry reads only: the six keys and the claims. The kit was NOT run with this file, so table equality under B is NOT_ESTABLISHED by a kit run; the five values being equal is the only evidence |
| Lambda artifact | the zip carries the 24-key file (as live does) | the zip no longer carries the 19 other keys |

The halves decide. Either way a manifest already served keeps the 24 keys (next section).

## What this release does NOT do (item 5)

- It **rewrites no manifest already served.** Every returns manifest written before the release keeps the whole 24-key object, including the 2 keys that hold account-number-shaped runs (row W100-S3). Only a manifest the Lambda writes AFTER the release (a scheduled fire or a backfill day) carries six keys.
- It does **not** remove, overwrite or version-delete any prior object. Removing the prior version of an already-served manifest is a delete; that is Andrew's act and is not in this release or this pair.
- It does **not** move the method row 2 keys (above), any Cottonwood object, or any data table byte on the kit day.
- A later Cottonwood mint with this producer would serve the same six keys in its own method manifest (the adapter passes its thresholds to the same `emit_method_row`); that is its own pair and is not covered here.

## Radius, blast and rollback per key class

No new key, read or grant: no Terraform root file is edited. Writers on the handler's path, counted again at these bytes: **4 `put_object` sites serving 6 objects** (`account_return_daily.py` the returns manifest; `account_class_daily.py`; `account_activity_lots.py` three tables; `handler.py` the lots status record), the data parquet writes through the shared `lib/stream_parquet.py`. Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`; `memory_size` already 3008). Any other count is a STOP.

| Key class | Moved by the Lambda release | Rollback |
|---|---|---|
| returns manifest `.../account_return_daily/date=<d>/manifest.json` (written by a fire or a backfill) | yes: the 3 R45 keys ADDED and `thresholds` 24 to 6 keys, on a day the Lambda writes after the release | the prior S3 version of the key, restored by `copy-object` from the version id READ at that moment; a new `date=` key with no prior object is removed only after Andrew's word |
| class and three lots manifests, status record | no change in bytes on the kit day | as REFRESH_3 |
| data parquet keys | no change on the kit day (5 of 5) | prior version by `copy-object` |
| method row 2 `data.parquet`, `manifest.json` | no (the Lambda never writes them) | only a later `main()` upload moves them: capture-first, `get-bucket-versioning`, never delete (REFRESH_3, section 4) |

**Lambda rollback, per key, back to `oNgy4rnr`:** the prior function is the live one (below); artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in the lambda-artifacts bucket, base S3 version `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ` (read by REFRESH_3 at 2026-10-11T15:10Z; NOT re-read today, no object read being granted here). Route: `copy-object` of that version onto the same key, re-record the source-map entry, targeted `safe-apply` (`aws lambda update-function-code` is barred). Per member (four pins restored): `handler.py` rollback build commit `072d27a4a1`; `account_return_daily.py` pin `ba544b60646d9b96e8bf126b4a47064dba0c70f5`; `account_activity_lots.py` pin `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c`; `sources.json` pin `efeb21df7147955a64f79a4f7b7ff2cc5d3d9426`. A returns manifest rewritten after the release carries the 3 added keys and six threshold keys; restoring the prior version removes them.

Branch A and Branch B (a backfill lands a stated day and the status record drops it; a backfill refuses a day and states it) stand as REFRESH_2 and REFRESH_3 wrote them: `handler.py` and `account_activity_lots.py` are byte-equal to theirs. This cell did not re-derive them.

## Memory headroom

Live MemorySize **3008 MB**, 85 percent line **2,556.8 MB**; this packet asks for no change. Local process RSS (a laptop `handler.local()` run, NOT the Lambda's figure): REFRESH_3's candidate 1,434.5 MB, **today's candidate 1,476.6 MB** (`lots_read` 1,260.3; the manifest capture ran at the same time, RSS is per process on a shared machine). The Lambda's own figure for the new bytes is still ARGUED, not measured; the live code last measured 1,672 MB at 3008 MB (65.4 percent of the line). The first scheduled fire after release remains the acceptance read.

## What is live today (read, not assumed)

ONE `get-function-configuration` of `irpt-49f-reporting-gold-lambda` at 2026-10-11T17:03:26Z (shim `.tools/aws` from the worktree root, rc 0): **CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`**, LastModified `2026-10-09T17:32:02.000+0000`, State Active, LastUpdateStatus Successful, **MemorySize 3008**, Timeout 900. All unchanged from REFRESH_3's reads. The live state is `oNgy4rnr`, the R44 build; the R45 release is not applied.

## Open questions for the halves

This worker decides none of these. 1 to 4 carry from REFRESH_3.
1. **Is `sources.json` (with the underscore-prefixed Cottonwood entry) in the release?** Unread by every 49 Financial path, carried in the bytes; no pin without it.
2. **Are the three ADDED returns-manifest keys inside the never-widen?** The reader count is 10 with `NO_STRICT_READER`.
3. **Does the pair cover the nine new method-row-2 columns, or only the release?** The Lambda moves no method-row key; the nine reach a served object only through a later `main()` upload (REFRESH_3, question 3, unchanged).
4. **Which thresholds file does a later `main()` run be given?** It decides five of the nine row-2 values and the claims a returns manifest serves (table above).
5. **NEW. Keep the pinned 24-key file in the package, or ship the tracked file with a claim per threshold?** (A) changes nothing in the member list or the source map and serves five `held` claims; (B) adds a 5th member and re-pins the source map's entry 6, serves `measured`/`measured`/`held`/`held`/`inferred`, and drops 19 keys from the package, but has no kit run on its tables. Choose neither here.
6. **NEW. Is a returns manifest that narrows from 24 keys to 6 inside the never-widen?** It removes content from future manifests (it widens nothing); the readers of the dropped keys found are zero within the repo's Python (limits above), and the prior manifests keep the 24.

## Conditions carried from the COO half on REFRESH_3 (restated at these pins)

1. The apply builds from the four PINS above, never from HEAD, and re-reads every pin's sha256 against this packet; a member whose bytes are not the packet's, or any member OTHER than the four (or the five, if the halves choose option B) differing from live's bytes, is a STOP before upload. The non-members stay at their pins.
2. The Lambda's memory on the new bytes is argued: the apply's first act after upload is ONE dry-run invoke of the 2026-10-08 backfill, read against 2,556.8 MB and 85 percent of the 900 s timeout (765 s). OVER on either: roll back to `oNgy4rnr` by its S3 version and restore the four pins.
3. The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr` (row D2-W78-S1, the R44 acceptance). If that fire reads OVER, R44's rollback comes first and this packet is re-cut over that base.
4. The scheduled call site (`handler.py:624`) is read at the first fire after release for the three added keys, `method_version` 2 and the six-key `thresholds` object before the ledger closes.
5. No run of the producer's `main()` with upload against 49 Financial (or Cottonwood) is made under this pair unless the halves cover it (open question 3).

Apply preconditions as REFRESH_3's: ledger first, pinned to this packet's sha256; read every live worktree's `.open_deploys/`; re-read live as `oNgy4rnr` and MemorySize 3008 before upload, else STOP; upload member census against live is exactly the four; one `.tools/safe-apply.sh` by an applier the gates admit; post-apply plan `No changes`; no ad-hoc invoke beyond condition 2's one dry run. **Until both halves are signed on this packet's sha256, no apply is made.**

## COO half

Status: UNSIGNED. Reads and signs: the four members and their pins, what changed in member 2, the kit comparison and the six-key manifest, the method-row reading, open questions 1 to 6, the carried conditions. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED. Reads and signs: the narrowing (open question 6), the thresholds-file choice (question 5), the three ADDED keys (question 2) and question 3. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
