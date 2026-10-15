# COO never-widen half -- COMM_ASSIST round 20, cell CA-l-4: deploy the narrower package (one targeted apply of `module.ldo_001`, CODE ONLY, the registry files cut from 17 to 12)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-15 (laptop). **Root:** `infra/aws/terraform/transcripts/`. **Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO`), each signed on the same pin. **Authority:** the CTO's round-19 analysis, ruling 2 (`ledger/ROUND_ANALYSIS.round19.md` @b4f6d499d0, msg 109356: package only the registry files the assistant reads; the foreign payload noted as C3 of the round-19 CTO half); PRD v0.10 FWD-4 and FWD-13; round-20 decomposition, cell CA-l-4. Adapted from the R19 half `NEVER_WIDEN_HALF_COO_COMM_ASSIST_R19_PENDING_DEPLOY_20261015.md` (CA-k-4, CLOSED).

**PIN:** `863dc0f739` (box/laptop, the trunk after CA-l-2 `c91b5dc61d` and CA-l-3 merged; CA-l-3 changes tests only, no packaged path). The pin is an ancestor of the trunk head read at this write (`17ac3101eb`, `git merge-base --is-ancestor`). Everything below that is measured was read at the PIN by `git diff --numstat 93a3f55d25..863dc0f739` over the packaged paths, by the author at ~08:1xZ on 2026-10-15; the issuer's figures are equal. Registry rows keep landing from other seats, so the pin is fixed and `check_m4_equiv.py` / `check_m4_live.py` compare at it.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z, with the package BUILT FROM A CLEAN DETACHED CHECKOUT AT THE PIN. It changes **code only**: `build.sh` now copies the twelve registry files named in `registry_files.txt` instead of all seventeen, so the zip holds 34 files, not 39. No environment value, policy, secret, Terraform resource or image moves, and no packaged code file (`handlers.py`, `ldo.py`, `teams_chat/`, `daily_reports/eod`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`) changes.

**Live pre-state, read by the author read-only at 2026-10-15T08:13Z** (`.tools/aws lambda get-function-configuration --function-name teams-global-chat-assist-{handler,ingress}-lambda`, and `.tools/aws sqs get-queue-attributes` on `teams-global-chat-assist-dlq.fifo`):

| item | handler | ingress |
|---|---|---|
| `CodeSha256` | `nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k=` | `nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k=` |
| `LastModified` | 2026-10-15T05:56:32Z | 2026-10-15T05:56:24Z |
| `CodeSize` | 320236 | 320236 |
| `INGRESS_MARK_MODE` | `enforce` | `enforce` |
| environment key names | 15 (as recorded in `r19/AFTER_*_config.json`) | 15 (same) |

The served zip (downloaded from `get-function` `Code.Location`) hashes to that `CodeSha256`, holds 39 files, 17 of them registry files; it is the CA-k-4 package built at `93a3f55d25`. The dead-letter queue `teams-global-chat-assist-dlq.fifo` reads `ApproximateNumberOfMessages` 0 and `ApproximateNumberOfMessagesNotVisible` 0. The trunk's Terraform default `chat_assist_ingress_mark_mode` reads `enforce` at the pin and at `93a3f55d25` (`chat_assist.tf`:41), equal to live, so a plan shows no environment change; the CA-k-2 gate in `safe-apply.sh` (`.tools/ldo001-mode-default-check.py`) must print `LDO001-MODE verdict=OK default=enforce live=enforce` (a `REFUSED` or `NO-VERDICT` is Branch B). `git diff --numstat 93a3f55d25..863dc0f739` over `infra/aws/terraform/transcripts` and `infra/aws/terraform/modules/ldo` is empty.

## What becomes live: the packaged-path diff `93a3f55d25..863dc0f739` (C-PACKAGE), numstat read at the pin `863dc0f739`

Read over the packaged paths (`handlers.py`, `modules/ldo/runtime/ldo.py`, `teams_chat/`, `daily_reports/eod`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`, `infra/logic/registry`, the transcripts root, `modules/ldo`):

| path | lines | what it does live |
|---|---|---|
| `infra/logic/registry/legacy_addresses.json` (FOREIGN) | +100 -0 | rows from `4.0.0_SA_CRO~Z` (`f636989b97` +90, nine `gateway-etfs-*` rows; `bb0e3bd764` +10, one `gateway-portal-tiered-market-overview` row); the assistant opens this file, so the rows ride the package; whether they move any S3 address it forms is read by the 17 probes |
| `infra/logic/registry/reporting_policies.json` (FOREIGN) | +2 -1 | one row edit from `0.9.0_WK_IRPT_BCKEND~397` (`df2468cbc8`, the filled-report object), same reason |
| `infra/logic/registry/catalog_fork_keys.json` | LEAVES the package (4954 lines in the repo) | the NFRA_MCPINDEX rows; not opened by the assistant |
| `infra/logic/registry/event_rules.json` | LEAVES (88 lines) | not opened by the assistant |
| `infra/logic/registry/key_rulings.json` | LEAVES (1643 lines) | not opened by the assistant |
| `infra/logic/registry/name_rulings.json` | LEAVES (920 lines) | not opened by the assistant |
| `infra/logic/registry/root_map.json` | LEAVES (2281 lines) | not opened by the assistant |
| every other packaged path (`handlers.py`, `ldo.py`, `teams_chat/`, `daily_reports/eod`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`) and `infra/aws/terraform/transcripts`, `infra/aws/terraform/modules/ldo` | 0 | unchanged |

