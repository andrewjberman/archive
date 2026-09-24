# FE-s-69 result -- FirmDropdown and Model Portfolios share one restyled class token

**FIXTURE-FED, not live-route.** Every capture below renders the real route (`/investor-reporting`,
`/portfolios`) against a local `vite` dev server with the app's OWN auth-bootstrap and OWN data-fetch
code paths exercised end to end; only the network responses are answered at the fetch layer by
`--fixtures` (a JSON map from URL substring to response body), never a live backend. That is the right
evidence for THIS card (FWD-12's DONE WHEN is about a control's visual/behavioural conformance -- font
weight, radius, box-shadow, and "the same restyled control in two places" -- none of which depends on
real portfolio data; the fixture only needs to get the two dropdowns to RENDER) and is not offered as a
live-route counterpart for the other seven round-11 cells, several of which are precisely about whether a
real answer-bearing state renders.

## The fix

One additive export, `PRIMARY_ON_SILVER_DROPDOWN_CLASS`, added to `portal/src/components/ui/PageSurfaceControl.tsx`
(`surfaceBase`/`controlVariants` untouched -- parked by CTO ruling on `font-medium`, four AdvisorIntelligence
pages depend on them outside this product). Both consumers now import it:

- `portal/src/pages/InvestorReporting/header/FirmDropdown.tsx` -- its local `PRIMARY_ON_SILVER_CLASS` constant
  deleted, `className={PRIMARY_ON_SILVER_DROPDOWN_CLASS}` in its place.
- `portal/src/pages/ModelPortfolios.tsx` -- ONLY the "Select Partner" firm dropdown's `className` prop
  (line ~1277, the one call site this order names); no other `PageSurfaceControl` use in that file was
  touched (there is only the one).

Old literal (portal `243089eb`): `h-11 px-5 pr-10 text-sm font-semibold tracking-wide rounded-lg shadow-sm
bg-transparent text-[hsl(var(--primary))] ring-1 ring-inset ring-[hsl(var(--primary))] ...`

New token: `h-11 px-5 pr-10 text-sm font-normal tracking-wide rounded-[3px] border
border-[hsl(var(--primary))] bg-transparent text-[hsl(var(--primary))] hover:bg-[hsl(var(--primary))]
hover:text-white active:bg-[hsl(var(--primary))]/85 bg-[right_0.85rem_center] bg-[url(...)]
hover:bg-[url(...)]` (chevron data-URIs unchanged, byte-identical to before).

Three changes, each tied to a live-measured violation:
- `font-semibold` (600) -> `font-normal` (400) -- C1 forbids 500/600.
- `rounded-lg` (8px) -> `rounded-[3px]` -- C11 allows 2/3/4px or a pill; `rounded.sm` is 3px.
- `ring-1 ring-inset ring-[hsl(var(--primary))]` + `shadow-sm` -> a plain `border
  border-[hsl(var(--primary))]`. **Why the ring had to go, not just the drop shadow:** Tailwind's `ring-*`
  utility renders through `box-shadow` (measured, not assumed -- see "Live values" below), so C11's "no drop
  shadow, the focus ring is the only box-shadow" cannot be met while ANY ring utility sits at rest, however
  thin. A `border` keeps the same purple outline on silver with `box-shadow: none` outside `:focus-visible`.

## Live values measured before pinning targets (HOW step 2's instruction)

Read on the UNEDITED file (`git show HEAD:<path>` swapped into place, dev server re-read, then swapped
back -- see "Before/after methodology" below), IRPT's FirmDropdown, port 5940, 1440 wide:

```
EXPECT-STYLE[select[aria-label="Firm"]::font-weight]: FAIL 600
EXPECT-STYLE[select[aria-label="Firm"]::border-radius]: FAIL 8px
EXPECT-STYLE[select[aria-label="Firm"]::box-shadow]: FAIL rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgb(95, 59, 227) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.1) 0px 1px 3px 0px, rgba(0, 0, 0, 0.1) 0px 1px 2px -1px
```

After the fix, same probe: `400`, `3px`, `none`. These ARE the acceptance targets (`=400`, `=3px`, `=none`)
-- they were read live before being pinned, not carried from the round-10 analysis.

## Before/after methodology (AC4)

