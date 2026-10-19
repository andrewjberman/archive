# COO never-widen half -- COMM_ASSIST round 22, cell CA-p-2: deploy the mail handler that refuses mail Andrew sent (one targeted apply of `module.ldo_001`, CODE ONLY)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-19 (laptop). **Root:** `infra/aws/terraform/transcripts/`. **Counterparts owed:** a CTO half
(`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO`), each signed on the same pin. **Authority:** Andrew's word to this seat 2026-10-19
~16:26Z (record `org/tier1_exec/2.0.0_SA_COO~CA/ANDREW_DIRECT_20261019_162xZ_MUSE_NO_SELF_DRAFT_RULE_APPROVED_AND_CALL_2396_WAIT_NATURAL.md`
@8eb8c7408a) and `1.0.0_SA_CTO` msg 109839 ("Go on the rule"); PRD v0.10 FWD-2; round-22 decomposition, cell CA-p-2. Adapted from the
R21 half `NEVER_WIDEN_HALF_COO_COMM_ASSIST_R21_THREADS_DEPLOY_20261016.md` (CA-n-2, CLOSED).

**PIN:** `e6c37673c8` (box/laptop: the drain merge of CA-p-1, worker ~33, instance VALID at e8d8ba4554). Everything below that is
measured was read by the author at ~17:0xZ on 2026-10-19 from a sparse detached worktree at the pin, built with
`bash infra/aws/lambda/teams-chat-assist/build.sh` (34 files).

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the COMM CloudOps lane (`0.7.0_AE_CloudOps~COMM1`, rule 34) on the
laptop, outside 20:00Z-21:45Z, with the package BUILT FROM A CLEAN DETACHED CHECKOUT AT THE PIN. It changes **code only**:
`mail_requests.py` refuses a considered-mail candidate whose sender address is Andrew's own mailbox (read from the cached `/me`
answer, key `mail`) before the domain and body tests, counts it as `from_andrew`, and drafts and texts nothing for it; when his mailbox
is unknown the handler raises (the event retries) and drafts nothing. No environment value, policy, secret, Terraform resource or image
moves.

**Live pre-state, read by the author read-only at 2026-10-19 ~16:5xZ** (`.tools/aws lambda get-function-configuration`, and
`.tools/aws sqs get-queue-attributes` on `teams-global-chat-assist-dlq.fifo`):

| item | handler | ingress |
|---|---|---|
| `CodeSha256` | `RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE=` | `RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE=` |
| `LastModified` | 2026-10-16T22:13:25Z | 2026-10-16T22:13:31Z |
| `CodeSize` | 238923 | 238923 |
| `INGRESS_MARK_MODE` | `enforce` | `enforce` |
| environment key names | 15 (listed in `check_p2_equiv.py` KEYS) | 15 (same) |

That is the CA-n-2 package built at `1aa63bde67` (34 files). The dead-letter queue reads 0 and 0. The CA-k-2 gate in `safe-apply.sh` must
print `LDO001-MODE verdict=OK default=enforce live=enforce`.

## What becomes live (C-PACKAGE), measured at the pin

`git diff --numstat 1aa63bde67 e6c37673c8` over the packaged paths (the Terraform root, the ldo module, `handlers.py` and `daily_reports/eod` read 0 changed files):

