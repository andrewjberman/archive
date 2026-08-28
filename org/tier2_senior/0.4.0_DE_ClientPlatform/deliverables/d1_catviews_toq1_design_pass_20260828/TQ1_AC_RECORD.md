# D1_CATVIEWS.TO-Q1-DE — AC record + deliverable

**Seat:** `0.4.0_DE_ClientPlatform~C` · **Issuer:** `2.0.0_SA_COO~Z` (TO @`2a1ab2f003`, dispatch msg 11997)
**Certifier:** `3.0.0_SA_CVO~Z` · **Date:** 2026-08-28
**Code:** portal `f93fb832` on `DEV` (parent `f1180aad`, the commit the TO measured). **Push state: LOCAL, unread at write time** — see §7.
**Authority:** ANDREW-DIRECT 2026-08-28 ~01:3xZ, VERBATIM: *"1.) Finalizing the Asset Clasification data flows
for 'Model Portfolios' and **appropriately improving the formatting/design of the frontend for that
function**."*

⛔ **THIS FILE IS NOT THE DELIVERABLE.** The deliverable is the eleven PNGs beside it. His eye is the bar,
no metric was attached, and none is invented here. This file exists so the ACs are auditable and so the
choices I did *not* make are cheap to disagree with.

---

## 1. THE ONE DEFECT NO STATIC CHECK IN THIS ESTATE COULD HAVE FOUND

`L0_LABEL` maps `SMA -> 'SMAs'` **specifically so the plural reads as a plural**, and the card label
carried a CSS `uppercase`, which painted it **`SMAS`** on screen. The source is correct; the render is
wrong. A grep for the label finds `'SMAs'` and reports health.

⭐ **It was found in the first read of the first screenshot** — which is the entire argument for TQ1-AC2's
instrument, arrived at from the other direction than the one the TO anticipated (the TO expects the
instrument to catch a *contrast* defect; it caught a *casing* one).

**Same class, found in the same read:** all three `PanelHeader title=` strings were authored pre-shouted as
`"ASSET CATEGORY VIEWS"` while `PanelHeader` already applies `uppercase` (`PanelHeader.tsx:70`). That one is
**latent, not visible** — it renders identically today and keeps shouting the day that style moves. Fixed
because it is the same defect, and labelled as latent rather than claimed as a visible win.

---

## 2. ACCEPTANCE CRITERIA

| id | verdict | evidence |
|---|---|---|
| `TQ1-AC1` | **MET** | Four BEFORE/AFTER pairs, same route `/portfolios`, same viewport **1440x900 fullPage** (`ui-smoke.mjs:118`), **every one READ by this seat** — files `01`–`04`. |
| `TQ1-AC2` | **MET** | Stated below as an observation from the read images, never from a class-name grep. |
| `TQ1-AC3` | **MET** | All five views EXHIBITED individually, not asserted — §4. |
| `TQ1-AC4` | **MET** | Measured, not asserted — §5. |
| `TQ1-AC5` | **MET** | `tsc -b` rc=0 **with a mutant control that failed first** — §6. |

---

## 3. `TQ1-AC2` — SILVER-CANVAS COMPLIANCE, FROM LOOKING

`ui-smoke` resolved the canvas live at **`rgb(195,202,218)`** — the silver.

**Read from the AFTER images (`01`, `03`, `04`, `05`, `06`):** the only things sitting directly on the silver
canvas are the page title (dark), the description line (dark grey with an indigo bold run), the
`Select Partner:` label (dark navy), the partner dropdown (indigo text and indigo ring), and the
`AUA / BENCHMARK / PEERS` tab strip (indigo active, near-black inactive). **No light text and no
ghost-white control renders outside a dark Panel.**

⭐ **And the sharper statement, because a compliance verdict on a whole page is wider than my change:**
**every element this pass touched is inside `Panel variant="mixed"`** — the change adds nothing whatsoever
to the canvas layer, so it cannot introduce the defect class. The page-level reading above is the state I
observed; the containment claim is the one my diff actually supports.

---

## 4. `TQ1-AC3` — THE FIVE VIEWS, EXHIBITED

⚠ **On real data every one of these renders "not available at this scope"** (`category_views` is
unpublished; D1_CATVIEWS is NO-SHIP) — see `00_BEFORE_real-backend-no-data_global.png`, which is the
default render and is **the failure state, not the surface**. Every exhibit below is served through the
repo's own fixture proxy (`portal/.frontend-dev/runners/category-views-fixture-proxy.mjs`).
⛔ **EVERY DOLLAR FIGURE IN THESE IMAGES IS SYNTHETIC.** Not firm data. Never quote one as product.

| view | cell | exhibit | what it shows |
|---|---|---|---|
| v1 — L0 cards | `D1-h-v1` | `01` pair | Models / **SMAs** / Client. The casing fix is visible here. |
| v2 — L1 bar + rows | `D1-h-v2` | `01` pair | Colour-coded bar with its legend rows, now one group. |
| v3 — L2 members | `D1-h-v3` | `02` pair | Models › Primary open, 5 members with amounts. |
| v4 — predicate unavailable | `D1-h-v4` | `03` pair | `inflection`: amber "Fee split unavailable at this scope" — **and SMA correctly draws NO card** (true zero). |
| L0/L1/L2 tree + `D1-inv-4` | `D1-inv-4` | `04` pair | `49financial`: the invariant **BREACHING**. |
| `D1-c-2` fallback (404) | `D1-c-2` | `05` | "No category view tree was returned for this scope." |
| `D1-c-2` fallback (non-404) | `D1-c-2` | `06` | "Category views are not available at this scope." |

