# MEASURE_BATCH_ROUND3 -- NFRA_MCPINDEX MX-m-1 -- 0.9.0_WK_NFRA_MCPINDEX~11

All four measures are READ-ONLY (S3 list/get, SSM list/get, EventBridge list-rules). Measured 2026-09-28 from 21:20Z to
22:55Z UTC. Counts, version ids and hashes only: no asset row, account id or name is in this file. Every S3 object read
was read BY VersionId (the 22:10Z scheduled asset-dim run landed during the session, so "latest" moved once: see (b)).
Scripts that reproduce the counts sit beside this file: `m1_a_fetch.sh`, `m1_a_pins.py`, `m1_a_classify.py`,
`m1_a_fees_objects.py`, `m1_b_measure.py`, `m1_c_measure.py`. Rows filed: NFRA_MCPINDEX-Z-W11-S1, -S2, -S3.

## (a)

**Question.** Do the BD SSM documents other than `opal-bd-asset-dim-download` report their own failure through a non-zero
exit, and how many recent runs have SSM Status Success while the run's own uploaded log records failure?

**Instrument.**
- Enumeration: `aws ssm list-documents --filters Key=Owner,Values=Self` (24 documents). BD plane = name prefix `opal-bd-`
  (7). `opal-cot-bd-session-fetch` also contains "bd" and is EXCLUDED by the firm line (cot). The order's set is the 7 minus
  asset-dim = 6; asset-dim is measured too as a CONTROL row.
- Content: `aws ssm get-document --name <doc> --document-version '$LATEST'`. **The bare verb returns the DEFAULT version, which
  is not what runs execute** (row Z-W11-S1): allocation default v3 vs $LATEST v4, transaction default v1 vs $LATEST v2.
- Runs: `aws ssm list-commands --filters key=DocumentName,value=<doc>` (all runs SSM still retains, N stated per row),
  `aws ssm list-command-invocations --command-id <id> --details` for the plugin ResponseCode.
- Log: `s3://opal-data-bd/logs/<name>-download-<date>.log`, the LAST S3 version uploaded within [start-2m, start+3h] of the
  run, read by VersionId (127 of 127 runs of the 6 daily documents found a log). "Log records failure" = any of: a line
  starting `ERROR:` containing "fail"; `Download exit code: N` or `Merge exit code: N` with N nonzero; a line `FAILED`.
  Predicate lives in `m1_a_classify.py`.

**Result table (version executed = $LATEST).**

