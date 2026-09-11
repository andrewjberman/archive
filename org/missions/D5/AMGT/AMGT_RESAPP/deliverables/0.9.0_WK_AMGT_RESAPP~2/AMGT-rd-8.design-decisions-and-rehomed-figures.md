# AMGT-rd-8 -- THE SURFACE ITSELF: design decisions, rehomed figures, and what was built

`0.9.0_WK_AMGT_RESAPP~2`, round 5/v5, cell AMGT-rd-8 (row S16, FWD-15).

## What was built

`portal/src/pages/SecurityAnalysis/` (new page, route `/security-analysis` +
`/security-analysis/:securityKey`, wired into `App.tsx`'s routes + sidebar nav) --
mirrors `SecurityScanner.tsx`'s shell composition (`PageThemeProvider >
PageHeaderCleanBadge > LeadPanel (sticky) > TabNavigation > tab content`):

- `components/LeadPanel.tsx` -- the persistent panel (deliverable (a)): mode dropdown
  (Trending/Breakout/Starred + ticker search), List/Chart toggle, Refresh action,
  Security overlay.
- `components/RankedList.tsx` / `RankedChart.tsx` -- List/Chart views, PRODUCER order
  only (no `.sort()`, no client-side score).
- `components/StarredList.tsx` -- Starred mode (List-only at this cut; see "Scoped
  simplifications" below).
- `components/SecurityOverlay.tsx` -- Security-mode overlay (rehome destination #2,
  below).
- `components/ProvenanceLine.tsx`, `CheckFaceBadge.tsx` -- shared figure-rendering
  primitives (provenance beside every value, three-state check-face badge).
- `components/PrintExportAction.tsx` -- header export action + PDF preview modal
  (deliverable (c)).
- `tabs/ThesisTab.tsx`, `PeersTab.tsx`, `CoverageTab.tsx` -- the three tabs
  (deliverable (b)).
- `hooks/useLeadPanelApi.ts`, `useSecurityAnalysisState.ts` -- React Query hooks
  (namespaced `amgt-lead` keys) + page UI state.
- `types.ts`, `constants.ts` -- shapes transcribed from measured artifacts (live
  DynamoDB reads, landed JSON fixtures from rd-1/rd-3/rd-4/rd-5/rd-6/rd-7), never
  invented.
- `portal/src/api/endpoints/amgt-lead-panel.ts` -- typed fetch client for the (not
  yet built) scoped read API, following the `tickets.ts` precedent for "contract
  written now, backend lands later."
- `__rendercheck__/renderCheck.tsx` -- deliverable (d), see below.

## The three shape decisions, honored

- **Print is a header export action, not a tab.** `PrintExportAction` renders in
  `PageHeaderCleanBadge`'s `actions` slot; `SECURITY_ANALYSIS_TABS` names exactly
  three tabs and Print is not among them.
- **The Model tab is CUT.** No `ModelTab` component exists; `SECURITY_ANALYSIS_TABS`
  = `[thesis, peers, coverage]`.
- **The Lead Panel is persistent.** Mounted once by `SecurityAnalysis.tsx`, outside
  `TabNavigation`'s content area (same structural position `ScannerHeaderPanel`
  occupies in the F10 precedent) -- it does not remount when the active tab changes.

## WHERE each rehomed Model-tab figure went (the task order's own required answer)

The cut Model tab showed AMGT-s-1's landed figures (header scalars + one row per
fiscal year), each with AMGT-s-3's provenance line and AMGT-s-10's check-face
verdict. Per the CTO's frontend synthesis (`AMGT_RESAPP_FRONTEND_SYNTHESIS_20260911.md`
s.3, "Model tab CUT ... its figures rehome into Thesis and the Security-mode
overlay -- FWD-1 the DATA is unchanged"), both destinations are built:

1. **Thesis tab (`ThesisTab.tsx`)** -- the FULL rehome: every header figure AND every
   fiscal-year figure, each still carrying its `ProvenanceLine` (value/unit/basis/
   vintage/source) and `CheckFaceBadge` (PASS/REFUSE/PROVISIONAL) exactly as the
   Model tab rendered them. This is the complete data, unchanged, just moved under a
   different tab label -- alongside the five drafted prose sections (AMGT-s-9),
   which is why Thesis is also "was Drafting" per the CTO synthesis.
2. **Lead Panel's Security overlay (`SecurityOverlay.tsx`)** -- the CONDENSED rehome:
   header-scope figures only (ticker, company name, market cap, price, etc. -- the
   fields a PM wants at a glance without opening the full page), plus that name's
   own CHATTER/PRICE ranking rows and a peer-set summary, so a reader who clicks a
   name from the Lead Panel's ranked list sees its key figures without leaving the
   panel. The full fiscal-year table is deliberately NOT duplicated here -- that
   stays exclusively in the Thesis tab, so there is one authoritative place for the
   complete figure set and one condensed place for the at-a-glance overlay.

No figure was dropped: `ModelFigure[]` (the type carrying value/unit/basis/vintage/
source/sign/currency_caveat) is identical whether it renders in Thesis or in the
overlay -- only which SUBSET (all vs. header-only) and which CONTAINER differs.

## The Trending/Breakout x Price/Chatter mapping -- a measured design decision

The task cell text reads "Trending / Breakout x Price / Chatter" and, in one place,
"the two ranking axes crossed against the two modes (Trending/Breakout x
Price/Chatter)" -- read literally, this could mean a 2x2 cartesian grid of FOUR
independently-meaningful views. **That is not what was built, and here is why, with
the measurement behind it:**

`opal-harvest-security-metrics` (renamed from `opal-amgt-security-metrics` mid-session
-- see this cell's surprise row `AMGT_RESAPP-Z-W2-S10`) was scanned live,
`--projection-expression axis`, both before and after the rename: the ONLY axis
values ever written are `CHATTER` and `PRICE` -- no `TRENDING` or `BREAKOUT` axis
prefix has ever existed. Only two server-side producers were built this round
(AMGT-rd-5 chatter, AMGT-rd-6 price); `C-SERVER-SIDE-RANKING` binds this cell to
NEVER re-derive a ranking at render time, so a third or fourth axis cannot be
synthesized client-side without violating that bound.

The FWD-15 outcome text itself resolves the apparent 2x2 into a 1:1: "ranked by how
much they are moving in price or spiking in discussion" names exactly TWO criteria.
So this cell maps: **Trending -> the CHATTER axis** (spiking in discussion) and
**Breakout -> the PRICE axis** (moving in price), 1:1 -- both are genuine,
pre-computed, producer-ranked reads (`useLeadPanelRankings(mode)` ->
`axisForMode(mode)` -> a single `RankingAxis`). "Crossed against" in the cell text is
read as naming both label-pairs together (Trending<->Chatter, Breakout<->Price), not
as asserting four independently-backed combinations that do not exist in the data.

This decision is documented here, in the code's own doc comments (`types.ts`,
`LeadPanel.tsx`), and is explicitly one of the two things AC4's judgment text asks a
human reader to weigh ("does it read pre-computed rankings rather than re-deriving
any ranking at render time") -- so it is surfaced for that grading, not hidden.

## Scoped simplifications, stated plainly (bound (b)-style declared exclusions)

- **Starred mode is List-only at this cut** (`StarredList.tsx`). The CTO synthesis
  describes "same List/Chart, filtered to the PM-starred set." Chart-view-for-Starred
  is not built; FWD-15's own DONE WHEN bar ("opens the page, reads a ranked list,
  clicks through to a name") is satisfied by the List view alone. Follow-on, not a
  cut corner on this cell's bound.
- **The Lead Panel's Chart view renders the current snapshot, not a multi-day time
  series.** MEASURED: each axis has exactly ONE `as_of_date` landed so far (the daily
  schedule has run once per axis). `RankedChart.tsx` renders a bar-per-ticker of the
  current snapshot and states this plainly in the chart's own caption; the data shape
  (`RankingRow.as_of_date`) already supports a real time series the day a second
  snapshot lands, without a component rewrite.
- **The backend read API does not exist yet.** `AMGT_RESAPP_FRONTEND_SYNTHESIS_20260911.md`
  s.7(d) names this explicitly as an open gap ("Portal READ API ... new read
  affordance, round-3 cell"), and it is out of this cell's `<paths>` grant
  (`portal/src/` + `lib/research/`, no `infra/aws/terraform/`). `amgt-lead-panel.ts`
  is written as a contract-ready client against `/api/scoped/amgt/*` routes (the
  estate's own established pattern, per `comp-routes`' 27-behavior census), the same
  relationship `useScannerApi.ts` documents for `security-scanner.ts` pending DE work.
  Every call 4xx/no-routes at the edge today; this is a stated, out-of-scope absence,
  not a hidden gap.
- **Coverage tab renders empty-but-correct.** `opal-harvest-articles` (renamed from
  `opal-amgt-articles`) is MEASURED empty (0 items) -- the four harvesters that would
  fill it are being built in a separate harvest estate another seat owns. No
  harvester, backfill, or vendor fetch was built here.

## THE RENDER CHECK (deliverable (d))

No headless-browser / MCP browser tool is available in this session's toolset, and a
prior fabric incident (`org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-06-01/
work_1523Z_bmkaud_visual_smoke_headless_blocked.md`) recorded a 180s environment-wide
headless-Chrome navigate-hang on this estate. Instead: `__rendercheck__/renderCheck.tsx`
server-renders (`react-dom/server`'s `renderToStaticMarkup`) this cell's presentational
components, wrapped in the REAL `Panel`/`PanelHeader`/`PanelContent` containers with
fixture data, covering every state the color-law warning names: List, Chart, Starred,
Security overlay, Thesis figures (PASS + REFUSE + PROVISIONAL), the Coverage
empty-state, and -- the highest-risk case named by the task text -- the Print header
action rendered LOOSE ON THE CANVAS (outside any Panel).

Run: `cd portal && npx tsx --tsconfig tsconfig.app.json
src/pages/SecurityAnalysis/__rendercheck__/renderCheck.tsx`. Output committed at
`rendercheck_output.html` (pretty-printed) / `rendercheck_output.raw.html` in this
deliverables folder -- this worker READ it (not merely captured it): every
`text-white*` / `text-{color}-100..300` / `bg-white/N` class in the output sits
inside a `bg-[hsl(var(--semantic-background-contentPanel))]` (Panel variant="mixed")
or `bg-[hsl(var(--bg-header))]` (PanelHeader) ancestor -- confirmed by direct
line-by-line trace, not a grep. The ONE element genuinely outside a dark container
(the Print button, `<section style="background:hsl(222 24% 81%)">` with no Panel
wrapper) uses `text-[hsl(var(--bg-header))]` -- DARK navy text directly on the silver
canvas, which the color law requires and this render confirms.

## The table rename mid-session

`opal-amgt-security-metrics` / `opal-amgt-articles` were renamed to
`opal-harvest-security-metrics` / `opal-harvest-articles` partway through this
worker's session (harvest-estate migration). Independently verified live (both
before and after) rather than trusted from any single source -- see surprise row
`AMGT_RESAPP-Z-W2-S10` for the full grounding, including one detail in a relayed
coordinator message that did NOT check out against the actual code (two claimed
code citations describing an env-knob pattern that does not exist in the named
files). This cell's own code never hardcoded the table name (the frontend crosses
HTTP, never DynamoDB, directly) -- six doc-comment citations were updated to the
current, live name.

## Two instrument defects filed as surprises, not silently routed around

- `AMGT_RESAPP-Z-W2-S8` -- AC1/AC2's literal `npx tsc ...` invocation resolves to an
  unrelated npm registry package in this worktree (reproduced; absent in a sibling
  checkout with byte-identical node_modules). Graded from a disambiguated,
  positive-control-verified substitute (`npx --package typescript tsc ...`), named
  explicitly.
- `AMGT_RESAPP-Z-W2-S9` -- AC2's exact flag shape (`--noEmit`, no `-b`) is vacuous on
  this repo's root tsconfig (checks 0 files) -- MEASURED via positive control (a
  deliberate, reverted type error, uncaught by AC2's shape, caught by AC1's `-b`
  shape). AC1's own result is offered as AC2's substitute oracle, since it already
  serves AC2's stated intent (confirming AC1 isn't stale).
