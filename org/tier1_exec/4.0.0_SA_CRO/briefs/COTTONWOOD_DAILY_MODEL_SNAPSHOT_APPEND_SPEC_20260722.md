# Cottonwood Daily Model Snapshot — APPENDED, QUERYABLE Series (Spec Brief)

**Author:** `4.0.0_SA_CRO` (Chief Research Officer) · **Home:** `org/tier1_exec/4.0.0_SA_CRO/` · **Date:** 2026-07-22
**Commissioned:** Andrew-direct, 2026-07-22 ~22:0xZ, verbatim: *"You were going to create a brief for some kind
of appended daily snapshot of the daily model holdings snapshot for cottonwood. The issue is that we, so far at
least, do not seem to have a way to query for these, so id like you to spec a brief for this."*
**Egress used: NONE.** Grounded on S3 listings + one gold parquet read. No vendor call.
**Route:** `1.0.0_SA_CTO` → MDPF_3FIRMS. **This brief PROPOSES; it does not build, dispatch, or register.**
**Grades:** **[PROVEN]** read/computed here · **[GROUNDED]** read at source · **[PROPOSAL]** design, CTO's to ratify.

> **One line: the per-day numbers Andrew wants already exist — CTO's gold `dim_model_portfolio` computes
> per-model `account_count` + `dollar_value` every day — but they land as isolated `date=` partitions with no
> appended series artifact and no query surface. The spec is an APPEND step, not a new computation.**

---

## 1. What exists today, measured **[PROVEN, S3 + parquet read 2026-07-22 ~22:1xZ]**

```
blackdiamond/cottonwood/silver/   fact_model_assignment/ fact_model_blend/ fact_model_definition/
                                  fact_model_roster/ fact_holdings/ ... (14 tables)
                                  -> model trio partitioned date=2026-07-21/ | date=2026-07-22/ ONLY
blackdiamond/cottonwood/gold/     dim_model_portfolio/date=2026-07-21/data.parquet   (8,244 B)
                                  dim_model_portfolio/date=2026-07-22/data.parquet   (8,244 B)
```

`dim_model_portfolio` (read directly, 07-22 partition): **9 rows × 12 columns** —
`model_id · model_name · rebalance_model_type · is_opal · account_count · dollar_value · accounts_with_value ·
accounts_missing_value · is_decomposed_target · is_direct_assignment · assignment_date · value_date`.

**This IS the daily model snapshot**: per-model allocation count + dollar value, with the TWO-DATES law already
applied in-band (07-22 partition carries `assignment_date=2026-07-22`, `value_date=2026-07-20` — the roster
vintage and the dollars' vintage ride every row separately).

## 2. The gap Andrew named, stated precisely

**The series is not queryable as a series.** Three concrete absences:

1. **No appended artifact.** Each day is a separate partition object. Answering *"allocation count and value for
   each Opal model, per day"* requires globbing every partition and stacking them yourself — there is no table
   where that query is a single read.
2. **No consumer surface.** The MDPF `aggregate-aua-timeseries` Cottonwood slice
   (`model_aua[] / non_model_aua[] / by_model{}` — sourcing brief §4) has nothing to read; nothing serves the
   accumulated series to the portal or to ad-hoc analysis.
3. **No firm/non-model companion.** `dim_model_portfolio` carries the model rows only. The identity
   `model_aua + non_model_aua == firm_total` (the standing 3F-G3 cross-check) needs the firm total, which lives
   in a different table (`fact_holdings`) and is re-derived ad hoc each time.

**History is retention-fragile too:** the series today is only as durable as the partition set; nothing asserts
append-only growth, and a producer change that flipped gold to overwrite-in-place would silently destroy the
accumulating history nobody is yet reading.

## 3. The proposed mechanism **[PROPOSAL]**

**An append-only daily series, accumulated from the artifacts that already land — plus a one-object query
surface.** Two pieces:

### 3a. `fact_model_portfolio_daily` — the appended series (canonical)

- **Grain:** one row per `(model_id, snapshot_date)`; `snapshot_date` = the pull/assignment date (the series axis).
- **Columns:** the 12 existing `dim_model_portfolio` columns, plus:
  - `snapshot_date` (partition key, = `assignment_date`),
  - `source` ∈ {`daily-snapshot`, `datamining-backfill`} — forward rows vs any future backfill rows,
  - `feed_live` (bool) + `feed_liveness_basis` — from 0.6.2's B6 signal (§5),
  - `row_appended_at` (UTC).
- **Companion table (or reserved `model_id='__FIRM__'` row set):** per `snapshot_date`:
  `firm_total_aua · model_aua_total · non_model_aua · account_count_total · opal_account_count` — so the
  identity check and the MDPF slice need no side-join.
- **Append rules (the contract):**
  1. **Append-only across dates.** A run may only write its own `snapshot_date` partition. Prior dates are
     never touched by the daily path.
  2. **Idempotent within a date.** Re-running a day overwrites that day's partition exactly (same key, newer
     `row_appended_at`), never duplicates rows.
  3. **Backfill-compatible by construction.** If the DataMining temporal probe ever opens the 05-28→07-21 gap,
     backfill rows land as their own `snapshot_date` partitions with `source=datamining-backfill` — keyed
     identically, additive, non-conflicting with forward data. **No hardcoded series start** (the migration
     constraint, lookback brief Amendment).
