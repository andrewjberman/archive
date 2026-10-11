# Never-widen packet R45 REFRESH -- ONE gold Lambda release over live `oNgy4rnr`, FOUR members at the new source bytes: handler.py, account_return_daily.py, account_activity_lots.py and sources.json (IRPT_DASHBD DB-b-113, AMENDMENT 1)

Author `0.9.0_WK_IRPT_DASHBD~88` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-113`. Ordered by `1.0.0_SA_CTO~DELL2` ruling msg 3940 (on ADDENDUM 20: the stage cut rides R45), enrichment item E1; shaped by AMENDMENT 1 (issuer `2.0.0_SA_COO~D2`, ruling on row `IRPT_DASHBD-D2-W88-S1`) and the CTO's addition msg 3999 (sources.json diff, reader count, per-member rollback).
This cell writes the packet and its evidence only. Nothing was built, uploaded, applied or edited under `data/`, `infra/` or `portal/`. Records, same folder: `R45_REFRESH_CENSUS.json`, `R45_REFRESH_DELTA0.json`, the harness `refresh_delta0_run.py`, the manifest probe `manifest_probe.py`. Client-data rule kept: the runs' parquet outputs and logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~88/`; this packet holds counts, sha256 and MB only.

**READ FIRST -- what the third run shows.** With all FOUR members at HEAD (sources.json at HEAD `f043506a7c`), every other member as pinned, the five output tables are hash-EQUAL to the live-pinned run on the 2026-10-08 kit day, `returns` included (section "DELTA=0 evidence"). The earlier three-member run (sources.json left at its live pin) differed in `returns` by one column, `method_version`; that is why sources.json is the fourth member, and the record keeps that run under `three_member_run`. Two things are NOT settled by the hashes and are the halves' to answer (section "Open questions for the halves"): (1) the returns MANIFEST says the literal `absent` for `method_version` and the three method fields where the live code writes `method_version` 2 (measured; row `IRPT_DASHBD-D2-W88-S3`); (2) sources.json carries ADVI_COTBKF's `_commonwealth_delivery` entry, which the 49F code never reads. Both halves are UNSIGNED.

## Supersedes

This packet replaces `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~80/NEVER_WIDEN_PACKET_R45_RELEASE.md`, sha256 `6fb32b81aa3a245933820391577c94d28f5005e36dfe2965b5fd30fa7003e018` (read in the first session of this order). That packet's census showed ONE member (`handler.py`); staged members have moved since (DB-b-110, drained `@5d339ced5b`; the redaction `@354214c55f`; DB-b-96 and DB-b-102 in the producer and its declaration). Per CTO msg 3940, halves signed on the old packet are VOID for the apply. Its Branch A, Branch B, rollback and radius are restated below at the new bytes. This file also replaces the earlier (three-member) text of this same refresh packet, which carried the open question that AMENDMENT 1 has ruled.

## Census (measured from each member's LIVE PIN to HEAD)

Base: live `irpt-49f-reporting-gold-lambda`, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (get-function-configuration read 2026-10-11T03:11Z: LastModified `2026-10-09T17:32:02.000+0000`, Active, Successful, **MemorySize 3008**, Timeout 900). Members compared: 18 `staged_from` pins (each pin blob's sha256 equals the source map's, 18 of 18) plus `handler.py` = 19. The bundle is built from the PINS, so what the release changes is measured from each live pin.

| Member | Live-pinned bytes (sha256 prefix) | HEAD bytes = pin (box/dell2 commit) | Commits since the live pin |
|---|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `212b6f7682bf` (R44 build `072d27a4a1`) | `ae334f6117b5` = `98ae364e98` | `4dc238fde6` DB-b-97; `39f31ab566` DB-b-104 |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `9935f5c7bcd7` (pin `ba544b6064`) | `14a6b91f5021` = `354214c55f` | `08194d1e33` **DB-b-96**; `26a3f3a38b` **DB-b-102**; `19ba6fe341` DB-b-110; `354214c55f` redaction (docstring only) |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `caf7655586b9` (pin `d18ddf000d`) | `c5364a9f81f0` = `5d339ced5b` | `19ba6fe341` DB-b-110 |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | `5dd1f367d4d0` (pin `efeb21df71`) | `b8f40af77658` = `f043506a7c` | `08194d1e33` DB-b-96; `d41d82a633` **ADVI_COTBKF CB-aq-1**; `26a3f3a38b` DB-b-102; `f043506a7c` **ADVI_COTBKF CB-au-1** |

