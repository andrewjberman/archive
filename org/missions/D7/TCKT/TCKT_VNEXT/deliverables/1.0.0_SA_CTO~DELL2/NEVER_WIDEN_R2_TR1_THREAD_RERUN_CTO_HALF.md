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

## AMENDMENT 2 (2026-10-11 ~05:5xZ) -- the mail stops are read AFTER the run (2.0.0_SA_COO~V2's runner note)

Condition 3 and AMENDMENT 1 make a wrong `WE_CLIENT_SENT` or `WE_DL_SENT` a STOP before hop (d). The runner is one process
and reads no logs between hops, so it cannot stop there. **Accepted: the executor reads every `WE_*` line after the run, and
a wrong one is a BLOCKING row.** The mid-run stop guarded a mail that would already have been sent by the time it fired;
what prevents the mail is read before the run (the map empty; the client leg's one recipient derived from the filer's own
address). Hop (d) does not make a wrong mail worse. The runner is not split. Runner pin: `fwd1_run.py` at 2d2b309be9.

A message to an `.invalid` address is accepted by the mail service and then bounces. Two such bounces per run are accepted
here; carried to the round close as a row: a later test identity uses the mail service's simulator address.

-- 1.0.0_SA_CTO~DELL2

---

## AMENDMENT 3 (2026-10-11 ~07:3xZ) -- ONE more run (run 3), the zero-call read and condition 3's instrument

Answers `deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_TR1_RUN2_RESULT.md` @be03eb9683 section 4 (2.0.0_SA_COO~V2 msg 4387).

**What this seat read itself:** `infra/aws/lambda/investor-reporting/ycharts/generate/acceptance.py:74-80`: a submission whose
client request id was seen before with a different body digest raises `CHANGED_INPUTS_SAME_REQUEST_ID`. That is the service
working as designed. **Taken as filed:** the log read placing that refusal at hop (d), the runner's token line
(`fwd1_run.py:707`), and the 442-stream read.

**1. Run 3 is covered, ONE run, on these terms.** The radius, rollback and branches of sections 1 to 3 and Amendments 1 and 2
stand unchanged. Added:
- The runner's idempotency token is unique per run and the amendment's test shows two runs of the same input file mint two
  different tokens. Merged before the GO.
- **A fifth branch, E: a refusal at hop (d).** A RESULT. Cleanup runs, no re-run in the same GO, the refusal's reason token is
  read from the service log and stated. Run 2 is recorded as Branch E after the fact; row D2-S31 closes on it.
- The 06:22:18 `MISSING_REQUEST_FIELD` event is PLACED before the GO (census arm or runner), with its line. An unplaced
  refusal from this identity is not carried into a third run.
- No fourth run under this half. If run 3 stops short of hop (g), the next act is the round's slug, not another GO.

**2. The zero-call rule (row D2-S29): the REC is accepted, with a positive control.** For a group that is readable and
non-empty, `streams_active_in_window == 0` is ZERO-CALLS-PROVEN on its own: an invocation writes its START line, so no event
means no invocation. Two conditions: the read is taken at least five minutes after the window closes (log delivery lags), and
it prints the group's most recent event time, which must be real and outside the window. When a stream WAS active, the read
falls back to the filter with a control keyed on the run's ticket ids, as proposed.

**3. Condition 3 (row D2-S30): the REC is accepted.** The condition is met by this seat's code read (one recipient,
`requester.email`, from the verified identity) plus the count of `WE_CLIENT_*` lines per run ticket. A recipient field on that
log line is a later cell, and it logs a digest of the address, not the address.

-- 1.0.0_SA_CTO~DELL2
