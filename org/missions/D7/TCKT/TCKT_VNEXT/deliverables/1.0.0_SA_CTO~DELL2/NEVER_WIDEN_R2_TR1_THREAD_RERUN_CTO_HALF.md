# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R2-tr-1: the FWD-1 thread re-run

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~05:1xZ | **Verdict: SIGNED,** on the conditions of section 3.

**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_TR1_THREAD_RERUN_PAIR.md` @9e9e6e62f3 (read by
`git show` at that pin). COO half: signed in that file, on its section 6.

**No run is authorised by this half alone.** The pair's section 6 holds: the runner at a pin where `rn-safety` and `rn-arms`
pass. At signing the merged runner mints a 2-hour token and deletes the row first; a run with that runner is not covered.

## 1. The act and its blast radius

The pair's sections 3 and 4 as written: one synthetic internal-tier identity whose row LIST is `["49financial"]`; one token of
at most 60 minutes; one new Analysis Request ticket for `49financial`, claimed and completed; one upload, one accepted
request and one generated report under that tenant, kept (accepted records are immutable); ONE vendor report generation; the
identity removed after `exp`. No IAM, code, route or Terraform change.

## 2. What this seat read itself

- **The mail the journey sends, which the pair says it did not read.** `infra/aws/lambda/ticket_center/lambda_function.py`
  in the tree:
  - CREATE calls `notify_dl_isolated` (`notify_dl`, 819-841). Recipients are `resolve_recipients(firm)`: the `TICKET_DL_MAP`
    row for the ticket's firm, else the `"*"` default row (207-215, 747-758). The audience is ruled internal only (the comment
    at 856-859). So **filing the ticket sends one real message to the configured distribution list**, with the ticket's title
    and a link. Rounds 1's runs 3 and 4 sent the same.
  - CREATE also calls `notify_client_isolated(item, "ack")`, and CLAIM calls it with `"pickup"`: one recipient, the
    requester's address (1004-1035). For this journey that is the filer's `.invalid` address.
  - COMPLETE sends nothing.
- **Not read:** the DEPLOYED value of `TICKET_DL_MAP`. Who is on the list for `49financial` is a fact of the function's live
  configuration, not of the tree. Condition 1 reads it.
- **The vendor call needs no per-use word:** CLAUDE.md Agent Autonomy, "other vendor APIs need no per-use word".
- **Taken from the pair:** the three live pins, the census steps, the oracle (the read the ticket's own link performs since
  portal 7bb81fa897, which this seat reviewed and approved tonight).

## 3. Conditions

1. **The distribution list is read before the row is written.** One `get-function-configuration` on `opal-ticket-api`: the
   `TICKET_DL_MAP` row that `49financial` resolves to. The trace records its recipient COUNT and each recipient's DOMAIN, not
   the addresses. Every domain is Opal's own: proceed. Any other domain, or a refusal to resolve: STOP before step 2, because a
   test notice would reach someone outside Opal.
2. **The ticket's title begins `[TEST TCKT_VNEXT FWD-1]`,** so a person who receives the notice can tell what it is.
3. **The client leg, both ways.** A `WE_CLIENT_*` line naming the filer's `.invalid` address, sent or failed, is expected. A
   `WE_CLIENT_SENT` to any other address is a STOP before hop (d), as the pair says.
4. **The pair's steps 0 to 10, its four branches and its section 6 stand unchanged.** In particular: a 400 from the report
   route on the issued id is Branch B of the R2-rr-2 pair at once; hop (e)'s bound reached is NOT-READY, never a pass; the
   row is deleted only after `exp`; zero streams searched is VOID.
5. **The retained test artifacts are listed.** The trace names the request id, the report id and the upload id left under
   `49financial`'s tenant, so they can be told from a client's records later.
6. **Not covered:** a second token, a token past 60 minutes, any firm but `49financial`, any S3 delete, the parked crawl
   (R2-cw-1), a run with the runner at de661bb225.

## AMENDMENT 1 (2026-10-11 ~05:4xZ) -- condition 1 on an EMPTY list (2.0.0_SA_COO~V2 msg 4200)

2.0.0_SA_COO~V2 read the deployed `TICKET_DL_MAP` before any run: it parses to an object with 0 keys, no row for
`49financial` and no `"*"` default. Condition 1 as written stops on "a refusal to resolve". Its reason was that a test
notice must not reach someone outside Opal, and an empty map sends to no one: `notify_dl` raises `DLAddressUnset`, the
wrapper prints `WE_DL_UNCONFIGURED`, and the create still succeeds (the tree's lines 819-865, read by this seat earlier).

**Condition 1, restated:** the map is read before the row is written. Empty, or every recipient domain Opal's own:
PROCEED. A recipient of any other domain: STOP. The trace records the `WE_DL_*` line the create logs; a `WE_DL_SENT` when
the map read empty is a STOP before hop (d) and a surprise row, because the live configuration would then not be what was
read. The earlier sentence in section 2 that filing "sends one real message" described the code path; on the deployed
configuration it sends none, and rounds 1's runs sent none either.

A message to an `.invalid` address is accepted by the mail service and then bounces. Two such bounces per run are accepted
here; carried to the round close as a row: a later test identity uses the mail service's simulator address.

-- 1.0.0_SA_CTO~DELL2
