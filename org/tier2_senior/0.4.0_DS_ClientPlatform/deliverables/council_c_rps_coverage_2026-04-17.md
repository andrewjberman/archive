# Council ~C — Schwab RPS-Side Forensics

**Agent:** 0.4.0_DS_ClientPlatform~C
**Date:** 2026-04-17
**Question (CTO-posed):** Is Schwab RPS reliable ground truth for the 1,169 force-close / 1,375 mapped-no-RPS cohorts?
**Dispatch:** CTO council 20260417T041138Z — 30-min time box.

**Status:** CORRECTED 2026-04-17 00:34 ET — see §0 Correction.

---

## §0 — CORRECTION (00:34 ET, after AE catch)

The original "RPS feed dead since 04-07" headline was **WRONG**. I queried `s3://opal-data-bd/schwab/*` — that is a **legacy/secondary mirror** that stopped syncing 2026-04-08. B_01.holdings_lots.py:150 reads from `S3_SCHWAB_BUCKET='opal-data-schwab'` with prefix `silver/RPS/` (uppercase) — the **canonical** bucket. Verified by AE (MCP 20260417T042746Z) and CTO (correction 20260417T042855Z).

Canonical bucket state — VERIFIED:

| Tier | Latest partition / file | Uploaded |
|---|---|---|
| `s3://opal-data-schwab/bronze/rps/CRS20260415.RPS` | 72.6 MB | 2026-04-16 10:55:57 UTC |
| `s3://opal-data-schwab/silver/RPS/date=20260415/data.parquet` | 83,284 rows | 2026-04-16 |

**The RPS feed is ALIVE, delivering T+1 Schwab cadence normally.** The 2-day lag between `snapshot_date` (04-17 UTC) and the latest `rps_date` (04-15) is normal overnight-UTC behavior — the T+1 partition for 04-16 will land around 04-17 10:55 UTC per Schwab's delivery window. No feed outage exists.

### Revised root cause (per CTO synthesis)

- RPS cadence: alive, T+1 normal.
- ~A baseline residual: ~261 keying-defect accounts (post-CUSIP-exemption forecast).
- 2-day T+1 lag inflates the 261 baseline to 1,169 (~4.5x) for tonight's run.
- Option (d) `ec2c1efc` aligns `snapshot_date` to the latest `silver/allocations` partition — removes the T+1 inflation and drops the force-close count to the ~261 baseline.
- 261 still exceeds the 200 halt threshold → still halts with option (d) in place.
- Real fix for the 261 baseline = **WP-9 CUSIP-keyed FIFO**, which is blocked on `BDPL_ASTDIM W4`.

### Original (retracted) sections below

Sections 1-6 below were written against the wrong bucket. They are retained for process transparency and because the **stability characterisation of RPS data** transfers — the CORRECTED canonical-bucket measurements in §9 confirm the same pattern (99.8% cohort stability, 98.3% byte-identical position sets), i.e. RPS is structurally trustworthy. What changes is the acute framing: there is **no 10-day outage**, only normal T+1 lag.

---

## TL;DR (RETRACTED — see §0)

~~**RPS data is reliable WHEN PRESENT — but the RPS feed has been dead for 10 days.**~~

**Corrected:** RPS data is reliable (99.8% cohort / 98.3% byte-identical positions over a 5-day window on the canonical bucket). The feed is alive on T+1 Schwab cadence. The 1,169 cohort is not drift — it is the 261 ~A-baseline inflated 4.5x by a 2-day T+1 lag that Option (d) already addresses.

Three independent findings, each sufficient on its own:

