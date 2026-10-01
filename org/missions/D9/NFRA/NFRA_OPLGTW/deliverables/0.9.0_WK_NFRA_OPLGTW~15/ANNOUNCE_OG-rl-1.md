# ANNOUNCE_OG-rl-1 -- PHASE A (pre-GO), `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-01 ~06:40Z

PHASE A only (steps 1-7). Nothing was uploaded, no secret was created or changed, no ledger is open, no manifest edit. The host
and the cot box were touched only by read-only SSM (3 commands, listed below). No secret value, principal or address is in this file.
`OG-pr-1` has NOT landed (amendment A2): its three items read `grant pending OG-pr-1` / ABSENT below and the phase continued.

| item | value |
|---|---|
| live commit (host md5 authority) | `d61fde46933221e8afbac7418f06d7525d3347c8` (EC2_MANIFEST `deployed_commit` at CLOUD @0110c22ed5; live S3 `-latest` and `-d61fde4693` objects: 430,017 bytes, `git-ref` = the same sha, 2026-10-01T01:38 UTC) |
| release branch / tree | `rel-nfra-oplgtw-trnspt-deps` at `/c/tmp/og-rel3` (sparse cone as og-rel2; `mcportal` seeded at `a3bff71ffa` = manifest `mcportal_commit`, never staged) |
| release HEAD | `f12f874154ae37c3133d6a699f53a012bf576085` (2 commits on live: `bfd65d743c` gateway files, `f12f874154` deploy-to-ec2.sh) |
| rollback tree | `/c/tmp/og-rb3` detached at the live commit, `mcportal` at the pin |
| live ref moved since the cut? | no: the manifest, the S3 `git-ref` and the host md5 all read `d61fde4693` (MX-r-7 / MS-d-2 not landed) |

## Step 1 -- live commit, by CONTENT

Read-only SSM (`b4b402cd-7cbb-40c9-8551-aee59280f210`, Success) on `i-07dccb1615503ac99`: `md5sum` of every file the artifact ships
from the host's `/opt/opal-gateway` (`app/**`, `deploy/**`, `requirements.txt`, `identity_tool_allowlist.txt`) against `git show d61fde4693:<file>`:
**84 of 84 files match** (this covers all 7 app files and `requirements.txt` the release touches). `app/transcript_route.py` and
`app/mail_route.py` read ABSENT on the host (expected: new files). Host `.env`: 35 lines (35 keys).

## Step 2 -- release tree

