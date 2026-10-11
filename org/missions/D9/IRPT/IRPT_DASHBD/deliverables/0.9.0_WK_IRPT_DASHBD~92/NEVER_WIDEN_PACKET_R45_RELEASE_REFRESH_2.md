# Never-widen packet R45 REFRESH 2 -- ONE gold Lambda release over live `oNgy4rnr`, FOUR members at the bytes after the handler fix (IRPT_DASHBD DB-b-117)

Author `0.9.0_WK_IRPT_DASHBD~92` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-117`. Ordered by `1.0.0_SA_CTO~DELL2` rulings msg 3940 (refresh at the new bytes), msg 3999 (four members and what the packet shows) and msg 4029 (every manifest compared field by field against the live one), enrichment item E1.
This cell writes the packet and its evidence only. Nothing was built, uploaded, applied or edited under `data/`, `infra/` or `portal/`; no S3 write, vendor call or secret read. Records, same folder: `R45_REFRESH2_CENSUS.json`, `R45_REFRESH2_DELTA0.json` (the five hashes, the run identities and the manifest comparison), the harness `refresh_delta0_run.py` (DB-b-113's, copied unchanged), `manifest_capture.py` and `manifest_compare.py`, and `manifest_probe.py` (DB-b-113's probe, kept for reference, not used). Client-data rule kept: the runs' parquet outputs, the raw manifest captures and logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~92/`; this packet holds counts, sha256 and MB only.

**READ FIRST.** The four members are the same four as DB-b-113's candidate; one of them, `handler.py`, moved since (DB-b-115, `080dc90d92`: both `ard.emit_day` calls now pass `src`). Measured at those bytes: (1) the five output tables are byte-equal between the live-pinned members and HEAD's four on the 2026-10-08 kit day; (2) of the **6 objects** the handler's run writes or can write (5 manifests and the lots status record), **5 are field-for-field EQUAL** to the live ones and the sixth, the returns manifest, differs by **three ADDED keys and nothing else**: `valuation_source`, `fee_treatment`, `price_basis`. `method_version` is 2 as live, and the `method` sentence is byte-equal. **No field is REMOVED; no existing field is CHANGED.** The three ADDED keys are a widening of what the served manifest states (section "Manifest comparison"); the halves decide it. Both halves are UNSIGNED.

## Supersedes

This packet replaces both earlier packets; halves signed on either are VOID for the apply:
- `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~80/NEVER_WIDEN_PACKET_R45_RELEASE.md`, sha256 `6fb32b81aa3a245933820391577c94d28f5005e36dfe2965b5fd30fa7003e018` (the one-member packet);
- `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md`, sha256 `e258a7bb66414826e6a1150baa2ad198796f4c54d392646d38d3871f199d5313` (the four-member candidate at the pre-fix handler, whose open question 2, row `IRPT_DASHBD-D2-W88-S3`, said the returns manifest would state `absent`; DB-b-115 fixed that and this packet measures the fix).
Its census, sources.json diff and readers, radius, rollback and branches are restated below at the new bytes, re-verified (one member moved: `handler.py`).

## Census (measured from each member's LIVE PIN to HEAD)

