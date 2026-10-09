# Never-widen packet R44 -- ONE gold Lambda release carrying DB-b-90 (uniqueness on the FINAL realized rows) and DB-b-91 (the lots-not-computed statement), over live `yIAQjspL` (IRPT_DASHBD DB-b-94)

Author `0.9.0_WK_IRPT_DASHBD~69` for `2.0.0_SA_COO~D2`, 2026-10-09. Order `IRPT_DASHBD.TO-DB-b-94`. Ordered by `1.0.0_SA_CTO~DELL2` ADDENDUM 12 (msg 3371, `@77e60c3d2b`), item 5 / enrichment E1.
This cell writes the packet only. The apply (source-map re-pin, rebuild, upload, targeted `safe-apply`) is a later cell, after both halves below are SIGNED. Nothing was built, uploaded or applied here.
Companion record: `R44_RELEASE_CENSUS.json` (same folder). Predecessor delta, same function and procedure: `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~63/R37_DELTA_PACKET_1008.md`.

## Census (the members this release changes)

Base: live `irpt-49f-reporting-gold-lambda`, CodeSha256 `yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE=` (get-function read 2026-10-09, LastModified `2026-10-09T12:55:44.000+0000`, LastUpdateStatus Successful). Members compared: the source map's 18 `staged_from` pins plus `handler.py` (the function's own `source_dir` member), at HEAD of `box/dell2`-derived branch `wk-irpt-dashbd-46-69`.

| Member | Owner order | New pin (box/dell2 drain commit) | Authoring commit | sha256 at pin = HEAD | Base sha256 |
|---|---|---|---|---|---|
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `TO-DB-b-90` | `d18ddf000d5bf4dc8e08d49b66ea97e79d4d0c9c` | `1b0b580292` | `caf7655586b9...` (full value in the census) | `cfa366ecbbe2...` (the R37-delta pin `0a41f929a3`) |
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `TO-DB-b-91` | `f14a1a2358825168e63edbc1c75529b586cce7d5` | `3697923e02` | `212b6f7682bf...` (full value in the census) | `18851ddab0d7...` (the blob at the artifact build commit `7fbf4eb108`) |

