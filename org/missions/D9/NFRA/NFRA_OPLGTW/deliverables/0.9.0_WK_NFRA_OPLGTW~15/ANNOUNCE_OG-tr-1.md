# ANNOUNCE_OG-tr-1 -- PHASE A, `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-01 ~18:20Z

Nothing was uploaded, no secret was created, changed or written, no ledger is open, no manifest edit. The host was touched only by read-only SSM (5 commands, listed in the table). No secret value,
no full oid and no address is in this file.

**STANDING RULE (row Z-S32): nobody sources `/opt/opal-gateway/.env` in a shell. A key read uses names only (`grep -o '^[A-Z0-9_]*='`) or `/proc/<service pid>/environ` for one named key,
never echoed.** This cut obeyed it: `.env` key names and two booleans (value empty or not) come from a name-anchored parse; `FERNET_KEY` and `TOKEN_CACHE_DIR` were read from `/proc/<MainPID>/environ`
inside the host's own Python and used, never printed.

| item | value |
|---|---|
| live commit | `0a1d9079c682c640e619612f804257681c5db357` (EC2_MANIFEST `deployed_commit` on CLOUD, `deployed_at` 2026-10-01T15:34:29Z, OG-rl-2); S3 `opal-gateway-latest.tar.gz` metadata `git-ref` = the same sha, 463,612 bytes, 95 files |
| host md5 vs live commit | **92 of 92 files match** (0 mismatch; `app/**`, `deploy/**`, `requirements.txt`, `identity_tool_allowlist.txt` at `0a1d9079c6`); files named `*taxsma*` on the host: 0; `.env` 46 lines |
| identity | records read **6**; username matches **2 records, 1 distinct oid** (row W15-S19); Part D **MATCH**; oid prefix **`517aa5ee`** |
| release branch / tree | `rel-nfra-oplgtw-taxsma-route` at `/c/tmp/og-rel6` (sparse cone; `mcportal` seeded at the manifest pin `a3bff71ffa`, never staged) |
| release HEAD | `3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7` (2 commits on live: `b97c822b28` gateway files, `3a7d6a7dc8` deploy-to-ec2.sh) |
| rollback tree | `/c/tmp/og-rb6`, detached at `0a1d9079c6`, `mcportal` at the pin; artifact built, not uploaded |
| audited override | `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses, release-branch commits only: `b97c822b28`, `3a7d6a7dc8` |
| host reads (SSM) | md5 `3eebd9f4-85cc-4b20-a1df-c032498e55fb`; identity `b141c294-8b60-4526-b01a-8c83dce6efad` and owner-kind read (Success); verify script BEFORE `b893b5ab-1b75-475d-bc39-8521e5e02e63` and negative-control AFTER `119af030-0c1f-49dc-8f28-03ebb5163611` |

## Step 1 -- live commit by CONTENT

`md5sum` of every file the artifact ships from `/opt/opal-gateway` against `git show 0a1d9079c6:<file>`: **92 of 92 identical**. The S3 `git-ref` and the manifest agree.

## Step 2 -- the identity (Andrew ~17:3xZ, CTO 27992 (b)), BEFORE anything else

The token broker's store is Fernet-encrypted MSAL caches under `TOKEN_CACHE_DIR` (default `./.token_cache`, the service working directory; `app/token_broker.py`). The host read decrypted each cache in the
host's own process and printed, per account record, its oid and whether its `username` equals `opalbloomberg@opalinvest.com`.

- **Records read 6** (6 cache files, 1 account each). Oid prefixes and match booleans: `2e21f8e5` false, `2e21f8e5` false, `2844f2b9` false, `517aa5ee` **true**, `ad037ea5` false, `517aa5ee` **true**.
- **Matches: 2 records, ONE distinct oid.** The two matching records are the same person's two caches: one principal-keyed (`sha256("principal:<tid>/<oid>")`) and one email-keyed (`sha256("opalbloomberg@opalinvest.com")`,
  the server-held identity cache), as `_principal_owner` / `_email_owner` define. The order's literal "exactly ONE record" reads 2; the identity it protects reads 1 oid. **Filed as row W15-S19 for the issuer
  to confirm before PHASE B; I did not file it BLOCKING and I did not fix the identity into any file or upload.**
- **Part D cross-check: MATCH.** The matching oid equals the Part D value for `opalbloomberg@opalinvest.com` (`517aa5ee...`, WRITE_CAPABLE 2 of 2, `%LOCALAPPDATA%/opal/og-principals/part_d_20260930.json`),
  compared by equality on the host (`PART_D_EQUAL True`). The other WRITE_CAPABLE oid, `ad037ea5`, is a different record whose username is not opalbloomberg@. The identity value for PHASE B is `6810043e-d171-4adc-9975-068b35e179da/<that oid>`,
  taken from the Part D values file by a python eval, never printed.

## Step 3 -- release tree

- `git worktree add --no-checkout -b rel-nfra-oplgtw-taxsma-route /c/tmp/og-rel6 0a1d9079c6`, sparse cone, `mcportal` cloned from the rel5 copy and checked out at `a3bff71ffa`.
- `app/taxsma_workbook.py` (sha256 `6acc3e8ce895...`) and `tests/test_taxsma_workbook.py` (`810148fe5477...`) from CLOUD HEAD `37fcbfcac9`: both equal the order's checksums.
- `app/server.py`: the import (CLOUD line 65) and the `Route` with its 3-line comment (lines 966-969), inserted onto the LIVE bytes after `from .token_broker import NeedsLogin` and after the `/otp/health` route: +5 lines.
  `app/config.py`: the comment block and the two `TAXSMA_WORKBOOK_*` fields (lines 257-266) after `FIRM_ROLE_ARNS`: +10 lines. No other line of either file changed.
- **Census `git diff --stat 0a1d9079c6 HEAD`: 5 files, 1,736 insertions, 1 deletion** -- `app/taxsma_workbook.py` (new, 534), `tests/test_taxsma_workbook.py` (new, 1,165), `app/server.py` +5, `app/config.py` +10, `deploy-to-ec2.sh` +23/-1.
  `git diff --name-only | grep -vc ^infra/aws/ec2/opal-gateway/` = **0**; `app/ms_ingest.py` is not among them.
- The release artifact (`rel6_build`): 472,247 bytes, **96 files**; against the live S3 artifact (95 files) it differs in exactly 3: `app/config.py`, `app/server.py` modified, `app/taxsma_workbook.py` new.

## Step 4 -- tests on the release tree (`AUDIT_PATH` isolated per run, tree clean after)

- `tests/test_taxsma_workbook.py` **21 passed**, `tests/test_mail_route.py` **10 passed**, `tests/test_mail_listing.py` **12 passed** (rc 0). **`moto` 5.2.3 was already installed** (Python 3.14.7); no venv was needed.
- `tests/test_entitlement_admin.py::test_ogz2_ac08` **1 passed**: `DENOMINATOR 60 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)` on the release tree AND the same line on the LIVE tree (`/c/tmp/og-rb6`):
  **LIVE 60 + OWN 0 = 60** (the route is not an MCP tool). The host tool list after the release must equal BEFORE (65 names in the host's in-process list at the cut).

## Step 5 -- the template edit, hand-merged onto the LIVE `0a1d9079c6` template

- **Early read, release template:** `OG_TAXSMA_WORKBOOK_IDENTITY="${OG_TAXSMA_WORKBOOK_IDENTITY:-}"` is validated against `^[0-9a-fA-F-]{36}/[0-9a-fA-F-]{36}$` (the template's own pair pattern, anchored) at line 178, ahead of `base_guard_check "early"` (184),
  the mcportal build (211) and the first upload (230); a miss is `exit 3`, nothing uploaded. **On the LIVE template: no such check** (the live template has no `TAXSMA` and no `OG_` shell variable beyond one comment).
  Synthetic run of the extracted block (`.scratch/tr_check.py`, output `tr_check_out.txt`): unset **rc 3**, empty **3**, tid only **3**, oid only **3**, two pairs **3**, short oid **3**, a `;` **3**, one valid pair **rc 0**.
- **Host bearer block**, in the on-host script right after the roster check and before the extract: `TAXSMA_WORKBOOK_BEARER` from `aws secretsmanager get-secret-value --secret-id gateway/global/taxsma-workbook-token`,
  `|| exit 3` on a failed read, `exit 3` on an empty value or the CLI's `None`. Synthetic run with a stubbed `aws`: read fails (rc 255) **rc 3**, empty **3**, `None` **3**, a value **rc 0**.
  The refusal precedes the tar extract, the `.env` write and the restart (printed positions, all True).
- **Render:** live 15 `%s`, 15 arguments, 46 keys; release **17 `%s`, 17 arguments, 48 keys, 48 unique**. The two new lines `TAXSMA_WORKBOOK_BEARER=%s` and `TAXSMA_WORKBOOK_IDENTITY=%s` end the format (after `MSP_CALLING_IDENTITIES=`),
  their two arguments end the list, key to argument checked. The existing 46 lines, their 15 arguments and `ENABLED_INTEGRATIONS` are unchanged and in order. `bash -n` rc 0.
- Neither value is echoed: the on-host script prints the bearer's length only.

## `.env` key census, names only (host read b893b5ab, MainPID 525830 active, `/health` 200)

- **Before (live host): 46 keys** -- AUDIT_S3_BUCKET AWS_REGION BIND_HOST BIND_PORT BLACKDIAMOND_READER_EXTERNAL_ID BLACKDIAMOND_READER_ROLE_ARN CLIENT_ID CLIENT_SECRET DASHBOARD_OWNER_EMAILS ENABLED_INTEGRATIONS FERNET_KEY FIRM_ROLE_ARNS
  GATEWAY_JWT_PRIVATE_KEY_FILE GATEWAY_WORKERS GRANT_WRITER_FUNCTION_NAME GRAPH_READ_BEARER IDENTITY_PROVIDER INTERNAL_READER_ROLE_ARN MAIL_BEARER MAIL_BEARER_LABELS MAIL_PDF_MAX_BYTES MAIL_SENDER_TABLE MASTER_ADMIN_EMAILS
  MASTER_ADMIN_PRINCIPALS MCPORTAL_CHANGES_TABLE MOCK_GRAPH MSP_CALLING_IDENTITIES MS_INGEST_BEARER MS_INGEST_BEARER_LABELS MS_INGEST_IDENTITY NFRA_OPLGTW_CONTRACT_PATH OTP_BEARER OTP_BEARER_LABELS OTP_MAILBOX PUBLIC_BASE_URL
  SCHWAB_ACCOUNT_REF_SECRET_ID SCHWAB_CATALOG_ROLE_ARN SCHWAB_EXTERNAL_IDS_SECRET_ID SCHWAB_READER_ROLE_ARN SPRINT_VIEW_ALLOWED_EMAILS TENANT_ID TRANSCRIPT_BEARER TRANSCRIPT_BEARER_LABELS TRANSCRIPT_MEETING_ALLOWLIST
  WRITE_CAPABLE_EMAILS WRITE_CAPABLE_PRINCIPALS. `ENABLED_INTEGRATIONS` = `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond`.
- **After (the release's render): 48 keys** = the same 46 + `TAXSMA_WORKBOOK_BEARER` + `TAXSMA_WORKBOOK_IDENTITY`; removed none; `ENABLED_INTEGRATIONS` unchanged.

## Step 6 -- rollback built, not uploaded

- `/c/tmp/og-rb6` at `0a1d9079c6` (clean; `mcportal` = `a3bff71ffa`): `bun install --frozen-lockfile` + `bun run build`, then the deploy's tar step (`.scratch/build_art.sh`): 463,577 bytes, **95 files**.
  The live S3 artifact (downloaded and extracted): 463,612 bytes, 95 files (35-byte container difference). `diff -rq` of the two extracted trees: **empty, 95 of 95 identical**.
- **Re-deploy (rollback) command.** The live template needs NOTHING from the shell (rosters, sender table and every bearer are read host-side; no `OG_` variable is used), so:
  `cd /c/tmp/og-rb6 && DEPLOY_BASE_REF=<the live ref at that time = the release deploy commit, full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  It renders the same 46-key `.env` (no TAXSMA lines: capability OFF again, the route module absent) and restores the 95-file artifact.