The five files that leave are still in the repo; only the manifest `infra/aws/lambda/teams-chat-assist/registry_files.txt` (twelve names: `exemptions`, `feeds`, `firm_pages`, `legacy_addresses`, `mail_parties`, `platinum_destinations`, `remediations`, `reporting_policies`, `resources`, `scopes`, `systems`, `tiers`) does not list them. The build inputs `build.sh` (+10 -1) and `registry_files.txt` (+15) are not packaged and not in the zip. The file count goes 39 -> 34; the packaged registry files 17 -> 12. `check_m4_equiv.py` reads where the change acts: the built package against the zip served NOW (live-only files exactly the five dropped, built-only none, every other file equal but the two foreign files, the registry list equal to the manifest, and the 17 probes equal). The issuer's `check_m2_build.py` read at the merge that the twelve are the files a trace of the 17 probes and every packaged module import opens plus the files the packaged code names.

## What changes for Andrew

Nothing he sees. The assistant forms the same S3 addresses and considers the same mail parties (the 17 probes), and the texts, tags, drafts, `pending` and `pending_list`, the ingress mark and the environment are untouched. The package is about 85 KB smaller (the zip reads 320236 bytes today; a build from the trunk with the manifest measured 235445 bytes).

## Named residual

A registry file the assistant opens LAZILY, on a code path none of the 17 probes or the module imports exercises, would not be in the package and would fail at run time (a missing file), where today it is read from the full set. The static scan and `opal_naming.REGISTRY_FILES` narrow that gap and cannot close it. The guards: the served-code probes of `check_m4_live.py` (the mark checks, the mention and mail records, the two-mail probe, and the 17 probes against the SERVED zip), the log read ten minutes on (no error), the dead-letter queue unchanged, and the rollback, which is one targeted apply back to the saved package. The manifest header tells the next editor to add a registry file the assistant starts to read.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only; changed keys a subset of {`source_code_hash`, `last_modified`} and NEVER `environment`; the after-hash equals the built package. No policy, role, secret, key or other address. Then apply that saved plan through `bash .tools/safe-apply.sh`.
- **B:** anything else, in which case apply NOTHING and report: any add, destroy or replacement; any other address or argument; an `environment` change (the mode must read `enforce` before and after); an `init` migrate or reconfigure prompt; a pre-state hash other than `nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k=` or a mode other than `enforce` (another writer moved something); the CA-k-2 gate reading anything but `verdict=OK`; the build not made from a clean checkout at the pin, or a built zip that does not hold 34 files; `check_m4_equiv.py` not reading `ok=True`; the import test failing against the built `dist/pkg`; `check_j5_obs.py` reading `DIRTY` for a non-`probe:` object; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; less than 5 GB free on `C:`; any `-var`.

## Rollback, per key

- **Code:** save the live zip BEFORE the act (the `/nQlJW0j...` package: `get-function` `Code.Location` download, its sha256 and base64 sha256 recorded, into `deliverables/0.7.0_AE_CloudOps~CA/r20/`), copy it over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a detached worktree at `93a3f55d25` (the commit the live package was built from; its Terraform default is `enforce`, so the mode stays `enforce`). The plan reads 0/2/0 back to hash `nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k=` with no environment change. NEVER from a commit whose default is `record` (`afa8752f44`). No `-var`. This is the CA-k-4 package, 39 files.
- **State:** this act writes no state and touches no state key; a rollback loses nothing (the R19 CVO note on reconciling `pending_list` after a rollback applied to the list code, which stays in both packages).

## Conditions (carried from the R19 halves, all adopted; none added)

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`. The CA-k-2 gate line must read `LDO001-MODE verdict=OK default=enforce live=enforce`; never set `LDO001_MODE_OVERRIDE`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values), the live zip saved with hashes, and the dead-letter queue counts (0 and 0 at this write). The NEVER-2 entry `comm-assist-r20-narrow-deploy`, naming both functions (code only; no image), is opened and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_m4_equiv.py` reads `ok=True` with `M4_PIN=863dc0f739`, and `check_j5_obs.py` is run and its output saved (it must NOT read `DIRTY`; the `probe:` row is counted apart). AFTER, live: `check_m4_live.py` reads PASS. A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`, neither function log shows an error or `AccessDenied`, and the dead-letter queue reads UNCHANGED from the BEFORE read (any rise is a rollback the same hour).
4. The secret's VALUE is never read. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. Not 20:00Z-21:45Z, and no End of Day event in flight; the apply lands before 19:30Z or waits until the window has closed. The mode stays `enforce`.
6. DISK: before `git worktree add`, `df` on `C:` must read at least 5 GB free (24 GB at this write). Below that: create nothing, stop and report; do not clean up files to make room.
7. ONE SITTING: the applier begins only when it can finish apply, AFTER reads, re-plan and ledger close in one sitting; a stalled half-landed apply is the NEVER-2 case, so a seat stopped on a spend limit does not begin.

**BLIND, stated:** a registry file opened lazily on a path the 17 probes do not exercise is not in hand (see the named residual); the real Teams and mail traffic after the apply is not exercised by the act, which sends no test mail. The served-code probes run against the SERVED zip on `probe:` objects and stand-in contexts and read nothing of Andrew's.

**SIGNED** -- `2.0.0_SA_COO~CA`