Base: live `irpt-49f-reporting-gold-lambda`, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (ONE get-function-configuration read 2026-10-11T04:29Z: LastModified `2026-10-09T17:32:02.000+0000`, Active, Successful, **MemorySize 3008**, Timeout 900; ONE head-object: S3 version **`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`**, 218,641 bytes, metadata `content-sha256` equal to the CodeSha256 -- unchanged from DB-b-113's reads of 03:11Z). Members compared: 18 `staged_from` pins (each pin blob's sha256 equals the source map's, 18 of 18, re-checked) plus `handler.py` = 19. Since DB-b-113's census (`e9ad1812f4`) exactly ONE of the 19 moved: `handler.py`. The bundle is built from the PINS, so the release is measured from each live pin.

| Member | Live-pinned bytes (sha256 prefix) | HEAD bytes = pin (box/dell2 commit) | Commits since the live pin |
|---|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `212b6f7682bf` (R44 build `072d27a4a1`) | `d95f42d54aac` = `080dc90d92` | `4dc238fde6` DB-b-97; `39f31ab566` DB-b-104; `080dc90d92` **DB-b-115** |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `9935f5c7bcd7` (pin `ba544b6064`) | `14a6b91f5021` = `354214c55f` | `08194d1e33` **DB-b-96**; `26a3f3a38b` **DB-b-102**; `19ba6fe341` DB-b-110; `354214c55f` redaction (docstring only) |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `caf7655586b9` (pin `d18ddf000d`) | `c5364a9f81f0` = `19ba6fe341` | `19ba6fe341` DB-b-110 |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | `5dd1f367d4d0` (pin `efeb21df71`) | `b8f40af77658` = `f043506a7c` | `08194d1e33` DB-b-96; `d41d82a633` **ADVI_COTBKF CB-aq-1**; `26a3f3a38b` DB-b-102; `f043506a7c` **ADVI_COTBKF CB-au-1** |

`git log <live pin>..HEAD` over each path lists exactly these commits. The pin for `account_activity_lots.py` is now the box/dell2 commit `19ba6fe341` (DB-b-113 recorded `5d339ced5b`, the same blob). Four staged pins differ from HEAD and STAY at their pins; they are not members of this release: `lib/opal_naming.py`, `infra/logic/registry/reporting_policies.json`, `infra/logic/registry/scopes.json`, and `MEASURED_THRESHOLDS_R1.json` (no file at that repo path at HEAD; the pin blob is the pinned file). 11 staged pins equal HEAD (11 + 4 + 3 = 18); none of these moved since DB-b-113.

## sources.json: the diff, the readers, the `_commonwealth_delivery` question

Unchanged from DB-b-113, re-computed here key by key from the two blobs at HEAD. **(a) The diff, live pin `efeb21df71` to HEAD pin `f043506a7c`.** Unchanged: `schema_version`, `doc`, `_reserved_keys_comment`, `_no_firm_token_comment`, and every existing key of the custody entry (the single declared source) including its `lot_source`. Changed or removed: none. Added: in the custody entry, `valuation_source` = `custodian_reported`, `fee_treatment` = `gross_of_advisory_fees`, `price_basis` = `custodian_closing_price`, `returns_method_comment` (DB-b-96), `method_version` = 2 and `method_version_comment` (DB-b-102), six keys; a new top-level entry `_commonwealth_delivery` (underscore-prefixed) of six keys, with `method_version` = 3, `valuation_source` = `positions_x_as_traded_close`, `fee_treatment` = `net_of_fees`, `price_basis` = `as_traded` (ADVI_COTBKF CB-aq-1, CB-au-1). Text form: `git diff efeb21df71 HEAD -- data/assets/scripts/gold/irpt_reporting/sources.json`.

**(b) Readers among the bundle's 19 members: 4 of 19 read it; 14 do not; sources.json is the 19th.** `account_return_daily.py` directly (`DECLARATION` `:127`, `load_declaration` `:297-308`, `declared_sources` `:311-317`, `source_entry` `:320-324`; `method_fields`, `method_version_of`, `build_manifest` `:1795-1860` read the custody entry's method keys); `account_class_daily.py` (`:526-530`, `:600-601`), `account_activity_lots.py` (`:1038-1042`, `:1200-1204`, `:1360-1361`) and `handler.py` (`:220-225`, `:556-557`, `:600-601`, `:653-654`) through the producer's loaders. Class, lots and handler read no key the diff changed (class and lots hash equal; the handler passes the entry on to `emit_day`, which is the DB-b-115 change).

