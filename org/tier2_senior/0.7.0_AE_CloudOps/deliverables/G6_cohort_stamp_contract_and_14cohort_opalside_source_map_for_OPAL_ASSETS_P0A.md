# G6 Cohort-Stamp Field Contract + 14-Cohort Opal-Side-Source Map

**For:** `0.8.0_AE_CloudComp` (OPAL_ASSETS.P0-A -- the one-bucket DynamoDB skeleton, TO `b9fafa92c`)
**From:** `0.7.0_AE_CloudOps~A` (G6 builder -- `mdpf-pipeline-v1.5.0`) | **CC:** `1.0.0_SA_CTO~B` (schema arch-gate), `2.0.0_SA_COO`
**Date:** 2026-07-13 | **Provenance:** derived entirely from the deployed G6 checker (`infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py` @ `bbedefb95`) + CVO~A blueprint `b2a17a7e3`. **NO new bd/Schwab/RPS reads** -- Opal-side-served only.

> **Why this matters:** OPAL_ASSETS.P0-A's row shape `{cohort, source_master(s), value, as_of, state}` IS the promoted G6 stamp. If the skeleton row matches the G6 stamp EXACTLY, the 14 deployed per-cohort alarms remain the acceptance oracle for the one-bucket. Divergence breaks that. This doc pins the contract so they cannot diverge.

---

## 1. THE G6 COHORT-STAMP FIELD CONTRACT (exact semantics)

Each cohort produces ONE stamp per day. Field-by-field, exactly as the deployed checker computes it:

