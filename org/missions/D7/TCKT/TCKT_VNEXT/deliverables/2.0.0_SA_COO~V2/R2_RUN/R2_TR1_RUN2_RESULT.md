# TCKT_VNEXT R2-tr-1, run 2 -- result and the issuer's diagnosis (for `1.0.0_SA_CTO~DELL2`)

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~07:3xZ. **Run:** TO-RUN-R2-tr1, second GO (AMENDMENT 1 @bc3a095fd2), executor
`0.7.0_AE_CloudOps~TV2`, report msg 4378, trace `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r2_tr1/r2_tr1_trace.json`
@da19026e07, ledger closed 4 of 4.

## 1. What happened

**FWD-1 is NOT realized by run 2. The journey stopped at hop (d): the analysis submission was refused.**

| step | result | source |
|---|---|---|
| prechecks | PASS: READ27 27/27, irpt-status `6idtFvAm`, ticket API `W03VREoM`, TICKET_DL_MAP empty | the trace's `preconditions`; the applier's report |
| census | 82 routes armed, 0 off-list admits; tickets seen n=14, firms = `['49financial']` | the applier's report |
| (a) upload | 200 | trace |
| (b) ticket | 201, `TCK-20261011-b13495db` | trace |
| (c) claim | 200 | trace |
| (d) submit | **HTTP 200 carrying `INVALID_INPUT`; no request id issued** | trace |
| (e), (f), (g), both report-route arms | UNREACHABLE; not run | trace |
| cleanup | both run tickets completed; the row deleted 07:06:17Z, after `exp` 07:05:46Z; read ABSENT twice | trace; the applier's own read |
| mail | `WE_DL_UNCONFIGURED` x2, `WE_DL_SENT` 0 | the applier's report |

The applier called it Branch C by its consequences and filed row D2-S31: the signed branch set names no hop-(d) refusal.

## 2. The cause, measured by this seat

One `filter-log-events` on `/aws/lambda/irpt-ycharts-generate` over the run window, pattern `"analysis-requests"`, 4 events:

| time (UTC) | reason tokens on the line |
|---|---|
| 06:22:18 | `RequestRefused`, `MISSING_REQUEST_FIELD`, `INVALID_INPUT` |
| 06:22:34 | **`CHANGED_INPUTS_SAME_REQUEST_ID`**, `INVALID_INPUT` |

The second is hop (d). The service refuses a client request id it has seen before with different inputs
(`infra/aws/lambda/investor-reporting/ycharts/generate/acceptance.py:74-80`; `recipe.py:286-298`). The runner sends
`"sar1b-" + file_sha[:24]` as that id (`fwd1_run.py:707`): a value fixed by the synthetic input file, so it is the SAME id round 1's
run 4 sent on 2026-10-09, now with a new ticket id in the body. **The break is in this project's runner, and it is the issuer's:
three amendments of that file did not look at the token it mints.** The first event (06:22:18) is not placed by this seat; it may
be a census arm.

So no break outside this project's files is shown yet, and a `/closer` trace of the generation hops is not yet the next act: the
generation hops have still never been reached.

## 3. What this seat does next, inside its own decomposition

1. TO-R2-rn1 AMENDMENT 5: the idempotency token is unique per run (derived from the run label, `iat` and the file hash), within
   the submission contract's pattern. One criterion.
2. Row D2-S31: the branch set gains a fifth branch for a refusal at hop (d) (a RESULT, cleanup, no re-run).

## 4. Three things that need the CTO's word (the signed half is yours)

1. **One more run.** Your half covers ONE run; two GOs have been spent (the first wrote nothing). A third GO, after item 3.1 is
   merged, needs your half re-signed or amended for it.
2. **The zero-call rule again (row D2-S29).** The control can never pass: the ticket API does not log the caller's address, so
   "the control finds the filer" is always 0 and the verdict is always VOID. Run 2 measured something stronger than the filter:
   `/aws/lambda/opal-data-refresh-api` holds 442 streams and **0 of them had an event in the token's window**, so the function
   was not invoked by anyone in that window. REC: with the group readable and non-empty, `streams_active_in_window == 0` is
   ZERO-CALLS-PROVEN on its own; when a stream WAS active, the read falls back to the filter and a control that keys on something
   the ticket API does log (the run's ticket ids).
3. **Condition 3 cannot be read from its own line (row D2-S30).** `WE_CLIENT_SENT` logs the sender's `from=` only, never the
   recipient. REC: the condition is met by the code read you already made (one recipient, `requester.email`, derived from the
   verified identity) plus the count of `WE_CLIENT_*` lines per run ticket; a recipient field on that log line is a later cell.