Read from the diffs: `handler.py` and `account_activity_lots.py` carry only the expected commits. `account_return_daily.py` and `sources.json` carry commits outside DB-b-97 / DB-b-104 / DB-b-110 / redaction (DB-b-96, DB-b-102, and for sources.json the two ADVI_COTBKF commits); the issuer ruled in AMENDMENT 1 that DB-b-96 and DB-b-102 changed the two files as one unit, so the candidate carries both. Whether R45 ships four members is for the halves.
Four staged pins differ from HEAD and STAY at their pins; they are not members of this release: `lib/opal_naming.py`, `reporting_policies.json` (the two the old census named) and, new since it, `infra/logic/registry/scopes.json` and `MEASURED_THRESHOLDS_R1.json` (no file at that repo path at HEAD; the pin blob is the pinned file). 11 staged pins equal HEAD (11 + 4 + 3 = 18). Row `IRPT_DASHBD-D2-W88-S2`.

## sources.json: the diff, the readers, the `_commonwealth_delivery` question

**(a) The full diff, live pin `efeb21df71` to HEAD pin `f043506a7c`, entry by entry** (computed key by key; text form: `git diff efeb21df71 HEAD -- data/assets/scripts/gold/irpt_reporting/sources.json`). Unchanged: `schema_version`, `doc`, `_reserved_keys_comment`, `_no_firm_token_comment`, and every existing key of the custody entry including its `lot_source`. Changed or removed: none. Added:
- In the custody entry (the single declared source): `valuation_source` = `custodian_reported`, `fee_treatment` = `gross_of_advisory_fees`, `price_basis` = `custodian_closing_price` (DB-b-96 `08194d1e33`); `returns_method_comment` (same commit); `method_version` = 2 and `method_version_comment` (DB-b-102 `26a3f3a38b`). Six keys.
- A new top-level entry `_commonwealth_delivery` (underscore-prefixed): `registry_key`, `valuation_source` = `positions_x_as_traded_close`, `fee_treatment` = `net_of_fees`, `price_basis` = `as_traded`, `entry_comment` (ADVI_COTBKF CB-aq-1 `d41d82a633`); `method_version` = 3 (ADVI_COTBKF CB-au-1 `f043506a7c`). Six keys.