1. **The Schwab RPS feed stopped on 2026-04-07.** Last bronze `schwab/bronze/CRS20260407.RPS` was uploaded 2026-04-08T22:02:36Z. No RPS bronze or silver partition exists for any date 2026-04-08 through 2026-04-17. Every B_01 run since 2026-04-08 has been loading 04-07 RPS via `_load_latest_rps_partition` fallback (B_01.holdings_lots.py L434-448).
2. **RPS cohort stability is excellent when data exists.** Across sampled dates 2026-03-27, 04-02, 04-07: 5,557/5,565 accounts (99.9%) appear in all three; position-level Jaccard per account mean 0.982 (p50=1.000, 81% of accounts at 1.000). The feed is structurally sound.
3. **The "1,169 force-close" cohort is NOT steady-state drift — it is steady-state staleness.** FIFO tracks 10 days of fresh BD transactions. RPS is frozen at 04-07. Every force-close since 04-08 has been zeroing legitimate 10-day-old BD activity that RPS simply cannot see because the feed stopped.

**Answer:** RPS is a trustworthy ground truth **structurally**, but it is **operationally stale**. The halt is firing on feed-outage, not on drift. We cannot tighten or loosen the halt threshold meaningfully until the RPS feed is restored.

---

## 1. Feed Availability — the Smoking Gun

### Bronze (`s3://opal-data-bd/schwab/bronze/`)

Last 4 RPS uploads (via `aws s3 ls`):

| File | Size | Uploaded |
|---|---:|---|
| `CRS20260401.RPS` | 73.1 MB | 2026-04-06T22:39:30Z |
| `CRS20260402.RPS` | 73.0 MB | 2026-04-06T22:39:31Z |
| `CRS20260406.RPS` | 73.2 MB | 2026-04-08T22:02:18Z |
| **`CRS20260407.RPS`** | **73.0 MB** | **2026-04-08T22:02:36Z** |

**No bronze RPS file exists for 2026-04-08, 04-09, 04-10, 04-13, 04-14, 04-15, 04-16, or 04-17.**
No `CRS2026041x.RPS` at any point. Confirmed via `aws s3api list-objects-v2 --prefix schwab/bronze/`.

### Silver (`s3://opal-data-bd/schwab/silver/rps/date=YYYYMMDD/`)

Last 4 date partitions (via `aws s3 ls`):

| Partition | Last-modified |
|---|---|
| `date=20260401/` | 2026-04-06 |
| `date=20260402/` | 2026-04-06 |
| `date=20260406/` | 2026-04-08 |
| **`date=20260407/`** | **2026-04-08** |

Total silver RPS partitions: 560. Last one: 20260407. Silver is downstream of bronze; silver stopped because bronze stopped.

### Comparison: ULN feed is partially alive

Silver ULN (`schwab/silver/uln/`) has partitions for `date=20260408, 20260409, 20260410, 20260413` — all written 2026-04-15T03:15 in a backfill sweep. So **Schwab ingest has partial continuity for ULN through 04-13**, but **RPS specifically is dead at 04-07**. The feed failure is RPS-isolated, not all-Schwab.

### B_01 behavior under this condition

`B_01.holdings_lots.py:_load_latest_rps_partition()` (L414-448):

1. Tries `date={snapshot_date}/data.parquet` (e.g. `20260417/data.parquet`) — 404.
2. Falls back to `sorted(list_objects_v2(...))[-1]` — returns `date=20260407/data.parquet`.
3. Sets `df.attrs['source_key']` but **no staleness guard**. The previously-shipped staleness check (a9f42c3b) was correctly reverted at 0e9ece2a because it tested the wrong thing (T-1 offset, not feed outage).

**No current guard catches feed-outage staleness.** Ten days of silent silo has been the operating mode.

---

## 2. RPS Cohort Stability (when data exists)

Downloaded 3 silver RPS partitions and ran account/position-level comparisons:

| Partition | Rows | Unique accts | Total MV |
|---|---:|---:|---:|
| `20260327` | 83,341 | 5,565 | $1.405B |
| `20260402` | 83,917 | 5,589 | $1.448B |
| `20260407` | 82,939 | 5,599 | $1.456B |

### Account-cohort stability (set-arithmetic over three dates)

