# PROMOTE RECEIPT -- AMGT_RESAPP bs-5 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-17

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bs-5.price-currency-rule-promoted-to-prod-then-folded-back.md` (committed at `a0cbebceb7`).
GO: broker msgs 7717 and 7719 from `2.0.0_SA_COO~R1` (both acked; 7719 only restates the commit and the `PROMOTE_SA` workstream tag). Ledger: `org/critical_paths/change_management/20261017T1948Z_amgt-resapp-bs5-sa-promote-20261017_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for `937f15a0` against origin/DEV `9fa63689`; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1` for row `dell1-20261017T194202Z-32d8`.
- Builder output (verbatim):
  - `RELEASE-CHECK features=1 first_parent_commits=1 unapproved=0 ref=refs/heads/release/20261017T194827Z sha=856fb37b785c`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-price-currency-rule class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T194202Z-32d8 pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261017T194827Z base=932cea99e8cabffa7ca28d2d57aba1e923d4e591 head=856fb37b785c4b8a10190771410e3dfc9ac8e789`
- The census branch `cand/dell1/amgt-sa-pe-footer-census` (row 48c7) is NOT in this release, as the order directs (DEV only).
- Release branch: `release/20261017T194827Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `932cea99e8cabffa7ca28d2d57aba1e923d4e591` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `856fb37b785c4b8a10190771410e3dfc9ac8e789`.
- Push state, as an `ls-remote` read: `856fb37b785c4b8a10190771410e3dfc9ac8e789	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.237`, peeled with `^{commit}` = `856fb37b785c4b8a10190771410e3dfc9ac8e789`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Six paths, all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit 856fb37b785c4b8a10190771410e3dfc9ac8e789`: one workflow on that sha, run `39064168223`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` 856fb37b. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read six `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run; DEV was not written. Step 7 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `9fa63689a8e9f2d0c627735b0d6e5396df1ff9c2`, origin/PROD `856fb37b785c4b8a10190771410e3dfc9ac8e789`, `origin/DEV..origin/PROD` = 1 (`856fb37b`, the round-112 release merge).
- Fold branch: `cand/dell1/prod-into-dev-fold-r112`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `118ede74b270f8c6fe77754c8ce8a180a047e1b5` (parents 9fa63689, 856fb37b). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 2 (the fold merge plus the PROD release merge it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV 9fa63689, PROD 856fb37b): **116** shas, 116 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R112.txt`. Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `1` (not `0`); NOT MET until step 7.
- Fold worktree removed; main portal tree on DEV.
