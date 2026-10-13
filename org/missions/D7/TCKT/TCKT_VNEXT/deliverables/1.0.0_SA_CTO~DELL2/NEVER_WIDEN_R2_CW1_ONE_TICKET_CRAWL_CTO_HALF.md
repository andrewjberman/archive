# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R2-cw-1: one-ticket browser crawl

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~03:5xZ | **Verdict: SIGNED,** on the conditions of section 3.

**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_CW1_CRAWL_PAIR.md` @532566cb3f (read by
`git show` at that pin). COO half: signed in that file.

**Authority for the act:** Andrew, 2026-10-10, "crawl that instead" (row 15 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261010_133xZ_FIFTEEN_OPEN_ITEMS_ANSWERED.md`). On 2026-10-11 ~03:2xZ he was
shown the same call in a list headed "acts only he can do" and answered items 10 to 16 "I will deal with later"
(`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261011_032xZ_OPEN_CALLS_ANSWERED_ITEMS_1_TO_9.md`). This seat reads the
earlier, specific word as standing and has told him so at its terminal. **If he says "later" replaces it, this half is void and
no run is staged.**

## 1. The act and its blast radius

The packet's sections 3 and 4, as written: one synthetic internal-tier identity with the row LIST `["cottonwood"]`, one token of
at most 20 minutes, two writes made by the page (`claim` then `complete`) on `TCK-20261009-a1052909`, and removal of the identity
after `exp` in the same sitting. No IAM, code, route or Terraform change.

## 2. What this seat read itself

The packet's SES line said the pickup mail is refused, "read from the code and the item, not exercised". This seat read the code
too, `infra/aws/lambda/ticket_center/lambda_function.py` in the tree:

- `_client_recipients` (1004-1014) derives the recipient from `requester.email` alone: one string, or none.
- `notify_client` (1017-1035) refuses any recipient count but one, then calls `send_raw_email` with that one destination.
- `claim_ticket` calls `notify_client_isolated(..., "pickup")` once (1281); the wrapper catches every exception and prints
  `WE_CLIENT_SEND_FAILED` (1038-1056). No distribution-list send sits on the claim path.
- `complete_ticket` (1285-1335) sends nothing.

So the only mail the act can attempt is one message addressed to the literal string `svc-commentary`. **That SES refuses a
destination with no domain is expected, not measured.** The tree source is what was read, not the deployed bytes.

Taken from the packet: the ticket's fields (ConsistentRead by its author), the clamp's 404 behaviour, and the v2.2 removal method.

## 3. Conditions

1. **The deployed code is the code read.** Before step 2, the executor reads the ticket Lambda's live CodeSha256 and shows it is
   the build of the tree's `lambda_function.py` (source-map digest, or a member diff of the downloaded zip for the four
   functions named in section 2). A difference is a STOP.
2. **The mail branch, both ways.** After CLAIM the trace records the one `WE_CLIENT_*` line. `WE_CLIENT_SEND_FAILED` or
   `WE_CLIENT_NOT_SINGULAR`: proceed. `WE_CLIENT_SENT`: STOP before COMPLETE, a surprise row, and the message id is reported to
   this seat at once.
3. **Cottonwood is read as little as the page allows.** The crawler opens the board and the one target ticket. It opens no other
   ticket's detail. Nothing of any other ticket is written to a file, a screenshot or a trace.
4. **The one-firm proof, the zero-call read with its positive control, and the removal after `exp` are the packet's steps 3, 6
   and 7, unchanged.** Zero streams searched is VOID.
5. **A refused COMPLETE leaves the ticket `in_progress`.** That residue is accepted for this test ticket. Its reset is a
   separate pair; nothing writes the table directly under this one.
6. **Not covered:** any other ticket, any other route, a second token, a token past 20 minutes, a row that outlives the sitting.

Both branches are the packet's. Open call `dell2-20261009T022719Z-fbb1` closes on the board read of branch A.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 -- both test tickets, on Andrew's card-7 word (2026-10-13 ~12:3xZ)

**Authority:** Andrew, 2026-10-13 ~12:23Z, card 7 "Yes do it" (close `TCK-20261009-a1052909` and `TCK-20261012-13cd3a1d`):
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_122xZ_ANSWERS_TO_NINE_DELL2_CARDS.md`. It replaces the
"later" question of the 2026-10-11 paragraph above: the word is now specific to both tickets.

This half was signed 2026-10-11 against the pair @532566cb3f and stands (V2 msg 6911 read it as owed; it is not). The amendment
widens it by exactly one ticket:

1. **Targets:** `TCK-20261009-a1052909` and `TCK-20261012-13cd3a1d`, each CLAIM then COMPLETE. No other ticket is written.
2. **One identity, one token for both, at most 20 minutes.** If it expires before the second COMPLETE, the run STOPs; a second
   token is not covered.
3. **Firm list:** before the identity is minted, the executor reads both tickets' firm fields. Both `cottonwood`: the LIST stays
   `["cottonwood"]`. Either one on another firm: STOP and return here; the identity never lists two firms.
4. **Conditions 1 to 5 of section 3 apply to each ticket.** Condition 2's mail branch is read after EACH claim. A `WE_CLIENT_SENT`
   on either is a STOP before any further write.
5. **The removal after `exp` is unchanged.** The identity does not outlive the sitting.

Open calls `dell2-20261009T022719Z-fbb1` and `dell2-20261012T221957Z-5cb1` close on the board read showing both tickets `completed`.

**CTO half, AMENDMENT 1 -- `1.0.0_SA_CTO~DELL2`: SIGNED.**
