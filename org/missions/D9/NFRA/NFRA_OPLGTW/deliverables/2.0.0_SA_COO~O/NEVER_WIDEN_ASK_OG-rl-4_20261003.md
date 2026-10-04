# Never-widen ask -- OG-rl-4, the next opal-gateway release on live 4231bd2ddc (round 14)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-03 ~02:0xZ. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-4.gateway-release-r14.md` (issued @544b8e2466).
Authority: Andrew-direct ~23:4xZ "all appproved go" (round 14; relay msg 28810). Spec: analysis round 12 s.5 item 2, as
amended by analysis round 13 s.4 item 2 @fea5fbcdbf and addendum @b100b15b2e. PHASE A evidence:
`deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-4.md`, drained @25be9d3c98.

**Halves owed:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O`, REQUIRED (analysis round 13, ruling 4): the symmetric refusal changes whom `/hx/mail` and
  `/hx/transcripts` admit;
- `2.0.0_SA_COO~O` (COO), signed in section 5.

All three are against THIS file at its commit.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r14` (`/c/tmp/og-rel9`) HEAD `af2d7629702528c050860314a7867d8ea0cecfbf`, two commits
on live `4231bd2ddc` (host md5 94 of 94 equal):
- `25335f8ac3`: OG-au-1's and OG-sr-1's gateway files;
- `af2d762970`: the template and the contract-source test.

**Census against live.** 9 files, +225/-22: `app/audit.py`, `app/tools.py`, `app/mail_route.py`, `app/transcript_route.py`,
`deploy-to-ec2.sh`, `tests/test_audit_bytes_principal.py`, `tests/test_mail_route.py`, `tests/test_transcript_route.py`
and `tests/test_schwab_host_inputs.py`. None of `ms_ingest.py`, `taxsma_workbook.py` or `teams_route.py` is in it. The
artifact differs from live in 4 files, 97 = 97.

**Issuer re-read, independent of the worker (01:2xZ).**
- The 4 OG-sr-1 files are sha-EQUAL to `03a23664b4`.
- The `audit.py` and `tools.py` hunk sets are sha-EQUAL to `070444e520`, and the new test is sha-EQUAL.
- The identity read refuses with rc 3 (`|| { ...; exit 3; }`) before any `.env` write.

**Tests on the release tree:**

| Test | Passed |
|---|---|
| test_audit_bytes_principal | 3 |
| test_mail_route | 11 |
| test_transcript_route | 10 |
| test_teams_route | 14 |
| test_schwab_host_inputs | 9 |
| test_taxsma_workbook | 21 |
| test_mail_listing | 12 |
| test_ogz2_ac08 | 60 = LIVE 60 + OWN 0 |

**Contract-source test, planted-mutant control.** M1 (the stager's source changed, bytes equal) fails 1 test; M2 (the
shipped copy off by one byte) fails 2; M3 (quoting removed) fails 1. Restored, 9 pass.

**Render.** On a masked sample, `_env_shape_host.py` reads `env_keys 50 whitespace_values 4 disagreeing 0` (live: 4).
Key names are the same 50, in order.

**Rollback.** `/c/tmp/og-rb9` at `4231bd2ddc`, 97 of 97 equal to the live S3 artifact. Its identity export reads
`IDENTITY_SHA256 MATCH`.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `4231bd2ddc`.
- After: the four app files above change; the test files are not executed by the service.
- Rollback: redeploy `/c/tmp/og-rb9` with `DEPLOY_BASE_REF` = the release sha and the identity export (that template
  still reads the identity from the shell).

**Host `.env`.**
- Before: 50 keys; 4 values read differently by systemd and bash.
- After: the same 50 names. FIVE values are quoted (row Z-W15-S29): `OTP_BEARER`, `OTP_BEARER_LABELS`,
  `ENABLED_INTEGRATIONS` and `MAIL_SENDER_TABLE` double-quoted; `FIRM_ROLE_ARNS` single-quoted, because its JSON carries
  double quotes. The VALUE each one carries must not change.
