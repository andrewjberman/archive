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

STATUS: DONE under AMENDMENT 2 (the CTO's one-time named waiver, `org/missions/D5/AMGT/AMGT_RESAPP/ledger/CTO_WAIVER_FOLDBACK_DEV_OVERLAP_20261017.md`). First attempt stopped at the register (`result=REFUSED reason=dev-overlap overlap=106 commits=107`), reported, ruled, resumed.

- Branch: `cand/dell1/prod-into-dev-fold`, cut from origin/DEV `cab233bfdfdb3b84db1f648f00a2883d507685be`, `git merge --no-ff origin/PROD` clean, fold merge `ac8b722a0b0f8d9549daceec1f1f5ad5512cc32c` (parents cab233bf, 99d2b2a7).
- Proof line: `TREE-EQUALS-DEV`, printed after the first merge and again immediately before the merge-forward. `git rev-list --count origin/DEV..HEAD` = 3 (the fold merge plus the two PROD release merges `40845c7e` and `99d2b2a7` it carries).
- Re-count before registering: `git rev-list origin/PROD..origin/DEV | wc -l` = 106; the waiver's 106 shas equal that set (`cmp` identical).
- Register `--check-only` with the waiver: `APPROVAL-REGISTER result=OK row=- head_sha=ac8b722a0b0f8d9549daceec1f1f5ad5512cc32c commits=107 check-only=yes waived=106`.
- Approval row id: `dell1-20261017T163932Z-f936`, opal-internal, pages none; `approval-status` read `state=APPROVED valid=yes by=1.0.0_SA_CTO~DELL1 head_sha=ac8b722a`.
- Merge-forward result line: `MERGE-FORWARD branch=cand/dell1/prod-into-dev-fold result=MERGED reason=- dev_before=cab233bfdfdb3b84db1f648f00a2883d507685be dev_after=d8df08e44092eb21d022adde9e672451d9d19d05 pushed=yes merge=d8df08e44092eb21d022adde9e672451d9d19d05` (DEV-PUSH-GATE result=ADMITTED).
- DEV head after, `ls-remote` read: `d8df08e44092eb21d022adde9e672451d9d19d05	refs/heads/DEV`. DEV's tree is unchanged (`6cb1b95163a2` before and after; `git diff cab233bf origin/DEV` empty).
- `git rev-list --count origin/DEV..origin/PROD` after a fetch: 0 (AC4).
- Worktree removed and pruned; main portal tree on DEV. Ledger `amgt-resapp-bq2-prod-into-dev-fold-20261017` CLOSED.
