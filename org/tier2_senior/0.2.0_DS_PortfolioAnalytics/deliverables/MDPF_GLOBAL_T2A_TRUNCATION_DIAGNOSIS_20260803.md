# MDPF_GLOBAL.T2A — Truncation Diagnosis (SOURCE-CONFIRMED)

**Author:** 0.2.0_DS_PortfolioAnalytics · **Date:** 2026-08-03 (~20:45Z) · **TO:** MDPF_GLOBAL.T2A.truncation-diagnosis (COO GO 20260803T201210Z; Andrew-direct GO @3e2b23ebb3)
**Question:** WHY does the accrual/hyphen global series end 2026-07-30 while the runner/underscore plane reached 2026-07-31?
**Repo pin:** all `file:line` cites @ commit `e82271228b` (CLOUD HEAD at trace time). Producer files last changed: `dim_mdpf_aggregate_aua_timeseries.py` @0d653d4aa3, `build_portal_gold_accrual.py` @499d956cc2.

---

## Verdict

The Addendum-C candidate — *"convergence truncation on the failed INF leg: the accrual writer truncates its global emission at the last date ALL feeders converge"* — is **REFUTED AS A MECHANISM**. No convergence/min-across-feeders logic exists anywhere on the accrual/hyphen path; nothing truncates anything.

The **causal core is CONFIRMED via a different mechanism**: the failed INF leg IS why the served series did not advance — not by truncating an emission, but by **preventing the only producer of the source tree from running at all** (a did-not-run freeze), after which two deliberately-ungated copy stages faithfully propagated the frozen 07-30-ending content to the served key.

The 07-30 value itself is not a defect of the last build: it was the **true input frontier (T-1)** of `fact_model_aum_daily` at the last successful chain run. The mechanism decomposes into three source-cited stages:

## The mechanism (three stages, all cited @ e82271228b)

### Stage 1 — The frontier bound: where "07-30" comes from

`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` (runs as Stage 6 of the daily chain, `--firm all`):

- 49F axis frontier = **max(`day`) inside the LATEST `fact_model_aum_daily` partition**: `:787-789` (`aum_days = sorted(...); frontier = aum_days[-1]; dates = canonical_trading_axis(frontier)`), reading `opal-data-assets/smartx/platform/silver/fact_model_aum_daily/` latest partition (`load_aum_daily`, `:309-317`).
- Inflection is **forced onto 49F's axis** when building global: `:2263-2266` (`axis=shared_axis`).
- Global axis = **UNION** of the three feeder axes: `:1779` (`dates = sorted(set(a49["dates"]) | set(ainf["dates"]) | set(acot["dates"]))`) — a union, NOT an intersection; cottonwood (D+2 cadence, carry window per CTO 230319Z) only ever contributes older dates. **There is no last-date-all-feeders-converge min anywhere.**
- `as_of_last = dates[-1]`: `:2113` (global), `:906` (49F), `:1145` (inflection).

**Measured input (the preserved Friday partition — the exact object the last successful build read):** `date=2026-07-31/data.parquet` (created 07-31 13:40:32Z, 4,374 rows) has **max(day) = 2026-07-30** (tail 07-28/07-29/07-30). SmartX silver is T-1: partition `date=D` carries `day <= D-1` (confirmed on both partitions measured). So the Friday 15:00Z build correctly produced `as_of_last=2026-07-30` — 07-30 WAS the frontier of its input. Nothing was cut.

### Stage 2 — The freeze: why it never advanced past 07-30

The revamp tree `opal-data-assets/gold/mdpf_revamp/*` has exactly ONE producer: Stage 6 of the daily chain (`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:476-488` runs the dim script and stages the three scope keys; global re-stage `:532-535`). The chain is event-gated on the INF sentinel (`mdpf-daily-trigger` fires on `opal-data-inf/gold/meta/pipeline-complete.json`).