AC4's BEFORE capture needed the file's state as of the round-11 issuance base, not my edited working
tree. This worktree carries no `git stash` (blocked here as a shared-worktree blast rule regardless of
worktree isolation) so the three edited files were copied out, overwritten in place with
`git show HEAD:<path>`, the AC4 capture taken, then the edited copies restored byte-for-byte (diffed
clean against the pre-copy backup after restore). `git status --porcelain` before and after the swap
shows the same three modified paths, confirming the restore.

## Acceptance criteria (raw output, verbatim tails)

**F69-AC1** -- `cd portal && bun run typecheck`: `rc=0`. PASS.

**F69-AC2** -- IRPT FirmDropdown, 1440:
```
EXPECT[select[aria-label="Firm"]]: PASS (1 visible)
EXPECT-STYLE[select[aria-label="Firm"]::font-weight]: PASS 400
EXPECT-STYLE[select[aria-label="Firm"]::border-radius]: PASS 3px
EXPECT-STYLE[select[aria-label="Firm"]::box-shadow]: PASS none
ASSERT-CONTENT: 1 of 1 met
ASSERT-STYLE: 3 of 3 met
FIXTURES-MATCH: matched 3 of 3
```
PASS. Capture: `f69_irpt_1440.png`.

**F69-AC3** -- same, 390:
```
EXPECT[select[aria-label="Firm"]]: PASS (1 visible)
EXPECT-STYLE[select[aria-label="Firm"]::font-weight]: PASS 400
EXPECT-STYLE[select[aria-label="Firm"]::border-radius]: PASS 3px
EXPECT-STYLE[select[aria-label="Firm"]::box-shadow]: PASS none
ASSERT-CONTENT: 1 of 1 met
ASSERT-STYLE: 3 of 3 met
FIXTURES-MATCH: matched 3 of 3
```
PASS. Capture: `f69_irpt_390.png`.

**F69-AC4** -- Model Portfolios BEFORE (HEAD, unedited), 1440: `SAVED : .../f69_mp_before_1440.png`. PASS.

**F69-AC5** -- Model Portfolios AFTER, 1440:
```
EXPECT[select]: PASS (1 visible)
EXPECT-STYLE[select::font-weight]: PASS 400
EXPECT-STYLE[select::border-radius]: PASS 3px
EXPECT-STYLE[select::box-shadow]: PASS none
ASSERT-CONTENT: 1 of 1 met
ASSERT-STYLE: 3 of 3 met
FIXTURES-MATCH: matched 1 of 1
```
PASS. Capture: `f69_mp_after_1440.png`. Read beside `f69_mp_before_1440.png`: the two panels are
pixel-identical apart from the restyled control itself (thinner purple outline vs. the old thicker
rounded-8px pill with a drop shadow; the semibold label reads visibly lighter).

**F69-AC6** -- Model Portfolios AFTER, 390:
```
EXPECT[select]: PASS (1 visible)
EXPECT-STYLE[select::font-weight]: PASS 400
ASSERT-CONTENT: 1 of 1 met
ASSERT-STYLE: 1 of 1 met
FIXTURES-MATCH: matched 1 of 1
```
PASS. Capture: `f69_mp_after_390.png`. (At 390 the header's "Select Partner:" label and the control
wrap/clip against the sidebar -- a pre-existing narrow-viewport layout condition, unrelated to this
cell's className-only grant; the control's OWN computed style is unaffected and is what this criterion
measures.)

**F69-AC7** -- `fe-s-3/dropdown-class.test.ts`: `67 pass, 11 skip, 0 fail` across 78 tests / 16 files.
PASS. Updated in this commit: the exact-class pin now checks for `border`, `border-[hsl(var(--primary))]`,
`font-normal`, `rounded-[3px]` and asserts the OLD tokens (`ring-1`, `font-semibold`, `rounded-lg`,
`shadow-sm`) are gone; the token-vs-substring rationale in the file's own docstring is unchanged and still
applies (`hover:text-white` legitimately survives).

**F69-AC8** -- whole `InvestorReporting` suite, dev server stopped first (port 5940 closed: `curl` -> `000`,
`Get-NetTCPConnection -LocalPort 5940 -State Listen` -> 0 listeners), `IRPT_FE_DEV_PORT` unset in that
shell: `619 pass, 22 skip, 0 fail` across 641 tests / 116 files. PASS.

