# MDPF_GLOBAL.T1C — Cottonwood Pattern-Parity Census + Checklist (v1, Phase 1-2)

**Author:** 0.2.0_DS_PortfolioAnalytics · **Date:** 2026-08-03 ~21:15Z · **TO:** MDPF_GLOBAL.T1C.cottonwood-on-pattern (COO GO 20260803T210322Z @760e567895)
**Pattern authority:** CTO T2.B ruling @440d16e018 (PRD s.C.3). **Cites @ e82271228b** unless noted. **This file is the acceptance instrument** — rows re-grade as work lands; v1 = pre-restructure baseline.

## The cottonwood leg today (grounded)

All four cottonwood artifact types are produced by **chain Stage 6d** (`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:497-541`), inside the same INF-event-gated chain as everything else:

1. `build_dim_model_portfolio.py --date <latest fact_model_assignment partition, runtime-resolved :521-524> --upload` → `blackdiamond/cottonwood/gold/dim_model_portfolio/date=D/data.parquet` (`:378-383` of the script)
2. `build_cottonwood_mdpf_pair.py --date D --upload` → the three sidecars `gold/mdpf_revamp/cottonwood/{account_distribution,aum_metrics,account_units}.json` (`:475-476,:500`)
3. `build_cottonwood_mdpf_slice.py --upload` → `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` (`:707-713`); reads cot's own gold + `fact_holdings` totals + the **global artifact for its DATE AXIS** (`:16`, docstring) + the frozen interpolated backfill compose
4. **Global-only re-stage** of `dim_mdpf_aggregate_aua_timeseries.py --firm all` (`dispatch:532-535`) — the deliberate circular-frontier resolution (`:499-509`): the slice needs 6a's fresh axis; the global fold needs tonight's slice.

Scripts live in `data/assets/scripts/gold/` (staged to the runner as `assets_gold/` with cross-tree PYTHONPATH `dispatch:510-518`). Downstream of `gold/mdpf_revamp/cottonwood/`, the chain is IDENTICAL to 49F/inflection: accrual bridge (content-derived as-of; T2.A telemetry shows all four cot types flowing) → publisher → `platinum/mdpf/cottonwood/*` with `_provenance`.

**Live as-ofs at census (from the 08-03 accrual telemetry):** aggregate 2026-07-27, account-distribution / aum-metrics / account-units 2026-07-24 — vendor D+2 cadence + value_date keying + the chain frozen since Friday (T2.A mechanism).

## Parity checklist (element × grade × evidence × closure path)

