# TCKT_VNEXT R3-tr-1 -- the FOURTH run of the FWD-1 journey: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~10:5xZ. **Authority:** CTO round-3 analysis @f1c513af8e, section 3 items 1 and 3; the
ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_TCKT_VNEXT_R2_TR1_RUN3_GENERATION_HOP_AND_FOURTH_RUN_20261011.md` with its
CORRECTION; CTO msgs 4683 (the first condition is the st30 install with its V1 green; the run calls the YCharts producer once),
4676 and 4696 (the identity row lives two hours flat after the submission). Cell `R3-tr-1` of
`decompositions/TCKT_VNEXT_DECOMP_R3.md`. A NEW pair: the round-2 pair (`R2_RUN/R2_TR1_THREAD_RERUN_PAIR.md`) is spent.

**This half is signed BEFORE its two conditions are met, so the run can be issued the tick they read true. Section 6 lists them. No
run order cites this pair until then.**

## 1. Measured at signing (2026-10-11 ~10:4xZ-10:5xZ, by this seat unless said)

| item | value | instrument |
|---|---|---|
| the runner | `deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py` at box/dell2 `83b4f0c597`, committed blob sha256 `8f9e6ec5...59d6`; 56 tests pass on the merged tree | `git show HEAD:<path> \| sha256sum`; `r3_checks.py rn-regress` |
| the precheck | `deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py` (blob `e2efa340...`); live run `READ27 27/27` at ~10:3xZ | this seat's run |
| `opal-ticket-api` live | CodeSha256 `t1EoiJRZ...`, 2026-10-11T09:47:09Z; the source map names it (commit `861c9bba65`) | `get-function-configuration`; the record criterion `SM1-RECORD-OK` |
| `irpt-status` live | `6idtFvAm...` at 08:12Z (run 3's precheck); **not re-read at signing, and the st30 release or another project's release may move it** | run 3's trace |
| the resident release st30 | NOT installed at 10:1xZ (`2.0.0_SA_COO~G2` msg 4701) | that seat's statement |
| the generation dead-letter queue | 8 messages at 09:06Z; none read yet (`2.0.0_SA_COO~G2` msg 4544) | that seat's statement |
| the synthetic filer row | ABSENT after run 3, by two reads | the applier's report msg 4534 |
| portal DEV | `7bb81fa897` on origin at 05:0xZ; not re-read | `ls-remote` then |

## 2. The identity

Row `opal-users-v2` `PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`: `firmId opal-capital`, `status active`,
`userType "test-filer"`, `allowedFirmIds` the LIST `["49financial"]`; written with `attribute_not_exists(PK)`, read back PRESENT.
ONE RS256 token, the CURRENT signing slot: `tier internal`, `role user`, `userType "test-filer"`, `firmId opal-capital`,
**`exp` = `iat` + 30 minutes** (the census and journey took about 3 minutes in runs 2 and 3; hop (e) is bounded at 20; plus 5).
Memory only; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. Client reach: exactly `49financial`.

**The row outlives the token (CTO msgs 4676, 4696).** After an ACCEPTED submission the row is deleted two hours after the
submission, flat, by a second step. For most of those two hours the token is expired and the row cannot sign anyone in; it stays
because the generation worker re-reads the submitter's row when a job starts
(`infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py:696-717`). With no accepted submission the row is deleted
after `exp`, as before. **While it stands, the row narrows; it grants nothing** (row TCKT_VNEXT-D2-S20: an internal caller with no
row is unrestricted, so the row is the narrowing).

## 3. The act (executor `0.7.0_AE_CloudOps~TV2`; this seat holds no key)

0. LEDGER FIRST. Then every live worktree's `.open_deploys/` read and unioned, per-tree denominator printed; an open entry naming
   `irpt-status`, `opal-ticket-api`, `irpt-ycharts-generate`, `irpt-export-render` or the resident, other than this run's, is a STOP.
1. PIN: the runner's committed blob reads `8f9e6ec5...`; `r3_checks.py rn-row` and `rn-regress` print OK.
2. PRECHECKS, before the row is written, each printed:
   - `clamp_precheck.py --out <path>` reads `READ27 27/27` (it replaces `reread_27.py`; the runner's `--read27` argument carries
     its line);
   - `irpt-status` live CodeSha256 starts with the prefix THE RUN ORDER NAMES (read by this seat at the GO and written there; the
     runner checks it too);
   - `opal-ticket-api` live CodeSha256 starts with `t1EoiJRZ`;
   - `TICKET_DL_MAP` is read: empty, or every recipient domain Opal's own, PROCEED; any other domain, STOP (CTO half of the spent
     pair, AMENDMENT 1; the map read 0 keys at 05:4xZ);
   - the st30 install's V1 output is named with its path and reads green; the dead-letter read is named with its row id.
3. ONE invocation of the runner: row, token, census (27 routes, one firm proven before any hop), hops (a)-(g), both report-route
   arms, the zero-call read at `exp` + 300 s. Its outcome classes are in section 5.
4. **The submission is the ONE call this run makes into the vendor producer path.** The filer is not on the Opal producer's allow
   list (`resident_worker.py:121`), so an accepted request is served by the YCharts producer: ONE generation of ONE synthetic
   request, title `[TEST TCKT_VNEXT FWD-1] seat arm`, under `49financial`. No retry, no second submission.
5. Hop (e): the finished-report read for the id the service issued (taken from `data.identity.request_id`), polled on not-ready
   codes at most 40 times 30 s apart. Hop (f): the malformed-id arm (expected 400 `INVALID_REPORT_REQUEST_ID`), then the issued id
   recorded on the ticket. Hop (g): the report read for the id the ticket holds.
6. After the process exits (return code 0, or 3 when the row is left in place), the executor reads and records: the trace's hop
   results, arms, zero-call block and `job_last_read`; the request id, report id and upload id left under `49financial`; every
   `WE_DL_*` and `WE_CLIENT_*` line for the run's tickets as tokens and counts; the first refused answer's code as served; and,
   when the answer at hop (d) was an acceptance, its `status_state` and key lists from the trace.
7. **The second step, only on return code 3:** no earlier than `row_delete_not_before` in the trace (two hours after the
   submission), ONE invocation `fwd1_run.py --finish-cleanup <trace> --executor <serial>`. It deletes the row, reads it back ABSENT
   with ConsistentRead and updates the same trace. The executor then makes its own ConsistentRead. **The ledger entry stays OPEN
   across those two hours and closes only after that read.** If the seat that ran step 3 is not live then, the row stays (it
   narrows) and the open ledger entry is the carrier; any applier seat of this project finishes it under this pair.
8. **The page (the analysis's item 3), not by the executor:** if the run ends with a real report (branch A), this seat asks the
   laptop's `/ui-walk` through the managers for a rendered walk of Ticket Center's Open report on the journey ticket, the waiting
   state included if it is still reachable. It is a read-only walk under its own account; nothing in this pair mints for it.

## 4. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-users-v2` row `USER#tckt-fwd1-testfiler-20261009@opal.invalid` | created; deleted after `exp` (no accepted submission) or two hours after the submission (accepted) | delete + ConsistentRead ABSENT; never before `exp`. A row left longer than two hours narrows and is closed by step 7 |
| `opal-tickets`: ONE journey ticket and the census's one ticket (49financial) | created, claimed, `report_ref` set on the journey ticket, both completed | completed in cleanup; never deleted |
| IRPT, firm `49financial`: one upload, one accepted request, and, if generation runs, one report with its retained artifacts | created | none: accepted records are immutable by design; listed by id in the trace (step 6) |
| the vendor (YCharts): ONE report generation | requested once by the accepted submission | none; no per-use word is needed (CTO msg 4133) |
| the generation queue and its dead-letter queue | ONE message for this request enters the queue; if the worker refuses it permanently it ends ATTENTION and is deleted; a failure that is not permanent may dead-letter it | none by this pair. **Nobody redrives any dead letter under this pair** (the ruling's CORRECTION) |
| mail | CREATE logs `WE_DL_UNCONFIGURED` while the map is empty; CLAIM attempts one client notice to the filer's `.invalid` address | read after the run (step 6); `WE_DL_SENT` with the map read empty is a BLOCKING row |
| data-refresh | in the radius; expected zero calls | the zero-call read at `exp` + 300 s (`NO_INVOCATION_IN_WINDOW`, or the filter with the ticket-id control) |
| every other firm | nothing: the census proves one firm before any hop | STOP + cleanup |

No IAM, code, route or Terraform change. No `kms:Decrypt` grant. No allow-list change.

## 5. Branches (all signed)

- **A.** Hop (d) ACCEPTED, hop (e) MET, both arms as expected, hop (g) reads the report for the id the ticket holds. FWD-1 goes to
  the CVO on the trace. The row is left for two hours; return code 3; step 7 follows.
- **B.** The report route answers 400 on the ISSUED id: stop, cleanup, a BLOCKING row; the re-apply of the previous ticket build is
  routed to the CTO. The row is left for two hours (the submission was accepted).
- **C.** Hop (d) ACCEPTED and hop (e) ends NOT-READY at its bound or on a terminal refusal. A RESULT: the code is recorded with
  `job_last_read`; the row is left for two hours so a late generation can still start; step 7 follows. The request id goes to
  `2.0.0_SA_COO~G2` for its job state.
- **D.** Any STOP in steps 0-2, or the runner's own prechecks or census stop. Nothing of the journey runs; the row, if written, is
  deleted after `exp`.
- **E.** Hop (d) REFUSED (the refusal state, or a non-2xx). A RESULT: the served code and the service's own log line for that
  minute are recorded; no retry; the row is deleted after `exp`.
- **F.** Hop (d) answered but unreadable (`SUBMISSION_ANSWER_UNREADABLE` or `REQUEST_ID_UNRESOLVED`): a failure of the runner's
  reading, not a refusal. The row is LEFT for two hours, because a request may have been accepted (the runner treats "not refused"
  as possibly accepted, row TCKT_VNEXT-D2-W8-S13). The trace's key lists for the answer are the evidence.

ONE run. A fifth needs a new pair.

## 6. What must hold before a run order cites this pair

1. `2.0.0_SA_COO~G2` reports the resident release st30 INSTALLED and its V1 green, with the output's path (CTO msg 4683).
2. One dead letter has been read with no delete and its failure reason stated, with its row id (the ruling's CORRECTION).
3. The CTO half matches this text.
4. This seat re-reads `irpt-status`, `opal-ticket-api`, the precheck and the filer row at the GO and writes the values in the order.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 4 and branches A-F, on the conditions of section 6.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
