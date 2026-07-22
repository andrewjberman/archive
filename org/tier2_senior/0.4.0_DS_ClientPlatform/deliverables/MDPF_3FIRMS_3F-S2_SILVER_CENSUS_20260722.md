# 3F-S2 — Silver completeness census + Rule-17 audit (six MDPF-feeding fact tables)

**Agent:** 0.4.0_DS_ClientPlatform · **TO:** `MDPF_3FIRMS.3F-S2` · **Vintage:** all measurements
2026-07-22 20:26–20:55Z, repo @ `61365878d`, bucket `opal-data-assets`, calendar
`lib/trading_calendar.py` (source: NYSE/hardcoded-fallback-2024-2027).
**Standard applied (Andrew-direct @`0b06b5a14`, ~20:41Z, relayed by COO 204333Z):** consistent and
validated values on the correct dates + **full coverage on trading dates** within the served window
(display floor 2024-11-01). Depth below the floor is a statement, not a defect.

## 1. Census verdict — 0 unexplained missing partitions on any table

Every denominator below was **enumerated at run time this session** (raw listings in the session
scratchpad; instrument = `aws s3 ls` prefix enumeration, cross-checked by a per-table `s3api
list-objects-v2` positive control — a different instrument — plus a planted-absence mutant control).

| # | Table | Bronze axis (enumerated) | Silver partitions | Bronze↔silver set diff | Trading-window coverage | Absences, each with named cause |
|---|---|---|---|---|---|---|
| 1 | `schwab/08242234/silver/fact_rps_s2` | `bronze/rps/` 632 dates (floor 2024-01-12) | 540 (2024-05-24→2026-07-21) | bronze−silver = 92, silver−bronze = 0 | **539/539 trading days** in window = 100% | The 92 are a contiguous HEAD-GAP 2024-01-12..2024-05-23, entirely below the 2024-11-01 display floor → **depth statement per Andrew @`0b06b5a14`**, zero mid-series gaps. +1 off-cadence partition `2025-01-09` (market closed, national day of mourning): vendor delivered a file that day; silver faithfully mirrors bronze — not a defect. |
| 2 | `smartx/platform/silver/fact_model_aum_daily` | `smartx/model/{rmid}/bronze/model_aum/` union over 11 rmids = 9 dates | 9 (2026-07-14→2026-07-22) | 0 / 0 | 9/9 run-dates (calendar-daily cadence) = 100% | None. ⚠ AXIS NOTE: run-date partitions (9) ≠ in-partition history depth (1,225 days 2021-09-02..2026-07-21 at D-1 — 0.5.0 3F-B2, corroborated). My initial 07-14/15/16 "silver-without-bronze" flag was a WRONG-AXIS comparison against `models_summary` (a different feed, moved to the yaliu bundle lane 07-17); **closed**, independently converged with 0.5.0 (his 99-object census == my 11×9 union). |
| 3 | `orion/inflection/silver/fact_assets` | `bronze/assets/*.jsonl.gz` 2272 dates | 2272 (2020-04-28→2026-07-22) | 0 / 0 | 2272/2277 calendar days; missing exactly **2026-07-11..07-15** | The 5 missing = the KNOWN monolith gap; source repaired in `opal-data-inf` (0.6.2, 07-22), propagation = tomorrow's scheduled mirror ~14:15Z + 16:00Z sweep (**3F-B3, 0.6.2 verifies; nothing hand-fired**). Bronze and silver agree exactly — the gap is upstream of this bucket, not a conversion miss. |
| 4 | `eclipse/inflection/silver/fact_portfolios_full` | `bronze/{YYYY-MM-DD}/` 54 dirs | 54 (2026-05-15→2026-07-21) | 0 / 0 | Trading-day misses in window: **6** — 05-21, 06-01, 07-01, 07-13, 07-14, 07-15 (remaining 8 calendar absences are weekends + 07-03 holiday) | All 6 are **bronze+silver joint absences** = vendor-pull-side, NOT conversion misses (conversion is 54/54 of everything bronze holds, sidecar-reconciled). Recoverability verdict = **3F-B4 (0.6.2)**. ⚠ **NEW FINDING: 2026-05-21 (Thu, trading day) is absent and was NOT on the previously-banked unfillable list (06-01/07-01/07-13/14/15) nor in PRD §2.2** — flagged to 0.6.2~A for the B4 census/verdict. Floor 05-15 is CORRECT (Inflection models began 05-15 — Andrew via COO 204333Z). |
| 5 | `blackdiamond/cottonwood/silver/fact_holdings_s2` | `bronze/holdings/HOLDINGS_DAILY_*.xlsx` 33 dates | 33 (2026-06-09→2026-07-20) | 0 / 0 | **28/28 trading days** in window = 100% | 5 off-cadence EXTRAS (06-13, 06-14, 06-19 Juneteenth, 06-20, 06-21): early-period weekend/holiday vendor deliveries, all converted faithfully; vendor stopped weekend files after ~06-22. Zero trading-day impact. 07-21's file due ~03:30Z 07-23 per the D+1 cadence contract (3F-B5 verifies the landing). Floor 06-09 = our ingest start (firm mid-migration, §8.1). |
| 6 | `blackdiamond/cottonwood/silver/fact_model_assignment` | `bronze/rebalancer_accounts/` + `rebalancer_models/` = 2 dates | 2 (2026-07-21→2026-07-22) | 0 / 0 | 2/2 since series start = 100% | None. Series started 07-21 (live-state endpoint; never backfilled — §8.2). |

