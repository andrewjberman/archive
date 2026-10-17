# PROMOTE RECEIPT -- AMGT_RESAPP bu-5 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-17

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bu-5.three-features-promoted-to-prod-then-folded-back.md` (committed at `2c1bd6e311`).
GO: broker msg 7778 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261017T2340Z_amgt-resapp-bu5-sa-promote-20261017_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for the three heads (`a3f2b727`, `9a8ef5e4`, `dac528b0`) against origin/DEV `d2d98f8f`; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1` for rows `dell1-20261017T233249Z-55a2`, `dell1-20261017T233313Z-5b5e`, `dell1-20261017T233315Z-c1c6`.
- Builder output (verbatim):
  - `RELEASE-CHECK features=3 first_parent_commits=3 unapproved=0 ref=refs/heads/release/20261017T234106Z sha=26d998f7f340`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-peers-subject-currency class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T233249Z-55a2 pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-page-dates-long-form class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T233313Z-5b5e pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-model-grid-scroll-cue class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T233315Z-c1c6 pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261017T234106Z base=d1bed0fbbce13db794e5f91b92452464394f8f3a head=26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`
- Release branch: `release/20261017T234106Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `d1bed0fbbce13db794e5f91b92452464394f8f3a` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`.
- Push state, as an `ls-remote` read: `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.239`, peeled with `^{commit}` = `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- 27 paths (3, 21 and 3), all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit 26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`: one workflow on that sha, run `39080069302`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` 26d998f7. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read 27 `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run; DEV was not written. Step 7 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `d2d98f8fe972c42126c39f2073b9e75f1232f46e`, origin/PROD `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`, `origin/DEV..origin/PROD` = 3 (`1cb8682d`, `32e3efb3`, `26d998f7`, the round-114 release merges).
- Fold branch: `cand/dell1/prod-into-dev-fold-r114`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `6d3286952f40f2941bda74dc5614f84c32053751` (parents d2d98f8f, 26d998f7). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 4 (the fold merge plus the three PROD release merges it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV d2d98f8f, PROD 26d998f7): **126** shas, 126 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R114.txt`. Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `3` (not `0`); NOT MET until step 7.
- Fold worktree removed; main portal tree on DEV.
