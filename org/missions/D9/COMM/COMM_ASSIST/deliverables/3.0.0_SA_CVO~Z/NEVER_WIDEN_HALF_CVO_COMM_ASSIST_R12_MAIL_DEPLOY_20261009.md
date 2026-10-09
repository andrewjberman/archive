# CVO never-widen half -- COMM_ASSIST round 12, cell CA-d-2: the FWD-4 mail deploy

By: `3.0.0_SA_CVO~Z`, 2026-10-09 ~09:5xZ, on `2.0.0_SA_COO~ZZ` msg 32631 (acked).
Against: `deliverables/2.0.0_SA_COO~ZZ/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R12_MAIL_DEPLOY_20261009.md` @743fcd4598. Bound to the
packaged-path diff `a5fde91788..b1b8f5b4fe` and the act it describes: one targeted apply of `module.ldo_001`, after
NFRA_OPLGTW `TO-OG-ap-3` creates `gateway/mail/commassist-bearer` and r29 serves.

## What I read before signing

- **The packaged diff** (`git diff --numstat a5fde91788 b1b8f5b4fe`): exactly the 12 files the COO's table lists. The 5
  `teams_chat/` files are +377/-12. The 7 `infra/logic/registry/` files have 0 deleted lines each.
- **`scopes.json`, the one registry file that feeds the mail test** (`mail_requests.firm_domains()` reads FIRM client
  tenants' `email_domain`): the diff adds `masters` to inflection and one MASTER row (`4698`, Orion). Neither is a tenant
  email domain, so the set of considered senders does not grow. `mail_requests.py`, `scopes.json` and
  `mail_parties.json` are unchanged from b1b8f5b4fe to HEAD.
- **The mail test on today's records:** `mail_requests.py --check-domains` reads `49financial`, `cottonwood`,
  `inflection` and `opal` at 1 domain each, Alongside with none, and `typed=0`. That is 4 of the 5 named parties, the
  same 4 the gateway's r29 domain table admits (my r29 half @c348b51df9).
- **The PRD** (COMM_ASSIST v0.2, ratified-text SIGNED):
  - C-MAIL (`:76-79`): his own mailbox only, through the gateway; a message is considered only when its sender's
    domain is one of the five, read from firm records, AND its body names "Andrew"; a failing message reaches no model;
    mail is drafted, never sent by an agent.
  - FWD-4 (`:60-67`): client or internal flag, text with draft.
  - C-ONE-YES: nothing goes out in his name without his `1`.

## SIGNED: what a caller can newly read or do

1. **The agent reads Andrew's mailbox through the gateway mail route, by sender domain**, with the `commassist`
   bearer. This is the read r29 widened and that I signed there, now exercised by its named holder, at the same five
   fields, the same domain table and the same mailbox. It adds nothing to r29's widening.
2. **A considered mail's body goes to the agent's existing model vendor.** C-MAIL ratifies passing a considered
   message to a model; it bars only a message that fails either test. Egress law is open except Bloomberg. The tests
   run before any model call (`mail_requests.considered` runs first, per its own header). No new vendor is added.
3. **Andrew receives a text with a draft reply and a client or internal flag.** No mail is sent by the agent, nothing
   goes out in his name without his `1`, and there is no schedule and no alarm.
4. **The 7 registry files become live in the package.** They are additive only (0 deletions). The guard against an
   address resolving differently is the COO's Branch B import test. `scopes.json`'s additions do not touch the mail
   test.

Both branches are covered by the COO half: Branch A (0/3/0, equal to round 11's PLAN_SET with the real ARN) applies, and
anything else applies nothing. Rollback is per key: the live zip plus the default reverted, in one targeted apply.

## Carried (not grounds)

- **The test is "every client firm the registry records", and C-MAIL says "the five he named".** Today they coincide
  (4 resolved, plus Alongside unresolved). A future FIRM client tenant row carrying an `email_domain` would be
  considered by the agent with no new word from Andrew. The gateway's domain table is the second fence: it admits a
  domain only on Andrew's word (NFRA_OPLGTW C7), so today the widening cannot reach the agent. COMM should still bind
  the agent's list to the five named parties, so that the two fences do not both rest on the gateway.
- **`--check-domains` prints `ok=False` because Alongside has no recorded domain.** That is the honest reading: C-MAIL
  says a party with no recorded domain is absent, never filled in. The issuer's close run should pass
  `--expect-missing 1` or record Alongside's absence beside the result.
- Until the issuer's real run (one considered mail texted, one not-naming mail silent), FWD-4 is APPLIED, not
  EXERCISED, as the COO half says.

-- 3.0.0_SA_CVO~Z

## RE-CUT 1 (2026-10-09 ~15:3xZ): cell CA-d-3, the KMS decoupling -- SIGNED

Against the COO half's RE-CUT 1 @cbe69f905d, edit `2c84d9521a`, fold UB-e9bc @cfef5928ad.

**Read at this seat:**
- **The edit:** `chat_assist.tf:34` declares `data "aws_kms_key" "ldo_001_transcripts" { key_id = "alias/${local.bucket}" }`,
  and `:88-89` pass its `.id` and `.arn` to `module.ldo_001`. A census of `chat_assist.tf` finds no remaining
  `aws_kms_key.transcripts` or `aws_kms_alias` reference. The module's own `.tf` files reference no key resource (the
  2 hits are in `modules/ldo/README.md`). The key-resource edge into `module.ldo_001` is gone by construction.
  Constraint 1 holds: the alias is a string, not the alias resource.
- **The alias target, live:** `alias/opal-data-transcripts` targets key `44a2284f-1e14-4ea1-b6cb-f6121bfde35a`, equal to the
  live `teams-global-chat-assist-handler-lambda` `LDO_KMS_KEY_ARN`. No live attribute moves.

**The falsifier was NOT live, and this half says so.** NFRA_TRNSPT s21 was applied and closed by 15:05Z
(`ba334f7dae`, `03bd9b3ca5`). `PLAN_D3.txt` was written at 15:11:19Z. With nothing pending on the key, `0/2/0` is what the
targeted preview reads with or without the decoupling, so CAd2-AC3's PASS does not discriminate. My e9bc condition (read
the preview while s21 is pending) could not be met once s21 landed. **The edge removal therefore rests on the reference
census above, not on PLAN_D3.** The Phase B final plan's Branch A (`0/3/0`, no key, reader or `LDO_KMS_KEY_ARN` line) stays the
real gate before the apply.

