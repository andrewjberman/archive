# IRPT_FNTEND.TO-FE-s-79 -- result

**FIXTURE-FED DISCLOSURE.** Every capture below is fed by `--fixtures` JSON served through the
smoke harness's stub transport (`scripts/ui-smoke.mjs`), never a live backend: F79-AC2 uses
`fe-s-18-frozen.json`; F79-AC4 uses `fe-s-18-holdings-observed.json` (as the task order names).
F79-AC3 originally named `fe-s-18-holdings-observed.json` too, but the issuing COO amended the
task order (`7310707142`, `353cb80d21`) to point F79-AC3 at the sibling fixture
`fe-s-18-holdings-missing-attribution.json` after independently confirming the original fixture
can never mount the selector (see F79-AC3 below); this result reflects the amended criterion. No
live API, no network egress.

## The fix

Three Tailwind default-palette utility classes carried no DESIGN.md token and, on this build
(Tailwind v4), genuinely serialise their computed `color` as `oklch(...)` rather than `rgb(...)`
-- confirmed directly (see Controls, below). Replaced, each with the DESIGN.md-named role its
surrounding surface already establishes (C3's ink table: primary/body = navy `#163372`,
12.00:1 on a white panel; secondary/supporting = `darkGray` `#6B7280`, 4.83:1 on a white panel):

