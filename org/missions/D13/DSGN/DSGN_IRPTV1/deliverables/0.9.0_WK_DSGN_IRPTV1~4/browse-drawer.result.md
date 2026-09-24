# DSGN_IRPTV1.TO-IV-e-8 -- result file (`0.9.0_WK_DSGN_IRPTV1~4`)

## IVE8-AC1 -- built behaviour (bun test)

PASS by output. `VERDICT: DRAWER-OK` (1 pass / 0 fail, 13 `expect()` calls).
A stubbed api serving 3 `directory-browse` pages across 2 firm contexts: `ROWS: 3 of 3 across 3
pages`, `GROUPS: 2`, terminated entry `terminated=true marker=TERMINATED`, filter `"Coastal"` ->
2 rows, filter `"sunset"` (case-insensitive) -> 1 row, `IDS-PRINTED: 0` (row labels and the
rendered markup both checked against every candidate id token). The rendered markup (TEST-ONLY
seed) carries both group headers and every row's kind word / Active-or-Terminated / account count.

## IVE8-AC2 -- the seam, difference control (bun test)

PASS by output. `VERDICT: SAME-SELECTION-PATH` (1 pass / 0 fail, 6 `expect()` calls). Arm 1:
`selectionForBrowseRow`'s output deep-equals the pair built independently from
`header/search.ts`'s own `selectionFor`/`toOptionRow`. Arm 2: `ClientSearch.tsx`'s `handleSelect`
block is byte-identical to the base pin (EOL-normalized -- see the surprise row below); the
`Combobox`'s `onChange={handleSelect}` wiring is unchanged. Arm 3: `"Load more clients"` and
`function loadMore` are absent from both the source and the rendered markup.

## IVE8-AC3 -- the ruled touch T6 (diff)

PASS by output. `HUNKS [156, 166, 191] OUTSIDE [] | UNTOUCHED-SET '' | F5/F3 MISSING [] |
PAGING-GONE True` / `VERDICT: DRAWER-IN-GRANT`. `index.tsx` carries ZERO hunks outside the import
region / IV-e-4's actions ternary / IV-e-3's `<IdentityCard` line / the `<ClientSearch>` element's
own span -- this cell needed no change there at all (`<BrowseDrawer/>` mounts entirely inside
`ClientSearch.tsx`'s own row). `search.ts`, `selectionRequest.ts`, `ScopeSummary.tsx` untouched.
`ClientSearch.tsx`'s F5/F3 markers (`PAGE_LIMIT`, `MIN_QUERY_CHARS`, `generation`,
`++generation.current`) survive byte-for-byte; `loadMore`/"Load more clients" are gone.

## IVE8-AC4 -- judgment (CVO at L9), RECORD only, NO VERDICT

Static markup: `iv-e-8.drawer.html` (this folder) -- CLOSED (229 bytes, just the "Browse"
trigger) and OPEN (2529 bytes, TEST-ONLY seeded with `loadBrowseGroups`' real output against a
stubbed api: two firm groups, three rows -- a relationship, an account, and a second-firm
relationship from `directory.multiple-relationships.json`). No IV-e-2 smoke fixture
(`fixtures/smoke/dsgn-irptv1-cottonwood.json`) exists on this worktree's base -- IV-e-2 is a
sibling chain-B cell, not yet merged into this worktree's history -- so no PNG is offered this
round; this is stated, not worked around (IVE8-AC1/AC2 already exercise `BrowseDrawer` directly
against real fixtures).

**No dedicated drawer/dialog-as-panel primitive exists under `ui/components` today** -- only
`catalyst/dialog.tsx`, a centred modal, not a right-hand drawer. Per the cell's own fallback
clause this renders as a `Panel`-styled aside, `fixed inset-y-0 right-0`, with its own close
control -- stated here as the order requires.

Self-check against `portal/DESIGN.md` (my own read, not a verdict): the trigger and every row
render with no filled/primary background -- one accent colour (indigo, on hover) throughout, no
second (C8); `rounded-[3px]` on the trigger, the filter input and every row (C11-family radius).
Brief O2's bar, read off the markup: an advisor who does not know a client's spelling can either
scroll the grouped list (by firm, then by client) or type into the filter box -- neither requires
knowing any part of the name in advance.

## Regression + determinism

The twelve `dsgn-irptv1` suites (round-1's seven + IV-e-3's two + IV-e-4's one + this cell's two)
re-run unaffected: `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 12 of 12
files pass, 102 `expect()` calls, 0 fail. `bun run typecheck` rc=0, 0 diagnostics. `fe-s-2/` +
`fe-s-10/` re-run: 42 pass / 1 skip / 5 fail -- the SAME 5 pre-existing failures as the recorded
baseline (row `DSGN_IRPTV1-W4-S2`), 0 new. IVE8-AC1/AC2/AC3 each re-run twice back-to-back,
identical output both times.

## Surprise row filed

`DSGN_IRPTV1-W4-S3` (OBSERVATION, INERT): a working-tree source file carries CRLF line endings
while `git show <pin>:<path>` always returns LF-normalized blob content for the same commit -- a
naive substring comparison (this worker's own first-draft IVE8-AC2 test) reads a real, unchanged
code block as CHANGED unless both sides are EOL-normalized first. Caught and fixed
(`s.split('\r\n').join('\n')` on both sides) before this criterion was graded; IVE8-AC2 PASSES.
