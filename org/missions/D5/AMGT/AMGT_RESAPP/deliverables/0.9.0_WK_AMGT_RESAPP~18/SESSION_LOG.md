# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~18, AMGT_RESAPP.TO-AMGT-rj-1

THE ROUTE BOUNDARY AND THE RANKED CLICK. Worktree `C:/tmp/wk-amgt-11-1`, superproject
branch `wk-amgt_resapp-11-1` (tip at spawn `10c74d0efb`), portal worktree on
`wk-amgt_resapp-11-1-portal` (tip at spawn `9aef37344cd68c06f37d9d33eb1f2bc886dd6c4c`).
2026-09-15, ~08:4xZ to ~09:5xZ.

## 1. The bar, then the premises

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-1`; `org/`, `.tools/`,
`lib/research/identity/crosswalk.py` and `portal/src/pages/SecurityAnalysis/` all present.
TREE-OK, no BLOCKING row.

Every premise the order states was re-grounded against live state before any edit:

- **The crosswalk exists and resolves three forms.** `crosswalk.resolve` over rj-4's
  committed dry-run copy (89 records, `as_of` 2026-09-15): `BABA_US_Equity` -> matched as
  `model_key`, `BABA US` -> `bloomberg`, `BABA_US` -> `association_key`, all three to
  `BABA_US_Equity`; `ZZZ_NOPE_Equity` -> UNRESOLVED.
- **The break is where the order says it is.** `read_security_overlay` at `:630`
  @`10c74d0efb` carried the underscore-to-space inverse; the pre-edit run of AC1's own
  invocation returned `header_figures 13` for the canonical key and `0` for `BABA US`.
- **The landed model block has 13 header figures** (196 figures = 183 `fiscal_year_line_item`
  + 13 `header`), which is AC1's denominator.
- **`_path()` reads `rawPath`**, so the portal's `encodeURIComponent` reaches the adapter as
  `BABA%20US`. The boundary percent-decodes before it resolves.

## 2. What the producer actually writes -- two live reads that changed a decision

`read_rankings('TRENDING','CHATTER')` on the live table, 2026-09-15:

- 10 rows in `TRENDING_CHATTER#2026-09-15`; the `ticker` column carries the BLOOMBERG form
  (`BABA US`, `BA US`, `COST US`, `BP/ LN`, `ASML NA`, `Enel IM`, ...), never the underscore
  key and never the ` Equity` display form the landed model block carries.
  -> the overlay's point read is keyed by the identity's `bloomberg` form. Before this cell
  it was keyed by the landed block's `security` value (`BABA US EQUITY` after the adapter's
  own upper-casing) and could not match. A Bloomberg-form click now reaches rank 6.
- 0 of 10 rows carry `security_key` or `identity_status`.
  -> `RankingRowBase` declares both OPTIONAL and nullable, and the page renders the absence
  as UNRESOLVED. AMGT-rj-5 (chain B) is the cell that emits them.

## 3. What was built

**`lib/research/api/scoped_amgt.py`** -- `resolve_identity()` is the boundary; `handler()`
decodes the segment, resolves ONCE and passes the block to the reader serving the leaf;
`read_security_overlay`, `read_thesis_bundle`, `read_coverage_set` and the `/peers` branch
all carry the same block; `_print_pack` hands the renderer the landed block's own display
form and refuses unless the resolver agrees it names the same identity. Three identifier
conversions removed, zero added.

TWO MEASURED SURFACES, in order: crosswalk/v1 first; the LANDED ARTIFACT PLANE second
(a `model_block_<requested>.json` matched by its own name, verbatim). The second arm is not
decoration -- the CVO's `BABACVOCTRL_US_Equity` control artifact is not in the
coverage-derived crosswalk, and AMGT-rf-4's UNRESOLVED arm is graded against it. Resolving
only through the crosswalk would have silently emptied that contract. The block names which
surface answered (`identity_basis`) rather than flattening two claims into one token.

**`lib/research/api/tests/test_route_boundary_identity.py`** -- 13 tests, offline by
construction. The click-vs-direct-key equality carries its denominator (13 header figures
asserted before the two sets are compared); the "the store was never asked" arms use a
DynamoDB seam that raises on any call; the one-resolution-per-request arm counts calls on
the RESOLVER, so a reader that re-resolved its argument would show up as a second call.

**Portal** -- `RankedList` and `StarredList` pass `row.security_key`; a row without one
renders a visible UNRESOLVED marker and does not navigate; `types.ts` re-cuts
`SecurityIdentity` to the block the boundary returns and drops `bloomberg_ticker` (one field
was carrying both a display value and a lookup key); `IdentityLine.tsx` is the ONE rendering
of that block, read by the overlay and all three tabs.

**Harnesses** -- `errorEmpty.harness.cjs` gains a seventh state and a SECOND INSTRUMENT: the
actual `RankedList` is called with a spy on `onSelectSecurity` and every row's own `onClick`
is invoked, because static markup carries no click handlers. The number of handlers found is
itself a check. `join.harness.mjs`'s two fixtures were re-captured from the adapter, with the
diff against the committed bytes printed before adoption.

## 4. Controls

- **MUTANT (fired).** The click was reverted to the ticker in the committed `RankedList.tsx`
  and both instruments were re-run: AC3 -> `ranked-passes-key 0 ranked-passes-ticker 1`;
  AC4 -> `unresolved_row_navigates true`, `resolved_row_click_sends_canonical_key false`,
  `a_click_sent_a_ticker true`, `CHECKS-WRONG-WAY`. Restored from the pre-mutation copy,
  `cmp` byte-identical, `git -C portal status --porcelain` empty.
- **DETERMINISM.** AC1 twice, byte-identical. AC4's CHECK block twice, byte-identical.
- **NEGATIVE CONTROL, pre-existing and still firing.** Both join-harness arms' own
  NEGATIVE CONTROL still reports the shipped identity joining 0/183 and 0/1.

## 5. Rows filed

`AMGT_RESAPP-Z-W18-S1..S7` -- S1 (AC2's invocation collects zero tests), S2 (6 of 47 tests
unrunnable in a sparse cone), S3 (the join harness has no ranked-row fixture), S4 (no
`RankedRow` type exists), S5 (AC4's `rc=$?` grades `tail`), S6 (`read_point` upper-cases a
mixed-case producer ticker), S7 (the Coverage tab stars a canonical key into a ticker-keyed
store). S6 and S7 are live defects outside this cell's bound: filed, not repaired.

## 6. Commits

- portal `ad275969` on `wk-amgt_resapp-11-1-portal` (13 files).
- superproject `85b127afa5` on `wk-amgt_resapp-11-1` (adapter, tests, 7 rows).
- superproject (this deliverable + the status flip).

The `portal` gitlink is NOT moved: `e85f6eb8` before and after. Nothing pushed, nothing
merged, nothing deployed, no vendor call.
