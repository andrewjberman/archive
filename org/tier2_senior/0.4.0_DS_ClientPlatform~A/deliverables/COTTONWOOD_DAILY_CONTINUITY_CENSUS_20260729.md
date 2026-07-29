# Cottonwood daily-continuity census — Andrew-direct ~0320Z (read-only)

**Agent:** 0.4.0_DS_ClientPlatform~A · **Run:** 2026-07-29 ~0330-0345Z · **Calendar basis:** `lib/trading_calendar.py`
(trading-day) or calendar-day, stated per row. Weekends/holidays are NOT gaps; roster-cadence lag (D+2) is ON TIME.
**Census date context:** run 07-29 early UTC → a D+2 feed current through 07-27 is at-frontier; same-day feeds through 07-29.

## The table (layer × feed)

| Layer / feed | First | Last | Present/Expected [basis] | REAL gaps | Mechanism |
|---|---|---|---|---|---|
| **BRONZE (monolith `blackdiamond/cottonwood/bronze/`)** | | | | | |
| old date-dirs (pre-switch) | 06-13 | 07-14 | 30/32 [cal] | 06-24..25 | convention era ended 07-14 (KNOWN switch, not a gap); 06-24..25 = the two-day outage (below) |
| allocations | 04-22 | **07-27** | 89 dates [weekday] | 06-24..25 only | weekday cadence; ON TIME at D+2 |
| unrealized | 04-22 | **07-27** | 89 dates [weekday] | 06-24..25 only | same |
| holdings | 06-09 | **07-27** | 38 dates [weekday] | NONE | all apparent holes are weekends/July-4; ON TIME |
| realized | 05-22 | **07-29** | 50 dates | May–June weekly ramp | ramp cadence (KNOWN onboarding shape); daily + current since |
| transactions | 03-09 | **07-29** | 52 dates | Mar–May weekly ramp | same ramp; daily + current since (+ a `_dryrun/` xlsx dir, inert) |
| rebalancer_{models,model_detail,accounts} | 07-21 | **07-28** | 8/8 [cal] | NONE | daily incl. weekends since birth (07-21 Rebalancer pull @64fdd919c) |
| `_retry_net` | 06-26 | 07-28 | 5 dates | n/a | retry artifacts, not a feed — sparse BY DESIGN |
| **SILVER (monolith, 14 tables)** | | | | | |
| fact_allocations(+_s2) | 04-22 | **07-27** | 89 | 06-24..25 | propagated bronze outage; ON TIME at D+2 |
| fact_unrealized(+_s2) | 04-22 | **07-27** | 89 | 06-24..25 | same |
| fact_holdings(+_s2) | 06-09 | **07-27** | 38/33 [trading] | **NONE** | **the COO-trace known-unknown ("frozen post-07-24") is RESOLVED: it ADVANCED to 07-27** |
| fact_realized(+_s2) | 05-22 | **07-29** | 50/46 | ramp-era only | ramp cadence |
| fact_transactions(+_s2) | 03-09 | **07-29** | 52/99 | Mar–May weekly | ramp cadence |
| fact_model_{roster,assignment,blend,definition} | 07-21 | **07-28** | 8/6 | NONE | daily incl. weekends since birth |
| **GOLD DDB `opal-assets-daily-aua`** (scan denominator: 4,678 cottonwood items, 6 cohort_ids) | | | | | |
| cottonwood_bd_holdings rows | 2020-04-28 | **07-28** | 2,281/2,283 [cal] | rows MISSING **07-23..24** | **KNOWN: 4c cadence-demand pending (AE)** |
| cottonwood_bd_holdings values | 06-09 | **07-22** | 35 values | none in-span beyond weekends | **KNOWN: G7 slice re-key pending (DS base)** — value=NULL 07-25..28 |
| cottonwood_bd_models | same shape | values 07-21..22 | | rows missing 07-23..24 | same two mechanisms |
| etf_*__held_cottonwood (×4) | 06-09 | **07-28** | 29/50 rows, all valued | row-gaps 06-26..07-01, 07-03..05, 07-09, 07-11..15, 07-19..24 | emitter-run coverage pre-G4-fold + ETFS baseline holes; **current 07-25..28 all VALUED (healthy now)**; precise per-gap sub-mechanism UNKNOWN-declared |
| **GOLD MDPF accrual (canonical `portal/gold/mdpf/cottonwood/{type}/{date}.json`)** | | | | | |
| account-distribution / account-units / aum-metrics | {07-20, 07-24} | | 2 dates each | n/a | **accrual BORN 07-28** (both write batches yesterday) — a birth, not a gap |
| aggregate-aua-timeseries | {07-22, 07-27} | | 2 dates | n/a | same |
| ⚠ duplicate write target | | | | | producer ALSO writes root `gold/mdpf_revamp/cottonwood/` 2 min earlier (+ an `_interpolated` file frozen 07-23). **Andrew flagged the root path as questionable; routed to CTO** — not touched |
| **PLATINUM (portal-v2)** | | | | | |
| per-firm cottonwood timeseries | grid 2024-11-01 | **07-27** | 450-date grid; **2 valued dates** (model_aua 07-21..22, $124.4mm; custody series all-null) | | **KNOWN: G7** — series born on reset night |
| global fold | | **07-27** | | | cottonwood folded via **declared carry**: `meta.cottonwood_carry` carried 07-23/24/27 ← 07-22, inside the 3-trading-day window @ D+2 (roster-basis). My first probe read "0 slots" — that was MY probe assuming a `partners{}` dict the global-slice schema doesn't have; **instrument error, corrected, not an estate break** |
| **ETFS daily (baseline)** | 06-08 | **07-24** | 30/33 [trading] | **06-23, 06-24, 07-20** | frontier = bd-vintage lag (contract working). ⚠ floor said "31/31 healthy" — I measure 30 present, 3 in-span gaps; discrepancy stated, per-gap mechanism UNKNOWN |
| **PARALLEL firm tree `opal-data-cot`** | bronze 06-13, silver 06-19 | **07-29 both** | 45+39 date-dirs [cal] | 06-24..25 | alive, daily incl. weekends; same outage window |

