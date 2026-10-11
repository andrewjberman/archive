# COO never-widen half -- COMM_ASSIST round 14, cell CA-f-1: deploy the round-13 package (one targeted apply of `module.ldo_001`, code only)

**Author:** `2.0.0_SA_COO~ZZ`, 2026-10-11 ~01:4xZ. **Read at:** `box/sitez` `2fd32e12c2` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO~Z`) and a CVO half (`3.0.0_SA_CVO~Z`). **Authority:** round-13 analysis
`ledger/ROUND_ANALYSIS.round13.md` @08b06f5d33, ruling 1 and D1 ("a never-widen pair naming the merged commits"); PRD v0.3
C-MAIL and C-PACKAGE.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by `0.7.0_AE_CloudOps~CA` on site Z. The package is BUILT
FROM A CLEAN DETACHED CHECKOUT AT `2fd32e12c2` (round 12's Z-S3 lesson: a half measured on a moving trunk certifies a package
nobody builds). It changes code only: no variable, no environment value and no policy moves.

**Live pre-state, read by this seat at ~01:3xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry
`CodeSha256` `SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM=` (LastModified 2026-10-09 23:03:08Z / 23:03:14Z). That is
NFRA_CTLPLN `TO-APPLY-31`'s package (`0.7.0_AE_CloudOps~CTL`, deploy commit `3af6f043b3`), built at `bde0c0fc90`, 268046 bytes. The
served zip's own hash equals that CodeSha256 (this seat's download). **Two projects deploy this module.** NFRA_CTLPLN is the other
writer, and its pending apply orders are its own. This half binds the diff from the LIVE build commit, not from COMM's last deploy.

## What becomes live: the packaged-path diff `bde0c0fc90..2fd32e12c2` (C-PACKAGE)

Packaged set, read out of `infra/aws/lambda/teams-chat-assist/build.sh`: `handlers.py`, the LDO runtime `ldo.py`,
`data/transcripts/scripts/teams_chat/`, `daily_reports/eod/post_format.py` and `VOICE.md`, `lib/opal_naming.py`,
`org/standards/NAMING_SCHEMA.json`, `infra/logic/registry/*.json`. **The diff is 2 files, +31 -9, both COMM round 13:**

| file | commit | what it changes live |
|---|---|---|
| `teams_chat/mail_requests.py` (+4 -3) | CA-e-2 `40d4d71c90` (merged `bf8492f48f`) | `firm_domains()` returns only C-MAIL's five party keys (`cottonwood`, `inflection`, `49financial`, `alongside`, `opal`; three read through `lib.opal_naming.lookup()` at import). Today it returns four (alongside has no measured domain), and it still returns those four. A sixth client firm with a tenant email domain is no longer considered. The import now reads the registry, so a missing registry fails the mail step at import rather than at the first call. Either way `_safe` reports the step as failed |
| `teams_chat/channel_mentions.py` (+27 -6) | CA-e-3 `1a6df54118` (merged `25d1247250`) | each caught gateway error is described (`route=<label> status=<n> error=<code>`, at most 200 characters, never content). The `channel_poll` line gains `error`, and after its work is saved the step RAISES, so `ingress_step_failed` (step `channels`) is logged. Live it fails every minute (59 of 59 per hour), so **this act adds about 60 `ingress_step_failed` lines an hour** to the ingress log. That is the intended escalation, not a regression. It sends nothing, texts nobody and creates no alarm (C-MORATORIUM) |

Measured unchanged in the span: `handlers.py`, `ldo.py`, `tenant.py`, `assist.py`, `daily_reports/eod/`, `lib/opal_naming.py`,
`NAMING_SCHEMA.json`, every `infra/logic/registry/*.json` (numstat over those paths: 0 lines; the 3 files that moved under
`lib/` are `lib/research/...`, which build.sh does not package). Root and module `.tf` (`infra/aws/terraform/transcripts/`,
`infra/aws/terraform/modules/ldo/`): 0 files changed.

## What changes for Andrew

Nothing he sees today. Channel @mentions still do not reach him (the gateway call still fails), but the failure now names its
call and status in the log, which is what round 14's D2 cures from. Mail from the four live parties is considered as before.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`. Exactly `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`;
  changed keys a subset of {`source_code_hash`, `last_modified`}; the after-hash equals the built package. No `environment`, policy,
  key, reader or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report. That covers:
  - an add, destroy or replacement, or any other argument or address;
  - an `init` migrate or reconfigure prompt;
  - a pre-state hash other than `SFSTGBQX...` (another writer moved it; re-measure the diff from the new build commit);
  - the build not made from a clean checkout at `2fd32e12c2`, or a packaged-path diff between that checkout and the pin;
  - the import test failing against the built `dist/pkg`:
    `python -c "import sys; sys.path[:0]=['<pkg>']; import handlers, data.transcripts.scripts.teams_chat.tenant"`;
  - the End of Day window 20:00Z-21:45Z, or an End of Day event in flight.

  The one permitted foreign `-var` is `second_reader_trust_principal_arns`, read live at the act from
  `aws iam get-role --role-name teams-global-transcripts-second-reader-role` (round-12 A3; TO-APPLY-31 used the same).

## Rollback, per key

- **Code:** the live zip downloaded before the act (`SFSTGBQX...`, 268046 B), copied over `dist/teams-chat-assist.zip`, then
  the same targeted apply. The plan then reads 0/2/0 back to that hash.
- **State:** none migrated. The ingress's cursor files are untouched by this code; the new raise runs after `put_json`.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`.
2. BEFORE: both `CodeSha256`/`LastModified` and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r14-deploy`,
   naming both functions, is opened, and its entry AND sentinel are committed before the act.
3. AFTER, live: `deliverables/2.0.0_SA_COO~ZZ/r14/checks/d1_live.py` reads PASS (both functions on one new package; the
   served zip's two round-13 files equal the pin's; the served code refuses a sixth firm). A targeted re-plan reads no changes.
   Within 10 minutes `d1_errorfield.py` reads PASS (the `error` field is readable and `ingress_step_failed[channels]` appears, or
   the step is healthy). `ingress_poll` continues, and the mail step still logs `polled`.
4. The applier reads no message content and sends no test mail.

**SIGNED** -- `2.0.0_SA_COO~ZZ`
