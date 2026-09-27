# DSGN_IRPTV1.TO-IV-e-38.header-identity -- result log (0.9.0_WK_DSGN_IRPTV1~25)

Cell `IV-e-38`, C29 header: UIR-05, 12, 13, 14, 22, 30.

## What changed (portal, commit 9516cab4 on `wk-DSGN_IRPTV1-25-portal`, base DEV `fdccc6e6` + this
slot's IV-e-37 commit `d6e6eda3`)

- `src/pages/InvestorReporting/header/IdentityCard.tsx`
  - UIR-12: `who` reads `row.displayName` (the client's name only), not `row.label` (name +
    the search list's own masked discriminator, e.g. `"Coastal Ridge Trust ****4417"`). The
    masked tail is a disambiguator for the search RESULT LIST; once a client is accepted the
    selection is already unambiguous, and the tail read as an account-shaped fact inside WHO,
    contrary to "accounts appear under Over what".
  - UIR-13: the firm/kind subtitle changed from `` `${firmName} -- ${kind}` `` (the doc-comment
    "--" em-dash substitute this repo's own prose convention uses) to `` `${firmName}
    (${kind})` `` -- the same "name (qualifier)" shape `header/firm.ts`'s own
    `${o.name} (unavailable)` option already uses, consumed by `FirmDropdown.tsx` in this same
    file group.
- `src/pages/InvestorReporting/index.tsx`
  - UIR-05: the Global-mode empty-state line (`globalContext && !selectedScope`) reworded from
    `"Choose a client to confirm its firm and accounts in Resolution."` to `"Choose a client to
    see its firm and accounts."` -- drops the internal "Resolution" surface name for plain
    client language.
- New test: `src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-38.header-identity.test.tsx`
  -- one named arm per UIR row, `VERDICT: HEADER-IDENTITY-OK`.

Not touched (already satisfied by existing code, verified by direct render against the
committed fixtures, no source edit needed):

- **UIR-14** (`header/FirmDropdown.tsx` / `index.tsx:264-268`): the validated single/multi-firm
  path only ever offers clients from the currently-resolved scope, so a picked client's firm
  can never disagree with the control; the internal Global-catalogue path renders "Global
  (All)" as selected for as long as the header stays in Global mode, independent of which
  client search returned.
- **UIR-22** (`IdentityCard.tsx`'s "About this scope" `<details>`): the summary text is already
  plain client language, and `ScopeSummary`'s own system vocabulary (fingerprints, revisions,
  "Scope match") is already confined behind that click.
- **UIR-30** (`global/FirmAttribution.tsx`): `findPermittedFirm` returns at most one match and
  the component renders it in exactly one visible span; the firm token only ever appears in
  the non-visible `title` hover.

## Verification

- `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-38.header-identity.test.tsx`:
  1 pass / 0 fail, 16 expect() calls, `VERDICT: HEADER-IDENTITY-OK` (run clean twice).
- Mutant: `who`'s assignment reverted to `row.label` (python edit) -- re-ran the same
  invocation: `VERDICT: HEADER-IDENTITY-FAIL -- UIR-12: WHO name span reads "Coastal Ridge
  Trust ****4417" ...`. File restored from a saved copy; `git diff --stat` against the
  committed state printed the same 3-file/252-line diff as before the mutant (no drift); re-ran
  clean, twice, identical `VERDICT: HEADER-IDENTITY-OK`.
- `bun run typecheck` (tsc -b --noEmit, whole portal): 0 errors.
- `bunx eslint` on the four touched/read product files plus the new test: 0 errors, 9
  pre-existing-class warnings (react-refresh/only-export-components on `IdentityCard.tsx`'s
  own already-exported non-component helpers, predating this cell; two unused-arg warnings on
  `onNarrow`/`onAccountEntries`, also pre-existing).
- No-regression sweep: `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 97
  pass / 0 fail, 503 expect() calls, 97 tests across 83 files (82 pre-existing + this cell's 1
  new file).

## Off-task observation (not a project defect)

`git status` in the portal worktree shows ~24 files under
`src/pages/InvestorReporting/contracts/wire/*.ts` as modified, byte-identical against `git show
HEAD:<path>` (confirmed with a direct diff) -- CRLF/LF normalization noise from
`core.autocrlf`, the same class already recorded as `DSGN_IRPTV1-W4-S3` (OBSERVATION, INERT).
None of these files are in this cell's `<paths>` grant and none were staged or committed by
this worker.

## Surprise row filed

`DSGN_IRPTV1-W25-S2` (INVESTIGATION_v1.md): the cell's "Where it lives" map names one code
location per row without stating whether that location is the live defect or an
already-correct answer, and UIR-13's acceptance line ("normal punctuation") names no literal
replacement string. Two of the six named locations (UIR-12, UIR-13) were the live defect and
needed a source edit; three (UIR-14, UIR-22, UIR-30) were already correct and needed only a
test; UIR-13's replacement wording was chosen from an existing in-repo precedent
(`header/firm.ts`'s `"(unavailable)"` shape) rather than a spec-given literal. Filed under
`UNDER_INVESTIGATION` so the CVO's live walk (IVE38-AC2) reads the choice as a judgment call.
