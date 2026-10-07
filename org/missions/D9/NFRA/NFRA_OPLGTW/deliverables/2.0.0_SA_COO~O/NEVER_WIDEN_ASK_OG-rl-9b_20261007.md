# Never-widen ask -- OG-rl-9 RE-CUT (A2), the r23 opal-gateway release on live 9d3e2eb3fc (round 23)

This file SUPERSEDES `NEVER_WIDEN_ASK_OG-rl-9_20261006.md` (@406becb990). Live moved to `9d3e2eb3fc` under the r24 hotfix
(OG-rl-10, 2026-10-06T23:59:57Z), so the halves signed on `ba27a07439` are void and all three are re-asked here. The
release's content is unchanged: the same six files, the same two cells.

By: `2.0.0_SA_COO~O` (issuer), 2026-10-07.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-9.gateway-release-r23.md`, with A1
  (@ee5e29b41d) and A2 (@e27046f80f).
- **Spec:** CTO R29-R31 (`ledger/ROUND_ANALYSIS.round22.md` @a28c065593). Cut to `RELEASE_ORDER_FORM.md`.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-9b.md` and `RL9_BEFORE.json`, worker commit
  `dd6c4b5598`.
- **Release sha the halves sign:** `7d65a28db026a44d7199ffe52a97e44952df75a1`, branch `rel-nfra-oplgtw-r23b`.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, because the dim_asset answers narrow and a route is added;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r23b` (`/c/tmp/og-rel19`), ONE commit `7d65a28db0` on live `9d3e2eb3fc`, carrying
OG-q-8 and ETFS_RIVALS gw-1 (A1). Host md5 reads 96 of 96 equal to live. The issuer's own reads at 01:3xZ:
- `git diff --name-only 9d3e2eb3fc 7d65a28db0` lists 6 files, all in the gateway tree;
- `git diff --stat 7d65a28db0 CLOUD -- infra/aws/ec2/opal-gateway` is one line, the CLOUD-only
  `runbooks/SCHWAB_PILOT_RUNBOOK.md`.

| File | Ships to the host | Change |
|---|---|---|
| `app/integrations/schwab/integration.py` | yes | R29: `position_cusips` drops None and whitespace-only values (one expression) |
| `app/rivalfunds_view.py` | yes | adds `audit_key` and `rivalfunds_audit` |
| `app/server.py` | yes | ONE Route line, `/rivalfunds/{day}/audit`, before `/rivalfunds/{day}` |
| `app/tests/test_rivalfunds_view.py` | yes | tests |
| `tests/test_schwab_q8_blank_cusip.py` | no | tests |
| `tests/test_principal_cutover.py` | no | ROUTE_CLASS declares the new route |

**Tests (72 files, each in its own process):** 601 passed and 7 failed. The same 7 ids fail on live, so none is new.
**R21 (a route is added):** `test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed.

**Rollback.** `/c/tmp/og-rb18` at `9d3e2eb3fc`, 96 of 96 equal to the live S3 artifact. `.env` is unchanged in either
direction.

## 2. Blast radius -- what the act may touch

**Part 1: the dim_asset answers NARROW.**
- Before (measured read-only on live code as the real holder): query 2173 rows and download 2173 rows, each with 23
  blank-cusip rows; 2150 held; 0 non-blank unheld.
- After (the staged release bytes on the host, same holder): 2150 rows on both paths, 0 blank, 0 unheld, no duplicates.
- Per key: the blank-cusip key leaves; every non-blank held CUSIP stays.
- Rollback: redeploy `og-rb18`; the 23 rows return.

**Part 2: one ADDITIVE route, `/rivalfunds/{day}/audit`.**
- Before: not registered; the URL returns 404.
- After: a signed-in GET returns 200 when the day's `audit.html` exists (staged, 2026-10-06: 200, 1,337,761 bytes) and
  404 when it does not (2000-01-01). No identity: 401. The read policy is unchanged.
- Rollback: redeploy `og-rb18`; the route is gone.

**Unchanged:** the S41 grant (revision 3) and the state store (0 writes); `.env`; every other tool, dataset and route;
Terraform, IAM, the ALB, secrets, the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `9d3e2eb3fc`.

**DRAIN-BACK (R16).** CLOUD already carries the release's six files, so the step is a check (`rl9.AC1`).

## 3. The named properties and their writers

**(a) Which dim_asset rows a holder receives.**
- Writers of the held set, N = 1: `integration.py` `_asset_holdings` (CHANGED). It feeds 3 call sites of
  `qualify_asset_plan`: query, download pre-check and export.
- Expected: the live holder gets exactly its 2150 held CUSIPs on both paths.
- Other branch: a holder whose every held position is blank is refused `asset_read_denied_unqualified`. This branch
  rests on the fixture test `test_ogq8_ac04` only: 0 of 6337 accounts hold only blank cusips, so live data cannot
  build it (row Z-W28-S5).
- Failure branch: a held non-blank CUSIP missing, or a blank row still present; roll back.

**(b) What `/rivalfunds/{day}/audit` returns.**
- Writers, N = 1: `rivalfunds_view.rivalfunds_audit` (NEW), reading the day's `audit.html` from the published prefix.
- Expected: 200 with the page bytes, or 404 with its own body.
- Failure branch: a 5xx, a 200 on a day with no object, or the `/rivalfunds/{day}` page changing; roll back.
- Limit (row Z-W28-S6): the route arms run in-process on the host, not through the ALB. The 200 arm needs the
  2026-10-06 `audit.html` to exist at Phase B.

**(c) Every other route.**
- Writers: unchanged.
- Expected: the floor holds (`rl4.AC1` on the 51-name baseline, `ht.AC2` at 51 keys).

## 4. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live; if it moved, re-cut.
2. Ledger `nfra-oplgtw-gateway-release-r23` is already OPEN (22:03Z, no act behind it). A line recording the re-cut and
   the new release sha is added to the entry and committed first.
3. Run `r23b_verify.sh before`.
4. Deploy from `/c/tmp/og-rel19` with `DEPLOY_BASE_REF=9d3e2eb3fce3ceabbf06f6c1819451894291be05`, by the issuer-serial
   halt-gate route that deployed r24 (row Z-S62).
5. Run `r23b_verify.sh after` immediately (11 checks, including the two route arms and the floor).
6. Run the real-holder read on both paths (R30.3). On any failure: roll back from `og-rb18`.
7. Run `rl9.AC1`, `rl9.AC2` and `rl9.AC3` against their `<expect>`.
   - All three were exercised pre-GO, each with an expected-PASS form and a negative control.
   - `rl9.AC1` reads the new live sha (A2) and drops the source-only `tests/` files (rows Z-W28-S4, Z-S60).
   - Host runs go strictly one at a time (row Z-W28-S9: two overlapping runs share one scratch directory).
   - `rl9.AC2` is `ga1.AC2`, unamended.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-07.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven.
- Both branches are named for each property in section 3, with each property's writers counted.
- The two limits (S5: the all-blank branch is fixture-only; S6: the route arms are in-process) are disclosed.
- My reads of release vs live (6 files) and release vs CLOUD (the runbook only) are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required).