| # | Pattern element | 49F/inflection (canonical, T2.B) | Cottonwood today | Grade | Closure |
|---|---|---|---|---|---|
| 1 | Dedicated schedule on producing tree | Target state per T2.B(3) — does not exist YET for any scope (chain is INF-event-gated; T2.C implements the clock) | Same chain, same gating; 6d additionally hard-fails whole revamp stage if scripts unstaged (`dispatch:538`) | **RED** (fabric-wide; cot rides it) | T2.C clock (AE); cot legs must sit INSIDE the scheduled rebuild; timing values NEVER invented locally |
| 2 | Cadence window declared | T-1 settled close (T2.B(2)) | D+2 vendor cadence, roster-declared `per_partner_max_lag` carry window=3td (`dim_mdpf_aggregate_aua_timeseries.py:1759-1799`) | **AMBER** | Window values re-anchor to T2.C declared clock when it lands; roster stays the single declaration point |
| 3 | Producer topology | ONE canonical in-memory producer from monolith silver (`dim_...timeseries.py` builds 49F+INF+global) | 3-script cross-tree sub-chain (`data/assets` vs `data/mdpf`), runtime partition resolution, PYTHONPATH bridging (`dispatch:510-528`) | **RED** | Restructure candidate — DS surfaces for script logic; dispatch/staging edits are AE/DT lane |
| 4 | Axis derivation | Own-frontier `canonical_trading_axis` (49F `:787-789`; inflection standalone `:1054-1060`) | Imports the GLOBAL artifact's date axis (`slice:16,:260`), forcing the 6d circular re-stage (`dispatch:529-535`) | **RED** (DS-fixable) | Slice derives its own axis via `canonical_trading_axis` to its own value_date frontier; de-circularizes 6d (re-stage removal itself = dispatch edit, AE/DT) |
| 5 | Route shape from `gold/mdpf_revamp/{scope}/` onward | silver→revamp gold→accrual→publisher→`platinum/mdpf/{scope}/` | IDENTICAL (accrual `DECLARED_TYPES` scope-agnostic; publisher listing-derived; proven flowing in T2.A telemetry) | **GREEN** | — |
| 6 | Firm separation (NEVER#2) | n/a | All cot paths under `blackdiamond/cottonwood/*` within opal-data-assets; consumed at revamp boundary; zero bd references | **GREEN** | — |
| 7 | Manifest/provenance emission | `meta.source_vintage` (per-feeder vintages + `trading_days_behind` NEVER#1 metric, `:175-232`), frontier-stamp staleness verdict, `trading_day_calendar` source, `latest_cross_section` | Rich but DIFFERENT-shape meta (`slice:388-415`): basis/value_date_rekey/covered_dates/absent-policy — NO source_vintage block, NO trading_days_behind, NO calendar declaration, NO latest_cross_section | **AMBER** (DS-fixable) | Add the four pattern fields to slice meta; T-1-settled-close declaration per T2.B(2) rides `source_vintage` |
| 8 | Sidecar production | `account_distribution` via `dim_mdpf_account_distribution.py` (6b loop `:491-493` — cottonwood NOT in loop) | cot sidecars via the pair script (different producer/derivation); `aum_metrics` cot-ONLY (49f/inf/global MISSING = the R4 errors CTO ruled correct-drift); `account_units` cot-only, consumer UNVERIFIED | **AMBER** (partly by-design) | Document grid as-declared; missing aum_metrics for other scopes is NOT this TO (surfaced); account_units consumer trace still open (CTO routed) |
| 9 | Completion-marker declaration | Marker enumerates artifacts per scope | Cot present in all relevant marker lists (`dispatch:568-570`) | **GREEN** | — |
| 10 | Incident-guard rules | absent-is-None; no-fabrication; count-axis discipline | Slice implements all four named guards (docstring §1-4: $107.2M false-dip class, no-axis-assumption, strict-Opal filter, 1.51x count no-sum) + dollar-equality asserts | **GREEN** | — |
| 11 | Serve-side `_provenance` | Publisher stamps source_keys + source_vintages | Scope-agnostic — cottonwood gets identical stamping (T2.A-verified mechanism) | **GREEN** | — |
| 12 | 3-consecutive-scheduled-cycle frontier evidence | Acceptance clock | Impossible until the schedule exists (row 1) | **RED** (pending) | Follows T2.C schedule live + rows 3/4/7 landed |

**Baseline: 5 GREEN / 3 AMBER / 4 RED.** DS-actionable now: rows 4 + 7 (slice-local). Row 3 topology: DS script logic + AE/DT dispatch legs, coordinate. Rows 1/2/12 pend the T2.C clock (AE).

## v1.1 updates (21:20–21:35Z, same session)

- **ROW 13 (NEW) — 6c starvation blocker: FOUND + REPAIRED.** Stage 6 failed EVERY cycle since 07-29 at 6c (`dim_mdpf_non_model_assets.py` deployed copy NoSuchKey on the retired `json/portfolios/non_model_assets.json`; the A4 DECOUPLE fix @6a9fe4f771 landed 07-21 but was NEVER deployed) → 6d (all cottonwood legs) never reached. **CENSUS CORRECTION (COO-confirmed): the stale cottonwood as-ofs in the grounding section were STARVATION, not vendor cadence.** Repair: repo HEAD deployed 21:24Z, `comp-pipescript deployed` MATCH, ledger `org/critical_paths/change_management/20260803T2125Z_mdpf-6c-non-model-assets-a4-decouple-deploy_completion.md`, COO NO-HOLD 21:24:55Z. Behavioral proof = next scheduled cycle (6d runs, marker advances past 07-29 00:33Z) — and per COO: if tonight's event trigger doesn't fire because INF failed this morning, that is the T2.C-class trigger gap, NOT this repair failing.
- **Rows 1/2/12 clock values DECLARED** (AE T2.C @f603923cf8, 21:24:42Z): dedicated 15:00Z MON-FRI EventBridge floor on the producing tree (UTC-fixed), cottonwood INSIDE the same run (no separate cot schedule — row-1 shape confirmed on-pattern); cadence window 15:00–16:15Z (floor → accrual 15:45Z → publisher 16:15Z); evidence clock = 3 consecutive NYSE trading days, zero hand-runs. Rows stay open until the schedule is LIVE + evidence accrues.
## v1.2 updates (21:40–21:50Z)

- **CLOCK v1 VALUES SUPERSEDED (COO HOLD 21:40:35Z; CTO-mandated v2):** the v1 values quoted in v1.1
  are VOID. **v2 @5a20433a5c (AE 21:45:59Z):** America/New_York anchor whole clock; floor
  `cron(0 11 * * ? *)` ET **DAILY incl. weekends**; window 11:00–12:15 ET; derived T-1 close 10:45 ET
  (= season-worst orion landing 10:16 ET + 29min); apply PENDS my 7-day landing pull + job→table proof
  + the F2 adjudication. Rows 1/2/12 re-fold to v2 on AE's apply. My row-7 emission cites the T2.B
  RULING semantic only (no clock value) — v2-safe by construction.
- **ROW-4 STOP (reprocess guard fired, as pre-registered — COO 21:49Z):** the parity diff vs the live
  artifact found **5 common dates (2026-06-13/14/19/20/21, all NYSE non-trading incl. Juneteenth)
  carrying real measured `partner_custody_total` ($373.1–373.6M)** that a pure canonical NYSE axis
  structurally drops (fact_holdings has WEEKEND partitions; the old global-axis import carried those
  dates). Clean elsewhere: 441/441 common dates identical on model_aua/by_model/cohort_provenance;
  9 live-only dates all-None padding; 4 new-only dates = the 07-28..31 frontier advance. Options
  (a) canonical+measured-augment / (b) pure-canonical-drop / (c) row-7-alone surfaced to COO — ruling
  interacts with v2's weekend fires. **Rows 4+7 implementation committed to repo DO-NOT-DEPLOY**
  (deployed S3 slice untouched; tonight's cycle runs current production; the 6c repair unaffected).
- **⚠ CLOCK COLLISION FLAG (v1-era, superseded by the v2 re-declaration it forced; kept for the record — routed to AE 21:29Z):** measured binding-input landings — smartx `fact_model_aum_daily` ~13:40Z (2 samples: 13:40:32Z 07-31, 13:41:10Z 08-03), orion `fact_assets` ~14:16Z (08-03), eclipse `fact_portfolios_full` ~03:30Z overnight — so the declared 13:00Z T-1-silver-close predates TWO binding inputs' landings, and **orion lands only ~44min before the 15:00Z floor** (a slow orion day crosses it → the rebuild reads a day-old orion partition). Floor VALUE unaffected today; declaration text + margin need AE's re-anchor.

## v1.3 (21:55–22:00Z) — rows 4+7 IMPLEMENTED + DEPLOYED under the converged ruling

**CONVERGED RULING (CTO+COO 20260803T215349Z): (b) pure canonical axis + MANDATORY (b+) declaration
rider.** Decisive ground: the global axis UNIONS feeder axes (my own T2.A cite, dim `:1779`) — a
non-trading date admitted per-firm propagates into the served Opal aggregate; with clock v2 firing
weekends that would be standing behavior. (c) rejected with a forward door (calendar-day custody =
a NEW artifact contract if ever needed). Andrew counterweight satisfied by silver retention; CTO
surfaces the decision to Andrew as MADE.

- **Row 4 → IMPLEMENTED (GREEN pending first rebuilt cycle):** self-derived canonical axis, global-axis
  import GONE (@4d442fac2a + rider @31af5a04f1). Parity: 441/441 common dates identical on the model
  leg; the 5 measured-weekend custody drops RULED; 9 padding rows dropped; frontier advances 07-31.
- **Row 7 → IMPLEMENTED (GREEN pending CTO emission-shape validation at close):** source_vintage /
  frontier_basis (T2.B-ruling-cited, clock-value-free) / trading_day_calendar / latest_cross_section
  + (b+) `meta.axis_rule` with the computed measured-excluded enumeration (== the ruling's 5) and the
  padding class stated separately.
- **DEPLOYED 22:00Z:** `s3://opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_slice.py`
  md5==ETag `44db6559905d506352a06d4585e45ae6`; ledger
  `org/critical_paths/change_management/20260803T2200Z_mdpf-t1c-cottonwood-slice-row4-row7-deploy_completion.md`.
  Served artifact advances on the next chain cycle reaching 6d (no hand-publish).
- **Open at my seat:** AE ask-1 (7-day landing pull) + ask-2 (job→table proof) — next window; row-12
  evidence clock once clock-v2 applies.

## Notes for the record

- **HOLDs read (comp-blast):** slice 1 / pair 2 / dim 3 claims — all deploy-completion ledgers with S3 md5 pins (`20260729T0510Z_mdpf-g7...` etc.): the deployed copies are content-pinned, so ANY edit re-deploys via safe-deploy + a new ledger entry, never a silent divergence.
- **Tool-coverage gap (for COO):** all three cottonwood producers are ABSENT from every comp-pipescript tree (valid trees: bd/inf/cot/mdpf — the `data/assets` gold tree is unmodeled). I/O hand-derived from source above per the mandate's cross-check clause; the gap is one step beyond the T2.A extractor-invisibility note and worth a WS4-hardening row.
- **comp-estate:** cot MDPF legs render nowhere as a chain (only `advi-cot` exists, a different ADVI thread); they ride the mdpf stitch chain implicitly — same rendering-gap class as the T2.A accrual-family note. Estate map does NOT contradict the T2.B lineage; no STOP condition.
- **data_reprocess_scope guard:** planned restructure (rows 4/7) changes FORWARD emission only — the axis self-derivation must reproduce the current covered-date content for past dates (parity assert planned in the implementation); if any past-date shape delta appears, STOP → COO per the TO.
