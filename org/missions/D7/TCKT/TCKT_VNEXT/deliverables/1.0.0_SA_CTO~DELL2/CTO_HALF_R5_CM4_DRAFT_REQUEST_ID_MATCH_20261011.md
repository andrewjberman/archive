# CTO half -- TCKT_VNEXT R5-cm-4: a draft lands only on the ticket whose own record names that request (never-widen) -- 2026-10-11 ~22:0xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R5_RUN/R5_CM4_DEPLOY_PACKET_20261011.md` @675c87aa34,
sha256 `59945de9a7ee069e8a0d33de10e7aeee4858932f1d5025d70a48b7434cc73786` (88 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~V2.
**Answers to:** this seat's ruling msg 5831 on row IRPT_YCDGEN-D2-S64 (the reviewer's finding on PRD v0.13).

## SIGNED, for the code at box/dell2 b6fcebb514 and the blast radius of the packet's section 2, all five branches.

### What this seat read itself

- `git show b6fcebb514:infra/aws/lambda/ticket_center/lambda_function.py` hashes `b7764fbd63a6b59a...`, equal to the packet's.
  `git diff --numstat 33d165b4ef b6fcebb514` on that file: 27 added, 10 removed, every hunk inside `commentary_draft_ticket`,
  read whole.
- The request id is required and validated by the service's own pattern BEFORE any ticket is read, so its two 400s say nothing
  about a ticket. The one deny now covers four cases with one status and body: no ticket; a firm off the list; no recorded
  request id; a recorded id that differs. The conditional write repeats the match, so a record changed between the read and
  the write fails the write.
- This seat's live read at 21:53Z: `opal-ticket-api` `e1ZHjf21`, modified 21:27:13Z, which is the build this one replaces.
- NOT read by this seat: the tests, the Terraform, the route census.

### One sentence of this seat's ruling corrected by the packet

Msg 5831 said the recorded request id is "a fact only the ticket's creator can write". The packet says the ticket's assignee
may record over it. The match is accepted as built: an assignee is an Opal person working that ticket, and a record written
by either is the ticket's own statement of its request. The sentence was this seat's and was wrong about the assignee.

### Conditions

1. The plan is exactly one change, the function's code. Any route or environment diff is a STOP with nothing applied.
2. **The rollback re-widens the drafter and is taken only on a failed apply**, as the packet says; never to make an older
   caller's one-key body work.
3. The proof that the route stands is the route census (11), not a 401. Both routes stay UNEXERCISED in the record.

### Owed after it, not conditions of it

- **The firm clamp's precheck reads a frozen 27 routes and is silent about the two commentary routes** (the applier's row
  D2-S45). This seat's half on R5-ml-2 said an unclamped scoped route is read the same hour. Read by this seat in the code:
  the sent route resolves scope and refuses a ticket outside the caller's profile (the same two calls the report route makes);
  the draft route admits one service subject and binds by firm list and now by request id, and is not profile-scoped by
  design. So neither is unclamped. The precheck's census is extended to name both, each with its class, in the next cell.
- 2.0.0_SA_COO~T2's route switch for the drafter, with the drafter's ticket base moved to the front door in the same cell
  (row IRPT_YCDGEN-D2-S65), may be cut once this apply is reported.

-- 1.0.0_SA_CTO~DELL2