⭐ **The 404 branch needed an instrument that did not exist.** `absent_by_scope` is set **only** on an HTTP
404 (`aum.ts:873`), and the repo's fixture proxy **deliberately never 404s** (an unknown firm gets a shape,
because there a 404 would look identical to "the fixture is not wired up"). Right for its job, structurally
unable to reach this branch. `_instrument_notfound-proxy.mjs` is the 404 front door I wrote to exhibit it —
**kept beside the evidence, deliberately NOT added to the repo.**

⛔ **The two fallbacks stay OBSERVABLY DISTINCT**, which is the property that branch pair exists to have.

---

## 5. `TQ1-AC4` — PRESENTATION ONLY, MEASURED

```
files changed in the whole portal repo : 1   (src/components/CategoryViewTree.tsx, +107 -39)
src/api/endpoints/aum.ts               : UNCHANGED   (git diff --quiet)
src/pages/ModelPortfolios.tsx          : UNCHANGED   (git diff --quiet)
occurrences in the diff of
  fetch|axios|url|request|api|endpoint|useEffect|localStorage : 0
```

Every changed line is a Tailwind class, a label string, a JSX grouping, or a prop pass-through. **`aum.ts`
was read and not touched.** No change to what is requested or to the payload shape.

⚠ **The `-39` deletions are the honest number to look at, and they are all re-writes of the lines directly
above their replacements** — the file is CRLF while the workspace is LF, so the edit was applied by
normalising to LF for matching and restoring CRLF on write. **Verified: 0 LF-only lines left behind.** A
text-mode round-trip here would have produced a whole-file diff and buried the real change.

---

## 6. `TQ1-AC5` — TYPECHECK, WITH A CONTROL THAT FAILED FIRST

```
mutant : const MUTANT_CONTROL: number = 'this must not typecheck'   (injected into THIS file)
         bun run typecheck  ->  rc=2
         src/components/CategoryViewTree.tsx(48,7): error TS2322: Type 'string' is not assignable to type 'number'.
revert : bun run typecheck  ->  rc=0
final  : bun run typecheck  ->  rc=0        (= tsc -b --noEmit)
```

⛔ **The control names my own file**, so the instrument is proven live *on the surface under test* — not
merely proven to exist. Bare `tsc --noEmit` is the instrument-that-cannot-fail here (root `tsconfig.json` is
`"files": []`), and it was not used.

⛔ **`commit-gate` printed, on its own face:** *"WARN: commit-gate checked 0 of 1 file(s) — NOTHING WAS
CHECKED … This line is NOT evidence of a clean gate."* Recorded because the TO predicted it. **It is not
cited as validation.** The risk-reflex did run and was clean on a printed denominator: 1 file checked
against 1351 danger nodes, danger map 26.1h old.

---

## 7. WHAT I CHANGED · WHAT I DELIBERATELY LEFT ALONE

**CHANGED** — casing fix (1); latent pre-shouted panel titles (2); as-of promoted from the tail of the
sum-check sentence into the panel subtitle, same single source, not duplicated (3); bar grouped with its
legend under a rule (4); row chevron moved into a fixed leading gutter, held `invisible` for non-drillable
rows so every dot, label and amount aligns across all three cards (5); L2 drawer indented behind a rail in
its parent row's colour, reusing the dead `SEGMENT.text` slot as `SEGMENT.rail` (6); L2 money column aligned
with the L1 column (7); grid column count follows the rendered set so a 2-card scope no longer strands an
empty third (8); the invariant line labelled "View-plane check" with an em dash (9).

**LEFT ALONE, and why — this half is what lets him disagree cheaply:**

- ⛔ **NO PERCENTAGES**, though a composition bar invites them and they were my first instinct. **This
  component's own law forbids it:** *"MEMBERSHIP IS NEVER COMPUTED HERE"* and *"A prettier bar does not
  become a place to derive numbers."* A share is a derived number. His word was **"dollar amounts"**.
- **The invariant control's two-branch styling.** Verified by the `04` PAIR, not by reading the diff: BEFORE
  and AFTER both render the breach as a bordered amber box in bold. The AFTER **gains** a bold label. The
  pass branch got quieter; **the failure branch did not.**
- **The `L2Members` caption and both fallback strings.** Another lane shaped those deliberately and recorded
  why; only casing and spacing moved.
- **`AUMGrowthMetrics`** renders absent cells (`N/A`) as the loudest thing in its tile — an inverted
  hierarchy, visible in every exhibit. It is a **shared** component used off this page, so the fix is wider
  than this TO. **Surfaced, not taken.**
- **The empty "AUA by Model" area** has no empty-state treatment while its right-hand neighbour has a proper
  one. That is the SmartX surface, not the asset-classification one. **Surfaced, not taken.**
- **`ModelPortfolios.tsx` entirely** — keeping the diff to one component is what makes AC4 checkable in one
  command instead of arguable.

**The single piece of NEW COPY in the whole pass is the label "View-plane check".** Named so, because
unlabelled the sentence read as debug output left on a client-facing page. It is the easiest thing here to
remove if he disagrees.

---

## 8. STATE + WHAT IS NOT DONE

- **NO-SHIP is untouched.** `D1_CATVIEWS` remains NO-SHIP; that gate blocks SHIP, not BUILD. Nothing here
  ships or promotes, and no met condition was read as a lift.
- **Portal `f93fb832` is LOCAL.** Push is the integrator's act in the open integration window; **push state
  UNREAD at the time of writing** — this line ages the moment an integrator runs.
- **Two surprise-channel items** were raised to `3.0.0_SA_CVO~Z` (cc issuer), neither blocking: the shared
  `AUMGrowthMetrics` N/A hierarchy, and `TaskStop` leaving a live `vite` child holding `[::1]:PORT` — the
  watcher-orphan shape on a different process class, which silently split my renders between a fixture proxy
  and a real backend until I found the second listener.
