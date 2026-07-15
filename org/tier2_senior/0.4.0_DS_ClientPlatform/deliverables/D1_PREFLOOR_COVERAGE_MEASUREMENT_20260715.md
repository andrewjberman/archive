# D1 pre-floor coverage measurement (S2 ruling 5, dim-consumption lens)

**Author:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~17:4xZ. **Duty:** S2 lock ruling 5 (conditional),
CTO routing 170239Z / COO consolidation 170333Z — single owner DS, "at your discretion pre-Wave-4."
Run early: read-only, close-nothing, denominators stated. **Routes to:** 1.0.0_SA_CTO for the
conditional-branch read (low/questionable -> backfill design -> Andrew).
**Method:** live listings + parquet-footer row counts (read-only) on `opal-data-bd` legacy feeds +
canonical dims; consumer needs read at source (`C_08.advisor_fee_efficiency.py`).

## 1. What the dim-consuming gold tables actually NEED (source-read)

- **C_08 (fee efficiency)** reads two SCD histories — `gold/dimensions/advisor_assignments_history.parquet`
  (A_01: fee splits SCD) + `gold/dimensions/fee_rate_history.parquet` (A_02: fee rates SCD) — and
  computes per-window regressions over **QTD, YTD, 1Y, 3Y, Max** (`C_08:492,522`). So the consumer
  class needs SCD depth up to **3Y explicitly and Max in principle**.
- **C_07 / A_00 / G-class** consume roles+splits at account grain, current-row — no deep-history need.
- **NOTE for honesty:** the legacy `advisor_assignments_history` C_08 reads TODAY is built by BD
  **txn archaeology** (the A_01 pathology, named in the design of record cell 4a) — the incumbent
  history is txn-derived by construction, not feed-grounded.

## 2. What pre-floor history EXISTS (measured, denominators stated)

**Axis 1 — FEE RATES: DEEP. Not questionable.**
`s3://opal-data-bd/silver/fees/` = **1,915 partitions, 2020-03-06 -> 2026-07-13** (~6.3 years,
~daily). Spot rows (parquet footers): 2020-03-06 = 2; 2023-07-14 = 491; 2026-07-13 = 1,086 — the
feed grew with the book. Covers QTD/YTD/1Y/3Y fully; Max to the feed's 2020-03 birth. Seam to the
new source is **seamless**: legacy rates through 07-13, the new rate source (alloc-template
account-section fee block) from 07-14.

**Axis 2 — ROLES/SPLITS: SHALLOW. Questionable for 1Y/3Y/Max.**
`s3://opal-data-bd/silver/allocations/` = **122 partitions, 2026-01-16 -> 2026-07-10**, ACCOUNT
grain (spot rows: 2026-01-16 = 6,147; 2026-07-10 = 6,877; the 46,277-byte partitions are 0-row —
verified 07-09 = 0). Zero-row on weekends/holidays (normal, trading-calendar-resolved: 06-27/28,
07-03/04/05) AND on trading days **07-06, 07-07, 07-09** (July intermittency, named); last healthy
07-10 (Fri); producer dead after.
- **RECORD CORRECTION (bytes falsify a hardened claim):** the design-note line "allocations feed
  MEASURED frozen/empty post-06-26" is **overbroad** — healthy ~1.2MB partitions exist at 06-29,
  06-30, 07-01, 07-02, 07-08, 07-10. The 06-29-era builder comment (written when the then-latest
  partitions were weekend-empties) hardened into a false general claim. Correct statement: the
  feed ran healthy-with-July-intermittency until 07-10, then died.
- **Seam to the new feed:** legacy 07-10 (Fri) -> new daily pull first partition as_of=2026-07-14
  (EMV as-of 07-13). With 07-11/12 a weekend, the role-snapshot hole is **ONE trading day
  (2026-07-13)** — immaterial for slow-changing SCD periods (periods carry; the dim's
  absent-handling is built for exactly this).
- **Pre-2026-01-16 role/split history: NO FEED EXISTS.** The only source is BD txn rows = the
  A_01 pathology; a standing derivation is banned by the design of record; a ONE-TIME labeled
  import (`period_source='txn-replay-import'`) is its own named escape hatch, Andrew-ruled.

**Canonical dim snapshots (not a history source):** `opal-data-bd/canonical/schwab/silver/
dim_advisor_{role,fee}/` carry asof = 2026-06-18, 06-24, 06-25, 07-06 (+ a malformed duplicate
`asof=20260625` in BOTH dims — unpadded format, hygiene note only).

## 3. The verdict line (the conditional, framed for the ruling)

- **Fee-rate axis: COVERED** (6.3y feed depth; every C_08 window satisfiable feed-grounded).
  No backfill design needed.
- **Role/split axis: QUESTIONABLE at Wave-4** — feed-grounded history floors at **2026-01-16**
  (~6 months by Wave-4). C_08's 1Y window would be ~half feed-grounded; 3Y/Max cannot be
  feed-grounded at all. Per ruling 5's conditional, the backfill design applies to THIS AXIS ONLY,
  and the design of record already names the shape: a **one-time, labeled txn-replay import**
  (`period_source='txn-replay-import'`, inf-AoR discipline: first-appearing-NAMED, assert-and-raise,
  never silently mixed with fact-sourced periods) — OR accept window truncation on the role axis
  (windows longer than the floor read no-role-history-before-floor, stated). Either way the
  canonical port also folds the CLEAN legacy feed span (01-16 -> 07-10, snapshot-diff — same
  mechanism as the daily process, just replayed) so the feed-grounded six months are never lost.
- **Decision returns to Andrew** per the ruling; nothing here builds anything.
