# EQUALITY_MX-t-13 -- the tool's figure against the served object, side by side

Measured 2026-09-30 ~10:28Z by 0.9.0_WK_NFRA_MCPINDEX~21, worktree wk-mcpindex-r5-21 at a73e9cf57e plus this cell's edits.
Pre-release read; graded live at the release (MX-r-7). Read-only throughout: one paginated ListObjectsV2 pass (1,992 keys at 1000 a page) and one GetObject
by the tool, one GetObject by VersionId and two head-object calls by me, all under my own read credentials
(`.tools/aws`, account 313476888478). The tool's role (gateway-blackdiamond-read-role) is NOT applied, so this read did not
go through it.

## The served object

- bucket `opal-data-bd`, key `silver/fees/2026-09-28.parquet` (the newest partition of the 1,992 under `silver/fees/`)
- **VersionId `ktHEUzzqCOa7Xp_YAl9UkEXPDRq1Dsuh`**, LastModified 2026-09-29T22:21:10+00:00, ETag `d0eb7eb9a10d23f3c4dbe8e9af0d42a9`, 122405 bytes
- `head-object` after the tool call returned the same VersionId and ETag; the tool's own GetObject response (recorded by a
  pass-through client) carried that VersionId and ETag; `s3api get-object --version-id` returned a file whose md5 is
  `d0eb7eb9a10d23f3c4dbe8e9af0d42a9`, equal to the ETag.

## The two sides

The headline figure: the trade date 2026-09-28, fee lines and the two de-duplicated totals.

| side | as-of (`trade_date`) | rows | distinct transaction_id | transaction_fee (deduplicated) | account_fee (deduplicated) |
|---|---|---|---|---|---|
| tool `blackdiamond_list_fees` (in-process, real S3 client, Opal-internal principal, scope 49financial) | 2026-09-28 | 1856 (`rows_matched`; 200 returned, `truncated` true) | 1813 (`rows_deduplicated`; `duplicate_transaction_ids` 43) | 117.59 | 8526.7 |
| served object by VersionId, read independently with pandas | 2026-09-28 | 1856 | 1813 | 117.59 | 8526.7 |

- The same file summed WITHOUT de-duplicating gives transaction_fee 134.12 (account_fee 8526.7): the 43 repeated ids (same
  account under two `relationship_id` values) would have over-stated transaction_fee by 16.53; the tool's figure does not.
- `source_as_of` 2026-09-28 (newest partition of the source); `as_of` 2026-09-28 (newest `trade_date` the totals speak to);
  neither is the call time. `partitions_read` ["2026-09-28"], `partitions_absent` [].
- All 1856 `account_id` start with `z08` (358 distinct); the tool's fence passed.
- The answer carries the four never-sum rules and the four caveats of the record.

## The call

`bd.answer(<pass-through boto3 s3 client>, (catalog_gate.OPAL_INTERNAL, ""), scope="49financial")`, calls: the paginated
`list_objects_v2` listing of `opal-data-bd` prefix `silver/fees/` (not recorded by the pass-through) and one recorded `get_object` of
`silver/fees/2026-09-28.parquet`. No write. The scripts are in the worker's scratch and are not committed.

## RE-READ at 2026-09-30T22:54Z -- the served object moved, so this section supersedes the headline above

The source refreshed while this continuation ran: `silver/fees/2026-09-28.parquet` was rewritten (VersionId
`aediF0DklYdAbocXBFYEyGH_kgPFTWPr`, 122719 bytes, ETag `7747f6fc0432ebdaf15c51c7cc552a63`, against the 122405 bytes above) and
a newer partition `silver/fees/2026-09-29.parquet` now exists, so the tool's default answer speaks to 2026-09-29. Same call
(`bd.answer(<pass-through boto3 s3 client>, (catalog_gate.OPAL_INTERNAL, ""), scope="49financial")`), same credentials, read-only.

- bucket `opal-data-bd`, key `silver/fees/2026-09-29.parquet`, **VersionId `Qp7FdHII2X4JQYzDSOAB9wGi1UcNJfpt`**, LastModified
  2026-09-30T22:21:10+00:00, ETag `0732083b012e3bb9ef1cfb8edc3835e9`, 1084791 bytes.
- The tool's own GetObject response (recorded) carried that VersionId and ETag; `head-object` after the read returned the
  same; `s3api get-object --version-id` returned a file whose md5 is `0732083b012e3bb9ef1cfb8edc3835e9`, equal to the ETag.

| side | as-of (`trade_date`) | rows | distinct transaction_id | transaction_fee (deduplicated) | account_fee (deduplicated) |
|---|---|---|---|---|---|
| tool `blackdiamond_list_fees` | 2026-09-29 | 22853 (`rows_matched`; 200 returned, `truncated` true) | 22221 (`rows_deduplicated`; `duplicate_transaction_ids` 632) | 63.43 | 0.0 |
| served object by VersionId, read independently with pandas | 2026-09-29 | 22853 | 22221 | 63.43 | 0.0 |

- Summed WITHOUT de-duplicating the same file gives transaction_fee 64.1 (account_fee 0.0).
- `source_as_of` 2026-09-29, `as_of` 2026-09-29; `partitions_read` ["2026-09-29"], `partitions_absent` [].
- All 22853 `account_id` start with `z08` (6078 distinct); the tool's fence passed.
- Equality holds on every column compared: as-of, rows, distinct ids, both totals. The figure differs from the section above
  because the object differs, not because the tool does; the first read's object (VersionId `ktHEUzz...`) is the prior version.
