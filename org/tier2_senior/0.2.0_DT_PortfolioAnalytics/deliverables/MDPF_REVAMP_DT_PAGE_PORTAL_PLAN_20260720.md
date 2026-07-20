# MDPF_REVAMP -- DT page/portal-side plan: bucketing + gold->DDB write path + re-point mechanism

**Author:** 0.2.0_DT_PortfolioAnalytics · **Date:** 2026-07-20 · **To:** 1.0.0_SA_CTO (gate + co-sign) · **Coordinate:** 0.4.0_DS_ClientPlatform (gold dim_* shapes), 0.7.0_AE_CloudOps (CF origin + DDB TF)
**Answers CTO respawn ask 20260720T201305Z (a)/(b)/(c). Binds:** audit brief (`docs/briefs/mdpf-revamp-audit-brief-20260716.md`), gold-projection spec v1.1 (`docs/briefs/mdpf-revamp-gold-projection-spec-20260720.md`), pre-swap baseline (`docs/briefs/mdpf-preswap-baseline-20260720.md`).
**Standing constraints:** build-alongside (legacy `opal-data-mdpf/model_aua_positions` keeps serving); pure-adds (no existing key/policy/notification/scheduler touched); NO new alarms; NOTHING re-points until parity streak N=3 + never-widen co-sign (CTO+Andrew).

---

## 0. Grounding (this session, @HEAD 92c9b0bea)

- **Router** `public-data-router` (Lambda@Edge, `infra/aws/lambda-edge/public-data-router/index.mjs`): pure URI-rewrite `/api/general/json-tiered/*`->`/json-tiered/*`, `/api/general/json/*`->`/json/*`, else `/api/general/*`->`/json/*`. Origin-request trigger. No origin override today; origin = `opal-data-portal-v2` (CF behaviors 16/17, `comp-routes behaviors`).
- **FE read path** (grounded): `ModelPortfolios.tsx:370` `getMdpfAggregateAUATimeSeriesByFirm('global')` -> request `/api/general/mdpf/{firm}/aggregate-aua-timeseries.json` -> router -> `json/mdpf/{firm}/aggregate-aua-timeseries.json` on `opal-data-portal-v2`. Client fns in `portal/src/api/portal-proxy.ts`. (firm in {global,49financial,inflection}.)
- **DDB** `opal-assets-daily-aua` (`infra/aws/terraform/opal-assets/main.tf:51`): PK=`run_date`(S), SK=`cohort_id`(S), GSI `cohort_history` (PK=`cohort_id`, SK=`run_date`, projection ALL), PITR on, SSE on, PAY_PER_REQUEST.
- **Current DDB writer** `opal-assets-daily-emitter` (`infra/aws/terraform/opal-assets/emitter.tf`): READS the served `platinum/mdpf/aggregate_aua/*` partition (opal-data-portal-v2) + `opal-data-etfs daily/*`, WRITES 14 base cohort rows + N G4 ownership rows discriminated by `value_class`, daily 17:15 UTC, idempotent on (run_date, cohort_id). **This "reads-the-serve" emitter IS the flow the inversion replaces.**

---

## (a) PORTAL BUCKETING PLAN -- channel-first (Andrew-ruled)

New consumption root `portal/` in `opal-data-assets` (purpose-anchored, beside the source-anchored `{source}/{scope}/{layer}/` grammar):

```
opal-data-assets/portal/
  model-portfolios/
    global/        aggregate_aua_timeseries.json
    49financial/   aggregate_aua_timeseries.json   account_distribution.json
    inflection/    aggregate_aua_timeseries.json   account_distribution.json
  portfolios/
    global/        non_model_assets.json
```

**Key list + source projection (per spec s4 A1-A7; audit L21-22 field inventory binds parity):**

| New key (opal-data-assets) | Served today (opal-data-portal-v2) | Gold projection (DS-authored) |
|---|---|---|
| `portal/model-portfolios/{global,49financial,inflection}/aggregate_aua_timeseries.json` | `json/mdpf/{firm}/aggregate-aua-timeseries.json` | A5/A6 (fact_model_aum_daily + roster; inflection eclipse/orion) |
| `portal/model-portfolios/{49financial,inflection}/account_distribution.json` | `json/mdpf/{firm}/account-distribution.json` (**prefix confirm -- see (c)/open-Q**) | A3/A7 (fact_allocation_valuation + roster) |
| `portal/portfolios/global/non_model_assets.json` | `json/portfolios/non_model_assets.json` | A4 (49f_schwab_custody DDB + A5 model_aum; v0_9 method VERBATIM) |

