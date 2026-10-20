# PROMOTE_RECEIPT_CH4 -- AMGT_RESAPP.TO-AMGT-ch-4 (round 126)

Executor: 0.4.0_DT_ClientPlatform~H2. Date: 2026-10-20. Order:
`org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ch-4.two-security-analysis-features-promoted-to-prod-as-one-chosen-set-release.md`
(GO msg 8585; AMENDMENT 1 at eca0f444b0, msg 8588, read before the push). Ledger entry:
`amgt-resapp-ch4-sa-promote-20261020`.

## Approvals

    APPROVAL branch=cand/dell1/amgt-sa-reader-words state=APPROVED valid=yes row=dell1-20261019T224555Z-fbb9 by=1.0.0_SA_CTO~DELL1 head_sha=c8cd2da0ebbb3cb8b27c4b34d161118a2913083c commits=1 class=opal-internal box=dell1 pages=Security Analysis
    APPROVAL branch=cand/dell1/amgt-sa-status-words state=APPROVED valid=yes row=dell1-20261020T013211Z-07df by=1.0.0_SA_CTO~DELL1 head_sha=ebd7b44720f2a9210d91e247072cac21654282a0 commits=2 class=opal-internal box=dell1 pages=Security Analysis

`git ls-remote origin refs/heads/<b>` read before the build:

    c8cd2da0ebbb3cb8b27c4b34d161118a2913083c	refs/heads/cand/dell1/amgt-sa-reader-words
    ebd7b44720f2a9210d91e247072cac21654282a0	refs/heads/cand/dell1/amgt-sa-status-words

Both equal the head_sha named in the order.

## Release

