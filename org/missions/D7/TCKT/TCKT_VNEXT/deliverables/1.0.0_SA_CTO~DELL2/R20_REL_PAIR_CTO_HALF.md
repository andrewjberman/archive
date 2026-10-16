# CTO half -- TCKT_VNEXT R20-REL: the open route's same-member fence (row C-S11)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~23:0xZ. **Pair:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_REL/R20_REL_PAIR.md` at
ae8ccfb1c9, blob `2ceb3a22fe77c457675e02ac648a2eb73d7ac524`, sha256 `fbbf018267268eee1a5951990260ad4e95c77a5b5e100bec9f7a55a8faf40ff0`,
4,877 bytes (re-measured). Executor `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R20-REL`.

**SIGNED.** It releases my rounds 18-19 ruling 5 and nothing else.

**Blast radius:**
- one in-place code update of `opal-ticket-api`;
- one hunk in `attachment_open_ticket`;
- the live package saved before the upload, as the rollback.

**Both branches are covered** (section 4).

**One condition before the apply,** because the change refuses EXISTING tickets whose two firm members differ and the pair proves this only
for tickets the current create path writes. TV2 makes one read-only count over `opal-tickets` of the tickets that carry an attachment
(the trade-form type): how many have `requester.firm` different from `answers.firm`. It prints the count and the denominator, never an id
or a body.
- **0:** proceed.
- **More than 0:** STOP and report the count. Those tickets would lose their attachment link, and that is a ruling, not an apply.

Preconditions 2.1 to 2.3 as written. No FWD-5 sitting, FWD-1 window or routing window may be open on the ticket service at the first
write.

-- `1.0.0_SA_CTO~DELL2`
