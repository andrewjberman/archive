# THE MDPF FRONTEND FORK PATTERN — INFLECTION AS THE TEMPLATE, COTTONWOOD AS THE COPY

**Andrew-direct 2026-07-22 ~1640Z:** *"scan the projects for the creation of the Inflection MDPF page, and
the structure of the 'Select Partners:' dropdown and firm selection as it pertains to Inflection, and what
is covered underneath those parameters, because that is what we effectively need to model to create the
same fork pattern for Cottonwood on the frontend."*
**And ~1642Z:** *"use comp-cache and check comp-tools list for those which can trace/map typescript
structures and data flow on the Portal surface."*

**Instruments used** (per that direction): `comp-which` → `comp-platinum page --firm` · `comp-cache
key|map` · `comp-types blast|fields` · `comp-cluster` (timed out — recorded unresolved, NOT clean).
**Read-only. Portal tracked tree clean at `08c6d8b2` (DEV).**

---

## 0. THE HEADLINE

**THE FORK IS ALREADY BUILT FOR COTTONWOOD AT LAYERS 1–3. THE GAP IS LAYER 4 AND THE ARTIFACT.**
And the failure mode we are walking into is **the one Inflection already hit, documented in its own project
record**: *"data layer passed but the portal did NOT work for firm-scoped views."*

---

## 1. THE TWO PROJECTS THAT CREATED THIS

| project | Andrew-direct | status | what it did |
|---|---|---|---|
| **`MDPF_SCOPED`** | 2026-05-28 | **complete** (closed 06-03) | Created the fork. *"split Model Portfolios apart by partner using the **EXACT same pattern as Advisor Intelligence** (Select Partner: dropdown upper-right, canonical placement + styling)"* — S1 selector, S3 multi-firm data spine, S4 canonical model naming (30 files). |
| **`MDPF_COTMDL`** | 2026-07-07 | **COMPLETE-AS-SUPERSEDED** (07-21) | *"Add a Cottonwood dropdown view on the Model Portfolios page (matching the existing Global/49F/Inflection pattern)"* — Cohort 3. |

**⚠ `MDPF_COTMDL` WENT ON HOLD ON A FALSE NEGATIVE, AND THE CORRECTION MATTERS.** Its on-hold premise was
*"Portfolio Strategy field 100% 'No Strategy' in silver transactions ⇒ Cottonwood runs NO model program in
BD."* **That was the WRONG SOURCE.** WS-E discovery (07-21) proved Cottonwood has **60 models (17 Opal
in-scope)** living in the **BD Rebalancer app** (`accountRebalStrategyID === Rebalancer model.id`), not in
the sparse silver strategy-field projection the TO checked. *An absence measured on the wrong surface
parked a project for two weeks* — the same instrument class this session keeps finding.

**ONE DESIGN DIFFERENCE FROM ADVI, stated in MDPF_SCOPED itself and load-bearing:**
> *"MDPF default = **Global** the aggregate, **not a firm**, unlike AI which defaults to a firm."*

---

## 2. THE FORK, IN FOUR LAYERS — and where Cottonwood actually stands

### LAYER 1 · THE SELECTOR — ✅ COTTONWOOD ALREADY PRESENT
`ModelPortfolios.tsx:244-249` — a page-local const, **not** a shared registry:
```
const ALL_MDPF_PARTNER_FIRMS = [
  { id: 'global', name: 'Global (All)' }, { id: '49financial', name: '49 Financial' },
  { id: 'inflection', name: 'Inflection Wealth Management' },
  { id: 'cottonwood',  name: 'Cottonwood Capital Advisors' },
] as const satisfies readonly { id: string; name: string }[]
type MdpfFirmId = (typeof ALL_MDPF_PARTNER_FIRMS)[number]['id']
```
Rendered at `:1094` as `PageSurfaceControl as="dropdown"` in the **`PanelHeader` actions slot**, label
**"Select Partner:"**, gated `internal ? … : undefined`.
**`comp-types blast MdpfFirmId` → blast radius = 1 file.** The MDPF fork is **entirely page-local**. That is
the single most useful structural fact here: it is a small, contained fork, not a cross-cutting system.

