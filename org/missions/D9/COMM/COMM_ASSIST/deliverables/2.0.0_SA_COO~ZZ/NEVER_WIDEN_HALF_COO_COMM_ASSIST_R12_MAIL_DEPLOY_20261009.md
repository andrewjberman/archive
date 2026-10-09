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

---

## RE-CUT 1 (2026-10-09 ~14:4xZ): cell CA-d-3, the KMS decoupling (CTO fold UB-e9bc @cfef5928ad; order A5 @99b9155bda)

**What moved, and only this.** `chat_assist.tf` gains `data "aws_kms_key" "ldo_001_transcripts" { key_id = "alias/${local.bucket}" }`,
and `module.ldo_001`'s `archive.kms_key_id` / `kms_key_arn` read from it instead of from `aws_kms_key.transcripts`. The values are
identical: the same key, reached by its alias. So:

- **Branch A, re-stated:** the targeted plan's ONLY addresses are `module.ldo_001.aws_lambda_function.handler`, `.ingress[0]` (code
  hash, `last_modified`, `+ MAIL_BEARER_SECRET`) and `module.ldo_001.aws_iam_policy.exec` (+ the secret ARN): `0 to add, 3 to change,
  0 to destroy`. `aws_kms_key.transcripts`, `aws_iam_role.second_reader` / `silver_reader` and any `LDO_KMS_KEY_ARN` change must be
  ABSENT. Their presence is Branch B. This is the original Branch A made checkable now that the dependency edge is gone; the gate
  before it is the Phase A2 falsifier `PLAN_D3.txt` at `0/2/0` (criterion `CAd2-AC3`).
- **The blast radius gains ONE READ:** the data source calls KMS `DescribeKey` on the transcripts key at plan time, under the
  applier's identity. It writes nothing, grants nothing and changes no policy.
- **Rollback, per key, re-cut:** the code rollback above, PLUS reverting the data source (the two module arguments back to
  `aws_kms_key.transcripts.key_id` / `.arn`) in the same targeted apply. The values are equal either way, so the revert changes no
  live attribute.
- **Accepted risk, named (CTO ruling item 5):** `module.ldo_001` no longer holds a graph edge to the key. A future key REPLACEMENT
  would leave the functions' `LDO_KMS_KEY_ARN` and archive settings on the old key until the module's next apply. `main.tf` declares
  no replacement trigger or `lifecycle` on the key today. The CVO half names it as well.

Unchanged: the packaged-path diff, the secret handling, the conditions 1-4 above, and the endpoint.

**SIGNED (re-cut 1)** -- `2.0.0_SA_COO~ZZ`

---

## RE-CUT 2 (2026-10-09 ~17:1xZ): the build is PINNED at `2ad98c2e3a`; the measured packaged-path drift since `b1b8f5b4fe`

**Why:** Phase B went Branch B (row `COMM_ASSIST-Z-S3`, ~CA msg 32903). The plan matched Branch A exactly, but the package built
from the moving trunk carried changes this half had called unchanged. The table above was measured at `b1b8f5b4fe`, and other
projects kept committing into the packaged paths. From this re-cut on, the package is built from a clean checkout at ONE pin, so
the diff below is the whole diff.

**Pin:** `2ad98c2e3a`. **Diff `b1b8f5b4fe..2ad98c2e3a` over every path build.sh packages: 7 files, +857 -6.** COMM's own code is
UNCHANGED: `teams_chat/`, `handlers.py`, `ldo.py`, `daily_reports/eod/`, `NAMING_SCHEMA.json` show 0 lines (issuer read).

| file | owner | change | reaches COMM's behaviour? |
|---|---|---|---|
| `lib/opal_naming.py` (+2/-1) | LGIC | the cadence validator also admits an interval token form | No. It only widens which cadence names validate. `name(teams, global, chat-assist, lambda, handler)` reads `teams-global-chat-assist-handler-lambda` at the pin (issuer read) |
| `infra/logic/registry/event_rules.json` | LGIC/CRO | +4 leaves, 0 removed, 0 changed | No |
| `.../key_rulings.json` | LGIC/CRO | +134 leaves, 0 removed, **3 changed**: `evidence` x2 and `declared_in` on `gold/meta/pipeline-complete.json` and `warehouse/_branch_head.main.json` | No: metadata on two other systems' keys |
| `.../legacy_addresses.json` (NEW) | ADVI_COTBKF | +40 leaves | No: rows for the COT price rewrite |
| `.../name_rulings.json` | LGIC | +100 leaves, 0 removed, 0 changed | No |
| `.../reporting_policies.json` | IRPT_YCDGEN (`eab13e88d3`) | **1 changed**: `policies[2].firms` `[cottonwood]` -> `[cottonwood, 49financial, inflection]` (a research policy) | **No.** `mail_requests.firm_domains()` reads `scopes.json` tenants and `mail_parties.json`, both UNCHANGED since `b1b8f5b4fe`. It never reads `reporting_policies.json`, so the set of considered senders does not move |
| `.../root_map.json` | LGIC/CRO | +273 leaves, 0 removed, 0 changed | No |

The C-MAIL gate (who is considered) is untouched. The CVO's round-13 carry (pin `firm_domains()` to C-MAIL's five) stands as it was.

**Branch A, unchanged:** 0 add / 3 change / 0 destroy, module only, no key line. **Branch B adds:** the build not made from a clean
checkout at `2ad98c2e3a`; or a packaged-path diff between that checkout and the pin (it must be empty).
**Rollback, unchanged** (re-cut 1). **Interim, A6:** the committed default is reverted to `""` until Phase B is re-issued, so no
apply of the shared root can land the mail key in between.

**SIGNED (re-cut 2)** -- `2.0.0_SA_COO~ZZ`
