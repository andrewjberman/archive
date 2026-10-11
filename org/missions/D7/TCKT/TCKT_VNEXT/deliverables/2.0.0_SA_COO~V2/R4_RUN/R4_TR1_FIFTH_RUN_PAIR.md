# TCKT_VNEXT R4-tr-1 -- the FIFTH run of the FWD-1 journey, which is also the ONE vendor sign-in diagnostic: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~16:4xZ. **Authority:** the CTO's round-4 analysis @8d93c41f11 sections 2 and 4 item 4;
CTO msg 5327 ("my word on the fifth run is this far and no further. Write its pair now ... ONE request, filed through the form's
one-step path, causing ONE vendor sign-in on the host ... No request is submitted until both halves are signed"); CTO msg 4918 (no
other request down the YCharts path); CTO msg 5176 (the two arms of `R4-la-1` ride this run). Cell `R4-tr-1` of
`decompositions/TCKT_VNEXT_DECOMP_R4.md`. A NEW pair: the fourth run's (`R3_RUN/R3_TR1_FOURTH_RUN_PAIR.md`) is spent.

**Nothing is submitted under this half. It is signed BEFORE its conditions (section 7), and one of them is a build this seat
still owes (section 1, the runner).**

## 1. Measured at signing (2026-10-11 ~16:3xZ, by this seat unless said)

| item | value | instrument |
|---|---|---|
| the resident release st32 | host runs `0485393f3a-st32` since 16:10Z, V1 green, 0 capture lines since start, unbound; the allow list holds Andrew's sign-in only | `2.0.0_SA_COO~G2`'s read of the host's own output, `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/ROUND13_DRAIN_END_READ_20261011.md` @379b54bea0; NOT re-read by this seat |
| `opal-ticket-api` live | CodeSha256 `d2w1YJ8A...`, 2026-10-11T15:18:51Z, handler `c4003667`; `PACKAGE_ALLOWED_FIRMS` present, length 0 | this seat, 15:38Z; a second apply (`R4-pk-3`) may move the env before the run |
| `irpt-status` live | `6idtFvAm...` since 11:26:53Z | the CTO's read at 13:52Z (msg 5101); NOT re-read by this seat |
| portal DEV | `c3a03c246a` on origin after a fetch at ~16:3xZ; the form's one-step path read at that commit (section 3) | `git -C portal rev-parse origin/DEV`; `git show origin/DEV:src/pages/TicketCenter/analysisRequest.ts` |
| the runner | at box/dell2 `bd97cf87e7`, blob `e4a6dac4`: it files with a CLAIM and submits a body WITHOUT `ticket_id`. **It cannot file the one-step path today.** A build cell `R4-rn-2` adds a one-step mode; the run order names the blob it produced | `git show HEAD:<path> \| sha256sum`; this seat's read of the form against the runner's hops |
| the synthetic filer row | ABSENT at 13:24Z | this seat's ConsistentRead |
| the vendor session on the host | signed out at 11:34Z (run 4); `2.0.0_SA_COO~P2`'s read (CTO msg 4918 item 1, relayed in the round-4 analysis): the sign-in form was submitted and the probe never passed; whether the vendor accepted the credentials cannot be told | the round-4 analysis section 2; NOT re-read by this seat |

## 2. The identity

Row `opal-users-v2` `PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`: `firmId opal-capital`, `status active`,
`userType "test-filer"`, `allowedFirmIds` the LIST `["49financial"]`; written with `attribute_not_exists(PK)`, read back PRESENT.
ONE RS256 token, the current signing slot: `tier internal`, `role user`, `userType "test-filer"`, `firmId opal-capital`,
`exp` = `iat` + 30 minutes. Memory only; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. Client reach:
exactly `49financial`. After an ACCEPTED submission the row is deleted two hours after the submission by the runner's second
step, as in the fourth run (the worker re-reads the submitter's row when a job starts); with no accepted submission it is deleted
after `exp`. While it stands the row narrows; it grants nothing (row TCKT_VNEXT-D2-S20).

## 3. "Filed through the form's one-step path": what that means here, said plainly

The form (portal DEV, `src/pages/TicketCenter/analysisRequest.ts`, `fileAndRequestAnalysis`, read at `c3a03c246a`) makes FOUR
calls in order: (1) the upload; (2) create the ticket with `source "ticketcenter:i1"` and the attachment; (3) submit the analysis
with `request_id "tckt-<ticket id>"`, `ticket_id`, the held `input_id`, and no claim by anyone; (4) record the issued id on the
ticket as the ticket's CREATOR.

**This run does not execute the form's code. The runner makes those same four calls, with the same fields, as the synthetic
filer.** No seat holds a portal sign-in for a filer, and this pair mints none. So this run exercises LIVE: the service side of
all four calls, including hop 16's creator branch (never exercised) and a ticket-bound request reaching the resident (never
exercised). It does NOT exercise: the page's own code path, its messages, or its rendering. The rendered read of the journey
ticket's page (the Open controls, the waiting state) is asked of the laptop's `/ui-walk` after the run, read-only, under its own
account; if the CTO half requires the page itself to do the filing, that is a staff person's act and this pair does not cover it.