**Naming note (load-bearing for (c)):** new keys use `_` (`aggregate_aua_timeseries`, `account_distribution`); served keys use `-` (`aggregate-aua-timeseries`, `account-distribution`) and the `mdpf`/`portfolios` prefixes. The divergence is bridged at re-point by the router translation, NOT by renaming (the underscore channel-first names are the spec's).

**Write/publish mechanism (my lane):** the DS gold `dim_*` projections emit the served-shape artifact; I wire the PUBLISH step (gold output -> `s3:PutObject` to the `portal/model-portfolios/*` + `portal/portfolios/global/*` keys). This is a pure-add producer path (new-territory: no existing key touched). Publish cadence rides the same signal as the gold run; no new scheduler (the gold projection's own run publishes). **No account-distribution `global/` variant** (none served today -- audit s1).

**Serving access (AE lane):** a page-serving read grant on `portal/model-portfolios/*` + `portal/portfolios/global/*` (one prefix per surface). Because CF reads S3, this is a CF Origin Access + bucket policy on `opal-data-assets` for the `portal/` prefix -- AE applies, CTO gates. Prefix-scoped (never bucket-wide).

---

## (b) GOLD->DDB WRITE PATH + PAGE QUERY PATTERNS

### The inversion (retire "reads-the-serve")
Today: feeders -> mdpf gold -> served JSON -> emitter reads-the-serve -> DDB. Revamp: monolith silver `fact_*` -> gold `dim_*` -> **(the same 14-cohort taxonomy)** -> DDB rows written FROM gold. Mechanism = **repoint `opal-assets-daily-emitter`'s SOURCE** from `platinum/mdpf/aggregate_aua/*` to the gold `dim_*` output (the roster-derived values), preserving the existing row shape `{cohort_id, value_class, value, account_count, as_of, state, basis}` and the NEVER-SUM-ACROSS-`value_class` consumer contract. Per spec F2, the `49f_smartx_platform` (`value_class=platform_model_aua`) cohort then carries the ROSTER-derived value (~$1,401.3M) instead of the legacy-feeder $1,397.2M -> ties by construction; the ~$4.1M is the named parity delta the gold author grounds.

- **value_class stays the discriminator, firm-prefixed cohort_ids unchanged:** 5-core `49f_{ultra_short_term,short_term,intermediate,lt_conservative,lt_aggressive}` (`model_value`, `basis=schwab-rps`), 2 SMA `49f_{dividend_sma,growth_sma}` (`model_value`, fold-to-non-model FE-side), `49f_smartx_platform` (`platform_model_aua`), `49f_schwab_custody` (`partner_custody_total`, `coverage_state=incomplete`), `inflection_*`, `etf_*` + G4 ownership rows. `vintage_state`/`coverage_state` are STRUCTURAL fields (spec s5) -- NOT alarms.
- **Additive cohorts/attributes = pure DATA-PLANE / zero-TF** (AE pre-scoped). The source-repoint is a Lambda code change (emitter is OPAL_ASSETS infra -> AE applies, CTO gates; I design the gold->row mapping).

### Build-alongside collision discipline
During the parity streak the LIVE emitter keeps writing the DDB from the served mdpf (the live page's registry stays consistent). The parity target is **artifact-vs-artifact** (new `portal/` gold projection vs served mdpf -- the baseline doc), NOT DDB-row overwrite. The DDB source-repoint lands AT the co-signed re-point (optionally a SHADOW dry-compare -- writer in compare-only mode, or a pure-add `-shadow` table -- to validate rows pre-swap). No two writers write the same (run_date, cohort_id) with different values during build-alongside.

### PAGE QUERY PATTERNS (the AE GSI question -- answered)
The DDB is the REGISTRY (current cohort values + per-cohort vintage/state served via the inversion); the 427-date history is NOT in DDB (it comes from `fact_model_aum_daily` via the `portal/` artifact -- spec s5 "registry is NOT the timeseries store"). Query patterns:

| # | Need | Access | Key used |
|---|---|---|---|
| Q1 | a day's cohorts (all, or firm-scoped) | `Query` base: `run_date = D` [`AND begins_with(cohort_id, "49f_")`] | base PK=run_date, SK=cohort_id (begins_with on SK) |
| Q2 | one cohort's rolling history (~21 run_dates) | `Query` GSI: `cohort_id = C [AND run_date BETWEEN ...]` | GSI cohort_history |
| Q3 | one cohort's current value+state | `GetItem` PK=run_date, SK=cohort_id | base |
| Q4 | latest run_date for a cohort | `Query` GSI: `cohort_id = C`, ScanIndexForward=false, Limit 1 | GSI cohort_history |

**CONCLUSION: existing keys cover ALL page query patterns -- NO new GSI required** (confirms CTO's read). Firm-scoping rides the `cohort_id` firm-prefix via `begins_with` on the base SK; no access pattern needs a hash other than `run_date` or `cohort_id`. The one invariant to preserve: cohort_ids stay firm-prefixed (`49f_*`/`inflection_*`/`etf_*`) so the `begins_with` firm filter holds. => the DDB write-path is **zero-TF** (data-plane only).

---

## (c) RE-POINT MECHANISM -- my read

**Current chain:** FE `/api/general/mdpf/{firm}/aggregate-aua-timeseries.json` -> `public-data-router` rewrite `/api/general/*`->`/json/*` -> S3 origin `opal-data-portal-v2` key `json/mdpf/{firm}/aggregate-aua-timeseries.json`. (account-distribution + non_model_assets analogous.)

Because the new bucket keys DIVERGE (prefix `portal/model-portfolios` vs `json/mdpf`; `_` vs `-`; `portfolios/global/` vs `portfolios/`), a bare CF origin swap will 404. Two mechanisms:

**Mechanism A (RECOMMENDED) -- router URI-translation + S3 origin-override, keys stay channel-first.**
Extend `public-data-router` (Lambda@Edge origin-request) with MDPF-family rules that, AFTER the existing rewrite, (1) TRANSLATE the key and (2) OVERRIDE `request.origin.s3.domainName` to `opal-data-assets`:
```
/json/mdpf/{firm}/aggregate-aua-timeseries.json  -> origin opal-data-assets, key portal/model-portfolios/{firm}/aggregate_aua_timeseries.json
/json/mdpf/{firm}/account-distribution.json      -> origin opal-data-assets, key portal/model-portfolios/{firm}/account_distribution.json
/json/portfolios/non_model_assets.json           -> origin opal-data-assets, key portal/portfolios/global/non_model_assets.json
```
- **Frontend unchanged** (spec s1 zero-FE-change); CF cache behaviors unchanged (still match `/api/general/mdpf/*`); the router does key-translation + origin-override for exactly the MDPF-family keys, everything else untouched.
- **Single reversible control:** the re-point is the router flag flipping on; rollback = flip off (instant, keys revert to opal-data-portal-v2). Old mdpf path runs SHADOW one cycle then retires (spec s6.3). Door 6 / mdpf trigger untouched in wave 1.
- **Preserves Andrew's channel-first bucketing** (the whole reason A beats B).

**Mechanism B (REJECTED) -- mirror exact served keys under opal-data-assets + per-behavior origin swap.** Requires writing artifacts at `json/mdpf/*`-style keys in the new bucket => violates the channel-first ruling. Rejected.

**Execution split:** router code (`infra/aws/lambda-edge/public-data-router`) = DT authors; the CF distribution behavior/origin + `opal-data-assets` Origin Access + bucket policy (`portal-auth` / opal-assets TF) = AE applies; CTO gates + never-widen co-sign (CTO+Andrew) before the flip. Mirrors the WS-4 DT-designs/AE-applies/CTO-gates split.

**Pre-execution grounding (before any flip):** enumerate the EXACT FE request paths + query keys in `portal/src/api/portal-proxy.ts` via `comp-cache` (resolve the account-distribution prefix ambiguity below); pin every served key the page actually fetches so no MDPF-family path is missed by the translation table.

---

## Open questions / coordination

1. **account-distribution prefix (confirm):** audit s1 (authoritative) says `json/mdpf/{firm}/account-distribution.json`; smartx producers write `json/portfolios/{firm}/account-distribution.json` -- possibly TWO distinct artifacts. Must pin the ModelPortfolios page's actual fetch via `portal-proxy.ts`/`comp-cache` before the re-point translation table is final. (Does not block the bucketing/DDB plan.)
2. **DS (0.4.0):** gold `dim_*` must emit the audit-L21-22 field inventory IN FULL (F4: incl. `partner_custody_total[]`, `cohort_provenance[]`), underscore key names, `generated_at` on A3/A7 (F6, `spineIsStale` input), the inflection `blend` cohort value+count (F7), key by `model_id` only (F5, no `model_name` fallback), SMA-fold only in the portal timeseries not platinum-daily (F8). I publish exactly what DS emits -> confirm shapes before I wire PutObject.
3. **AE (0.7.0):** (i) `opal-data-assets` CF Origin Access + bucket policy for the `portal/` prefix (page-serving read); (ii) DDB write-path = data-plane, NO new GSI (per (b)); (iii) the emitter source-repoint at re-point (I supply the gold->row mapping spec).
4. **CTO:** gate the router-translation design + the emitter-repoint spec; co-sign (with Andrew) the never-widen re-point after N=3 parity.

## Sequencing
1. DS authors gold `dim_*` (gated on smartx-silver-current [DONE per AE] + min-day floor F1 at first-conversion). 2. I wire the `portal/` publish path (pure-add) once shapes are fixed. 3. Parity streak N=3: `portal/` gold projection vs served mdpf (baseline doc is the fixed target; F2 ~$4.1M + the two count denominators + the two non-model numbers reproduced distinctly). 4. Optional DDB shadow dry-compare. 5. Never-widen co-sign -> router re-point flip (Mechanism A) + emitter source-repoint -> old path shadow one cycle -> retire.
