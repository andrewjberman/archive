# PROMOTE RECEIPT -- AMGT_RESAPP bq-2 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-17

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bq-2.what-changed-and-money-display-features-promoted-to-prod.md`
GO: broker msg 7616 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261017T1443Z_amgt-resapp-bq2-sa-promote-20261017_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for `bc0a5cd9` and `aba098da` against origin/DEV.
- Builder output (verbatim):
  - `RELEASE-CHECK features=2 first_parent_commits=2 unapproved=0 ref=refs/heads/release/20261017T144424Z sha=99d2b2a70cc1`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-changed-list-value class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T133543Z-fa30 pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-money-display class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T123830Z-d775 pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261017T144424Z base=15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8 head=99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7`
- Release branch: `release/20261017T144424Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8` (equal to the order's cut head; no deviation from the order's numbers).
- PROD head after: `99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7`.
- Push state, as an `ls-remote` read: `99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.235`, peeled with `^{commit}` = `99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7`.
- Main portal tree: back on DEV (verified); worktree removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Sixteen paths, all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit 99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7`: one workflow on that sha, run `39042189942`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` 99d2b2a7. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read sixteen `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back

STATUS: STOPPED at the approval register (AMENDMENT 1 step 6). Nothing was merged forward; DEV was not written.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `cab233bfdfdb3b84db1f648f00a2883d507685be`, origin/PROD `99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7`, `origin/DEV..origin/PROD` = 2 (`40845c7e`, `99d2b2a7`).
- Branch: `cand/dell1/prod-into-dev-fold`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean, fold merge `ac8b722a0b0f8d9549daceec1f1f5ad5512cc32c`. LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line: `TREE-EQUALS-DEV` printed. `git rev-list --count origin/DEV..HEAD` = 3: the fold merge plus the two PROD release merges it carries (the order's prose says "exactly the fold-back merge"; the three-commit list is `ac8b722a`, `99d2b2a7`, `40845c7e`).
- Register, run `--check-only` as the order directs: `APPROVAL-REGISTER result=REFUSED reason=dev-overlap overlap=106 commits=107` (rc=3). Per the order, no `--waive-overlap`, no register, no approval row, no merge-forward.
- Approval row id: none. Merge-forward result line: none.
- DEV head after, `ls-remote` read: `cab233bfdfdb3b84db1f648f00a2883d507685be` (unchanged).
- `origin/DEV..origin/PROD` after: 2 (unchanged). AC4 does NOT read 0.
- Ledger `amgt-resapp-bq2-prod-into-dev-fold-20261017`: HELD-PRE-APPLY, gate = the CTO's ruling on the refusal. Worktree removed; main portal tree on DEV.