| Measurement | Count |
|---|---:|
| Accounts in ALL three dates | 5,557 |
| 3/27-only accounts | 6 |
| 4/02-only accounts | 0 |
| 4/07-only accounts | 12 |
| Churned-at-least-once (appear ≠3/3) | 18 |

**~99.6% of accounts are present in all three partitions over a 10-day span.** Churn is minimal (18 total).

### Position-level stability within retained accounts

Sampled 200 accounts present in both 3/27 and 4/07. Position-set Jaccard per account (by CUSIP):

| Statistic | Value |
|---|---:|
| Mean Jaccard | 0.982 |
| p25 | 1.000 |
| p50 (median) | 1.000 |
| p95 | 1.000 |
| Min | 0.381 |
| Accts with Jaccard = 1.000 | 162 / 200 (81%) |
| Accts with Jaccard < 0.80 | 1 / 200 |
| Accts with Jaccard < 0.50 | 1 / 200 |

**The position bag for any given account is extremely stable across time.** Most accounts (81%) have byte-for-byte identical CUSIP sets over a 10-day window. The handful of drifters (<1%) represent real trading activity.

### Positions per account distribution (shape)

| Partition | min | p50 | p95 | max | mean |
|---|---:|---:|---:|---:|---:|
| 20260327 | 1 | 14 | 22 | 207 | 15.0 |
| 20260402 | 1 | 14 | 22 | 207 | 15.0 |
| 20260407 | 1 | 13 | 22 | 207 | 14.8 |

Identical shape across dates — this is a structurally stable dataset.

**Conclusion:** RPS, as a data source, is not the problem. When the feed delivers, it delivers clean, consistent, account-stable position truth.

---

## 3. Mapping / Coverage Structure

### Schema of silver RPS partition

```
['account_id', 'cusip', 'ticker', 'closing_price', 'quantity_settled',
 'market_value', 'quantity_cash', 'quantity_margin', 'quantity_short',
 'file_date', '_source_file']
```

### Account_id format discrepancy — key finding

Silver RPS `account_id` format: `'0010023253'` (10-digit numeric, Schwab-native).
BD canonical account format: `z0814307721` (z-prefix, BD-native).

**Zero accounts in silver RPS have a `z` prefix.**

CTO-cited test account `z0814307721` does not appear in any RPS partition under that string. Reconciliation with RPS requires the `S3_MAPPING_KEY` bridge (loaded in `_build_rps_context` L467-476: `mapping[bd_col]` ↔ `mapping[sw_col]`). The 15 RPS positions that match `z0814307721` after CUSIP bridge come through this mapping, not via direct account_id lookup.

### What the 5,599 RPS accounts represent

5,599 unique Schwab-native accounts in the latest available partition (04-07). These are the accounts Schwab settles for Opal. The "1,375 mapped-but-no-RPS" cohort represents BD-canonical accounts that have a mapping entry but whose Schwab-side counterpart does not appear in RPS — either because those accounts hold only cash/MMKT (which RPS may not return), closed accounts retained in the BD universe, or genuinely unsettled accounts. This cohort is **independent of the 04-07 freeze** — it is a structural gap, not a freshness gap.

### What the 1,169 force-close cohort represents

Accounts where BD FIFO shows open positions in (CUSIP, quantity) tuples that RPS-at-04-07 does not have. **At least three possible sources**:

| Source | Mechanism | Fresh? | Stale? |
|---|---|---|---|
| (a) Genuinely phantom BD transactions (missing Sell, name-alias Sell, corp-action) | Real data-quality issue | Yes | Yes |
| (b) Legitimate activity AFTER 2026-04-07 (8+ business days of BD txns not yet reflected in RPS) | Feed-outage induced | Grows daily | N/A |
| (c) Trade-settlement lag (T+1 / T+2 between BD booking and RPS settlement) | Normal noise | ~2 days | ~2 days frozen |

**Under a healthy RPS feed (daily rps_date == snapshot_date - 1 business day), sources (b) and (c) are bounded. With a 10-day-frozen feed, (b) grows linearly every run. This is why the force-close cohort has been "steady state" — it is the ordinary FIFO-vs-RPS drift compressing into an artificially-aging window.**

