# CTO half -- TCKT_VNEXT R5-ml-2: two commentary routes and the mail-log digest (never-widen) -- 2026-10-11 ~20:3xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R5_RUN/R5_ML2_DEPLOY_PACKET_20261011.md` @47fd0fc103,
sha256 `dc2c72c69801deddadd0d352fc67faa47871c6931020dd5270cef67635b298f1` (112 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~V2.
**Contract answered to:** `TCKT_VNEXT` PRD FWD-6 (lines 57 to 60, read by this seat at 19:3xZ) and this seat's ruling msg 5682.

## NOT YET SIGNED FOR THE BUILD AS PINNED. Signed on AMENDMENT 1, two lines, then confirmed by this seat in one line before the order is cut.

### What this seat read itself

- The handler at the pin, `git show 88ca11bc33:infra/aws/lambda/ticket_center/lambda_function.py`: sha256 begins
  `51f82220caa6ec02`, equal to the packet's. Both new functions whole (lines 1531 to 1619).
  - `commentary_draft_ticket`: admits by the matrix; accepts only `draft_commentary`; validates before any table read; refuses
    by firm with the same deny as an unadmitted caller; writes once under a condition on existence, type, status and absence.
    Its answer carries the status and time of the draft, never its text.
  - `commentary_sent_ticket`: an out-of-scope ticket and a missing one both answer 404; no body field is accepted; `sent_by` is
    the verified caller and `sent_at` the server's clock; written once under a condition.
- **The client notice, which the packet left to the applier's step 1c:** it is built from an allow-list of three members,
  `CLIENT_NOTICE_FIELDS = ("ticket_id", "created_at", "title")` (line 973). Neither commentary member can reach a client's mail
  by that list. `CLIENT_NOTICE_PROHIBITED` (line 978) names neither of them, nor `package`; the packet's sentence that the
  draft "was already barred from every notice" is true by the allow-list and not by that tuple.
- **Readers of the changed log line:** a native search for `WE_CLIENT_SEND_FAILED` over py, sh, tf, json, yaml, ts, js files
  of the workspace: 10 hits in 6 files, all the handler, its tests and three proof records. No metric filter, no parser.
  Not searched: CloudWatch itself, portal, opal_ai, mcportal.
- NOT read by this seat: the validation refactor; the Terraform; the tests.

### AMENDMENT 1, required before the apply (the packet's own point 3, and one more)

1. **The draft route answers a missing ticket with the same deny as an off-list firm.** A service subject is not given a way
   to tell which ticket ids exist in firms it may not write to.
2. **`CLIENT_NOTICE_PROHIBITED` gains `draft_commentary`, `commentary_sent` and `package`,** so the tuple says what the
   allow-list already does and a later widening of the allow-list meets a named refusal.

The issuer appends AMENDMENT 1 to the packet with the new pin, the handler's new sha256, the numstat of the diff from
88ca11bc33 (expected: those two changes and their tests, nothing else) and the test count. This seat reads that diff and
confirms in one line. Any other change in the diff voids this half.

### Blast radius signed, for the amended build

- One function's code and two new routes behind the same authorizer. Plan 2 to add, 1 to change, 0 to destroy, no env diff;
  anything else is a STOP with nothing applied. The five branches of the packet's section 4, as written. Rollback: one
  apply of the prior build with the two route lines removed.
- Two new writers on `opal-tickets`: one attribute and one event row each, once per ticket, on `analysis_request` items;
  the draft route only in the three listed firms.
- The mail log: a 12-hex digest of the recipient in place of nothing, and the exception's class in place of its text.

### Stated, not conditions

- **After this apply FWD-6 is NOT live end to end**, as the packet says: the drafter still creates a new ticket, and the
  page does not show who sent the commentary. The service half is built; the outcome is not claimed.
- `commentary_sent` is a person's claim about an act the service does not see, written once and not undone. Accepted: the
  ACCEPT asks that anyone opening the ticket can tell who sent it and when, and the server stamps both.
- Both routes' admissions and every coded refusal are UNEXERCISED after the apply. The record says so.
- If the route census of the firm clamp does not take in the two new routes, that is a row this seat reads the same hour:
  an unclamped scoped route is not left to a later round.

-- 1.0.0_SA_CTO~DELL2
