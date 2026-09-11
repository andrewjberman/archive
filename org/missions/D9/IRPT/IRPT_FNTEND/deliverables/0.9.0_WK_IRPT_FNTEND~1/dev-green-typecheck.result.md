# IRPT_FNTEND.TO-FE-s-12 -- dev-green typecheck (round 2, cell FE-s-12)

**Worker** `0.9.0_WK_IRPT_FNTEND~1` · **workspace worktree** `/c/tmp/wk-irpt_fntend-2-1-fe-s-12` (branch
`wk-irpt_fntend-2-1-fe-s-12`, HEAD `d45d2760f2`) · **portal worktree** `/c/tmp/wk-irpt_fntend-2-1-fe-s-12/portal`
(portal repo, branch `wk-irpt_fntend-2-1-fe-s-12`, base `edab15b5`, repair commit `2750d80b`, **LOCAL**).

## Conclusion

All five criteria PASS by output. `bun run typecheck` went from **rc=2 with eight errors to rc=0 with none**,
and every test figure the repair could have moved is **identical to the pre-repair baseline**: 86 pass / 0 fail /
**359 expect() calls** on `fe-s-11`, `COMPONENTS: 65 (REUSED 27, NEW 38)`, `SCANNED: 38 files`, and
322 pass / 1 skip / 0 fail / 1496 expect() calls across 48 files on the whole Investor Reporting set.
Four lines changed across two test files; the ambient shims and `tsconfig.json` are untouched.

One surprise row filed: `IRPT_FNTEND-W1-S15` (the order specifies a `phase` value the ratified schema's enum
does not hold). It moves no criterion.

## The base, reproduced here first

The order's premise was re-grounded in this worktree before any edit. `bun run typecheck` printed the eight
errors **verbatim as the face lists them** -- same files, same line/column pairs, same TS codes -- and `rc=2`.
The `fe-s-11` suite was green at the same time (86 pass, 0 fail, 359 expect() calls), which is the whole point:
bun runs these tests without typechecking them, so the suite could not have caught any of the eight.

## Why the eight errors exist

The portal deliberately does **not** install `bun-types` or widen `tsconfig`'s `types` array, so `bun:test` and
`node:fs` are supplied by three **type-only ambient shims** inside the test tree, which TypeScript merges into
one surface per module:

| shim | contributes |
|---|---|
| `__tests__/fe-s-1/bun-test.d.ts` | `describe`, `test`, `it`, `beforeEach`, `afterEach`, `expect`, and a 15-member `Matchers` |
| `__tests__/fe-s-1/node-builtins.d.ts` | `readdirSync` (plain **and** a `withFileTypes: true` overload), `readFileSync`; `fileURLToPath` |
| `__tests__/fe-s-3/ambient-shims.d.ts` | `test.skip`, `mock.module`; **`existsSync`** |
| `__tests__/fe-s-7/ambient-shims.d.ts` | `Matchers.toBeCloseTo` |

Each shim's own header states the reason for staying narrow: widening the declared surface changes what *every*
file in the portal sees. The eight errors are exactly the four places `fe-s-11` reached past that surface --
`test.each` (x2), `Matchers.toMatch`, `node:fs.statSync` -- plus the four `TS7006` implicit-`any` parameters that
are a *consequence* of `test.each` being untyped, not independent defects.

## The four repairs (both files, nothing else)

1. **`census.test.ts` -- `test.each` over census rows -> a plain `for` loop.** One `test(\`row ${row.component}\`, ...)`
   per row, same names as the `'row %s'` template produced, same assertions. `row` now carries its declared
   `ComponentRow` type, so **two `TS7006`s disappear without an annotation**.
2. **`census.test.ts` -- the same conversion for the PRD accounting loop**, names `PRD reuse row #<n>`. Two more
   `TS7006`s gone.
3. **`census.test.ts` -- `expect(row.path).not.toMatch(/\(UNRESOLVED/)` -> `expect(UNRESOLVED_MARKER.test(row.path ?? '')).toBe(false)`.**
   The marker is a module-level regex with **no `g` flag, deliberately**: a global regex retains `lastIndex`
   between `.test()` calls, which would have made the new per-row loop order-dependent -- a bug the conversion
   could have introduced silently and no criterion would have caught.
4. **`colour-law.test.ts` -- `readdirSync(dir)` + `statSync(abs).isDirectory()` -> `readdirSync(dir, { withFileTypes: true })`**
   and the entry's own `isDirectory()`. The `withFileTypes` overload *is* declared by the shim and its entry type
   already carries `isFile()`/`isDirectory()`; one syscall per directory instead of one per entry, same partition.