**(b) Readers of sources.json among the bundle's members.** Members searched: **19** (18 staged pins plus `handler.py`; the pattern `sources.json | load_declaration | declared_sources | source_entry | DECLARATION` over the bytes as packaged). **4 of 19 read it; 14 do not; sources.json is the 19th.**
| Reader | File and line | Moved by `_commonwealth_delivery`? | Moved by the other changed entries? |
|---|---|---|---|
| `account_return_daily.py` (direct) | `DECLARATION` `:127`, `load_declaration` `:297-308`, `declared_sources` `:311-317`, `source_entry` `:320-324`, `main` `:1976-1983` | no | YES: `method_fields`, `method_version_of`, `build_manifest`, `emit_method_row` (`:1795-1823`, `:1842-1860`, `:1889`) read `valuation_source`, `fee_treatment`, `price_basis`, `method_version`; the row column `method_version` comes from the entry |
| `account_class_daily.py` (via the producer's loaders) | `:526-530`, `:600-601` | no | no (refuses unless exactly one declared source, `:527-528`; reads trade tokens by name) |
| `account_activity_lots.py` (via the loaders) | `:1038-1042`, `:1200-1204`, `:1360-1361`; `lot_spec` `:108` | no | no (refuses unless exactly one declared source, `:1040`, `:1202`; reads `lot_source` and trade tokens by name) |
| `handler.py` (via the loaders) | `:220-225`, `:555-556`, `:597-598`, `:649-650` | no | no for the compute path; it passes no `src` to `emit_day` (`:579`, `:620`) |
The 14 non-readers: `etf_classifications_dynamodb.py`, `stream_parquet.py`, `trading_calendar.py`, the transaction-code classification JSON, `MEASURED_THRESHOLDS_R1.json`, `NAMING_SCHEMA.json`, and the seven `infra/logic/registry` JSON files; `lib/opal_naming.py` has 7 hits on a DIFFERENT file (the registry `resources.json`), not on sources.json.

**Does the 49F run read the `_commonwealth_delivery` entry? No, from the code.** `account_return_daily.py:311-317` `declared_sources(doc)` returns "every top-level key whose value is an OBJECT and whose name is not underscore-prefixed". `_commonwealth_delivery` (sources.json `:123`) begins with an underscore, so it is never a declared source. Every 49F path takes its source through `declared_sources`: `handler.py:221-225` (`compute`, which also refuses unless exactly one source is declared, `:222`), `:556`, `:598`, `:650`; `account_class_daily.py:527-530`; `account_activity_lots.py:1039-1042`, `:1201-1204`, `:1361`. `source_entry` (`account_return_daily.py:320-324`) refuses a name that is not in `declared_sources`. No Python file in the `irpt_reporting` tree and no handler line names the key; its only occurrence is `sources.json:123` itself. The measured result agrees: class and the lots tables hash equal on the four-member run.

## Open questions for the halves

This worker decides none of these.
1. **Is sources.json (with `_commonwealth_delivery`) in the release?** The 49F code is not moved by the ADVI_COTBKF entry, but the bundle would CARRY it, and it ships in the same bytes as DB-b-96/102's fields. **No commit in sources.json's history holds the 49F method fields without that entry:** the entry arrived at `d41d82a633` (2026-10-09 10:36 -0400), before `method_version` arrived at `26a3f3a38b` (11:17). The earliest commit holding the three fields without the entry is `08194d1e33` (it has no `method_version`, so HEAD's producer would read none from it; not run). A four-field file without the entry would be a NEW blob, not a commit that exists.
2. **The returns MANIFEST (row `IRPT_DASHBD-D2-W88-S3`).** Measured, not argued (`R45_REFRESH_DELTA0.json` `manifest_method_fields`; `manifest_probe.py` calls each kit's own `emit_day` with the arguments `handler.py:579` and `:620` pass, no `src`, against a capturing stub): LIVE writes `method_version` 2 and has no key for `valuation_source`, `fee_treatment`, `price_basis`; the FOUR-member candidate (and the three-member one) writes the literal `absent` for all four, and its `method` sentence states the formula with the three fields as `absent` and no custodian claim. Moving sources.json does not change this, because the handler passes no `src`. The returns ROWS are unaffected (hash-equal). Is a manifest that says `absent` where the live one said 2 inside the never-widen?

## Radius

No new key, read or grant. No Terraform root file is edited by this cell. Writers, counted again at the new bytes:
- The status key `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json` (`_lots_status_location`, `handler.py:448-451`, built by `address()`): ONE writer rule, `record_lots_status` (`:458-490`), the only `put_object` in `handler.py` (`:485`), with TWO callers: `catch_up_lots` (`:515`, scheduled fire) and `run_backfill` (`:585`, explicit `backfill` event only). Same key, same `PutObject`, same prefix as before; the key is unchanged in bytes (DB-b-104). It never begins `date=`.
- `returns`: ONE writer rule, `account_return_daily.emit_day` (`:1863`; manifest `put_object` `:1875`, partition through `stream_parquet`), called from `handler.py:579` (backfill) and `:620` (scheduled). `emit_method_row` (`:1881`, manifest put `:1931`) has no caller in `handler.py`, so `dim_return_method` is not written by this function at any member's bytes.
- `class`: ONE writer rule, `account_class_daily.emit_class_day` (`:569`, manifest put `:593`), called at `handler.py:304` inside `emit_classes` (`:295`). Lots tables: ONE writer rule, `account_activity_lots.emit_day` (`:1318`, manifest put `:1352`), called only from `emit_lots` (`handler.py:430`).
- sources.json is read-only data in the bundle: it adds no writer, key, prefix or action. This release adds no write to any `date=` key and no new object, prefix, action or read. DB-b-110 changes how the lots read converts frames (arrow mask first), not what it reads or writes.
- Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`; `memory_size` already 3008 and in the config, so no memory change). Any other count is a STOP.

## Branch A

A backfill lands a stated day and the status record drops it. Producer rule at HEAD: `run_backfill` (`handler.py:546-589`) calls `emit_lots` (`:584`); `lots_days` (`:380-409`) returns the day's rows; `emit_lots` (`:412-445`) writes the three tables with the activity table LAST; the day is then in `lots_written`. `record_lots_status(s3, firm, set(lots_written), lots_failed, not dry_run)` (`:585`) keeps `kept = {prior statements for days not in landed}` (`:479`), then adds this call's failures (`:480`).
- A statement existed for that day: `prior` is read from the status object (`:474-477`); the landed day leaves `kept`; one `put_object` (`:485`) overwrites the object with that day removed (an empty `statements` list if nothing else is owed).
- No statement existed (absent object, `NoSuchKey`, is an empty prior `:476-478`) and nothing refused: `if not kept and not prior: return {}` (`:481-482`): NOTHING is written, the key stays absent.
- Dry run (`upload` False): `if aal is None or not upload: return None` (`:465-466`): nothing read or written.
- A statement for a day the backfill did NOT land stays (`:479`). The returns and class partitions are written before the lots stage (`:577-583`), unchanged by this branch.
Branch A is stated from the handler's rule and is not changed by the other members. A backfill that rewrites returns days writes them with the HEAD producer and the HEAD declaration: the rows are hash-equal on the kit day, and the manifest is the one described in open question 2.

## Branch B

A backfill refuses a day and the status record states it. Producer rule: a repeat of the realized key on the final rows raises `SystemExit("REFUSED: realized lot id ... repeats ...")` (`account_activity_lots.py:325-327` in `check_realized_unique`, called at `:374` and `:1094`). `lots_days` catches `(Exception, SystemExit)` (`handler.py:396`) and returns the reason for EVERY day of the producer call (`:397-398`): one producer call covers all the backfill's days, so all are refused together. `emit_lots` prints `LOTS_SKIPPED <day> <reason>` (`:437-438`) and writes nothing to any lot table for them.
- STATEMENT: `record_lots_status` (`:585`) writes the one object, one entry per refused day, `text` = `lots not computed for <date>: <reason>` (`lots_status_statement`), reason cut to 300 characters (`:397`), via the single `put_object` (`:485`); at most `MAX_BACKFILL_DAYS` = 25 days (`:119`). A failed read or write is logged by name (`LOTS_STATUS_READ_SKIPPED` `:478`, `LOTS_STATUS_WRITE_FAILED` `:488`) and never raises.
- RETURNS AND CLASS STILL LAND: `run_backfill` writes the returns days (`:578-581`) and the class days (`:583`) before the lots stage; the lots functions never raise; the return value carries `lots_failed` (`:586-589`).
- Limit stated, not hidden: a backfill rewrites landed days, so a day it refuses is NOT owed again by the scheduled catch-up (`class_owed_days`, `:322-338`); its statement stays until a later backfill that lands that day drops it (Branch A).

## Rollback

Per key, back to `oNgy4rnr`:
- Lambda function: the prior function is the live one, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`, artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in `opal-313476888478-lambda-artifacts`, S3 version **`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`** (head-object read 2026-10-11T03:11Z, latest at that read, LastModified `2026-10-09T14:29:21+00:00`, 218,641 bytes, metadata `content-sha256` equal to the CodeSha256). Route: `copy-object` of that version onto the same key, re-record the source map entry, targeted `safe-apply` (`aws lambda update-function-code` is barred).
- **Per member (four members; three source-map pins restored plus handler.py's build commit, with the S3 version restoring the artifact):**
  - `handler.py`: no source-map pin; the build takes it from the build commit's tree; rollback build commit `072d27a4a1` (blob `7c9bb9dcdc5b`, sha256 `212b6f7682bf...`).
  - `account_return_daily.py`: pin restored to `ba544b60646d9b96e8bf126b4a47064dba0c70f5` (sha256 `9935f5c7bcd7...`).
  - `account_activity_lots.py`: pin restored to `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c` (sha256 `caf7655586b9...`).
  - `sources.json`: pin restored to `efeb21df7147955a64f79a4f7b7ff2cc5d3d9426` (sha256 `5dd1f367d4d0...`).
  The S3 version copy is what puts the old bytes back; the pins are the source map's record of what the artifact holds (restored if the apply moves them).
- Status key `_status/lots_not_computed.json`: its state now is UNREAD by this cell; the apply cell reads the prefix first. If a fire or backfill writes it, restore its prior version by `copy-object`; with no prior version, removal is an S3 delete, a human-confirmed act after Andrew's word. 0 served readers.
- Lot partitions, returns and class partitions (and their manifests) of any day a released backfill rewrites: prior versions restored by `copy-object` from the version id read at that moment; a new `date=` key with no prior object is removed by an S3 delete after Andrew's word.

## Memory headroom

Setting: live MemorySize **3008 MB** (memory-step record `0.9.0_WK_IRPT_DASHBD~87/MEMSTEP_APPLY_RECORD.json`, applied 2026-10-09T17:32:02Z); 85 percent line **2,556.8 MB**. The halves forbid raising a limit; this packet asks for none.
The two kinds of figure, kept apart:
- **The Lambda's own (REPORT lines, measured on the LIVE code `oNgy4rnr`, pre-cut):** at 3008 MB, dry run of the 2026-10-08 backfill (request `ecfbecbd`): Max Memory Used **1,672 MB** = 65.4 percent of the line, 55.6 percent of the size; headroom 884.8 MB to the line. At 2048 MB (DB-b-107): 1,685 MB. No Lambda run exists on the new bytes.
- **Local process RSS (Windows working set, a laptop `handler.local()` run; NOT the Lambda's figure and not comparable to it by ratio):** DB-b-110 (`0.9.0_WK_IRPT_DASHBD~85/STAGE_MEMORY.json`): process peak 1,725.2 -> 1,459.1 MB, `lots_read` stage 1,725.2 -> 1,263.3 MB. This cell, same method: live-pinned members **1,691.1 MB** (`lots_read` 1,691.1); three-member run 1,467.2 MB (`lots_read` 1,257.0); **four-member run 1,459.6 MB** (`lots_read` 1,256.1), a fall of 231.5 MB from the live-pinned members. The four-member run ran alone; the live and three-member runs shared the machine (RSS is per process). The HEAD members include DB-b-96/102 and the sources.json fields (returns stage peaks 230.2 live, 237.9 four-member).
Statement: the new members' local peak is lower than the live members' in DB-b-110's run and in this cell's, by 266.1 and 231.5 MB; the added `record_lots_status` call is about 0.05 MB (old packet's micro-measurement, same code). The Lambda figure for the new bytes is ARGUED, not measured: the live code already sat 884.8 MB under the 85 percent line and the local peak fell, so the new code is expected below 1,672 MB. The first scheduled fire after the release remains the acceptance read.

## DELTA=0 evidence

Kit day 2026-10-08; thresholds sha256 `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` in all runs (pinned blob `6be02af162`, verified before use; DB-b-110's private copy (row D2-W85-S1) has the SAME sha256). Method: DB-b-110's harness adapted in `refresh_delta0_run.py`; kits in the Lambda layout outside the repo (LIVE: `handler.py` from `072d27a4a1`, the producers and sources.json from their live pins; NEW: the four members at HEAD bytes); every other member as pinned; S3 GETs only; the status write to a counting stub (1 stub put in each run, no S3 write). Control: the live returns hash equals DB-b-110's recorded `sha256_before`, and the five live parquet files were re-hashed in this session and equal the committed live hashes (5 of 5).

| Table | Rows | sha256 live-pinned | sha256 four-member HEAD | Equal |
|---|---|---|---|---|
| returns | 6,901 | `9e5d6e92760d0ae2...` | `9e5d6e92760d0ae2...` | yes |
| class | 25,057 | `2028f91d7e2a652f...` | `2028f91d7e2a652f...` | yes |
| account_activity_daily | 6,901 | `f81aaa0b4f33691c...` | `f81aaa0b4f33691c...` | yes |
| account_lot_realized | 35,834 | `651421e336953941...` | `651421e336953941...` | yes |
| account_lot_unrealized_daily | 542,546 | `9e2df0d8f7fb0579...` | `9e2df0d8f7fb0579...` | yes |

Full hashes in `R45_REFRESH_DELTA0.json`; `output_hash_equal` is **true**; `members_at_head` names the four paths. Run identities: LIVE kit code sha256 prefixes `handler.py 212b6f7682bf`, `account_return_daily.py 9935f5c7bcd7`, `account_activity_lots.py caf7655586b9`, `sources.json 5dd1f367d4d0`; four-member kit `ae334f6117b5`, `14a6b91f5021`, `c5364a9f81f0`, `b8f40af77658`; `account_class_daily.py 2def366fb5de` and the thresholds identical in both. Wall 911.7 s live (shared machine), 880.2 s four-member (alone).
The earlier **three-member run** (sources.json at its live pin) is kept in the record under `three_member_run`: its `returns` hash was `a5a3921b9b99...` (not equal), the single differing column was `method_version` (2 on all 6,901 rows live, null on all 6,901 there), the other four tables equal. That is the finding that made sources.json the fourth member.
**Manifest fields as each run wrote them** (`manifest_method_fields`, measured with `manifest_probe.py`; see open question 2): live `method_version` 2, `valuation_source` / `fee_treatment` / `price_basis` not keys of the manifest; four-member `method_version` `absent`, `valuation_source` `absent`, `fee_treatment` `absent`, `price_basis` `absent` (identical in the three-member run).

## COO half

Status: UNSIGNED.

Reads and signs: the census (four members over `oNgy4rnr`, each pinned to HEAD bytes with its commits since the live pin), the sources.json diff, readers and the `_commonwealth_delivery` question, the radius, the per-member rollback and the memory statement. The COO answers open question 1 (is sources.json, with `_commonwealth_delivery`, in the release) first. Stamp and date go here when signed. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED.

Reads and signs: both branches (A and B) with the stated limit on a refused backfill day, the per-key and per-member rollback, and the DELTA=0 evidence (five hashes equal on the four-member run; the three-member run's returns difference kept beside it), including open question 2 on the returns manifest. Stamp and date go here when signed. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
