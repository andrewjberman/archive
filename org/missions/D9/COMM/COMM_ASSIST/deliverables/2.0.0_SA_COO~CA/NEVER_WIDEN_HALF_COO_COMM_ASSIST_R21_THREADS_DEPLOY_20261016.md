# COO never-widen half -- COMM_ASSIST round 21, cell CA-n-2: deploy the poller that reads replies in older threads (one targeted apply of `module.ldo_001`, CODE ONLY)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-16 (laptop). **Root:** `infra/aws/terraform/transcripts/`. **Counterparts owed:** a CTO half
(`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO`), each signed on the same pin. **Authority:** the CTO's ruling on call 446a
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_446A_COMM_ASSIST_TEAMS_THREAD_REPLY_MENTIONS_20261016.md` @f418537712, msg
109753: one cell plus its deploy plus one retest); PRD v0.10 FWD-3 and FWD-13; round-21 decomposition, cell CA-n-2. Adapted from the
R20 half `NEVER_WIDEN_HALF_COO_COMM_ASSIST_R20_NARROW_DEPLOY_20261015.md` (CA-l-4, CLOSED).

**PIN:** `1aa63bde67` (box/laptop: the drain merge of CA-n-1, worker ~32, instance VALID at 37948413b3). Everything below that is
measured was read by the author at ~21:2xZ-21:3xZ on 2026-10-16: `git diff --numstat 863dc0f739..1aa63bde67` over the packaged paths,
and a build of the package from a clean detached worktree at the pin.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the COMM CloudOps lane (`0.7.0_AE_CloudOps~COMM1`, seated
under CLAUDE.md rule 34) on the laptop, outside 20:00Z-21:45Z, with the package BUILT FROM A CLEAN DETACHED CHECKOUT AT THE PIN. It
changes **code only**: `channel_mentions.py` also reads, through the gateway's replies route, the replies of a bounded set of threads
per channel (the pinned End of Day parent, and every post with activity in the last 14 days, at most 10 per channel), inside the
existing per-poll budget (`MAX_CALLS` 20). No environment value, policy, secret, Terraform resource or image moves.

**Live pre-state, read by the author read-only at 2026-10-16T21:23Z** (`.tools/aws lambda get-function-configuration`, and
`.tools/aws sqs get-queue-attributes` on `teams-global-chat-assist-dlq.fifo`):

| item | handler | ingress |
|---|---|---|
| `CodeSha256` | `gSq68yr2uV/DwTwAuhWRGzRJoSTo3fzU4mmeitNCpok=` | `gSq68yr2uV/DwTwAuhWRGzRJoSTo3fzU4mmeitNCpok=` |
| `LastModified` | 2026-10-15T09:18:48Z | 2026-10-15T09:18:55Z |
| `CodeSize` | 235445 | 235445 |
| `INGRESS_MARK_MODE` | `enforce` | `enforce` |
| environment key names | 15 (`GATEWAY_BASE` ... `SMS_ORIGINATION`, listed in `check_n2_equiv.py` KEYS) | 15 (same) |

That is the CA-l-4 package built at `863dc0f739` (34 files). The dead-letter queue reads 0 and 0. The Terraform default
`chat_assist_ingress_mark_mode` reads `enforce` at the pin (`chat_assist.tf`:41), equal to live; the CA-k-2 gate in `safe-apply.sh`
must print `LDO001-MODE verdict=OK default=enforce live=enforce`. `git diff --numstat 863dc0f739..1aa63bde67` over
`infra/aws/terraform/transcripts`, `infra/aws/terraform/modules/ldo`, `handlers.py`, `daily_reports/eod` and `lib/opal_naming.py` is
EMPTY.

## What becomes live (C-PACKAGE), measured at the pin

| path | lines | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/channel_mentions.py` | +83 -8 | the change: thread replies read; a failing thread costs only itself |
| `infra/logic/registry/legacy_addresses.json` (FOREIGN) | +300 -0 | rows from other seats (authors since the live pin: `0.7.0_AE_CloudOps~ZS`, `0.0.0_AB_MSTR~DELL1`, `4.0.0_SA_CRO~Z`, `0.9.0_WK_SOC2_MSLOGS~4`, `0.9.0_WK_TCKT_MTADTA~1`); the assistant opens this file, so they ride the package |
| `infra/logic/registry/scopes.json` (FOREIGN) | +11 -0 | same reason |
| `infra/logic/registry/systems.json` (FOREIGN) | +9 -0 | same reason |
| every other packaged path | 0 | unchanged (34 files, the same set as live) |

