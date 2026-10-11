# Never-widen packet R45 REFRESH -- ONE gold Lambda release over live `oNgy4rnr`, refreshed at the new source bytes: DB-b-97, DB-b-104, DB-b-110, the docstring redaction AND two commits the old packet did not expect (IRPT_DASHBD DB-b-113)

Author `0.9.0_WK_IRPT_DASHBD~88` for `2.0.0_SA_COO~D2`, 2026-10-11. Order `IRPT_DASHBD.TO-DB-b-113`. Ordered by `1.0.0_SA_CTO~DELL2` ruling msg 3940 (on ADDENDUM 20: the stage cut rides R45), enrichment item E1.
This cell writes the packet and its evidence only. Nothing was built, uploaded, applied or edited under `data/`, `infra/` or `portal/`. Records, same folder: `R45_REFRESH_CENSUS.json`, `R45_REFRESH_DELTA0.json`, the harness `refresh_delta0_run.py`. Client-data rule kept: the run's parquet outputs and logs are under `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~88/`; this packet holds counts, sha256 and MB only.

**READ FIRST -- this packet does not state a clean release.** The DELTA=0 test FAILED on one of five tables: `returns` is not hash-equal between the live-pinned members and HEAD's (section "DELTA=0 evidence"). The cause is two commits in `account_return_daily.py` outside the expected set (section "Open question for the halves"). The order says: record, file a row, name the member as an open question, do not decide it. Row `IRPT_DASHBD-D2-W88-S1` (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~D2`). Neither half below should be signed as a clean never-widen until that question is answered.

## Supersedes

This packet replaces `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~80/NEVER_WIDEN_PACKET_R45_RELEASE.md`, sha256 `6fb32b81aa3a245933820391577c94d28f5005e36dfe2965b5fd30fa7003e018` (read now). That packet's census showed ONE member (`handler.py`); two staged members have moved since (DB-b-110, drained `@5d339ced5b`; the redaction `@354214c55f`). Per CTO msg 3940, halves signed on the old packet are VOID for the apply. Its Branch A, Branch B, rollback and radius are restated below at the new bytes.

## Census (measured from each member's LIVE PIN to HEAD `4597d0d2a7`)

Base: live `irpt-49f-reporting-gold-lambda`, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (get-function-configuration read 2026-10-11T03:11Z: LastModified `2026-10-09T17:32:02.000+0000`, Active, Successful, **MemorySize 3008**, Timeout 900). Members compared: 18 `staged_from` pins (each pin blob's sha256 equals the source map's, 18 of 18) plus `handler.py` = 19. The bundle is built from the PINS, so what the release changes is measured from each live pin, not from the commit before DB-b-110.

| Member | Live-pinned bytes (sha256 prefix) | HEAD bytes = pin (box/dell2 commit) | Commits since the live pin |
|---|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `212b6f7682bf` (R44 build `072d27a4a1`) | `ae334f6117b5` = `98ae364e98` | `4dc238fde6` DB-b-97; `39f31ab566` DB-b-104 |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `9935f5c7bcd7` (pin `ba544b6064`) | `14a6b91f5021` = `354214c55f` | `08194d1e33` **DB-b-96**; `26a3f3a38b` **DB-b-102**; `19ba6fe341` DB-b-110; `354214c55f` redaction (docstring only) |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `caf7655586b9` (pin `d18ddf000d`) | `c5364a9f81f0` = `5d339ced5b` | `19ba6fe341` DB-b-110 |

Read from the diffs: `handler.py` and `account_activity_lots.py` carry only the expected commits. `account_return_daily.py` carries **two executable changes outside DB-b-97 / DB-b-104 / DB-b-110 / redaction: DB-b-96 `08194d1e33` and DB-b-102 `26a3f3a38b`**. Row S1.
Five staged pins differ from HEAD and STAY at their pins; they are not members of this release: `sources.json` (pin `efeb21df71`), `lib/opal_naming.py`, `reporting_policies.json` (the three the old census named), and, new since it, `infra/logic/registry/scopes.json` and `MEASURED_THRESHOLDS_R1.json` (no file at that repo path at HEAD; the pin blob is the pinned file). 11 staged pins equal HEAD. Row `IRPT_DASHBD-D2-W88-S2`.

