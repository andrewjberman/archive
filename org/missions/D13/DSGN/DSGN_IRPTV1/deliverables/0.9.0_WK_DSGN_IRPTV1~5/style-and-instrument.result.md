# DSGN_IRPTV1.TO-IV-e-2 (style-and-instrument) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~5`. Portal branch `wk-DSGN_IRPTV1-5-portal`, commit
`4a55727eb7e49f9185045b7cd83caba11ea54d6e` (LOCAL, carries IV-e-1's a380bcb5/538fe641 first).
Workspace branch `wk-DSGN_IRPTV1-5`.

## What changed

**(a) Style (row C-S13).** `PerformanceHeadline.tsx` and `SecurityList.tsx`: every
`text-slate-*`/`border-slate-*` class moved onto the DESIGN.md token set --
`text-[hsl(var(--palette-navy))]` for primary figures/values, `text-[hsl(var(--palette-
darkGray))]` for secondary labels, `border-[hsl(var(--hairline))]` for hairlines (borders,
table rules) -- and every `font-semibold` (600) to `font-bold` (headings/figures) or
`font-normal` (body), matching `header/IdentityCard.tsx`'s own usage (read, not edited beyond
one attribute -- see (b)). No wire fact's text changed; a class-only diff, confirmed unchanged
by every dsgn-irptv1 suite (13 pass / 0 fail).

**(b) Instrument (row C-S14).** New fixture `fixtures/smoke/dsgn-irptv1-cottonwood.json`: a
full envelope set (resolve-scope, directory-browse, selections, holdings-snapshot,
performance-report) built from round 1's seed shape (`fe-s-14-cottonwood.json`) but fixing TWO
defects that seed carried (isolated with a direct `bun run` against
`contracts/envelope.ts`'s `parseIrEnvelope`, no browser, before touching `ui-smoke.mjs` at
all):

