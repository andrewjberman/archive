# Never-widen ask -- OG-rl-6, the r17 opal-gateway release on live 4b6b823fae (round 17)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-05 ~02:xxZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-6.gateway-release-r17.md`, issued @3ae49bc24b.
- **Spec:** analysis round 16 section 4, item 2 (@1f439fe6aa); R13 (a) for the release-branch commit.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-6.md`, drained @33be896a10.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO).
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, because `dim_asset` downloads open.
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r17` (`/c/tmp/og-rel11`), HEAD `e91819e281`, one commit on live `4b6b823fae`. Host
md5 reads 94 of 94 equal to live (SSM 822b5abe). The commit touches 3 files:
- `app/integrations/schwab/integration.py` (108 lines in the diffstat);
- `tests/test_schwab_q7_asset_download.py` (new);
- `tests/test_schwab_rl5_asset_query.py` (restated).

Only `integration.py` changes service behaviour. `tests/conftest.py` stays at live's bytes, because it is outside the
release set (row Z-W15-S40).

**Issuer re-read, independent of the worker:**
- `git -C /c/tmp/og-rel11 diff --stat 4b6b823fae HEAD` lists exactly those 3 files. Nothing under
  `infra/aws/terraform`, and nothing in `deploy-to-ec2.sh`, the contract or the template.
- The release `integration.py` holds 0 `_asset_policy is None` guards (live has 2: `prepare_download` and
  `export_query`). The live-only `environ_with_external_ids` call is present.
- q-7's own checks PASS on CLOUD @fc70572578: `q7.AC1` 4 of 4; `q7.AC2` with guards 0, 3 call sites, 0 beyond the
  baseline.

**Rehearsal on the host, not installed (SSM 32d33e0a).** The release `integration.py` was staged in a scratch copy; the
installed tree and `.env` were untouched.
- The `dim_asset` download is OK and held-only: 49 returned, 0 unheld, discriminated as 49 held against a 2,160-CUSIP
  universe.
- An empty-holdings grant is REFUSED `asset_read_denied_unqualified`.
- The query's held set equals the download's.

**Rollback.** `/c/tmp/og-rb11` at `4b6b823fae`. Its 94 gateway files equal the live S3 artifact
`opal-gateway-4b6b823fae.tar.gz`.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `4b6b823fae`.
- After: `integration.py` changes. Test files are not executed by the service.
- Rollback: redeploy `/c/tmp/og-rb11` with `DEPLOY_BASE_REF` set to the release sha.

**Host `.env`.** Not changed; the template is untouched. The 50 key names are verified after the act.

**Served `dim_asset` download and export, the capability change.**
- Before: REFUSED `asset_policy_selection_unavailable` for every grant.
- After: a grant naming `dim_asset` gets only the CUSIPs its accounts hold in the same master/date position snapshot.
  A grant whose accounts hold nothing is REFUSED `asset_read_denied_unqualified`.
- Rollback: redeploy.

**Served `dim_asset` query.** Unchanged: the same held set as before.

**Unchanged:** the tool list (65); grants and the state store (0 writes); Terraform, IAM, the ALB, the instance, secrets,
the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `4b6b823fae`. Rollback reverts the manifest commit.

**Not in this release: `/yearinreview` (R14).** Its kit @0b6a5aff58 is not on origin CLOUD at the cut, so it rides the
next gateway release.

## 3. The named properties and their writers

**(a) Which CUSIPs a `dim_asset` download or export returns.**
- Writers, N = 4:
  - the download and export paths, now calling `qualify_asset_plan` (CHANGE);
  - `sem.qualify_asset_plan` (unchanged);
  - grants (unchanged);
  - the silver `dim_position` snapshot content (unchanged; CVO r16 Q1).
- Expected: `returned > 0`, `unheld_returned = 0`, held < universe.
- Other branch: any unheld CUSIP is a widening beyond C3; roll back at once.

**(b) An empty-holdings grant.**
- Writers, N = 1: `qualify_asset_plan`'s empty-set denial (unchanged code, newly reached on downloads).
- Expected: REFUSED `asset_read_denied_unqualified`.
- Other branch: served, which means an unrestricted list; roll back at once.

**(c) The `dim_asset` query.**
- Writers, N = 2: the query path, which q-7 refactored to share the holdings read, and `qualify_asset_plan`.
- Expected: OK, with the same held set as the download.
- Other branch: a different set or a refusal; roll back.

**(d) Who can download `dim_asset`.**
- Writers, N = 1: grants naming `dim_asset` (unchanged).
- r16's pre-act read found 1 live grant, and it names `dim_asset`.
- Expected: the pre-act read prints the count. Those holders gain downloads their grants already authorize; the act
  adds no authorization.
- Other branch: a download by a principal without a `dim_asset` grant is a defect; roll back.

## 4. Act and verify (PHASE B, from the order, steps 7-10)

1. Re-read live; if it moved, re-cut. Print the count of live grants naming `dim_asset`.
2. Open ledger `nfra-oplgtw-gateway-release-r17`, entry and sentinel first.
3. Run `rl6_verify.sh before`.
4. Deploy from `/c/tmp/og-rel11` with `DEPLOY_BASE_REF=4b6b823faec5288c714b70117fcd691239a2633f`.
5. Run `rl6_verify.sh after` immediately. It checks: md5, the 65 tools, the 50 key names, the download held-only check
   with its discriminator, the empty-holdings refusal, query equality, the floor `rl4.AC1` and `ht.AC2`.
6. On any failure or any unheld CUSIP: roll back from `/c/tmp/og-rb11`, re-verify, and close ROLLED BACK.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-05.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven equal to live.
- Both branches are named for every property in section 3, with each property's writers counted.
- My reads of the release diff and the guard count are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required: served output moves).
