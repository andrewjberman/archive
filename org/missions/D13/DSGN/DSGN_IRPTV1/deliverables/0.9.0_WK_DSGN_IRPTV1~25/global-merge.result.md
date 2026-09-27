# DSGN_IRPTV1.TO-IV-e-47.global-merge -- result log (0.9.0_WK_DSGN_IRPTV1~25)

Cell `IV-e-47`, UIR-07 Global view: the one exception to "the page never re-ranks" -- in Global mode
only, the merge of the per-firm answers puts a full-name match first, mirroring the server's own
`handler.full_name_match` predicate.

**Final status: BLOCKING on the `<status>` flip only.** IVE47-AC1 is PASS-by-output
(`VERDICT: GLOBAL-MERGE-OK`) and IVE47-AC2 is RECORDED (judgment). The proof-of-spec instance
was VALID (rc=0) by this order's own named invocation while the reconstructed TO file sat
untracked on disk; it reads INVALID (rc=1) now that the file has been removed (it cannot be
committed -- see S5), so the order's own `<status>` stays `pending`. See S5 below.

## What changed (portal, commit `b5915df3` on `wk-DSGN_IRPTV1-25-portal`, base DEV `fdccc6e6` +
this slot's IV-e-37 (`d6e6eda3`) and IV-e-38 (`9516cab4`) commits)

- `src/pages/InvestorReporting/header/search.ts`
  - `tokensFor`: fold to lowercase ASCII alphanumeric tokens (diacritics stripped) -- mirrors the
    server's own `normalize`/`tokens` (`infra/aws/lambda/investor-reporting/directory/handler.py`
    :64-74): everything that is not `[a-z0-9]` is a separator, so a comma and any run of
    whitespace are never tokens.
  - `isFullNameMatch`: the server's `full_name_match` predicate, mirrored -- the entry's display
    name's tokens, in any order, equal the query's tokens, in any order; an empty query never
    matches.
  - `mergeGlobalOrder(rows, query, scopeCount)`: a STABLE PARTITION (full-name matches first, in
    their original relative order; everyone else after, in their original relative order) --
    never a re-sort by score. `scopeCount <= 1` (single-firm mode) or an empty/no-token query
    returns the rows UNCHANGED.
- `src/pages/InvestorReporting/header/ClientSearch.tsx`
  - the Global browse effect's `setRows(toOptions(entries, firms))` became
    `setRows(mergeGlobalOrder(toOptions(entries, firms), query, scopes.length))` -- the ONE call
    site, no inline `.sort(` added to this file (kept true for `iv-e-37.search.test.tsx`'s
    UIR-07r arm, which still reads the file for the absence of `.sort(`).
- New test: `src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-47.global-merge.test.tsx` --
  four named arms ("first last", "last first", single-firm unchanged, non-matching rows keep
  served/firm order) plus a wiring check, `VERDICT: GLOBAL-MERGE-OK`.

## Fixtures

Every entry in the new test is a clone of the shared `directoryEntry.success.json` fixture
(already used unmodified by `iv-e-37.search.test.tsx`) with only `entryId`/`displayName`
overridden to synthetic names (Wren Aldercote, Piper Callahan, Bramble Court Estate, etc.) --
no real client name, no firm token anywhere in the file.

## Verification

- `bun test .../iv-e-47.global-merge.test.tsx`: 1 pass / 0 fail, 1 expect() call,
  `VERDICT: GLOBAL-MERGE-OK` (run clean twice).
- Mutant: `mergeGlobalOrder`'s partition comparator inverted (`a.match ? 1 : -1`, i.e. matches
  LAST) -- re-ran the same invocation: Arm 1/Arm 2 both failed, naming the match landing at the
  back of its firm's answers instead of the front. File restored from the edit and re-diffed
  clean against the committed state; re-ran twice, identical `VERDICT: GLOBAL-MERGE-OK`.
- `bun run typecheck` (tsc -b --noEmit, whole portal): 0 errors.
- `bunx eslint` on the two touched product files plus the new test: 0 errors.
- No-regression sweep: `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- all
  prior tests in the directory still pass, including `iv-e-37.search.test.tsx`'s UIR-07r arm
  (still reads `ClientSearch.tsx` as carrying no inline `.sort(`) and `iv-e-38.header-identity`.

## Surprise rows filed

- `DSGN_IRPTV1-W25-S3` (INVESTIGATION_v1.md): the cell's cited record (`2.0.0_SA_COO~P` @
  `80833001cb`) describes `handler.full_name_match` in prose only; the actual predicate body
  lives on a non-ancestor commit (`177719486c`), located by an all-branches search. This
  worker's independently-derived `isFullNameMatch` was written from the prose plus the file's
  existing `normalize`/`tokens` helpers before finding that commit; the later read confirmed no
  divergence. Filed `UNDER_INVESTIGATION`, class OBSERVATION, `INERT` (not blocking -- confirmed
  byte-identical in effect).
- `DSGN_IRPTV1-W25-S4` (INVESTIGATION_v1.md): this order's own identity block cites its issuance
  commit `dca01c9765`, which is NOT an ancestor of this worktree's HEAD -- the task-order file
  itself (`DSGN_IRPTV1.TO-IV-e-47.global-merge.md`) did not exist anywhere in this worktree
  (sibling TOs IV-e-37/IV-e-38 do, minted by the round-7 issuance that IS an ancestor). Written
  verbatim from `git show dca01c9765:<path>` (byte-identical) under BOUNDS's "this order's file"
  grant so `decomp_ref.to_ref` resolves and the `<status>` flip has a file to land on. Filed
  `UNDER_INVESTIGATION`, class OBSERVATION, `INERT`.
- `DSGN_IRPTV1-W25-S5` (INVESTIGATION_v1.md, **BLOCKING/ARMED**): the flip attempt was REFUSED
  by `.tools/to-pipeline-gate.py` (run automatically by `safe-commit.sh`) on TWO independent
  grounds: (1) a worker may not author a NEW tree task-order file (COO-only, LD-0521 A3) and this
  worktree's git history never received one for IV-e-47; (2) this worktree's own decomposition
  file carries only 28 cells and does NOT include `IV-e-47` (decomp v7 addendum 2 never landed
  here either), so the cell-alignment check refuses regardless. The reconstructed TO file was
  removed (plain delete, not `git clean`) rather than left unlandable. **This order's `<status>`
  therefore stays `pending` -- it cannot be flipped to `complete` from inside this worktree by any
  route this worker's grant permits.** Disarm owner: `2.0.0_SA_COO~D` (land the addendum-2 decomp
  and the TO-IV-e-47 issuance into this worktree's branch, or merge/rebase past `dca01c9765`).