**⚠ THE ID IS THE ARTIFACT PATH** — the file says so at `:238-243`: the id *"is interpolated straight into
`/api/general/mdpf/{firmId}/aggregate-aua-timeseries.json`… A mismatch here 404s into the queryFn's catch
and renders an **EMPTY partner rather than an error — silent, and indistinguishable from 'no data yet'.**"*

### LAYER 2 · FIRM RESOLUTION — ✅ WORKS FOR COTTONWOOD TODAY (exercised)
`:418-429`
```
const internal = isInternal() || isDev()          // firmId==='opal-capital' || userType==='Dev'
const [selectedFirmId, setSelectedFirmId] = useState<string>('global')
const effectiveFirmId = internal ? selectedFirmId : (claims?.firmId ?? 'global')
```
**Internal users pick from the dropdown; an external partner is pinned to their own `claims.firmId`.**
I exercised this today with a stubbed external Cottonwood advisor session — the page resolved
`effectiveFirmId='cottonwood'`, routed correctly, and rendered Cottonwood chrome and attribution.

### LAYER 3 · THE DATA KEYS — ✅ CODE DONE / ❌ NO ARTIFACT
`comp-cache key mdpf` (**denominator stated by the tool: 104 of 104 `useQuery` call-sites captured, 0
unparseable; `useQueries`/`useInfiniteQuery` explicitly NOT audited**):

| line | cache key | fn | enabled |
|---|---|---|---|
| `:463` | `['mdpf-per-firm-timeseries', effectiveFirmId]` | `getMdpfAggregateAUATimeSeriesByFirm` | `!== 'global'` |
| `:476` | `['mdpf-aggregate-timeseries', 'global']` | same fn, `'global'` | `=== 'global'` |
| `:487` | `['mdpf-per-firm-distribution', effectiveFirmId]` | `getAccountDistributionByFirm` | `!== 'global'` |

URL: `/api/general/mdpf/{firmId}/aggregate-aua-timeseries.json`. **The queries are firm-generic and already
accept Cottonwood** — `:488` even notes the cast was widened to `MdpfFirmId` *"so Cottonwood is not silently
outside the accepted set."* **What is missing is the artifact at that path, not the wiring.**

**THE CONTRACT COTTONWOOD MUST SATISFY IS NARROW.** `comp-types fields MdpfPerFirmTimeSeries` — 19 fields,
by FE consumer count:
`meta` **37** · `by_model` **21** · `dates` **10** · `firm_id` 3 · `partner_custody_total` 3 ·
`non_model_aua` 2 · `honest_none` 2 · `as_of_last` 1 · `model_aua` 1 · `opal_aggregate_aua` 1
**UNUSED (7): `partner_name`, `as_of_first`, `n_dates`, `sma_aua`, `backfill_methods`, `contract`,
`source_prefix`.**
→ **Cottonwood's artifact needs `meta`, `by_model`, `dates` and the value arrays. Seven fields can be
absent with zero FE consequence.**

### LAYER 4 · PER-FIRM PRESENTATION CONTRACTS — ❌ **THIS IS THE ACTUAL GAP**

| contract | shape | Cottonwood |
|---|---|---|
| `MDPF_SOURCE_ATTRIBUTION` `:258-282` | **`Record<MdpfFirmId, …>` — EXHAUSTIVE BY TYPE** | ✅ **present, and a missing entry would be a COMPILE ERROR.** The file says so: *"this Record is what makes a new firm a compile error instead of a silent 'SmartX' mislabel."* **This is the only layer-4 contract that is safe by construction — and it is the model the others should follow.** |
| `STACK_SERIES` `:142-151` | **closed 7-entry literal** | ❌ **the defect.** Legend (`:939`) + donut (`:613`) are data-driven; the stack is not. **Render-confirmed today: a Cottonwood model key outside the 7 → BOTH trend charts BLANK, legend still naming the models.** |
| `getModelColor` `modelPortfolioColors.ts:113-118` | fuzzy two-way `includes` over 7 Opal names | ❌ both Cottonwood models collapse to the **same blue** — visually indistinguishable (render-confirmed). |
| `MODEL_KEY` / `BLEND_AFTER` `:97-131` | 49F+INF model taxonomy | ❌ no Cottonwood entries; `keyForModel` mints `m_<slug>` that nothing mounts. |
| `assetsLabel(effectiveFirmId !== 'global')` | AUM for a firm, AUA for the aggregate | ⚠ works, but `AUMGrowthMetrics.tsx:87` hardcodes **"Total AUA"** — contradicts the donut's "Total AUM" on the same panel, **for all three firms**. |