## Open question for the halves

`account_return_daily.py` at HEAD reads the source entry for `valuation_source`, `fee_treatment`, `price_basis` (DB-b-96) and `method_version` (DB-b-102) and writes the returns row column `method_version` from `method_version_of(src)`, which is `absent` (null) for an entry naming none. The staged `sources.json` stays at its pin, which names none. Measured on the kit day (below): the returns table changes in that one column, 2 on all 6,901 rows live, null on all 6,901 at HEAD. Read from the code, not run: `handler.py:579` and `:620` call `ard.emit_day` without `src`, so the returns manifest would also state `method_version`, `valuation_source`, `fee_treatment` and `price_basis` as the literal `absent` and word the `method` sentence without a custodian claim.
Questions this worker does not decide: (1) is `account_return_daily.py` in this release at HEAD's bytes, or does the release hold it at its live pin (`ba544b6064`) and carry only `handler.py` and `account_activity_lots.py`? Note DB-b-110's cut edits both producer files, so holding `account_return_daily.py` at its pin would leave the lots read of that file uncut; (2) if it rides at HEAD, does `sources.json` move with it (and with it `dim_return_method` row selection and the manifest fields), which widens the release past this packet's radius; (3) if neither, is a changed served `method_version` column inside the never-widen? The DELTA=0 evidence for any choice other than the one measured needs a new run.

## Radius