PROD before (`git rev-parse --short=10 origin/PROD` after `git fetch origin DEV PROD`): `ba2c341279` (equals the order's cut value; no deviation).

Builder (`bash .tools/portal-release-build.sh --features cand/dell1/amgt-sa-reader-words,cand/dell1/amgt-sa-status-words`), lines verbatim:

    RELEASE-CHECK features=2 first_parent_commits=2 unapproved=0 ref=refs/heads/release/20261020T023043Z sha=e890aaa94fea
    PROMOTE-LIST branch=cand/dell1/amgt-sa-reader-words class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261019T224555Z-fbb9 pages=Security Analysis
    PROMOTE-LIST branch=cand/dell1/amgt-sa-status-words class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261020T013211Z-07df pages=Security Analysis
    PROMOTE-CLIENT-FACING count=0
    RELEASE result=READY reason=- branch=release/20261020T023043Z base=ba2c34127915f721ef034929b5a04feeb3838ade head=e890aaa94fea58506a6670cf663a38f67345617d ref=refs/heads/release/20261020T023043Z sha=e890aaa94fea

Release branch: `release/20261020T023043Z`. Promote by /prod-deploy: ephemeral worktree on PROD, `bun install` in the foreground, `git merge --ff-only` of the release branch, parity diff against the release branch empty (0 lines), `bun run typecheck` rc=0, plain `git push origin PROD` (VALGATE D-1 PASS no-op, pre-push typecheck passed): `ba2c3412..e890aaa9  PROD -> PROD`.

PROD after, as an `ls-remote` read (`git ls-remote origin refs/heads/PROD`):

    e890aaa94fea58506a6670cf663a38f67345617d	refs/heads/PROD

Tag: `portal-v2.1.246`, peeled (`git rev-parse portal-v2.1.246^{commit}`) = `e890aaa94f`, the PROD head. The previous tags peel to the previous heads (`portal-v2.1.245` to `ba2c341279`).

The release carries exactly these two features and no other candidate. The main portal tree stayed on DEV throughout; the worktree is removed and pruned.

Workspace submodule pointer (skill Step 6): not touched. The order's paths do not name `portal`, so no pointer commit was made here.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

- Route: /security-analysis
- Class: Opal-internal (staff-only); `PROMOTE-CLIENT-FACING count=0`

## CI

Read with `gh -R Opal-Capital/portal run list --branch PROD ...` listed by headSha, then `gh run list --repo Opal-Capital/portal --branch PROD --limit 1 --json conclusion,headSha,status`:

    [{"conclusion":"success","headSha":"e890aaa94fea58506a6670cf663a38f67345617d","status":"completed"}]

Run 39359584436, workflow `Deploy to Production`: status completed, conclusion success, on headSha `e890aaa94fea58506a6670cf663a38f67345617d`. It is the only workflow listed for that sha (the list held other shas' runs, so the empty-list trap does not apply).

## Fold-back (prepared)

Prepared only, per step 7; nothing registered, `portal-merge-forward.sh` not run, DEV not written.

- Fold branch: `cand/dell1/prod-into-dev-fold-r126`, cut from `origin/DEV` (`7d5ba57ec6`), local only (not on origin).
- Fold merge sha: `8de015fca648fc6edceec2fd2a5c3a2719683738` (`git merge --no-ff origin/PROD`, clean; message file written with the Write tool). PROD carried three merge commits DEV lacked: `e890aaa9`, `713ae4cb` (this release's two feature merges) and `ba2c3412` (the dell2 release merge of `cand/dell2/pkg-null-commentary`).
- Proof 1: `git diff --quiet origin/DEV HEAD && echo TREE-EQUALS-DEV` printed `TREE-EQUALS-DEV`.
- Proof 2: `git rev-list --count origin/DEV..HEAD` printed `4`.
- Overlap: `git rev-list origin/PROD..origin/DEV`, measured after the promote and a fetch (DEV `7d5ba57ec6`, PROD `e890aaa94f`): 153 shas, written to `FOLDBACK_OVERLAP_SHAS_R126.txt` in this folder.
- AC4 (`git rev-list --count origin/DEV..origin/PROD`) reads `3` after the promote: not yet met, as the amendment records, until the fold-back lands.

STOPPED here as ordered: awaiting the issuer's step-8 amendment with the CTO's named waiver. (Step 8 followed; see below.)

## Fold-back (landed)

Step 8 of AMENDMENT 2 (bf2a23b34d, GO msg 8592), under the CTO's one-time named waiver `org/missions/D5/AMGT/AMGT_RESAPP/ledger/CTO_WAIVER_FOLDBACK_DEV_OVERLAP_R126_20261020.md` (@b6328c50dd). Ledger entry: `amgt-resapp-ch4-prod-into-dev-fold-20261020`.

(a) Re-measured after a fetch, before registering: overlap `git rev-list origin/PROD..origin/DEV | wc -l` = 153, DEV `7d5ba57e`, PROD `e890aaa9`; the sorted set equals `FOLDBACK_OVERLAP_SHAS_R126.txt`.

(b) Register, `--check-only` first:

    APPROVAL-REGISTER result=OK row=- head_sha=8de015fca648fc6edceec2fd2a5c3a2719683738 commits=154 check-only=yes waived=153

then once, without it:

    APPROVAL-REGISTER result=OK row=dell1-20261020T025056Z-cefb head_sha=8de015fca648fc6edceec2fd2a5c3a2719683738 commits=154 waived=153
    ADDED id=dell1-20261020T025056Z-cefb kind=approval

Row id: `dell1-20261020T025056Z-cefb`.

(c) Approval, as read by `python .tools/open-calls.py approval-status --branch cand/dell1/prod-into-dev-fold-r126`:

    APPROVAL branch=cand/dell1/prod-into-dev-fold-r126 state=APPROVED valid=yes row=dell1-20261020T025056Z-cefb by=1.0.0_SA_CTO~DELL1 head_sha=8de015fca648fc6edceec2fd2a5c3a2719683738 commits=154 class=opal-internal box=dell1 pages=none

(d) Immediately before the merge-forward, after a fetch (DEV `7d5ba57e`, PROD `e890aaa9`, overlap 153): `git diff --quiet origin/DEV cand/dell1/prod-into-dev-fold-r126 && echo TREE-EQUALS-DEV` printed

    TREE-EQUALS-DEV

(e) `bash .tools/portal-merge-forward.sh cand/dell1/prod-into-dev-fold-r126 --push`, run alone, result line:

    MERGE-FORWARD branch=cand/dell1/prod-into-dev-fold-r126 result=MERGED reason=- dev_before=7d5ba57ec6c611e7fa16166a8f05d480578046e6 dev_after=84b680871fbe1542a45fa9babbb94ed15df3ee2d pushed=yes merge=84b680871fbe1542a45fa9babbb94ed15df3ee2d

Gate lines from the same run: `PASS 84b680871f route=A Merge cand/dell1/prod-into-dev-fold-r126 into DEV (approved feature)`; `DEV-PUSH-GATE result=ADMITTED reason=- commits=1`.

DEV head after, as an `ls-remote` read (`git ls-remote origin DEV`):

    84b680871fbe1542a45fa9babbb94ed15df3ee2d	refs/heads/DEV

DEV..PROD count after a fetch (`git rev-list --count origin/DEV..origin/PROD`): `0`. AC4 now reads `0`.
