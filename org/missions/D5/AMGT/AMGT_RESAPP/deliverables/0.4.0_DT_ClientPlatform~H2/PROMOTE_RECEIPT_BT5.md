# PROMOTE RECEIPT -- AMGT_RESAPP bt-5 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-17

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bt-5.three-features-promoted-to-prod-then-folded-back.md` (committed at `20d492f238`).
GO: broker msg 7752 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261017T2156Z_amgt-resapp-bt5-sa-promote-20261017_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for the three heads (`c4e4f96a`, `4f8299bd`, `be136f28`) against origin/DEV `eea01c16`; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1` for rows `dell1-20261017T210225Z-5058`, `dell1-20261017T211106Z-3af9`, `dell1-20261017T215021Z-044d`.
- Builder output (verbatim):
  - `RELEASE-CHECK features=3 first_parent_commits=3 unapproved=0 ref=refs/heads/release/20261017T215619Z sha=d1bed0fbbce1`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-earnings-long-dates class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T210225Z-5058 pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-price-currency-trim class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T211106Z-3af9 pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-model-tooltip-last-rows class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T215021Z-044d pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261017T215619Z base=856fb37b785c4b8a10190771410e3dfc9ac8e789 head=d1bed0fbbce13db794e5f91b92452464394f8f3a`
- `cand/dell1/amgt-sa-model-layout-repairs` was never registered and is NOT in this release, as the order directs.
- Release branch: `release/20261017T215619Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `856fb37b785c4b8a10190771410e3dfc9ac8e789` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `d1bed0fbbce13db794e5f91b92452464394f8f3a`.
- Push state, as an `ls-remote` read: `d1bed0fbbce13db794e5f91b92452464394f8f3a	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.238`, peeled with `^{commit}` = `d1bed0fbbce13db794e5f91b92452464394f8f3a`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Ten paths (5, 2 and 3), all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit d1bed0fbbce13db794e5f91b92452464394f8f3a`: one workflow on that sha, run `39073112254`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` d1bed0fb. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read ten `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run; DEV was not written. Step 7 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `eea01c164b18846c523e36146761b605e2c4e41a`, origin/PROD `d1bed0fbbce13db794e5f91b92452464394f8f3a`, `origin/DEV..origin/PROD` = 3 (`03aa37cd`, `8b15e3d0`, `d1bed0fb`, the round-113 release merges).
- Fold branch: `cand/dell1/prod-into-dev-fold-r113`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `002681becf3819f24e6e97ca58b475d50b9d7d18` (parents eea01c16, d1bed0fb). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 4 (the fold merge plus the three PROD release merges it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV eea01c16, PROD d1bed0fb): **121** shas, 121 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R113.txt`. Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `3` (not `0`); NOT MET until step 7.
- Fold worktree removed; main portal tree on DEV.

## Fold-back (landed)

STATUS: DONE under AMENDMENT 1 step 7 (the CTO's one-time named waiver, `org/missions/D5/AMGT/AMGT_RESAPP/ledger/CTO_WAIVER_FOLDBACK_DEV_OVERLAP_R113_20261017.md`, for `cand/dell1/prod-into-dev-fold-r113` at fold merge `002681be` only).

- Re-count before registering: `git rev-list origin/PROD..origin/DEV | wc -l` = 121; `git rev-parse origin/DEV` = `eea01c164b18846c523e36146761b605e2c4e41a` (unchanged); origin/PROD `d1bed0fb`. The waiver's 121 shas equal the live set (`cmp` identical).
- Register `--check-only` output: `APPROVAL-REGISTER result=OK row=- head_sha=002681becf3819f24e6e97ca58b475d50b9d7d18 commits=122 check-only=yes waived=121`.
- Registered: `APPROVAL-REGISTER result=OK row=dell1-20261017T221039Z-a997 head_sha=002681becf3819f24e6e97ca58b475d50b9d7d18 commits=122 waived=121` (opal-internal, pages none). Approval: `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1`.
- Proof line: `TREE-EQUALS-DEV`, re-printed in the same call, immediately before the merge-forward.
- Merge-forward result line: `MERGE-FORWARD branch=cand/dell1/prod-into-dev-fold-r113 result=MERGED reason=- dev_before=eea01c164b18846c523e36146761b605e2c4e41a dev_after=eb2c7b20168ff32af6d45be1d9547a38aeaedfe7 pushed=yes merge=eb2c7b20168ff32af6d45be1d9547a38aeaedfe7` (DEV-PUSH-GATE result=ADMITTED).
- DEV head after, `ls-remote` read: `eb2c7b20168ff32af6d45be1d9547a38aeaedfe7	refs/heads/DEV`. DEV's tree is unchanged (`f6b6dd55dfdd` before and after; `git diff eea01c16 origin/DEV` empty).
- `git -C portal rev-list --count origin/DEV..origin/PROD` after a fetch: **0** (AC4, guarded command; PROD `d1bed0fb` is off `856fb37b`).
- Fold worktree removed and pruned; main portal tree on DEV. Ledger `amgt-resapp-bt5-prod-into-dev-fold-20261017` CLOSED.
