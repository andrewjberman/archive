# COO never-widen half -- COMM_ASSIST round 19, cell CA-k-4: deploy the mail object's list of open drafts (one targeted apply of `module.ldo_001`, CODE ONLY, two packaged files)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-15 (laptop). **Root:** `infra/aws/terraform/transcripts/`. **Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`), each signed on the same pin. **Authority:** the CTO's round-18 analysis, ruling 2 (`ledger/ROUND_ANALYSIS.round18.md` @5e4395ae5c, msg 109267); PRD v0.10 FWD-4 (the draft loop) and FWD-13 (an alert for each mail); round-19 decomposition, cell CA-k-4 and AMENDMENT 1.

**PIN:** `93a3f55d25` (box/laptop, the trunk after CA-k-1 `2d0a8f5027`, CA-k-2 `d128627a96` and CA-k-3 merged; CA-k-3 changes no packaged path)
Everything below that is measured was read at the PIN `93a3f55d25`, by `git diff --numstat 0774100edc..93a3f55d25` over the packaged paths (the issuer's re-read at ~01:3xZ on 2026-10-15; the foreign registry file grew from +4736 at `d128627a96` to +4954 at the pin because other seats merged rows in between, which is why the pin is fixed and the equivalence check reads the 17 probes at it). The two packaged files change only in CA-k-1 (`41cd03765f`).

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z, with the package BUILT FROM A CLEAN DETACHED CHECKOUT AT THE PIN. It changes **code only**, two packaged files (`mail_requests.py`, `tenant.py`): no environment value, no policy, no secret, no Terraform resource, no image.

**Live pre-state, read by the issuer read-only at ~01:4xZ on 2026-10-15** (`.tools/aws lambda get-function-configuration`, both functions): `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `BBiNwhfKGcPciG5+zFa2KCIsJ/kF18g+x4ozNN2EnIA=` (the CA-j-14 package, `CodeSize` 297733, `LastModified` 2026-10-14T15:46:59Z handler and 15:47:05Z ingress, built at `0774100edc`; ledger `comm-assist-r18-records-deploy` CLOSED, entry `20261014T1540Z_comm-assist-r18-records-deploy_deploy_completion.md`) and `INGRESS_MARK_MODE=enforce`, the same fifteen environment key names as recorded in `deliverables/0.7.0_AE_CloudOps~CA/r18e/AFTER_ingress_config.json`. The trunk's Terraform default `chat_assist_ingress_mark_mode` reads `enforce` too, so a plan from the trunk shows no environment change; the CA-k-2 gate in `safe-apply.sh` (`.tools/ldo001-mode-default-check.py`) reads default against live and must print `LDO001-MODE verdict=OK default=enforce live=enforce` (a `REFUSED` or `NO-VERDICT` is Branch B).

## What becomes live: the packaged-path diff `0774100edc..HEAD` (C-PACKAGE), numstat read at the pin `93a3f55d25`

| path | lines | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/mail_requests.py` | +54 -6 | each considered mail APPENDS an entry to `ctx.state["pending_list"]` (the open drafts, oldest first); `state["pending"]` stays and holds the newest; a new mail's tag never repeats an open tag; the same mail again replaces its own entry; on every write entries older than 7 days drop and the newest 20 stay (`folder_records.prune`); the reply helpers (find by tag, set newest, remove) |
| `data/transcripts/scripts/teams_chat/tenant.py` | +20 -4 | `on_sms_reply` (mail branch) and `on_muse_reply` resolve the entry by tag; `open_items` lists every open draft |
| `lib/opal_naming.py` (FOREIGN) | +18 -2 | another seat's builder block (`MDPF_GLOBAL_VIEW_FIRMS`, `4.0.0_SA_CRO~DELL1`, commit 21426addd0); packaged because `build.sh` copies it; whether it moves any S3 address the assistant forms is read by the 17 probes below |
| `infra/logic/registry/catalog_fork_keys.json` (FOREIGN) | +4954 | NFRA_MCPINDEX registry rows (`2.0.0_SA_COO~MI` MX-c-12/14 workers), packaged because `build.sh` copies the whole registry |
| `infra/logic/registry/legacy_addresses.json` (FOREIGN) | +1516 | registry rows from `4.0.0_SA_CRO~DELL1` and NFRA_MCPINDEX, packaged for the same reason |
| `infra/logic/registry/exemptions.json` (FOREIGN) | +24 | registry rows from `4.0.0_SA_CRO~DELL1` and NFRA_MCPINDEX, packaged for the same reason |
| every other packaged path (`handlers.py`, `ldo.py`, the other `teams_chat` files, `daily_reports/eod`, `NAMING_SCHEMA.json`) and `infra/aws/terraform/transcripts`, `infra/aws/terraform/modules/ldo` | 0 | unchanged |

`check_l4_equiv.py` reads where the foreign paths act: it builds the same 17 probes (the S3 addresses for a fixed battery of chats and the mail parties) from the built and the served package and requires them equal; the foreign count it prints is 4 at the pin. The reader file `data/transcripts/scripts/muse_reader/refresh.py` also changed in CA-k-1 but is NOT packaged and not part of this act. The text sent to Andrew, the tags, `draft_seq`, `mail_log`, the mention record, the ingress mark and the environment are untouched (CA-k-1's `check_l1_pending` 15 of 15, `check_i2_regression` 64 passed, `check_k2_reader` 7 of 7 at the merge).

## What changes for Andrew

Nothing he sees now. When two considered mails arrive close together, BOTH drafts stay open (today the second REPLACES the first and the first can no longer be answered); his reply by tag (`#M123 1`, `0`, notes) acts on that draft only, a signed answer binds to its tagged entry, and the "what is waiting" list shows every open draft. The texts are unchanged. The one new failure mode, named: the list code runs inside the mail handler, so an exception in it fails that mail event (the queue retries it, then dead-letters it). It is straight-line code over a small list and covered by 15 issuer arms plus the unit tests, and `check_l4_live.py` runs it against the SERVED code before the act is called done.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only; changed keys a subset of {`source_code_hash`, `last_modified`} and NEVER `environment`; the after-hash equals the built package. No policy, role, secret, key or other address. Then apply that saved plan through `bash .tools/safe-apply.sh`.
- **B:** anything else, in which case apply NOTHING and report: any add, destroy or replacement; any other address or argument; an `environment` change (the mode must read `enforce` before and after); an `init` migrate or reconfigure prompt; a pre-state hash other than `BBiNwhfKGcPciG5+zFa2KCIsJ/kF18g+x4ozNN2EnIA=` or a mode other than `enforce`; the CA-k-2 gate reading anything but `verdict=OK`; the build not made from a clean checkout at the pin; `check_l4_equiv.py` not reading `ok=True`; the import test failing against the built `dist/pkg`; `check_j5_obs.py` reading `DIRTY` for a non-`probe:` object; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; less than 5 GB free on `C:` (below); any `-var`.

## Rollback, per key

- **Code:** save the live zip BEFORE the act (the `/BBiNwhfK...` package: `get-function` `Code.Location` download, its sha256 and base64 sha256 recorded, into `deliverables/0.7.0_AE_CloudOps~CA/r19/`), copy it over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a detached worktree at `0774100edc` (the commit the CA-j-14 package was built from; its Terraform default is `enforce`, so the mode stays `enforce`). The plan reads 0/2/0 back to hash `BBiNwhfKGcPciG5+zFa2KCIsJ/kF18g+x4ozNN2EnIA=` with no environment change. NOT from a commit whose default is `record` (`afa8752f44`). No `-var`. This is the CA-j-14 package.
- **State:** the only state key the new code writes is `pending_list` on mail objects; the CA-j-14 code ignores it and keeps reading `pending`, which the new code keeps equal to the newest open entry. A rollback therefore loses no draft that `pending` already holds; drafts held only in `pending_list` stay stored, unanswerable by tag under the old code until the redeploy.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values), the live zip saved with hashes, and the dead-letter queue `teams-global-chat-assist-dlq.fifo` `ApproximateNumberOfMessages` and `ApproximateNumberOfMessagesNotVisible` (the last read before this deploy: 0 and 0, `r18e/BEFORE_dlq_counts.json`). The NEVER-2 entry `comm-assist-r19-pending-deploy`, naming both functions (code only; no image), is opened and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_l4_equiv.py` reads `ok=True` with `K4_PIN=93a3f55d25`, and `check_j5_obs.py` is run and its output saved (it must NOT read `DIRTY`; the `probe:` row is counted apart). AFTER, live: `check_l4_live.py` reads PASS (one new package; every served file equals the pin; `INGRESS_MARK_MODE=enforce` and the fifteen key names; the served-code probe keeps both of two mails). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`, neither function log shows an error or `AccessDenied`, and the dead-letter queue reads UNCHANGED from the BEFORE read.
4. The secret's VALUE is never read. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. Not 20:00Z-21:45Z, and no End of Day event in flight. The mode stays `enforce`; nothing in this act touches it.
6. NEW DISK PRECONDITION: the pinned worktree and the build need room. Before `git worktree add`, `df` on `C:` must read at least 5 GB free (the laptop read 5.9 GB free at 98% used at this write). Below that: create nothing, stop and report; do not clean up files to make room.

**BLIND, stated:** a real considered mail pair is not in hand (calls 44eb and e435 are Andrew's), so the list is exercised by the served-code probe and the unit tests, not by live traffic. The issuer's close run is a served-code probe on a `probe:` object: two stand-in mails inside one minute both keep their drafts, read by object and seq and never by content, no text sent. The dell2 reader's own pick-up of the per-draft rows rides the box pass, not this act.

**SIGNED** -- `2.0.0_SA_COO~CA`
