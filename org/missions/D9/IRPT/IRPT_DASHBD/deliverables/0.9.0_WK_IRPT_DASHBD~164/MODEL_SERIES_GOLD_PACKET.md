# NEVER-WIDEN PACKET -- the model daily series into the report's gold (table `market_topic_daily`, firm home `49financial`)

**Cell:** IRPT_DASHBD.TO-DB-b-199 (round 104, workstream B). **Worker:** 0.9.0_WK_IRPT_DASHBD~164, issued by 2.0.0_SA_COO~D2.
**Status of this packet:** a DRAFT for the CTO's half. Nothing is applied. This cell writes nothing to AWS, pushes nothing and deploys nothing.
**Contract:** `org/standards/IRPT_DASHBD_MARKET_TOPIC_DAILY_CONTRACT.json`. **Producer:** `data/assets/scripts/gold/irpt_reporting/adapters/model_series_market_topic_daily.py`. **Tests:** `data/assets/scripts/gold/irpt_reporting/tests/test_model_series_market_topic_daily.py`.
**Live reads made by this cell (GET and LIST only):** one GET of the served object, one named-prefix LIST of the target prefix, one `get-bucket-versioning`. Counts, dates and names only are printed below.

## 1. The act

ONE landing of the Yang model-design daily return series (the served object `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json`, column `index_benchmark_return`, four stems UST, ST, INT, LT) into the report's gold as table `market_topic_daily`, under the firm gold home the address call below names.

- **address_args:** `["irpt", "49financial", "gold", "market_topic_daily", "date=2026-10-13"]` (`lib/opal_naming.address()`), resolving to `s3://opal-data-49financial/irpt/49financial/gold/market_topic_daily/date=2026-10-13`.
- **Exact keys the FIRST apply writes:** bucket `opal-data-49financial`; for each trading date D of the live series (616 partitions, section 2), the prefix `irpt/49financial/gold/market_topic_daily/date=D/` holding two objects in this order: `data.parquet` (one row) then `manifest.json` (written last, so its presence marks a complete partition). Objects per partition: 2. Total objects: 616 x 2 = 1,232.
- **By whom:** an AE applier seat (not this worker; the COO names it at the apply).
- **Invocation shape (not run):** a later act under its own packet. This cell provides no apply path: `emit_partition(row, firm, upload=True)` raises `NotImplementedError`. The shape the apply would take: a GET-only reader calls `read_model_series(reader)`, then `build_rows(stems, data_as_of, "49financial")`, then for each row writes `data.parquet` and `manifest.json` at `partition_address("49financial", row["business_date"])`. The writer is not in the repo yet and is not run here.

## 2. What moves, measured (counts and dates only)

- **Served object read by this cell:** `generated_at` 2026-10-14T11:05:59Z; object LastModified 2026-10-14T11:06:01Z; VersionId `9wcMYjBbgI9jMxGANcPBhPIAKBRQMcZt`; `data_as_of` 2026-10-13; `inception_date` 2024-04-30.
- **Rows:** 3,205 in the object across five codes (641 per code). The ULT code is not used. For each of UST, ST, INT, LT, 25 weekday rows fall on exchange holidays and are dropped; nothing is interpolated.
- **Partitions the series covers:** 616 trading dates per stem, identical date sets across the four stems, no duplicate date, no non-numeric value on a trading day, max absolute daily value 0.0482 (below the 0.1 scale guard).
- **Date range:** first 2024-04-30, last 2026-10-13. The last date equals `data_as_of`, so the series is not short of its claim and nothing is extended.
- **Vintage drift against the cited source read:** the round-103 read (`BENCHMARK_FILL.json`) recorded `data_as_of` 2026-10-12 and 615 trading days per stem. The live object is one trading day later (616). Recorded as a surprise row (`IRPT_DASHBD-D2-W164-S2`); the apply records the live vintage, not the cited one.
- **Opal figures that change in the report afterward:** the 32 benchmark members (the four stems across the QTD, YTD, last-12-months and since-inception windows, for both the period and the annualised views) and the 12-month chart, once a later round repoints the report's source to this table. What stays equal: the arithmetic (a window is the product of one plus each daily return on trading days, minus one; the anchor is the prior trading day) and every daily value dated on or before the earlier vintage's last date, as far as the two vintages share it. What moves: every window whose end is the latest date, since its end now includes 2026-10-13, and the chart's last point. NOT ESTABLISHED: whether the shared history agrees value for value between the two vintages. This cell did not re-read the earlier object, and no report was rendered.