Not used anywhere: `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, an `any` cast, a `tsconfig` change, a tsc
exclusion, or any strictness reduction. Verified by a scan of both changed files for all six forms (no hits, rc=1).

## Mutant control -- the check that mattered

A `for` loop that registers tests can register **zero** of them, and an inverted regex assertion passes
vacuously. Both would have read as a clean `86 pass`, so both repairs were mutated together and re-run:

| arm | mutation | predicted | observed |
|---|---|---|---|
| a | the converted assertion flipped to `.toBe(true)` | exactly the 27 REUSED rows fail, named individually | **27 fail / 59 pass**, `... > row YAxis` etc.; 27 is exactly the REUSED count the census prints |
| b | `if (entry.isDirectory()) continue` (no recursion) | `SCANNED` collapses far below 38 | **`SCANNED: 1 files`** |

Both fired as predicted. The mutation was then reverted and `git status --porcelain -- src | wc -l` read **0**
against commit `2750d80b`, so the restored files are byte-identical to the committed ones; all three live
criteria were re-run clean afterwards.

## Criteria

| id | invocation | deciding output | denominator | verdict |
|---|---|---|---|---|
| F12-AC1 | `bun run typecheck` | `rc=0`, no diagnostics, 26s (base: `rc=2`, 8 errors) | 8 of 8 base errors cleared; whole-program `tsc -b --noEmit` over all of `src/` | **PASS** |
| F12-AC2 | `bun test .../fe-s-11` | `86 pass, 0 fail, 359 expect() calls`; `COMPONENTS: 65 (REUSED 27, NEW 38)`; `SCANNED: 38 files` | 86 of 86 tests, 2 of 2 files; assertion count equals the base | **PASS** |
| F12-AC3 | `bun test src/pages/InvestorReporting` | `322 pass, 1 skip, 0 fail`, 1496 expect() calls | 322 of 323 across 48 of 48 files -- the issuer's base figure, unmoved | **PASS** |
| F12-AC4 | `git diff --name-only edab15b5 -- src \| grep -vc ...` | `OUTSIDE-GRANT: 0` | 2 of 2 changed files inside the grant | **PASS** |
| F12-AC5 | `git diff --name-only edab15b5 -- <shims> tsconfig.json \| wc -l` | `SHIMS-EDITED: 0` | 4 of 4 named shim/config paths | **PASS** |

**F12-AC4 corroborated with a wider instrument, not a repeat of the same one.** The criterion's own pathspec is
`-- src`, which cannot see a change outside `src/`. A second read with the pathspec *removed* -- `git diff
--name-only edab15b5` over the whole portal repo -- returned exactly the two granted test files, and
`git status --short` showed no untracked artifact left behind by `tsc` or `bun`.

**Determinism:** every live criterion run twice after the mutant revert. Identical on every graded figure; only
wall-clock timings differed (126ms vs 130ms; 2.32s vs 1.83s), which no criterion grades.

## Surprise

**`IRPT_FNTEND-W1-S15` (OBSERVATION, INERT).** This order's `<proof_of_spec>` block specifies `phase BUILD`;
`org/standards/PROOF_OF_SPEC.schema.json`'s `phase` enum holds eight members and `BUILD` is not one of them.
The instance was authored with the **ordered** value and run through the gate first, so the refusal is measured
rather than inferred: `VIOLATION: schema: phase: 'BUILD' is not one of [...]`, `INVALID (rc=1)`. It was then
carried as `BUILD-GENERAL`, the nearest and only build-flavoured member, with the substitution disclosed in the
instance's own `surprises` array. Whether future IRPT orders should specify `BUILD-GENERAL` or whether `BUILD`
belongs in the ratified enum is a schema/issuance decision above this lane, left open.

## What this order did NOT cover

- **Nothing about the shims' narrowness was fixed** -- `test.each`, `toMatch` and `statSync` remain undeclared,
  so the next test to reach for them fails the same way. The order forbids widening them (F12-AC5), and this is
  a standing condition of the design, not a defect introduced here.
- **`colour-law.test.ts`'s positive control is weak against the recursion arm**: mutant (b) dropped `SCANNED`
  from 38 to 1 and the suite still reported 0 fail, because the control only asserts `scannedFiles > 0`. That is
  pre-existing (it graded identically before this repair) and out of this order's grant, so it is recorded here
  rather than changed.
- **No render, no dev server** -- the order states none is needed; all five criteria are a typecheck, two test
  runs and two git diffs.

## Push state

**LOCAL.** Portal commit `2750d80b` on branch `wk-irpt_fntend-2-1-fe-s-12` of the portal repo; workspace records
on branch `wk-irpt_fntend-2-1-fe-s-12`. Nothing pushed, merged or rebased in either repo.
