# ADVI_SHARED — Project Brief (Request for PRD)

| Field | Value |
|---|---|
| **Brief author** | 0.4.0_DT_ClientPlatform |
| **Date** | 2026-05-12 |
| **Directed to** | 1.0.0_SA_CTO |
| **Directed by** | Andrew (direct 2026-05-12) |
| **Ask** | Author PRD for `ADVI_SHARED` |
| **Project type** | Macro `ADVI` / Suffix `SHARED` — full code `ADVI_SHARED` |

---

## Why this brief exists

Andrew directive 2026-05-12 evening, post `portal-v2.1.82` PROD deploy:

> "Write a briefing for CTO about component-level refactoring for the linting.
> It will actually be part of a larger project called ADVI_SHARED — which will
> be all about how to manage the shared vs fine-tuned/bespoke components and
> elements of ADVI between the various advisors. We want to be able to get this
> very clean and streamlined, because as we add new advisors, we want to be
> able to easily generate fine-tuned ADVI pages to their business, which will
> generally look the same but may have different asset structuring, features,
> maybe even different tabs/routes. Tell CTO to make a PRD on it."

The lint refactor is **one work-stream inside ADVI_SHARED**, not the whole project. ADVI_SHARED is the multi-tenant architecture project; the lint warnings are the empirical surface area exposing where the current architecture is fraying.

---

## Empirical trigger — `portal-v2.1.82` deploy gate