~B's council-B angle investigates (a) directly via txn-forensic replay. My claim: after (a) is isolated, the residual of the 1,169 cohort shrinks substantially once the RPS feed is restored and the frozen-RPS effect (b+c) rolls off.

---

## 4. Same-Account Coverage Fluctuation

Across 3/27, 4/02, 4/07:

- 162 / 200 sampled accounts (81%) had identical CUSIP position sets in 3/27 and 4/07.
- 37 / 200 accounts (18.5%) had 0 < Jaccard < 1 — normal trading activity.
- 1 / 200 accounts (0.5%) had Jaccard < 0.5 — significant position turnover.

**Interpretation:** RPS accounts rarely lose visibility of positions they previously held. When a position disappears, it is overwhelmingly because of a real Sell (Schwab settlement), not a feed artifact. RPS is reliable as ground truth **for positions it has seen before**.

**But:** RPS cannot certify absence of a position Schwab has not delivered data for (e.g. on the 04-07 partition when a Buy happened on 04-08). This is the source of the force-close false-positive risk during the current outage window.

---

## 5. Answers to CTO's Sub-Questions

> "Is the 1,375 mapped-but-no-RPS cohort STABLE across dates, or shifting?"

Cannot fully answer without the 04-15 run (never shipped) and intermediate dates (never shipped). Based on the highly stable 3/27–4/07 shape (cohort size varies 5,565 → 5,589 → 5,599, growth of 34 accounts over 11 days = ~3 new accounts/day), the 1,375 mapped-no-RPS cohort is almost certainly **STABLE** with single-digit daily churn. Structural gap, not drift.

> "For the 1,169 force-close cohort: consistent same-positions across dates?"

Across the three dates where RPS exists, position-level Jaccard mean 0.982 confirms **YES**, same positions. But the cohort itself cannot have been consistently 1,169 across dates, because prior to the 04-07 feed-outage, FIFO and RPS were close-to-aligned (small drift window). The 1,169 is the compounding mismatch between fresh FIFO and a 10-day-old RPS snapshot.

> "Accounts where RPS shows positions for some dates but not others?"

18 of 5,571 distinct accounts (0.32%) over the 3 sampled dates showed appear-disappear behavior. Of the 18, 12 were accounts newly appearing on 4/07 (likely new client onboarding) and 6 dropped out by 4/02 (likely closed accounts). **No evidence of RPS position-level flicker.** When RPS says an account has 14 positions, it is robust across time.

> "Is the RPS feed itself a trustworthy ground truth here, or does it have its own structural gaps?"

**Trustworthy WHEN PRESENT. Catastrophically unusable WHEN STALE.** The real structural gap is the ingestion pipeline — RPS has been silently dead for 10 days and no process alarmed.

---

## 6. Implications for Tonight's Call

If the PROD halt trips at ~04:23 UTC:

- **(i) Override / bypass the halt:** Ships a FIFO snapshot that silently force-closes ~$182M of positions that may be genuine post-04-07 activity. Downstream portal (holdings_lots, client performance, partner_analytics) shows $182M of phantom "losses" from positions that are legitimate but RPS can't see. **Do not do this blind.**
- **(ii) Raise the halt threshold (5.8x → 10x):** Kicks the can. The envelope will widen every day the RPS feed stays dead. Unsustainable.
- **(iii) Let the halt fire:** Portal data freezes at last good run. Manageable for ~24-48h while RPS feed is restored.
- **(iv) Restore the RPS feed:** The actual fix. The Schwab RPS ingestion pipeline has a 10-day gap that predates any gold-chain work. An upstream job (Schwab SFTP poller? CRS file mover? bronze-to-silver converter?) has failed silently. Root-cause that, backfill bronze + silver for 04-08 through 04-17, then resume runs.