| file:line | before | after | role (C3) | measured `color` |
|---|---|---|---|---|
| `tabs/analysis/RequestList.tsx:38` | `text-slate-600` | `text-[hsl(var(--palette-darkGray))]` | secondary (informational message on panel) | `rgb(107, 114, 128)` |
| `tabs/holdings/HoldingsTab.tsx:99` | `text-slate-800` | `text-[hsl(var(--palette-navy))]` | primary/body (file's own comment: "dark text on a white panel") | `rgb(22, 51, 114)` |
| `tabs/holdings/SliceTable.tsx:143` | `text-slate-700` | `text-[hsl(var(--palette-darkGray))]` | secondary (a supporting data value in a table row, same convention as EtfModal/ModelPortfolioModal/SatelliteModal `<dt>` labels and `PanelStates.tsx`'s `SECONDARY_INK`) | `rgb(107, 114, 128)` |

`--palette-navy` and `--palette-darkGray` are both defined, real CSS custom properties
(`portal/design/themes/opal-capital.css:23,30`) already used across the codebase via this exact
`text-[hsl(var(--palette-X))]` idiom (`comp-find`, 16 and 83 hits respectively). No new token was
invented; C6's exempt data palette was not touched (none of these three lines are in a chart or
data-family component).

## Acceptance results

**F79-AC1** -- `cd <WS>/portal && bun run typecheck` -- `rc=0` (`tsc -b --noEmit`, no errors).
**PASS.**

**F79-AC2** -- `RequestList.tsx:38`'s ground, `fe-s-18-frozen.json`, click Analysis:
`EXPECT-GROUND[[data-slot="requests-unavailable"]]: PASS rgb(255, 255, 255)` /
`ASSERT-GROUND: 1 of 1 met`. Capture: `f79_analysis.png`. **PASS.**

**F79-AC3** -- ORIGINAL RUN (named fixture `fe-s-18-holdings-observed.json`, click Holdings):
`EXPECT-GROUND[[data-slot="holdings-qualification"]]: UNMEASURABLE (selector matched nothing)` /
`ASSERT-GROUND: 0 of 1 met`. **REFUSED as an order defect, not a code or instrument defect** --
`HoldingsTab.tsx`'s own `HoldingsQualification` only mounts when
`gap.unknownNodes > 0 || showsTargetWeights(snapshot)`, and every node in that fixture is
`authoritative: true` on basis `OBSERVED`, so the panel legitimately never renders for this data
(confirmed by direct PNG read, `f79_holdings.png`: a plain READY holdings view, no qualification
banner). Filed as row `IRPT_FNTEND-W29-S1` (OBSERVATION, INERT) rather than substituted, per
BOUNDS ("REFUSE any criterion you cannot satisfy as written ... do not weaken a criterion").

**AMENDMENT (`2.0.0_SA_COO~F`, `7310707142` + `353cb80d21`).** The issuing COO independently
confirmed the diagnosis above (read `classificationGapOf`/`showsTargetWeights` in `slices.ts`
directly against the fixture's raw JSON, then re-ran the exact invocation live) and swapped
F79-AC3's fixture to the sibling `fe-s-18-holdings-missing-attribution.json` (whose nodes carry
no `classification` block, which the app treats as non-authoritative -- that fixture's whole
documented purpose). The fix itself (`HoldingsTab.tsx:99`) was confirmed correct throughout;
only the criterion's fixture reference was wrong.

**RE-RUN (this session, amended fixture `fe-s-18-holdings-missing-attribution.json`, click
Holdings):** `EXPECT-GROUND[[data-slot="holdings-qualification"]]: PASS rgb(255, 255, 255)` /
`ASSERT-GROUND: 1 of 1 met`. Capture: `f79_holdings.png` (re-saved over the original capture at
the same path, now showing the qualification banner rendered on its white ground). **PASS.**

**F79-AC4** -- `SliceTable.tsx:143`'s ground, `fe-s-18-holdings-observed.json`, click Holdings:
`EXPECT-GROUND[[data-slot="slice-supervision"]]: PASS rgb(255, 255, 255)` /
`ASSERT-GROUND: 1 of 1 met`. Capture: `f79_slice.png`. **PASS.**

**F79-AC5** -- whole-suite, dev server stopped (`curl` -> `000`), `IRPT_FE_DEV_PORT` unset:
`627 pass / 22 skip / 0 fail / 2642 expect() calls`, 649 tests across 119 files. **PASS.**

**F79-AC6** -- judgment, graded at L9 by the CVO. RECORDED (see Controls below for the
underlying measurements): each replacement is a real, pre-existing DESIGN.md-named token
(`--palette-navy` / `--palette-darkGray`, never invented), the ground/color pairing is measured
against the actual backdrop with the hardened FE-s-74 instrument (never `UNMEASURABLE` where the
element renders), and the C6 data/status palette is untouched. **NO VERDICT TAKEN.**

## Controls (a control is a claim)

**Mutant.** Temporarily reverted `RequestList.tsx:38` to its original `text-slate-600` (working
tree only, portal DEV server live, no commit) and re-ran a direct
`--expect-style '[data-slot="requests-unavailable"]::color=rgb(107, 114, 128)'`:
`EXPECT-STYLE[...]: FAIL oklch(0.446 0.043 257.281)` -- confirms Tailwind v4's default palette
genuinely serialises as `oklch(...)` on this build (the exact defect the cell names), and that
the check discriminates. Restored the fix (`git diff` confirmed byte-identical to the
pre-revert state) and reconfirmed `PASS rgb(107, 114, 128)`.

**Determinism.** F79-AC2's exact invocation run twice in immediate succession; the deciding
`EXPECT-GROUND`/`ASSERT-GROUND` lines are byte-identical across both runs (only the PID in a
Node warning and the output filename differ).

**Direct color reads (all three replacements, non-acceptance, supporting AC6):**
`RequestList` -> `PASS rgb(107, 114, 128)`; `HoldingsTab` (against the missing-attribution
fixture, since the observed fixture never mounts the element) -> `PASS rgb(22, 51, 114)`;
`SliceTable` -> `PASS rgb(107, 114, 128)`. All match their DESIGN.md C3 role hex exactly.

## Status

`<status>` flipped to `complete`: all 6 of 6 criteria now stand PASS-by-output or RECORDED
(judgment), following the issuer's amendment of F79-AC3's named fixture and this session's
re-run confirming `ASSERT-GROUND: 1 of 1 met` on the amended fixture.

## Surprises filed

`IRPT_FNTEND-W29-S1` (OBSERVATION, INERT) -- F79-AC3's original fixture mismatch, detailed
above; resolved by the issuer's amendment (`7310707142`, `353cb80d21`).