**Does the 49F run read `_commonwealth_delivery`? No, from the code.** `declared_sources` (`account_return_daily.py:311-317`) returns every top-level key whose value is an object and whose name is not underscore-prefixed; `_commonwealth_delivery` begins with an underscore, so it is never a declared source, and every 49F path takes its source through `declared_sources`. No Python file in the tree names the key. The bundle nevertheless CARRIES it, and no commit holds the 49F method fields without it (`d41d82a633` precedes `26a3f3a38b`); a file without the entry would be a NEW blob. That is the halves' question (open question 1).

## Open questions for the halves

This worker decides none of these.
1. **Is sources.json (with `_commonwealth_delivery`) in the release?** As stated in (b) above: unread by the 49F code, but carried in the same bytes as DB-b-96/102's fields.
2. **Are the three ADDED returns-manifest keys inside the never-widen?** `valuation_source`, `fee_treatment` and `price_basis` appear in the served returns manifest after the release and do not today. A reader of the manifest sees MORE stated, not different. The rows, `method_version`, the `method` sentence and every other field are byte-equal (section "Manifest comparison").

## Radius

No new key, read or grant. No Terraform root file is edited by this cell. Writers, counted again at the new bytes:
- The status key `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json` (`_lots_status_location`, `handler.py:448-451`, built by `address()`): ONE writer rule, `record_lots_status` (`:458-489`), the only `put_object` in `handler.py` (`:485`), with TWO callers: `catch_up_lots` (`:515`, scheduled fire) and `run_backfill` (`:587`, explicit `backfill` event only). The key is unchanged in bytes (DB-b-104); it never begins `date=`. **Measured on the kit day: the handler's run writes it on NEITHER the live nor the new code** (every lots day lands, nothing was stated before), so the status object is not touched by the 2026-10-08 run.
- `returns`: ONE writer rule, `account_return_daily.emit_day` (`:1863`; manifest `put_object` `:1875`, partition through `stream_parquet`), called from `handler.py:581` (backfill) and `:624` (scheduled), both passing `src=src` at HEAD. `emit_method_row` (`:1881`, manifest put `:1931`) has no caller in `handler.py` (only a docstring mention, `:16`), so `dim_return_method` is not written by this function at any member's bytes.
- `class`: ONE writer rule, `account_class_daily.emit_class_day` (`:569`, manifest put `:593`), called at `handler.py:304`. Lots tables: ONE writer rule, `account_activity_lots.emit_day` (`:1318`, manifest put `:1352`), called only from `emit_lots` (`handler.py:430`), once per table (three).
- **Count of writers, again: 4 `put_object` sites on the handler's path (`account_return_daily.py:1875`, `account_class_daily.py:593`, `account_activity_lots.py:1352`, `handler.py:485`), serving 6 objects (the lots site serves three tables).** The measured run put 5 objects on each side (the status record is the sixth, written on neither).
- sources.json is read-only data in the bundle: it adds no writer, key, prefix or action. This release adds no write to any `date=` key and no new object, prefix, action or read.
- Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`; `memory_size` already 3008). Any other count is a STOP.

## Branch A

A backfill lands a stated day and the status record drops it. Producer rule at HEAD: `run_backfill` (`handler.py:546-590`) calls `emit_lots` (`:586`); `lots_days` (`:380-409`) returns the day's rows; `emit_lots` (`:412-439`) writes the three tables with the activity table LAST; the day is then in `lots_written`. `record_lots_status(s3, firm, set(lots_written), lots_failed, not dry_run)` (`:587`) keeps `kept = {prior statements for days not in landed}` (`:479`), then adds this call's failures (`:480`).
- A statement existed for that day: `prior` is read from the status object (`:474-477`); the landed day leaves `kept`; one `put_object` (`:485`) overwrites the object with that day removed (an empty `statements` list if nothing else is owed).
- No statement existed (absent object, `NoSuchKey`, is an empty prior `:476-478`) and nothing refused: `if not kept and not prior: return {}` (`:481-482`): NOTHING is written, the key stays absent. This is the case measured on the kit day.
- Dry run (`upload` False): `if aal is None or not upload: return None` (`:465-466`): nothing read or written.
- A statement for a day the backfill did NOT land stays (`:479`). The returns and class partitions are written before the lots stage (`:577-585`).
Branch A is stated from the handler's rule and no other member changes it. The returns manifest a backfill writes is the one in "Manifest comparison".

## Branch B

A backfill refuses a day and the status record states it. Producer rule: a repeat of the realized key on the final rows raises `SystemExit("REFUSED: realized lot id ... repeats ...")` (`account_activity_lots.py:317-327` `check_realized_unique`, called at `:374` and `:1094`). `lots_days` catches `(Exception, SystemExit)` (`handler.py:396`) and returns the reason for EVERY day of the producer call (`:397-398`): one producer call covers all the backfill's days, so all are refused together. `emit_lots` prints `LOTS_SKIPPED <day> <reason>` (`:437-438`) and writes nothing to any lot table for them.
- STATEMENT: `record_lots_status` (`:587`) writes the one object, one entry per refused day, `text` = `lots not computed for <date>: <reason>` (`lots_status_statement`, `:454-455`), reason cut to 300 characters (`:397`), via the single `put_object` (`:485`); at most `MAX_BACKFILL_DAYS` = 25 days (`:119`). A failed read or write is logged by name (`LOTS_STATUS_READ_SKIPPED` `:478`, `LOTS_STATUS_WRITE_FAILED` `:488`) and never raises. **The record's shape (`statements`: `date`, `reason`, `text`; one key) was captured on both kits by a forced refusal and is field-for-field EQUAL, same object key.**
- RETURNS AND CLASS STILL LAND: `run_backfill` writes the returns days (`:578-584`) and the class days (`:585`) before the lots stage; the lots functions never raise; the return value carries `lots_failed` (`:588-590`).
- Limit stated, not hidden: a backfill rewrites landed days, so a day it refuses is NOT owed again by the scheduled catch-up (`class_owed_days`, `:322-338`); its statement stays until a later backfill that lands that day drops it (Branch A).

## Rollback

Per key, back to `oNgy4rnr`:
- Lambda function: the prior function is the live one, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`, artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in `opal-313476888478-lambda-artifacts`, base S3 version **`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`** (head-object read 2026-10-11T04:29Z, latest at that read, LastModified `2026-10-09T14:29:21+00:00`). Route: `copy-object` of that version onto the same key, re-record the source map entry, targeted `safe-apply` (`aws lambda update-function-code` is barred).
- **Per member (four pins restored, with the S3 version restoring the artifact):**
  - `handler.py`: no source-map pin; the build takes it from the build commit's tree; rollback build commit `072d27a4a1` (blob `7c9bb9dcdc5b`, sha256 `212b6f7682bf...`).
  - `account_return_daily.py`: pin restored to `ba544b60646d9b96e8bf126b4a47064dba0c70f5` (sha256 `9935f5c7bcd7...`).
  - `account_activity_lots.py`: pin restored to `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c` (sha256 `caf7655586b9...`).
  - `sources.json`: pin restored to `efeb21df7147955a64f79a4f7b7ff2cc5d3d9426` (sha256 `5dd1f367d4d0...`).
  The S3 version copy is what puts the old bytes back; the pins are the source map's record of what the artifact holds.
