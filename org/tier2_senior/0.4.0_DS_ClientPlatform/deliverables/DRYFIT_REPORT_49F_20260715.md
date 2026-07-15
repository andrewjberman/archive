# DRY-FIT REPORT — 49F legacy D publishers vs the canonical seed (OPAL_GLDRNS.A3, exercise half)

**TO:** OPAL_GLDRNS.A3 | **Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-07-15 (~21:5x-22:xxZ)
**GO:** CTO 212552Z (D_04 + shim-census-first; D_00f exercise-1 on low canonical coverage — triggered).
**Read/write surfaces of the whole run (TO evidence requirement):** READS = opal-data-bd GET/LIST
(legacy gold + platinum + `canonical/schwab/` seed outputs) + ONE monolith GET
(`opal-data-assets .../dim_account_xref/date=2026-07-14`, the D1 v1.1 bridge). WRITES = LOCAL SINK
ONLY (session scratchpad `dryfit_sink/`); the driver wraps the module s3 client in a guard
(put/delete RAISE, copy neutralized) and D_00f ran under its native `--dry-run --validate` path.
ZERO bucket writes of any kind. Vehicle: seed execution pattern (build plan: box not a blocker);
driver committed at `runners_49f/dryfit_driver.py`.

## 1. THE SHIM CENSUS (the run's first output, per the GO)

Seed materialized estate (listed live): 15 gold tables @ `opal-data-bd canonical/schwab/gold/`,
ALL at `date=2026-07-06` (hand-run 2026-07-07 10:56-10:58Z) + silver dims (`dim_account`,
`dim_advisor_fee`, `dim_advisor_role`, `dim_asset`, `dim_relationship`, `fact_*`).

**D_00f (3 direct inputs):**

| legacy input | seed candidate | census verdict (bytes-grounded) |
|---|---|---|
| `gold/canonical/nna/{date}.parquet` — DAILY atomic (date, account_id) w/ daily_inflow/daily_outflow/nna_txn (measured: 6,672 rows x 15 cols per day) | `canonical_nna/date=2026-07-06` | **NOT-SHIMMABLE — GRAIN GAP.** Seed table is WINDOWED (period_start, period_end, account_id; nna_cash/nna_in_kind/nna_total; 30,008 rows x 13 cols). NO daily-atomic flow table exists anywhere in the seed estate (account_gains is also period-windowed). STRUCTURAL FINDING -> sec-3 F1 |
| `gold/dimensions/accounts_dimension_latest.parquet` (33 cols incl. geo, first_seen, display names) | `silver/dim_account/asof=2026-07-06` | **NOT-SHIMMABLE-TODAY — COLUMN GAP, SPEC-COVERED.** Seed dim is 12 cols (identity/tax/strategy); NO client_city/state/country, NO relationship_first_seen_date, NO account/relationship display names. The A_00 spec (dictionary §5) ALREADY carries rows for all of these — a seed-vs-spec materialization gap, NOT a spec gap. -> sec-3 F2 |
| `gold/views/account_team.parquet` (6,535 rows; 6 roles incl. architect_no_infer) | `advisor_attribution/date=2026-07-06` (5,923 rows; 6 roles + splits + provenance) | **SHIMMABLE VIA TWO-STEP DECLARED ADAPTER** — (1) ID-SPACE BRIDGE (sec-3 F3): seed is CRS-keyed (`0010023253`), legacy is BD-z-keyed (`z0822930271`) — zero direct join; the D1 v1.1 `dim_account_xref` bridges (6,200 rows, unresolved in-band); (2) rename `architect_no_infer := architect` (lawful in divergence D6 — seed roles are bd-bridge FACTS, inference obsolete) |

**Denominator: 0/3 drop-in, 1/3 adapter-shimmable, 2/3 structural findings.**

**D_04 (from the A1 input map):** its build is dominated by OTHER-D/C_06 JSON artifacts
(clients_tab, employee_leaderboard, fee_efficiency, header_metrics_{gran}, firm_mix_views,
firm_composition, advisor book/timeseries/mix, client detail/views/composition, account
aua_timeseries) — the seed produces NONE of these JSON surfaces (its `portal_aggregates` /
`partner_analytics` are TABLES, not the artifact family). Parquet-side inputs (account_performance,
holdings_lots, nna, dims, account_team) have seed candidates but every one inherits the F3 id-space
bridge requirement. **Denominator: ~0/14 of D_04's direct inputs shim mechanically.**

**COVERAGE JUDGMENT (stated, per the GO): MATERIALLY LOW.** Per the GO's rule, D_00f ran as
exercise-1 (the FIT, on the one adapter-shimmable axis) and D_04 as exercise-2 (the SHIM/plumbing,
all-legacy reads DECLARED — it exercises run-and-diff mechanics, not the C-fit).