**Measured:** INF `pipeline-complete.json` last 2026-07-31 14:56:49Z → chain ran; revamp tree staged 15:00:39–44Z (all three `aggregate_aua_timeseries.json` LastModified). No completes 08-01/08-02 (weekend — normal). 08-03: INF wrote **`pipeline-failed.json` 14:50:25Z** → the chain never fired → **the tree froze at Friday's build**. Meanwhile the silver kept advancing: partition `date=2026-08-03` (created 08-03 13:41:10Z, 4,382 rows) has **max(day) = 2026-07-31** — fresh Friday-close data sat unused. *(This is the NEVER#4 passenger-defect shape the accrual seam split was built to escape — the escape covered the copy stages but the tree PRODUCER is still chain-gated.)*

### Stage 3 — The faithful propagation: how the frozen vintage reached clients

- **15:45:47Z accrual bridge** (`mdpf-accrual-bridge-daily` cron(45 15)Z → `mdpf-accrual-trigger` → `build_portal_gold_accrual.py`): **deliberately ungated** — module docstring "NO convergence/freshness gate ... reads whatever the CURRENT gold source objects are" (`build_portal_gold_accrual.py:11-15` of the docstring; trigger docstring `infra/aws/lambda/mdpf-pipeline/mdpf-accrual-trigger/lambda_function.py:11-15`). It derives each as-of FROM CONTENT (`:155-175` `derive_as_of`; `as_of_last` else `dates[-1]`), plans `portal/gold/mdpf/global/aggregate-aua-timeseries/2026-07-30.json`, and **R5-skips** (key exists since Friday's 15:46Z run). Telemetry `20260803T154521Z.log`: `PLANNED 11 ... global aggregate-aua-timeseries as_of=2026-07-30 341529B ... DONE written=0 skipped_existing=11 errors=3`. **The 08-03 accrual run wrote ZERO objects** (Addendum-C's "wrote all four scopes" describes the 16:15Z publisher's served writes, not the accrual).
- **16:15:31Z publisher** (`opal-assets-mdpf-portal-publisher`, cron(15 16)Z): derives latest-date per (scope,type) from the accrual-tree LISTING (`lambda_function.py:88-108`) → latest global key = `2026-07-30.json` → re-wrote served `opal-data-portal-v2/platinum/mdpf/global/aggregate-aua-timeseries.json` (LastModified 08-03 16:15:32Z). The served object's own `_provenance` names it: `source_keys=[.../aggregate-aua-timeseries/2026-07-30.json], source_vintages={global/aggregate-aua-timeseries: 2026-07-30}, written_at 2026-08-03T16:15:31Z`.

Served content verified byte-equivalent to the frozen revamp global (same tail `[07-28, 07-29, 07-30]`, same n=453, same `model_aua[-1]=1,687,095,883.86`).

## Exercise (Phase 2 — scratch only, zero production writes)

1. **Accrual replay** (`build_portal_gold_accrual.py --dry-run`, 20:42Z): reproduces the 08-03 production derivation **line-for-line** — same 11 planned objects, same as-ofs (global `as_of=2026-07-30`, 341,529B), same 3 R4 errors. Dry-run writes nothing by construction (`:269-271`).
2. **Counterfactual on real inputs** (`dim_mdpf_aggregate_aua_timeseries.py --firm global --out-dir <scratchpad>`, 20:43–44Z): reading TODAY's real silver (partition `date=2026-08-03`, max day 07-31), the SAME producer emits `as_of_last=2026-07-31`, 454 dates, frontier cross-section 2026-07-31 (global model_aua $1,562,212,642.87). Output written to local scratchpad ONLY (script has no S3 write path — dispatch stages its local output; `comp-pipescript io` confirms WRITES: none). **A converged INF leg on 08-03 ⇒ the chain runs Stage 6 ⇒ the served global reaches 07-31.** Demonstrated, not argued.
3. **Refutation datum:** ALL THREE revamp timeseries scopes end 07-30 (08-03 telemetry: 49financial, inflection, global each `as_of=2026-07-30`). A global-specific convergence truncation cannot produce that pattern; a shared input frontier (Stage 1) does.

## The plane delta (input to CTO's T2.B ruling)

The underscore plane (`platinum/mdpf/aggregate_aua_timeseries.json`, `as_of_last=2026-07-31`, n=436, written 07-31 15:00:01Z) keys its axis on each daily slice's internal `as_of_date` = the **min-common vintage-bearing-feeder vintage** (`mdpf_aggregate_aua.py:1139-1150`; rollup `build_aggregate_aua_timeseries.py:299 → :425`), fed by the SmartX-live WS-B feeder — which carried a 2026-07-31 vintage on Friday's run. The revamp/hyphen plane reads monolith silver `fact_model_aum_daily`, which is **T-1** (measured on two partitions). **The two planes have different frontier SEMANTICS (feeder-vintage vs T-1 silver close), so they can legitimately differ by one trading day at the frontier even on a converged day.** Which semantics is canonical is exactly the T2.B producer-unification question — flagged, not ruled here.

## Notes bound by the TO

- **`dim_mdpf_aggregate_aua_timeseries.py` bare `except` (banked as `:567`; sits at `:570` @ e82271228b — line drift):** the trace CROSSES it (`load_served_account_count`, runs during the 49F/global build) but it seeds only `account_count[]` values and **cannot touch the date axis — it did NOT participate in this truncation**. Untouched per HOLD (T5.B's enumerated fix).
- **No producer edits made** (13 corpus HOLDs confirmed via comp-blast). Diagnosis only.
- **Phase-1 comp-tool notes for COO:** (a) `comp-pipescript io dim_mdpf_aggregate_aua_timeseries` now REFUSES without `--pipeline mdpf` (2026-07-30 hardening) and, with it, reports WRITES: none-detected — the platinum/revamp writes are dispatch-staged/dynamic, invisible to the extractor; (b) `comp-estate mdpf` renders the accrual family as C0 fact `mdpf-accrual-trigger` (roster), not as its own chain block — both chains present, substance matches the TO's expect, no producer-map change.
- **Scratch artifacts** (session scratchpad `t2a/`, self-expiring with the session dir): downloaded evidence copies + `replay/global_aggregate_aua_timeseries.json`. Never production evidence — production claims above cite S3/CloudWatch-side state directly.

## Evidence index (live-state reads, 2026-08-03 ~20:30-20:45Z)

| Evidence | Observed |
|---|---|
| `opal-data-inf/gold/meta/` listing | `pipeline-complete.json` 07-31 14:56:49Z; `pipeline-failed.json` 08-03 14:50:25Z |
| `gold/mdpf_revamp/{49financial,inflection,global}/aggregate_aua_timeseries.json` | all LastModified 07-31 15:00:39–44Z (frozen) |
| revamp global content | `as_of_last=2026-07-30`, n=453, tail 07-28/29/30 |
| `portal/gold/mdpf/global/aggregate-aua-timeseries/` listing | latest key `2026-07-30.json`, written 07-31 15:46:05Z |
| accrual telemetry `20260803T154521Z.log` | planned global `as_of=2026-07-30`; `written=0 skipped_existing=11 errors=3` |
| served `platinum/mdpf/global/aggregate-aua-timeseries.json` | LastModified 08-03 16:15:32Z; `_provenance.source_vintages={global/aggregate-aua-timeseries: 2026-07-30}`; tail = revamp global |
| served `platinum/mdpf/aggregate_aua_timeseries.json` (underscore) | `as_of_last=2026-07-31`, n=436, written 07-31 15:00:01Z |
| `fact_model_aum_daily/date=2026-07-31/data.parquet` | created 07-31 13:40:32Z; 4,374 rows; **max(day)=2026-07-30** |
| `fact_model_aum_daily/date=2026-08-03/data.parquet` | created 08-03 13:41:10Z; 4,382 rows; **max(day)=2026-07-31** |
| Replay A (accrual `--dry-run`) | identical derivation to production 08-03 log |
| Replay B (dim `--firm global`, local out-dir) | `as_of_last=2026-07-31`, n=454, frontier $1.562B model_aua |

*(Also observed, non-load-bearing: `platinum/mdpf/global/aggregate_aua_timeseries.json` — an underscore-named residue INSIDE the global/ served dir, 07-31 15:00:01Z vintage, presumably the old parallel-serve; surfacing for the T3/T5 cleanup census.)*