During the 2026-05-12 PROD deploy preparation (Andrew directive: "clean working
tree + deploy to PROD") I ran `bun run typecheck` and `bun run lint` against
the post-RD-marathon DEV head (commit `939138a7`).

| Check | Pre | Post (DT fixes) | Notes |
|---|---|---|---|
| typecheck (`tsc -b --noEmit`) | **12 errors** | 0 errors | DT commit `bf26d1b8` |
| lint errors | **7 errors** | 0 errors | `eslint --fix` (unused imports) |
| lint warnings | 103 warnings | **102 warnings** | Refactor-scope — not interim-safe to fix one-off |

The 12 TS errors I fixed in `bf26d1b8` were narrow type-shape mistakes (e.g.
`tsData.points` vs `tsData.data`, missing `SecurityType` import, redundant
`Record<>` casts). Those are normal regressions from a fast marathon — not
architectural.

**The 102 remaining lint warnings are different in kind.** They cluster into
two categories that *both* point at the same architectural seam ADVI_SHARED is
meant to formalize.

---

## The 102 warnings, decomposed

### Category A — `react-refresh/only-export-components` (~75 of 102)

Files exporting **both** React components and non-component values
(constants, types, helper functions) from the same module. Fast Refresh has to
remount the whole module on every edit, losing component state during HMR and
sometimes during navigation.

**Worst offenders:**
- `src/pages/Attribution/constants/holdings-shared.tsx` — 13 warnings; mixes
  component cells, constants, and helper functions in one file.
- `src/pages/AdvisorIntelligence/_shared/panels/ClientsTable.tsx`,
  `_shared/AdvisorBookView.tsx`, `_shared/tabs/AdvisorsTab.tsx`,
  `_shared/AdvisorPublicProfile.tsx`, `_partners/inflection/InflectionInsightsPanel.tsx` —
  each exports both a top-level page/panel component and a handful of helper
  constants/sub-types used by sibling files.
- `src/contexts/AuthContext.tsx`, `src/context/TimeMachineContext.tsx` — context provider files
  exporting both `<Provider>` and `useContext()` hooks.

**Root cause:** there is no convention for where firm-agnostic constants
("asset class color palettes", "role labels", "cohort enum") live versus
where the components that consume them live. So they end up in the file
that first needed them.

### Category B — `react-hooks/static-components` (~12 of 102)

Components declared **inside another component's render body** — e.g.
`SortIcon` declared inside `FeeSummaryPanel`'s function body. Every parent
re-render constructs a new component identity; React unmounts/remounts the
inner component and its state is wiped.

**Worst offenders:**
- `src/pages/AdvisorIntelligence/_shared/tabs/AdvisorsTab.tsx:246,265,293,1112` —
  four inner components.
- `src/pages/AdvisorIntelligence/_shared/panels/ClientsTable.tsx:125,138` —
  two inner components.
- `src/pages/AdvisorIntelligence/_shared/AdvisorPublicProfile.tsx:1672` —
  long-lived page-component with nested helpers.
- `src/pages/AdvisorIntelligence/_shared/ClientDetail/panels/*.tsx`,
  `_shared/components/AUATrendChart.tsx`, `_shared/panels/ClientListPanel.tsx`,
  `_shared/panels/useSyncedHeight.tsx`.

**Root cause:** when an inner component closes over multiple parent props +
tenant flags + sort state, the cleanest *local* refactor is to inline it.
Extracting it requires either threading a 6-argument props bag, or pulling
the surrounding state out into a shared hook. Without a convention for
where those hooks live (or whether they're shared across firms), authors
inline.

---

## How both categories trace back to multi-tenant architecture

ClientPlatform pod is the only one carrying the firm-multiplexing concern in
AdvisorIntelligence. Today's structure:

```
portal/src/pages/AdvisorIntelligence/
├── _partners/
│   ├── 49financial/   { constants.ts, index.tsx, roles.ts }
│   └── inflection/    { constants.ts, index.tsx, layout.ts, roles.ts, overrides/, InflectionInsightsPanel.tsx }
├── _shared/
│   ├── AdvisorBookView.tsx        (1 file, 2.3K lines — reads firm flags)
│   ├── AdvisorPublicProfile.tsx   (1 file, ~2K lines — reads firm flags)
│   ├── ClientDetail/              (many panels — some firm-aware)
│   ├── components/                (AdvisorAnalytics, PartnerAnalytics, ...)
│   ├── hooks/useTenantLayout.ts   ← THE EXISTING PRIMITIVE
│   ├── panels/                    (ClientsTable, FeeSummaryPanel, etc.)
│   ├── tabs/                      (AdvisorsTab, ClientsTab, etc.)
│   └── types/TenantLayoutConfig.ts ← THE EXISTING CONFIG SHAPE
└── index.tsx (dispatcher: PARTNER_VIEWS[firmId])
```

There IS already a tenant primitive: `useTenantLayout(firmId): TenantLayoutConfig`,
covering tab visibility, cohort availability, role composition, advisor-list
caps. **It is only adopted in 4 call-sites** (`AdvisorBookView`,
`AdvisorPublicProfile`, `PartnerAnalytics`, `ClientsTab`). Everywhere else
the `firmId === 'inflection'` style of inline branch still leaks across the
codebase. The two patterns coexist:

```ts
// Existing good pattern (useTenantLayout)
const layout = useTenantLayout(firmIdFromOverride(firmOverride))
if (!layout.panels.roleComposition?.enabled) return null

// Existing bad pattern (firmId conditional inline)
if (firmId === 'inflection') { ... }
```

Today's 102 warnings are the symptom of a **half-migrated tenant abstraction.**
Each new advisor (next up: at least one more advisor partner, per Andrew's
intent in this briefing) increases the cost of every inline `firmId === '...'`
conditional combinatorially.

---

## What ADVI_SHARED PRD should cover

The CTO PRD should establish the canonical architecture for:

### 1. Tenant configuration completeness

Extend `TenantLayoutConfig` (already exists) to be the **single source of truth**
for per-firm divergence. Audit and add:

- **Asset class taxonomy** — per-firm asset class list, ordering, color palette,
  groupings (today the Inflection Mix pie has different colors than 49F).
- **Role taxonomy** — per-firm advisor role enum (Inflection has no role
  breakdowns; 49F has architect/consultant/implementor/local_ops/addl). The
  `roleComposition.enabled` flag is the seed; this expands into a full role
  registry.
- **Feature flags** — per-firm enablement of: ADV cohort, GEO cohort, OFC
  cohort, role-stacked AUA Clients sub-mode, fee-bucket split availability,
  GRO mode, AUATrendChart Max-window cap, etc. (Each of those is currently a
  scattered inline conditional or a per-firm component override.)
- **Route tree** — per-firm tab order, hidden tabs, custom tabs (e.g.
  `InflectionInsightsPanel` lives only on Inflection; 49F has Performance/Peers).
- **Panel registry** — per-firm panel substitution
  (e.g. `revenueOpsPanel: 'standard' | 'inflection_insights' | 'suppressed'`
  already exists; extend pattern to TaxCostBasis, FeeEfficiency, Concentration,
  etc.).
- **Data sources** — per-firm Lambda routing (`LAMBDA_FIRM_ID` map already
  exists in `api/endpoints/advisor-intelligence.ts`; consolidate with
  `TenantLayoutConfig`).
- **Numeric defaults** — per-firm window defaults, period defaults, fee-view
  defaults.

### 2. File organization discipline (resolves Category A)

Adopt one-of:

- **Co-location with split modules.** A page becomes a directory:
  `_shared/panels/ClientsTable/{index.tsx, constants.ts, types.ts, helpers.ts, ClientsTable.test.tsx}`.
  Components export ONLY from `index.tsx`; constants/types/helpers export
  from their respective siblings.
- **Per-domain shared modules.** Move all asset-class constants to
  `_shared/constants/assetClasses.ts`, all role constants to
  `_shared/constants/roles.ts`, etc. Component files import from these.

The PRD picks the convention. Either resolves Category A wholesale.

### 3. Component extraction discipline (resolves Category B)

Mandate: **no component declared inside another component's render body.**
Two acceptable patterns when a sub-component needs many parent values:

- Extract to sibling component file; thread props bag explicitly.
- Extract to local non-component helper that *returns* JSX as a function
  call (not a component — no JSX `<Inner />`, just `inner(args)`). Still
  testable, no remount problem.

The PRD picks the convention. Either resolves Category B wholesale.

### 4. New-firm scaffolding

Document the canonical onboarding path. Suggested form:

```
bun run scaffold-firm --id=<new-firm-id> --name="<Display Name>"
```

Emits:
- `_partners/<new-firm>/{constants.ts, index.tsx, layout.ts, roles.ts}`
- Wires entry in `PARTNER_VIEWS` (index.tsx dispatcher)
- Wires entry in `LAYOUTS` (useTenantLayout hook)
- Wires entry in `LAMBDA_FIRM_ID` (api endpoints)
- Wires entry in `SCOPE_FIRMS` (auth claims, scoped routing)

After scaffolding, the new firm renders all `_shared/*` components with
the `DEFAULT_LAYOUT` config; the team customizes by editing `layout.ts`
flags, not by adding `if (firmId === 'newfirm')` branches.

### 5. Migration plan from today's state

The PRD should sequence:

- **Phase 0** — Audit. Enumerate every existing `firmId === '...'` inline
  branch + every per-firm component override + every per-firm constant
  override. Map each to a `TenantLayoutConfig` field. Confirm coverage.
- **Phase 1** — Resolve the 102 lint warnings concurrently with the audit:
  every file refactored under Categories A and B above adopts
  `useTenantLayout` in the same commit. This collapses the half-migration.
- **Phase 2** — Land scaffolding tool. Validate against a synthetic
  `firm-test` tenant.
- **Phase 3** — Documentation; deprecate inline-firmId pattern in lint
  config (custom rule or grep gate in CI).

Phase 1 is where the lint refactor lives. The 102-warning surface area
becomes the empirical work-list — finite, bounded, mechanical once the
architecture is set.

---

## Out-of-scope for this PRD (separate threads)

- Pseudonymization / scope-token concerns (owned by AUTH / 0.7.0_AE_CloudOps).
- Lambda-side data shape divergence per firm (owned by DS + AE; ADVI_INFETL).
- 49F vs Inflection data-availability gaps (owned by DS lanes A/B/C/D under
  ongoing INFLEC parity work).

ADVI_SHARED is portal-side architecture only. Data-side multi-tenancy is a
companion PRD if one is needed; this brief does not pre-suppose it.

---

## Acceptance for the PRD

The PRD is accepted as authored when it:

1. Picks a convention for Category A (file split) and Category B (component
   extraction) and documents the rationale.
2. Specifies the full extended `TenantLayoutConfig` field-set with examples
   for both 49F and Inflection.
3. Specifies the new-firm scaffolding flow at command-level.
4. Decomposes Phase 1 into task orders (one per file or per cluster of files)
   that DE 0.4.0 can dispatch to RD 0.4.2 / DT 0.4.0 / DE 0.4.0 itself.
5. Names the lint regression gate that prevents re-introduction
   (eslint rule, grep gate, codeowner mandate, or alternative).

---

## Cross-references

- Existing tenant primitive: `portal/src/pages/AdvisorIntelligence/_shared/hooks/useTenantLayout.ts`
- Existing config shape: `portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts`
- Deploy artifact: `portal-v2.1.82` (PROD, 2026-05-12, rollback baseline tag)
- DT post-deploy lint summary: 102 warnings, 0 errors, 0 CI blockers
- Pod owners: 0.4.0_DE_ClientPlatform (PM), 0.4.0_DT_ClientPlatform (deploy + tooling),
  0.4.2_RD_AdvisorIntelligence (page implementation)
- Andrew direct: 2026-05-12 evening
