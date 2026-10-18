# PROMOTE RECEIPT -- AMGT_RESAPP cb-3 -- 0.4.0_DT_ClientPlatform~H2 -- 2026-10-18

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-cb-3.feature-merged-forward-promoted-to-prod-then-folded-back.md` (issued at `eec0e7b329`).
GO: broker msg 8171 from `2.0.0_SA_COO~R1` (acked). Ledger: `org/critical_paths/change_management/20261018T1724Z_amgt-resapp-cb3-sa-promote-20261018_deploy_completion.md`.

## Merge-forward

- Step 1: `approval-status` read `APPROVAL branch=cand/dell1/amgt-sa-ceo-three-states state=APPROVED valid=yes row=dell1-20261018T171501Z-a713 by=1.0.0_SA_CTO~DELL1 head_sha=43762e0d999d3b67a7a955dc16ac638bbfcdea88 commits=1 class=opal-internal`; `git -C portal rev-parse cand/dell1/amgt-sa-ceo-three-states` read `43762e0d999d3b67a7a955dc16ac638bbfcdea88`.
- Feature branch push (step 2), `ls-remote` read: `43762e0d999d3b67a7a955dc16ac638bbfcdea88	refs/heads/cand/dell1/amgt-sa-ceo-three-states` (on origin).
- DEV before (read after `git fetch origin DEV PROD`): `3a7791c107ce891af3eaf2a22c390893f80e5003` (equal to the order's cut; no deviation).
- Merge-forward result line (step 3): `MERGE-FORWARD branch=cand/dell1/amgt-sa-ceo-three-states result=MERGED reason=- dev_before=3a7791c107ce891af3eaf2a22c390893f80e5003 dev_after=522985eff2d65234f89181c3f2c986f4731d04b6 pushed=yes merge=522985eff2d65234f89181c3f2c986f4731d04b6` (DEV-PUSH-GATE result=ADMITTED; `merge=` is a sha, not `-`).
- After a fetch: `IN-DEV` printed for `43762e0d`; DEV after, `ls-remote` read: `522985eff2d65234f89181c3f2c986f4731d04b6	refs/heads/DEV`.
- Gate note (no override used): the push hook (`.tools/hooks/never-rules-gate.sh`, NFRA_DEVPLN S03) denied the feature-branch push twice with "a DT seat no longer pushes portal DEV" -- first from the main portal tree whose HEAD is DEV, then from the feature branch's own worktree (`C:/dev/wk-resapp-523/portal`, HEAD the feature branch) when the same command line also named `git -C C:/dev/ajb_workspace/portal` for a read. The same push run ALONE from that worktree was admitted and succeeded. Nothing was overridden; no `# never-override` was appended.

## Release

- Builder output (verbatim):
  - `RELEASE-CHECK features=1 first_parent_commits=1 unapproved=0 ref=refs/heads/release/20261018T172512Z sha=d729ee6d8456`
  - `PROMOTE-LIST branch=cand/dell1/amgt-sa-ceo-three-states class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261018T171501Z-a713 pages=Security Analysis`
  - `PROMOTE-CLIENT-FACING count=0`
  - `RELEASE result=READY reason=- branch=release/20261018T172512Z base=ff61156612682ec15c67d79c92f6ce30a1d95a4f head=d729ee6d84565bfa4ce508ddf199d40ac0851482`
- Release branch: `release/20261018T172512Z`, fast-forwarded onto PROD in an ephemeral worktree; parity diff 0 lines.
- PROD head before: `ff61156612682ec15c67d79c92f6ce30a1d95a4f` (equal to the order's cut head; `ls-remote` re-read just before the push; no deviation from the order's numbers).
- PROD head after: `d729ee6d84565bfa4ce508ddf199d40ac0851482`.
- Push state, as an `ls-remote` read: `d729ee6d84565bfa4ce508ddf199d40ac0851482	refs/heads/PROD` (on origin).
- Pre-push gates passed: VALGATE D-1 (no-op), `tsc -b --noEmit`.
- Tag `portal-v2.1.241`, peeled with `^{commit}` = `d729ee6d84565bfa4ce508ddf199d40ac0851482`.
- Main portal tree: back on DEV (verified); both worktrees removed and pruned.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`
- Seven paths, all under `src/pages/SecurityAnalysis/`. No client-facing page.

## CI

Read by headSha with `gh run list --repo Opal-Capital/portal --commit d729ee6d84565bfa4ce508ddf199d40ac0851482`: one workflow on that sha, run `39149629746`, "Deploy to Production", status completed, conclusion success. Branch read `gh run list --repo Opal-Capital/portal --branch PROD --limit 1`: `status: completed`, `conclusion: success`, `headSha` d729ee6d. Repo positive control: `gh repo view Opal-Capital/portal` read `Opal-Capital/portal`.

- Status as read: completed
- Conclusion as read: success

AC1 read seven `EQUAL` lines, zero `DIFFERS`.

## Surprises

None filed. The hook behaviour above is recorded in the Merge-forward section; it blocked nothing in the end.

## Fold-back (prepared)

STATUS: PREPARED ONLY, as the order directs. No approval row was registered and `portal-merge-forward.sh` was NOT run for the fold-back; DEV was not written by it. Step 9 waits on the CTO's named waiver and the issuer's amendment.

- Start state (after `git fetch origin DEV PROD`): origin/DEV `522985eff2d65234f89181c3f2c986f4731d04b6`, origin/PROD `d729ee6d84565bfa4ce508ddf199d40ac0851482`, `origin/DEV..origin/PROD` = 1 (`d729ee6d`, the round-121 release merge).
- Fold branch: `cand/dell1/prod-into-dev-fold-r121`, cut from origin/DEV in a temporary worktree, `git merge --no-ff origin/PROD` clean. Fold merge sha: `d8473c5b46344e31e96a7b0b65c3d1a4584c14ed` (parents 522985ef, d729ee6d). LOCAL only (`ls-remote` of the branch on origin reads empty).
- Proof line 1: `TREE-EQUALS-DEV` printed (`git diff --quiet origin/DEV HEAD`).
- Proof line 2: `git rev-list --count origin/DEV..HEAD` = 2 (the fold merge plus the PROD release merge it carries).
- Overlap shas: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV 522985ef, PROD d729ee6d): **132** shas, 132 unique, all 40-hex, written to `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.4.0_DT_ClientPlatform~H2/FOLDBACK_OVERLAP_SHAS_R121.txt` (the order's cut read 131 before this feature's own DEV merge). Exactly one commit on the fold branch lies outside that set (the fold merge).
- AC4 as read now (guarded command): `1` (not `0`); NOT MET until step 9.
- Fold worktree removed; main portal tree on DEV.