- `git worktree add --no-checkout -b rel-nfra-oplgtw-trnspt-deps /c/tmp/og-rel3 d61fde4693`, sparse cone, checkout.
- The five gateway commits of the four cells (`9fcd257fbd`, `a7c70dc5b2` OG-tx-1; `2fbc683db9` OG-hr-1; `adc979b13b` OG-ml-1; `1afce6312e` OG-hr-2),
  oldest first, applied by diff PER FILE as a three-way merge (`git merge-file`, base = the commit's parent, other = the commit)
  onto the live bytes. A plain `git apply --3way` left conflicts and was discarded; the merge script is `.scratch/merge.py` (not committed).
- **Three files conflicted** because CLOUD carries other cells' work that live does not (MX-t-13's `blackdiamond_list_fees`,
  MX-t-10, MS-sg-1's sender gate, OA-e-10, MX-q-3 registrations): `app/destructive_ops.py`, `app/server.py`,
  `tests/test_entitlement_admin.py`. Each was resolved by hand to LIVE bytes plus the cells' own additions only
  (SAFE_TOOLS +5 names; server.py +2 imports +5 routes; ac08 count = LIVE 53 + OWN 5 = **58**, C3). Row Z-W15-S10.
- Pinned: no non-gateway path differs from live (`git diff --name-only d61fde4693 HEAD | grep -v ^infra/aws/ec2/opal-gateway/` = 0).
- Audited `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses (one per release-branch commit): `bfd65d743c`, `f12f874154`.
- Census `git diff --stat d61fde4693 HEAD -- infra/aws/ec2/opal-gateway`: **17 files, 1,989 insertions, 39 deletions**:
  app: `config.py data_entitlement.py destructive_ops.py graph.py mail_route.py(new) server.py tools.py transcript_route.py(new)`;
  `requirements.txt` (+pypdf==6.16.2); tests: `test_entitlement_admin.py` and 6 new files; plus `deploy-to-ec2.sh`. Every file is one the cells changed,
  plus `deploy-to-ec2.sh`. Per-file +/- equals the cells' own (sum of their commit numstats); `ms_ingest.py` is not among them.

## Step 3 -- tests on the release tree (`AUDIT_PATH` isolated, tree clean after)

- The cells' 6 new test files (`test_transcript_tools`, `test_transcript_route`, `test_mail_route`, `test_inspect_email_attachment`,
  `test_list_email_filtered`, `test_read_email_fields`): **46 passed**, rc 0. (The order counts 4 new + 3 adopted = 7; the cells add 6. Row Z-W15-S9.)
- `tests/test_entitlement_admin.py::test_ogz2_ac08`: **1 passed** (`DENOMINATOR 58 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)`).
- `tests/test_ratelimit.py` in its own process: **6 passed**, rc 0.
- Beyond the order, one whole-suite run on each tree (`tests`, ratelimit excluded, `AUDIT_PATH` isolated): live 358 passed / 27 failed / 35 errors;
  release 410 passed / 21 failed / 35 errors; both are order-dependent (a StreamableHTTP session-manager reuse error) and the failing sets differ
  by 7 on the live side. **One failure is the release's own**, reproduced alone: `tests/test_browser_oidc.py::test_oga3_ac07` KeyError
  `'transcript_route'` (the test's route-declaration parser resolves only `oauth_as`/`browser_oidc` attributes; the same test fails on CLOUD today with KeyError
  `'taxsma_workbook'`). It is a test file outside the cells' census, not shipped in the artifact, and was not edited. Row Z-W15-S11.

## Step 4 -- secrets and host access

- **Mechanism today.** The deploy's on-host SSM script runs `aws secretsmanager get-secret-value ... --query SecretString --output text` under the
  instance role into a shell variable and renders it into `.env` (`OTP_BEARER`, `MS_INGEST_BEARER`, `GRAPH_READ_BEARER`); the value is never in the command text.
  The two new bearers use the same lines (`TRANSCRIPT_BEARER`, `MAIL_BEARER`). Names from `ROUTE_NAMES.json`: `gateway/transcripts/bearer`, `gateway/mail/bearer`
  (plus `gateway/principals/rosters`, read host-side).
- **Host role reads (policy read, `opal-gateway-role`, 16 inline policies):** it reads `blackdiamond/cot/otp-gateway-token` and `blackdiamond/49f/otp-gateway-token`
  (inline `opal-gateway-golive`). **It reads NONE of the three new secrets: `grant pending OG-pr-1`.** No IAM change applied here.
- **`describe-secret` (no value read):** `gateway/transcripts/bearer` ABSENT, `gateway/mail/bearer` ABSENT, `gateway/principals/rosters` ABSENT
  (ResourceNotFoundException x3; positive control: the cot secret reads present below). Before OG-pr-1 this is the expected state.
- **Rotation (CTO ruling (c), row Z-W17-S1), `blackdiamond/cot/otp-gateway-token`:**
  - Shape (SSM `b31b63e7-2a9d-4a0a-9afa-9dc186092380`, Success, booleans only): the secret is **64 hex: True**; host `.env` `OTP_BEARER` is **line 14** (35-line file),
    two tokens, labels `49f cot`; **second token equals the cot secret: True**; first token equals the 49f secret: True; cot secret equals 49f secret: False
    (the 49f secret is not 64 hex). The attribution holds.
  - Presenters, by reading source and IAM: (1) the gateway host itself (loads the value from `.env` at process start; the deploy's restart reloads it);
    (2) the cot box script `infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js` run on `cot-exporter` (`i-0643a5bee8a8feabf`,
    role `cot-exporter-ec2-role`, the only other role granted the secret, `terraform/cot-pipeline/iam.tf:302`): `smGet(BD_OTP_GATEWAY_SECRET_ID)` shells out
    to `aws secretsmanager get-secret-value` on each OTP request (line 187), once per login attempt, no module-level cache: **per call, not cached**.
    The 49f liveness Lambda (`otp-liveness.tf:88`) reads the 49f secret, not cot. No other reader found in the repo (`comp-find`/`git grep`: 4 non-doc hits).
  - **Unmeasured:** the cot box's DEPLOYED copy of the script. `cot-exporter` is `stopped` and not SSM-registered (SendCommand: InvalidInstanceId), so I could not read it;
    the repo copy md5 is `7d37465ba68e8ddf44a66c008179d080`. No caching presenter is known; this is not a BLOCKING row, and it is recorded as ARMED (row Z-W15-S13).
  - Non-mutating probe for the verify: `GET /otp/health` on the host (`http://localhost:8080/otp/health`) with `Authorization: Bearer <value>`: refused = 401, accepted =
    200 `{"ok":true}` or 503 `{"needs_login":true}` (past the gate). It reads no mail. The pre-rotation value is taken after the put from the secret's `AWSPREVIOUS` stage
    and the new one from `AWSCURRENT`, both in host memory, never printed (the host role holds GetSecretValue on the secret).
  - Window: the new value is effective on the gateway only at the `.env` re-render and restart; between the put and that restart the cot box (if it ran) would be refused 401.
    The box is stopped; step 10 puts the value immediately before the act.

## Step 5 -- `.env` render (`deploy-to-ec2.sh`, hand-merged onto the LIVE `d61fde4693` template)

