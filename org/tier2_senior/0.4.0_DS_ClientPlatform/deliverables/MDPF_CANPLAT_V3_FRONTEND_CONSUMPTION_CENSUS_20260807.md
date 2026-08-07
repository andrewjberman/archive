# MDPF_CANPLAT.V3 — frontend consumption census (V9/V10/V11)

**TO:** `MDPF_CANPLAT.V3.frontend-consumption-census` (GO 2.0.0_SA_COO~Z 010058Z)
**Author:** `0.4.0_DS_ClientPlatform~Z` · 2026-08-07 ~0110Z
**Measured against:** `portal/` LOCAL clone @DEV `604101df`, clean tree, READ-ONLY (Rule 19 held; no lingering CWD)
**Prior evidence adopted by citation:** CTO~Z 010334Z (endpoint-layer anchor + basis@global zero-read) · MSTR~Z 005808Z (proxy-level facts)

> §0 held: measures only, verdicts not patches. **HEADLINE: ZERO BREAKS VERDICTS.**
> Every added or newly-nullable §B field is SAFE or NO-CONSUMER at @604101df.
> No SURPRISE lines were warranted — nothing surprising was found and nothing was acted on.

---

## V9 — census, denominator printed

**Denominator: 403 src files** (`git -C portal ls-files src/**` = 403, the TO's stated
baseline). Sweeps ran over the full `portal/src` scope via comp-grep (rail);
**comp-cache captured 102 of 102 useQuery call-sites, 0 unparseable** — 5 carry mdpf keys,
ALL in `ModelPortfolios.tsx`. comp-transform/comp-glob resolved on-device as promised.

**The shape-changer layer (CTO~Z anchor, adopted + verified by citation):** artifact reads
happen in the ENDPOINT layer, not the page —

| artifact type | fetcher | scopes | URL → served key |
|---|---|---|---|
| account-distribution | `aum.ts:531 getAccountDistributionByFirm` | ALL FOUR incl. global (`:490-491`: legacy read DEAD) | `/api/general/mdpf/{scope}/account-distribution.json` → `platinum/mdpf/{scope}/…` (deployed router v6, F4 @b48634789a, `:501-507`) |
| aum-metrics | `aum.ts:611 getAUMMetricsByFirm` | ALL FOUR | `/api/general/mdpf/{scope}/aum-metrics.json` → platinum |
| aggregate-aua-timeseries | `portal-proxy.ts:525 getMdpfAggregateAUATimeSeriesByFirm` | per-firm + global (`ModelPortfolios.tsx:379,:392`) | `/api/general/mdpf/{scope}/aggregate-aua-timeseries.json` → platinum |

The frontend already reads exactly the 12 canonical scoped paths. Every fetcher returns
null-on-error (graceful degrade).

**Component layer (who consumes what the fetchers return):**
- `ModelPortfolios.tsx` — the ONLY page with mdpf queries (5/5).
- `AccountDistributionChart.tsx` + `AccountDistributionMetrics.tsx` — bell renderers;
  **named-field readers only** (`:28-:89` histogram/percentiles/median; `:27-:82`
  account_count/percentiles/median).
- `lib/pairedProvenanceRead.ts` — "the ONLY legal reader of the raw value arrays"
  (`ModelPortfolios.tsx:659`); page imports readModelSeries / readFirmAggregateSeries /
  readNonModelSeries / readGlobalPointClass / readGlobalEnterpriseSeries /
  readGlobalCompleteFrontier (`:40`).
- Legacy family (`json/portfolios/aum-metrics.json`, FROZEN — writer flag-disabled, F1
  @b48634789a): `FactorTilts.tsx:83 getAUMMetrics()`, `SelectionTab.tsx:90` +
  `HoldingsTab.tsx:565 getAUMSummary()`. Untouched by the R-series (D9: `json/*` never moves).

## V10 — per-field verdicts (field → consumer → verdict, cited @604101df)

