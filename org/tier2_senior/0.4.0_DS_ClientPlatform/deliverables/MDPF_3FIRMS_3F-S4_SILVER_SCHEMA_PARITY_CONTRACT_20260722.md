# 3F-S4 — Cross-firm silver schema parity contract

**Agent:** 0.4.0_DS_ClientPlatform · **TO:** `MDPF_3FIRMS.3F-S4` · **Repo vintage:** `61365878d`.
**Evidence law:** every schema statement below is EMPIRICAL pyarrow inspection of a real parquet at
the stated partition (auto-rule 7); every consumer read cites file:line @ `61365878d`. Read
2026-07-22 21:0x–21:1xZ.

---

## LAW 1 — `_s{N}` IS NOT A SCHEMA CONTRACT (the headline; demonstrated on this project's own PRD)

**`_s{N}` means "section N of the vendor workbook/file." Which section carries what is a PER-VENDOR
ACCIDENT OF LAYOUT — never a tier, never a schema version, never a pattern to bind on.**

| Table | Empirical content @ vintage | What section 2 turned out to be |
|---|---|---|
| `schwab/08242234/silver/fact_rps_s2` @date=2026-07-21 | 7,086 × 39 — account-level balances (`net_mv_plus_cash`, `money_mkt_funds`, …) | The REAL custody-envelope table — the 49F AUA source |
| `blackdiamond/cottonwood/silver/fact_holdings_s2` @date=2026-07-20 | 5 × 7 — key-value: Created / Template Name / Start Date / End Date / Date Range | The BD vendor **Timestamps sheet** (metadata; mirror_schemas `TIMESTAMPS_SECTION`) |

Consequence, already exercised: PRD §1.2 pattern-matched Schwab and named `fact_holdings_s2` as the
Cottonwood AUA source — a builder pointed at it would have computed a firm total from a metadata
sheet. Settled by the 3F-S3 joint determination (@`517bcb235`, three independent limbs):
**`fact_holdings` is canonical for the COT AUA total; the live builder is correct as-is.**

**BINDING RULE: a consumer binds to a table by NAME + EMPIRICALLY VERIFIED SCHEMA at a stated
vintage — never by suffix analogy to another vendor.** Landing every section is correct Rule-17
behavior (never drop a sheet); *naming* a section a source requires reading it.

## §1 Canonical per-firm AUA reads (settled; consumed from 3F-S3, not re-decided here)

| Firm | Total-AUA read (all silver, per PRD §3.1) | Empirical basis @ vintage |
|---|---|---|
| 49F | Σ `fact_rps_s2.net_mv_plus_cash` | decimal128(15,2), 7,086 rows @07-21; read at `dim_mdpf_aggregate_aua_timeseries.py:326` |
| Inflection | Σ `fact_assets.currentValue` | double, 34,900 rows @07-22; read at `:373` |
| Cottonwood | Σ `fact_holdings["Market Value"]` | double, 16,762 rows @07-20; read via `build_dim_model_portfolio.py:61-62,130-146` (null-ness carried as `has_value`, never laundered to 0) |

## §2 Canonical shape per DATA CLASS (empirical, stated partitions)

**Class HOLDINGS / positions (row = one position/asset of one account):**
- BD `fact_holdings` @07-20: 16,762 × 24 — **raw vendor headers with spaces** (`Market Value`,
  `AccountID`, `Cash Equivalent`) + mirror sidecar.
- Schwab `fact_rps` (s1) @07-21: 93,061 × 63 — CRS snake_case (`market_value_settled_unsettled`,
  `account_id`) + schwab sidecar.
- Orion `fact_assets` @07-22: 34,900 × 63 — vendor camelCase (`currentValue`, `accountNumber`,
  `isManaged:bool`) + mirror sidecar.

**Class ACCOUNT/ALLOCATION ENVELOPE (row = one account/allocation, money as scalars):**
- Schwab `fact_rps_s2` @07-21: 7,086 × 39, money = decimal128(15,2).
- SmartX `fact_allocation_valuation` @07-22: 9,597 × 15, money = double
  (`equity/long_equity/short_equity/cash/accrued_*`), counts int32.

**Class MODEL/PORTFOLIO (row = one model, portfolio, or model-day):**
- Eclipse `fact_portfolios_full` @07-21: 847 × 62 — vendor camelCase; **booleans land as int64**
  (`isDeleted`, `autoRebalanceOn`, `OUB`).