**Bottom line:** silver-vs-bronze conversion completeness is **6/6 tables at zero unconverted
bronze partitions**. Every calendar absence has a named cause; **no reprocess fired by this TO**
(the only in-window repairs belong to 3F-B3/3F-B4 scheduled paths — no races with 0.6.2's 3F-S1
regex reprocess were created).

## 2. Controls (each could have failed; run separately)

- **Positive control, per table (6/6 PASS):** independent `s3api list-objects-v2` on a
  known-present partition key (KeyCount ≥ 1), then assert that date appears in the census set
  produced by the *other* instrument. One call per table, separate invocations.
- **Mutant control (PASS):** planted deletion of `2026-07-01` in a copy of the BD-holdings set →
  calendar instrument reported exactly that date MISSING. The instrument can fail.
- **Denominator provenance:** raw date-set files preserved in session scratchpad
  (`census/*.txt`); calendar resolution script reproducible (imports `lib/trading_calendar.py`).

## 3. Rule-17 compliance audit — violation list: **EMPTY** (one divergence noted, not a violation)

Converters inspected at source, repo @ `61365878d` (deployed-hash parity is 3F-S1's census cell —
0.6.2/0.7.0; not re-claimed here):

| Table(s) | Converter | Dedup mechanism | Verdict |
|---|---|---|---|
| fact_rps_s2 | `data/assets/scripts/silver/schwab_conversion.py` (+ `schwab_runtime.py`, `schwab_schemas.py`) | whole-row 16-byte-signature dedup (`:320 cr.dedup`, `:476 cr.dedup_rows`), RECONCILE-to-T1 **before** dedup (`:337-339`); explicit `typed_table` schemas | **COMPLIANT.** No fillna/dropna/filter/slimming hits. `schwab_projections.py` emits `dim_*` projections but these are the SS7-contract projection family (select-only, row-parity asserted) — the `fact_` table stays complete. |
| fact_assets, fact_portfolios_full, fact_holdings_s2 | `data/assets/scripts/silver/mirror_conversion.py` (+ `mirror_schemas.py`, `raw_json_reader.py`) | whole-table `drop_duplicates()` (`:294`) — all vendor columns; `VendorDriftError` on ANY column-set difference | **COMPLIANT.** AC-4 statement in header matches body behavior; nulls preserved (`raw_json_reader.py:162`). |
| fact_model_assignment | `data/assets/scripts/silver/rebalancer_conversion.py` | `dedup_exact` whole-row (`:171`), docstring states the law ("key-based dedup would require deciding which duplicate wins = gold's job") | **COMPLIANT.** Missing `pagedResults` RAISES rather than degrading to `[]`. |
| fact_model_aum_daily | `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py` (+ `smartx_conversion.py`) | `drop_duplicates(subset=ident_cols, keep="last")` where `ident_cols` = **all columns except our own `_ingested_at` stamp** (`:271-272`, `:358-359`, et al.) — i.e., all-vendor-columns dedup; CONFLICTING natural-key duplicates RAISE (`:274-281` one-equity-per-model-day invariant) | **COMPLIANT** — the subset excludes only our ingest timestamp, not vendor data, and conflicts refuse rather than adjudicate. |

**Itemized divergence (NOT a violation; disposition → 3F-S4 canonical-pattern contract):**
`silver.py` uses `pd.to_numeric(errors="coerce")` at `:269, :351, :449, :490, :644, :746, :908,
:1018, :1103` @ `61365878d` — an unparseable vendor numeric silently becomes null, where the
mirror family would RAISE `VendorDriftError`. Both are dtype standardization (legal under Rule 17;
nothing is fabricated — bronze retains the original bytes), but the families disagree on
strictness, and a coerced null is indistinguishable from a vendor null downstream. 3F-S4 should
pin ONE canonical behavior. **Escalation trigger check: no fillna/dropna on any served-number
path anywhere in the six-table converter set — nothing to escalate.**

## 4. Phase-1 instrument results (mandate rows)

- `comp-pipescript io <converter>`: **INSTRUMENT GAP** — the registry resolves gold scripts only;
  none of the four silver converter families are registered (`Script not found` for
  schwab_conversion / mirror_conversion / rebalancer_conversion). Fell back to reading source, as
  the mandate's own `if_mismatch` note directs. Gap noted for the comp-tools registry.
- `comp-freshness artifact` on all six tables: 6/6 PASS **but 6/6 carry "No cadence config entry
  — using default daily thresholds"** — i.e., **no MDPF leg has a `freshness_basis:
  trading-day-frontier` entry; all six sit on the flat-hours fallback that NEVER#1 warns will
  false-alarm every Monday.** Recorded as a gap per the TO (no staleness raised off it); config
  ownership routes via COO (candidate: 0.7.0 config lane).

## 5. Handoffs out of this TO

1. **0.6.2~A (3F-B4):** eclipse 2026-05-21 trading-day absence — new, vendor-side, needs a
   recoverability disposition alongside the banked five.
2. **0.6.2~A (3F-B1):** RPS depth statement — bronze floor 2024-01-12, silver floor 2024-05-24,
   92-date head-gap wholly below the display floor; zero mid-series gaps. (His depth statement can
   cite this census.)
3. **3F-S4 (me, next in sequence):** the coerce-vs-raise strictness divergence; the
   `fact_holdings` vs `fact_holdings_s2` canonical question stays OPEN for 3F-S3/S4 — deliberately
   not resolved inside this census.
4. **COO:** the comp-freshness cadence-config gap (six legs on flat-hours defaults).
