# Never-widen ask -- OG-rl-10, the r24 opal-gateway HOTFIX on live 2c27f3a795 (round 23, workstream PORTAL-LOGIN-HOTFIX)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-06.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-10.gateway-hotfix-r24-portal-login.md`
  (@d32e40998d).
- **Spec:** CTO R32 (`1.0.0_SA_CTO~O` msg 30413), inside the fabric hold's carve-out (`0.0.0_AB_MSTR~Z` msgs 30408,
  30411, 30418).
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-10.md`, worker commit `601a6874e7`.
- **Release sha the halves sign:** `9d3e2eb3fce3ceabbf06f6c1819451894291be05`, branch `rel-nfra-oplgtw-r24`.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO);
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r24` (`/c/tmp/og-rel18`), one commit on live `2c27f3a795`. The issuer's own read:
`git diff --name-only 2c27f3a795 9d3e2eb3fc` lists ONE file,
`infra/aws/ec2/opal-gateway/app/integrations/opal_portal/integration.py` (+6/-6):
- `AUTH_API_BASE = PORTAL_FRONT_DOOR` replaces the raw API Gateway host;
- the `hosts` tuple drops `7k3ed8px20.execute-api.us-east-1.amazonaws.com`;
- two comments say why.

**Tests.** Nine gateway test files, each in its own process: 5 ids fail, and the same 5 fail on live. The other 63
files were not run; the order did not require them for a one-file hotfix. The floor reads yes/yes on live.

**Rollback.** `/c/tmp/og-rb17` at `2c27f3a795`, 96 of 96 equal to the live S3 artifact.

## 2. Blast radius -- what the act may touch

**The portal login of the `opal_portal` integration.**
- Before (measured on the live installed code, in-process): `IntegrationAuthError portal login 403`, posted to the raw
  host. The auth Lambda's log reads `Origin verification FAILED: POST /auth/login` for 7 of 7 gateway logins,
  23:06-23:11Z.
- After (the staged release bytes on the host, same service secret): `login: OK`, posted to `www.opalinvest.dev`.
- Rollback: redeploy `og-rb17`; the login returns to the raw host and to 403.

**Egress.** `www.opalinvest.dev` was already on this integration's allowlist. No host is added, and one is removed.

**Unchanged:** every other tool (65) and route; `.env` (51 names and every value); grants and the state store
(0 writes); the service secret `opal/portal/svc-data-refresh`; Terraform, IAM, the ALB and the template. The service
restarts once.

**Manifest.** `deployed_commit` moves; the previous value is `2c27f3a795`.

**Not in this release:** the held r23 set (OG-rl-9, `ba27a07439`). CLOUD will differ from live by r23's six files and
the CLOUD-only runbook until r23 re-cuts on the new live. No drain-back check runs here.

## 3. The named property and its writers

**Which host the gateway's portal login is posted to.**
- Writers, N = 1: the one `AUTH_API_BASE` assignment (CHANGED). One reader, `_PortalSession.token()`, reached from two
  call sites in `opal_data_refresh_upload`.
- Expected: a 200 from the front door yields the service JWT, and the upload tool proceeds as designed.
- Other branch: any non-200 raises `portal login <code>`, exactly as today. That is a rollback trigger at the
  post-deploy read.
- What this enables downstream: `opal_data_refresh_upload(confirm=True)` can again fire the live yang-pipeline. That
  send is `0.0.3_BG_BBGTerminal`'s act on Andrew's word. It is not part of this release.

## 4. Act and verify

1. Re-read live; if it moved, re-cut.
2. Open ledger `nfra-oplgtw-gateway-hotfix-r24`, with entry and sentinel committed first.
3. Run `r24_verify.sh before`.
4. Deploy from `/c/tmp/og-rel18` with `DEPLOY_BASE_REF=2c27f3a7958de0aa644374cdd08fc188a27e9e3f`.
5. Run `r24_verify.sh after` immediately (7 checks: health, md5, the floor, the login).
6. Run the installed code's own login on the host and write `RL10_LOGIN.json`. Not OK: roll back.
7. Run `rl10.AC1` and `rl10.AC2`. Both were exercised pre-GO, each with a pass form and negative controls.
8. The issuer's close read: `opal_data_refresh_upload(dry_run=True)` returns no `portal login` error. The dry run
   stages two files in `pending/` and triggers nothing.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-06.**
- The act may touch exactly the one file in section 1 and the manifest.
- The rollback is pre-built and proven.
- Both branches of the one property are named, with its writers counted.
- My read of release vs live (one file) is independent of the worker's.
- Limit disclosed: 63 of 72 test files were not run.

**CTO -- owed.**

**CVO -- owed.**