- SmartX `fact_model_aum_daily` @07-22: 4,318 × 10 — run-date partitioned, `day:date32` carries the
  FULL history inside the partition (consumers must NEVER accumulate run_dates —
  `dim_mdpf_aggregate_aua_timeseries.py:310` F1).
- SmartX `fact_model_allocation_roster` @07-22: 9,597 × 13 (`rmid`+`model_id` = the live bridge).
- BD `fact_model_roster` @07-22: 60 × 15 / `fact_model_blend` @07-22: 29 × 9 / `fact_model_assignment`
  @07-22: 911 × 21 — house snake_case; carries derived label `is_opal:bool` (see D6).

**Partition-date semantics differ per table (consumers read THIS row, never assume):**

| Table | `date=` means |
|---|---|
| fact_rps / fact_rps_s2 | business date (T; file lands T+1 ~10:15Z/22:15Z) |
| fact_model_aum_daily + smartx family | RUN date; history rides inside the partition |
| fact_assets | as-of snapshot day (calendar-daily) |
| fact_portfolios_full | pull day — CURRENT state filed by day (⛔ never a temporal query axis) |
| fact_holdings (+ _s2) | data as-of date (file lands D+1 ~03:30Z) |
| fact_model_assignment / roster / blend | ASSIGNMENT date; holdings value_date is separate (two-dates law) |

## §3 Column-level contract per gold consumer — **ZERO UNMAPPED READS** (acceptance #2 MET)

All references @ `61365878d`. Every silver column read by every MDPF gold consumer maps to an
empirically-present source column or a NAMED derivation:

| Consumer (file:line) | Silver table | Columns read | Map |
|---|---|---|---|
| `dim_mdpf_aggregate_aua_timeseries.py:298-306` | fact_model_allocation_roster | value, advisor_name, status, model_id (+rmid via bridge) | all present @07-22 ✓ |
| same `:312-314` | fact_model_aum_daily | rmid, day, closing_equity | present ✓ |
| same `:326`, `:341` | fact_rps_s2 | net_mv_plus_cash | present ✓ |
| same `:373` | fact_assets | currentValue | present ✓ |
| same `:409-411` | fact_portfolios_full | id, modelId, model, totalValue, isDeleted | present ✓ (isDeleted int64 — see D8) |
| `dim_mdpf_account_distribution.py:205-207` | fact_model_allocation_roster | model_id, allocation_id, advisor_name, status | present ✓ |
| same `:207-209` | fact_allocation_valuation | allocation_id, equity, as_of | present ✓ |
| same `:239-241` | fact_portfolios_full | id, modelId, model, totalValue, isDeleted | present ✓ |
| `mdpf_revamp_model_crosswalk.py:255-268` | fact_model_allocation_roster (or fact_allocation_account_map) | model_id, rmid | present ✓; bridge validated functional, conflict RAISES |
| `build_dim_model_portfolio.py:348` | fact_model_roster | model_id, model_name, is_opal, rebalance_model_type | present ✓ |
| same `:349` (+`build()` body `:169-214`) | fact_model_blend | model_id, child_model_id, child_model_name, child_rebalance_model_type, relative_allocation | present ✓ |
| same `:350` (+`:219-260`) | fact_model_assignment | strategy_name, external_id | present ✓; `assigned.model_id` = NAMED derivation (strategy_name → roster.model_name join `:222`) |
| same `:61-62,130-146` | fact_holdings | `AccountID`, `Market Value` | present ✓ (raw vendor headers — constants pinned at `:61-62` with the cot-tree contrast documented `:56`) |

Non-silver-reading MDPF gold (`dim_mdpf_non_model_assets.py`, `mdpf_revamp_count_source_audit.py`,
`build_cottonwood_mdpf_slice.py`) read gold JSONs / gold dim only — in the chain but out of this
contract's silver scope, stated for completeness.

## §4 Divergence register — every one NAMED with a DISPOSITION (acceptance #3)