Result: of the 19 members compared, 16 `staged_from` pins equal their HEAD bytes, and 2 differ from the live bundle and are exactly the two above. A THIRD member differs from its pin at HEAD, `infra/logic/registry/reporting_policies.json` (pin `0c35aeeaa8`, sha256 `dc0eccfd...`; HEAD `1479826b...`, moved by other seats' registry commits). The artifact is built from the PIN, so that member's bytes in the released artifact do not change; it is not a member of this release. Row `IRPT_DASHBD-D2-W69-S1` records it for the issuer's reading. The apply cell must keep the pin (the same condition the R37 delta carried).
`handler.py` has no source-map pin: the builder takes it from the working tree at the build commit, so the apply cell builds at a commit whose `handler.py` blob is `7c9bb9dcdc5b` (git blob id) and records the artifact's member hashes.

What each member changes, read from the diff against the base bytes:
- DB-b-90, `account_activity_lots.py`: new `check_realized_unique(rows)` (`:317-328`) compares the realized key `PRIMARY_KEYS[TABLE_REALIZED]` on the FINAL rows; called in `compute_local` after `apply_inkind_reference` has rewritten `realized_gain` in place (`:1088`) and as an early pass in `realized_rows` (`:374`). The old inline check in the row loop is removed. The key, the columns and the refusal texts are unchanged.
- DB-b-91, `handler.py`: new `LOTS_STATUS_KEY`, `lots_status_statement`, `record_lots_status` (`:448-487`), one call in `catch_up_lots` (`:513`).

## Radius

No new read, no new grant, no new prefix, no new action, no new table, no new role statement. The Terraform root files `iam.tf`, `locals.tf` and `lambda.tf` of `infra/aws/terraform/investor-reporting/reporting-gold/` are at their R37 release bytes (sha256 prefixes `2c0ed377`, `5fe82384`, `9ae18719`, read now, unchanged) and are not edited.
- ONE new written key: `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json` (the activity table's own prefix, `locals.tf:86`; address from `opal_naming.address("irpt", firm, "gold", "account_activity_daily", ...)` via `_lots_location`, `handler.py:442-446`, never typed). It sits inside the existing PutObject set (`WriteTheFiveGoldPrefixesOnly`, `iam.tf:91-95`, `locals.tf:96-102`, the activity prefix `*`) and its one read (`get_object`, `handler.py:472`) inside the existing read ARNs (`locals.tf:90-91`). It never begins `date=`, so the newest-landed listing cannot read it as a landed day.
- Writers of that key, counted: ONE rule, `record_lots_status` (the only `put_object` in `handler.py`, `:483`), reached by ONE caller, `catch_up_lots` (`:513`), which is reached by ONE path, the scheduled fire (`lambda_handler`, `:629` -> `run`, `:588`; the call is `:623`). The explicit backfill path calls `emit_lots` (`:582`) and does not call `record_lots_status`. N = 1 writer, 1 rule read. No delete is granted: the object is overwritten, never removed (`iam.tf:87-89`).
- The key changes WHERE the lots check runs (the final rows, before `emit_day`), and adds neither a writer nor a path to any lot partition: the lot partitions are still written only by `account_activity_lots.emit_day` (`:1312`), whose own repeated-key refusal (`:1327-1329`) is unchanged.
- Expected targeted plan at the apply: **0 to add, 1 to change, 0 to destroy**, `-target=module.irpt_reporting_gold.aws_lambda_function.this` (the function only: `s3_object_version` and `source_code_hash`). Any other count, add, destroy or resource is a STOP.

## Branch A

A lots day lands: the final-rows check passes, and the status record drops that day.
Producer rule: `check_realized_unique` (`account_activity_lots.py:317-328`) raises only when two realized rows repeat the key `PRIMARY_KEYS[TABLE_REALIZED]` (`firm, account_id, business_date, lot_id, quantity, proceeds, realized_gain`); on a unique frame it returns, `compute_local` (`:1088`) completes, `lots_days` (`handler.py:380-409`) returns the day's rows, and `emit_lots` (`:412-439`) writes `account_lot_realized`, `account_lot_unrealized_daily` and `account_activity_daily` LAST for that day through `emit_day`. The day is in `lots_written`, so `record_lots_status` (`:455-487`) computes `kept = prior minus landed` (`:477`).
Expected outcomes, both from that rule:
- No statement existed before (the first fire after the apply, since the 2026-10-08 backfill left no refusal): `if not kept and not prior: return {}` (`:479-480`) -- NOTHING is written, the status key stays absent (expected 0 objects under `_status/`).
- A statement existed for that day: the object is overwritten once with that day removed, and an empty `statements` list when nothing is owed.
- The returns and class partitions of the day are written by the same fire BEFORE the lots stage (`run`, `:617-623`), unchanged.
Limit stated, not hidden (row `IRPT_DASHBD-D2-W69-S2`): `record_lots_status` is called on the scheduled path only. A refused day later landed by an explicit BACKFILL (`run_backfill`, `:582`) is NOT dropped from the status record by that backfill, and the scheduled catch-up does not re-owe it (it is owed only after the activity table's newest landed day), so its statement would stay until a later scheduled fire rewrote the object with it removed -- which `kept = prior minus landed` never does for a day outside that fire's landed set. This branch does not claim a backfill clears a statement.

## Branch B

A lots day is refused by name: the statement is written, and returns and class still land.
Producer rule: a repeat of the realized key on the final rows raises `SystemExit("REFUSED: realized lot id ... appears twice in one frame, identical in every column")` when the two rows are whole-row equal (`account_activity_lots.py:325`), else `SystemExit("REFUSED: realized lot id ... repeats with the same closing date, quantity, proceeds and gain: the key is not unique")` (`:326-327`). `lots_days` catches `(Exception, SystemExit)` (`handler.py:396`) and returns a failure reason for EVERY day of that producer call (`:398`, one producer call for all owed days: all owed days are refused together, not one). `emit_lots` prints `LOTS_SKIPPED <day> <reason>` (`:437-438`); nothing is written to any lot table for those days (the refusal precedes `emit_day`).
Expected outcomes, both from that rule:
- STATEMENT: `record_lots_status` (`:513`) writes the one object, one entry per refused day, `text` = `lots not computed for <date>: <reason>` (`lots_status_statement`, `:451-452`; reason truncated to 300 characters at `:397`), via the single `put_object` (`:483`). A failed read or write of the object is logged by name (`LOTS_STATUS_READ_SKIPPED`, `LOTS_STATUS_WRITE_FAILED`) and never raises (`:455-487`). A dry run writes nothing (`:462`, `upload` False).
- RETURNS AND CLASS STILL LAND: returns days are written by `emit_day` of the returns producer (`:617-620`) and class days by `catch_up_classes` (`:621`) before `catch_up_lots` (`:623`); `catch_up_lots`, `emit_lots` and `lots_days` are documented and coded never to raise (`:380-383`, `:412-413`, `:490-497`), so the returns and class partitions of the same fire are written byte-equal to a fire without a refusal.
- The refused day stays owed: the next scheduled fire retries it (owed after the activity table's newest landed day, `class_owed_days`, `:322-338`).

## Rollback

Per key, back to `yIAQjspL`:
- Lambda function: the prior function is the live R37-delta function, CodeSha256 `yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE=`, artifact `investor-reporting/irpt-reporting-gold-lambda.zip` in the lambda-artifacts bucket (`ARTIFACT_BUCKET`, `infra/aws/lambda/ci/build-and-upload.sh:54`), S3 version `a.YllA9SmwwfY34NlajqOaNsex2bBZAy` (head-object read 2026-10-09, latest at that read, LastModified `2026-10-09T12:48:58+00:00`, 217,498 bytes). Route: `copy-object` of that version onto the same key, re-pin the source-map entry's `account_activity_lots.py` to `0a41f929a3`, targeted `safe-apply` of the function (`aws lambda update-function-code` is barred).
- Status key `_status/lots_not_computed.json`: before the apply it is expected to hold 0 objects (UNREAD here: this cell reads only the two named AWS objects; the apply cell reads the prefix first). If it exists after a Branch-B fire, its prior version is read at that moment and restored by `copy-object`; if it has no prior version, removal is an S3 delete, a human-confirmed act after Andrew's word. The object has 0 served readers.
- Lot partitions (`account_lot_realized`, `account_lot_unrealized_daily`, `account_activity_daily`) of any day the released function lands: new `date=` keys written by `emit_day` (no prior object), removal likewise an S3 delete after Andrew's word. The 2026-10-08 partitions already landed by the R37 delta are not rewritten by this release.
- Returns and class partitions of a fire day: prior versions read from the version id at that moment, restored by `copy-object`, as in the R37 delta section 7.

## Sizing

UNMEASURED, and named as such: the release adds one pass over the realized rows (`check_realized_unique` on the final rows; the early pass in `realized_rows` replaces the removed inline loop, so the net is one pass). No local kit day was run by this cell. Reference only, from the R37 delta record (`R37_DELTA_RECORD.json`, the live backfill of 2026-10-08, 35,834 realized rows): Max Memory Used 1,649 MB of the 2,048 MB size, Duration 389.1 s of the 900 s timeout; the 85% lines are 1,740.8 MB and 765 s. The added pass holds references to rows already in memory plus one key-to-row dict of the realized rows; its effect is not measured here and is not asserted to be small.

## COO half

Status: UNSIGNED.

Reads and signs: the census above (exactly two changed members, pinned), the radius (one new written key, one writer), the rollback and the sizing statement. Stamp and date go here when signed. `2.0.0_SA_COO~D2` signs; this worker signs nothing.

## CTO half

Status: UNSIGNED.

Reads and signs: both branches (A and B) with their stated limit on the backfill path, the per-key rollback, and the one-release pairing of DB-b-90 and DB-b-91 as ruled in ADDENDUM 12 item 5. Stamp and date go here when signed. `1.0.0_SA_CTO~DELL2` signs; this worker signs nothing.