| §B delta | consumer evidence | verdict |
|---|---|---|
| `basis`/`source` newly NULL @global (dist) | **CTO~Z 010334Z, adopted:** zero `.basis`/`.source` reads in ModelPortfolios (2,463 lines); corroborated: the `AccountDistribution` interface (`aum.ts:164-171`) declares only generated_at/period/total/by_model — undeclared fields are unreachable without casts, and no cast exists | **SAFE** |
| `firm_id`/`firm_name` newly present @global (dist) | same interface bound; zero reads | **NO-CONSUMER** (additive-inert) |
| `meta` + `meta.account_count_by_model_key` newly present @49financial (dist) | zero `.meta` reads on distribution data; page's own record `ModelPortfolios.tsx:516` "no consumer of the legacy-only meta keys exists". (The staged-dist meta IS read by my own GOLD frontier-count loader — a gold-side reader, not portal.) | **NO-CONSUMER** |
| `total.account_units` folded, ALL FOUR (dist) | total consumed by named reads only: `ModelPortfolios.tsx:1155` (.account_count), `:1591` (.excluded_unfunded_count), `:1579` (Chart data), `:1583` spread `{...total}` into Metrics — the spread FORWARDS the new key but both components read named fields only (cited above); nothing iterates `total` keys | **SAFE** (additive-inert) |
| `non_model_assets_detail` on aum-metrics AND timeseries (real@global, null@firms) | 403-file sweep: **0 references** | **NO-CONSUMER** |
| W-1 `account_count_total` + `count_provenance` newly present @cottonwood | sole legal reader `readCountTotalSeries` (`pairedProvenanceRead.ts:396`, guard-enforced `:133`) has **ZERO callers** in portal/src. Forward-safe when a caller arrives: `source_absent` ∈ KNOWN_COUNT_CLASSES (`:220-226`) and is NOT value-bearing (`:75-78` = {band_2firm, frontier_stamp}) → maps to 'absent', the correct render for a null-count date; `measured` is in the VALID render enum | **NO-CONSUMER** (component layer), reader-library COMPATIBLE |
| W-1 `source_vintage_last` newly present @cottonwood | 403-file sweep: 0 reads (matches the spine's own "not FE-consumed" grounding, re-verified at this pin) | **NO-CONSUMER** |
| §B3 `opal_aggregate_aua` @firm scopes (my Δ5 ruling) | firm values flow through `readFirmAggregateSeries` which reads `partner_custody_total?.[i] ?? null` (`:337-350`); `opal_aggregate_aua` is read ONLY by `readGlobalEnterpriseSeries` (`:510+`) on the global series, which is unchanged; the field is already typed optional (`portal-proxy.ts:456`) | **NO-CONSUMER** at firm scope; global read unchanged → SAFE |
| §B3 `point_class` @firm scopes | `readGlobalPointClass` is global-scoped (`:370` "the ONLY correct Global source"); firm-series classes derive from `cohort_provenance` via `provenanceIndex` — the firm `point_class` channel is unread; tolerant enum handling (`:273`) if ever read | **NO-CONSUMER** |
| §B3 `count_basis` / `count_as_of` / `account_count_total_raw` (all scopes) | 403-file sweep: **0 references** to any of the three | **NO-CONSUMER** |
| `partner_custody_total` present-as-NULL @global timeseries (my honest-absence decision) | global flows through `readGlobalEnterpriseSeries`/`readNonModelSeries` (`ModelPortfolios.tsx:713-730`), neither reads custody; even `readFirmAggregateSeries` is null-tolerant (`?? null` → honest-absent points) if ever pointed at global | **SAFE** |

**A NO-CONSUMER verdict carries its denominator:** every "0 references / 0 callers" above
is against the full 403-file `portal/src` sweep at @604101df.

## V11 — legacy bell verdict

- **From source @604101df: ZERO live `json/mdpf/*` readers exist in portal/src.** The only
  occurrences are comments: `aum.ts:549` (recording that a prior json/mdpf claim was
  FALSIFIED on the deployed plane) and `ModelPortfolios.tsx:450` — a **stale comment**
  claiming the per-firm endpoint resolves by `json/mdpf/{firmId}` path; the code beneath it
  calls `getAccountDistributionByFirm`, which hits the mdpf family route → platinum
  (deployed router v6, F4 @b48634789a). Cited as a comment-nit beside MSTR~Z's two known
  nits; not chased, not patched.
- The bell COMPONENTS (Chart/Metrics) therefore consume platinum bodies exclusively in this
  source version. `json/mdpf/*` is untouched by the R-series (D9), so any out-of-source
  consumer of that tree (an older deployed edge version, an external reader — V12's
  question, not V3's) sees byte-identical data regardless.
- **MSTR~Z fact 2 folded + extended to the component layer:** `portal-proxy.ts:410-417
  getNonModelAssets` does target the legacy `json/portfolios/non_model_assets.json` — the
  proxy-level fact is TRUE — and it has **ZERO component callers** (the non-model display
  retired that fetch, `ModelPortfolios.tsx:528`; the Global view field-reads the canonical
  timeseries' `non_model_aua`). The surviving legacy-family consumers are the FROZEN
  `json/portfolios/aum-metrics.json` trio (FactorTilts `:83`, SelectionTab `:90`,
  HoldingsTab `:565`) — stated here for the eventual extras-retirement TO, which should
  treat THAT key (not `non_model_assets.json`) as the legacy family's live read surface.

**VERDICT: LEGACY BELL UNAFFECTED.** No §B-changed field flows to any `json/*` reader.

## Compiler tools used
comp-cache (key mdpf; map denominator 102/102) · comp-grep (all sweeps, portal/src scope,
403 files) · comp-glob (component location) · comp-transform fields (ModelPortfolios —
thin output, superseded by direct citation) · targeted Reads at the cited lines.
