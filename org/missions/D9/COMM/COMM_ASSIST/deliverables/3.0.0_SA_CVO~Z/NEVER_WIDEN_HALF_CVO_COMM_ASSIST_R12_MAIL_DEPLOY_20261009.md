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
