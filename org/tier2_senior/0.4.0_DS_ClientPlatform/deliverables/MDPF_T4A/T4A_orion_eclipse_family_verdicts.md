# MDPF_GLOBAL.T4A -- Tranche 1: Orion/Eclipse family verdicts (8 exemplar tables)

**archetype:** VALIDATE
**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-08-03 (~22:10-22:30Z)
**TO:** MDPF_GLOBAL.T4A.exemplar-table-verdicts @a9f8f06c55 (self-activated on WS-1 completion; COO proceed-confirm 220451Z)
**Registry rows updated:** data/_contracts/vendor_asof_registry.yaml (8 rows now carry
`T4.A EXERCISED` keys + `t4a_completeness_verdict` fields; header key-authority note amended)

## Method (all read-only; harness in session scratchpad `t4a_verdicts.py` + `t4a_schema_scan.py`)

1. **Schema scan** -- latest partition of each table read whole; candidate-key uniqueness
   printed with denominators.
2. **Key exercise** -- POSITIVE control (a REAL row duplicated in-memory must collapse to a
   size-2 key group) and NEGATIVE control (two REAL distinct rows must carry distinct keys),
   run as **separate invocations** per the TO. 8/8 PASS on both.
3. **Rates** -- within-partition duplicate rate on the declared key, last 5 existing
   partitions per table.
4. **Completeness** -- full partition-date enumeration vs `lib/trading_calendar.py`
   trading days over serve-window 2024-11+ intersected with corpus birth; weekend
   partitions counted separately as carries; shells screened within the rate window.

## Verdicts

