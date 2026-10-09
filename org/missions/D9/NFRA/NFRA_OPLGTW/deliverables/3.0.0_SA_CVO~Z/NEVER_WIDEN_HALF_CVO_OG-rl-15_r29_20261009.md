# Never-widen half (CVO) -- OG-rl-15, the r29 gateway release

By: `3.0.0_SA_CVO~Z`, standing in for `3.0.0_SA_CVO~O` (not registered), 2026-10-09 ~07:5xZ, on `2.0.0_SA_COO~O` msg
32437 (acked).
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/ANNOUNCE_OG-rl-15.md` @368e48e533 (now in
box/sitez HEAD), section 13 Half 3 and section 14 (Phase C). Pinned to release sha
`91811b648ab119e73e22f8d401dd09f45b8ab19b`. COO half: @40b39ad88d.

## What I read before signing

- **Release sha** `91811b648a` exists as a commit.
- **Its domain table** (`infra/aws/ec2/opal-gateway/deploy/mail_sender_domain_table.txt`, non-comment lines) holds
  exactly four entries: `opalinvest.com`, `49financial.com`, `cottonwoodmail.com`, `inflectionwealth.com`. Alongside
  is absent and `demo.test` is absent.
- **Its matcher** (`app/mail_route.py:107-109`, `:168-170`): the table is lowercased into a frozenset; a sender's domain
  is the text after the last `@`, stripped and lowercased; membership is whole-string. No subdomain match and no
  suffix match, as PRD C7 (v1.8, `:668-670`) states.
- **The PRD at HEAD** (v2.3 @39f5404132, ratified-text SIGNED):
  - C7 v1.8/v1.9 (`:685-695`): the table holds the named parties' domains, looked up, five at most, read by these
    halves.
  - FWD-12 (`:155-163`, "13 months for now") and v2.0 item 4 (`:740`): `calendar_months` 1-13, exactly one of the two
    fields.
  - `:731`: authorized grants are Andrew's and Alyssa's principals only.

## SIGNED: what a caller can newly read or do (Half 3)

1. **Mail by sender domain.** Before r29, the route reads 3 exact addresses. After r29, it reads every address at the 4
   domains above, in Andrew's own mailbox only (C7 `:663-665`). It is GET only and returns v1.4's five fields, with
   windows of at most 31 days and audit hashes with no addresses. An empty table refuses with 403. These are the
   table entries C7 says the halves read. **Signed.**
2. **A second holder of the mail bearer (`commassist`, the laptop Teams agent).** C7 `:694` ratified the domain read
   "by the bearer's one holder", and the PRD carries no text for a second holder. Its authority is issuer amendment A1
   and ruling D4, on `1.0.0_SA_CTO~O` msg 32212 relaying the laptop's COMM_ASSIST ask. **Signed, as a named widening of
   WHO may read**, for three reasons:
   - The new holder is an internal Opal agent reading Andrew's own mailbox for Andrew's stated purpose (C7 `:657-661`:
     his mail read for work requests, the body test done by the laptop's caller).
   - The same five fields and the same four domains apply.
   - The label is audited per presenter.
   Both branches are covered: if the leg is applied, there are two values and two labels; if the secret is missing,
   the deploy refuses before any change (section 10 item 7). Writers: 1 of `.env`, 1 of the role policy.
3. **Alyssa's reach, 30 days -> 13 months (Phase C).** One principal and one field (`scope.dates.calendar_months` = 13).
   Her prior revision 3 is recorded before the write; the rollback is a re-activation of revision 3's scope. Both
   branches are covered: the grant parses and a 13-month read returns at least one qualified date per master, or
   nothing is written. The grant rolls back before any gateway rollback, never after, because the r28 parser refuses
   the field. This is within FWD-12 and `:731`. **Signed.**
4. **`opal_asker_query` becomes SAFE.** It is a read tool, its output is unchanged, and no confirm step remains.
   **Signed.**
5. **Contract 1.4 is additive.** No tool or route is added or removed (66 -> 66), consent stays at 9, and there is no
   Bloomberg change. **Signed.**

## Carried (not grounds)

- **PRD text vs the act.** C7 `:694` still says "the bearer's one holder". `1.0.0_SA_CTO~O` should addend C7 to name
  both holders (`msgpull`, `commassist`) so the ratified text matches the served state. Until then, this half is the
  record of the widening.
- **The domain list is a lookup, not Andrew's list read by this seat.** C7 says the five parties come from his
  2026-10-07 ~18:3xZ record item 6, as read by this seat in an earlier session. The four entries match the registry
  rows the ask prints (`scopes.json`, `mail_parties.json`). Other firm domains on user rows (`cottonwood.com`,
  `inflection.com`, `inflectionwealthmgmt.com`) are not admitted; adding one needs Andrew's word.
- **Z-W42-S2 stays ARMED** (the 13-month read cost is unmeasured). Phase C records the elapsed time.

-- 3.0.0_SA_CVO~Z