| path | what | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/mail_requests.py` | +17 -5 | the change: his own mailbox refused first |
| `infra/logic/registry/exemptions.json` (FOREIGN) | +11 -3 | other seats' rows (`0.7.0_AE_CloudOps~TM1`, `4.0.0_SA_CRO~DELL1`); the assistant opens the registry, so they ride the package |
| `infra/logic/registry/legacy_addresses.json` (FOREIGN) | +70 | same reason (`4.0.0_SA_CRO~DELL1`, `4.0.0_SA_CRO~Z`) |
| `lib/opal_naming.py` (FOREIGN) | +14 -9 | the naming library's validator and a Lambda-map reader; neither is on the assistant's runtime path (it calls `address()` and `name()`) |
| `org/standards/NAMING_SCHEMA.json` (FOREIGN) | +13 -7 | schema v1.17 to v1.19: a legacy platform bucket list and an ECR kind; nothing the assistant forms changes |
| every other packaged path | 0 | unchanged (34 files, the same set as live) |

`check_p2_equiv.py` with `P2_PIN=e6c37673c8` against that build read at ~17:0xZ: `P2-EQUIV ok=True differ=5 foreign=4 probes=17
same=17 p1=6 of 6`: the same file set as live; the files that differ are `mail_requests.py` and the four foreign files; the 17 address
probes (S3 keys for five chats and the mail parties) are identical, so the foreign changes move no address the assistant forms; and the
issuer's six P1 arms pass against the BUILT package. The live-mode check reads `ok=False` today (`p1=1 of 6` on the served zip), the base.

## What changes for Andrew

A mail he sent himself that names him is no longer drafted and texted back to him. Mail from a colleague (any of the five parties'
domains, including Opal's own) is drafted and texted exactly as before.

## Named residual

- An alias, a shared mailbox or a second address of his that is not the cached `mail` is not refused.
- "A thread whose latest message is his": for a Teams chat this already holds; for mail it is NOT built (each mail is its own event,
  one message). A colleague's earlier mail in a thread he has since answered keeps its draft until he drops it.
- When the cached `/me` has no `mail` or cannot be read, mail events fail and retry (the dead-letter queue is the place that shows it).

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only; changed
  keys a subset of {`source_code_hash`, `last_modified`}, NEVER `environment`; the after-hash equals the built package. Then apply that
  saved plan through `bash .tools/safe-apply.sh`.
- **B:** anything else: apply NOTHING and report. Any add, destroy or replacement; any other address or argument; an `environment`
  change; an `init` migrate or reconfigure prompt; a pre-state hash other than `RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE=` or a mode
  other than `enforce`; the CA-k-2 gate reading anything but `verdict=OK`; a build not from a clean checkout at the pin, or not 34
  files; `check_p2_equiv.py` not reading `ok=True`; the 20:00Z-21:45Z window or an End of Day event in flight; less than 5 GB free on
  `C:`; any `-var`.

## Rollback, per key

- **Code:** save the live zip BEFORE the act (the `RoH5DIiH...` package: `get-function` `Code.Location`, its sha256 and base64 sha256
  recorded), copy it over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a detached worktree at
  `1aa63bde67` (the commit the live package was built from; its Terraform default is `enforce`). The plan reads 0/2/0 back to
  `RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE=` with no environment change. No `-var`.
- **State:** the new code writes a `from_andrew` key into the mail objects' `counts` (a count only). A rollback leaves it there; the old
  code adds keys by `counts.get(reason, 0)` and ignores the extra one. Nothing else is written.

## Conditions (carried from the R21 halves)

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never
   `aws lambda update-function-code`. Never set `LDO001_MODE_OVERRIDE`.
2. BEFORE: both `CodeSha256`/`LastModified`, both environments' KEY NAMES (never values), the live zip saved with hashes, the
   dead-letter queue counts. The NEVER-2 entry `comm-assist-r22-selfmail-deploy`, naming both functions (code only; no image), is opened
   and its entry AND sentinel committed before the act.
3. BEFORE the act: `P2_PIN=e6c37673c8 python .../r22/checks/check_p2_equiv.py` reads `ok=True`. AFTER, live:
   `P2_PIN=e6c37673c8 P2_MODE=live python .../r22/checks/check_p2_equiv.py` reads `ok=True`. A targeted re-plan reads no changes. Within
   10 minutes the ingress logs show `channel_poll` lines with `failed=0` (or only the 502s the gateway already shows) and `calls` at
   most 20, `ingress_poll` and the mail step `polled`; no function log shows an error or `AccessDenied`; the dead-letter queue reads
   UNCHANGED.
4. The secret's VALUE is never read. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. Not 20:00Z-21:45Z, no End of Day event in flight. The mode stays `enforce`.
6. DISK: at least 5 GB free on `C:` before the worktree (37 GB at this write).
7. ONE SITTING: begin only when apply, AFTER reads, re-plan and ledger close can finish in one sitting.
8. (ADDED) The first `mail_considered` line after the apply that carries a mail event reads without a `RuntimeError: me-without-mail` raise; such a raise is a defect row to the issuer, and the rollback above applies if more than one mail event fails on it.

**BLIND, stated:** real mail traffic after the apply is not exercised by the act; the issuer's real run at close reads the live
`mail_considered` counts.

**SIGNED** -- `2.0.0_SA_COO~CA`
