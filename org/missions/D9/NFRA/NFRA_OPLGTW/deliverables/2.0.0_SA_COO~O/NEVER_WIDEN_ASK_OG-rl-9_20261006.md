# Never-widen ask -- OG-rl-9, the r23 opal-gateway release on live 2c27f3a795 (round 23)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-06.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-9.gateway-release-r23.md`, with A1
  (@ee5e29b41d).
- **Spec:** CTO R29-R31 (`ledger/ROUND_ANALYSIS.round22.md` @a28c065593). Cut to `RELEASE_ORDER_FORM.md`.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-9.md` and `RL9_BEFORE.json`, worker commit
  `1cfe589511`.
- **Release sha the halves sign:** `ba27a074394bbaa08c7a7c720b4802edc2ecd72a`, branch `rel-nfra-oplgtw-r23`.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, because the dim_asset answers narrow and a route is added;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r23` (`/c/tmp/og-rel17`), two commits on live `2c27f3a795`: `91c00bdff1` (OG-q-8)
and `ba27a07439` (ETFS_RIVALS gw-1, A1). Host md5 reads 96 of 96 equal to live. The issuer's own reads at 21:5xZ:
- `git diff --name-only 2c27f3a795 ba27a07439` lists 6 files, all in the gateway tree;
- `git diff --stat ba27a07439 CLOUD -- infra/aws/ec2/opal-gateway` is one line, the CLOUD-only
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

**Rollback.** `/c/tmp/og-rb17` at `2c27f3a795`, 96 of 96 equal to the live S3 artifact. `.env` is unchanged in either
direction.

## 2. Blast radius -- what the act may touch

**Part 1: the dim_asset answers NARROW.**
- Before (measured read-only on live code as the real holder): query 2173 rows and download 2173 rows, each with 23
  blank-cusip rows; 2150 held; 0 non-blank unheld.
- After (the staged release bytes on the host, same holder): 2150 rows on both paths, 0 blank, 0 unheld, no duplicates.
- Per key: the blank-cusip key leaves; every non-blank held CUSIP stays.
- Rollback: redeploy `og-rb17`; the 23 rows return.

**Part 2: one ADDITIVE route, `/rivalfunds/{day}/audit`.**
- Before: not registered; the URL returns 404.
- After: a signed-in GET returns 200 when the day's `audit.html` exists (staged, 2026-10-06: 200, 1,337,761 bytes) and
  404 when it does not (2000-01-01). No identity: 401. The read policy is unchanged.
- Rollback: redeploy `og-rb17`; the route is gone.

**Unchanged:** the S41 grant (revision 3) and the state store (0 writes); `.env`; every other tool, dataset and route;
Terraform, IAM, the ALB, secrets, the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `2c27f3a795`.

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
2. Open ledger `nfra-oplgtw-gateway-release-r23`, with entry and sentinel committed first.
3. Run `r23_verify.sh before`.
4. Deploy from `/c/tmp/og-rel17` with `DEPLOY_BASE_REF=2c27f3a7958de0aa644374cdd08fc188a27e9e3f`.
5. Run `r23_verify.sh after` immediately (11 checks, including the two route arms and the floor).
6. Run the real-holder read on both paths (R30.3). On any failure: roll back from `og-rb17`.
7. Run `rl9.AC1`, `rl9.AC2` and `rl9.AC3` against their `<expect>`.
   - All three were exercised pre-GO, each with an expected-PASS form and a negative control.
   - `rl9.AC1` was corrected before GO: its host list now drops the source-only `tests/` files (rows Z-W28-S4, Z-S60).
   - `rl9.AC2` is `ga1.AC2`, unamended.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-06.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven.
- Both branches are named for each property in section 3, with each property's writers counted.
- The two limits (S5: the all-blank branch is fixture-only; S6: the route arms are in-process) are disclosed.
- My reads of release vs live (6 files) and release vs CLOUD (the runbook only) are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required).