**F69-AC9** -- judgment, recorded, no verdict given:
- `PRIMARY_ON_SILVER_DROPDOWN_CLASS` lives in `PageSurfaceControl.tsx` as an additive export; `surfaceBase`
  and `controlVariants` are byte-unchanged from before this cell (diffed).
- Full-repo census of `PageSurfaceControl` consumers (`comp-find`, corpus=all, denominator printed): 8 files
  import/reference it. Two are the ones this token now flows through
  (`FirmDropdown.tsx`, `ModelPortfolios.tsx`); the other six --
  `AdvisorIntelligence/_partners/{49financial,cottonwood,demo,inflection}/index.tsx`,
  `AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx`, `Positioning/Positioning.tsx` -- are
  untouched (no diff against HEAD on any of them).
- Before/after Model Portfolios pair (`f69_mp_before_1440.png` / `f69_mp_after_1440.png`): read side by
  side, identical layout, copy, data and surrounding chrome; the only visible difference is the dropdown
  control itself (radius, weight, outline, absent drop shadow).

## The four-part criterion rule, applied

(a) **WIRE MATCH** -- every capture above prints `FIXTURES-MATCH: matched N of N` (3 of 3 for the IRPT
route's `firm.json`, 1 of 1 for the Model Portfolios route's `mp.json`).
(b) **NAMED CONTENT** -- every capture asserts the specific control by selector (`select[aria-label="Firm"]`
or `select`), never by eye; `ASSERT-CONTENT: 1 of 1 met` on every one.
(c) **WRONG-STATE NEGATIVE CONTROL** -- run and confirmed to discriminate, for BOTH consumers (not
individually named as an acceptance id, but required by "THE CRITERION RULE" binding on every visual
state this round):
  - IRPT FirmDropdown: a `directory/resolve` fixture whose `permitted_firm_catalogue` carries exactly ONE
    firm (`fixtures/firm.one-firm.json`) makes `shouldRenderFirmDropdown` return false. Same selector,
    same invocation shape: `EXPECT[select[aria-label="Firm"]]: FAIL (0 visible)`,
    `ASSERT-CONTENT: 0 of 1 met`.
  - Model Portfolios: this is also the answer to the open question about a Model Portfolios
    content-control state where the dropdown disappears -- `internal = isInternal() || isDev()` gates the
    entire "Select Partner:" block (`ModelPortfolios.tsx` `actions={internal ? (...) : undefined}`); a
    non-internal PARTNER session (`--firm 49financial --claim userType=Partner`, which flips both
    `isInternal()` -- firmId no longer `opal-capital` -- and `isDev()` -- userType no longer `Dev`) removes
    the control entirely: `EXPECT[select]: FAIL (0 visible)`, `ASSERT-CONTENT: 0 of 1 met`. (Screenshots
    of both wrong-state runs are in `.scratch` only, not deliverables -- they are not named by any
    acceptance criterion and are offered here as the control record HOW step 4 requires, not as a graded
    artifact.)
(d) **GROUND** -- not applicable to this cell: every assertion here is a STYLE assertion on the control
element itself (`font-weight`, `border-radius`, `box-shadow`), never a ground/background-colour read, so
there is no `--expect-ground` in any of this cell's criteria and none was fabricated.

## Fixtures authored

- `src/pages/InvestorReporting/__tests__/fe-s-69/fixtures/firm.json` -- 3 wire-keyed entries
  (`directory/resolve` with a 2-firm `permitted_firm_catalogue`, `performance/`, `holdings/`), same
  operation/contract shapes as the existing `fe-s-63/fixtures/export-ready.json` pattern.
- `src/pages/InvestorReporting/__tests__/fe-s-69/fixtures/mp.json` -- 1 key, `category-views.json` (the
  URL substring `getCategoryViewsByFirm` always fetches, no `enabled` guard), a minimal valid
  `MdpfCategoryViews` block.
- `src/pages/InvestorReporting/__tests__/fe-s-69/fixtures/firm.one-firm.json` -- the wrong-state control
  fixture for (c) above (one permitted firm, dropdown does not render).

## Surprises

None filed for this cell. No fix needed a file outside the `<paths>` grant; the ModelPortfolios.tsx edit
touched only the one named `className` call site (confirmed: `git diff` against HEAD on that file is a
2-line change, the import line and the one className prop).
