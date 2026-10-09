# COO never-widen half -- COMM_ASSIST round 12, cell CA-d-2: the FWD-4 mail deploy (one targeted apply of `module.ldo_001`, code + one variable)

**Author:** `2.0.0_SA_COO~ZZ`, 2026-10-09 ~09:3xZ. **Read at:** `box/sitez` `b1b8f5b4fe`. Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO~Z`) and a CVO half (`3.0.0_SA_CVO~Z`), as for r29. **Authority:** round-11 analysis
`ledger/ROUND_ANALYSIS.round11.md` @4c14e95965 (E1), PRD v0.2 C-MAIL and C-PACKAGE.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by `0.7.0_AE_CloudOps~Z` on site Z, from a trunk that contains
`b1b8f5b4fe`. It runs only after NFRA_OPLGTW `TO-OG-ap-3` has created `gateway/mail/commassist-bearer` (its AC1 PASS) and the gateway
serves r29. Before the plan, ONE committed edit sets `var.chat_assist_mail_bearer_secret_arn`'s default in
`chat_assist.tf` to that secret's full ARN as `describe-secret` returns it. The value is committed, never passed as `-var`: a later
apply of this shared root (NFRA_TRNSPT owns the rest of it) would otherwise silently unwire the mail key.

**Live pre-state, read by this seat at ~09:2xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry
`CodeSha256` `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=` (LastModified 22:32:01Z / 22:31:55Z, the round-7 deploy built at
`a5fde91788`). Neither has `MAIL_BEARER_SECRET`. Policy `teams-global-chat-assist-policy` is at v3. The secret is ABSENT
(`ResourceNotFoundException`).

## What becomes live: the packaged-path diff `a5fde91788..b1b8f5b4fe` (C-PACKAGE), 12 files, +2583/-12

The CTO's analysis names the three round-9 commits. **The measured diff is wider, and this half binds the measured one.**

| file | owner | what it changes live |
|---|---|---|
| `teams_chat/mail_poll.py` (new, 162 lines) | COMM r9 (`bc17e69176`) | the mail poller: each minute the ingress asks the gateway's mail route for his mailbox's new mail. It is inert until `MAIL_BEARER_SECRET` is set; this act sets it |
| `teams_chat/mail_requests.py` | COMM r9 (`9fbe789aa3`, merged `b986bd863f`) | a considered mail (C-MAIL: sender domain one of the five, read from firm records, AND the body names Andrew) is texted once with a draft reply and a CLIENT `<firm>` / Opal flag; a 1 points at the draft. Drafted, never sent |
| `teams_chat/tenant.py` | COMM r9 (`31980c736e`) | the ingress gains the mail step |
| `teams_chat/assist.py` | COMM r9 (`bc17e69176`) | +49 lines with the poller: the gateway mail client and its bearer read |
| `teams_chat/inbound_count.py` | COMM r8 (`787d564135`) + r10 (`e20a098e6f`) | the FWD3 verdict line and the FWD2 draft-acceptance line in the count reader. These are log lines only and send nothing |
| `infra/logic/registry/` x7 (`event_rules`, `key_rulings`, `name_rulings`, `reporting_policies`, `root_map`, `scopes`, `systems`) | **OUTSIDE COMM**: LGIC_BLANKFIX (CRO), IRPT_DASHBD, IRPT_ANLREQ, MDPF_DEMQUE | rows read by `address()`/`name()` at run time. **Measured additive:** 1,464 leaves added, **0 removed, 0 changed** across the 7 files (this seat's leaf-by-leaf JSON diff, keyed by id/key/name where present). An additive row could change an address only if it is more specific than one the agent already resolves; Branch B's import test is the guard |

Unchanged since the live build: `handlers.py`, `ldo.py`, `daily_reports/eod/`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`.
Root `.tf` diff in the same span: `chat_assist.tf` (round 11's variable), `main.tf` +19 and `commentary.tf` +320, which are NOT in
this act. The apply is targeted, and the round-11 plan showed 0 addresses outside the module.

## What changes for Andrew

He gets a text for each considered client mail: one of Cottonwood, Inflection, 49 Financial, Alongside or Opal (internal) wrote, and
the body names him. Each text carries a draft reply in his voice and a client/internal flag. A mail failing either test reaches no
model and sends nothing. NEW EGRESS, within C-MAIL as ratified: the body of a considered mail goes to the agent's existing model
vendor (Kimi). No new vendor, no send to anyone but him, no mail ever sent by the agent, no schedule, no alarm (C-MORATORIUM).

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 3 to change, 0 to destroy`. The two functions change `source_code_hash` and `last_modified`, and
  `environment.variables` gains `MAIL_BEARER_SECRET` = the ARN. `aws_iam_policy.exec`'s secrets-read `Resource` list gains that ARN.
  No other address, statement or argument changes; this equals round 11's `PLAN_SET.txt` with the real ARN. -> apply.
- **B:** anything else, in which case apply NOTHING and report. That covers: an add, destroy or replacement; any other argument,
  statement or address outside the module; an `init` migration prompt; the secret absent; a packaged-path diff since `b1b8f5b4fe`
  outside the table above; `python -c "import sys; sys.path[:0]=['<pkg>']; import handlers, data.transcripts.scripts.teams_chat.tenant"`
  failing against the built `dist/pkg`; the End of Day window 20:00Z-21:45Z; or an End of Day event in flight.

## Rollback, per key

- **Code:** the live zip downloaded before the act (hash `xWURpe/n...` unless it moved), copied over `dist/teams-chat-assist.zip`,
  plus the default reverted to `""`, then the same targeted apply. This removes the env var and the policy ARN in the same step.
- **Secret:** not this act's. It belongs to NFRA_OPLGTW and is never written, read for its value, or deleted here.
- **State:** none migrated. Mail texts already sent are not recalled.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`.
2. BEFORE: both `CodeSha256`/`LastModified` and the live zip saved with hashes. A NEVER-2 entry
   `comm-assist-r12-mail-deploy` is opened and closed, naming both functions and the policy, and its entry AND sentinel are
   committed before the act.
3. AFTER, live: `deliverables/2.0.0_SA_COO~ZZ/r12/checks/d2_live.py` reads PASS, and a targeted re-plan reads no changes. Within
   5 minutes the `ingress_poll` lines continue with no `ingress_step_failed`, and the mail step logs `polled`, not
   `not-configured`.
4. The applier reads no message content and sends no test mail. The exercise is the issuer's real run at close: one real mail from
   one of the five that names him arrives as a text with a draft and the right flag, and one that does not name him sends nothing.
   Until that run the outcome is APPLIED, not EXERCISED.

**SIGNED** -- `2.0.0_SA_COO~ZZ`
