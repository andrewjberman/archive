# PROMOTE RECEIPT -- AMGT_RESAPP br-5 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-17

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-br-5.three-features-promoted-to-prod-then-folded-back.md`
GO: broker msg 7699 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261017T1816Z_amgt-resapp-br5-sa-promote-20261017_deploy_completion.md`.

## Release

- Step 1: `IN-DEV` printed for the three heads (`164c9fd5`, `3eb64c26`, `259da4c4`) against origin/DEV `990164ae`; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1` for rows `dell1-20261017T180053Z-887f`, `dell1-20261017T180746Z-f0a9`, `dell1-20261017T180918Z-b4db`.
- Builder output (verbatim):
  - `RELEASE-CHECK features=3 first_parent_commits=3 unapproved=0 ref=refs/heads/release/20261017T181705Z sha=932cea99e8ca`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-changed-object-cells class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T180053Z-887f pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-pe-footer-words class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T180746Z-f0a9 pages=Security Analysis`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-peers-currency class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261017T180918Z-b4db pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261017T181705Z base=99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7 head=932cea99e8cabffa7ca28d2d57aba1e923d4e591`
- Release branch: `release/20261017T181705Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `99d2b2a70cc1b5d39705d89a38312a4b8f7c3fa7` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `932cea99e8cabffa7ca28d2d57aba1e923d4e591`.
- Push state, as an `ls-remote` read: `932cea99e8cabffa7ca28d2d57aba1e923d4e591	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.236`, peeled with `^{commit}` = `932cea99e8cabffa7ca28d2d57aba1e923d4e591`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Thirteen paths (4, 2 and 7), all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit 932cea99e8cabffa7ca28d2d57aba1e923d4e591`: one workflow on that sha, run `39057551567`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` 932cea99. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read thirteen `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run; DEV was not written. Step 7 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `990164aecc45c314dfe76d36cfb80de354d35760`, origin/PROD `932cea99e8cabffa7ca28d2d57aba1e923d4e591`, `origin/DEV..origin/PROD` = 3 (`44233f1d`, `7b317be8`, `932cea99`, the round-111 release merges).
- Fold branch: `cand/dell1/prod-into-dev-fold-r111`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `f3aa4207de45d8f19c36b2c84359aa3571af3d9e` (parents 990164ae, 932cea99). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 4 (the fold merge plus the three PROD release merges it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV 990164ae, PROD 932cea99): **111** shas, 111 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R111.txt`. Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `3` (not `0`); NOT MET until step 7.
- Fold worktree removed; main portal tree on DEV.

## Fold-back (landed)

STATUS: DONE under AMENDMENT 1 step 7 (the CTO's one-time named waiver, `org/missions/D5/AMGT/AMGT_RESAPP/ledger/CTO_WAIVER_FOLDBACK_DEV_OVERLAP_R111_20261017.md`, for `cand/dell1/prod-into-dev-fold-r111` at fold merge `f3aa4207` only).

- Re-count before registering: `git rev-list origin/PROD..origin/DEV | wc -l` = 111; `git rev-parse origin/DEV` = `990164aecc45c314dfe76d36cfb80de354d35760` (unchanged); origin/PROD `932cea99`. The waiver's 111 shas equal the live set (`cmp` identical).
- Register `--check-only` output: `APPROVAL-REGISTER result=OK row=- head_sha=f3aa4207de45d8f19c36b2c84359aa3571af3d9e commits=112 check-only=yes waived=111`.
- Registered: `APPROVAL-REGISTER result=OK row=dell1-20261017T182833Z-e870 head_sha=f3aa4207de45d8f19c36b2c84359aa3571af3d9e commits=112 waived=111` (opal-internal, pages none). Approval: `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1`.
- Proof line: `TREE-EQUALS-DEV`, re-printed in the same call, immediately before the merge-forward.
- Merge-forward result line: `MERGE-FORWARD branch=cand/dell1/prod-into-dev-fold-r111 result=MERGED reason=- dev_before=990164aecc45c314dfe76d36cfb80de354d35760 dev_after=0f6dc96b0f1829713fc164f80cbf08ae5425c818 pushed=yes merge=0f6dc96b0f1829713fc164f80cbf08ae5425c818` (DEV-PUSH-GATE result=ADMITTED).
- DEV head after, `ls-remote` read: `0f6dc96b0f1829713fc164f80cbf08ae5425c818	refs/heads/DEV`. DEV's tree is unchanged (`16977dce708d` before and after; `git diff 990164ae origin/DEV` empty).
- `git -C portal rev-list --count origin/DEV..origin/PROD` after a fetch: **0** (AC4, guarded command; PROD `932cea99` is off `99d2b2a7`).
- Fold worktree removed and pruned; main portal tree on DEV. Ledger `amgt-resapp-br5-prod-into-dev-fold-20261017` CLOSED.
