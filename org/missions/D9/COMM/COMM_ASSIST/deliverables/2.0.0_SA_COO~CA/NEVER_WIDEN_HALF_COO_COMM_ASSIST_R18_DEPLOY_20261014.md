# COO never-widen half -- COMM_ASSIST round 18, cell CA-j-3: deploy the ingress mark (the secret shell, its value out of band, then one targeted apply of `module.ldo_001`)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~04:3xZ (laptop). **Read at:** `box/laptop` `38ce5a7981` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CTO's round-17 analysis item 1 (`ledger/ROUND_ANALYSIS.round17.md`, row `W10-S2`, P1: the SMS ingress mark; his ruling `CTO_RULING_20261013_231xZ_COMM_ASSIST_SMS_FORGERY_AND_J290_DRAFTS.md`); PRD v0.7; the round-18 decomposition cell CA-j-3 (`COMM_ASSIST_DECOMP.round18.md`).

## The act, in THREE steps by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z, all from a clean DETACHED worktree at `38ce5a7981`

The order is three steps so that no function runs the new code while the secret has no value (the producers read the secret on every text): the secret shell first, its value second, the code last.

1. **The shell.** ONE `safe-apply`, TARGETED at exactly `aws_secretsmanager_secret.ca_ingress_mark`: creates the secret `teams/global/ingress-mark` (name from the `NAMES.json` row), no value.
2. **The value, out of band.** The seat generates 32 random bytes (hex) into a file OUTSIDE every git tree, puts it with `aws secretsmanager put-secret-value --secret-id teams/global/ingress-mark --secret-string file://<that file>`, deletes the file, and never prints, logs, commits or sends the value. It then reads `describe-secret` (an `AWSCURRENT` version exists; the value is never read back).
3. **The code, the mode and the grant.** ONE `safe-apply`, TARGETED at exactly `module.ldo_001`, from the package BUILT FROM THE CLEAN DETACHED CHECKOUT AT `38ce5a7981`.

**Live pre-state, read by this seat at ~04:2xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `sWltfUwyJQpANEhbY+KFkszo8ScLKEIi7Lm4qyUNWrM=` (the third r17 deploy, pin `abc5ad424a`, ledger `comm-assist-r17c-deploy` CLOSED @33c61626c2), read by `check_j3_live.py` (its first two lines). The secret `teams/global/ingress-mark` does not exist (`describe-secret` returns `ResourceNotFoundException`). The environment carries no `INGRESS_MARK_MODE`.

## What becomes live: the packaged-path diff `abc5ad424a..38ce5a7981` (C-PACKAGE)

| path | lines | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/ingress_mark.py` (new) | +71 | stdlib `stamp`/`verify` of an HMAC-SHA256 mark over object id, kind, mark time and the canonical payload; `verify` returns `ok`, `no-mark`, `bad-mark` (constant-time compare) or `stale-mark` (older than 15 minutes or more than 5 ahead) |
| `data/transcripts/scripts/teams_chat/tenant.py` | +46 -6 | the four producers of `sms.reply`/`owner.text` (ingress `_route_commands` x2, handler `on_owner_text`, `on_owner_reply`) stamp their payload; `dispatch` checks the mark in the mode `INGRESS_MARK_MODE` gives (`off`/`record`/`enforce`; unset is `off`; a typo raises) and records `mark_refusals`, `unmarked_seen`, `marks_seen` (reason and time only, never a secret, mark or payload) |
| `data/transcripts/scripts/teams_chat/NAMES.json` | +2 -1 | the row `secrets.ingress_mark` = `teams/global/ingress-mark` |
| `infra/aws/terraform/transcripts/chat_assist.tf` (Terraform, not packaged) | +13 | the secret shell, the secret in `secret_arns`, the variable `chat_assist_ingress_mark_mode` default `record`, and `INGRESS_MARK_MODE` in the environment |
| `infra/logic/registry/legacy_addresses.json` (FOREIGN, +60) | | six registry rows another project added for its own S3 prefixes; it rides the package. `check_j3_equiv.py` reads where it acts: 17 of 17 probes (S3 addresses for a fixed battery of chats and the mail parties) are identical between the built package and the live one |

`numstat` over every other packaged path and `infra/aws/terraform/modules/ldo`: 0 lines. No other file rides this package.

## What changes for Andrew

Nothing he sees. In `record` mode every text still acts as today; the handler only counts a missing or bad mark. The mode flips to `enforce` only in cell CA-j-5, after a stated observation window and a second never-widen set.

## Expected plans, BOTH branches

- **Step 1 A:** `1 to add, 0 to change, 0 to destroy`, exactly `aws_secretsmanager_secret.ca_ingress_mark` (name `teams/global/ingress-mark`, no policy, no version). **Step 1 B:** anything else (a change, a destroy, any other address, a name other than the row's).
- **Step 3 A:** targeted `0 to add, 3 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler`, `module.ldo_001.aws_lambda_function.ingress[0]` and `module.ldo_001.aws_iam_policy.exec`. On each Lambda the changed keys are within {`source_code_hash`, `last_modified`, `environment`}, and `environment` differs ONLY by the added key `INGRESS_MARK_MODE = "record"` (every other value, key names and `MUSE_ANSWER_PUBKEY`, `MAIL_BEARER_SECRET`, `SMS_ORIGINATION` identical); the after-hash equals the built package. On the policy the only change is the `Secrets` statement's `Resource` gaining the new secret's ARN. Then apply that saved plan.
- **Step 3 B:** anything else, in which case apply NOTHING and report: an add, destroy or replacement; any other address or argument; an `environment` change other than the one key; a policy change other than the one ARN; an `init` migrate or reconfigure prompt; a pre-state hash other than `sWltf...`; the build not made from a clean checkout at `38ce5a7981`; `check_j3_equiv.py` not reading `ok=True`; the import test failing against the built `dist/pkg`; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`; the secret having no `AWSCURRENT` version.

## Rollback, per key

- **Code and environment (step 3):** the live zip downloaded before the act (`sWltf...`), copied over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a worktree at `abc5ad424a`'s Terraform (no `INGRESS_MARK_MODE`, the policy without the ARN); the plan reads 0/3/0 back. No `-var`. The seat records the hash it returns to.
- **Secret (steps 1-2):** left in place; it is read by nothing once the code is rolled back. If the whole mark is withdrawn, `aws secretsmanager delete-secret --secret-id teams/global/ingress-mark` (30-day recovery window) is a separate act under its own word, never part of a rollback.
- **State:** the only state keys written are the handler's `marks_seen`, `mark_refusals` and `unmarked_seen` on the objects that receive a text; the older code ignores them.

## Conditions

1. Each Branch A read immediately before its apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values), and the live zip saved with its hash. The NEVER-2 entry `comm-assist-r18-deploy`, naming both functions (code only; no image) and the secret, is opened, and its entry AND sentinel are committed before the first apply.
3. BEFORE step 3: `check_j3_equiv.py` reads `ok=True` with `J3_PIN=38ce5a7981` (17 of 17 probes, files=3, foreign=1; the issuer's own pre-flight build read exactly that). AFTER, live: `check_j3_live.py` reads PASS (one new package; the served zip equals the pin; `INGRESS_MARK_MODE=record` in both environments and the other keys as recorded; the secret has a current version with its value never read; each role may read it by simulation; the served code round-trips a mark and refuses a tampered one). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`.
4. The secret value never appears in any file, log, message, commit, ledger entry, plan output or proof instance; the generating file is deleted before the seat reports. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. The mode stays `record`. Flipping it to `enforce`, by any route, is not this act.

**SIGNED** -- `2.0.0_SA_COO~CA`