- printf: live **11 `%s`, 11 arguments**; release **14 `%s`, 14 arguments**
  (`pr.py template` read: `.env render: %s 14, args 14`). Rendered with synthetic values: **42 keys, 42 unique**; live 35; **added 7, removed 0, existing literal values changed 0**;
  `ENABLED_INTEGRATIONS` equals live's six-id value.
- Added keys: `TRANSCRIPT_BEARER`, `TRANSCRIPT_BEARER_LABELS=trnspt`, `TRANSCRIPT_MEETING_ALLOWLIST=` (empty until G-MEETINGS), `MAIL_BEARER`, `MAIL_BEARER_LABELS=msgpull`,
  `MAIL_SENDER_TABLE` (from `OG_MAIL_SENDER_TABLE` in the deploying shell, a datum supplied by the issuer at GO, never committed; character-set checked before any
  build or upload; empty = the mail route refuses every message), `MAIL_PDF_MAX_BYTES=10000000` (the route's own default, explicit).
- R4: the deploying-shell guard for `OG_MASTER_ADMIN_PRINCIPALS` / `OG_WRITE_CAPABLE_PRINCIPALS` is removed. The first lines of the on-host script fetch
  `gateway/principals/rosters`, parse `master_admin` and `write_capable` with `python3.11`, and refuse (non-zero before any extract, `.env` write or restart) unless
  `master_admin` is one `<tid>/<oid>` pair and `write_capable` a non-empty comma list of them. The two parse one-liners were run on synthetic rosters:
  valid -> rc 0/0; master not a pair -> 1; a bad write entry -> 1; empty write -> 1; missing keys -> 1/1; not JSON -> 1/1. The `MASTER_ADMIN_PRINCIPALS=` and
  `WRITE_CAPABLE_PRINCIPALS=` lines stay (now from the host variables).
- `ANNOUNCE`: the script echoes the `.env` KEY set (`cut -d= -f1`, names only) as `ENV_KEYS_BEFORE` and `ENV_KEYS_AFTER`.
- **AC3 early read** against this release template (`_pr.py template`): `GUID literals in the template: 0`, `template reads gateway/principals/rosters host-side: True`,
  `deploying-shell roster requirement still present: False`, `bash -n rc=0`, `RESULT: PASS`. Its final grade is after the release.
- Hand-off needed at GO: `OG_MAIL_SENDER_TABLE` (Manav's addresses as they stand; Yang's join as a data change); the four AC1 ids (`OG_RL_OFF_TABLE_MSG`, `OG_RL_THREAD_MSG`,
  `OG_RL_NONPDF_MSG`, `OG_RL_NONPDF_ATT`).

## Step 6 -- rollback built, not uploaded

- `/c/tmp/og-rb3` at `d61fde4693` (clean; `mcportal` = `a3bff71ffa`): `bun install --frozen-lockfile` "Checked 77 installs across 128 packages (no changes)", `bun run build` produced `dist/index.html`.
  A mirror of the deploy's tar step gives 429,899 bytes, 87 files. Live `opal-gateway-d61fde4693.tar.gz`: 430,017 bytes, 87 files. `diff -rq` of the two extracted trees: **empty, 87 of 87 identical**
  (the 118-byte difference is gzip/tar container metadata).
- The release artifact (same mirror, `/c/tmp/og-rel3-build`): **89 files**; differs from live in exactly 9 files (`app/config.py data_entitlement.py destructive_ops.py graph.py
  server.py tools.py` and `requirements.txt` modified; `mail_route.py`, `transcript_route.py` new); `app/ms_ingest.py` identical to live; `deploy-to-ec2.sh` is not in the tarball.
- Re-deploy (rollback) command, run with `DEPLOY_BASE_REF` = the release commit's full sha read at act time and `OG_MASTER_ADMIN_PRINCIPALS` / `OG_WRITE_CAPABLE_PRINCIPALS` exported **because the LIVE template
  still carries the deploying-shell guard** (row Z-W15-S12):
  `cd /c/tmp/og-rb3 && OG_MASTER_ADMIN_PRINCIPALS=<..> OG_WRITE_CAPABLE_PRINCIPALS=<..> DEPLOY_BASE_REF=<release full sha at that time> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  It renders the old 35-key `.env`; the three new secrets are then simply unused.

## Rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W15-S9` (test-file count in the order), `-S10` (three hand-resolved conflicts), `-S11` (`test_browser_oidc::test_oga3_ac07` fails on the release),
`-S12` (rollback needs the principal env), `-S13` (cot box script copy unmeasured).

## At GO (PHASE B, not authorized)

Re-read the live ref and the host (7a); if it moved, re-cut `og-rel3` on it and re-commit this file. Then the ledger `nfra-oplgtw-trnspt-deps-release`, step 10 with the issuer's inputs above, and the verify. OG-pr-1 must have landed (three secrets present, grant in place);
a missing grant after it is a BLOCKING row naming the exact grant.