## 2. Exercises

### 2a. Exercise-1 — D_00f (THE FIT, attribution axis)

Design: BASELINE (all-legacy inputs) vs SHIMMED (account_team <- seed advisor_attribution bridged
through the xref) — (baseline vs served) is the plumbing control; (baseline vs shimmed) isolates
the seed-attribution fit signal inside divergence D6's declared domain.

RUN NOTE (honest): the first attempt OOM'd at a 21.8M-row melt (999MiB allocation) under
multi-agent host memory pressure — a LOCAL RESOURCE fact, not a code defect (the same build runs
nightly on the r6i.4xlarge). Mitigation: one build per process (`--run` flag added to the driver).

**RESULTS (runs 21:48-22:16Z, one build per process):**

- **BASELINE:** 2,382 nna partitions (7,286,806 rows, 2020-01-02..2026-07-10), account_team 6,535,
  ALL in-artifact invariants PASS (AC-F4b.1 cohort tie-outs; W1 geo/city/client partition
  completeness to-the-cent, 9 windows; W6 reconciliation all_pass). Artifact 81.9MB (indented local
  form). 168 advisors (2 buckets), 11,746 client leaves, 4,213 bucket-fallback accounts.
- **PLUMBING CONTROL (baseline vs SERVED, harness):** 4,100,619 fields — **DESIGN 0 / FAIL 0 =
  PASS** under the declared one-cent policy (streak 1/3 recorded). The raw exact-diff first
  measured 369/4,100,619 fields (0.009%) as +-0.01 cent-flips (float summation-order jitter at the
  artifact's cent-rounding; max abs delta 0.0100000054). TWO instrument findings folded into the
  harness at source, test-pinned: (1) `--abs-tol` added — a tolerance is a DECLARED POLICY, never a
  default (0.01 = the money cent-flip policy; exact remains default); (2) the bound carries a
  micro-cent epsilon because a one-cent delta between ~1e6-scale binary floats measures 5.4e-9
  ABOVE 0.01 — without it, 7 rows leaked and were saved only by declared-domain luck.
- **SHIMMED:** xref bridge carried **4,926/5,923 seed attribution rows** into BD id space (997
  unbridged DROPPED-AND-COUNTED); account_team 6,535 -> 4,926; bucket-fallback accounts
  4,213 -> 5,822 (+1,609); advisors 168 -> **149 (19 named books vanish**: Andrew Rose, Andrew
  Stafford, Bryan Guzman, Connor Haney, Dominic DePizzol, Ethan Schwab, Jack Burgess, Jimmy Evans,
  Jon-Michael Chadwick, Kate Gotta, Logan Parrott, Luke Blackmon, Madelyn Devillier, Meredith
  Lipps, Mike Kipniss, Nathan Grande, Noah Plotkin, Taylor Funke, Tyler Pace); client leaves
  11,746 -> 9,587; all-roles advisor NNA mass QTD 33.3M -> 18.6M (-44%), YTD 837.8M -> 308.4M
  (-63%), MAX 4,876.8M -> 3,522.3M (-28%). **ALL in-artifact invariants STILL PASS** under seed
  inputs, and the FIRM SPINE IS BYTE-IDENTICAL (firm windows/series, geo, nmnc/nmec — proven at
  field level: attribution does not touch the firm numbers).
- **THE FIT DIFF (baseline vs shimmed, harness + registry, cent policy):** 4,100,619 fields,
  148,058 diff rows — **148,046 (99.99%) classified DESIGN inside divergence D6's declared domain
  (`advisors.*`)**: the registry routed the attribution-axis shift exactly as designed. **11 FAIL
  rows are the TUNING LAW working:** consequence fields of the same divergence
  (`granularity_coverage.n_advisors/n_client_leaves/n_individual_advisors` +
  `reconciliation.per_window.*.advisors_sum`) whose globs D6 does not carry — widening them is a
  design event, REQUESTED of CTO in the close (not applied unilaterally).
- **FIT VERDICT (attribution axis):** the C_08 port has a MEASURED coverage bar to clear before
  D parity can streak — close the 997-row xref gap + the seed-attribution universe gap (6,535 vs
  4,926 accounts; 19 advisor books; 1,609 bucket-fallback accounts; the -44%/-63% attributed-mass
  deltas are the acceptance denominators). Failures are A2-verdict inputs per the TO: T5's CARRIED
  verdict gains the same xref-coverage condition F3 named.

### 2b. Exercise-2 — D_04 firm phases (THE SHIM/plumbing)

8 firm-level builders run with writes to the local sink; reads all-legacy (DECLARED); prior_week
copy_object NEUTRALIZED by the guard. Expectation: near-identity vs served (same nightly inputs,
same calendar day for window anchors); the harness classification proves the diff mechanics on
real full-size artifacts.

**RESULTS (run ~22:2xZ): 8/8 phases ran, 0 failed, 13 files to the local sink, prior_week
`copy_object` NEUTRALIZED by the guard (logged), zero bucket writes.** Harness diff vs served,
12 firm surfaces, declared cent policy: **12/12 PASS, DESIGN 0 / FAIL 0, 2,921,738 fields total**
(dashboard 21 / mix_summary 368 / header_metrics 75 / timeseries_overview 10,594 / partner_analytics
q/m/a 394,442+375,005+407,738 / cumulative_chart 171,925 / leaderboard 72,327 / clients-tab-slim 20 /
timeseries_chart 1,460,111 / fee_efficiency 29,112). The local rebuild reproduces the served platinum
surfaces EXACTLY (same nightly inputs, same-day window anchors) — the run-and-diff mechanics are
proven on real full-size artifacts, as declared this exercises the SHIM, not the C-fit.

## 3. FINDINGS (each routes somewhere; none silent)

- **F1 — STRUCTURAL, A2 CORRECTION (T10): the daily-atomic NNA table is a HARD D-group input and
  the seed/plan C_03 does not carry it.** Legacy `canonical/nna` daily grain feeds D_00b (daily
  chart series), D_00c, D_00f (window sums from atomic), D_01, D_02, D_04. The seed's G6 is
  windowed-only. The C_03 spec (Wave-3, freeze released 211544Z) MUST include the daily-atomic
  grain (or every D port loses its daily series — not viable). ROUTES TO CTO pre-C_03-port; A2
  T10's CARRIED verdict gains this grain condition.
- **F2 — seed-vs-spec materialization gap (dim_account):** geo/first-seen/display-name columns are
  in the A_00 spec but not the seed's materialized dim. The A_00 port must materialize them before
  ANY D publisher fits. No A2 verdict change (T3 cites the spec, and the spec covers). Noted for
  the Wave-2 live-run evidence plan (A_00 vs legacy overlap diff already names these axes).
- **F3 — MEASURED: the id-space duality is the FIRST fit dependency of every D port.** Seed/monolith
  keys are CRS space; every legacy D input is BD-z space. `dim_account_xref` (D1 v1.1) is the ONLY
  bridge; unbridged rows (826 unresolved in-band at 07-14) are a permanent census line in any
  parity denominator. The dictionary §4 named the duality as design ("the xref carries BOTH or one
  feed strands"); the dry-fit turned it from a design note into a measured run requirement: the
  A3 harness parity runs will need the xref in the comparison path until ports emit BD-space ids
  (or the FE/platinum contract re-keys — a cutover-scope question, NOT this lane's).
- **F4 — host-resource note for local exercises:** full D-publisher builds at 0833 scale exceed
  comfortable local memory under fleet load; one-build-per-process is the standing driver pattern,
  and anything heavier belongs on the box (0.7.0's vehicle thread, per the build plan).

## 4. Harness classification + run denominators (the TO's acceptance rows)

| exercise | fields compared | DESIGN | FAIL | verdict |
|---|---|---|---|---|
| Plumbing control (D_00f baseline vs served) | 4,100,619 | 0 | 0 | PASS (cent policy; raw exact-diff: 369 cent-flips, 0.009%) |
| THE FIT (D_00f baseline vs seed-shimmed) | 4,100,619 | 148,047 (99.99% in D6's `advisors.*`) | 11 (consequence fields; D6-widening requested, not applied) | FIT MEASURED — C_08 coverage bar quantified (sec-2a) |
| THE SHIM (D_04 firm x12 vs served) | 2,921,738 | 0 | 0 | PASS 12/12 |

Field match rates w/ denominators per the TO: control 4,100,619/4,100,619; fit 3,952,561/4,100,619
matched (96.39% — the 3.61% delta IS the measured attribution-axis divergence, 99.99% of it
declared); shim 2,921,738/2,921,738. Streak state recorded (all exercised surfaces at 1/3 — the
multi-day accounting begins with the real parallel-prefix runs, not these locals).

**Instrument changes made DURING the dry-fit (all test-pinned, committed with this report):**
`--abs-tol` declared-policy tolerance + micro-cent float-repr epsilon (the 7-leaked-rows lesson);
one-build-per-process driver mode; the xref-bridged adapter. **Registry widening REQUESTED (tuning
law, CTO sign-off): D6 field globs + `granularity_coverage.*` + `reconciliation.per_window.*.advisors_sum`.**

-- FINAL — exercises complete 2026-07-15 ~22:3xZ --