---

## 3. THE HISTORICAL WARNING — INFLECTION ALREADY FAILED EXACTLY THIS WAY

**`MDPF_SCOPED` REOPENED on 2026-05-29** on Andrew's own portal smoke, verbatim from the project record:

> *"Andrew's portal smoke had caught **3 FE DEFECTS** — **data layer passed but the portal did NOT work for
> firm-scoped views.** (D1) **NO data surfaces for firm-scoped (49F/Inflection) Daily AUA Analysis —
> per-firm views EMPTY** (`perFirmMdpfData` query/binding gap; **the data EXISTS in S3**, so FE-wiring not
> data)."*

**THAT IS THE SAME SENTENCE AS TODAY'S RENDER FINDING, ONE FIRM LATER.** Inflection's per-firm view came up
empty because of a query/binding gap; Cottonwood's comes up empty because of a **series-mounting** gap
(`STACK_SERIES`). *Different mechanism, identical symptom, identical detection method — Andrew looking at
the page.*

> **THE LESSON THE RECORD ALREADY PAID FOR: on this page, a green data layer does not predict a working
> firm view, and only a RENDER distinguishes them.** MDPF_SCOPED needed an Andrew visual-smoke as a formal
> close leg (S5). **Cottonwood should carry the same close leg, and it should be a render, not a diff.**

---

## 4. WHAT TO ACTUALLY BUILD — the fork-pattern copy, in dependency order

1. **The artifact** at `json/mdpf/cottonwood/aggregate-aua-timeseries.json` (needs the producer fold + the
   publisher's `PUBLISH_MAP` entry + the bucket-policy ARN + the CF behavior — **three enumerations in
   three languages**, none of which currently name Cottonwood).
2. **`STACK_SERIES` → derive from the data** (or merge Cottonwood onto canonical keys). **This is the D6
   fork:** merge ⇒ no FE change; add ⇒ this change is mandatory or every Cottonwood model renders blank.
3. **`getModelColor`** — a Cottonwood entry, or a deterministic distinct-colour fallback.
4. **`account-distribution.json`** for the donut/bell-curve panel.
5. **Nothing at layers 1–2.** Already done.

**AND ONE PATTERN TO COPY DELIBERATELY:** `MDPF_SOURCE_ATTRIBUTION` is `Record<MdpfFirmId, …>` — adding a
firm without its metadata is a **compile error**. `STACK_SERIES`, `MODEL_KEY` and `getModelColor` are plain
literals, so adding a firm without them is **silent**. **The single highest-leverage FE change here is
making the other three exhaustive-by-type too** — it converts every future firm onboarding from a render-
discovered defect into a build failure.

---

## 5. NOT COVERED
- **`comp-cluster ModelPortfolios` TIMED OUT** (>120s, no output). The panel→drilldown tree and cross-panel
  coupling are **unresolved, NOT clean**.
- **`comp-platinum page ModelPortfolios --firm inf|cot` traces are byte-identical except the bucket line,
  and enumerate only 2 fetches** (`aum-metrics`, `account-distribution`) — **it does not see the three MDPF
  per-firm queries `comp-cache` found.** So its "no firm delta" result is an **instrument limit, not a
  finding**; I did not report it as one.
- Benchmark/Peers tabs (firm-blind), COUNT mode, and the AdvisorIntelligence `useTenantLayout` fork (a
  *separate*, registry-based pattern where Cottonwood is **already registered** — `LAYOUTS` in
  `useTenantLayout.ts`, plus `_partners/cottonwood/layout.ts`).