`check_n2_equiv.py` with `N2_PIN=1aa63bde67` against that build read at ~21:3xZ: `N2-EQUIV ok=True differ=4 foreign=3 probes=17
same=17 n1=8 of 8`: the same file set as live; the files that differ are `channel_mentions.py` and the three foreign registry files;
the 17 address probes (S3 keys for five chats and the mail parties) are identical, so the foreign rows move no address the assistant
forms; and the issuer's eight N1 arms pass against the BUILT package.

## What changes for Andrew

An @mention of him posted as a REPLY inside an older thread of a watched channel (the End of Day parent above all) is now texted to
him and recorded for muse, within the poller's 5-minute channel cadence. Nothing else he sees changes.

## Named residual

- One page of replies per thread per read (every 5 minutes): a busy thread that gains more than about 50 replies between two reads
  loses the older ones of that burst.
- A post older than 14 days with a new reply is read only if it is pinned (today: the End of Day parent alone).
- Gateway calls per poll stay at most 20, but more of them are spent; the channel_poll `calls` count reads it.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only;
  changed keys a subset of {`source_code_hash`, `last_modified`}, NEVER `environment`; the after-hash equals the built package.
  Then apply that saved plan through `bash .tools/safe-apply.sh`.
- **B:** anything else: apply NOTHING and report. Any add, destroy or replacement; any other address or argument; an `environment`
  change; an `init` migrate or reconfigure prompt; a pre-state hash other than `gSq68yr2uV/DwTwAuhWRGzRJoSTo3fzU4mmeitNCpok=` or a mode
  other than `enforce`; the CA-k-2 gate reading anything but `verdict=OK`; a build not from a clean checkout at the pin, or not 34
  files; `check_n2_equiv.py` not reading `ok=True`; the 20:00Z-21:45Z window or an End of Day event in flight; less than 5 GB free
  on `C:`; any `-var`.

## Rollback, per key

- **Code:** save the live zip BEFORE the act (the `gSq68...` package: `get-function` `Code.Location`, its sha256 and base64 sha256
  recorded), copy it over `dist/teams-chat-assist.zip`, then a targeted apply of `module.ldo_001` from a detached worktree at
  `863dc0f739` (the commit the live package was built from; its Terraform default is `enforce`). The plan reads 0/2/0 back to
  `gSq68yr2uV/DwTwAuhWRGzRJoSTo3fzU4mmeitNCpok=` with no environment change. No `-var`.
- **State:** the new code adds a `threads` key to the poller's own state file `channel_cursors.json`. A rollback leaves it there; the
  old code reads only `cursors` and `read_at` and ignores it (measured: the CA-l-4 `poll` builds its put_json from those two keys
  alone, so the next write drops `threads`). Nothing else is written.

## Conditions (carried from the R20 halves; one added)

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never
   `aws lambda update-function-code`. Never set `LDO001_MODE_OVERRIDE`.
2. BEFORE: both `CodeSha256`/`LastModified`, both environments' KEY NAMES (never values), the live zip saved with hashes, the
   dead-letter queue counts. The NEVER-2 entry `comm-assist-r21-threads-deploy`, naming both functions (code only; no image), is
   opened and its entry AND sentinel committed before the act.
3. BEFORE the act: `N2_PIN=1aa63bde67 python .../r21/checks/check_n2_equiv.py` reads `ok=True`. AFTER, live:
   `N2_PIN=1aa63bde67 N2_MODE=live python .../r21/checks/check_n2_equiv.py` reads `ok=True`. A targeted re-plan reads no changes.
   Within 10 minutes the ingress logs show `channel_poll` lines with `failed=0` (or only the 502s the gateway already shows) and
   `calls` at most 20, `ingress_poll` and the mail step `polled`; no function log shows an error or `AccessDenied`; the dead-letter
   queue reads UNCHANGED.
4. The secret's VALUE is never read. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. Not 20:00Z-21:45Z, no End of Day event in flight. The mode stays `enforce`.
6. DISK: at least 5 GB free on `C:` before the worktree (20 GB at this write).
7. ONE SITTING: begin only when apply, AFTER reads, re-plan and ledger close can finish in one sitting.
8. (ADDED) The FIRST read after the apply of the `channel_poll` line for the End of Day channel shows the pinned thread read without
   a failure; a `replies` route refusal (403/404) on the pinned parent is a defect row to the issuer, not a rollback (the fix
   isolates a failing thread by construction, arm 8).

**BLIND, stated:** real Teams traffic after the apply is not exercised by the act; the retest CA-n-3 needs a person's post.

**SIGNED** -- `2.0.0_SA_COO~CA`