- Rollback: the same redeploy renders the old `.env`.

**Secret `gateway/principals/rosters`.**
- Before: the roster keys.
- After: it also carries `taxsma_workbook_identity`. Its value's sha256 equals the host's current
  `TAXSMA_WORKBOOK_IDENTITY`, and every pre-existing key's value hash is unchanged.
- Rollback: `put-secret-value` of the prior version's value. The rollback template never reads the new key.

**Served behaviour -- the capability change.**
- Before: `/hx/mail` and `/hx/transcripts` admit their own bearer even when its value equals another route's credential.
- After: they REFUSE a value shared with any other route (the `teams_route` pattern). Admission with today's distinct
  values is unchanged.
- Rollback: redeploy.

**Audit records.**
- Before: `read_meeting_transcript` records have no `bytes` or `principal`.
- After: the ok-path records gain both; every other tool's record is byte-for-byte as before.
- Rollback: redeploy.

**Tax route identity source.**
- Before: the deploying shell.
- After: host-side, from the rosters secret. The shell variable is no longer read.
- Rollback: redeploy (the rollback template reads the shell again).

**Unchanged:** the tool list (65). **Manifest:** `deployed_commit` moves; the previous value is `4231bd2ddc`; rollback
reverts the manifest commit.

**Not touched, by name:** Terraform, IAM, the ALB, the instance, the identity allowlist, `taxsma_workbook.py`,
`teams_route.py`, `ms_ingest.py`, the mcportal pin. No secret other than the one key is written.

## 3. The named properties and their writers

**(a) Whom `/hx/mail` and `/hx/transcripts` admit.**
- Writers, N = 2: each route's `match_bearer` (code) and the `.env` render (values).
- Expected: each route's own bearer is still accepted after the deploy. The verify reads `/hx/mail` 200, `/hx/teams/me`
  200, and `/hx/transcripts` accepted (403 `meeting_not_allowed`, because the allowlist is empty, row Z-W15-S30), never
  401. A shared value is refused (unit tests).
- Other branch: any own bearer returns 401, so roll back.

**(b) Every `.env` value the service reads.**
- Writers, N = 1: the render.
- Expected: all 50 service-process value hashes equal before and after. The quoting changes the representation only.
- Other branch: any hash differs (for example, systemd 252 keeps `FIRM_ROLE_ARNS`'s single quotes, which was not
  exercised on the host), so roll back.

**(c) Whose identity the Tax route reads as.**
- Writers, N = 2: the step-13 secret write and the render's host-side read.
- Expected: the host's `TAXSMA_WORKBOOK_IDENTITY` hash is unchanged after the deploy.
- Other branch: it differs, so roll back. If the key were absent, the template would refuse rc 3 before any write and
  the host would stay as it was.

**(d) The transcript audit record shape.**
- Writers, N = 1: `log_call`.
- Expected: the new keys appear on the transcript ok-path only. `rl4.AC2` grades the first post-deploy read, which the
  issuer makes.

## 4. Act and verify (PHASE B, from the order)

Re-read live. Open ledger `nfra-oplgtw-gateway-release-r14` (entry and sentinel). Add the secret key. Deploy from
`/c/tmp/og-rel9` with `OG_TAXSMA_WORKBOOK_IDENTITY` UNSET. Run `rl4_verify.sh after` immediately: md5, tool list,
50-key names, the 50 value hashes, the three own-bearer reads, `rl4.AC1`, and `tr.AC1` arms 1-3 plus the 50-key line
(row Z-W15-S31). Any failure: roll back, re-verify, close ROLLED BACK.

Gateway queue: no other gateway releaser is LIVE (`get_live_agents` ~02:0xZ). `OG-r-4` is complete (drained
@7258b0d6c5), so the bench cannot overlap the deploy.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-03 ~02:0xZ.**
- The act may touch exactly the keys in section 2 and the manifest.
- Each rollback is pre-built and stands alone.
- Both branches are named for every property in section 3; the writers of each are counted there.
- My reads of the bytes are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required: a capability change).