No new key, read or grant. No Terraform root file is edited by this cell. Writers, counted again at the new bytes (HEAD `4597d0d2a7`):
- The status key `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json` (`_lots_status_location`, `handler.py:448-451`, built by `address()`): ONE writer rule, `record_lots_status` (`:458-490`), the only `put_object` in `handler.py` (`:485`), with TWO callers: `catch_up_lots` (`:515`, scheduled fire) and `run_backfill` (`:585`, explicit `backfill` event only). Same key, same `PutObject`, same prefix as before; the key is unchanged in bytes (DB-b-104). It never begins `date=`.
- `returns`: ONE writer rule, `account_return_daily.emit_day` (`:1863`; manifest `put_object` `:1875`, partition through `stream_parquet`), called from `handler.py:579` (backfill) and `:620` (scheduled). `emit_method_row` (`:1881`, manifest put `:1931`) has no caller in `handler.py`.
- `class`: ONE writer rule, `account_class_daily.emit_class_day` (`:569`, manifest put `:593`), called at `handler.py:304` inside `emit_classes` (`:295`). Lots tables: ONE writer rule, `account_activity_lots.emit_day` (`:1318`, manifest put `:1352`), called only from `emit_lots` (`handler.py:430`).
- This release adds no write to any `date=` key and no new object, prefix, action or read. DB-b-110 changes how the lots read converts frames (arrow mask first), not what it reads or writes.
- Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version`, `source_code_hash`; `memory_size` already 3008 and in the config, so no memory change). Any other count is a STOP.

## Branch A

A backfill lands a stated day and the status record drops it. Producer rule at HEAD: `run_backfill` (`handler.py:546-589`) calls `emit_lots` (`:584`); `lots_days` (`:380-409`) returns the day's rows; `emit_lots` (`:412-445`) writes the three tables with the activity table LAST; the day is then in `lots_written`. `record_lots_status(s3, firm, set(lots_written), lots_failed, not dry_run)` (`:585`) keeps `kept = {prior statements for days not in landed}` (`:479`), then adds this call's failures (`:480`).
- A statement existed for that day: `prior` is read from the status object (`:474-477`); the landed day leaves `kept`; one `put_object` (`:485`) overwrites the object with that day removed (an empty `statements` list if nothing else is owed).
- No statement existed (absent object, `NoSuchKey`, is an empty prior `:476-478`) and nothing refused: `if not kept and not prior: return {}` (`:481-482`): NOTHING is written, the key stays absent.
- Dry run (`upload` False): `if aal is None or not upload: return None` (`:465-466`): nothing read or written.
- A statement for a day the backfill did NOT land stays (`:479`). The returns and class partitions are written before the lots stage (`:577-583`), unchanged by this branch.
Branch A is stated from the handler's rule. It is not changed by `account_return_daily.py`; but a backfill that rewrites returns days writes them with the HEAD `account_return_daily.py` (open question).

## Branch B

A backfill refuses a day and the status record states it. Producer rule: a repeat of the realized key on the final rows raises `SystemExit("REFUSED: realized lot id ... repeats ...")` (`account_activity_lots.py:325-327` in `check_realized_unique`, called at `:374` and `:1094`). `lots_days` catches `(Exception, SystemExit)` (`handler.py:396`) and returns the reason for EVERY day of the producer call (`:397-398`): one producer call covers all the backfill's days, so all are refused together. `emit_lots` prints `LOTS_SKIPPED <day> <reason>` (`:437-438`) and writes nothing to any lot table for them.
- STATEMENT: `record_lots_status` (`:585`) writes the one object, one entry per refused day, `text` = `lots not computed for <date>: <reason>` (`lots_status_statement`), reason cut to 300 characters (`:397`), via the single `put_object` (`:485`); at most `MAX_BACKFILL_DAYS` = 25 days (`:119`). A failed read or write is logged by name (`LOTS_STATUS_READ_SKIPPED` `:478`, `LOTS_STATUS_WRITE_FAILED` `:488`) and never raises.
- RETURNS AND CLASS STILL LAND: `run_backfill` writes the returns days (`:578-581`) and the class days (`:583`) before the lots stage; the lots functions never raise; the return value carries `lots_failed` (`:586-589`).
- Limit stated, not hidden: a backfill rewrites landed days, so a day it refuses is NOT owed again by the scheduled catch-up (`class_owed_days`, `:322-338`); its statement stays until a later backfill that lands that day drops it (Branch A).

## Rollback

Per key, back to `oNgy4rnr`:
- Lambda function: the prior function is the live one, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`, artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in `opal-313476888478-lambda-artifacts`, S3 version **`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`** (head-object read 2026-10-11T03:11Z, latest at that read, LastModified `2026-10-09T14:29:21+00:00`, 218,641 bytes, metadata `content-sha256` equal to the CodeSha256). Route: `copy-object` of that version onto the same key, re-record the source map entry, targeted `safe-apply` (`aws lambda update-function-code` is barred).
- The source-map pins restored: `account_return_daily.py` to `ba544b60646d9b96e8bf126b4a47064dba0c70f5` and `account_activity_lots.py` to `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c` (if the apply moves them); `handler.py` has no pin (the build takes it from the build commit's tree; the rollback build commit is `072d27a4a1`).
- Status key `_status/lots_not_computed.json`: its state now is UNREAD by this cell; the apply cell reads the prefix first. If a fire or backfill writes it, restore its prior version by `copy-object`; with no prior version, removal is an S3 delete, a human-confirmed act after Andrew's word. 0 served readers.
- Lot partitions, returns and class partitions of any day a released backfill rewrites: prior versions restored by `copy-object` from the version id read at that moment; a new `date=` key with no prior object is removed by an S3 delete after Andrew's word.

## Memory headroom

Setting: live MemorySize **3008 MB** (memory-step record `0.9.0_WK_IRPT_DASHBD~87/MEMSTEP_APPLY_RECORD.json`, applied 2026-10-09T17:32:02Z); 85 percent line **2,556.8 MB**. The halves forbid raising a limit; this packet asks for none.
The two kinds of figure, kept apart:
- **The Lambda's own (REPORT lines, measured on the LIVE code `oNgy4rnr`, pre-cut):** at 3008 MB, dry run of the 2026-10-08 backfill (request `ecfbecbd`): Max Memory Used **1,672 MB** = 65.4 percent of the line, 55.6 percent of the size; headroom 884.8 MB to the line. At 2048 MB (DB-b-107): 1,685 MB. No Lambda run exists on the new bytes.
- **Local process RSS (Windows working set, a laptop `handler.local()` run; NOT the Lambda's figure and not comparable to it by ratio):** DB-b-110 (`0.9.0_WK_IRPT_DASHBD~85/STAGE_MEMORY.json`): process peak 1,725.2 -> 1,459.1 MB, `lots_read` stage 1,725.2 -> 1,263.3 MB. This cell, same method, live-pinned members vs HEAD members: process peak **1,691.1 -> 1,467.2 MB** (a fall of 223.9), `lots_read` **1,691.1 -> 1,257.0 MB**. The HEAD run holds all three members at HEAD, including DB-b-96/102 in `account_return_daily.py` (the returns stage peaks 230.2 live, 239.5 new).
Statement: the new members' local peak is lower than the live members' in DB-b-110's run and in this cell's, by 266.1 and 223.9 MB; the added `record_lots_status` call is about 0.05 MB (old packet's micro-measurement, still the same code). The Lambda figure for the new bytes is ARGUED, not measured: the live code already sat 884.8 MB under the 85 percent line and the local peak fell, so the new code is expected below 1,672 MB. The first scheduled fire after the release remains the acceptance read.

## DELTA=0 evidence

Kit day 2026-10-08; thresholds sha256 `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` in both runs (pinned blob `6be02af162`, verified before use; DB-b-110's private copy (row D2-W85-S1) has the SAME sha256, read now). Method: DB-b-110's harness adapted in `refresh_delta0_run.py`; two kits in the Lambda layout outside the repo (LIVE: `handler.py` from `072d27a4a1`, the two producers from their live pins; NEW: the three at HEAD); every other member as pinned; S3 GETs only; the status write to a counting stub (1 stub put in each run, no S3 write). Control: the live returns hash equals DB-b-110's recorded `sha256_before`.

| Table | Rows | sha256 live-pinned | sha256 HEAD | Equal |
|---|---|---|---|---|
| returns | 6,901 | `9e5d6e92760d0ae2...` | `a5a3921b9b99aa5a...` | **NO** |
| class | 25,057 | `2028f91d7e2a652f...` | `2028f91d7e2a652f...` | yes |
| account_activity_daily | 6,901 | `f81aaa0b4f33691c...` | `f81aaa0b4f33691c...` | yes |
| account_lot_realized | 35,834 | `651421e336953941...` | `651421e336953941...` | yes |
| account_lot_unrealized_daily | 542,546 | `9e2df0d8f7fb0579...` | `9e2df0d8f7fb0579...` | yes |

Full hashes in `R45_REFRESH_DELTA0.json`; `output_hash_equal` is **false**. The one differing column in `returns` is `method_version` (see Open question). Run identities: LIVE kit code sha256 prefixes `handler.py 212b6f7682bf`, `account_return_daily.py 9935f5c7bcd7`, `account_activity_lots.py caf7655586b9`; NEW kit `ae334f6117b5`, `14a6b91f5021`, `c5364a9f81f0`; `account_class_daily.py 2def366fb5de`, `sources.json 5dd1f367d4d0` and the thresholds identical in both. The two runs ran together as separate processes (wall 911.7 s live, 898.3 s new); RSS is per process.

## COO half

Status: UNSIGNED.

Reads and signs: the census (three members over `oNgy4rnr`, each pinned to HEAD bytes with its commits since the live pin), the radius, the rollback and the memory statement. The COO answers the open question on `account_return_daily.py` first. Stamp and date go here when signed. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED.

Reads and signs: both branches (A and B) with the stated limit on a refused backfill day, the per-key rollback, and the DELTA=0 evidence, including the returns difference. The half is not a clean never-widen while `returns` differs. Stamp and date go here when signed. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