## 3. When and where it takes effect

- Nothing in the report changes when the apply lands. The report reads its own gold, and no reader of `market_topic_daily` exists in the repo yet (section 4b). The series reaches the report only when a later round repoints the report's source to this table.
- Where: the bucket and prefixes of section 1, from the moment each `manifest.json` is written.

## 4b. Writers

- **Writers of the target prefix in the repo: 0.** Basis: `comp-find 'market_topic_daily'` over the worktree (corpus all) printed 25 hits across 79,515 files scanned, banded DEF=1, CONFIG=7, DOC=17. The one DEF hit is a table-name tuple in the round-101 checker; the CONFIG hits are contract, readiness and proof records that declare or mention the table; the DOC hits are the PRD and the briefs. None writes to the prefix. The producer added in this cell has no put path.
- **Schedules:** the repo census above covers the infrastructure-as-code in the worktree. No schedule in the repo names this table. The live EventBridge rules and the live account were NOT read, so the live writer count is NOT ESTABLISHED beyond the LIST below.
- **Expectation:** none. The target prefix LIST returned no objects, so nothing currently writes or holds this table.

## 5. Both branches

- **A run that lands:** each of the 616 partitions is new (no key exists before the apply). Each partition is written as `data.parquet` then `manifest.json`. The result is 616 partitions and 1,232 objects under the prefix of section 1, and no existing key is overwritten. The served object is only read, so no served output moves.
- **A run that fails part-way (an apply that fails after some partitions):** the applier stops at the first failed write. A partition whose `manifest.json` landed is complete. A partition holding only `data.parquet` is incomplete and is removed by the rollback of section 6, or completed by a re-run of that date only. No other partition is touched. No served output changes at any point in either branch.

## 6. Rollback

- **Versioning state of `opal-data-49financial`, read live on 2026-10-14:** `Status: Enabled` (`get-bucket-versioning`).
- **Target prefix before any apply:** a named-prefix LIST of `irpt/49financial/gold/market_topic_daily/` returned no objects. The prefix holds nothing today, so every key the apply writes is a new key.
- **Rollback per key:** delete each key the apply wrote (the exact keys of section 1, for the dates the apply actually wrote). Because versioning is Enabled, each delete leaves a delete marker, and the object version remains as a noncurrent version. The rollback is therefore a deletion that needs Andrew's word under the S3-delete rule, and its record must say that the objects are noncurrent versions, not gone.
- **No other key moves:** the producer writes only under the target prefix and reads the served object by GET only. The rollback touches only the target prefix. The served object `json/benchmarks/model_portfolio_timeseries.json` is not written by anything in this cell or in the apply.

## 7. Conditions, and the questions for the CTO's half

**Conditions of the apply.**
1. Re-read at the moment of the apply: the target prefix LIST is still empty; bucket versioning is still Enabled; the served object is re-read and its `data_as_of` and day count are restated in the apply record.
2. The producer and tests pass at the committed bytes: 7 tests pass, and the mutant that drops the `data_as_of` column is caught by 2 tests and reverted to identical bytes. The commit gate passes on both `.py` files.
3. The apply waits for the CTO's ruling on the questions below.
4. The apply is not made while another seat holds an open ledger entry on the same bucket. None was measured in this cell.

**Questions for the CTO's half.**
1. **The table and the home.** The PRD and the brief define `market_topic_daily` as a general, non-client topic table with a general platinum home and no firm location. This cell carries a return series in it under a firm gold address. Accept `market_topic_daily` as the carrier, and accept `49financial` as the firm home (or name another)?
2. **The source.** Is the served Yang object a source the report's gold may carry? The source read records this as a CTO decision.
3. **The vintage.** The series is recorded at its live vintage (`data_as_of` 2026-10-13, 616 days), not the round-103 vintage (2026-10-12, 615 days). Accept the live vintage as the claim?

## 8. Not established, and so not covered

- The live writers of the target prefix beyond the repo census (live EventBridge rules and the live account were not read).
- Whether the shared history agrees value for value between the round-103 vintage and the live vintage.
- The IAM permission of the applier role to put under `irpt/49financial/gold/market_topic_daily/`.
- The figures the report shows after a repoint (no report was rendered in this cell).
- Whether the served object's versions are stable between this read and the apply (one GET was made).
- The downstream readers of the table (none in the repo yet).
- The applier's identity and its write path, which does not exist in this cell.