## The sovereign answer

**YES — cottonwood is being pulled every single day.** Bronze and silver are at-frontier on BOTH trees at their
declared cadences (D+2 feeds at 07-27, same-day feeds at 07-29, Rebalancer daily including weekends), and the
model tables run daily since birth.

**Every downstream daily-ness break is accounted for by the known mechanisms — with these named residuals:**
1. **G7 slice re-key** (KNOWN, DS base): DDB values + platinum series end 07-22; global headline covered by the
   declared carry through 07-27. ✔ matches exactly.
2. **4c cadence-demand** (KNOWN, AE): DDB rows missing 07-23..24; accrual family born 07-28. ✔ matches exactly.
3. **fact_holdings post-07-24** (was the known UNKNOWN): **RESOLVED HEALTHY — advanced to 07-27.** Not a break.

**No fourth LIVE break exists.** Three bounded residuals are named rather than absorbed:
- **(a) The 06-24..25 two-day pull outage** — all feeds, BOTH trees, healed 06-26. Historical + bounded;
  mechanism NOT on tonight's record → **UNKNOWN, declared** (candidate: session/trigger outage window).
- **(b) ETFS daily in-span gaps 06-23, 06-24, 07-20** (and the 30-vs-"31/31" floor discrepancy) — small,
  historical; mechanism **UNKNOWN, declared**; feeds the etf_*__held row-gaps via the fold.
- **(c) The duplicate gold write target** (root `gold/mdpf_revamp/` beside canonical `portal/gold/mdpf/`) —
  structural two-names-one-quantity, Andrew-flagged live during this census; **CTO to rule** (E-pass class).

Read-only throughout; zero writes, zero re-runs. Denominators printed inline per row above.
