# R37 packet DELTA -- the realized-lot key gains `realized_gain`; release of ONE changed bundle member and ONE backfill of 2026-10-08 (IRPT_DASHBD DB-b-88)

Author `0.9.0_WK_IRPT_DASHBD~63` for `2.0.0_SA_COO~D2`, 2026-10-09. Order `IRPT_DASHBD.TO-DB-b-88`. Ordered by `1.0.0_SA_CTO~DELL2` ADDENDUM 10 (msg 3225, row S40), item E6.
Signed packet this is a DELTA of: `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~51/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37.md`, sha256 `848dd8640688c28cb62ffab109c4d55ea4e5348bc5286400a824d8e1405fd40b`, both halves SIGNED (`2.0.0_SA_COO~D2` COO half, `1.0.0_SA_CTO~DELL2` CTO half GIVEN). This delta changes nothing the R37 halves signed except the one member and the one event named below.

## 1. The one changed member

| Member (`repo_path`) | R37 pin (signed) | R37 sha256 | New pin | New sha256 |
|---|---|---|---|---|
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `c0afa6f55e7446fa7634d63b011c670b6b8a632c` | `63f9e20f1735f4f0003b41713ca1820d62b6ed716c047328a04458b854c8ea6c` | `0a41f929a33c4345e6108e2792b0af84f96453be` | `cfa366ecbbe2a81a5a5961878fef7c71e983b255a08e2c0032b79fa146e3cda1` |

The new pin is the DRAIN commit of DB-b-87 (`drain: merge wk-IRPT_DASHBD-62`). The authoring commit is `9c980c6c15` (DB-b-87, `0.9.0_WK_IRPT_DASHBD~62`); both carry the same blob `db068fe88b85`. It is NOT yet on `origin/CLOUD` (the local remote-tracking ref `6be2fbae1c` does not contain either commit; `origin/CLOUD` still carries the R37 bytes `63f9e20f`). The order allows the drain commit with this line saying so. The other 17 pins of the entry are unchanged and stay on the R37 table; `handler.py` is unchanged (`18851ddab0d77743d25a0b6c157cafe35eaa5673d7db2d83817b0abe525a2b34`). Note: `infra/logic/registry/reporting_policies.json` at HEAD differs from its pin (other seats' commits); the artifact is built from the PIN (`0c35aeeaa8`, sha256 `dc0eccfde86127327934064eec85ecd33f71ea56f2594dd3f032f78d0ca47e17`), so that member of the artifact is unchanged.

## 2. The new realized key

`account_lot_realized` primary key, from `(firm, account_id, business_date, lot_id, quantity, proceeds)` to
`(firm, account_id, business_date, lot_id, quantity, proceeds, realized_gain)`.
Why: 2026-10-08 held 8 wash-sale pairs that share the whole R37 key (one lot split in two by a wash sale: same quantity, proceeds and cost basis, a different gain). The R37 function therefore logged `LOTS_SKIPPED 2026-10-08` at the 11:41Z fire. Record: `deliverables/0.9.0_WK_IRPT_DASHBD~62/LOTS_KEY_R41.json` (decision EXTEND_KEY, 0 of 8 pairs identical) and the rule-24 record `deliverables/0.9.0_WK_IRPT_DASHBD~62/rule24_realized_gain_key.md`. The contract `org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json` carries the same key. The producer still refuses by name a row identical in every column and a repeat of the whole new key with another column differing. No column is added to the table; the set of columns is unchanged.

## 3. The day

2026-10-08 (the newest landed returns day). Its returns and class partitions are landed (written by the 11:42Z fire); its three lot partitions (`account_lot_realized`, `account_lot_unrealized_daily`, `account_activity_daily`) hold 0 objects (read 2026-10-09T12:4xZ). Kit rows on 2026-10-08 (DB-b-87): realized 35,834, unrealized 542,546, activity 6,901; 0 refusals.

## 4. Radius unchanged

No new prefix, no new read, no new grant, no new action, no new table and no new role statement. The Terraform root files `iam.tf`, `locals.tf` and `lambda.tf` are at the `efeb21df71` release bytes (sha256 `2c0ed377...`, `5fe82384...`, `9ae18719...`, unchanged since the R37 apply) and are not edited. Expected targeted plan: **0 to add, 1 to change, 0 to destroy** (the function only: `s3_object_version` and `source_code_hash`); `-target=module.irpt_reporting_gold.aws_lambda_function.this`. Any other count, add, destroy or resource is a STOP. Writers counted: one rule per property (`account_activity_lots.emit_day`), two paths (scheduled fire, explicit backfill); the key change is inside the rule's validation, before `emit_day`, and adds neither a writer nor a path.

## 5. The backfill event

ONE invoke of `irpt-49f-reporting-gold-lambda`, payload `{"accounts": "population", "backfill": {"start": "2026-10-08", "end": "2026-10-08"}}` (accounts at event level), no `dry_run`, after the apply. It writes the three lot partitions of 2026-10-08 (new keys, two objects per table) and REWRITES the returns and class partitions of 2026-10-08 (same code path as the scheduled fire; the returns bytes must be equal). No other invoke is made by this order; the next scheduled fire is the organic read.
Stop: the returns `data.parquet` of 2026-10-08 hashes unequal before and after.

## 6. Sizing against the 85% line

Kit (dell2, DB-b-87): 2026-10-07 peak 1,685.5 MB, 545.47 s; 2026-10-08 peak 1,698.6 MB, 561.89 s. The 85% line is 1,740.8 MB and 765 s: margin to the line on memory 55.3 MB (10-07) and 42.2 MB (10-08), on time 219.5 s and 203.1 s. The Lambda's own `Max Memory Used` and `Duration` come from the backfill's REPORT line and are recorded beside these.

## 7. Rollback, per key

- Lambda: the prior function is the live R37 function, CodeSha256 `ciTGx5UVE3BJ4mMgwlzSYCDpYBkvtefHbNlT2KCxh5Y=`, artifact object `investor-reporting/irpt-reporting-gold-lambda.zip` version `pPnoTZs86qlqo2waxfP4h2ogXwq3hoR5` (latest before this act). Route: `copy-object` of that version onto the same key, re-pin the source-map entry to `c0afa6f55e`, targeted `safe-apply` (an `aws lambda update-function-code` is barred).
- Returns 2026-10-08: `data.parquet` prior version `_mAW3R_ELlTFNcoGHryExfDbaIdVJuml` (299,812 bytes), `manifest.json` prior version `Sssb275y0PmJ5hg76zgrvyYGzj5Hfwth` (227,762 bytes), restored by `copy-object` from the version id read at that moment.
- Class 2026-10-08: `data.parquet` prior version `1VL0MbEJw134zOCDyQneqw2ZfkJqlvIK`, `manifest.json` prior version `rGOR6l8nenXR2zH0zbEvXQNnAq9rxuCy`.
- Three lot partitions of 2026-10-08: 0 prior objects, so no key to restore. Removal is an S3 delete, a human-confirmed act after Andrew's word (as the R37 CTO half, condition 4); the objects have 0 served readers.

## 8. Signing context

The R37 COO and CTO halves above govern this delta; this document adds no new authority. Status of this delta when written: PLAN NOT YET READ, BACKFILL NOT YET RUN. The deploy ledger entry opened for this act is pinned to this file's sha256.