- **Location:** monolith tree, alongside what it accumulates — `blackdiamond/cottonwood/silver/` or `gold/`
  per the naming law (silver `fact_*` complete tables / gold `dim_*` projections / gold is the ONE parse-down
  point). **This is a fact-shaped series derived at the parse-down point; the name/layer call is CTO's**
  (naming law is a channel-wide contract cell). The content spec above is invariant to that call.

### 3b. The query surface — one object, regenerated on append

After each append, materialize the full series as **one consolidated artifact** (single parquet + the MDPF-shaped
JSON slice), overwritten daily from the canonical partitions:

```
.../gold/model_portfolio_series/latest.parquet          # the whole series, one read
.../gold/model_portfolio_series/cottonwood_mdpf.json    # model_aua[]/non_model_aua[]/by_model{} per §4 of the sourcing brief
```

This is what "a way to query for these" means operationally: **one GET answers the per-model daily series**,
for the portal, for MDPF, and for any agent's ad-hoc read. The partitioned table stays canonical; the
consolidated object is a derived view, cheap to regenerate (the whole series is KB-scale for years — 9 rows/day).

## 4. Per-append validation (FAIL-LOUD, from the standing identities)

Every append run carries, LOUD on any failure — never a silent land:

1. `model_aua_total + non_model_aua == firm_total_aua` to the penny (3F-G3 identity).
2. Per-model `account_count` ties to the roster: Σ opal counts == assignment-roster Opal count
   (the 296-class number), **cross-validated against the models/strategies roster `accountCount`**
   (the determinism brief's 17/17 check — two independent vendor endpoints must agree).
3. `externalId ↔ account_id` bridge exact; any drop = a named coverage flag, never a silent drop.
4. **Continuity:** `snapshot_date` gaps against the trading calendar are flagged in-band (a missed pull day is
   a visible hole, not an invisible one). Resolve trading days via `lib/trading_calendar.py` — never wall-clock.
5. **Vintage:** `value_date` staleness vs `assignment_date` is carried per-row (today's live pair is
   07-22/07-20); a widening lag is a flag, not a crash.

## 5. Liveness — the B6 fold

A stable roster and a frozen feed are byte-identical on the assignment surfaces (07-21 vs 07-22 measured
identical). Per 0.6.2's B6 determination, the **model_detail nightly revaluation heartbeat (~05:01Z)** decides
feed liveness on trading-day pairs. The appender reads that signal and stamps `feed_live` per row — **an
unchanged snapshot still appends** (unchanged is a legitimate value), but a dead-feed day is labelled, so the
series can never silently freeze while looking healthy.

## 6. What this spec deliberately does NOT do

- **No backfill.** Forward-accrual only; the 05-28→07-21 gap stays gated on the DataMining temporal probe
  (separate campaign, running under Andrew's 2026-07-22 egress word). This spec only guarantees backfill rows
  will FIT when/if they exist.
- **No re-derivation.** The appender consumes `dim_model_portfolio` (and the G8 build's output once live) —
  it does not recompute the rollup. One parse-down point stays one.
- **No serve.** Landing the MDPF JSON slice into the served pipeline is a CTO/COO call against the MDPF revamp
  state (single-flip law); this spec produces the artifact, not the serve.

## 7. Build shape + routing **[PROPOSAL — CTO/COO to staff]**

- **Effort:** small. An appender step at the tail of the existing daily chain (after gold lands) + the
  consolidated-view write + the checks in §4. No new vendor surface, zero egress, no new dependencies.
- **Natural lane:** an extension of **3F-G8** (DS is already building the current-state pair carrying identities
  (i)–(iii) as per-run checks — the appender is "G8's output, retained and accumulated"). CRO stays advisory.
- **Producer placement:** under `data/assets/scripts/` (the deploy-map hazard: `data/cot` gold auto-deploys on
  push past co-sign — keep the producer out of that tree).
- **Decision points for CTO:** (a) table name + layer under the naming law; (b) whether the appender folds into
  the G8 producer or trails it as a separate step; (c) when the MDPF JSON slice is wired to the revamp.

**Bottom line: every number this series needs is already computed daily and already correct — the spec is to
stop letting those numbers evaporate into unqueryable per-day partitions, and to make the accumulated series a
single-read artifact with its identities checked on every append.**
