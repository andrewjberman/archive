# IRPT_FNTEND.TO-FE-s-51 -- carried-hunks arm keyed to ancestry, not hardcoded to zero

Assignee: `0.9.0_WK_IRPT_FNTEND~2` (slot ~2). Worktree `C:/tmp/wk-irpt_fntend-9-2-fe-s-51`
(branch `wk-irpt_fntend-9-2-fe-s-51`, based on CLOUD HEAD `a21bf57e05` at spawn), portal sub-worktree
(branch `wk-irpt_fntend-9-2-fe-s-51-portal`, based on portal DEV `be8cf218`).

## What changed

`portal/src/pages/InvestorReporting/__tests__/fe-s-49/admin-gate.test.ts`, test `F49-AC8` (was
`:576-582`, now `:576-593` after the insert): replaced the hardcoded
`expect(carried.length).toBe(0)` with an ancestry-aware expectation. Uses the file's own
`run()` helper (the non-throwing sibling of `git()`, already used elsewhere in the file for
non-zero-rc-tolerant git reads) to run `git merge-base --is-ancestor c29a8b86 HEAD`: rc 0 means
`c29a8b86` (`RENDERING`, `2.0.0_SA_COO~D`'s `d13-visual-elevation` rendering commit -- confirmed
its subject: "rebrand(DSGN_REBRND, ...): Investor Reporting is Opal Admins only; ...") is an
ancestor of HEAD, so 2 unrelated hunks are expected (its merge legitimately carries visual-elevation
changes near the gate lines); rc 1 means it is not, so 0 remain the expectation. Any other rc throws
(the same discipline `git()` uses). The branch fired and its reason are printed:
`` `${RENDERING} ${c29a8b86IsAncestor ? 'IS' : 'IS NOT'} an ancestor of HEAD; expecting ${expectedCarried} unrelated hunk(s)` ``.

Committed to portal (local only, PORTAL IS FROZEN): `e52e9ba1` on
`wk-irpt_fntend-9-2-fe-s-51-portal`, 1 file changed, 13 insertions(+), 1 deletion(-).

## Acceptance

- **F51-AC1** (typecheck): `tsc -b --noEmit` at portal `e52e9ba1` -- rc=0.
- **F51-AC2** (admin-gate suite, this worktree's own HEAD): 10 pass / 0 fail / 20 expect() calls at
  portal `e52e9ba1`. The AC8 line printed: `c29a8b86 IS an ancestor of HEAD; expecting 2 unrelated
  hunk(s)` -- this worktree's HEAD (`be8cf218` before the amendment commit, `e52e9ba1` after) descends
  from `c29a8b86` (it is DEV, and DEV carries the rebrand). `UNRELATED HUNKS CARRIED INTO HEAD: 2 of 2`,
  matching the expectation; `carried.length` = `expectedCarried` = 2, PASS.
- **F51-AC3** (`9adad7ce` descends from `c29a8b86`): `git merge-base --is-ancestor c29a8b86 9adad7ce`
  -> rc=0. Confirms the analysis's own premise before relying on it.
- **F51-AC4** (measure `10c2f07d`'s ancestry, never assume): `git merge-base --is-ancestor c29a8b86
  10c2f07d` -> rc=1 -- `10c2f07d` is NOT a `c29a8b86` descendant (it is FE-s-49's own drain point, cut
  before the DSGN_REBRND rendering landed on this line). Implied branch: expect 0 unrelated hunks at
  that ref. Confirmed independently with a scratch harness (`.scratch/f51-ac4-harness.mjs`) that
  replicates the test's F49-AC8 hunk-carry logic against `git show <ref>:src/App.tsx` for an arbitrary
  ref (never a live checkout switch of this worktree's own branch):
  - `9adad7ce`: 5 hunks, 3 gate, 2 unrelated; `c29a8b86 IS an ancestor` (rc=0); expecting 2; CARRIED 2
    of 2; MATCHES: yes.
  - `10c2f07d`: 5 hunks, 3 gate, 2 unrelated; `c29a8b86 IS NOT an ancestor` (rc=1); expecting 0;
    CARRIED 0 of 2; MATCHES: yes.
  Both refs confirm the ancestry-aware expectation the amended test now encodes.
- **F51-AC5** (judgment, L9): reuses the file's own `run()` git-read helper (no second way to shell
  out introduced); still fails loudly on ANY unrelated hunk carried that neither branch's number
  admits (mutant control below). RECORDED, NO VERDICT.

## Control (mutant, not committed, restored before continuing)

Inverted the ternary (`c29a8b86IsAncestor ? 0 : 2` instead of `? 2 : 0`) in a scratch copy, swapped it
in, ran the suite, then restored the original file byte-for-byte (`git status --porcelain` read clean
after). At this worktree's HEAD (`c29a8b86 IS an ancestor`), the mutant printed `expecting 0 unrelated
hunk(s)` against the real carried count of 2: `F49-AC8` FAILED (`expect(carried.length).toBe(expectedCarried)`,
received 2, expected 0) -- 9 pass / 1 fail. The assertion is not vacuous: it discriminates the two
branches of the ancestry-aware expectation, not just "any non-negative number".

## Bounds

- Only `admin-gate.test.ts`'s `F49-AC8` block (`:576-593`) was touched; no other test in the file, and
  no other criterion in the suite, changed.
- Both repos: local commits only, no push/merge/rebase/`checkout --`/`clean` on a tracked branch.
  `9adad7ce` and `10c2f07d` were read via `git show <ref>:<path>` / `merge-base --is-ancestor`, never a
  branch switch of this worktree's own portal checkout.
- No surprise row filed: nothing off-task surfaced, no premise failed, every measurement matched the
  order's own analysis (round-8 item 9) at both named refs.

## Instruments

- `tsc -b --noEmit` (via `bun run typecheck`), portal `e52e9ba1`.
- `bun test` 1.3.9, `admin-gate.test.ts` alone, portal `e52e9ba1` and (mutant control) an uncommitted
  scratch swap of the same file.
- `git merge-base --is-ancestor` (workspace-repo shell, and the file's own `spawnSync`-based `run()`
  helper inside the test), against `HEAD`, `9adad7ce` and `10c2f07d`.
- `.scratch/f51-ac4-harness.mjs` (node, this worker's own scratch harness): replicates the F49-AC8
  hunk-carry computation against an arbitrary ref's committed `src/App.tsx` blob.