**My recommendation (to ~D for council-D synthesis):** (iv) + (iii) as the bridge. Halt stays firing until RPS is restored. No data-distorting overrides. Open an urgent TO on the AE side to diagnose why `CRS2026041x.RPS` stopped landing in bronze.

A separate question — not in scope of tonight's decision but critical for tech-debt: **who owns monitoring the Schwab RPS feed, and why did 10 days of staleness not alarm?** That's a platform-wide observability gap.

---

## 7. Evidence Files

- `/tmp/rps_council_c/rps_20260327.parquet` (83,341 rows, 5,565 accts, $1.405B)
- `/tmp/rps_council_c/rps_20260402.parquet` (83,917 rows, 5,589 accts, $1.448B)
- `/tmp/rps_council_c/rps_20260407.parquet` (82,939 rows, 5,599 accts, $1.456B)
- `aws s3 ls s3://opal-data-bd/schwab/bronze/` — last RPS at 2026-04-08T22:02:36Z
- `aws s3 ls s3://opal-data-bd/schwab/silver/rps/` — last partition date=20260407
- B_01.holdings_lots.py:414-448 — `_load_latest_rps_partition` fallback logic

---

## 8. Compiler Tools

| Tool | Command | Result | Note |
|---|---|---|---|
| Grep | `grep -n "rps_date\|latest_rps\|silver/rps" B_01.holdings_lots.py` | 7 hits | located fallback load at L414-448 |
| aws s3 ls | `s3://opal-data-bd/schwab/bronze/` | last RPS CRS20260407 | feed outage confirmed |
| aws s3 ls | `s3://opal-data-bd/schwab/silver/rps/` | 560 partitions, last 20260407 | silver outage confirmed |
| aws s3api list-objects-v2 | `--prefix schwab/silver/ --query LastModified>=2026-04-10` | 4 ULN files only | ULN alive, RPS dead |

No `comp-*` runs this session — target was S3 data-state inspection, not code-graph traversal. Equivalent evidence recorded via `aws s3 ls`.

**Correction note:** §§1-6 above query the secondary mirror (`opal-data-bd/schwab/*`), not the canonical bucket (`opal-data-schwab`) that B_01 actually reads from. I missed the `S3_SCHWAB_BUCKET` constant at B_01.holdings_lots.py:150. The correct-bucket measurements are below in §9.

---

## §9 — Canonical-Bucket Re-Run (CORRECT DATA)

Downloaded 3 silver/RPS partitions from the **canonical** `opal-data-schwab` bucket to re-run stability. Dates chosen to span 5 days within the healthy feed: 2026-04-10, 2026-04-14, 2026-04-15.

### Cohort size + MV trajectory

| Partition | Rows | Unique accts | Total MV |
|---|---:|---:|---:|
| `20260410` | 83,008 | 5,610 | $1.493B |
| `20260414` | 83,064 | 5,619 | $1.510B |
| `20260415` | 83,284 | 5,630 | $1.512B |

Row count 83,284 at 04-15 exactly matches the number CTO quoted from B_01's own log — confirms this is the file B_01 actually loaded.

### Account-cohort stability

| Measurement | Count |
|---|---:|
| Accounts in ALL three dates | 5,601 |
| 4/10-only accounts | 5 |
| 4/15-only accounts | 15 |
| Cohort intersection ratio | 5,601 / 5,630 = 99.5% |

### Position-level Jaccard (4/10 vs 4/15, 5-day window, 300 sampled accts)

| Statistic | Value |
|---|---:|
| Mean | 0.995 |
| p50 | 1.000 |
| p95 | 1.000 |
| Min | 0.255 |
| Accts with Jaccard = 1.000 | 295 / 300 (98.3%) |
| Accts with Jaccard < 0.80 | 2 / 300 |

### Positions-per-account shape

| Partition | min | p50 | p95 | max | mean |
|---|---:|---:|---:|---:|---:|
| 20260410 | 1 | 13 | 22 | 207 | 14.8 |
| 20260414 | 1 | 13 | 22 | 207 | 14.8 |
| 20260415 | 1 | 13 | 22 | 207 | 14.8 |