- Status key `_status/lots_not_computed.json`: not written by the kit-day run on either code; the apply cell reads the prefix first. If a fire or backfill writes it, restore its prior version by `copy-object`; with no prior version, removal is an S3 delete, a human-confirmed act after Andrew's word. 0 served readers.
- Lot, returns and class partitions (and their manifests) of any day a released backfill rewrites: prior versions restored by `copy-object` from the version id read at that moment; a new `date=` key with no prior object is removed by an S3 delete after Andrew's word. A returns manifest rewritten after the release carries the three ADDED keys; restoring the prior version removes them.

## Memory headroom

Setting: live MemorySize **3008 MB** (applied 2026-10-09T17:32:02Z; confirmed by this cell's get-function-configuration); 85 percent line **2,556.8 MB**. This packet asks for no change of the limit.
The two kinds of figure, kept apart:
- **The Lambda's own (REPORT lines, measured on the LIVE code `oNgy4rnr`, pre-cut; carried from DB-b-113's packet, not re-measured here):** at 3008 MB, dry run of the 2026-10-08 backfill (request `ecfbecbd`): Max Memory Used **1,672 MB** = 65.4 percent of the line; headroom 884.8 MB to the line. At 2048 MB (DB-b-107): 1,685 MB. No Lambda run exists on the new bytes.
- **Local process RSS (Windows working set, a laptop `handler.local()` run; NOT the Lambda's figure and not comparable to it by ratio):** live-pinned members **1,691.1 MB** (`lots_read` 1,691.1; DB-b-113's run, reused); HEAD's four members **1,458.6 MB** (`lots_read` 1,247.3), a fall of 232.5 MB. The new run shared the machine with the two manifest captures (RSS is per process); the live run shared it with another run. The handler fix adds no stage: its change is an argument on two calls.
Statement: the new members' local peak is lower than the live members' by 232.5 MB (DB-b-113: 231.5; DB-b-110: 266.1). The Lambda figure for the new bytes is ARGUED, not measured: the live code already sat 884.8 MB under the 85 percent line and the local peak fell, so the new code is expected below 1,672 MB. The first scheduled fire after the release remains the acceptance read.