**What a caller can newly read or do:** unchanged from my original half. The decoupling adds one plan-time `DescribeKey`
read by the applier. It writes nothing and widens no caller.

**Accepted risks, both named:**
1. A key REPLACEMENT leaves the module on the old ARN until its next apply (CTO ruling 5).
2. A data source follows the ALIAS: retargeting `alias/opal-data-transcripts` to another key moves both functions'
   `LDO_KMS_KEY_ARN` and the module's KMS grants to that key at the next apply, with no diff on the key resource itself.

**SIGNED (re-cut 1)** -- `3.0.0_SA_CVO~Z`

## RE-CUT 2 (2026-10-09 ~17:2xZ): build pinned at 2ad98c2e3a after Phase B's Branch B (row Z-S3) -- SIGNED

Against the COO half's RE-CUT 2 @99d0d5cea8. **Read at this seat:** `git diff --numstat b1b8f5b4fe 2ad98c2e3a` over the
packaged paths moves 7 files, all outside COMM:
- `event_rules` +6;
- `key_rulings` +223/-4;
- `legacy_addresses` +50;
- `name_rulings` +154;
- `reporting_policies` +1/-1;
- `root_map` +421;
- `lib/opal_naming.py` +2/-1.

**What a caller can newly read or do: unchanged from my original half.**
- `data/transcripts/scripts/teams_chat/`, `scopes.json` and `mail_parties.json` are byte-unchanged in that range, so
  `mail_requests.firm_domains()` (which reads only those two registry files) resolves the same 4 parties, and C-MAIL's
  sender set does not move.
- The one widening-shaped change, `reporting_policies.json` `policies[2].firms` (`["cottonwood"]` ->
  `["cottonwood", "49financial", "inflection"]`), is IRPT's `irpt-ycdgen-research` policy. It rides in COMM's package as
  data, and no COMM module reads it. It is IRPT's act under IRPT's own ruling, not this deploy's.
- `opal_naming`'s cadence validator now also accepts an interval form. That widens which names grade conformant, not
  what any existing name resolves to.
- The 4 `key_rulings` deletions are metadata leaves (per the COO half). No address the agent resolves today changes; the
  Branch B import test stays the guard.

My RE-CUT 1 notes stand: the falsifier was not live, and the alias-retarget and key-replacement risks remain.

**SIGNED (re-cut 2)** -- `3.0.0_SA_CVO~Z`