1. The envelope's top-level `firm_id` must equal `data.verified_request_firm_id`
   (`parseIrEnvelope`'s resolve-scope-specific check) -- round 1's seed had
   `firm_id='fir_c07701a9d3b5e2f4860c1a7b'` against `data.verified_request_firm_id='F-CW'`,
   mismatched, throwing on every parse despite the URL matching a declared fixture (so
   `FIXTURES-MATCH` still read "matched", which is exactly round 1's own recorded state,
   "resolve-scope unresolved", without a mechanism named).
2. Every non-refused envelope's `unprojected_grant.kinds` must be a RECORD (object), never an
   array -- round 1's `kinds: []` failed `isRecord()` and threw `EnvelopeMismatch
   ('unprojected_grant', ...)` unconditionally, on every route, before the resolve-scope-
   specific check even ran.

`header/IdentityCard.tsx` gets one wrapping `<div data-slot="identity-card">` around its
existing `<Panel>` root -- the same one-attribute-touch pattern `SecurityList.tsx`'s own
`<div data-slot="security-list">` already uses (`Panel` does not forward arbitrary DOM
attributes). Admitted by BOUNDS.

## IVE2-AC1 -- TOKENS-ONLY

`python -c "...CLASS-CENSUS..."` over the two files -- PASS. `CLASS-CENSUS over 2 files: slate
tokens 0 | 600 weights 0` / `VERDICT: TOKENS-ONLY`. Measured 19 slate / 2 semibold in these two
files at this order's own branch tip before the fix (differs from the order text's issuance
figure of 38/11, measured at a different vintage; both are pre-fix nonzero counts the fix
reduces to 0).

Mutant control: reverted `PerformanceHeadline.tsx`'s tile-value class back to `font-semibold
text-slate-900`, re-ran -- `CLASS-CENSUS over 2 files: slate tokens 1 | 600 weights 1` /
`VERDICT: SLATE-OR-600-REMAIN`. Fired as expected; file restored, `git diff` clean afterward.

## IVE2-AC2 -- the instrument

`node scripts/ui-smoke.mjs investor-reporting iv-e-2.png --port 5181 --fixtures
dsgn-irptv1-cottonwood.json` (the order's own required invocation, no `--click` steps) --
PASS. `FIXTURES: 5 declared; 2 matched >=1 URL` / `FIXTURES-MATCH: matched 2 of 5` /
`FIXTURE-DEAD: .../performance/sel_... | .../holdings/sel_... | .../selections`.

2 of 5 is the genuine ceiling for a click-free run on THIS app: `resolve-scope` and the page's
own UNCONDITIONAL initial `directory-browse` (fired by `ClientSearch`'s mount effect, no typing
needed) both auto-fire; `selections`/`holdings`/`performance` only fire after a server-accepted
account selection, which `TabShell`'s own docstring states plainly ("Reporting and holdings
require a server-accepted account set") and no `--click`-free invocation can reach. `iv-e-2.png`
(55485 bytes) shows `IdentityCard` mounted with real tile text (WHO "No client selected", HOW
MUCH "value pending", AS OF "not supplied", OVER WHAT "Account details not supplied") -- **not**
the "Scope could not be resolved" page.

Negative control: re-ran the identical invocation against round 1's UNFIXED seed
(`fe-s-14-cottonwood.json`) -- `FIXTURES: 2 declared; 1 matched >=1 URL` / `FIXTURES-MATCH:
matched 1 of 2` / `FIXTURE-DEAD: .../performance/` -- byte-identical to the failure mode the
task order's own text names, confirming this fixture's two isolated fixes (not a timing
coincidence) are what closes it.

**Beyond AC2's own invocation** (documented per the order's own allowance: "If the page needs a
--select/--click sequence, put the exact ui-smoke.mjs command in the result file"):
`scripts/ui-smoke.mjs`'s `--fill`/`--click`/`--clicktext` vocabulary CANNOT reach the "Client
search" control -- measured directly: `--fill "Client search=Cottonwood"` ->
`FILL-FAIL: ... locator.fill: Timeout 30000ms exceeded` (its accessible role is
`combobox`, not `textbox`; `getByRole('textbox', {name:'Client search'})` finds nothing). This
is the SAME gap already named at `IRPT_FNTEND` FE-s-78 and already worked around there, and at
`org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_P/*.mjs`, with a STANDALONE Playwright
driver -- never an edit to `scripts/ui-smoke.mjs` (out of this order's `<paths>` grant either
way). This order's own such driver,
`iv-e-2-selection-driver.mjs` (in this deliverables folder), replicates `ui-smoke.mjs`'s own
auth-stub/CORS/fixture-route recipe byte-for-byte, then drives `page.getByRole('combobox',
{name:'Client search'})` directly to select "Cottonwood Trust" and clicks the Holdings tab
(`page.getByRole('button', {name:'Holdings', exact:true})` -- `TabNavigation`'s tab strip is
plain `<button>`s, no `role="tab"`). Result: `DRIVER-FIXTURES-MATCH: matched 5 of 5`;
`iv-e-2-selected.png` (173077 bytes) shows `IdentityCard` (Cottonwood Trust, account A-CW-01),
`PerformanceHeadline` (4 tiles, mounted on the Performance tab before the Holdings click) and,
after the Holdings click, `CategoryViewTree`'s donut + `SecurityList`'s SECURITIES table (2 rows,
Ticker "not supplied" on both -- no `display.symbol` planted, honest per IV-e-1's fix). DOM read:
`identityCard=2, securityRows=2, headlineTiles=0` (Holdings tab active at capture time; a
separate run before the Holdings click read `headlineTiles=4`). Netlog:
`iv-e-2-selected.netlog.tsv`.

## IVE2-AC3 -- the seam

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- PASS. `13 pass / 0 fail`
across 9 files, 91 `expect()` calls; every round-1 and IV-e-1 suite unchanged.

## IVE2-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-e-2.png` (55485 bytes) -- the order's own required AC2 invocation: IdentityCard only.
- `iv-e-2-selected.png` (173077 bytes) -- the supplementary driver's richer capture: IdentityCard
  + PerformanceHeadline + SecurityList/CategoryViewTree, all navy-on-white, no slate visible.
- `iv-e-2-selection-driver.mjs` -- the driver script itself, for reproduction.
- `iv-e-2-selected.netlog.tsv` -- the driver's own request log (5 of 5 fixture routes hit).

## Surprise rows filed

`DSGN_IRPTV1-W5-S2` (OBSERVATION, INERT) -- the fixture's two parser-level defects (firm_id
match; `unprojected_grant.kinds` as a record) and the `scripts/ui-smoke.mjs` role=combobox
instrument gap, both isolated and worked around before the graded runs; cites `W3-S2` for the
naming-gate mechanism (this order's own naming-gate hit was on a fixture VALUE, not the
filename -- renamed `bd-2026-09-23` to `src-cw-2026-09-23`, commit landed clean).
