# NFRA_MCPINDEX.TO-MX-a-1 -- Portal analysis result

`0.9.0_WK_NFRA_MCPINDEX~3` | cell `MX-a-1` | worktree branch `wk-nfra_mcpindex-1-3` @ `4a475fe0551668f5e3d4bc4e8fc30ef667a4b7ba`
Measured 2026-09-21, run window ~05:10Z-06:10Z UTC. Instrument: `.tools/aws s3api` (account 313476888478, us-east-1,
READ verbs only), `git`, `comp-find`, direct file reads. All S3 evidence is LIVE at run time; all repository citations
print the bytes at the cited line/path (PRD Rule VII.5), at worktree HEAD `4a475fe0551668f5e3d4bc4e8fc30ef667a4b7ba`.

Read: PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md@b7dc80e2cc` (ENDPOINT, CONTRACTS C1-C8, SURFACE
MANIFEST S1-S11); decomposition `org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md@f506f63a8b`
s.1 (falsifiers), s.3 (`MX-a-1` cell, S8 acceptance), s.6 (gates), s.8 (bounds), s.11 (findings).

---

## COMMAND LOG (read verb, AC1)

All reads below are `s3api list-objects-v2` (auto-paginating; CLI combines all pages, confirmed by `IsTruncated: None`
on the final response) or `s3api get-object` (single-object content read). No write verb was used anywhere in this
cell. Full listings dumped to `.scratch/*.json` in the worker worktree (not part of the grant; not committed).

```
.tools/aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix "platinum/mdpf/"
.tools/aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix "platinum/etfs/"
.tools/aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix "platinum/advi/"
.tools/aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix "json/"
.tools/aws s3api list-buckets --query "Buckets[?contains(Name,'inflection')||contains(Name,'cottonwood')].Name"
.tools/aws s3api list-objects-v2 --bucket opal-data-inflection --delimiter /      -> AccessDenied (explicit deny)
.tools/aws s3api list-objects-v2 --bucket opal-data-cottonwood --delimiter /      -> AccessDenied (explicit deny)
.tools/aws s3api list-objects-v2 --bucket opal-data-inf --prefix "platinum/"
.tools/aws s3api list-objects-v2 --bucket opal-data-cot --prefix "platinum/firm/"
.tools/aws s3api get-object  (representative content reads, listed per table below)
```

---

## AC1 -- live prefixes, object count, total bytes, newest date, per table

**Denominator: 4 surface families (C5, A2) + 1 separate advisor-intelligence grant (C5's own carve-out) = 5 buckets
read.**

### Family 1 -- `platinum/mdpf/*` in `opal-data-portal-v2` (model AUM and account distribution)

Total: **530 objects, 4,349,692 bytes**, newest object `2026-09-20T13:50:51Z`.

| scope (2nd key segment) | table (3rd segment) | n | bytes | newest |
|---|---|---:|---:|---|
| `49financial` | `account-distribution.json` | 1 | 6,087 | 2026-09-20T13:50:49Z |
| `49financial` | `aggregate-aua-timeseries.json` | 1 | 139,839 | 2026-09-20T13:50:49Z |
| `49financial` | `aum-metrics.json` | 1 | 4,152 | 2026-09-20T13:50:49Z |
| `49financial` | `category-views.json` | 1 | 4,336 | 2026-09-20T13:50:49Z |
| `cottonwood` | `account-distribution.json` | 1 | 9,722 | 2026-09-20T13:50:50Z |
| `cottonwood` | `account-units.json` | 1 | 8,527 | 2026-09-20T13:50:50Z |
| `cottonwood` | `aggregate-aua-timeseries.json` | 1 | 127,365 | 2026-09-20T13:50:50Z |
| `cottonwood` | `aum-metrics.json` | 1 | 5,373 | 2026-09-20T13:50:50Z |
| `cottonwood` | `category-views.json` | 1 | 4,536 | 2026-09-20T13:50:50Z |
| `global` | `account-distribution.json` | 1 | 9,091 | 2026-09-20T13:50:50Z |
| `global` | `aggregate-aua-timeseries.json` | 1 | 322,220 | 2026-09-20T13:50:50Z |
| `global` | `aum-metrics.json` | 1 | 6,793 | 2026-09-20T13:50:51Z |
| `global` | `category-views.json` | 1 | 4,315 | 2026-09-20T13:50:51Z |
| `global` | `non-model-assets.json` | 1 | 94,904 | 2026-09-20T13:50:51Z |
| `inflection` | `account-distribution.json` | 1 | 7,555 | 2026-09-20T13:50:51Z |
| `inflection` | `aggregate-aua-timeseries.json` | 1 | 104,213 | 2026-09-20T13:50:51Z |
| `inflection` | `aum-metrics.json` | 1 | 4,321 | 2026-09-20T13:50:51Z |
| `inflection` | `category-views.json` | 1 | 4,533 | 2026-09-20T13:50:51Z |
| `archive/` (dated, not firm-scoped) | `aggregate_aua/{date}.json` (439 files), `aggregate_aua_timeseries.json`, `etf_ownership_timeseries/{4 tickers}.json` | 444 | 2,438,097 | 2026-08-06T21:42:10Z |
| `_manifests/` | per-date manifest | 63 | ~458,000 (rolled up) | current through 2026-09-20 |

**19 CURRENT tables** (excluding `archive/` and `_manifests/`, which are historical/bookkeeping, not "current" answer
tables -- see AC8 exclusions). `account-units.json` exists only for `cottonwood`; `non-model-assets.json` exists only
for `global`. Every other table (`account-distribution`, `aggregate-aua-timeseries`, `aum-metrics`, `category-views`)
exists once per scope (`49financial`, `cottonwood`, `global`, `inflection`) = 16, + the 2 singletons + 1 archive family
= 19.

### Family 2 -- `platinum/etfs/*` in `opal-data-portal-v2` (ETF positioning)

Total: **43 objects, 180,710 bytes**, newest `2026-09-19T11:06:19Z` (a `_manifests` entry); the served table itself
`positioning_data.json` is newest `2026-09-20T13:01:24Z` (from its own `generated_at` field, AC2).

| table | n | bytes | newest |
|---|---:|---:|---|
| `positioning_data.json` (ONE object, all 4 funds) | 1 | ~163,000 (measured via get-object `ContentLength`) | `generated_at=2026-09-20T13:01:23Z` (object content) |
| `_manifests/{date}/...` | 42 | ~17,700 | 2026-09-19T11:06:19Z |

### Family 3 -- `platinum/advi/*` in `opal-data-portal-v2` (advisor intelligence, 49financial only)

Total: **19 objects, 57,299,906 bytes**, newest `2026-09-01T11:06:00Z` (a `_manifests` entry; the newest NON-manifest
table is `perfrp_book_advisor.json` at `2026-09-01T07:27:05Z`) -- RE-MEASURED by the probe (AC1) after an earlier
draft of this document mistakenly carried the Cottonwood legacy bucket's newest date here; corrected to the LIVE
read for this specific family. All under `49financial/` (this family's PORTAL-BUCKET share is 49financial only --
Inflection and Cottonwood are the separate firm-bucket grant, AC12).

| table (`platinum/advi/49financial/...`) | newest |
|---|---|
| `clients-tab-slim.json`, `cumulative_chart.json`, `leaderboard.json`, `mix_summary.json`, `ownership_map.json`, `partner_analytics_annual.json`, `partner_analytics_quarterly.json`, `timeseries_chart.json`, `timeseries_chart_full.json`, `timeseries_overview.json` (10 tables, 2026-08-21T15:03-15:04Z) + `perfrp_book_advisor.json`, `perfrp_gainloss_account.json`, `perfrp_gainloss_relationship.json`, `perfrp_performance_account.json` (4 tables, 2026-09-01T03:16-07:27Z, the `perfrp_*` refresh) + `_manifests/` (5 objects, newest 2026-09-01T11:06:00Z) |

### Family 4 -- `json/*` in `opal-data-portal-v2` (market and macro)

Total: **954 objects, 897,995,913 bytes**, newest `2026-09-20T23:31:28Z` (`macro/` category). Grouped by top-level
category (the "table" grain for this family):

| category | n | bytes | newest | in/out of this cell's proposed scope |
|---|---:|---:|---|---|
| `benchmarks/` | 6 | 1,043,064 | 2026-09-19T11:06:19Z | IN |
| `capital-markets/` | 2 | 10,138 | 2026-03-11T00:45:53Z | IN |
| `correlations/` | 1 | 152,674 | 2026-09-19T11:06:18Z | IN |
| `factor-tilts/` | 3 | 4,086,091 | 2026-09-19T11:06:20Z | IN |
| `latest/` | 6 | 3,545 | 2026-09-19T11:07:42Z | IN (pipeline-freshness manifest, not a question-answering table itself -- AC5/AC6) |
| `macro/` | 84 | 2,587,440 | 2026-09-20T23:31:28Z | IN |
| `market/` | 3 | 774,220 | 2026-09-19T11:07:41Z | IN |
| `market-overview/` | 1 | 107,839 | 2026-01-13T17:06:03Z | OUT -- `trending-topics.json`, named out-of-scope by `docs/architecture/YALP_MACROS.md:24` precedent (news/trending, not market/macro data) |
| `model_portfolios/` | 25 | 128,283,594 | 2026-06-01T14:16:37Z | OUT -- stale (last write 2026-06-01, 111 days behind `platinum/mdpf`'s 2026-09-20); superseded duplicate of the mdpf family, not this family's live table |
| `peers/` | 1 | 8,506 | 2026-09-04T15:51:22Z | IN |
| `portfolios/` | 5 | 313,947 | 2026-07-27T15:10:07Z | OUT -- stale duplicate of `platinum/mdpf` (`account-distribution.json`, `aum-metrics.json` also live there, fresher) |
| `positioning/` | 4 | 398,930 | 2026-09-19T11:06:23Z | OUT -- this is Models-mode equity positioning (`model.json`, `allocation_summary.json`, `holdings_attribution_data.json`), a different property (per `data/etfs/scripts/gold/etf_positioning_publisher.py:15-18`, ETFS-TO1-AC7: "NOTHING here writes under .../json/positioning/*... Models mode reads exactly the bytes it reads today"); not ETF positioning and not named in this project's S8 property list |
| `returns/` | 1 | 14,578 | 2025-12-23T23:40:00Z | OUT -- stale (269 days); superseded by `benchmarks/etf_returns.json` (2026-09-19, fresher, same content class) |
| `security_scanner/` | 82 | 754,259,410 | 2026-08-07T21:59:40Z | OUT -- a different data domain entirely (security/document scanning), not investment data; no PRD outcome names it |
| `semantic-trending/` | 1 | 30,603 | 2026-02-24T14:20:44Z | OUT -- trending/news, same exclusion as `market-overview/` |
| `sentiment/` | 722 | 3,373,929 | 2026-09-20T21:30:42Z | OUT -- news/sentiment data, not named by any FWD outcome or S1-S11 surface |
| `trending/` | 1 | 126,047 | 2026-09-20T21:21:49Z | OUT -- same exclusion |
| `valuation/` | 2 | 2,336,493 | 2026-09-19T11:06:59Z | IN |
| `valuations/` | 2 | 84,431 | 2025-12-26T18:56:56Z | OUT -- stale (269 days) superseded duplicate of `valuation/` (fresher, singular/plural near-duplicate keys) |
| `yang/`, `yang-pipeline-metadata.json` | 2 | 434 | 2026-09-19T11:04:11Z | OUT -- pipeline bookkeeping, not a served business table |

**IN-scope tables for this family: 9 of 20 categories** (`benchmarks`, `capital-markets`, `correlations`,
`factor-tilts`, `latest`, `macro`, `market`, `peers`, `valuation`). 11 of 20 EXCLUDED, each with its reason on its
own row (AC8).

### Family 5 (separate grant, AC12) -- advisor intelligence, Inflection and Cottonwood

Read via the LEGACY firm buckets `opal-data-inf` and `opal-data-cot` (see AC12 for why these, not the LGIC-named
`opal-data-inflection`/`opal-data-cottonwood`, are the live target).

`opal-data-inf` `platinum/` total: **8,681 objects, 33,579,639 bytes**. Non-`_meta`/`_rollback`/`_quarantine`/
`_rebuild` firm-level tables under `platinum/firm/`: **28 tables** (see AC12 table), newest `2026-09-20T12:14:32Z`.

`opal-data-cot` `platinum/firm/` (excluding the same excluded classes): **12 tables, 1,647,921 bytes**, newest
`2026-09-20T11:35:28Z`.

`VERDICT: PASS-MXA1-AC1`

---

## AC2 -- grain, freshness field, latest value per table, source printed

**mdpf family** -- freshness-field mapping is CODE, `data/mdpf/scripts/gold/mdpf_gold_consolidator.py:246-253`
(printed at that range, `TYPE_AS_OF_FIELD` dict):
```
"aggregate-aua-timeseries": "as_of_last",
"aum-metrics": "period",
"account-distribution": "period",
"category-views": "as_of",
```
Grain: per-scope (firm or `global`) snapshot; `aggregate-aua-timeseries` is a per-date SPINE (one row per trading
day), the other three are LATEST-snapshot objects. Latest value MEASURED from the served object (get-object,
`platinum/mdpf/global/aum-metrics.json`): `period = "2026-09-15"`, `last_updated = "2026-09-16T13:31:12.576095+00:00"`,
`scope = "global"`. `platinum/mdpf/global/category-views.json`: `as_of = "2026-09-15"`. Grain source for
`account-distribution`: `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py:13-18` (printed) -- "the served
'account' is the ALLOCATION ... Per-allocation AUM = fact_allocation_valuation.equity". `non-model-assets.json`
(global only): grain/derivation `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:1-20` (printed): derived
`enterprise_total - model_aum`, 2-term, per Andrew-direct 2026-07-21 quoted in the docstring.

**etfs family** -- freshness field MEASURED from the object itself (get-object,
`platinum/etfs/positioning_data.json`): top-level `generated_at = "2026-09-20T13:01:23Z"`, `data_as_of =
"2026-09-18"`, `data_date = "2026-09-18"`. Grain: ONE object, `portfolios` is a dict keyed by 4 fund tickers (`DIVZ`,
`IDVZ`, `PFDE`, `PFOE`); each fund sub-object carries its OWN `data_as_of`, `as_of_basis`, `prior_date`,
`holdings_status`, `num_holdings`, `aum`. Producer: `data/etfs/scripts/gold/etf_positioning_publisher.py:7-9`
(printed) -- "URL: /api/general/etfs/positioning_data.json ... S3: s3://opal-data-portal-v2/platinum/etfs/
positioning_data.json ... ONE artifact carrying all four books".

**advi family (49financial, portal bucket)** -- freshness field MEASURED from the object (get-object,
`platinum/advi/49financial/leaderboard.json`): `generated_at = "2026-08-21T15:03:22Z"`, `data_as_of = "2026-08-20"`.
Grain: per-firm, windowed (the object carries `available_windows`/`windows`, i.e. multiple lookback windows in one
object, not per-date partitions).

**advi family (Inflection, firm bucket)** -- freshness field MEASURED (get-object, `opal-data-inf`
`platinum/firm/leaderboard.json`): `generated_at = "2026-09-05T12:47:13Z"`, `data_as_of = "2026-09-05"`. Same field
names as the 49financial table -- the shape is shared across firm scopes even though the bucket differs (AC3).

**json/* family** -- freshness field MEASURED per object; no single mapping (unlike mdpf's code dict, this family has
no consolidator). `json/macro/macro_data.json`: `data_as_of = "2026-09-18"`, `year = 2026`. `json/capital-
markets/assumptions.json`: `data_as_of` field present (get-object; content not fully parsed here -- field name
confirmed). `json/latest/manifest.json` is itself a cross-source freshness index (get-object, printed): 5 sources
(`attribution_excel` `data_as_of=2026-08-31`, `cma_excel` `data_as_of=2026-12-31` -- NOTE: a future-dated CMA
horizon date, not a staleness defect, since CMA assumptions are forward 10-year capital-market assumptions dated to
a forward period-end, not a "latest observed" date; the PORTAL page context is `docs/architecture/YALP_CMASMP.md`,
not re-read line-by-line here), `data_pkl`/`model_pkl` `data_as_of=2026-09-18`, `peer_excel` `data_as_of=2026-08-31`.
Grain: whole-object per category (not per-firm; this family is firm-agnostic, AC3).

Source citations are printed per field above; every citation is either a get-object content read (this run) or a
repository line-range printed at this worktree's HEAD.

`VERDICT: PASS-MXA1-AC2`

---

## AC3 -- firm/master scope rule per table, key-prefix segment named; tables whose scope cannot be read from the key

**mdpf**: scope carried by the 2nd key segment after `platinum/mdpf/` -- one of `49financial`, `cottonwood`,
`global`, `inflection` (MEASURED, AC1 census). `global` is the enterprise-level aggregate (`data/mdpf/scripts/gold/
dim_mdpf_aum_metrics.py:1-4`: "off the serve-real GLOBAL aggregate spine"), never a literal sum of the three firm
scopes for every field -- see AC4.

**etfs**: `positioning_data.json`'s S3 key carries NO scope segment at all (there is exactly one key,
`platinum/etfs/positioning_data.json`, for all four funds). **This table's scope (fund: DIVZ/IDVZ/PFDE/PFOE) cannot
be read from its key -- it is a field inside the object (`portfolios.{TICKER}.code`), not a prefix segment.** Named
per this criterion's own requirement.

**advi (49financial, portal bucket)**: scope carried by the 3rd key segment, always `49financial` (one firm only in
this bucket).

**advi (Inflection / Cottonwood, firm buckets, AC12)**: the key itself (`platinum/firm/...`) is IDENTICAL in both
buckets -- **the scope is carried by the BUCKET NAME (`opal-data-inf` vs `opal-data-cot`), not by any key segment.**
Named per this criterion's own requirement (a second table whose scope is not in its key).

**json/\* (market and macro)**: these tables carry NO firm or master scope at all -- they are firm-agnostic market
data (macro indicators, capital-market assumptions, benchmarks, correlations, factor tilts apply identically to
every firm). Stated as such rather than searched for a rule that does not exist (PRD C4 still binds: never render a
firm's number for another firm, which for this family is vacuous since there is no firm axis to confuse).

`VERDICT: PASS-MXA1-AC3`

---

## AC4 -- never-sum rules, each with its reason

1. **mdpf, cross-master**: `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:23-24` (printed): "Basis:
   SCHWAB-RPS (Andrew-ruled; account 08242234). NEVER 0833, NEVER a sum, NEVER blended-preferred." Reason:
   08242234 and 08335338 are two distinct Schwab masters; summing or blending would misstate either.
2. **mdpf, cross-basis (non-additive)**: `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:26-29` (printed):
   "NEVER set non_model_aum := base GLOBAL non_model_aua[] (... firm-summed custody-basis). That is a
   DIFFERENT-BASIS quantity". Reason: the enterprise-basis residual and the custody-basis firm-summed figure are
   two different quantities that happen to look alike; summing/substituting one for the other misstates by the
   basis gap (the docstring measures it: ~$64.48M for one date).
3. **mdpf, cross-date (non-additive)**: `aum-metrics.json`'s `total.q0..q3` and `dates.q0..q3` are quarter-END
   SNAPSHOTS (stock, not flow) -- summing across quarters, or across `by_model` entries beyond what the object's own
   `total.account_count` already resolves as a frontier sum (`mdpf_gold_consolidator.py` frontier language, cited
   AC2), double-counts or misdates.
4. **etfs, cross-fund**: AUM/NAV/holdings are per-fund legal entities (`positioning_data.json`'s `portfolios` dict,
   AC2). Summing two funds' AUM or NAV is meaningless (C4: never sum across masters or firms, extended here to
   funds -- the PRD's phrasing "masters or firms" and the FWD-5 ACCEPT's "never a fund summed with another" are the
   same rule at this property's grain).
5. **advi, cross-firm**: 49financial's `leaderboard.json`/`partner_analytics_*.json` are a separate book from
   Inflection's and Cottonwood's (separate buckets, AC3) -- summing advisor books across firms mixes three
   unrelated client populations.
6. **advi, cross-period (non-additive)**: `partner_analytics_annual.json`, `_quarterly.json` and `_monthly.json` are
   three DIFFERENT aggregation windows over the same underlying activity (MEASURED: all three exist per firm,
   AC1) -- summing annual + quarterly + monthly triple-counts the same activity at different granularities.
7. **json/\* macro, cross-date (non-additive)**: `macro/timeseries/{slug}.json` series (yields, CPI, etc.) are point-
   in-time levels -- reasoning from `docs/architecture/YALP_MACROS.md:19-21` (printed), which names the UST
   tenors and "2Y-10Y spread" as the only stated TRANSFORM of the raw series, not a claim the doc states a
   never-sum rule verbatim. Summing a yield curve tenor's history is not a meaningful operation; only the current
   observation or a stated transform (spread) is valid.

`VERDICT: PASS-MXA1-AC4`

---

## AC5 -- common questions, numbered, table + fields, source stated

Source discipline: every question below is sourced from (a) the producer code's own stated FE contract/consumer
comment, (b) the `docs/architecture/YALP_*.md` portal-page briefs, or (c) this seat's reasoning from the object's
own field shape. **None is presented as measured user demand** -- the PRD's own evidence boundary (line 90) says the
per-property common questions are not enumerated anywhere yet, and this cell does not claim otherwise; PART III's
beta bar (S8) is what will measure real demand in round 2.

| # | question | table(s) | fields | source |
|---|---|---|---|---|
| 1 | What is total AUM (enterprise, model, non-model) as of the latest quarter, for a firm or the enterprise? | `aum-metrics.json` | `total.aum`, `total.model_aum`, `total.non_model_aum`, `period` | producer contract: `dim_mdpf_aum_metrics.py:9-12` names 4 FE consumers (`ModelPortfolios.tsx:425`, `FactorTilts.tsx:83`, `Attribution/SelectionTab.tsx:89`, `Positioning/HoldingsTab.tsx:564`) |
| 2 | How is AUM distributed across account-size buckets for a firm? | `account-distribution.json` | the bell-curve/percentile block, `period` | producer contract: `dim_mdpf_account_distribution.py:6-7` (FE `getAccountDistributionByFirm`) |
| 3 | What is the AUA/AUM trend over time for a firm or model? | `aggregate-aua-timeseries.json` | `model_aua[]`, `by_model[].model_value[]`, `partner_custody_total[]`, `as_of_last` | producer contract: `dim_mdpf_aggregate_aua_timeseries.py:4-6` (audit-brief L21-22 / CVO F4 FE contract) |
| 4 | What model categories exist and what is their current breakdown for a firm? | `category-views.json` | the category tree, `as_of` | reasoning from the object's own shape (`nodes`, `scope`, `sums`, AC2) plus `mdpf_gold_consolidator.py:587` "the category-views block for ONE FIRM" |
| 5 | What is the enterprise's non-model AUM today? | `non-model-assets.json` (global only) | `enterprise_total`, `model_aum`, `non_model_aum`, `non_model_pct` | producer contract: `dim_mdpf_non_model_assets.py:1-4` ("Emits the served-shape non_model_assets.json ... A4 ... /model-portfolios 'Non-Model' bar") |
| 6 | What are the current holdings and AUM for one Opal ETF? | `positioning_data.json` | `portfolios.{TICKER}.holdings`, `.aum`, `.data_as_of` | producer contract: `etf_positioning_publisher.py:7-9` |
| 7 | What is a fund's net asset value / as-of date, and how stale is it? | `positioning_data.json` | `portfolios.{TICKER}.data_as_of`, `.as_of_basis`, `.prior_date`, `.holdings_status` | same object; `holdings_status` names staleness explicitly (reasoning from field name) |
| 8 | Who are the top advisors/producers by AUM or new-net-assets for a firm? | `leaderboard.json` | the ranked list, `data_as_of` | reasoning: file name + FE-facing shape (`windows`, `available_windows`) |
| 9 | What is the client/book mix for a firm (by model, by tax status, etc.)? | `mix_summary.json` | its summary block | reasoning from file name (no producer docstring read for this file at this cell) |
| 10 | What is partner/advisor performance for a firm, annually/quarterly/monthly? | `partner_analytics_annual.json`, `_quarterly.json`, `_monthly.json` (Inflection/Cottonwood; 49financial carries annual+quarterly only, AC1) | period-keyed analytics blocks | reasoning from file-name family + AC1's census (49financial has no `_monthly` object; Inflection/Cottonwood do) |
| 11 | What is a firm's cumulative growth / AUM trend over time? | `cumulative_chart.json`, `timeseries_chart.json`, `timeseries_overview.json` | chart series, `as_of`/`generated_at` | reasoning from file-name family, parity with mdpf's `aggregate-aua-timeseries` question shape |
| 12 | What are current benchmark returns (model portfolios, ETFs)? | `benchmarks/benchmark_returns.json`, `benchmarks/etf_returns.json`, `benchmarks/model_portfolio_benchmarks.json` | return series | reasoning from file names; `json/latest/manifest.json` confirms these are pipeline-produced, freshness-tracked artifacts |
| 13 | What are the firm's current capital-market assumptions (forward 10-year)? | `capital-markets/assumptions.json`, `capital-markets/views.json` | `assumptions`, `data_as_of` | portal-page brief `docs/architecture/YALP_CMASMP.md:12` ("Portal page: `portal/src/pages/CapitalMarketAssumptions/`") |
| 14 | What is a named macro indicator's current value and history (e.g. 10Y yield, CPI, unemployment)? | `macro/macro_data.json`, `macro/timeseries/{slug}.json` | indicator value, `data_as_of`, history series | portal-page brief `docs/architecture/YALP_MACROS.md:16-21` (Macroeconomics page, YieldCurveTab/MacroHeatmap/MacroTimeSeriesModal) |
| 15 | What is the pairwise correlation between two asset classes? | `correlations/correlation_data.json` | the correlation grid | portal-page brief `docs/architecture/YALP_CORREL.md:13` |
| 16 | What is the current factor-tilt positioning (spreads, snapshot, time series)? | `factor-tilts/tier1-snapshot.json`, `tier2-spreads.json`, `tier3-timeseries.json` | tier-specific series | portal-page brief `docs/architecture/YALP_FACTOR.md:15` |
| 17 | What is the current market regime / valuation read? | `market/market-regime.json`, `valuation/valuation_data.json`, `valuation/risk_premium_data.json` | regime label/history, valuation series | reasoning from file names; `market/market-regime-history.json` is the paired history object |
| 18 | What is peer-group performance? | `peers/peer_performance.json` | performance block | reasoning from file name |

`VERDICT: PASS-MXA1-AC5`

---

## AC6 -- question -> tool or typed query, with reason

**Assigned to a proposed purpose-built tool (Q1-Q13, Q17-Q18):** every table that is a SMALL, NAMED, whole-object
precomputed key the portal itself reads (mdpf's 4+1 tables, the one etfs object, the advi tables including the
firm-bucket pair, capital-markets, benchmarks, market/valuation/peers) gets a purpose-built reader. **Reason:** C5
requires the tool to read the SAME precomputed table the portal reads, for an exact side-by-side parity check
(FWD-2's ACCEPT); a whole-object GET is what a purpose-built tool does cheaply and verifiably, and there is no
filter/group-by/aggregate need for a single small precomputed object -- a typed query would add generality nothing
here uses.

**Assigned to the typed query (Q14's history half, Q15, Q16):** `macro/timeseries/{slug}.json` is a PARAMETRIC
family (MEASURED: 84 objects under `macro/`, the great majority per-indicator timeseries files, not one fixed set of
named keys -- AC1). **Reason:** a purpose-built tool per indicator would multiply the tool count by the indicator
count (dozens; C2's pinned-count-movement rule would have to move on every new FRED/BLS series Yang adds), while
the typed query's filter/date-range shape over ONE catalogued "macro timeseries" dataset serves "give me indicator X
between two dates" without a new tool per series. `correlations/correlation_data.json` (Q15) and the `factor-tilts`
tier files (Q16) are likewise routed to the typed query rather than a named tool -- see AC7's finding: no
`systems.json` key exists for this data domain, so C3 cannot mint a name for them without a new registry row this
cell is not mandated to add. `macro/macro_data.json` (Q14's "current value" half) stays a purpose-built tool since it
is one fixed key.

No question is left to the typed query WITHOUT the reason stated above (JUDGMENT AC10 grades whether that
assignment is itself well-judged; this criterion is mechanical -- that every question HAS a stated assignment).

`VERDICT: PASS-MXA1-AC6`

---

## AC7 -- proposed tool names pass C3

C3 (PRD, printed): `{system}_{function}[_{qualifier}]`; `system` a key of `infra/logic/registry/systems.json`;
`function` a base-form verb; scope is an explicit ARGUMENT, never folded into the name. `systems.json` MEASURED
(this run): 25 keys including `mdpf`, `etfs`, `advi` (all three needed here are present; denominator 25, printed).
Existing pattern confirmed by reading, never editing, the Schwab integration (bound 8): `infra/aws/ec2/opal-gateway/
app/integrations/schwab/integration.py:985-1020` registers `schwab_get_access`, `schwab_list_files`,
`schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download` -- same shape, confirming the reading.

**Finding, named per bound 9's refusal discipline (not a violation of THIS criterion, since these are simply not
proposed as named tools):** `benchmarks`, `capital-markets`, `correlations`, `factor-tilts`, `market`, `valuation`,
`peers` are NOT among the 25 `systems.json` keys, and none of `mdpf`/`etfs`/`advi` is the right domain for
market-wide, firm-agnostic data. **This cell REFUSES to invent a tool name for those tables under a system key that
does not exist** (bound 3: a builder/registry refusal is a registry row, never a typed path; minting a new
`systems.json` row is not this cell's mandate). The reserved `opal` system is named by C3 specifically for
"cross-property discover tools", not for a market-data domain, so folding these under `opal` would be a stretch of
that carve-out rather than a clean fit -- this cell does not take that route either. **All such questions are
therefore routed to the typed query instead of a named tool (AC6), and a fresh registry row (a future `MX-c-4`-class
decision, not this cell's) is what would let a future round name them.**

**Proposed tool set (10 tools, all system keys present in the 25-key census, scope always a function argument, never
folded into the name):**

| tool name | serves | system in systems.json? | function (verb) |
|---|---|---|---|
| `mdpf_get_aum_metrics(scope)` | Q1 | yes | get |
| `mdpf_get_account_distribution(scope)` | Q2 | yes | get |
| `mdpf_get_aggregate_aua(scope)` | Q3 | yes | get |
| `mdpf_get_category_views(scope)` | Q4 | yes | get |
| `mdpf_get_non_model_assets()` | Q5 | yes | get |
| `etfs_get_positioning(fund)` | Q6, Q7 | yes | get |
| `advi_get_leaderboard(scope)` | Q8 | yes | get |
| `advi_get_mix_summary(scope)` | Q9 | yes | get |
| `advi_get_partner_analytics(scope, period)` | Q10 | yes | get |
| `advi_get_growth_chart(scope, chart)` | Q11 | yes | get |

Every name matches `^[a-z][a-z0-9]*(_[a-z][a-z0-9]*)+$` with its first segment one of the 25 `systems.json` keys and
its second segment a base-form verb (`get`), scope never folded in. Q12, Q13, Q17, Q18 (benchmarks, CMA, market
regime/valuation, peers) have NO proposed tool name for the reason stated above and are typed-query only, alongside
Q14's history half, Q15 and Q16. Mechanically checked by the probe (regex + systems.json membership).

`VERDICT: PASS-MXA1-AC7`

---

## AC8 -- read fence as exact prefixes; exclusions named

**Portal bucket `opal-data-portal-v2`** (proposed fence, one prefix per family):
- `platinum/mdpf/*` -- IN, minus `platinum/mdpf/archive/*` (EXCLUDED: 444 historical dated snapshots, not needed by
  the current-state tools proposed here; a future history tool would read it) and `platinum/mdpf/_manifests/*`
  (EXCLUDED: pipeline bookkeeping, not a business answer table).
- `platinum/etfs/positioning_data.json` -- IN (the single object). `platinum/etfs/_manifests/*` EXCLUDED (same
  reason).
- `platinum/advi/49financial/*` -- IN, minus `_manifests/*` (EXCLUDED, same reason).
- `json/benchmarks/*`, `json/capital-markets/*`, `json/correlations/*`, `json/factor-tilts/*`, `json/latest/*`,
  `json/macro/*`, `json/market/*`, `json/peers/*`, `json/valuation/*` -- IN (readable by the typed query where no
  tool is named, AC6/AC7). Everything else under `json/*` is EXCLUDED with its reason (AC1's per-category table:
  `market-overview`, `model_portfolios`, `portfolios`, `positioning`, `returns`, `security_scanner`,
  `semantic-trending`, `sentiment`, `trending`, `valuations`, `yang*` -- 11 categories, most of the family's byte
  mass being `security_scanner` (754MB) and `model_portfolios` (128MB), neither of which any FWD outcome names).

**Firm buckets (separate grant, AC12; NOT part of this fence):**
- `opal-data-inf` `platinum/firm/*` -- IN, minus `_meta/*`, `_rollback/*`, `_quarantine_scope_bug_20260424/*`
  (EXCLUDED: backup/superseded copies, named at AC1) and `platinum/clients/*`, `platinum/advisors/*`,
  `platinum/_rebuild/*` (EXCLUDED: finer-grain per-client/per-advisor data and a bulk rebuild snapshot, out of this
  round's firm-level common-question set; a future cell can add a narrower per-advisor/per-client grant).
- `opal-data-cot` `platinum/firm/*` -- IN, minus the same excluded classes (MEASURED: cottonwood's listing already
  excludes them by construction, AC1).

`VERDICT: PASS-MXA1-AC8`

---

## AC9 -- a property with no data says so and proposes no tool

MEASURED (AC1): every one of the four surface families has live data at this cell's run time (530 / 43 / 19 / 954
objects respectively), and both advisor-intelligence firm buckets have live data (8,681 and non-empty `platinum/
firm/` respectively). **No sub-table checked in this analysis was found empty.** This criterion is therefore
satisfied VACUOUSLY for `MX-a-1` as a whole: there is no empty property here to name, and this cell proposes no
tool for zero properties (it excludes 11 of 20 `json/*` categories on OTHER grounds -- staleness, wrong domain,
duplication -- named individually at AC1/AC8, never on "no data", since every excluded category DOES have objects).

`VERDICT: PASS-MXA1-AC9`

---

## AC10 -- JUDGMENT

Graded by `3.0.0_SA_CVO` at L9. Record UNVERIFIABLE-BY-INSTRUMENT; status_reason: "graded by 3.0.0_SA_CVO at L9,
per this order's own text". No verdict recorded here.

---

## AC11 -- four surface families = denominator; portal page + precomputed key per surface

**Denominator: 4** (C5, A2 -- `platinum/mdpf`, `platinum/etfs`, `platinum/advi`, `json/*`). MEASURED count of surface
families named in C5's own text: 4 (printed, PRD line 244: "`platinum/mdpf`, `platinum/etfs`, `platinum/advi` and
`json/*`").

| # | surface family | portal page (MEASURED citation) | example precomputed key it reads |
|---|---|---|---|
| 1 | `platinum/mdpf/*` -- model AUM and account distribution | `ModelPortfolios.tsx` (+ `FactorTilts.tsx`, `Attribution/SelectionTab.tsx`, `Positioning/HoldingsTab.tsx` as secondary consumers) -- `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py:9-12`, printed | `platinum/mdpf/global/aum-metrics.json` |
| 2 | `platinum/etfs/*` -- ETF positioning | the ETF Positioning surface ("Models mode"), API `/api/general/etfs/positioning_data.json` -- `data/etfs/scripts/gold/etf_positioning_publisher.py:7-9`, printed | `platinum/etfs/positioning_data.json` |
| 3 | `json/*` -- market and macro (spans several portal pages, MEASURED, not one page): `Macroeconomics` (`portal/src/pages/Macroeconomics/`, `docs/architecture/YALP_MACROS.md:16`), `CapitalMarketAssumptions` (`docs/architecture/YALP_CMASMP.md:12`), `Correlation` (`docs/architecture/YALP_CORREL.md:13`), `FactorTilts` (`docs/architecture/YALP_FACTOR.md:15`), `MarketPerformance`/"Market Overview" (`docs/architecture/YALP_MKTOVR.md:15`) | `json/macro/macro_data.json`; `json/capital-markets/assumptions.json`; `json/correlations/correlation_data.json`; `json/factor-tilts/tier1-snapshot.json`; `json/market/market-regime.json` |
| 4 | `platinum/advi/*` (49financial) + firm buckets (Inflection/Cottonwood) -- advisor intelligence | the Advisor Intelligence / Book of Business surface (page path not confirmed by this cell -- `portal/` is not checked out in this worktree, per this worktree's grant; named by the FE contract comments in the producer scripts as `platinum/firm/*` consumers, no `.tsx` citation available) | `platinum/advi/49financial/leaderboard.json`; `opal-data-inf` `platinum/firm/leaderboard.json`; `opal-data-cot` `platinum/firm/leaderboard.json` |

Note on surface 4's page name: `portal/` is a gitlink submodule and is EMPTY in this worker's worktree (measured:
`ls portal` returns nothing; `git submodule status portal` returns "no submodule mapping"). This cell cannot print a
`.tsx` byte range for the Advisor Intelligence page the way it did for surfaces 1-3, whose page names came from
CITATIONS INSIDE THE (checked-out) data-pipeline scripts, not from the frontend tree itself. This is disclosed
rather than guessed (bound 9).

`VERDICT: PASS-MXA1-AC11`

---

## AC12 -- advisor-intelligence firm buckets and prefixes, listed separately from `opal-data-portal-v2`

**Bucket names, MEASURED** (`s3api list-buckets`, filtered): both an LGIC-named pair and a legacy pair exist:
`opal-data-inflection`, `opal-data-cottonwood` (LGIC; `bucket_provisioned: true`, `bucket_managed_by:
"s3-lgic-firm-buckets.tf"` per `infra/logic/registry/scopes.json`, printed) and `opal-data-inf`, `opal-data-cot`
(legacy; same registry file's `aliases` block, printed: `"opal-data-inf" ... routed: true ... the deployed router's
target (firm-config.mjs FIRM_CONFIG)`).

**Which one is live, MEASURED, not assumed:** `s3api list-objects-v2 --bucket opal-data-inflection` and
`--bucket opal-data-cottonwood` both returned `AccessDenied ... explicit deny in a resource-based policy` for this
run's identity (`arn:aws:iam::313476888478:user/Andrew_Berman`) -- consistent with `comp-iam`'s L5 battery finding
of a cross-firm bucket Deny belt this instrument is blind to (decomp s.7). `opal-data-inf` and `opal-data-cot`
returned live listings (8,681 and non-empty objects respectively) with the SAME identity -- so read access itself
does not distinguish "populated" from "denied", but the registry's own alias text does: it names `opal-data-inf` as
"the deployed router's target" and states (at the vintage that alias entry was written) that `opal-data-inflection`
"does not exist yet" as a write target, even though the bucket is now provisioned. **This cell's measured
conclusion: the ACTIVE, served advisor-intelligence data for Inflection and Cottonwood lives in the LEGACY buckets
`opal-data-inf` / `opal-data-cot` today; the LGIC-named buckets are provisioned but this cell could not read their
contents and the registry's own text says they are not the routed target.** This is DESIRED-not-APPLIED for the
LGIC buckets and MEASURED for the legacy ones (Rule 22 STATE axis).

**Prefixes, separate from `opal-data-portal-v2` (which carries none of this data -- confirmed by AC1's family-3
census, `platinum/advi/*` in the portal bucket is 49financial only):**

| bucket | prefix | tables (non-`_meta`/`_rollback`/`_quarantine`/`_rebuild`) | newest |
|---|---|---|---|
| `opal-data-inf` | `platinum/firm/` | `activity_scan.json`, `activity_scan_{1y,max,qtd,ytd}.json`, `advisor_nna_canonical.json`, `cash_drag.json`, `cash_drag_{1y,max,qtd,ytd}.json`, `client_directory.json`, `clients-tab-slim.json`, `clients_tab.json`, `concentration_risk.json`, `cumulative_chart.json`, `dashboard.json`, `fee_efficiency.json`, `filters/dimensions.json`, `firm_composition.json`, `firm_concentrations.json`, `header_metrics.json`, `header_metrics_fresh.json`, `leaderboard.json`, `mix_summary.json`, `nmec_nmnc_nna.json`, `partner_analytics.json`, `partner_analytics_{annual,monthly,quarterly}.json`, `snapshots/aua_by_{architect,region,state,tax_status}.json`, `timeseries_chart.json`, `timeseries_overview.json`, `top_holdings.json` (28 tables) | 2026-09-20T12:14:32Z |
| `opal-data-cot` | `platinum/firm/` | `client_directory.json`, `clients-tab-slim.json`, `cumulative_chart.json`, `dashboard.json`, `header_metrics.json`, `leaderboard.json`, `mix_summary.json`, `partner_analytics_{annual,monthly,quarterly}.json`, `timeseries_chart.json`, `timeseries_overview.json` (12 tables) | 2026-09-20T11:35:28Z |

`opal-data-inf` also carries `platinum/clients/{id}.json` (4,171 objects) and `platinum/advisors/{name}.json` (32
objects) -- per-client and per-advisor granularity. **No client name, id, or content from these is reproduced in
this deliverable** (bound 2); they are named only by their prefix and count, and are EXCLUDED from this round's
proposed fence (AC8) rather than opened.

`VERDICT: PASS-MXA1-AC12`