| Table | Key (exercised) | Dup rate (last 5 parts) | Completeness |
|---|---|---|---|
| orion fact_assets | `id` (35,219/35,219 unique) | 0.0 all 5 | **COMPLETE 437/437** trading days 2024-11-01..2026-08-03; 654 weekend carries |
| orion fact_positions | `id` (confirms the Andrew-direct retro-dedup spec's measured key) | 0.0 all 5 | 436/437 -- **missing 2026-07-01 only** (assets does NOT share the hole) |
| orion fact_performance | `(client_id, date)` -- factor VALUE deliberately excluded from the key | 0.0 (full 460,676-row series unique per client-day) | **CUMULATIVE-WINDOW CLASS**: partition presence is the wrong rule; series coverage in the LATEST partition is the rule. Partition gaps 46/63 since birth 05-03 (17, all May ramp) = LOW severity |
| orion fact_transactions | `id`, LATEST-PARTITION-WINS (resolves the EditedDate mutation hazard by design) | 0.0 on 1.4M-row partitions | 53/57 since birth 05-12 -- missing 07-01 + 07-13/14/15 (the inf outage window) |
| eclipse fact_models | `id` (18/18) | 0.0 | 47/53 since birth 05-15 -- **6 missing** incl. the NEW 05-21 |
| eclipse fact_portfolios_simple | `id` (843/843) | 0.0 | same 47/53 (one pull vehicle) |
| eclipse fact_portfolios_full | `id` (855/855) | 0.0 | same |
| eclipse fact_model_composition | `id` (9/9) | 0.0 | same |

## Findings (each with an owner-shaped next step)

1. **Eclipse's known-gap ledger is short by one: 2026-05-21 is a sixth missing day** the
   puller docstring's list (5 gaps) does not carry. All 6 permanently unfillable
   (current-state-no-date). Owner: the docstring/ledger correction routes to the inf-tree
   DS lane with the _orion_vendor_asof premise refresh already queued via COO.
2. **fact_positions has a single-day hole (2026-07-01) that fact_assets does not share** --
   the two feeds pull the same endpoint family; a one-sided hole means one converter/mirror
   leg missed a day the other caught. Owner: WS-5 sweep / mirror set-identity census.
3. **The 07-01 + 07-13/14/15 cluster recurs across transactions + all eclipse tables** --
   consistent with the known inf outage window; now MEASURED per table rather than
   remembered. No backfill possible for eclipse (honest-Nones); transactions IS
   backfillable (date-addressed window) if anyone ever wants those days -- a ruling, not
   a default.
4. **Cumulative-window tables need a different completeness rule** (performance,
   transactions): each daily partition snapshots the whole series/window, so a missed
   partition day does NOT lose those dates' content -- the rule that matters is series
   coverage inside the latest partition. Registry rows updated to say so; WS-5's
   evaluator should implement that rule for this class.
5. **Dual-producer attribution is structurally unobservable at silver** for the inf dim
   feeds: both producers write the SAME bronze key (last-writer-wins), so per-producer
   duplicate attribution cannot be measured downstream of the collapse. The overlap's
   real risk is content-vintage, not row duplication (measured dup rate 0.0 supports
   this). Recorded here against the TO's attribution constraint, honestly.
6. **Eclipse silver sat at 08-02 while its bronze had 08-03** at measure time (~22:15Z) --
   an intra-day conversion-lag observation; the sweep schedule for the eclipse family is
   the confirm point. NOT an outage claim (NEVER#1 discipline).
7. **transactions 08-02 and 08-03 partitions carry identical row counts** (1,417,631) --
   same-count is not same-content; noted for the retro-dedup fingerprint axis, not
   adjudicated here.

## Repair note (process, on the record)

The first registry write of the eclipse verdicts landed on the WRONG four rows (a
first-occurrence replace walked into the orion dimension rows that precede eclipse in file
order). Caught by the immediate post-write field-position verify (grep of every
dedup_stable_key line + row-context read), reverted, re-applied anchored, YAML re-parsed
(39 rows, 31 TODO + 8 filled). The defect never reached a commit.

## Tranche 2 -- SmartX family (landed 2026-08-03 ~22:30Z, same method)

| Table | Key (exercised) | Dup rate | Completeness |
|---|---|---|---|
| fact_model_aum_daily (THE MDPF feed) | `(rmid, day)` | 0.0 x5 | **COMPLETE 15/15** trading days since C5 birth 07-14; cumulative-series class (whole per-model history each partition, day-series back to 2024-11) |
| fact_model_allocation_roster | `allocation_id` (9,650/9,650) | 0.0 x5 | COMPLETE 15/15 |
| fact_allocation_account_map | `allocation_id` (7,214/7,214) | 0.0 x3 non-shell | 14/15 -- missing 07-15 (permanent, current-state class) + **0-row WEEKEND SHELLS 08-01/08-02** that sibling tables do not produce |

Tranche-2 findings: (8) per-feed weekend-shell divergence inside one pull vehicle --
account_map lands empty weekend partitions while roster/aum carry rows; WS-5's presence
evaluator must exclude shells (it already must per the TO; this is a live instance).
(9) fact_model_aum_daily is the second cumulative-series-class table (with orion
fact_performance) -- the class rule generalizes.

Scope note: the smartx/platform/silver family carries 13 tables; tranche 2 verdicts cover
the 3 MDPF-named feeds (the TO's exemplar priority). The remaining 10 are enumerated
residue for a follow-on pass alongside BD + Schwab-0824.

## Tranche 3 -- Black Diamond cottonwood family (landed 2026-08-03 ~22:4xZ)

| Table | Key (exercised) | Dup rate | Completeness |
|---|---|---|---|
| fact_model_roster | `model_id` (61/61) | 0.0 x5 | COMPLETE 10/10 since birth 07-21; frontier current (08-03) |
| fact_holdings | `(Relationship ID, PortfolioID, AccountID, AssetID)` (16,893/16,893) | 0.0 x5 | COMPLETE 37/37 trading days 06-09..07-31 |
| fact_allocations | `(Relationship ID, PortfolioID, AccountID, Rep Code)` (1,534/1,534) | 0.0 x5 | 68/70 (missing 06-24/25) + the oscillation finding below |

Tranche-3 findings (the sharpest of the whole TO so far):

10. **The relationship dimension is part of the BD grain -- and it double-counts if
    ignored.** What first read as "2 duplicate holdings rows" is one account
    (z0927448821) holding the same LP assets under TWO relationships (rows differ only
    in Relationship ID/PortfolioID; full-row exact dups = 0, the Rule-17 silver dedup is
    clean). Any consumer summing Market Value without collapsing to (AccountID, AssetID)
    double-counts those positions (~$205K on 07-31). Semantic hazard recorded on the
    registry row.
11. **The cot LAG=0 latent snapshot risk is now MEASURED IN THE DATA**: fact_allocations
    partitions alternate full/near-empty (07-27: 3 rows -> 07-28: 1,525 -> 07-29: 1 ->
    07-30: 1,525 -> 07-31: 1,534). Landing-conservation reads GREEN while content
    collapses ~99.9% on alternating days -- the exact shape the registry's named cot
    snapshot risk predicted. Routed with the cot follow-on owner.
12. **partner_roster.json registers the DISCLAIMER SHEETS as the MDPF cottonwood custody
    feeds**: fact_holdings_s2 / fact_allocations_s2 contain 5-6 rows of (c1, c2) --
    sheet-2 footer blocks of the BD xlsx, measured at 3 vintages each -- yet the MDPF
    feed registry (data/mdpf/config/partner_roster.json:295,311, feed_ids
    bd_holdings_s2/bd_allocations_s2) points the custody feeds at them, and the emitter's
    accept_date() gates date-acceptance on those prefixes' partitions. The evidence
    blocks were built by LISTING-ONLY methods (aws s3 ls) -- existence + cadence, never
    content: the exact vintage-is-not-content class banked 08-03. The schwab precedent
    (fact_rps_s2 = real data per the emitter's own docstring) explains the pattern-match.
    Whether any consumer reads s2 CONTENT (vs dates-only) is NOT fully traced --
    ESCALATED to COO/CTO + the roster's author lane (0.7.0_AE~B), not adjudicated here.
13. **The cottonwood monolith silver plane frontier-stops at 07-31** while its
    firm-bucket source carries files labeled through 08-03 -- mirror/converter lag >= 1
    trading day at measure time. Finding for the mirror owner.

## Next tranches (per TO order)

Schwab-0824 (19 silver tables), then residue: smartx (10 tables), blackdiamond
cottonwood siblings (fact_model_assignment/blend/definition, the _s2 pair disposition
after the roster escalation resolves, fact_transactions/realized/unrealized + firm-bucket
tables), 49f monolith silver (dim_account_xref, dim_advisor_fee_role, fact_taxsma_report).
