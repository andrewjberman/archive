# ANNOUNCE_OG-rl-2 -- PHASE A (train slot 5), `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-01 ~14:45Z

Nothing was uploaded, no secret was created or changed, no ledger is open, no manifest edit. The host was touched only by read-only SSM (2 commands, listed). No secret value,
principal or address is in this file.

**STANDING RULE (row Z-S32): nobody sources `/opt/opal-gateway/.env` in a shell. A key read uses names only (`grep -o '^[A-Z0-9_]*='`) or `/proc/<service pid>/environ` for one named key,
never echoed.** This cut obeyed it: key names from a name-anchored `grep -o`; the one value read (`MAIL_SENDER_TABLE`, from `/proc/<MainPID>/environ`) was reduced to an item count and a length on the host.

| item | value |
|---|---|
| live commit | `e3567ce5f788f45195bec065f4d2fc5a68a38cd3` (EC2_MANIFEST `deployed_commit` at CLOUD 2f895e20a5, `deployed_at` 2026-10-01T12:37:03Z, MX-r-8; previous `daa56d81ac`). **The handoff said MX-r-8 had not landed; it had** -- row Z-W15-S16 |
| live S3 | `opal-gateway-latest.tar.gz` and `opal-gateway-e3567ce5f7.tar.gz`: 460,595 bytes each, `git-ref` = the live sha |
| host md5 vs live commit | **91 of 91 files match** (0 mismatch); `app/mail_route.py` and `app/transcript_route.py` PRESENT, `deploy/mail_sender_table.txt` ABSENT (expected: the release adds it) |
| release branch / tree | `rel-nfra-oplgtw-hx-mail-listing` at `/c/tmp/og-rel5` (sparse cone; `mcportal` seeded at the manifest pin `a3bff71ffa`, never staged) |
| release HEAD | `0a1d9079c6` (2 commits on live: `54d5c219b8` gateway files, `0a1d9079c6` deploy-to-ec2.sh) |
| rollback tree | `/c/tmp/og-rb5`, detached at `e3567ce5f7`, `mcportal` at the pin; artifact built, not uploaded |
| audited override | `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses, release-branch commits only: `54d5c219b8`, `0a1d9079c6` |
| host reads | SSM `097772bc-f82e-450b-a628-afd55bd87964` (md5, Success) and `82c946ad-b364-402e-9c2a-0894da32f36e` (key names, count, Success) |

## Step 1 -- live commit by CONTENT

`md5sum` of every file the artifact ships from `/opt/opal-gateway` (`app/**`, `deploy/**`, `requirements.txt`, `identity_tool_allowlist.txt`; 91 files at `e3567ce5f7`) against
`git show e3567ce5f7:<file>`: **91 of 91 identical**. Host `.env`: 46 lines.

## Step 2 -- release tree

- `git worktree add --no-checkout -b rel-nfra-oplgtw-hx-mail-listing /c/tmp/og-rel5 e3567ce5f7`, sparse cone, `mcportal` seeded.
- The gateway commits naming `OG-hl-1`: **one**, `cdd4e5cb08` (author `~16`; no later gateway commit names it). Applied per file as a three-way merge (`git merge-file`, base = its parent,
  other = the commit) onto the LIVE bytes: `app/mail_route.py` and `app/server.py` merged clean; `deploy/mail_sender_table.txt` and `tests/test_mail_listing.py` are new files.
  The cell's own per-file +/-: `mail_route.py` +193/-3 net, `server.py` +1, table +3, test +339 -- equal to `cdd4e5cb08`'s stat.
- Pinned: `git diff --name-only e3567ce5f7 HEAD | grep -vc ^infra/aws/ec2/opal-gateway/` = **0** of 5.
- Census `git diff --stat e3567ce5f7 HEAD`: **5 files, 555 insertions, 13 deletions** -- `app/mail_route.py`, `app/server.py`, `deploy/mail_sender_table.txt` (new), `tests/test_mail_listing.py` (new),
  `deploy-to-ec2.sh`. Exactly OG-hl-1's four files plus the template. `app/ms_ingest.py` is not among them.

## Step 3 -- tests on the release tree (`AUDIT_PATH` isolated per run, tree clean after)

- `tests/test_mail_listing.py` **12 passed**; `tests/test_mail_route.py` **10 passed**; `tests/test_transcript_route.py` **9 passed** (31 together, rc 0).
- `tests/test_entitlement_admin.py::test_ogz2_ac08`: **1 passed**; `DENOMINATOR 60 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)` on the release AND the same line on the LIVE tree
  (`/c/tmp/og-rb5`): **LIVE 60 + OWN 0 = 60**. The host tool list after the release must equal BEFORE.
- Beyond the order: `tests/test_deploy_base_guard.py` 6 passed on release and on live; `tests/test_schwab_host_inputs.py` 6 passed / 1 failed on release AND on live identically (the already-filed row Z-W15-S14).

## Step 4 -- the template edit (row Z-S36), hand-merged onto the LIVE `e3567ce5f7` template

- Placement, in the on-host script, right after the artifact is extracted and before the venv, the `.env` printf and any restart: `sudo rm -f deploy/mail_sender_table.txt` (before the extract, so a
  present file proves this artifact shipped it), then the read of `${REMOTE_DIR}/deploy/mail_sender_table.txt` (CR stripped, blank lines dropped, joined with commas), then two refusals, both
  `exit 3`: (a) `REFUSED: MAIL_SENDER_TABLE is empty (...missing from the artifact or holds no address); no .env written, no restart.` and (b) `REFUSED: MAIL_SENDER_TABLE holds a character outside an
  address list`, grep -E `^[A-Za-z0-9@._%+, -]*$` (the template's own address set). The deploying-shell `OG_MAIL_SENDER_TABLE` block and its pre-upload check are deleted; 0 occurrences remain.
- **`_rl2.py` on the release template:** `reads deploy/mail_sender_table.txt host-side: True`; `still takes OG_MAIL_SENDER_TABLE from the deploying shell: False`;
  `empty-table refusal lines naming MAIL_SENDER_TABLE: 1`; `.env render: %s 15, args 15; MAIL_SENDER_TABLE line True`; `bash -n rc=0`; **RESULT: PASS, rc 0**.
  **On the LIVE template (`e3567ce5f7`):** `False` / `True` / `0` / `%s 15, args 15` / `bash -n rc=0`; **RESULT: FAIL, rc 1**.
- **Render:** live 15 `%s`, 15 arguments; release 15 `%s`, 15 arguments; the only argument that changed is the MAIL_SENDER_TABLE one (`${OG_MAIL_SENDER_TABLE}` -> `\$MAIL_SENDER_TABLE`, aligned to its key).
  Rendered with synthetic values: **46 keys, 46 unique** on both; key set equal; every literal line equal; `ENABLED_INTEGRATIONS` equal (7 ids).
- **Synthetic refusal, outside the host** (the block rendered as the deploying shell's unquoted heredoc, run under `set -euo pipefail`; `.scratch/rehearse3.py`, output `rehearse3_out.txt`):
  missing file **rc 3**; empty file **rc 3**; blank/whitespace lines only **rc 3**; one valid address **rc 0** (1 entry); three valid with CRLF and no final newline **rc 0** (3 entries);
  a semicolon **rc 3**; shell metacharacters **rc 3**. The whole on-host script rendered with dummy variables: `bash -n` rc 0.
- Sender table content: `deploy/mail_sender_table.txt` holds **3** entries; `criterion.DEFAULT_AUTHORS` has **3** entries, 67 characters joined, character set True, and the file equals it in order.
  The running process's `MAIL_SENDER_TABLE` today: 3 items, 67 characters (supplied from `criterion.py` at the MX-r-8 deploy).
- Row Z-W15-S17: the refusal necessarily runs AFTER the extract (the file ships in the artifact), so a refusal leaves new files on disk with the old process and `.env` untouched.

## `.env` key census, names only (host read 82c946ad, MainPID 519984 active, `/health` 200)

- **Before (live host): 46 keys** -- AUDIT_S3_BUCKET AWS_REGION BIND_HOST BIND_PORT BLACKDIAMOND_READER_EXTERNAL_ID BLACKDIAMOND_READER_ROLE_ARN CLIENT_ID CLIENT_SECRET DASHBOARD_OWNER_EMAILS ENABLED_INTEGRATIONS
  FERNET_KEY FIRM_ROLE_ARNS GATEWAY_JWT_PRIVATE_KEY_FILE GATEWAY_WORKERS GRANT_WRITER_FUNCTION_NAME GRAPH_READ_BEARER IDENTITY_PROVIDER INTERNAL_READER_ROLE_ARN MAIL_BEARER MAIL_BEARER_LABELS
  MAIL_PDF_MAX_BYTES MAIL_SENDER_TABLE MASTER_ADMIN_EMAILS MASTER_ADMIN_PRINCIPALS MCPORTAL_CHANGES_TABLE MOCK_GRAPH MSP_CALLING_IDENTITIES MS_INGEST_BEARER MS_INGEST_BEARER_LABELS MS_INGEST_IDENTITY
  NFRA_OPLGTW_CONTRACT_PATH OTP_BEARER OTP_BEARER_LABELS OTP_MAILBOX PUBLIC_BASE_URL SCHWAB_ACCOUNT_REF_SECRET_ID SCHWAB_CATALOG_ROLE_ARN SCHWAB_EXTERNAL_IDS_SECRET_ID SCHWAB_READER_ROLE_ARN
  SPRINT_VIEW_ALLOWED_EMAILS TENANT_ID TRANSCRIPT_BEARER TRANSCRIPT_BEARER_LABELS TRANSCRIPT_MEETING_ALLOWLIST WRITE_CAPABLE_EMAILS WRITE_CAPABLE_PRINCIPALS.
- **After (the release's render): 46 keys, the same set** (`keys_cmp.py`: release 46, host 46, added [], removed []). `ENABLED_INTEGRATIONS` = `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond`, unchanged.

## Step 5 -- rollback built, not uploaded

- `/c/tmp/og-rb5` at `e3567ce5f7` (clean; `mcportal` = `a3bff71ffa`): `bun install --frozen-lockfile` + `bun run build`, then the deploy's tar step (`.scratch/build_art.sh`): 460,587 bytes, 94 files.
  The live S3 artifact: 460,595 bytes, 94 files (8-byte container difference). `diff -rq` of the two extracted trees: **empty, 94 of 94 identical**.
- The release artifact (same mirror on `/c/tmp/og-rel5`): **95 files**, 463,611 bytes; differs from live in exactly 3 (`app/mail_route.py`, `app/server.py` modified; `deploy/mail_sender_table.txt` new).
  `deploy-to-ec2.sh` and `tests/` are not in the tarball.
- **Re-deploy (rollback) command.** The live template still takes `OG_MAIL_SENDER_TABLE` from the shell (`_rl2.py` reads True on it), so the rolling-back shell exports it from `criterion.py` (A4 of OG-rl-1), never printed;
  the rosters are host-side already (R4), so no roster hand-off:
  `cd /c/tmp/og-rb5 && OG_MAIL_SENDER_TABLE="$(python -c 'import sys;sys.path.insert(0,".");from data.transcripts.scripts.outlook import criterion;print(",".join(criterion.DEFAULT_AUTHORS))')" DEPLOY_BASE_REF=<the live ref at that time = the release deploy commit, full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  It renders the same 46-key `.env` (table from the shell, equal to today's 3 items), restores the 94-file artifact, and leaves the shipped table file on the host unused (the service reads the environment).

## Rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W15-S16` (OBSERVATION, INERT: live moved to e3567ce5f7 before PHASE A; the cut is on it) and `NFRA_OPLGTW-Z-W15-S17` (OBSERVATION, INERT: the refusal runs after the extract).
This worktree's sparse cone gained `data/transcripts/scripts/outlook` (worktree-only, no tracked change; same as ~16's accepted row Z-W16-S3, not re-filed).

## At GO (PHASE B, not authorized)

Step 7: re-read the live ref (manifest, S3 `git-ref`, host md5); if it is not `e3567ce5f7`, re-cut `og-rel5` on it and re-run steps 1-6. Then the ledger `nfra-oplgtw-hx-mail-listing-release`, the before reads,
the act through `safe-ec2-deploy.sh`, and step 10 (host `MAIL_SENDER_TABLE` count = 3 at the cut, then `rl2.AC1.sh`). Inputs the issuer supplies at GO: the AC1 ids that script names.
