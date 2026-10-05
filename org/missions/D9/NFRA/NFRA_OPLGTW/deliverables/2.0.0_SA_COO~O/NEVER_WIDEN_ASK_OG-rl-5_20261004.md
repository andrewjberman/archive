# Never-widen ask -- OG-rl-5, the r16 opal-gateway release on live af2d762970 (round 16, amendment A3)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-04 ~22:xxZ. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-5.gateway-release-r16.md` (issued @565223dd62,
amended A3 @68c5438a60). Spec: analysis round 15 item 2 (R9) and section 8 addendum R12 @261571c07e. PHASE A evidence:
`deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-5.md`, drained @2b8b20df7b.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO): R12 says this half names the blast radius at Phase B;
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: the act moves served output (snapshots go from 0 servable to servable, and `dim_asset`
  queries become servable);
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r16` (`/c/tmp/og-rel10`) HEAD `4b6b823fae`, two commits on live `af2d762970`.
Live is confirmed by host md5, 94 of 94 equal (SSM 922501dc):
- `95a7dccc4d`: OG-gr-3's R9 grain and R9a single-page fallback;
- `4b6b823fae`: A3, the contract whole, the deleted query-path guard, and the no-seam test.

**Census against live.** 10 files. Four of them ship and change service behaviour:
- `app/integrations/schwab/{query.py, datasets.json, integration.py}`;
- `deploy/NFRA_OPLGTW_CONTRACT.json`.

The rest are tests and the `org/standards` twin of the contract.

**Issuer re-read, independent of the worker (~21:5xZ):**
- The deploy contract is `cmp`-equal to CLOUD's `org/standards/NFRA_OPLGTW_CONTRACT.json` at 261571c07e. Against live,
  its diff is exactly the two `silver/dim_transaction/` prefixes.
- `integration.py` on the release keeps 2 of the 3 `_asset_policy is None` guards: `prepare_download` and
  `export_query`. Live has 3. The only one removed is on the query path (`:569-570`).

**Tests:**
- Release tree: 50 of 50 in step 2's set (including `test_ogq2_ac20` and `test_ogz2_ac08` 60/0), and the new file 2 of 2.
- Worker worktree: no failure beyond the CLOUD-HEAD baseline. One-process errors are listed in row Z-W15-S37.

**Census on the release contract, in memory on the host (SSM 71fca05f).** The domain is 24 marker dates per master,
of which 14 are qualified. 14 `dim_position` and 14 `dim_asset` snapshots are servable at each master, 56 of 56 in all,
with 0 lacking an R9 column and 0 blank.

**Rollback.** `/c/tmp/og-rb10` at `af2d762970`. Its artifact is 97 of 97 equal to the live S3 object.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `af2d762970`.
- After: the four shipped files above.
- Rollback: redeploy `/c/tmp/og-rb10` with `DEPLOY_BASE_REF` set to the release sha. Since OG-rl-4 the template reads
  the Tax identity host-side, so nothing is exported.

**Host `.env`.** Not changed; the template is untouched. The 50 key names are verified after the deploy.

**Served Schwab catalog, the capability change.**
- Before: 0 snapshots servable at either master (every closure day REJECTED_FOREIGN_DATASET).
- After: 14 qualified days per master servable for `dim_position` and `dim_asset`.
- Rollback: redeploy.

**`dim_position` rows paging.**
- Before: REFUSED `INCOMPLETE_SNAPSHOT`.
- After: a rows page is served on the R9 grain.
- Rollback: redeploy.

**`dim_asset` query.**
- Before: REFUSED `asset_policy_selection_unavailable`.
- After: served under the C3 holdings restriction, which returns only CUSIPs held by the grant's accounts.
- Rollback: redeploy.

**`dim_asset` download and export.** Unchanged: still REFUSED. This is the control.

**`dim_transaction`.** It becomes a data-readable prefix. Whether anyone reads it is decided by grants, which this act
does not write (see property e).

**Unchanged:** the tool list (65); grants and the state store (0 writes); Terraform, IAM, the ALB, the instance, secrets
and the template.

**Manifest.** `deployed_commit` moves; the previous value is `af2d762970`. Rollback reverts the manifest commit.

## 3. The named properties and their writers

**(a) Which snapshots the catalog serves.**
- Writers, N = 3:
  - the contract `data_prefixes` (CHANGES);
  - `catalog.py` membership (unchanged);
  - the closure-marker producer in S3 (unchanged).
- Expected: servable snapshots at both masters (in-memory census: 14 per master per dataset), 0 lacking.
- Other branch: still 0 servable, or any snapshot lacking an R9 column. Then `rl5.AC1` fails, so roll back.

**(b) `dim_position` paging.**
- Writers, N = 2: `datasets.json` grain and the `integration.py` R9a path (both change).
- Expected: the rows page is OK.
- Other branch: REFUSED. Roll back.

**(c) Which CUSIPs a `dim_asset` query returns.**
- Writers, N = 3:
  - the query path, now without the guard (CHANGES);
  - `sem.qualify_asset_plan` (the C3 restriction, unchanged);
  - grants (unchanged).
- Expected: `returned > 0`, and `unheld_returned = 0` against the grant's accounts' `dim_position` CUSIPs.
- Other branch: any unheld CUSIP is returned. That is a widening beyond C3, so roll back at once.

**(d) `dim_asset` download and export.**
- Writers, N = 1: the two retained guards (unchanged).
- Expected: REFUSED `asset_policy_selection_unavailable`.
- Other branch: served. Roll back at once.

**(e) Who reads `dim_transaction`.**
- Writers, N = 2: the contract prefix (CHANGES) and grants in the state store (unchanged; per PRD v1.7, every grant
  beyond the one authorized act needs Andrew's word).
- Expected: the Phase B pre-act re-read prints the count of live grants naming `dim_transaction`.
  - If the count is 0: nothing new is read.
  - If the count is N > 0: those N holders gain `dim_transaction` reads, which their grants already authorized. The act
    adds no authorization.
- Other branch: any `dim_transaction` read by a principal without such a grant. That is a defect, so roll back.

## 4. Act and verify (PHASE B, from the order, steps 7-10)

1. Re-read live; if it moved, re-cut.
2. Print the count of live grants naming `dim_transaction` (property e).
3. Open ledger `nfra-oplgtw-gateway-release-r16`, entry and sentinel committed first.
4. Run `rl5_verify.sh before`.
5. Deploy from `/c/tmp/og-rel10` with `DEPLOY_BASE_REF=af2d7629702528c050860314a7867d8ea0cecfbf`, through
   `safe-ec2-deploy.sh`.
6. Run `rl5_verify.sh after` immediately. It checks:
   - md5 equals the release bytes, including the contract;
   - the 65 tools and the 50 key names are unchanged;
   - paging pages are OK;
   - the served census;
   - the asset held-check;
   - the download control;
   - the floor checks `rl4.AC1` and `ht.AC2`.
7. On any failure: roll back from `/c/tmp/og-rb10`, re-verify, and close ROLLED BACK.

## 5. Halves

**COO: SIGNED, `2.0.0_SA_COO~O`, 2026-10-04.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven equal to live.
- Both branches are named for every property in section 3, and the writers of each are counted there.
- My reads of the contract bytes and the guard count are independent of the worker's.

**CTO: owed.**

**CVO: owed** (required, because served output moves).