## 4. The act (executor `0.7.0_AE_CloudOps~TV2`; this seat holds no key)

0. LEDGER FIRST. Every live worktree's `.open_deploys/` read and unioned, denominator printed; an open entry naming
   `irpt-status`, `opal-ticket-api`, `irpt-ycharts-generate`, `irpt-export-render` or the resident, other than this run's, is a STOP.
1. PIN: the runner's committed blob reads the value THE RUN ORDER NAMES (from `R4-rn-2`'s drain); its checks print OK.
2. PRECHECKS, before the row is written, each printed: `clamp_precheck.py` reads `READ27 27/27`; `irpt-status` and
   `opal-ticket-api` live CodeSha256 start with the prefixes the run order names; `TICKET_DL_MAP` empty or Opal-only domains; the
   filer row ABSENT; **the host runs st32 and its journal shows 0 capture, eviction or session-refresh lines since the last read
   `2.0.0_SA_COO~G2` names** (that seat's read, taken at the GO and written in the order: it is the proof that this run's sign-in
   is the FIRST after st32, and that nobody else sent a request meanwhile); **the generation queue reads 0 visible and 0 in
   flight** (the same seat's read).
3. ONE invocation of the runner in its one-step mode:
   - the row, the token, the census (one firm proven before any hop);
   - call 1 the upload; call 2 the ticket, `source "ticketcenter:i1"`, NOT claimed;
   - **the two arms, BEFORE anything is recorded:** the malformed report id as the creator on the unclaimed ticket (expected 400
     `INVALID_REPORT_REQUEST_ID`, `report_ref` still absent); ONE POST to the package door as the filer (expected 403, `package`
     still absent). An unexpected answer on an arm is recorded and the run GOES ON to the submission only if nothing was written
     to the ticket; a 2xx from the package door STOPS the run before the submission (cleanup, no request sent);
   - **call 3, THE ONE SUBMISSION**: the form's body, `request_id "tckt-<ticket id>"`, `ticket_id` the journey ticket. This is
     the only call in the run that reaches the vendor path. It is sent ONCE. No retry on any answer, including a timeout: a
     timeout is treated as possibly accepted (branch F);
   - call 4, on an accepted answer: record the issued `REQ-` id on the ticket as the creator (expected 200, `recorded_by` the
     filer). Then ONE repeat of the same record call (expected 409 `REPORT_ALREADY_RECORDED`, the stored value unchanged);
   - the finished-report read for the issued id, polled on not-ready codes at most 40 times 30 s apart; then the report read for
     the id the ticket holds;
   - cleanup: both tickets completed; the row left in place on an accepted submission (return code 3); the zero-call read.
4. After the process exits the executor reads and records: the return code; every call's status, state and code; the answer's
   `status_state` and key lists at the submission; both arms; both record calls; `job_last_read`; what was left under
   `49financial` by id, named as immutable test artifacts in a client firm's store; every `WE_DL_*` and `WE_CLIENT_*` line for the
   run's tickets as tokens and counts; its own ConsistentRead of the row.
5. **The host-side reads are NOT the executor's.** `2.0.0_SA_COO~G2` orders them of `0.7.0_AE_CloudOps~YC2`, read-only, after
   the report read ends or its bound is reached: (i) the journal's named lines for this request id: received, producer, and
   where it stopped or that it reached READY; (ii) **the sign-in receipt st32 keeps. Before ANY of it is quoted in any file or
   message it is checked for a posted value, a cookie and a tokenised URL; what is quoted is field NAMES, status codes, lengths
   and hash prefixes only. If the check finds any of the three, the finding is reported as a count and the receipt is not
   copied off the host.** This seat quotes nothing from the receipt that `2.0.0_SA_COO~G2` has not already cleared.
6. The second step, only on return code 3: no earlier than `row_delete_not_before`, ONE `--finish-cleanup`; the executor's own
   ConsistentRead ABSENT; the ledger stays OPEN until then.
7. The page: after a real report (branch A), this seat asks the laptop's `/ui-walk` through the managers for a rendered walk of
   the journey ticket. Read-only; nothing in this pair mints for it.

## 5. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-users-v2` row `USER#tckt-fwd1-testfiler-20261009@opal.invalid` | created; deleted after `exp`, or two hours after an accepted submission | delete + ConsistentRead ABSENT; never before `exp` |
| `opal-tickets`: ONE journey ticket (source `ticketcenter:i1`, unclaimed) and the census's one ticket, both `49financial` | created; `report_ref` set ONCE on the journey ticket by its creator; both completed | completed in cleanup; never deleted. A `report_ref` once recorded by the creator cannot be replaced by the creator |
| IRPT, firm `49financial`: one upload, ONE accepted request carrying `ticket_id`, and, if the sign-in passes, one report with its retained artifacts | created | none: immutable by design; listed by id |
| **the vendor account (YCharts): ONE sign-in attempt by the host, and on success ONE report generation** | one attempt; on failure the vendor may count a failed sign-in against the account | none. **This is the act's one irreversible outward effect. The bound is the count: ONE request, so ONE job, so the host's one capture attempt and at most its one redelivery** (run 4: a retry at +15 minutes found the session signed out and ended ATTENTION with its refresh already used; whether st32's redelivery makes a SECOND sign-in attempt is NOT known to this seat and is `2.0.0_SA_COO~G2`'s to state in the CTO half or before it) |
| the generation queue and its dead-letter queue | ONE message for this request; it ends handled (READY or ATTENTION) or, on a non-permanent failure, may dead-letter | none by this pair. Nobody redrives it or any dead letter |
| the host's kept receipt of the sign-in | written by st32 | none; read under step 5's rule |
| mail | CREATE logs `WE_DL_UNCONFIGURED` while the map is empty; no CLAIM happens in the one-step path, so no client notice is expected | read after the run; `WE_DL_SENT` with the map read empty, or any `WE_CLIENT_*` send, is a BLOCKING row |
| data-refresh | in the radius; expected zero calls | the zero-call read |
| the package door | ONE refused POST by the filer; with the list empty nobody can be admitted | none needed |
| every other firm | nothing: the census proves one firm before any hop | STOP + cleanup |

No IAM, code, route or Terraform change. No `kms:Decrypt` grant. No allow-list change. No identity but the filer's.

## 6. Branches (all signed)

**The sign-in, both branches the CTO named:**
- **S-PASS.** The host signs in, the job reaches READY, a report is made. The run goes on to branch A or its failures below.
- **S-FAIL.** The sign-in fails under the reason st32 records; the job ends ATTENTION. **NO second request is sent by anyone:
  not by this executor, not by this seat, not as a retry, not as a "confirmation", and no dead letter is redriven.** The run's
  report read ends NOT-READY at its bound (branch C). The receipt and the journal are read under step 5. The next request on the
  vendor path needs the CTO's word again.

**The journey:**
- **A.** Submission ACCEPTED, the creator's record 200 and its repeat 409, the finished report read for the issued id and for
  the id the ticket holds. FWD-1 goes to the CVO on the trace, stated as: the service journey of the one-step path, the form's
  code not executed, the YCharts producer.
- **B.** The creator's record is refused (anything but 200) after an accepted submission: a RESULT and a BLOCKING row; the
  request stands, the report read still runs for the issued id; hop (g) is UNREACHABLE. No second record attempt beyond the one
  repeat the act names.
- **C.** ACCEPTED and no finished report at the bound, or a terminal refusal of the report read. A RESULT; the row left two
  hours; step 5 says why.
- **D.** Any STOP in steps 0-2, the runner's own precheck or census stop, or a 2xx from the package door. NOTHING is submitted.
- **E.** The submission is REFUSED (the refusal state or a non-2xx): no sign-in is caused if the refusal precedes the queue; the
  served code and the service's log line for that minute are recorded; no retry.
- **F.** The submission's answer is unreadable or the call times out: treated as possibly accepted. The row is left two hours;
  NO second submission; the request list is read once for a `tckt-<ticket id>` request to settle it.

ONE run. A sixth needs a new pair and the CTO's word.

## 7. What must hold before a run order cites this pair

1. `R4-rn-2` (the runner's one-step mode) is built, drained and its blob named in the order.
2. The CTO half matches this text, and states or accepts the open point of section 5 (whether st32's redelivery makes a second
   sign-in attempt).
3. `2.0.0_SA_COO~G2` gives, at the GO: the host's journal count since st32 (0 expected) and the queue's two counts.
4. This seat re-reads `irpt-status`, `opal-ticket-api`, the precheck, portal DEV's form (the four calls unchanged) and the filer
   row at the GO and writes the values in the order.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 5 and every branch of section 6, on the conditions of section 7.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
