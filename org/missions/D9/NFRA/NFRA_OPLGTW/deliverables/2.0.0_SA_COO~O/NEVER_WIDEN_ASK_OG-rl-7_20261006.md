# Never-widen ask -- OG-rl-7, the r19 opal-gateway release on live 37be3485db (round 19)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-06.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-7.gateway-release-r19.md`, issued
  @9703690791.
- **Spec:** analysis round 18 s.4 item 2 (@b397c851c0), under R16 and R21. Cut to `RELEASE_ORDER_FORM.md`.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-7.md` and `RL7_LOGIN.json`, drained
  @cc230fab61.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, because `/login` narrows;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 0. ONE INSTRUMENT DEVIATION FOR BOTH HALVES TO ACCEPT OR REFUSE (rows Z-W15-S52 ARMED, S53)

R16 asks for the `/login` admit lists "from 30 days of live audit". The audit lake CANNOT see `/login`: `login()` and
the guard write no audit record for the route. 97,430 lake records across 58 shapes hold none, by construction.

The worker used the host's access journal instead. It found **0 bare `/login` requests in 257,393 access-log lines,
32 of 32 days** (2026-09-05..2026-10-06). A journal line names no identity, so the journal proves NO USE, not "no
outsider". With 0 uses, the outsider set is empty: no identity used `/login` in the window, so none falls outside the
configured set.

Row S53: the host holds email-keyed token caches for three opalinvest.com identities (alyssa, opalbloomberg, one more),
last written 2026-09-17.
- None of them shows `/login` use or `needs_login` in the window.
- After the release, `/login` can no longer re-mint them.
- That is the intended fail-closed narrowing of OA-e-10. Nobody has used it in 32 days.

**Issuer reading:** the precondition holds on the journal, with the narrower claim, "no `/login` use", stated. S52
(the lake's blind spot for `/login`) is routed to the round-19 analysis as an audit-coverage item. It is not a
release blocker. A half that requires an identity-bearing instrument refuses, and names it.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r19` (`/c/tmp/og-rel14`), one commit `619e8ddfd6` on live `37be3485db`. Host md5
reads 96 of 96 equal to live. The commit has 23 gateway files, and its gateway subtree EQUALS CLOUD @cc230fab61: the
issuer's `git diff --stat 619e8ddfd6 CLOUD -- infra/aws/ec2/opal-gateway` is empty.

Behaviour lives in 3 app files (the issuer's `diff --stat 37be3485db..619e8ddfd6 -- app`):

| File | Change | Author |
|---|---|---|
| `app/server.py` | +18/-2 | OA-e-10 `/login` narrowing; hunks equal 8ed37b3266's |
| `app/admin_refusals.py` | +8/-3 | MS-sg-1 |
| `app/integrations/schwab/envelope.py` | +3/-2 | OG-o-4, docstring-only and AST-equal to live (row S54) |

The other 20 files are tests, the runbook and the walkthrough protocol. None ships to the host except as files the
service does not execute.

**Tests.** 70 test files ran, each in its own process: 588 passed and 7 failed in 6 files. Live fails 7 in the same 6
files, with 6 of 7 ids identical and 1 swapped (row S55).
- `test_login_retire.py` and `test_admin_refusals.py` pass.
- **R21 inventory:** `test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed. The release
  adds and removes no route.

**Rehearsal on the host (scratch copy; the installed tree untouched).**
- The configured identity gets the consent redirect.
- An unconfigured identity gets 403.
- With both settings empty, everyone gets 403.
- Sender fields are null when the entry carries none.

**Rollback.** `/c/tmp/og-rb14` at `37be3485db`, equal to the live S3 artifact for 96 of 96 files. The template is
untouched, so `.env` stays at 51 names with every value unchanged.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `37be3485db`.
- After: 3 app files change. Tests, runbook and protocol files ride along.
- Rollback: redeploy `/c/tmp/og-rb14`.

**Served `/login`.**
- Before: any ALB-verified tenant identity that is not blocked or email-denied.
- After: only the configured identity. `OTP_MAILBOX` and `MS_INGEST_IDENTITY` both hash-equal andrew@. With both
  unset, nobody is admitted.
- Rollback: redeploy.

**The admin refusals listing.**
- Before: the sender is derived from the caller.
- After: sender fields come from entry args only, and are null when absent. 0 records in the 32-day window are
  affected.
- Rollback: redeploy.

**`envelope.py`.** No behaviour change (AST-equal).

**`.env`.** Unchanged: 51 names, value hashes equal.

**Unchanged:** the 65 tools; grants and the state store (0 writes); Terraform, IAM, the ALB, secrets, the contract and
the template.

**Manifest.** `deployed_commit` moves; the previous value is `37be3485db`.

**After the act: DRAIN-BACK (R16).** CLOUD already equals the release for the gateway tree, so the drain-back is a
check, not a merge: `git diff <deployed> CLOUD -- infra/aws/ec2/opal-gateway` must be empty (`rl7.AC2`).

## 3. The named properties and their writers

**(a) Who `/login` admits.**
- Writers, N = 2: `server.py` `login()` (CHANGED), and the configured-identity settings (unchanged values).
- Expected: the configured identity is admitted; any other verified identity gets 403; empty settings give 403.
- Other branch: an unconfigured identity is admitted; roll back. Also, if the configured identity were REFUSED, Andrew's
  own re-mint path breaks; roll back.

**(b) The refusal listing's sender fields.**
- Writers, N = 1: `admin_refusals._shape` (CHANGED).
- Expected: the entry args are used, else null.
- Other branch: the caller's address leaks into the field; roll back.

**(c) Every other route.**
- Writers, N = 1: `server.py` routing (CHANGED in `/login` only).
- Expected: the floor (`rl4.AC1` on the 51-name baseline, `ht.AC2` at 51 keys) and the 65 tools hold.
- Other branch: any regression; roll back.

## 4. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live. Open ledger `nfra-oplgtw-gateway-release-r19`.
2. Run `r19_verify.sh before`.
3. Deploy from `/c/tmp/og-rel14` with `DEPLOY_BASE_REF=37be3485db9a00522c55a260666f708336c918f3`.
4. Run `r19_verify.sh after` immediately. It checks md5, the 65 tools, `.env` names and hashes, the `/login` arms, the
   sender fields and the floor.
5. On any failure: roll back from `/c/tmp/og-rb14`.
6. Run `rl7.AC1` and `rl7.AC2` against their `<expect>`, then record the drain-back check.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-06.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven equal to live.
- Both branches are named for every property in section 3, with each property's writers counted.
- The instrument deviation (section 0) is disclosed, with the narrower claim it supports.

**CTO -- owed.**

**CVO -- owed** (required).
