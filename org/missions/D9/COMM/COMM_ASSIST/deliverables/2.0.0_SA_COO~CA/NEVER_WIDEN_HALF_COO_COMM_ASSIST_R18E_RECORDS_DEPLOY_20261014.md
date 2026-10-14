# COO never-widen half -- COMM_ASSIST round 18, cell CA-j-14: deploy the assistant's two metadata-only records (one targeted apply of `module.ldo_001`, CODE ONLY, three files)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~15:5xZ (laptop). **Read at:** `box/laptop` `0774100edc` (THE PIN: the trunk after CA-j-12, CA-j-13 and CA-j-17 merged). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CTO's ruling on call 608c (`RULING_20261014_124xZ_COMM_ASSIST_608C_FWD13_TWO_SCRUBBED_RECORDS.md`, msg 109140): the assistant may keep two small records, METADATA ONLY, written where the item is texted today, 7-day expiry on write, the negative arm unchanged; PRD v0.10 FWD-13; round-18 decomposition AMENDMENT 8.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z, with the package BUILT FROM A CLEAN DETACHED CHECKOUT AT `0774100edc`. It changes **code only**: no environment value, no policy, no secret, no Terraform resource.

**Live pre-state, read by the issuer at ~15:5xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `/amW90t7TNsAAcx8Ap0t/eD7Jgk1HAOXJHCv8t8Mkho=` (the CA-j-10 package, unchanged by the CA-j-5 flip) and `INGRESS_MARK_MODE=enforce` (CA-j-5, ledger `comm-assist-r18-enforce-deploy` CLOSED @4dddae3aad). The trunk's `chat_assist.tf` default now reads `enforce` too (merged @0774100edc), so a plan from the trunk shows no environment change.

## What becomes live: the packaged-path diff `afa8752f44..0774100edc` (C-PACKAGE)

| path | lines | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/folder_records.py` (new) | +61 | `snippet(text, limit=120)`: strips tags, collapses whitespace, REMOVES links, anything shaped like an address and any run of 20 or more key-like characters, cuts to 120; and `prune(...)`: drop older than 7 days, keep the newest N |
| `data/transcripts/scripts/teams_chat/channel_mentions.py` | +23 -2 | where a mention is TEXTED (never on the paused path), `ctx.state["mentions"]` gains one entry `{id, team, channel, from, snippet, mentioned_at, seen_at}`; a repeat id adds nothing; 7-day expiry and the newest 50 on write |
| `data/transcripts/scripts/teams_chat/mail_requests.py` | +15 | for each CONSIDERED mail, `ctx.state["mail_log"]` gains `{seq, tag, considered_at, from, domain, firm, subject}`; never the body, never an address; 7-day expiry and the newest 10 on write |
| `infra/aws/terraform/transcripts/chat_assist.tf` (Terraform, not packaged) | +1 -1 | the variable default `enforce`: it equals the live environment, so no environment change |
| `infra/logic/registry/event_rules.json` (FOREIGN, +6) | | another seat's registry row (`4.0.0_SA_CRO~DELL1`, an exec-summary trigger name) that ships in every build because `build.sh` copies the whole registry; `check_k3_equiv.py` reads where it acts: 17 probes (the S3 addresses for a fixed battery of chats and the mail parties) between the built and the live package |

`numstat` over every other packaged path and `infra/aws/terraform/modules/ldo`: 0 lines. The text sent to Andrew, the drafts, `state["pending"]`, `draft_seq` and the marks are untouched (the issuer's `check_k1_records` and the assistant's flow tests read this at the merge: K1 8 of 8, `check_i2_regression` 64 of 64, the whole set 562 passed).

## What changes for Andrew

Nothing he sees. The records are written to state rows and read later by the dell2 reader (cell CA-j-15); no text, draft or alert changes. The one new failure mode, named: the two writers run inside the mention and mail handlers, so an exception in one would fail that event (the queue retries it and then dead-letters it). Both writers are straight-line code over small lists, covered by unit tests, and `check_k3_live.py` runs both against the SERVED code before the act is called done. The mention writer runs AFTER the text is sent and its once-record is set, so a retry cannot text twice.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only; changed keys a subset of {`source_code_hash`, `last_modified`} and NEVER `environment`; the after-hash equals the built package. No policy, role, secret, key or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report: any add, destroy or replacement; any other address or argument; an `environment` change (the mode must read `enforce` before and after); an `init` migrate or reconfigure prompt; a pre-state hash other than `/amW90t7...` or a mode other than `enforce`; the build not made from a clean checkout at `0774100edc`; `check_k3_equiv.py` not reading `ok=True`; the import test failing against the built `dist/pkg`; `check_j5_obs.py` reading `DIRTY` for a non-`probe:` object (the CTO's C3 reading, applied before any further change to the live handler); the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`.

## Rollback, per key

- **Code:** the live zip downloaded before the act (`/amW90t7...`), copied over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a detached worktree at `8c5e0b278e` (the live package's code with the `enforce` default; its branch `enforce-pin-j5` is kept for exactly this). The plan reads 0/2/0 back to that hash with no environment change. NOT from `afa8752f44`, whose default is `record` and would flip the mode. No `-var`.
- **State:** the only state keys the new code writes are `mentions` and `mail_log` on objects that handle a mention or a considered mail; the older code ignores them.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values) and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r18-records-deploy`, naming both functions (code only; no image), is opened, and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_k3_equiv.py` reads `ok=True` with `J14_PIN=0774100edc` (the three CA-j-12 files are in the packaged diff and equal the pin's bytes, the Terraform file and the registry file counted as foreign, and 17 of 17 probes equal), and `check_j5_obs.py` is run and its output saved. AFTER, live: `check_k3_live.py` reads PASS (one new package; the served zip equals the pin on eight files; `INGRESS_MARK_MODE=enforce` in both environments and the other keys as recorded; the key policy intact is read by `check_j5_live.py`; the served code runs the mark checks, writes a clean mention record and a clean mail record). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`, and neither function log shows an error or `AccessDenied`.
4. The secret's VALUE is never read. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. Not 20:00Z-21:45Z, and no End of Day event in flight. The mode stays `enforce`; nothing in this act touches it.

**BLIND, stated:** a real `@mention` and a real mail are not in hand (calls 44eb and e435 are Andrew's), so the records are exercised by the served-code probe and the unit tests, not by live traffic, until the dell2 pick-up and the FWD-13 exercise (cells CA-j-15 and CA-j-16).

**SIGNED** -- `2.0.0_SA_COO~CA`