| # | Divergence | Disposition |
|---|---|---|
| D1 | `_s{N}` semantics differ per vendor (LAW 1) | **CANONICALIZE THE RULE, not the tables**: bind by name+schema at vintage; suffix is layout, never contract. PRD §1.2/§2.2 COT rows = text defect, CTO amendment routed via COO @58d24b18e |
| D2 | Column naming: CRS snake_case (schwab) vs camelCase (orion/eclipse) vs raw headers with spaces (BD holdings) vs house snake_case (smartx/rebalancer) | **ACCEPT-WITH-REASON**: Rule 17 forbids renames at silver; names mirror each vendor's own format. Canonicalization happens at GOLD (the one parse-down point). In-place rename = historical rewrite = forbidden by this TO's own reprocess fence |
| D3 | Money dtype: decimal128(15,2) (schwab, fixed-decimal vendor format) vs double (all JSON vendors) | **ACCEPT-WITH-REASON + forward default**: dtype mirrors vendor delivery fidelity. New family default: decimal when the vendor is fixed-decimal, double when the vendor is JSON float. No historical rewrite |
| D4 | Provenance sidecar: schwab `{_source_file,_source_as_of,_master_observed,_section,_schema_version}` · mirror `{_source_file,_source_as_of,_source,_feed,_schema_version}` · smartx `{run_date,_ingested_at}` only · **rebalancer family: NONE (0 provenance columns)** | **CANONICALIZE FORWARD (separate TO — Rule-17-sensitive converter change)**: minimum sidecar `{_source_file|_source, _source_as_of, _schema_version}`. Rebalancer family is the priority candidate; until then a consumer needing the date derives it from the partition key = NAMED derivation |
| D5 | Numeric-parse policy: smartx `pd.to_numeric(errors="coerce")` (9 sites, silver.py @61365878d — silent null-creation) vs mirror `VendorDriftError` (refuse) | **PIN CANONICAL = RAISE-ON-DRIFT** (a refused conversion is loud; a coerced null is indistinguishable from a vendor null downstream — tonight's silent-failure class). SmartX migration = separate TO; named divergence until then. Per COO 205514Z: pinned here, NOT changed here |
| D6 | `is_opal:bool` derived business label carried AT SILVER (BD fact_model_roster/blend) | **ACCEPT-WITH-REASON**: PRD-ruled (WSE sec-3), deterministic token function of a vendor column (`rebalancer_schemas.py:157`), documented label-NOT-filter; the filter itself lives at gold. Precedent boundary: derived columns at silver require a PRD ruling — never habit |
| D7 | Partition-date semantics differ per table (§2 table) | **DOCUMENT + BIND**: this contract's table is the reference; a consumer assuming another table's semantics is a defect. fact_model_aum_daily's never-accumulate-run_dates rule is part of this row |
| D8 | Boolean dtype: eclipse booleans land int64 (0/1) vs real bool (orion/rebalancer) | **ACCEPT-WITH-REASON** (vendor JSON carries ints; declared-schema dtype standardization) + consumer hazard note: `df["isDeleted"] != True` works on int64 in pandas but any `is True` / `.astype(bool)` shortcut is a trap |
| D9 | fact_model_assignment carries NO in-table date column | Folded into D4 forward fix; until then partition-key derivation is the named path |

## §5 Instrument results (mandate rows, observed)

- `comp-pipescript io` ×6 gold consumers: registry resolves 5/6 (build_dim_model_portfolio
  UNREGISTERED — data/assets gold absent from registry, same gap-class as the silver converters);
  of the resolved, READS surfaced only hardcoded gold-JSON paths — **all six silver reads are
  dynamic-key and invisible to `io`** (its own WARN says manual review required). Column map built
  from source; io's blindness on dynamic keys itemized as a finding for the comp-tools lane.
- Empirical parquet inspection: 10 tables read at stated partitions (the 6 census tables + roster /
  valuation / model_roster / model_blend).
- `comp-blast` ×6: **NOT-FOUND with denominator printed (2,218 nodes)** — monolith silver artifacts
  are not graph nodes; a NOT-FOUND is not a nothing-breaks clear. Consumer enumeration therefore
  grounded on the `comp-grep` sweep (data/ scope, 6 gold hits) + source reads. Graph-coverage gap
  routed with the other tool gaps.
- Phase-3 `io` re-run: N/A-safe — this TO changed no script; contract-only commit (re-run performed,
  no new COLUMN GAPS possible on a doc commit).

## §6 Handoffs

- 0.6.2~A + 0.7.0: this contract is the reference their B/S1/S3 verifications cite (circulated same
  window as the commit).
- CTO (via COO): PRD §1.2/§2.2 `_s2` amendment; D5 pin ratification; D4 sidecar TO authoring.
- 3F-G-lane (me): D7 semantics table + §1 reads are the G3/G4/G8 read contract.
