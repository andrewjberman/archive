# Chunking-Lambda Pattern -- Validation & Canonical-Readiness Review

**Reviewer:** 0.7.0_AE_CloudOps | **Date:** 2026-07-15 | **Trigger:** Andrew-direct (mid-session):
review/validate the chunking pattern; if effective, make canonical for heavy INGESTION (esp. backfills);
analytics/gold runners stay EC2 for stability.
**Doc under review:** `docs/architecture/chunking_lambda_architecture.md` (DS, @ 988f39914 + 11e614747)
**Reference impl:** `data/assets/scripts/lib/stream_parquet.py` + `convert_orion` @ delta-6 (6ff338a21).
**Grounding advantage:** I deployed the reference impl (delta-6 orion swap) THIS session and measured it
in the REAL Lambda runtime -- so this review carries the runtime confirmation number the doc's own
Section 3 requires, not just a doc read.

## VERDICT: EFFECTIVE. Adopt as canonical for heavy INGESTION, after closing 2 gaps (below).

Validated on three axes:

### 1. MECHANICAL (source-confirmed)
`stream_parquet.py` matches the doc's two load-bearing contracts exactly:
- **Atomic per partition:** each batch -> local temp parquet (peak RAM = one batch); ONE `put_object`
  on `finalize()`; any raise before finalize -> `abort()`/`__exit__` discards temp, ZERO bytes land
  (`stream_parquet.py:126-173`). This is what keeps a pre-write reconciliation gate a true pre-write gate
  under streaming.
- **Write-verified:** `finalize()` compares S3 ETag to local-file MD5, raises `StreamWriteUnverified`
  on mismatch (`:133-148`). Schema-strict (`write_table` refuses non-conformant batches, never coerces).
- Fan-out (fact + N dims one pass, abort-all-on-raise) present and correct for the CRS class.

### 2. EMPIRICAL (live runtime, the doc's required confirmation)
The 1.39M-row orion `fact_transactions` unit that OOM'd at BOTH 3008 and the 10240 platform max now
converts on the **deployed** artifact at:
- **Max Memory Used 1131 MB / 1127 MB** (two independent real conversions, CW REPORT) -- **1877 MB
  headroom under the 3008 envelope.**
- **Wall ~91 s** -- well under the 600 s timeout (and the ~400 s bar).
- rows_in == rows_out == 1,394,630, parity true, SCHEMA_ASSERTED (conversion manifests 151355Z/151457Z).

Doc's dev-host proxy was 988 MB / 47.2 s; my runtime numbers are **+14% RAM, +93% wall**. The pattern
holds with margin -- but see Gap-A (wall variance).

### 3. ARCHITECTURAL
The write-side (shared, family-blind `ChunkedParquetWriter` -- the ONE place the memory bound lives) /
read-side (per-family `row->RecordBatch` iterator -- grammars do NOT merge) split is the correct shape
for canonical reuse. The Section-2 decision fork **is** Andrew's ingestion-vs-EC2 law verbatim, and it
already routes whole-workbook/global-sort/whole-dataset-dedup work to EC2 -- so "analytics/gold stay EC2"
is already encoded (blackdiamond xlsx is the in-doc example that stays whole-read).

## GAPS to close before stamping it the estate standard

**Gap-A (matters most for Andrew's stated use case -- BACKFILLS): no multi-partition drain pattern.**
The doc covers per-PARTITION conversion beautifully but a backfill is MANY partitions. A single
`run_sweep` converts all misses sequentially in ONE invocation -> 58 orion units x ~91 s >> 600 s
timeout -> it times out partway + DLQs. The correct backfill drain is **per-partition event fan-out**
(one invocation per partition, gated by reserved concurrency), with the sweep as reconciliation-only. I
built this by hand for the delta-6 drain today; it should be a named part of the canonical standard.

**Gap-B (safety on OTHER buckets): the ETag==MD5 verify is SSE-dependent.** Validated AES256/non-KMS on
`opal-data-assets` (confirmed live). But the identity **breaks under KMS or multipart** -- and then the
write-verify silently needs a different instrument. Canonical adoption on any new bucket must gate on an
SSE/size precondition (deny, or fall back to read-back-compare, for KMS/multipart targets). The doc
states the assumption; a canonical standard must make it an enforced precondition, not a footnote.

**Refinements (lower priority):**
- **Wall variance:** runtime wall was ~1.9x the dev-host. RAM headroom is handled; wall is not -- a
  family measured ~350 s dev-host could blow 600 s in runtime. Weight the ~400 s dev-host bar strictly.
- **/tmp (ephemeral_storage):** the RAM-for-disk trade puts the growing parquet in `/tmp` (default
  512 MB; `silver.tf` sets none). Delta-6 was 29.9 MiB (16x inside), but this is a Rule-5 sizing
  dimension a bigger-output family must size explicitly.
- **Write-verify failure leaves an untrusted object at the key** (raise is AFTER the put). Sound
  (idempotent reconvert overwrites; never-marked-converted + listing-based landing check keep it out of
  served) -- but that companion invariant must be REQUIRED, not optional, wherever the primitive is used.

## RECOMMENDATION
1. YES -- canonical for heavy INGESTION (mirror/silver converters, backfills). It directly kills the
   materialize-whole-partition OOM class and the primitive is clean + shared.
2. Keep the decision fork as the gate; gold/analytics stay EC2 (already in the doc).
3. Close Gap-A (backfill drain orchestration) and Gap-B (SSE precondition gate) before declaring it THE
   estate standard -- they are exactly the two things Andrew's "particularly for backfills, on heavy
   ingestion generally" scope exercises.
4. Honest bar: n=1 family today (orion). The schwab CRS heavy class on the SAME primitive (PartnerETL,
   post-0833) is the natural second proof; two families validated is the threshold for "canonical."
