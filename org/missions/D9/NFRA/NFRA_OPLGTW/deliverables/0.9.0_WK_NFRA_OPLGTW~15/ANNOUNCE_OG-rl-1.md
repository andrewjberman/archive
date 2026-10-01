# ANNOUNCE_OG-rl-1 -- PHASE A RE-CUT (amendment A5, train slot 3), `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-01 ~10:10Z

Supersedes the d61fde4693 cut of this file (release tree `/c/tmp/og-rel3`, left alone). Nothing was uploaded, no secret was created or changed, no ledger is
open, no manifest edit. The host was touched only by read-only SSM (3 commands, listed). No secret value, principal or address is in this file.

**STANDING RULE (A5, CTO 27705 (1), row Z-S32): nobody sources `/opt/opal-gateway/.env` in a shell. A key read uses names only (`grep -o '^[A-Z_]*='`) or
`/proc/<service pid>/environ` for one named key, never echoed.** This re-cut obeyed it: key names came from a name-anchored `grep -o`, the one bearer read was
`/proc/<pid>/environ` for `OTP_BEARER` into a variable compared by boolean, and the release template's own before/after key print uses the same name-anchored pattern.

| item | value |
|---|---|
| live commit | `2c0f84966dc452d367ab1e4fc5d4849f08c1625e` (EC2_MANIFEST `deployed_commit` on CLOUD @5bd7735253, `deployed_at` 2026-10-01T09:08:45Z; MS-d-2, previous `05e3eff563`) |
| live S3 | `opal-gateway-latest.tar.gz` and `opal-gateway-2c0f84966d.tar.gz`: 444,479 bytes each, byte-identical (`cmp`), `git-ref` = the live sha, 2026-10-01T09:08:2x UTC |
| host md5 vs live commit | **89 of 89 files match** (0 mismatch; covers the 7 app files and `requirements.txt` the release touches) |
| release branch / tree | `rel-nfra-oplgtw-trnspt-deps-r2` at `/c/tmp/og-rel4` (sparse cone; `mcportal` seeded at `a3bff71ffa` = manifest pin, never staged) |
| release HEAD | `daa56d81ac7c91795f1a9c47b2c2430cb3879e24` (2 commits on live: `2c41151a26` gateway files, `daa56d81ac` deploy-to-ec2.sh) |
| rollback tree | `/c/tmp/og-rb4`, detached at `2c0f84966d`, `mcportal` at the pin; artifact built, not uploaded |
| audited override | `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses, release-branch commits only: `2c41151a26`, `daa56d81ac` |
| live ref moved since the cut? | no, at the time of writing (manifest, S3 `git-ref`, host md5 all `2c0f84966d`); step 7a at GO re-reads it |

## Step 1 -- live commit by CONTENT

Read-only SSM `ae6cf272-40f2-4fb6-b531-b8233c7c5ea3` (Success) on `i-07dccb1615503ac99`: `md5sum` of every file the artifact ships from `/opt/opal-gateway`
(`app/**`, `deploy/**`, `requirements.txt`, `identity_tool_allowlist.txt`; 89 files at `2c0f84966d`, up from 86 at `05e3eff563`) against `git show 2c0f84966d:<file>`:
**89 of 89 match**. `app/transcript_route.py` and `app/mail_route.py` read ABSENT on the host (expected, new files). Host `.env`: 39 lines.

## Step 2 -- release tree

- `git worktree add --no-checkout -b rel-nfra-oplgtw-trnspt-deps-r2 /c/tmp/og-rel4 2c0f84966d`, sparse cone, checkout.
- The five gateway commits of the four cells (`9fcd257fbd`, `a7c70dc5b2` OG-tx-1; `2fbc683db9` OG-hr-1; `adc979b13b` OG-ml-1; `1afce6312e` OG-hr-2; authors `~15 <` and `~16 <`; no later
  gateway commit by either), oldest first, applied per file as a three-way merge (`git merge-file`, base = the commit's parent, other = the commit) onto the LIVE bytes.
- **One file conflicted: `app/server.py`** (the live file has no `taxsma_workbook` import line, the anchor the cells' hunks sit beside). Resolved by hand to live bytes plus the cells'
  own two imports and five routes only. The other 15 files merged clean (`destructive_ops.py` and `tests/test_entitlement_admin.py`, which conflicted in the d61fde4693 cut, now merge clean
  because MX-r-7 put CLOUD's MX-t-13/MX-t-10 changes into live). Per-file +/- equals the cells' own.
- Pinned: `git diff --name-only 2c0f84966d HEAD | grep -v ^infra/aws/ec2/opal-gateway/` = **0** of 17.
- Census `git diff --stat 2c0f84966d HEAD -- infra/aws/ec2/opal-gateway`: **17 files, 1,989 insertions, 39 deletions** -- app: `config.py data_entitlement.py destructive_ops.py graph.py mail_route.py(new)
  server.py tools.py transcript_route.py(new)`; `requirements.txt` (+pypdf); tests: `test_entitlement_admin.py` and 6 new files; plus `deploy-to-ec2.sh`. Every file is one the cells changed plus
  `deploy-to-ec2.sh`; the file set equals the d61fde4693 cut's. `ms_ingest.py` is not among them.

## Step 3 -- tests on the release tree (`AUDIT_PATH` isolated per run, tree clean after)

- The cells' 6 new test files: **46 passed**, rc 0 (the order's "4 new + 3 adopted" reads as these 6, A3/S9).
- `tests/test_entitlement_admin.py::test_ogz2_ac08`: **1 passed**; `DENOMINATOR 60 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)`. The count is **LIVE 55 + OWN 5 = 60** (the live base's own assert is 55;
  OG-tx-1's 3 transcript tools + OG-ml-1's 2 mail tools add 5). The host tool list after the release should read BEFORE + exactly 5.
- `tests/test_ratelimit.py` in its own process: **6 passed**, rc 0.
- Beyond the order: `tests/test_deploy_base_guard.py` on the release, no roster variable in the shell: **6 passed**; the same file on the LIVE tree without them: 5 of 6 refuse (the OG-t-2 guard), with two synthetic
  pairs: 6 passed. `tests/test_schwab_host_inputs.py`: 6 passed / 1 failed on release AND on live identically (ENABLED_INTEGRATIONS holds 7 ids since MX-r-7, the test expects 6). Row Z-W15-S14.
  `tests/test_browser_oidc.py::test_oga3_ac07` still fails on the release (KeyError `transcript_route`), passes on live: the already-filed row Z-W15-S11, not re-filed. No whole-suite run was repeated.

## Step 4 -- secrets and host access

- **Mechanism.** The on-host SSM script runs `aws secretsmanager get-secret-value ... --query SecretString --output text` under the instance role into a shell variable and renders it into `.env`
  (`OTP_BEARER`, `MS_INGEST_BEARER`, `GRAPH_READ_BEARER`); the two new bearers use the same lines (`TRANSCRIPT_BEARER`, `MAIL_BEARER`). Names from `ROUTE_NAMES.json`.
- **`describe-secret` (no value read), all three PRESENT, `AWSCURRENT` only, default KMS key (no CMK grant needed):** `gateway/transcripts/bearer` (created 2026-10-01T03:07 -04:00, changed 03:28),
  `gateway/mail/bearer` (changed 03:29), `gateway/principals/rosters` (changed 03:29).
- **Role grant read (`opal-gateway-role`, inline policy `gateway-read-secrets-policy`):** one statement, `secretsmanager:GetSecretValue`, Resource = exactly the three ARNs above (suffixes `-tY9tUO`, `-g8XFDo`, `-wg59oX`,
  equal to the three describe-secret ARNs). The grant is in place; no IAM change applied here.
- **Rotation (CTO ruling (c), row Z-W17-S1; A5: consumer = the cot bd-auto-login `/otp/fetch` caller; the 49f token is untouched).** Read-only SSM `dc68bec2-9e13-4e9a-a614-126c32d2349d` (Success; booleans and counts only;
  the first attempt `1c6bf3e9-...` died on a typo in my own script before reading any token and printed only line/key counts):
  - `blackdiamond/cot/otp-gateway-token` is **64 hex: True**; the running service's `OTP_BEARER` (from `/proc/<MainPID>/environ`) has **2 tokens**, labels `49f cot`; **second token equals the cot secret: True**; first token equals
    the 49f secret: True; cot secret equals 49f secret: False (49f secret is not 64 hex). The attribution holds. The cot secret has only `AWSCURRENT` today, so after the put `AWSPREVIOUS` is the pre-rotation value.
  - Consumer and presenters, by reading source (repo copy md5 `7d37465ba68e8ddf44a66c008179d080`, unchanged since `6a0ce7fe65`): `infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js` run on `cot-exporter`
    (`i-0643a5bee8a8feabf`) calls `smGet(BD_OTP_GATEWAY_SECRET_ID)` per login attempt (line 187) and presents it as `Bearer` on `POST /otp/fetch` in a loop (lines 203-206); no module-level cache. The gateway host loads the
    value at process start and re-reads it at the deploy's restart. Repo census (`comp-find 'cot/otp-gateway-token'`): 79 hits / 17,282 files, no reader beyond the script, the box's `secret-ids.env`, Terraform IAM and the deploy template.
  - **Unmeasured (row Z-W15-S13 stands, ARMED):** the cot box's DEPLOYED copy of the script. `cot-exporter` is still `stopped` (ec2 describe-instances), so it cannot be read; A3/S13 lets the rotation proceed with the box stopped.
  - **Non-mutating probe:** `GET /otp/health` on the host (`http://localhost:8080/otp/health`, static-bearer gated, past the gate = 200 `{"ok":true}` or 503 `{"needs_login":true}`; it writes one credential audit record, nothing else).
    Measured now: **no bearer 401, a 64-zero bearer 401, the current cot value 200**. At PHASE B the pre-rotation value (the `AWSPREVIOUS` stage) must read 401 and the new one 200, both held in host memory, never printed.
  - Window: the new value is effective on the gateway only at the `.env` re-render and restart; between the put and that restart a cot login would read 401. The box is stopped; step 10 puts the value immediately before the act.

## Step 5 -- `.env` render (`deploy-to-ec2.sh`, hand-merged onto the LIVE `2c0f84966d` template, never a CLOUD-sourced one)

- printf: live **12 `%s`, 12 arguments**; release **15 `%s`, 15 arguments** (`_pr.py template`: `.env render: %s 15, args 15`). Positional alignment checked key by key (the new bearer, bearer and table arguments sit
  between `WRITE_CAPABLE_PRINCIPALS` and the Black Diamond ExternalId argument, which stays last). Rendered with synthetic values: **46 keys, 46 unique**; live **39**; **added 7, removed 0, existing literal values
  changed 0**; `ENABLED_INTEGRATIONS` equals live's seven-id value; the MS-d-2 lines `INTERNAL_READER_ROLE_ARN` and `MSP_CALLING_IDENTITIES` are untouched.
- **`.env` KEY set before (live host, 39, names only, SSM `dc68bec2`):** MOCK_GRAPH IDENTITY_PROVIDER AWS_REGION PUBLIC_BASE_URL BIND_HOST BIND_PORT TENANT_ID CLIENT_ID CLIENT_SECRET FERNET_KEY GATEWAY_JWT_PRIVATE_KEY_FILE
  GATEWAY_WORKERS AUDIT_S3_BUCKET OTP_BEARER OTP_BEARER_LABELS OTP_MAILBOX MS_INGEST_BEARER MS_INGEST_BEARER_LABELS MS_INGEST_IDENTITY GRAPH_READ_BEARER MASTER_ADMIN_EMAILS WRITE_CAPABLE_EMAILS MASTER_ADMIN_PRINCIPALS
  WRITE_CAPABLE_PRINCIPALS ENABLED_INTEGRATIONS NFRA_OPLGTW_CONTRACT_PATH SCHWAB_READER_ROLE_ARN SCHWAB_CATALOG_ROLE_ARN SCHWAB_EXTERNAL_IDS_SECRET_ID SCHWAB_ACCOUNT_REF_SECRET_ID BLACKDIAMOND_READER_ROLE_ARN
  BLACKDIAMOND_READER_EXTERNAL_ID DASHBOARD_OWNER_EMAILS SPRINT_VIEW_ALLOWED_EMAILS GRANT_WRITER_FUNCTION_NAME MCPORTAL_CHANGES_TABLE FIRM_ROLE_ARNS INTERNAL_READER_ROLE_ARN MSP_CALLING_IDENTITIES.
- **After (expected, 46):** the 39 above plus `TRANSCRIPT_BEARER`, `TRANSCRIPT_BEARER_LABELS=trnspt`, `TRANSCRIPT_MEETING_ALLOWLIST=` (empty until G-MEETINGS), `MAIL_BEARER`, `MAIL_BEARER_LABELS=msgpull`,
  `MAIL_SENDER_TABLE`, `MAIL_PDF_MAX_BYTES=10000000`. The script prints `ENV_KEYS_BEFORE` and `ENV_KEYS_AFTER` (names only, name-anchored `grep -o`, nothing sources the file).
- **R4:** the deploying-shell guard for `OG_MASTER_ADMIN_PRINCIPALS` / `OG_WRITE_CAPABLE_PRINCIPALS` is gone. The first lines of the on-host script fetch `gateway/principals/rosters`, parse `master_admin` and `write_capable` with
  `python3.11`, and refuse (non-zero before any extract, `.env` write or restart) unless `master_admin` is one `<tid>/<oid>` pair and `write_capable` a non-empty comma list of them (parse one-liners re-run on synthetic rosters:
  valid 0/0; master not a pair 1; bad write entry 1; empty write 1; missing keys 1/1; not JSON 1/1). The release needs NO off-repo roster hand-off.
- **Sender table (A4):** `MAIL_SENDER_TABLE` carries `data/transcripts/scripts/outlook/criterion.py` `DEFAULT_AUTHORS` evaluated by importing the module at GO from HEAD (read now: 3 entries, 67 characters joined, character-set
  check against the template's `^[A-Za-z0-9@._%+,\ -]*$` True, every entry an address). The template commits no address; the deploying shell sets `OG_MAIL_SENDER_TABLE` from that import.
- **AC3 early read** (`_pr.py template` on the release template): `GUID literals in the template: 0`, `template reads gateway/principals/rosters host-side: True`, `deploying-shell roster requirement still present: False`,
  `bash -n rc=0`, `RESULT: PASS`. Control on the LIVE template: FAIL on exactly the two roster arms (False / True). The final grade is after the release.

## Step 6 -- rollback built, not uploaded

- `/c/tmp/og-rb4` at `2c0f84966d` (clean; `mcportal` = `a3bff71ffa`): `bun install --frozen-lockfile` and `bun run build` produced `dist/index.html`; a mirror of the deploy's tar step (`.scratch/build_art.sh`) gives 444,383 bytes,
  92 files. The live S3 artifact: 444,479 bytes (the 96-byte difference is gzip/tar container metadata), 92 files. `diff -rq` of the two extracted trees: **empty, 92 of 92 identical**.
- The release artifact (same mirror on `/c/tmp/og-rel4`): **94 files**; differs from live in exactly 9 (`app/config.py data_entitlement.py destructive_ops.py graph.py server.py tools.py` and `requirements.txt` modified;
  `app/mail_route.py`, `app/transcript_route.py` new); `app/ms_ingest.py` identical to live; `deploy-to-ec2.sh` is not in the tarball.
- **Re-deploy (rollback) command** (the template on this tree is the LIVE one, so it needs the rosters in the rolling-back shell, row Z-W15-S12 / A3 ruling): the two values come from the site-Z Part D file
  (`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/PART_D_RECORD_20260930.md`) into the shell only, with the `OG-pr-1` script's mapping, never printed:
  `cd /c/tmp/og-rb4 && OG_MASTER_ADMIN_PRINCIPALS=<..> OG_WRITE_CAPABLE_PRINCIPALS=<..> DEPLOY_BASE_REF=<the live ref at that time = the release deploy commit, full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  It renders the old 39-key `.env`; the three new secrets are then simply unused. (After a rollback the cot bearer stays at its rotated value; the host `.env` is re-rendered from the then-current secret.)

## Rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W15-S14` (OBSERVATION, INERT: the live tree already fails two template-reading tests; the release template fixes one). Rows S9-S13 from the d61fde4693 cut stand as ruled by Z-S29.

## At GO (PHASE B, not authorized)

Re-read the live ref and the host (7a); if it moved, re-cut `og-rel4` on it and re-commit this file. Then the ledger `nfra-oplgtw-trnspt-deps-release`, step 10, the verify. Inputs the issuer supplies at GO: the four AC1 ids
(`OG_RL_OFF_TABLE_MSG`, `OG_RL_THREAD_MSG`, `OG_RL_NONPDF_MSG`, `OG_RL_NONPDF_ATT`). `OG_MAIL_SENDER_TABLE` is produced at GO by importing `criterion.py` (A4), no hand-off.
