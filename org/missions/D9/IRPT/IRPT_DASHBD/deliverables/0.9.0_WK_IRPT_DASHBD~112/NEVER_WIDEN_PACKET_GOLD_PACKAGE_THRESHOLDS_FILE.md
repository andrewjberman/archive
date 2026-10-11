# Never-widen packet -- the gold Lambda's package carries a thresholds file of the five values and their claims, not the 24-key file: its own release, AFTER R45 REFRESH 4 is applied

Author `0.9.0_WK_IRPT_DASHBD~112` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-139` (cell DB-b-139, round 73). Ordered by `1.0.0_SA_CTO~DELL2` msg 5496 (its signed half on REFRESH 4, answer to question 5): "One cell in your next issuance replaces it with a file of the five values and their claims, after a kit run on that file."
This cell writes this packet and its records only. **Nothing was built, uploaded, applied or edited** under `data/`, `infra/` or `portal/`; the tracked thresholds file is NOT changed by this cell (it already holds exactly the six keys). `s3_writes: 0`: no S3 put, copy or delete, no Lambda, Terraform or IAM act, no `upload=True` call, no deploy, no push. **Both halves below are UNSIGNED.** This packet does not amend, supersede or edit REFRESH 4's packet, record or halves (`deliverables/0.9.0_WK_IRPT_DASHBD~110/`, untouched). Records, same folder: `THRESHOLDS_FILE_SWAP.json` (the criterion's record), `method_scripts/` (four scripts kept as `.txt`: REFRESH 4's `build_kit` and `dry_method`, copied unchanged, and this cell's `cmp_swap` and `build_record`). Harness reused UNCHANGED from `deliverables/0.9.0_WK_IRPT_DASHBD~92/` (`refresh_delta0_run.py`, `manifest_capture.py`). Client-data rule kept: the kit, the parquet outputs, the raw manifest capture and the logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~112/`; this packet holds counts, key names of the six-key file, hashes and booleans only. Of the old file's other 19 keys it states COUNTS only.

## READ FIRST

