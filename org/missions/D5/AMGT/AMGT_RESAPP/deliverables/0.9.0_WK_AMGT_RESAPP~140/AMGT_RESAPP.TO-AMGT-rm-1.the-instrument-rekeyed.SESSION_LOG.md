# AMGT_RESAPP.TO-AMGT-rm-1.the-instrument-rekeyed -- session log

**Worker:** `0.9.0_WK_AMGT_RESAPP~140`. **Worktree:** `C:/tmp/wk-amgt-38-140` (outer), portal nested at
`C:/tmp/wk-amgt-38-140/portal` (branch `wk-AMGT_RESAPP-140-portal`). **Round:** 38, cell `AMGT-rm-1`,
wave 0.

## What was built

`portal/scripts/ui-measure.mjs` and `portal/scripts/ui-contract-check.mjs` re-keyed per the cell's s.1:

1. **Band predicate**: `bandContainersTopLevel` now counts elements carrying the Panel's own
   `.dark-band` class (`Panel.tsx:89-90`, applied on `variant="chart"|"mixed"`) OR whose computed
   background matches the RESOLVED `--bg-band` custom property, resolved off `document.body` (see
   surprise `AMGT_RESAPP-W140-S1` for why `document.body`, not the literally-named
   `document.documentElement` -- the latter resolves to the pre-DSGN_REBRND-round-2 `:root` value,
   which is numerically the STRIP colour).
2. **Strip predicate**: new `stripContainers` field, the OLD hard-coded-`rgb(10,23,51)` test renamed
   to what it actually measured -- panel title strips and the sidebar `<aside>`.
3. **`--scope main|body`**: both scripts accept a CSS-selector scope (unchanged generic mechanism,
   `main`/`body` are just selector strings). `ui-contract-check.mjs` now ALWAYS measures both scopes
   per state and prints both tables; the `--scope` flag chooses which one is GRADED (drives exit
   code) and prints first, the other prints beneath as informational, plus a `main` vs `body`
   comparison table (`stripContainers`, `identityAccents`).
4. **Action fills vs identity accents**: `purpleFills` now counts only INTERACTIVE elements
   (`button, a, [role="button"], input`) filled with the resolved `--semantic-action-primary` colour,
   excluding the C8 identity set (the page-title rule, `w-[3px]` class marker, and anything inside
   `<aside>` -- the sidebar's active nav item and avatar). The excluded set is printed separately as
   `identityAccents`.
5. **Clipped text**: new `clippedTextBlocks` (+`clippedTextSamples`, up to 8) -- LEAF text-bearing
   elements (no element children, matching the existing `cands` leaf test used for the overlap
   signal) whose `scrollWidth > clientWidth + 1` under `overflow:hidden|clip` or
   `text-overflow:ellipsis`. Leaf-scoped deliberately: an all-elements pass caught the page's own
   `<main className="... overflow-x-hidden">` wrapper as a giant false "clip", capping the field at
   a constant 8 (the sample-slice length, not a real count) on every state -- see the code comment
   at the fix site.
6. **`ui-measure.mjs --self-test --fixture <path>`**: loads a static fixture HTML
   (`src/pages/SecurityAnalysis/__harness__/tests/uiMeasureFixture.html`, this worker's own file, not
   the dev server) via `page.setContent`, runs the SAME classifier function, asserts the five new/
   changed values on the fixture's POSITIVE arm and a NEGATIVE arm built by string-transforming the
   SAME source (band class removed, strip inline style recoloured) so the two arms cannot drift
   apart by hand-editing only one.

`ui-smoke.mjs` was not touched (screenshots are scope-agnostic; nothing in s.1 named a smoke mis-key).
`Panel.tsx` was read only (for the `.dark-band` marker). `App.tsx`, `index.css`, `DESIGN.md` were not
edited (Bound 3; DESIGN.md carries no clause to cite for clipped text per the cell's own s.1 item 4).

## Bugs found and fixed in my own build, before proof (not filed as surprises -- caught pre-shipment)

- `isIdentityAccent`'s class-marker check first used a `\b`-anchored regex (`/\bw-\[3px\]\b/`) against
  a className string ending `...w-[3px] identity-rule`; `\b` never fires between `]` (non-word) and
  the following space (also non-word), so the regex silently never matched. Replaced with a token
  split/`includes` check. Caught by the AC1 self-test failing `identityAccents: got 1, expected 2`
  before any proof run.
- `clippedTextBlocks` originally reported `clippedTextSamples.length` (capped at 8) instead of the
  full `clippedEls.length` -- see item 5 above.

## Surprises filed

- `AMGT_RESAPP-W140-S1` (INERT, DISMISSED_WITH_REASON): the cell text's literal
  `document.documentElement` instruction for resolving `--bg-band` would reproduce the exact defect
  being fixed; resolved off `document.body` instead, verified against the live rendered colour.
- `AMGT_RESAPP-W140-S2` (INERT, UNDER_INVESTIGATION): AC3's literal `&&`-chained invocation
  (`ui-contract-check.mjs ... && ui-class-census.mjs ...`) can never reach the census command on
  state `list`, because `list` carries pre-existing, out-of-this-cell's-scope predicate FAILs
  (`weights`, `radii`) at every scope, and Bound 2 requires leaving those standing rather than fixing
  them. Ran the literal invocation verbatim (recorded, exit 1, no census line) and separately ran the
  un-chained census command for completeness (`FILES 31 TOTAL 0`, matches expectation -- no page
  source moved).

## Runs

- AC1 (`ui-measure.mjs --self-test --fixture ...`): `ac1.final.out.txt` -- exit 0, `SELF-TEST OK`.
- AC2 (`ui-contract-check.mjs --port 5182 --scope main --out contract-check-rekeyed`):
  `ac2.final.out.txt`.
- AC3 (`ui-contract-check.mjs --port 5182 --scope body --states list --out
  contract-check-body-control && ui-class-census.mjs ... | tail -1`, literal, plus the un-chained
  census run for completeness): `ac3.final.out.txt` / `ac3-census.final.out.txt`.

Dev server: `bun run dev --port 5182` from `portal/`, log at `dev.log`, stopped at end of session.
