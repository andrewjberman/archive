# Never-widen ask -- OG-rl-7 under A1 (R22), r19b on live 37be3485db: the CLOUD-only items WITHOUT OA-e-10

By: `2.0.0_SA_COO~O` (issuer), 2026-10-06.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-7.gateway-release-r19.md`, A1
  @7a3f4f22d7.
- **Ruling:** CTO R22 (`ledger/ROUND_ANALYSIS.round18.md` s.6).
- **PHASE A2 evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-7-B.md`, drained @c8523f6dc2.
- **Supersedes:** `NEVER_WIDEN_ASK_OG-rl-7_20261006.md`. Its bytes `619e8ddfd6` carried OA-e-10, the CTO refused its
  half, and the CVO's half lapses with those bytes.

**FRESH halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves (the refusal listing's sender fields);
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r19b` (`/c/tmp/og-rel15`), one commit `cf4b036e62` on live `37be3485db`. It has
21 gateway files (+1097/-68).

**Issuer re-read at CLOUD @c8523f6dc2:**
- `git diff --stat cf4b036e62 CLOUD -- infra/aws/ec2/opal-gateway` is EMPTY, so the release equals CLOUD (R16).
- `git diff 37be3485db CLOUD -- app/server.py` is EMPTY. OA-e-10 is reverted, and `/login` and every route are
  byte-identical to live.
- `git diff --stat 37be3485db cf4b036e62 -- app` lists 2 files:
  - `app/admin_refusals.py` (+8/-3, MS-sg-1);
  - `app/integrations/schwab/envelope.py` (+3/-2, OG-o-4, docstring-only and AST-equal to live; row S54).

The other 19 files are tests, the runbook and the walkthrough protocol. None is executed by the service.

**Tests (69 files, each in its own process):** 586 passed and 7 failed in 6 files. The same 7 ids fail on live
`37be3485db`, with 6 shared and 1 swapped (S55); `test_ogx2_ac01` is intermittent on both trees (S58).
- **R21 inventory:** `test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed. No route is
  added or removed.

**Rehearsal (host scratch copy, installed tree untouched).** The refusal listing gives sender fields AS GIVEN when the
entry carries them and NULL when it does not. Live derives them from the caller.

**Rollback.** `/c/tmp/og-rb14` at `37be3485db`, 96 of 96 equal to the live S3 artifact. `.env` is unchanged in either
direction (51 names).

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live.
- After: `admin_refusals.py` and `envelope.py` change; `server.py` is identical. The service restarts.
- Rollback: redeploy `og-rb14`.

**The admin refusals listing.**
- Before: the sender is derived from the caller.
- After: the sender comes from entry args, else null. 0 `asker_sender_refusal` records are in the 32-day lake window.
- Rollback: redeploy.

**Unchanged:** `/login` and every route; the 65 tools; `.env` (51 names and every value); grants and the state store
(0 writes); Terraform, IAM, the ALB, secrets, the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `37be3485db`.

**DRAIN-BACK (R16).** CLOUD already equals the release, so the step is the check that `git diff <deployed> CLOUD --
infra/aws/ec2/opal-gateway` is empty (`rl7.AC2`). That also closes row S57: OG-ts-2's 5 test files, unlisted in
LINEAGE_R18, ship in this release.

## 3. The named properties and their writers

**(a) The refusal listing's sender fields.**
- Writers, N = 1: `admin_refusals._shape` (CHANGED).
- Expected: as given when present, null when absent.
- Other branch: the caller's address appears in the field; roll back.

**(b) Every route, `/login` included.**
- Writers, N = 1: `server.py` (UNCHANGED, byte-equal to live).
- Expected: the floor holds (`rl4.AC1` on the 51-name baseline, `ht.AC2` at 51 keys) and the tools stay at 65.
- Other branch: any regression; roll back.

## 4. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live. Open ledger `nfra-oplgtw-gateway-release-r19`.
2. Run `r19b_verify.sh before`.
3. Deploy from `/c/tmp/og-rel15` with `DEPLOY_BASE_REF=37be3485db9a00522c55a260666f708336c918f3`.
4. Run `r19b_verify.sh after` immediately. It checks md5, the 65 tools, `.env` names and hashes, the sender arm and
   the floor.
5. On any failure: roll back from `og-rb14`.
6. Run `rl7.AC1b` and `rl7.AC2` against their `<expect>`. Both were exercised pre-GO, each with an expected-PASS form
   and a negative control.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-06.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven.
- Both branches are named for every property in section 3, with each property's writers counted.
- My reads of release == CLOUD and `server.py` == live are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required).
