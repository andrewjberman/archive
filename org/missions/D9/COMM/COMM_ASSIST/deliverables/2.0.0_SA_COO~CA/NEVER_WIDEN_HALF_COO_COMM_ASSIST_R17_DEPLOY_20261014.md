# COO never-widen half -- COMM_ASSIST round 17, cell CA-i-4: deploy the round-17 package (one targeted apply of `module.ldo_001`: code and ONE environment value)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-13 ~23:5xZ (laptop). **Read at:** `box/laptop` `b19849b51c` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** CTO round-16 analysis `ledger/ROUND_ANALYSIS.round16.md` @6e9e2fc1ff
(the receiver check meets FWD-7; the key is a change-managed deploy) and its addendum items 6 and 7 (@e6e0464bbc); Andrew-direct ~22:3xZ via MSTR msg 108965; PRD v0.7.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by a CloudOps seat on the laptop (`0.7.0_AE_CloudOps~CA`), outside 20:00Z-21:45Z. The package is BUILT FROM A CLEAN
DETACHED CHECKOUT AT `b19849b51c` (the Z-S3 lesson: a half measured on a moving trunk certifies a package nobody builds). It changes **code** on both functions and **one environment
value** on both: `MUSE_ANSWER_PUBKEY`, a public key, joins the map. No policy, no secret, no other key.

**Live pre-state, read by this seat at ~23:5xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `nIQW+3XvvaFNJQfwX5lrI99XSexESb68Pd1uLldlTgI=`
(LastModified 2026-10-11T02:16:55Z / 02:17:01Z), 269206 bytes, python3.12, no layers. That is the package of change-management entry `comm-assist-r14-deploy` (pin `2fd32e12c2`).
Environment keys on both: `GATEWAY_BASE`, `SMS_ORIGINATION` (the toll-free number's ARN), `IGNORE_NAMES`, `MAIL_BEARER_SECRET` (`...gateway/mail/commassist-bearer-cPYbR3`), and the nine `LDO_*`
keys the module sets (table, alarm prefix and role, KMS key, dedup days, mailbox ARN and URL, id, archive bucket). No `MUSE_ANSWER_PUBKEY`. The required root variable `second_reader_trust_principal_arns` is now supplied by the committed `readers.auto.tfvars` (`e284d59428`), so no `-var` is
needed or permitted.

## What becomes live: the packaged-path diff `2fd32e12c2..b19849b51c` (C-PACKAGE)

Packaged set, read out of `infra/aws/lambda/teams-chat-assist/build.sh`: `handlers.py`, the LDO runtime `ldo.py`, `data/transcripts/scripts/teams_chat/`, `daily_reports/eod/post_format.py`
and `VOICE.md`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`, `infra/logic/registry/*.json`. **13 files, +1373 -48.** `handlers.py`, `ldo.py`, `daily_reports/eod/` and
`NAMING_SCHEMA.json`: 0 lines.

**COMM round 17 (this project):**

| file | change | what it does live |
|---|---|---|
| `teams_chat/muse_verify.py` (new, +182) | CA-i-2 | stdlib Ed25519 / SSHSIG verifier |
| `teams_chat/tenant.py` (+75 -3) | CA-i-2 | event kind `muse.reply`: acts only on a signature that verifies against `MUSE_ANSWER_PUBKEY`, else refuses and records; a versioned edit now meets the stale check (also `owner.text` redrafts) |
| `teams_chat/mail_requests.py` (+53 -12) | CA-i-7, CA-i-8 | a received-mail draft: notes redraft, his 1 approves and the assistant texts the final draft to paste, the text names the answers; **nothing is ever sent** |
| `teams_chat/assist.py` (+2 -1) | CA-i-6 | agentbus sends carry `from_tailnet=ldo-001` (the register holds it) |

**Foreign files (other projects' commits riding this package; named, not owned):** `lib/opal_naming.py` (+724 -24: firm pages, fence class, lambda-plane consumers; NFRA_CTLPLN CT-w-1/w-4, ADVI_FIRMBKTS
FB-g-24), and registry rows: `exemptions.json` +110, `feeds.json` +16, `firm_pages.json` +58, `name_rulings.json` +21, `platinum_destinations.json` +125, `root_map.json` -6, `scopes.json` +5 -2,
`systems.json` +2. **Measured effect on the assistant, where it acts, not by the plan:** `check_i4_equiv.py` imports the assistant from the BUILT package and from the zip the live function SERVES
and compares 17 probes: the bucket, `state_key`, `silver_key` and `bronze_key` for five chat shapes, and `mail_requests.firm_domains()` read from each package's own registry. **17 of 17 equal**
(run at the real pre-flight build of the pin, 2026-10-13 ~23:5xZ); the four mail parties are unchanged. The check is run again by the applier before the act (condition 3).

## What changes for Andrew

A mail that names him gets a draft he can finish by text: notes redraft it, his 1 approves it and the assistant texts the final draft to paste into his own Outlook reply. **Nothing is sent**; the
draft text now ends with a line that names 1, notes, 0 and #dev. A muse answer is accepted only when muse's signature verifies; muse cannot answer until a forwarder is installed on dell2 (cell CA-i-5), so
nothing changes for him on that path today. The agent bus stops logging `unstamped sender=LDO-001`.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`. Exactly `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`; changed keys a subset of {`source_code_hash`, `last_modified`,
  `environment`}; the `environment` diff is EXACTLY one added key `MUSE_ANSWER_PUBKEY` (its value the line whose fingerprint is `SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ`), every
  existing key unchanged (`MAIL_BEARER_SECRET` and `SMS_ORIGINATION` named); the after-hash equals the built package. No policy, key, reader or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report. That covers: an add, destroy or replacement, or any other argument or address; an `init` migrate or reconfigure prompt; a pre-state hash other than
  `nIQW...` (another writer moved it; re-measure from the new build commit); the build not made from a clean checkout at `b19849b51c`; `check_i4_equiv.py` not reading `ok=True`; the import test failing against the
  built `dist/pkg` (`python -c "import sys; sys.path[:0]=['<pkg>']; import handlers, data.transcripts.scripts.teams_chat.tenant"`); the End of Day window 20:00Z-21:45Z or an End of Day event in flight;
  any `-var`.

## Rollback, per key

- **Code and environment:** the live zip downloaded before the act (`nIQW...`, 269206 B), copied over `dist/teams-chat-assist.zip`, then the same targeted apply with the variable at `""`
  (`-var chat_assist_muse_answer_pubkey=` is the ONLY `-var` permitted, and only for rollback). The plan then reads 0/2/0 back to that hash, with `MUSE_ANSWER_PUBKEY` present but empty (the receiver reads an empty key as unset and refuses every muse answer).
- **State:** none migrated. `state["muse_refusals"]` is a new key written only on a refused muse answer, which cannot occur until CA-i-5.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values) and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r17-deploy`, naming both functions (code and one environment value; no image, so no task family pulls it), is opened, and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_i4_equiv.py` reads `ok=True`. AFTER, live: `check_i4_live.py` reads PASS (one new package; the served zip's four round-17 files equal the pin's; both environments as recorded; the served code
   routes `muse.reply`, accepts a real signature, refuses another key, and stamps `ldo-001`). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`.
4. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.

**SIGNED** -- `2.0.0_SA_COO~CA`
