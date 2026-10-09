# Never-widen packet R45 -- ONE gold Lambda release carrying DB-b-97 (a backfill clears the lots status record) and DB-b-104 (the status key built by address()), over live `oNgy4rnr` (IRPT_DASHBD DB-b-105)

Author `0.9.0_WK_IRPT_DASHBD~80` for `2.0.0_SA_COO~D2`, 2026-10-09. Order `IRPT_DASHBD.TO-DB-b-105`. Ordered by `1.0.0_SA_CTO~DELL2` ADDENDUM 16 item 1 and ADDENDUM 17 (msg 3583, `@6d3d12876c`), enrichment item E1.
This cell writes the packet only. The apply (source-map handler re-record, rebuild, upload, targeted `safe-apply`) is a later cell, after both halves below are SIGNED. Nothing was built, uploaded or applied here.
Companion record: `R45_RELEASE_CENSUS.json` (same folder). Template and predecessor, same function and procedure: `../0.9.0_WK_IRPT_DASHBD~69/NEVER_WIDEN_PACKET_R44_RELEASE.md`; its apply record `../0.9.0_WK_IRPT_DASHBD~70/R44_APPLY_RECORD.json`; its sizing record `../0.9.0_WK_IRPT_DASHBD~78/R44_SIZING_DRYRUN.json`.

## Census (the member this release changes)

Base: live `irpt-49f-reporting-gold-lambda`, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (lambda get-function-configuration read 2026-10-09, LastModified `2026-10-09T14:34:30.000+0000`, LastUpdateStatus Successful, State Active, 2048 MB, 900 s). Members compared: the source map's 18 `staged_from` pins plus `handler.py` (the function's own `source_dir` member) = 19.

| Member | Owner orders | Pin (box/dell2 first-parent drain commit) | sha256 at pin = HEAD | Base sha256 (inside live `oNgy4rnr`) |
|---|---|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `TO-DB-b-97` (authoring `4dc238fde6`), `TO-DB-b-104` (authoring `39f31ab566`) | `98ae364e98e9715ca25ea3e27014a6951246cd65` | `ae334f6117b5...` (full value in the census) | `212b6f7682bf...` (the blob at the R44 build commit `072d27a4a1`) |

Result: exactly ONE member differs from the live bundle, `handler.py`. The build commit for the apply must carry a `handler.py` blob `c8ef82373e5e` (git blob id). `handler.py` has no source-map pin: the builder takes it from the working tree at the build commit.
The other 18 members equal the live bundle by construction: the artifact is built from the source map's `staged_from` pins, and the R44 apply verified them member by member against the live zip (`R44_APPLY_RECORD.json`: `members_live` 19, `members_built` 19, `only_in_live` [], `only_in_built` [], `reporting_policies_equal_live` true). The gold function's pins have not moved since the upload commit `f0d129281f` (`git diff f0d129281f HEAD` on the source map touches other functions and this function's deploy-record lines only). Of the 18 pins, 14 equal their HEAD bytes and 4 differ from HEAD (`account_return_daily.py`, `sources.json`, `lib/opal_naming.py`, `reporting_policies.json`, moved by other seats' commits). Those 4 are the same bytes in the live bundle and in the next build; they are NOT members of this release and the apply cell must keep the pins. Row `IRPT_DASHBD-D2-W80-S1`.
`account_activity_lots.py` is unchanged: HEAD equals its pin `d18ddf000d`, the bytes already live.

What the member changes, read from the diff `072d27a4a1..HEAD` of `handler.py` (9 lines, 6 added, 3 removed):
- DB-b-104: the constant `LOTS_STATUS_KEY` is replaced by `_lots_status_location(firm)` (`:448-451`), which builds the status object's bucket and key with `opal_naming.address("irpt", firm, "gold", "account_activity_daily", "_status", "lots_not_computed.json")`; `record_lots_status` calls it (`:468`).
- DB-b-97: one call, `record_lots_status(s3, firm, set(lots_written), lots_failed, not dry_run)`, in `run_backfill` (`:585`), after `emit_lots` (`:584`).

## Radius