### `cohort_id` (string, PK component)
The stable id. The 14 (the checker's static `EXPECTED_COHORTS` taxonomy -- version-pinned to `b2a17a7e3`; repoints to the OPAL_ASSETS cohort registry when it lands):
```
etf_divz, etf_idvz, etf_pfoe, etf_pfde, inflection_models,
49f_dividend_sma, 49f_growth_sma, 49f_schwab_custody, 49f_smartx_platform,
49f_ultra_short_term, 49f_short_term, 49f_intermediate, 49f_lt_conservative, 49f_lt_aggressive
```

### `as_of` (ISO date string) -- the cohort's OWN-FIELD vintage, NEVER a cross-partner min
The single most important semantic. Read from the SERVED daily partition
`s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json`, per cohort `kind`:

| Cohort `kind` | `as_of` source field in the served partition |
|---|---|
| `etf_feeder` (the 4 ETFs) | `source_vintage.by_feeder.etf_net_assets[<TICKER>]` |
| `partner` (inflection + the 8 49F model/SMA/platform cohorts) | `as_of_by_partner[<partner>]` |
| `partner_multi_master` (cohort-8) | `as_of_by_partner["49financial"]` for the present side |

**DO NOT** use `source_vintage.overall` / `as_of_date` -- those are forced to `min(as_of_by_partner)` when any partner is rolled forward (the "vintage discrepancy" CVO~A flagged). Each cohort ages on ITS OWN feeder/partner date.

### `state` (enum) -- how it is computed
- **`fresh`** -- the cohort's `as_of` is current (staleness 0 vs the expected trading day) AND (for `partner`) the partner is NOT in `rolled_forward_partners`.
- **`rolled_forward`** -- the partner IS present in `rolled_forward_partners` (a carried block). It **ages on the OLD `as_of`** -- a rolled-forward value is STALE, never read as fresh. (This is 8 of the 14 today: all 49F cohorts, carried from 07-06.)
- **`missing`** -- the cohort's source field is ABSENT from the served partition (e.g. a partner dropped from `as_of_by_partner`). Emits the EXPLICIT high staleness value (see below), never no-data.
- **`incomplete`** -- ONLY `partner_multi_master` (cohort-8): the primary master is present-but-stale, but an EXPECTED-ADDITIONAL master is not represented in the served artifact's source-master enumeration. Present side ages normally; the gap forces the explicit high value.

### `staleness` (int, the metric value) -- what the alarm reads
NYSE-trading-days behind the expected last trading day (holiday-aware; the checker's own calendar). `fresh` -> 0. `rolled_forward` -> the real age (e.g. 5). **`missing`/`incomplete` -> explicit `99`** (`MISSING_STALENESS`). The explicit-99 is load-bearing: it keeps "I looked and it is absent" distinct from "the checker did not run" (no-datapoint = dead checker). CVO~A R7. **P0-A should carry this same convention** so the alarm value and the bucket row agree.

### `source_master(s)` -- per cohort (the source-of-record master account)
**Always a LIST from day 1** (CTO~B forward-compat gate 2026-07-13), even where single-valued today -- so a cohort that gains a second master later does not force a schema change. See the map in section 2. Only cohort-8 is multi-master TODAY (`[08242234]` present + `08335338` expected-absent); at P2 cohort-8's list is `[08335338, 08242234]`. ETF cohorts carry an empty list (fund-level, master-agnostic).

### `value` (the AUA dollar amount)
G6 itself does NOT stamp value (it is a FRESHNESS monitor -- it stamps `as_of`/`state`/`staleness`). P0-A ADDS `value`, read from the SAME served partition per cohort:
- ETFs: `etf_decomposition[<ticker>].etf_total_net_assets` (fund-level net assets).
- inflection / 49F model+SMA cohorts: the matching `partners[].by_model[]` row's `model_value` (keyed by `model_key` + `cohort_class`). See section 2 for the exact `model_key` per cohort.
- **`value` MUST carry the same `as_of`/`state` as the freshness stamp** -- a rolled_forward cohort's value is the carried value; do not present it as fresh.

---

## 2. THE 14-COHORT OPAL-SIDE-SOURCE MAP (fold-able NOW vs honest-missing)

For P0-A: which cohorts have an already-daily OPAL-SIDE served source the skeleton folds NOW, vs which land `state=missing`/`incomplete` by design (NO sovereign read -- cohort-8's absent master is P1/G2). All values below are read from the served `aggregate_aua/{date}.json`; the `model_key` is the join key into `partners[].by_model[]`.

| # | cohort_id | source_master(s) | Opal-side served source (fold NOW?) | P0 state today | value field |
|---|---|---|---|---|---|
| 1 | `etf_divz` | n/a (fund-level) | **FOLD NOW** -- `etf_decomposition[DIVZ]` + `by_feeder.etf_net_assets.DIVZ` | fresh (~T+1/2) | `etf_decomposition[DIVZ].etf_total_net_assets` |
| 2 | `etf_idvz` | n/a | **FOLD NOW** -- same, IDVZ | fresh | `etf_decomposition[IDVZ].etf_total_net_assets` |
| 3 | `etf_pfoe` | n/a | **FOLD NOW** -- same, PFOE | fresh | `etf_decomposition[PFOE].etf_total_net_assets` |
| 4 | `etf_pfde` | n/a | **FOLD NOW** -- same, PFDE | fresh | `etf_decomposition[PFDE].etf_total_net_assets` |
| 5 | `inflection_models` | inflection (WS-C/advi-inf) | **FOLD NOW** -- `as_of_by_partner.inflection` (FRESH daily) | fresh | sum of `partners[inflection].by_model[].model_value` (or per-model rows) |
| 6 | `49f_dividend_sma` | 08242234 (SmartX/bd) | **FOLD NOW (stale)** -- via 49F block, `as_of_by_partner.49financial` | rolled_forward | `by_model[model_key=opal_div_sma, cohort_class=sma].model_value` |
| 7 | `49f_growth_sma` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_growth_sma, sma].model_value` |
| 8 | `49f_schwab_custody` | **08242234 (present-stale) + 08335338 (ABSENT)** | **PARTIAL** -- 08242234 side folds (stale); 08335338 has NO Opal-side source | **incomplete (99)** | 49F custody (present side); 08335338 = no value until G2 |
| 9 | `49f_smartx_platform` | 08242234 (SmartX REST WS-B) | **FOLD NOW (stale)** | rolled_forward | 49F `model_aua` (platform total) |
| 10 | `49f_ultra_short_term` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_ultra_short_term].model_value` |
| 11 | `49f_short_term` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_short_term].model_value` |
| 12 | `49f_intermediate` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_intermediate].model_value` |
| 13 | `49f_lt_conservative` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_long_term_conservative].model_value` |
| 14 | `49f_lt_aggressive` | 08242234 | **FOLD NOW (stale)** | rolled_forward | `by_model[opal_long_term_aggressive].model_value` |

**Summary for P0-A scoping:**
- **13 of 14 populate NOW** from the served Opal-side partition (5 genuinely fresh: 4 ETFs + inflection; 8 present-but-`rolled_forward`-stale: the 49F model/SMA/platform cohorts). The skeleton can carry all 13 with honest `state`.
- **1 (cohort-8) lands `incomplete`** because its 08335338 sub-source has NO Opal-side source (never pulled). It is NOT populated by a sovereign read -- it lands honest-`incomplete`/`99` BY DESIGN and self-heals to present when G2 wires 08335338 into the served artifact. **P0-A must NOT attempt to pull 08335338** -- that is P1/sovereign-held.

**GUARDRAIL restated (COO):** every value above is read from the SERVED `opal-data-portal-v2` mdpf partition. NONE requires an `opal-data-bd` / `opal-data-schwab` / RPS source read. The rolled-forward 49F cohorts populate from the mdpf served block (carried), NOT from a fresh bd pull. cohort-8's absent master stays `missing`/`incomplete`, never pulled.

---

## 3. Match points (so the alarms stay the acceptance oracle)
1. `cohort_id` set = the 14 above verbatim (both sides pin to `b2a17a7e3` -> OPAL_ASSETS registry when it lands).
2. `state` enum = `{fresh, rolled_forward, missing, incomplete}` with the semantics in section 1 (`incomplete` only for cohort-8).
3. `as_of` = the cohort's OWN-field, never `overall`/min.
4. `missing`/`incomplete` -> explicit `99` staleness (not no-data), so the bucket row and the CloudWatch alarm agree.
5. The G6 checker emits `cohort_freshness.cohorts[]` in its invoke response + structured log -- P0-A can read that SAME structure as its populate source (or re-derive from the partition with these rules; they are identical by construction).
6. `source_master(s)` = a LIST from day 1 (match point 5 above), and the DynamoDB KEY = bucket/run-day, NOT `as_of` (`as_of` is a FIELD + `state`) -- these are CTO~B's forward-compat criteria that sit ON TOP of this field contract; they compose, this doc does not restate his key/schema half.

*Bounded contract hand-off from deployed-G6 knowledge; no new source reads. Operational half (this doc) + CTO~B's key/forward-compat half = the P0-A design input; CTO~B arch-gates 0.8.0's table-schema + emitter DESIGN before apply.*