## Step 10 -- the PHASE B verify script, written now (rows W15-S20, S21)

`tr_verify.py` / `tr_verify.sh` / `tr_release_md5.txt` in this folder. `tr_verify.sh before <state.json>` before the act; `tr_verify.sh after <state.json>` immediately after the deploy returns: one SSM host read (/health, 93-file md5 against the release bytes, tool list,
`.env` key names 46 -> 48 and the other 46 unchanged, both TAXSMA keys non-empty, `ENABLED_INTEGRATIONS`, 8 `/ms/*` `/hx/*` `/otp/*` `/mcp` probe codes against BEFORE, the route's no-bearer 401), then `tr.AC1.sh`. Exercised now on the live
(un-deployed) host: BEFORE saved (keys 46, tools 65, route 404); the AFTER run is the negative control, **VERIFY FAIL 4 of 8** with exactly the three md5 files, the key count, the two TAXSMA keys and the route refusal failing, and the 4 unchanged checks passing.

## Rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W15-S19` (identity: 2 records, 1 distinct oid), `-S20` (the order's "row W15-S18" id is already taken; the verify script is filed here), `-S21` (the identity value rides SSM command text and step 2's SSM output carried the full oid);
all OBSERVATION, INERT.

## At GO (PHASE B, not authorized)

Re-read the live ref; if it is not `0a1d9079c6`, re-cut `og-rel6` and re-run steps 1-6. Then the ledger `nfra-oplgtw-taxsma-route-release`, `tr_verify.sh before`, the act through `safe-ec2-deploy.sh` with
`OG_TAXSMA_WORKBOOK_IDENTITY` exported by a python eval from the Part D values file, `tr_verify.sh after`, the manifest, the ledger close. Input needed from the issuer at GO: confirmation of row W15-S19 (2 records / 1 oid).
