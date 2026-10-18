# PROMOTE RECEIPT -- AMGT_RESAPP bv-4 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-18

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bv-4.feature-promoted-to-prod-then-folded-back.md` (committed at `18832c313b`).
GO: broker msg 7855 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261018T0312Z_amgt-resapp-bv4-sa-promote-20261018_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for `aa207184` against origin/DEV `a2bdeb78`; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1` for row `dell1-20261018T030519Z-3155`.
- Builder output (verbatim):
  - `RELEASE-CHECK features=1 first_parent_commits=1 unapproved=0 ref=refs/heads/release/20261018T031234Z sha=ff6115661268`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-remaining-date-bypasses class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261018T030519Z-3155 pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261018T031234Z base=26d998f7f34015d3ad9d70360e9135ecf5d1ddfe head=ff61156612682ec15c67d79c92f6ce30a1d95a4f`
- Release branch: `release/20261018T031234Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `ff61156612682ec15c67d79c92f6ce30a1d95a4f`.
- Push state, as an `ls-remote` read: `ff61156612682ec15c67d79c92f6ce30a1d95a4f	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.240`, peeled with `^{commit}` = `ff61156612682ec15c67d79c92f6ce30a1d95a4f`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Five paths, all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit ff61156612682ec15c67d79c92f6ce30a1d95a4f`: one workflow on that sha, run `39092905765`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` ff611566. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read five `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run; DEV was not written. Step 7 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `a2bdeb78647919c8073d61fddbe6dbbcd51c6f0f`, origin/PROD `ff61156612682ec15c67d79c92f6ce30a1d95a4f`, `origin/DEV..origin/PROD` = 1 (`ff611566`, the round-115 release merge).
- Fold branch: `cand/dell1/prod-into-dev-fold-r115`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `39d439fbc1c969952c5f18ef99860cc08ca1bea9` (parents a2bdeb78, ff611566). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 2 (the fold merge plus the PROD release merge it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV a2bdeb78, PROD ff611566): **129** shas, 129 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R115.txt`. Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `1` (not `0`); NOT MET until step 7.
- Fold worktree removed; main portal tree on DEV.