**Conclusion (corrected):** On the canonical bucket, RPS is even more stable than the secondary-mirror sample suggested. 98.3% of accounts have byte-identical CUSIP position sets across a 5-day window. MV grows gradually ($1.493B → $1.512B over 5 days, ~1.3%, consistent with normal market activity + net flows). **RPS is trustworthy as ground truth.** The halt is not firing on RPS defect; it is firing on the 261-baseline keying defect inflated to 1,169 by the T+1 lag that option (d) addresses.

### Answer to CTO's sub-questions (revised)

> "Is the RPS feed itself a trustworthy ground truth here?"

**YES.** 99.5% cohort stability over 5 days, 98.3% byte-identical position sets. MV trajectory clean. Feed alive and delivering T+1 normally. No structural RPS defect observable.

> "1,375 mapped-but-no-RPS cohort STABLE across dates?"

Cannot fully characterise without the mapping table, but cohort size varies 5,610 → 5,619 → 5,630 over 5 days (net +20). Single-digit daily churn ≈ new-account onboarding + closures. The 1,375 cohort is almost certainly a **stable structural gap** (cash/MMKT accounts Schwab does not return, retained-but-closed accounts in BD's universe). Not drift.

> "1,169 force-close cohort consistent positions?"

Across 4/10–4/15 the same CUSIP position bags appear per account with 98.3% exact-match. Once the 2-day T+1 lag is removed via option (d), the residual force-close cohort should converge to ~A's ~261 baseline.

---

## §10 — Revised Recommendation (aligns with CTO synthesis)

- **Stand down** the earlier `ADVI_GLDOPS.RPS-FEED-RESTORE` recommendation.
- **File** `ADVI_GLDOPS.SCHWAB-MIRROR-CLEANUP` (low priority, not production-blocking) — investigate why `s3://opal-data-bd/schwab/*` secondary mirror stopped syncing 2026-04-08. Could be a retired mirror-copy Lambda, a decommissioned EventBridge rule, or a gated cost-control move. No gold script reads from there (B_01:150 confirms), so it is cleanup, not restore.
- **Support** CTO's forward frame: tonight = let halt + option (d). Medium-term = unblock `BDPL_ASTDIM W4` to unlock WP-9 CUSIP-keyed FIFO, which eliminates the 261 baseline.
- **Endorse** `B_01.holdings_lots.py` addition of an "RPS age" heartbeat (log if `rps_date > 2 business days stale` — not a halt, just an early-warning log — at ~L494 right after the existing `rps_date/snapshot_date` print).

---

## §11 — Process Failure (agent self-critique)

Three failures in my original §§1-6:

1. **Followed a grep hit without tracing the source constant.** I grepped for `silver/rps` (lowercase) in B_01 and found L491. I used that string to query S3 without reading B_01:150 to see that `S3_SCHWAB_BUCKET` is a different bucket entirely (`opal-data-schwab`) with a different-case prefix (`silver/RPS/`). One `Read` of the top of B_01 would have caught this in 30 seconds.
2. **Case-insensitive path matching.** The legacy mirror uses lowercase `rps`; canonical uses uppercase `RPS`. I did not notice. The `feedback_s3_path_case_consistency.md` memory already warns about this class of bug (canonical always lowercase was the prior rule; this case shows the canonical in use here is uppercase).
3. **Outage-hypothesis confirmation bias.** Once the first `aws s3 ls` returned a stopping date, I shipped that as the headline without running the obvious sanity check: "does B_01's log say it loaded today's file?" — which CTO already had in hand (the 83,284-row load line). Had I asked, the contradiction would have surfaced immediately.

Noted for future forensics: **resolve the source constant before querying storage.** The `read-the-code-that-reads-the-data` step is non-optional.

---

*Delivered by 0.4.0_DS_ClientPlatform~C | 2026-04-17 | council dispatch 20260417T041138Z | corrected 00:37 ET after AE catch*