1. **ONE member changes: the thresholds file.** Its source-map entry is re-pinned from the 24-key blob to the tracked six-key file. Nothing else in the release moves. The four REFRESH 4 members, `handler.py`, and the 14 other staged files are byte-for-byte as REFRESH 4's kit had them (19 files compared: 18 equal, 1 differs, the thresholds file).
2. **The tracked file is already the replacement.** `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`, pin `aaeb1866ff6e06b00af7987cfd5849c4fa0e4329`, sha256 `69e0a889a7e639336d3c01105804e05173ab49528b5882d38cf6aa94a09bad0f`, top-level keys exactly `tolerance`, `large_flow_share`, `plausibility_band_low`, `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims`. Changed by this cell: no. Its five values equal the 24-key file's five on 5 of 5.
3. **Kit day 2026-10-08, run today on that file, dry: the five output tables are byte-equal to REFRESH 4's candidate run (5 of 5) and to the live-pinned run (5 of 5); `method_version` is 2 on 6,901 of 6,901 returns rows.** The thresholds object of the captured returns manifest holds the same six keys as REFRESH 4's; the five values are equal; the claims served are `measured`, `measured`, `held`, `held`, `inferred` (REFRESH 4's kit, with the 24-key file, served all five `held`).
4. **The package no longer contains 19 of its 24 keys; 3 of those 19 carry a run of 8 or more digits in a value** (none in a key name). Counts only.
5. **Order: this release is applied AFTER REFRESH 4 is applied and its first scheduled fire is read.** It does not amend REFRESH 4 and is not part of its apply.

## The one member that changes

| | Today (REFRESH 4's kit, and live) | This release |
|---|---|---|
| `repo_path` | `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json` (path deleted at HEAD; read by `git show <pin>:<path>`) | `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json` |
| `pin` | `6be02af162eaeff01ca19d2e5b228ffce6091cc7` | `aaeb1866ff6e06b00af7987cfd5849c4fa0e4329` (the commit that last changed the file; `git log -1 --format=%H -- <file>` at HEAD `d094118b07`) |
| sha256 | `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` (re-hashed today from `git show`, equal) | `69e0a889a7e639336d3c01105804e05173ab49528b5882d38cf6aa94a09bad0f` (`git show aaeb1866ff:<path>` equals the file at HEAD) |
| top-level keys | 24 (no `threshold_claims`) | 6 (the five values and `threshold_claims`) |
| `packaged_as` | `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json` | the same (unchanged) |

**The source-map entry that must be re-pinned** (`infra/aws/lambda/ci/lambda-source-map.json`, function `irpt-49f-reporting-gold-lambda`, file last changed `fde5036262` at this HEAD): the `staged_from` element at index 6 (the seventh), lines **6062 (`repo_path`), 6063 (`pin`), 6064 (`packaged_as`, unchanged), 6065 (`sha256`)** at this HEAD. Three fields change; `packaged_as` does not. The same file's `files` list (line 6011) already names the tracked path; it is not edited by this release. This cell did NOT edit the source map. The apply re-pins it as part of its own commit and re-reads the pin's sha256 against this table. If `MEASURED_THRESHOLDS_R1.json` is changed again before the apply, the pin and sha256 are re-cut and this packet re-signed.

## Kit comparison on the kit day REFRESH 4 used (2026-10-08), DRY

**Method.** Kit `kit_swap` built by REFRESH 4's `build_kit.py` (`method_scripts/build_kit.py.txt`, unchanged): every staged_from entry at its source-map pin, the three producer-side members and `handler.py` at REFRESH 4's pins; then ONE file replaced: the thresholds file, from the tracked file above. Compared with REFRESH 4's `kit_new7` over all 19 files by sha256: 18 equal, 1 differs (the thresholds file; `551920f0c364...` there, `69e0a889a7e6...` here). `refresh_delta0_run.py` calls `handler.local()` for the one day in one process: S3 GETs and LISTs only; the lots status write goes to a counting stub (1 stub put, 0 S3 writes); `manifest_capture.py` ran at the same time (5 objects captured, 5 puts captured and sent nowhere, its data writer stubbed). The live-pinned tables are DB-b-113's run (re-hashed here). The run first launched died with its shell before it read anything (empty logs) and was relaunched; nothing partial was kept.

| Table | Rows | Equal to REFRESH 4's candidate | Equal to live-pinned |
|---|---|---|---|
| returns | 6,901 | yes | yes |
| class | 25,057 | yes | yes |
| account_activity_daily | 6,901 | yes | yes |
| account_lot_realized | 35,834 | yes | yes |
| account_lot_unrealized_daily | 542,546 | yes | yes |

**`kit` = {ran: true, tables: 5, tables_equal_to_refresh4: 5, tables_equal_to_live_pinned: 5}.** Full hashes in `THRESHOLDS_FILE_SWAP.json`. Run identity: `handler.py d95f42d54aac`, `account_return_daily.py 73361b54df39`, `account_activity_lots.py c5364a9f81f0`, `sources.json b8f40af77658`, `account_class_daily.py 2def366fb5de`, thresholds file `69e0a889a7e6`. Wall 1,015.9 s, process peak 1,493.7 MB (REFRESH 4: 956.1 s, 1,476.6 MB; both runs shared the machine with the manifest capture). `method_version`: 6,901 of 6,901 rows equal to live's, value 2, none null. No table is unequal; nothing to explain.

## What changes for served objects, per key class

Measured on the kit's OWN captured returns manifest (the guard client captured `put_object` and sent nothing).

**(a) The returns manifest `thresholds` object.** `manifest_thresholds_keys` = `tolerance`, `large_flow_share`, `plausibility_band_low`, `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims` (six). Against REFRESH 4's candidate manifest: the key list is the same, the five values equal (5 of 5, and equal to live's 5 of 5), no run of 8 or more digits in it, and **the only thing that moves is `threshold_claims`**:

| Value | Claim served after REFRESH 4 alone (24-key file in the package) | Claim served after this release |
|---|---|---|
| `tolerance` | `held` | `measured` |
| `large_flow_share` | `held` | `measured` |
| `plausibility_band_low` | `held` | `held` |
| `plausibility_band_high` | `held` | `held` |
| `comparability_max_excluded_weight` | `held` | `inferred` |

Three of the five claims differ from what REFRESH 4 serves; two do not. `threshold_claims_source` for this file reads `stated` (REFRESH 4's pinned file: `defaulted_no_claims`). Every other top-level field of the returns manifest is EQUAL to REFRESH 4's candidate on 18 of 18 fields other than `thresholds`.

**(b) Nothing else.** The class and three lots manifests captured are byte-equal to REFRESH 4's candidate (4 of 4); the forced status record is byte-equal. The data tables: 5 of 5 equal, no byte moves.

**(c) The method row 2 (a later producer `main()` upload, not part of any Lambda release).** The dry read of the 49 Financial entry with this file (`upload=False`, 31 columns) carries the claims `measured`, `measured`, `held`, `held`, `inferred` with source `stated`; the Lambda never writes it (REFRESH 4, section "The method row"). REFRESH 3's condition 5 stands: no `main()` upload under this pair.

**What this release does NOT do.** It rewrites no manifest already served: every manifest written before the REFRESH 4 apply keeps the 24-key object, and every one written between the two applies keeps `held` claims. Removing a prior version is a delete and Andrew's act. It moves no data table byte on the kit day.

## What the package no longer contains

The 24-key file's keys that are not among the six: **19 keys dropped**. **3 of the 19 carry a run of 8 or more digits** (in their VALUES; none in a key name); two of them are the account-number-shaped ones row `IRPT_DASHBD-D2-W100-S3` names, the third is a decimal in a sentence. No value is printed here. The five values are kept; `threshold_claims` is the one key added. After REFRESH 4 none of the 19 is served by a manifest; after this release none rides the zip either, so the Lambda artifact stops holding the account-number-shaped runs. Objects already served keep them, and the zip already in the artifact bucket (including the prior S3 version) keeps them (below, rollback).

## Writers and readers, counted as REFRESH 4 counted them

- **Writers on the handler's path at these bytes: 4 `put_object` sites serving 6 objects** (`account_return_daily.py` the returns manifest; `account_class_daily.py`; `account_activity_lots.py` three tables; `handler.py` the lots status record), data parquet through the shared `lib/stream_parquet.py`. None is a member of this release; this release adds no writer and no key. The kit capture put 5 objects, none a method row.
- **Readers of the FILE:** in `handler.py`, `thresholds_path()` reads `THRESHOLDS_PACKAGED` (the packaged path, the one this release changes the bytes of) and falls back to `THRESHOLDS_REPO` (the deleted `0.4.0` path, absent in the zip); `load_thresholds()` refuses a file marked `SUPERSEDED` or with `comparability_max_excluded_weight` unset. Read at the replacement: neither refusal fires (no `SUPERSEDED` key; the weight is set), and the kit ran through it. 1 non-test reader under `data/assets/scripts` and `infra` outside the source map (`handler.py`); 1 test reader (`tests/test_thresholds_file_claims.py`, in the 190-test base).
- **Readers of a served manifest's `thresholds` object:** REFRESH 4's count stands, 10 readers of the returns manifest each reading a named top-level key and none reading `thresholds`; the claims are new content a reader accepts as an unknown key. Limits as REFRESH 4 stated them (`portal/`, `mcportal/`, notebooks not searched).

## Branches (both stated)

- **Branch A (a backfill lands a stated day):** the status record drops the day; no data byte differs from REFRESH 4's behaviour on the kit day; the manifest the day lands carries the six threshold keys with the three changed claims.
- **Branch B (a backfill refuses a day and states it):** the refusal and the status record are `handler.py` and `account_activity_lots.py` behaviour, byte-equal to REFRESH 4's members; the thresholds file is loaded at the start of each invocation (`handler.py:572` backfill, `:620` scheduled), before any day, and a refusal at its load (`SUPERSEDED` or unset weight) cannot occur on this file. Stated as the kit run read it; the Lambda's own run is the first fire's read.

## Rollback, per key class

No Terraform root file is edited. Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`). Any other count is a STOP.

| Key class | Moved by this release | Rollback |
|---|---|---|
| returns manifest `.../account_return_daily/date=<d>/manifest.json` written after it | yes: `threshold_claims` content (3 of 5 values' claims) | the prior S3 version of the key by `copy-object` from the version id READ at that moment; a new `date=` key with no prior object is removed only on Andrew's word |
| class and three lots manifests, status record, data parquet | no change in bytes on the kit day | prior version by `copy-object` as REFRESH 4 |
| method row 2 `data.parquet`, `manifest.json` | no (the Lambda never writes them) | only a later `main()` upload moves them: capture-first, never delete |
| the Lambda artifact `investor-reporting/irpt-reporting-gold-lambda.zip` | yes: the zip's thresholds file goes 24 keys to 6 | back to the REFRESH 4 build's S3 version, which the apply records at its own upload (read at that moment, not assumed here), re-record the source-map entry (pin `6be02af162` and sha256 `551920f0c364...` restore the 24-key file), targeted `safe-apply` (`aws lambda update-function-code` is barred). Removing the 24-key file from earlier S3 versions of the zip is a delete and not done |

## Memory headroom

Live MemorySize **3008 MB**, 85 percent line 2,556.8 MB; no change asked. Local process RSS on this kit: 1,493.7 MB (REFRESH 4's candidate 1,476.6 MB; a laptop `handler.local()` run, NOT the Lambda's figure). The file is smaller than the 24-key file; the memory difference is not measured here and is argued as nil. The first scheduled fire after this release is the acceptance read.

## What is live today (read, not assumed)

ONE `get-function-configuration` of `irpt-49f-reporting-gold-lambda` at 2026-10-11T18:23:25Z (shim `.tools/aws` from the worktree root, rc 0; an earlier read in the same session returned the same values): **CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`**, LastModified `2026-10-09T17:32:02.000+0000`, State Active, LastUpdateStatus Successful, MemorySize 3008, Timeout 900. The live state is `oNgy4rnr`, the R44 build. **Neither the R45 release (REFRESH 4) nor this swap is applied.** The sequence is therefore: R44 acceptance fire (Mon 2026-10-12 07:41 ET) -> REFRESH 4's pair signed -> REFRESH 4 applied -> its first scheduled fire read -> THIS packet's pair signed -> this release applied.

## Conditions this release inherits (restated at these pins)

1. **Pins.** The apply builds from pins, never from HEAD: REFRESH 4's four member pins (restated in its packet) plus this packet's thresholds pin `aaeb1866ff`; it re-reads every pin's sha256 against the packets; a member whose bytes differ, or any staged file other than the thresholds file differing from the REFRESH 4 build's bytes, is a STOP before upload. The non-members stay at their source-map pins.
2. **One dry-run invoke.** The apply's first act after upload is ONE dry-run invoke of the 2026-10-08 backfill, read against 2,556.8 MB and 85 percent of the 900 s timeout (765 s). OVER on either: roll back to the REFRESH 4 build by its S3 version.
3. **An applier the gates admit.** Ledger first, pinned to this packet's sha256; read every live worktree's `.open_deploys/`; re-read live as the REFRESH 4 build (its CodeSha256, read then) and MemorySize 3008 before upload, else STOP; upload member census against live is exactly one file (the thresholds file); one `.tools/safe-apply.sh`; post-apply plan `No changes`; no ad-hoc invoke beyond condition 2's.
4. **Read at the first fire.** The scheduled call site (`handler.py:624`) is read at the first fire after THIS release for the six-key `thresholds` object and its claims `measured`, `measured`, `held`, `held`, `inferred` before the ledger closes.
5. **Ordered after REFRESH 4.** This release is not applied before REFRESH 4 is applied AND its first scheduled fire is read (REFRESH 4's condition 4). It is not bundled into REFRESH 4's apply, and it does not wait on, or change, REFRESH 4's signed halves.
6. **No `main()` upload** against 49 Financial or Cottonwood under this pair.

**Until both halves are signed on this packet's sha256, no apply is made.**

## Open questions for the halves

1. Are the three claim changes (`held` to `measured`, `measured`, `inferred` on the returns manifest `thresholds`) inside the never-widen? They add stated claims to content of future manifests; they remove and widen no key.
2. Is the 24-key file's removal from the zip, with its prior zip versions left in the artifact bucket, sufficient for row W100-S3's concern, or is the prior-version removal (a delete, Andrew's act) wanted? This worker decides neither.

## COO half

Status: UNSIGNED. Reads and signs: the one member and its re-pin (by line), the kit comparison, the claims served, the 19 dropped keys (counts), writers and readers, both branches, rollback, the inherited conditions, the order after REFRESH 4. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED. Reads and signs: open questions 1 and 2, and that this release answers question 5 of REFRESH 4's half as ordered. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