No new key, read or grant. The Terraform root files `iam.tf`, `locals.tf` and `lambda.tf` of `infra/aws/terraform/investor-reporting/reporting-gold/` are not edited (sha256 prefixes `2c0ed377`, `5fe82384`, `9ae18719`, read now, equal to R44's).
- The status key is unchanged in bytes (DB-b-104). Measured locally with the PINNED kit (the 18 staged pins plus the pinned `handler.py`, the exact bytes the build will carry): `_lots_status_location(<firm>)` returns bucket `opal-data-<firm>` and key `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json`, byte-equal (`True`) to the key the old code built as `<activity prefix> + "_status/lots_not_computed.json"`. It sits in the activity prefix, inside the existing PutObject set (`locals.tf:96-99`, `iam.tf:94`) and its one read (`handler.py:474`) inside the existing read ARNs (`locals.tf:91`, `iam.tf:84`). It never begins `date=`, so the newest-landed listing cannot read it as a landed day. No delete is granted (`iam.tf:87-89`): the object is overwritten, never removed.
- Writers of that key, counted: ONE rule, `record_lots_status` (`:458-490`), the only `put_object` in `handler.py` (`:485`), now with TWO callers: `catch_up_lots` (`:515`), reached by the scheduled fire (`lambda_handler` `:632` -> `run` `:591`, call at `:627`), and `run_backfill` (`:585`), reached only by an explicit event carrying a `backfill` object (`run`, `:591-596`). N = 1 writer rule, 2 callers, 2 entry paths (R44 had 1 caller, 1 path). The new caller adds no new object, prefix or action: the same key, the same `PutObject` on the same prefix.
- The lot partitions are still written only by `account_activity_lots.emit_day`; this release adds no write to any `date=` key.
- Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (`s3_object_version` and `source_code_hash` of the function only). Any other count, add, destroy or resource is a STOP.

## Branch A

A backfill lands a stated day and the status record drops it.
Producer rule: `run_backfill` (`handler.py:546-589`) calls `emit_lots` (`:584`), whose `lots_days` (`:380-409`) returns the day's rows and `emit_lots` writes `account_lot_realized`, `account_lot_unrealized_daily` and `account_activity_daily` LAST (`:421-432`); the day is then in `lots_written`. `record_lots_status(s3, firm, set(lots_written), lots_failed, not dry_run)` (`:585`) computes `kept = {prior statements for days not in landed}` (`:479`), `kept` then takes this call's failures (`:480`).
Expected outcomes, both from that rule:
- A statement existed for that day: `prior` is read from the status object (`:474-477`), the landed day leaves `kept`, and the single `put_object` (`:485`) overwrites the object once, with that day removed (an empty `statements` list when nothing else is owed). Measured locally with the pinned kit and a fake client: prior `{2026-10-08}` + that day landed -> one put, `statements` empty (22 bytes written).
- No statement existed (an absent object, `NoSuchKey`, is an empty prior, `:476-478`) and nothing refused: `if not kept and not prior: return {}` (`:481-482`) -- NOTHING is written and the status key stays absent. Measured locally: 0 puts.
- A dry-run backfill (`dry_run` true -> `upload` False): `if aal is None or not upload: return None` (`:465-466`) -- nothing is read or written.
- A statement for a day the backfill did NOT land stays (`:479`). The returns and class partitions of the backfill are written before the lots stage (`:577-583`), unchanged.
This closes the limit the R44 packet stated (row `IRPT_DASHBD-D2-W69-S2`): a refused day later landed by an explicit backfill is now dropped by that backfill.

## Branch B

A backfill refuses a day and the status record states it.
Producer rule: a repeat of the realized key on the final rows raises `SystemExit("REFUSED: realized lot id ... repeats ...")` (`account_activity_lots.py:325-327`, called at `:1088` and `:374`). `lots_days` catches `(Exception, SystemExit)` (`handler.py:396`) and returns the reason for EVERY day of the producer call (`:397-398`): one producer call covers all the backfill's days, so all of them are refused together, not one. `emit_lots` prints `LOTS_SKIPPED <day> <reason>` (`:437-438`) and writes nothing to any lot table for them.
Expected outcomes, both from that rule:
- STATEMENT: `record_lots_status` (`:585`) writes the one object, one entry per refused day, `text` = `lots not computed for <date>: <reason>` (`lots_status_statement`, `:454-455`; reason truncated to 300 characters at `:397`), via the single `put_object` (`:485`). At most `MAX_BACKFILL_DAYS` = 25 days per invocation (`:119`). Measured locally: 25 refused days -> one put of 18,424 bytes. A failed read or write is logged by name (`LOTS_STATUS_READ_SKIPPED` `:478`, `LOTS_STATUS_WRITE_FAILED` `:488`) and never raises.
- RETURNS AND CLASS STILL LAND: `run_backfill` has already written the returns days (`:578-581`) and the class days (`:583`) before the lots stage; `emit_lots`, `lots_days` and `record_lots_status` are documented and coded never to raise, so the backfill's return value carries `lots_failed` (`:586-589`) and the returns and class partitions are byte-equal to a backfill without a refusal.
- Limit stated, not hidden: a backfill rewrites landed days, so a day it refuses is NOT owed again by the scheduled catch-up (owed only AFTER the activity table's newest landed day, `class_owed_days` `:322-338`). Its statement therefore stays until a later backfill that lands that day drops it (Branch A).

## Rollback

Per key, back to `oNgy4rnr`:
- Lambda function: the prior function is the live R44 function, CodeSha256 `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`, artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in the lambda-artifacts bucket `opal-313476888478-lambda-artifacts`, S3 version `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ` (head-object read 2026-10-09, latest at that read, LastModified `2026-10-09T14:29:21+00:00`, 218,641 bytes, metadata `content-sha256` equal to the CodeSha256). Route: `copy-object` of that version onto the same key, re-record the source map's gold entry for it, targeted `safe-apply` of the function (`aws lambda update-function-code` is barred). Nothing is re-pinned: no staged pin moves in this release.
- Status key `_status/lots_not_computed.json`: the R44 apply read 0 objects under `_status/` before the R44 release (`R44_APPLY_RECORD.json` `status_prefix_objects_before` 0); this cell reads no S3 prefix, so its state now is UNREAD and the apply cell reads the prefix first. If a fire or backfill writes it, its prior version is read at that moment and restored by `copy-object`; with no prior version, removal is an S3 delete, a human-confirmed act after Andrew's word. The object has 0 served readers.
- Lot partitions of any day a released backfill rewrites (the three lot tables): prior versions read from the version id at that moment and restored by `copy-object`; a new `date=` key with no prior object is removed by an S3 delete after Andrew's word. The returns and class partitions of a backfilled day likewise.

## Memory headroom

The R44 sizing dry run (`R44_SIZING_DRYRUN.json`, request `bfac402b`, dry run of the 2026-10-08 backfill, 7,620 accounts, 585,281 lot rows) used Max Memory 1,661 MB: 95.4% of the 1,740.8 MB (85%) line, 81.1% of the 2,048 MB size. Headroom: 79.8 MB to the 85% line, 387 MB to the size. The halves forbid raising a limit; this packet asks for none.
What this release adds to memory, ARGUED FROM THE CODE with file and line, plus one MICRO-MEASUREMENT of the added function (NOT a kit day):
- The release adds ONE call, `record_lots_status` (`handler.py:585`), in `run_backfill`, and replaces a constant with a call to the same `opal_naming.address` the handler already calls at `:171`, `:188`, `:443` (its registry load is cached per process, `lib/opal_naming.py:230-237`, so no second load). No import, no new module, no new dependency.
- The call runs AFTER the lots stage returns (`:584` -> `:585`): the lots producer's batches (`compute_local_batched`, the stage's peak) and `emit_lots`' `rows_by_day` are out of scope by then, so the added work sits below the stage's peak, not on it.
- What it holds is one JSON object of at most 25 statements (`MAX_BACKFILL_DAYS`, `:119`) with reasons cut to 300 characters (`:397`): the object read (`:474`), a dict of the prior statements, `kept` (`:479-480`) and the encoded record (`:483-485`).
- Micro-measurement, local, pinned kit, `tracemalloc` peak of one `record_lots_status` call in the worst case (25 refused days of 300-character reasons, one prior statement): 49,007 bytes (about 0.05 MB). This is the added function alone, not a run of the producer.
- The dry run that produced 1,661 MB never executed this call (`upload` is False on a dry run, `:465-466`); the real path adds the call's about 0.05 MB. Its other real-path allocations (the writes of `emit_day`) are unchanged by this release, and also were not exercised by that dry run (the dry run wrote 0 objects); this release does not change them.
- Statement: this release adds about 0.05 MB (argued from the code, bounded by the micro-measurement), against 79.8 MB of headroom to the 85% line; the 95.4% reading stays 95.4% to the first decimal. No kit day was run and no Lambda invoke was made by this cell. The Monday 2026-10-12 first scheduled fire remains the acceptance read for the whole function (row `IRPT_DASHBD-D2-W78-S1`).

## COO half

Status: UNSIGNED.

Reads and signs: the census above (exactly one changed member, `handler.py`, pinned to HEAD bytes), the radius (no new key, read or grant; one writer rule, two callers), the rollback and the memory statement. Stamp and date go here when signed. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED.

Reads and signs: both branches (A and B) with the stated limit on a refused backfill day, the per-key rollback, and the one-release pairing of DB-b-97 and DB-b-104 as ruled in ADDENDUM 16 item 1 and ADDENDUM 17. Stamp and date go here when signed. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
