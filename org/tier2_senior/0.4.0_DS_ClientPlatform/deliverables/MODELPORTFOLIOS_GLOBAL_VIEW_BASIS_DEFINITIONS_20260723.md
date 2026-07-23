# MODEL PORTFOLIOS "GLOBAL" VIEW — PER-FIRM BASIS DEFINITIONS (the recorded spec)

**Authority:** Andrew-direct rulings 2026-07-23 (via COO/CTO relays, verbatim quoted with scope).
**Author:** 0.4.0_DS_ClientPlatform. **Referenced from:** the Global spine + radial artifact `meta`.
**The governing frame (Andrew, 134944Z relay, verbatim):** *"the Model Portfolios 'Global' view is
not a true aggregate, it is a business-logic driven subsection."*

## 49financial — the served AUA of Schwab 08242234 (Andrew-DEFINITIVE, 135805Z relay)

**Verbatim:** *"This is not complicated, the 49 full number should be whatever the aua content of
the schwab 08242234 account serves."*

- **Definition:** 49F leg = the served AUA content of Schwab account **08242234** (the 0824 Model
  Portfolios master). Business-purpose-correct use of 0824 for its own view — NOT a 0824/0833
  substitution (the standing never-substitute law is not tripped; sovereign-directed).
- **The served quantity, grounded on live bytes (2026-07-23 135xZ):**
  `SUM(net_mv_plus_cash)` over `schwab/08242234/silver/fact_rps_s2/date=D/data.parquet` —
  the account's full RPS custody envelope. **07-22: $1,689,302,889.53 (7,090 rows); 07-21:
  $1,688,831,869.52.** Basis label: **SCHWAB-RPS basis** (`conversion_manifest.py:38`
  `BASIS_LABEL["08242234"]` — the Andrew-ruled basis).
- **LIVENESS (CTO condition 1, confirmed before reading it as ground):** 541 partitions, latest =
  2026-07-22 (same-day), fed by the ENABLED auto-pull (`SCHWAB_AUTO_PULL_DESIGN.md:250`,
  cron 10:15/22:15). The 07-16 decommission order was the legacy **01_raw** path on
  opal-data-schwab — NOT this live monolith feed. D1 coverage: 427/427 axis dates, zero gaps
  (named-delta ledger D-2).
- **Quantity enumeration (CTO condition 2 — cite, don't pick):** the account's feed carries
  position-grain rows; candidate quantities historically named: (a) the full envelope
  `net_mv_plus_cash` (THIS is "the AUA content the account serves" — the account's own statement
  total); (b) the model_aua projection ($1,411.3M-class, fact_model_aum_daily) — a SLICE of (a)
  used for the model leg, not the account AUA; (c) the record's old "blended-preferred
  ~$1,621.6mm" — an **01_raw-era feeder quantity, retired with that path**, not served today.
  The served AUA = (a).
- **THE PINNED DELTA vs the staged number (CTO condition 4): ZERO.** The staged 49F leg
  ($1,688,831,869.52 @07-21) was ALREADY sourced from `schwab/08242234/silver/fact_rps_s2`
  (the D-2 serve-real source; the S3 path itself scopes it to the account). Andrew's definition
  and the staged value are the SAME quantity — the earlier "raw aggregate vs subsection" framing
  dissolved on grounding: the staged leg was never a firm-wide aggregate, and the $1.64B
  reference was the legacy schwab_canonical PARTIAL-CASH REDERIVED ESTIMATE of this same account
  ($1,644,993,954.34 @07-17 common; D-2 named delta $20.3M envelope + $23.5M real growth).

## inflection — model-scope (standing)

INF leg = eclipse model AUA (`fact_portfolios_full` Opal-crosswalked), fee_scope=model.
Frontier $136,809,631.99 @07-21. No full-book component enters the view.

## cottonwood — the two-source overlay, model-scope (standing; Andrew 134545Z)

COT leg = Rebalancer-domain models overlaid with DataMining holdings values, fee_scope=model —
the full record: `COTTONWOOD_BASIS_METHODOLOGY_20260723.md`. Current measured pair value
$124,376,009.73.
