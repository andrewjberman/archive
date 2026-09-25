# DSGN_IRPTV1.TO-IV-e-22 -- worker session record, 0.9.0_WK_DSGN_IRPTV1~13

## What round-3 caught (IVE14, IVE19, IVE18 -- ADJUDICATION_v2 C-S15)

With a client chosen, `AnalysisTab.tsx` mounted `ProspectComposer` unconditionally BEFORE
`GenerateComposer`, so the prospect upload sat above the three variant cards; both composers'
whole forms (title, prepared-for, comparisons, upload dropzone) rendered open at rest
(~1,900px); and `GenerateComposer`'s `clientLabel` fell back to the raw `inputs.clientId`
("C-CW-01") whenever a client was chosen, so the report-title placeholder printed the client's
id.

## The fix

- `AnalysisTab.tsx` now reads `useHeaderSelection()` directly. With a client accepted
  (`header.selection` truthy): `GenerateComposer` (cards first) renders, then `ProspectComposer`
  moves inside one closed `<details data-slot="prospect-disclosure">` whose `<summary>` reads
  "Analyze a prospect portfolio instead". With no client the order is UNCHANGED (upload leads,
  open) -- this arm already passed before this cell (verified against the base commit).
- `GenerateComposer.tsx` moves the three secondary sections (comparisons, title, prepared-for)
  into one closed `<details data-slot="generate-secondary-disclosure">` ("Report title, recipient
  and comparisons"); nothing fetched-on-open, only WHERE each fact renders moved (DESIGN.md C14).
  `clientLabel` now reads `header?.row?.label` (the picked row's display name) instead of falling
  back to the raw client id; the comparison input's placeholder drops "key"
  ("Opal model or ETF symbol" -- its `aria-label` already said "Compare with an Opal model").

## Tests (new, this cell)

- `iv-e-22.client-order.test.ts` (AC1): renders `AnalysisTab` inside/outside a
  `HeaderSelectionContext.Provider`; checks index order of `variant-cards` vs `upload-dropzone`
  and the closed-`<details>`/trigger-text state of the upload control, both arms.
- `iv-e-22.at-rest.test.ts` (AC2): renders the whole tab with a client; a depth-tracked
  `<details>` scanner (IVE19's own convention) confirms zero of the three secondary slots
  (`composer-title`, `composer-prepared-for`, `composer-comparisons`) sit outside a closed
  `<details>`, the cards render on the face, and exactly one `generate-button` renders on the
  face (a positive control shows all three secondary slots exist somewhere in the whole markup,
  not deleted).
- `iv-e-22.client-words.test.ts` (AC3): reads the `id="ir-composer-title"` input's `placeholder`
  attribute directly and checks it carries the producer fixture's `display_name` ("Smith Family")
  and not its `client_id` ("C-000123"); reads the comparison input's `placeholder`/`aria-label`
  for the word "key"; scans the whole render for `acc_`.

Every fixture used is `fixtures/wire/DirectoryEntry.valid.json` (producer contract fixture,
`client_id: "C-000123"`, `display_name: "Smith Family"`), adapted through
`contracts/adapt.ts`'s `adaptDirectoryEntry` + `header/search.ts`'s `toOptionRow`/`selectionFor`
-- the same producer instance `__tests__/fe-s-15/_load.ts`'s `resolvedScope()` already adapts.
No new firm token was hand-typed (this cell's BOUNDS, row W3-S2).

## Controls run

- **Mutant** (IVE22-AC1): `AnalysisTab.tsx`'s `hasClient` forced to `false` in place; re-ran
  `iv-e-22.client-order.test.ts` -- failed exactly as expected (ARM1: cards not first, upload not
  in a closed `<details>`, no trigger text). File restored from `.scratch/AnalysisTab.tsx.good`;
  `diff` against the restored file printed nothing (byte-identical); re-ran clean
  (`VERDICT: CLIENT-ORDER-OK`).
- **Determinism**: all three new tests run together, twice in a row post-restore -- identical
  VERDICT lines both times (`CLIENT-ORDER-OK`, `ANALYSIS-AT-REST-OK`, `CLIENT-WORDS-OK`).
- **Typecheck**: `bun run typecheck` (`tsc -b --noEmit`) rc=0 across the whole portal program
  after the fix (an earlier draft of the two new test files typed `firmId` as
  `SCOPE.scope.firmId` without its `| null` coalesce and was fixed to `?? ''` before this run).
- **No-regression, full suite**: `bun test src/pages/InvestorReporting/__tests__/` --
  701 pass / 82 fail / 2 errors. This matches the round-3-close baseline recorded in this
  project's own channel (`DSGN_IRPTV1-S14`: "742 pass / 82 fail" at a different merge point,
  f9a954b3+ecfd327a) -- the fail set was grepped for any mention of `analysis`,
  `generate-composer`, `prospect`, `iv-e-22` or `iv-e-14`: zero hits. Filed as a surprise row
  (`DSGN_IRPTV1-W13-S1`, OBSERVATION/INERT) rather than investigated further, since
  `contracts/envelope.ts` and `fixtures/fe-s-15/**` are outside this order's `<paths>` grant and
  the failing assertion (`parseIrEnvelope`) runs before either failing test's render call.

## IVE22-AC4 (judgment)

Not self-graded. Recorded `UNVERIFIABLE-BY-INSTRUMENT`, naming `2.0.0_SA_COO~D`'s drain trace
(CTO 100991) per the task order's own instruction. This worker's own AC1/AC2 mechanical reads are
offered as the proxy a live walk would confirm: with a client chosen, an advisor sees the three
cards and one Generate action without scrolling past a form, and the prospect path is one labeled
click away.