## DELTA=0 evidence

Kit day 2026-10-08; thresholds sha256 `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` in both runs (pinned blob `6be02af162`, verified before use). Run identities:
- LIVE (DB-b-113's run, reused; its five outputs re-hashed in this session, 5 of 5 equal to the committed `sha256_live`): kit code sha256 prefixes `handler.py 212b6f7682bf`, `account_return_daily.py 9935f5c7bcd7`, `account_activity_lots.py caf7655586b9`, `sources.json 5dd1f367d4d0`.
- NEW (this cell, one run, 889.9 s): kit `kit_new5` outside the repo in the Lambda layout, `handler.py d95f42d54aac`, `account_return_daily.py 14a6b91f5021`, `account_activity_lots.py c5364a9f81f0`, `sources.json b8f40af77658`; `account_class_daily.py 2def366fb5de` and the thresholds identical in both; every other member as pinned (checked by sha256 against the live kit). The status write went to a counting stub (1 stub put, no S3 write).

| Table | Rows | sha256 live-pinned | sha256 four-member HEAD | Equal |
|---|---|---|---|---|
| returns | 6,901 | `9e5d6e92760d0ae2...` | `9e5d6e92760d0ae2...` | yes |
| class | 25,057 | `2028f91d7e2a652f...` | `2028f91d7e2a652f...` | yes |
| account_activity_daily | 6,901 | `f81aaa0b4f33691c...` | `f81aaa0b4f33691c...` | yes |
| account_lot_realized | 35,834 | `651421e336953941...` | `651421e336953941...` | yes |
| account_lot_unrealized_daily | 542,546 | `9e2df0d8f7fb0579...` | `9e2df0d8f7fb0579...` | yes |

Full hashes in `R45_REFRESH2_DELTA0.json`; `output_hash_equal` is **true**; `members_at_head` names the four paths.

## Manifest comparison

**Method.** The objects were enumerated from the code (section "Radius": 4 `put_object` sites, 6 objects) and then CAPTURED live and new by running each kit's OWN `handler.run_backfill()` (the handler's real path, so the arguments to `ard.emit_day`, `acd.emit_class_day` and `aal.emit_day` are the ones each handler actually passes; HEAD's passes `src=src`, the live one passes none) for the one landed day 2026-10-08, accounts = population, against a guard client that delegates S3 reads and CAPTURES every `put_object` (never sent), with the shared data write (`stream_to_parquet`) replaced by a stub. Each side put **5 objects** (returns, class, three lots tables) and no other. The status record, which the run does not write, was captured by calling each kit's own `record_lots_status` once with a forced refusal. **Denominator: 6 objects compared (5 manifests + 1 status record), 91 field comparisons (the manifest keys plus 3 derived fields per object: its object key, a key-equal flag and its key count): 87 EQUAL, 3 ADDED, 1 CHANGED (a derived key count), 0 REMOVED.**

| Object | Fields compared | EQUAL | ADDED | CHANGED | REMOVED |
|---|---|---|---|---|---|
| `account_return_daily` manifest | 22 (19 keys + 3 derived) | 18 | 3 | 1 (derived key count) | 0 |
| `account_class_daily` manifest | 17 | 17 | 0 | 0 | 0 |
| `account_activity_daily` manifest | 16 | 16 | 0 | 0 | 0 |
| `account_lot_realized` manifest | 16 | 16 | 0 | 0 | 0 |
| `account_lot_unrealized_daily` manifest | 16 | 16 | 0 | 0 | 0 |
| `lots_not_computed.json` status record (forced-refusal shape) | 4 | 4 | 0 | 0 | 0 |

**What a reader of the served returns manifest will see differ after the release:**

| Field | Live manifest | After the release | Verdict | Tied to |
|---|---|---|---|---|
| `valuation_source` | no such key | `custodian_reported` | ADDED | DB-b-96 `08194d1e33` (reads it from the source entry; sources.json declares it) with DB-b-115 `080dc90d92` (the handler passes `src`) |
| `fee_treatment` | no such key | `gross_of_advisory_fees` | ADDED | same |
| `price_basis` | no such key | `custodian_closing_price` | ADDED | same |
| (key count, derived) | 16 | 19 | CHANGED | exactly the three ADDED keys |

Everything else in the returns manifest is EQUAL, including `method_version` **2 as live** (the DB-b-113 finding was `absent`; DB-b-115 closes it), the `method` sentence (byte-equal: it states the custodian method, GROSS of advisory fees, because the entry's `valuation_source` is `custodian_reported`), `rows`, the two censuses, `first_data_date` (equal by sha256; it is account-keyed), `thresholds` (equal by sha256), `address`, `asof`, `schema_version`, `source_pipeline`, `calendar_source`, `carried_days`. The class and the three lots manifests are field-for-field EQUAL, including `method_version` (1 for class, 3 for lots), their censuses and primary keys.

**This is a widening of what the served manifest states** (three keys appear where none existed), not a change of any served number or of any key already served. The halves decide whether it is inside the never-widen (open question 2). Limits stated: the data write is stubbed on both sides, so the `landed` field reads equal by construction (the data bytes are carried by the table hashes above); the scheduled call site `handler.py:624` was not exercised, but it is the same expression as `:581` (`first_data_date=first_seen, src=src`) over the same `src` resolved the same way (`:601`, as `:557`); the live handler's `run_backfill` does not call `record_lots_status` (DB-b-97 added it), so the status record was compared by calling each kit's function directly, not through the backfill.

## COO half

Status: UNSIGNED.

Reads and signs: the census (four members over `oNgy4rnr`, each pinned to HEAD bytes with its commits since the live pin), the sources.json diff, readers and the `_commonwealth_delivery` question (open question 1), the radius, the per-member rollback and the memory statement. Stamp and date go here when signed. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED.

Reads and signs: both branches (A and B) with the stated limit on a refused backfill day, the per-key and per-member rollback, the DELTA=0 evidence (five hashes equal) and the manifest comparison, including the three ADDED returns-manifest keys as a widening (open question 2). Stamp and date go here when signed. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