| document | $LATEST | failure branch | ends non-zero? | runs N | SSM Success | SSM Failed | log records failure | SSM Success AND log failure |
|---|---|---|---|---|---|---|---|---|
| opal-bd-allocation-download | v4 | ERROR echo + exit 1 (before `shutdown`) | yes | 21 | 0 | 21 | 21 | 0 |
| opal-bd-fees-download | v1 | ERROR echo + re-upload, then falls through to `shutdown` | NO exit statement | 21 | 21 | 0 | 21 | **21** |
| opal-bd-realized-download | v2 | ERROR echo + exit 1 (before `shutdown`) | yes | 21 | 0 | 21 | 21 | 0 |
| opal-bd-transaction-download | v2 | ERROR echo + exit 1 (before `shutdown`) | yes | 21 | 0 | 21 | 21 | 0 |
| opal-bd-unrealized-download | v2 | ERROR echo + exit 1 (before `shutdown`) | yes | 21 | 0 | 21 | 21 | 0 |
| opal-bd-49f-session-fetch | v1 | none of its own: `set -e`, wrapper's rc is the doc's rc | inherits the wrapper's rc | 2 | 2 | 0 | 0 (its output records `OK` and `exit rc=0`; no upload log exists) | 0 |
| opal-bd-asset-dim-download (CONTROL, not in the order's set) | v1 for 21 runs, v2 for 1 | v1: no exit; v2: exit added | v1 no, v2 yes | 22 | 21 (all v1) | 1 (v2) | 22 | 21 (all v1) |

Runs are dated 2026-08-28 to 2026-09-28 (asset-dim to 2026-09-26; fees to 2026-09-25, its 22:15Z run of today had not
fired at the cut-off). For the five daily documents of the order's set: SSM Success AND log failure = 21 of 105 runs; all
21 are fees. The reverse mismatch (SSM not Success while the log records no failure) = 0 of 127 runs with a log.

**Z-S47 re-measured in the same table.** At the S3 log-object grain, latest version per key, fees: 121 log objects, 69
record failure, 69 are exactly 886 bytes, first failing date 2026-06-23, last non-failing 2026-06-22 -- Z-S47's 69 of 121
reproduces exactly. At the SSM-run grain (this table) fees is 21 of 21, because SSM retains only 21 runs. The other 48
failing days are beyond SSM retention: their SSM status is INFERRED Success from the unchanged v1 document (created
2026-04-10, no exit), not measured.

**Zeros with their cause.** The four exit-1 documents read 0 mismatches because their $LATEST captures both return codes
and exits 1 before the SSM plugin returns; a mismatch would appear only if a run executed a document without that exit,
and the two default versions that lack it (allocation v3, transaction v1) are not the version any run used (Z-W11-S1).
Z-S47 recorded these four as "unmeasured, not asserted broken": they are measured, and honest. Note (Z-S17, not
re-measured): allocation, realized, transaction, unrealized place `exit 1` before `shutdown -h +2 &`, as read in $LATEST.

DENOMINATOR: 24 SSM documents (Owner Self) -> 7 with prefix opal-bd- (6 in the order's set + asset-dim control); runs: 107 in the order's 6-document set (fees 21, allocation 21, realized 21, transaction 21, unrealized 21, 49f-session-fetch 2) + 22 asset-dim control = 129 SSM runs; 127 logs read by VersionId; plus 121 fees log objects for the Z-S47 grain
FINDING: SSM Success while the log records failure = 21 of 105 runs across the five daily documents, all 21 on opal-bd-fees-download (21 of 21 fees runs), the only one of the six whose executed version swallows a failure; allocation, realized, transaction and unrealized are honest (0 of 84; each exits 1 on failure, SSM Failed on 21 of 21); 49f-session-fetch has had no failing run (0 of 2), so its failure branch is untested; Z-S47's 69 of 121 reproduces at the log-object grain

## (b)

**Question.** Did the 42 cusip deltas of the dim rewritten 2026-09-28 ~06:22Z reach silver transactions?

**Instrument.** `aws s3api list-object-versions --prefix silver/bd_assets_dim.parquet`; each version read by VersionId and
compared on `asset_id -> cusip` (script `m1_b_measure.py`); `list-object-versions --prefix silver/transactions/` for every
object written after the version.

**Dim versions (VersionId prefix, LastModified UTC, bytes, asset_ids).**
- V0 `4dfwFfuZ4qRb...` 2026-04-14T20:44:16Z, 884,599 B, 10,937 asset_ids (the predecessor).
- V1 `pdoQY5Waj63_...` 2026-09-28T06:22:06Z, 967,128 B, 12,141 asset_ids (the MX-s-6 version).
- V2 `Pa4qx5SjiCh...` 12:04:24Z, 884,875 B, 10,937 (the bare-rebuild regression, live 4m19s).
- V3 `bSQWML9E4qUX...` 12:08:43Z, ETag equal to V1 (the rollback).
- V4 `kittUyy.WHGf...` 12:22:57Z, 977,308 B, 12,141.
- V5 `qcSdLjLW0d1Q...` 22:11:33Z, 977,308 B, 12,141 (the scheduled 22:10Z run; new ETag, same mapping).

**Delta confirmed.** V0 to V1: 10,937 asset_ids in common, cusip changed on **42** (all value-to-other-value: 0 null-to-value,
0 value-to-null), 1,204 asset_ids added, 0 removed. V1 vs V3, V1 vs V4, V4 vs V5: 0 changed of 12,141 on each pair.

**Silver transactions written after V1.** Under `silver/transactions/`: 2,405 object versions, 1,913 live keys; exactly ONE
was written after 2026-09-28T06:22:06Z: `silver/transactions/2026-09-28.parquet` (VersionId `fgzzqFZOaFvM...`,
2026-09-28T21:54:42Z, 34,882 B). Its pyarrow metadata reads num_rows=0, 73 columns, no `cusip` column. The compacted
`silver/bd_transactions.parquet` has no version after 2026-01-28. The count of rows carrying a cusip that differs from what
V0 would give, and the count of rows on the 42 asset_ids, are both 0 of 0.

**The zero has a named cause, and it is not "the deltas propagated".** The 21:54Z run's log says `[enrich] bd_assets_dim
unavailable; skipping cusip join` and `(0 rows)`. That line appears in 10 of 10 runs (of 21 in the SSM window) that
processed a file; 0 of 10 print an `[enrich] cusip: N/M non-null` line. The deployed script
(`s3://opal-data-bd/scripts/merge-daily-incremental.py`, version `MF9tYCkR4uu_...`, 43,492 B) is not the repo file
(59,077 B); its `load_bd_assets_dim` returns None silently only when boto3 is None or the dim is empty. That boto3 is
absent on the host is INFERRED, not measured (row Z-W11-S2). What would have made the count non-zero: a run that
processes a file WITH rows after V1, with the join working. Neither happened.

**Not measured.** Rows written BEFORE V1 (silver partitions rewritten 2026-09-27T00:1xZ, e.g.) and carrying V0's cusip on
the 42 asset_ids: reading them is ~596 MB of live-key objects and is outside this cell.

DENOMINATOR: silver/transactions/ = 2,405 object versions (1,913 live keys); 1 written after V1 (2026-09-28.parquet, 0 rows); dim = 10,937 (V0) vs 12,141 (V1) asset_ids, 10,937 in common; 21 transaction-download logs read for the enrichment line
FINDING: 0 of 0 silver transaction rows written after V1 carry a cusip differing from V0's value (0 of 0 on the 42 asset_ids) -- because the only object written after V1 is a 0-row partition and the EC2 daily merge logged "bd_assets_dim unavailable; skipping cusip join" in 10 of 10 runs that processed a file, so the 42 deltas have NOT been shown to reach silver and the join is not running on the SSM path (rows Z-W11-S2)

## (c)

**Question.** Of the null-cusip rows in gold `holdings_lots` at the latest partition, how many are cash rows?

**Instrument.** `s3://opal-data-bd/gold/timeseries/holdings_lots/<date>.parquet` (`B_01.holdings_lots.py:3006-3028`, key
builders), each object read by VersionId, columns `asset_name, ticker, cusip, snapshot_date, is_open` (script
`m1_c_measure.py`). The gold table has no `asset_id` column, so the cash predicate must run on `asset_name`.

**Predicates.**
- **P1 (primary, strict): `asset_name.fillna('').astype(str).str.upper().str.strip() == 'CASH'`.** This is B_01's own cash
  test, `is_cash_lot = (name_u == 'CASH')` at `data/black_diamond/scripts/gold/B_01.holdings_lots.py:2371`
  (`_apply_silver_noncash_cap`), the same line that labels the lot class CASH at :2388.
- **P2 (upper bound): asset_name upper-cased contains any of `CASH, MONEY, MMKT, SWEEP`, and not `CASH COWS`.** The pattern
  tuple is `_CASH_PATS` at `B_01.holdings_lots.py:579` (and :925), applied as at :951-953. It is a bound, not a cash
  test: at 2026-09-25 P2 also matches 119,016 rows that carry a real cusip (money-market funds).

**Latest partition = 2026-09-25** (`kMi6dV9.2HGB...`, LastModified 2026-09-28T04:56:39Z): 1,270,177 rows, 22,344 null cusip
(0 blank/'nan'/'None' strings beyond the nulls).
- P1: **2,800 of 22,344 null rows (12.53%)**; P1 rows with a non-null cusip: 0 of 2,800 (all P1 rows are null, as
  `B_01.holdings_lots.py:291` and :302 force 'CASH' to None).
- P2: 15,329 of 22,344 (68.60%). Null rows matching neither: 7,015 (31.40%) across 1,923 distinct asset_names; 20,355 of
  the 22,344 null rows have a null ticker.

**Reconciliation to R-11.** R-11's 22,172 of 1,264,679 reproduces exactly on the 2026-09-18 partition as it stood before its
rewrite: VersionId `h9YkSI9zxp.lEGq...` (2026-09-25T23:55:58Z) and `poNnzHRAOWNGx...` (2026-09-25T04:54:28Z) both read
1,264,679 rows, 22,172 null; on that version P1 = 2,664 of 22,172 (12.02%), P2 = 15,186 (68.49%). The same key was
rewritten 2026-09-26T23:54:43Z (`QAlmTUrGaRB7...`) and now reads 1,265,193 rows, 22,248 null, P1 2,703 (12.15%). A
historical gold partition moves after it is read, so "latest of 99" names a version as well as a date.

DENOMINATOR: 2026-09-25 partition (VersionId kMi6dV9.2HGB...): 1,270,177 rows, 22,344 null cusip; cross-check 2026-09-18 version h9YkSI9zxp.lEGq...: 1,264,679 rows, 22,172 null (R-11's figures)
FINDING: 2,800 of 22,344 null-cusip rows (12.53%) are cash by B_01's own predicate asset_name == 'CASH' (B_01.holdings_lots.py:2371); at most 15,329 (68.60%) by the broader name-pattern bound at :579/:951-953; on R-11's own version 2,664 of 22,172 (12.02%) -- so about 88% of the null cusips are NOT the literal cash rows

## (d)

**Question.** Who reads gold `canonical/lots_unrealized` and `canonical/lots_realized`, and is any reader live?

**Instrument.** `comp-find` over the worktree corpus (regex on `canonical_lots_unrealized_key`,
`canonical_lots_realized_key`, `CANONICAL_LOTS_UNREALIZED_PREFIX`, `CANONICAL_LOTS_REALIZED_PREFIX`,
`canonical/lots_unrealized`, `canonical/lots_realized`, `lots_unrealized`, `lots_realized`); `comp-read --enumerate` on each
candidate; `aws s3api list-objects-v2` for object recency; `aws events list-rules`. Denominator: 43,870 files scanned
(corpus=all), 1,176 to 1,183 hits (the count drifts by a few between calls as peer seats add files and rail logs), bands
HEAD=40 DEF=10 SURFACED=90-97 CONFIG=758 TEST=24 DOC=254; 3 ephemeral-floor and 2,721 binary files not searched. The portal
submodule is an empty directory in a worker worktree and is NOT in the population (row Z-W11-S3); `infra/aws/lambda`
IS in it and holds 0 code hits (its only 4 infra hits are a census text file).

**BD-plane code that names the keys (5 files, of the first-party bands).**
1. `data/black_diamond/scripts/gold/B_02.canonical_lots.py` -- the PRODUCER (`:624`, `:630` write keys; `:818-819`, `:1014-1015`,
   `:1149-1150` list ETags for its own watermark). Not a consumer.
2. `data/black_diamond/scripts/gold/B_03.account_gains.py` -- **CONSUMER**: `:280` and `:305` read
   `canonical_lots_realized_key(d)` / `canonical_lots_unrealized_key(d)` when `d` is in the listed dates; `:657-658`,
   `:854-886` list and bulk-load every date.
3. `data/black_diamond/scripts/gold/C_05.client_tax_liability.py` -- **CONDITIONAL consumer**: `:145` lists the unrealized
   prefix only inside `load_latest_canonical_lots()`, which `:432-445` calls ONLY when holdings_lots is unreachable or its
   money columns are all zero. The live path reads gold `holdings_lots`.
4. `data/black_diamond/scripts/gold/lib/s3_layout.py` (`:102-109`) -- the key builders; a definition, not a reader.
5. `org/modules/graph/tests/test_pipeline_gaps.py` -- a test.
Also: `gold_freshness_config.yaml:243-253` declares both artifacts (`bd_gold_canonical_lots_unrealized`, `..._realized`);
that is a declared expectation, not a read. One peer probe `deliverables/0.9.0_WK_NFRA_MCPINDEX~4/probes/mx_q_2.py` names
them (a one-off read). The `data/cot/` copies of B_02, B_03, C_05, s3_layout and `diag_gold_silver_recon.py` are cot's
scripts on cot's plane: by the firm line they were listed by name and not opened.

**Live?** The word "silent since 2026-07-23" is the newest PARTITION DATE, not the job's activity. On 2026-09-28 the
producer rewrote 631 of 658 `lots_unrealized` objects and 1,402 of 1,402 `lots_realized` objects
(realized LastModified 04:59:35Z to 05:01:09Z; unrealized newest 05:01:09Z), and then all 2,459 `account_gains` objects (B_03's output; LastModified
05:03:05Z to 05:03:59Z, newest key date 2026-09-25). That is a nightly gold run in which B_03 read the two prefixes; it is
INFERRED from writer mtimes and the code, not from a run log. The chain is `gold_dispatch.sh:152`
(`CHAIN_CANONICAL="B_00 B_01 B_01b B_02 B_03 ..."`), C_05 in `CHAIN_DOWNSTREAM` (`:155`). The EventBridge rule
`bd-gold-nightly-fallback` is ENABLED `cron(0 23 ? * MON-SAT *)`; the trigger of the 05:0xZ run itself was NOT identified.
No Lambda and no served page in the searched population reads either key.

DENOMINATOR: 43,870 files scanned (corpus=all), 1,176-1,183 hits, 5 BD-plane first-party code files name the keys (B_02, B_03, C_05, s3_layout.py, test_pipeline_gaps.py) + 1 declaring config + 1 peer probe; 4 cot-plane files listed and not opened; portal submodule not in the worktree; objects: lots_unrealized 658, lots_realized 1,402, account_gains 2,459
FINDING: 1 live consumer reads them today -- B_03.account_gains, inside the scheduled gold chain (all 2,459 of its outputs written 2026-09-28T05:03Z, INFERRED from mtimes, not a run log); C_05 reads them only on a fallback arm and its live path reads holdings_lots; the producer B_02 is also live and rewrote 631 + 1,402 partitions on 2026-09-28, so "silent since 2026-07-23" means no NEW partition date, not no job; no Lambda and no served page in the searched population reads either prefix
