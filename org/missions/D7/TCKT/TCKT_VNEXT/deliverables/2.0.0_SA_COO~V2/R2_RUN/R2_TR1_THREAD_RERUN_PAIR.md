# TCKT_VNEXT R2-tr-1 -- the FWD-1 thread re-run: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~05:2xZ. **Authority:** CTO round-2 analysis @bbba700c22, section 4 item 3 ("a re-signed
pair") and section 3; CTO rulings msg 4015 and msg 4026 (the oracle is the read the ticket's own link performs, and that link opens
the finished report); CTO half of R2-rr-2 @51c5e7538b, condition 3. Cell `R2-tr-1` of `decompositions/TCKT_VNEXT_DECOMP_R2.md`.
The shape it re-signs: `R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md` v2.2 with COO-half AMENDMENTS 1-2, which is otherwise unchanged.

**This half is signed for a runner that does not exist at a pin yet.** Section 6 says what must be true of the runner before a run
order may cite this pair.

## 1. Measured at signing (2026-10-11 ~05:0xZ-05:2xZ, by this seat unless said)

| item | value | instrument |
|---|---|---|
| `irpt-status` live | CodeSha256 `6idtFvAmYk73...`, LastModified 2026-10-11T04:44:47Z, Successful | `get-function-configuration` |
| `opal-ticket-api` live | CodeSha256 `W03VREoMEmxN...`, LastModified 2026-10-11T04:19:14Z (the report-id check, R2-rr-2) | `get-function-configuration` |
| portal DEV | `7bb81fa897` on origin (the ticket's Open report reads the finished report) | `git -C portal ls-remote origin DEV` |
| portal DEV CI | run 38113443256 was `in_progress` at 05:0xZ; NOT read green by this seat | `gh run list` |
| the served DEV page | NOT measured: whether the DEV site serves the `7bb81fa897` build | -- |
| the synthetic filer row | ABSENT at 03:2xZ (ConsistentRead); not re-read since | `get-item` |

## 2. The identity (v2.2's, unchanged)

Row `opal-users-v2` `PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`: `firmId opal-capital`, `status active`,
`userType "test-filer"`, `allowedFirmIds` the LIST `["49financial"]`; written with `attribute_not_exists(PK)` and read back PRESENT.
ONE RS256 token, the CURRENT signing slot: `tier internal`, `role user`, `userType "test-filer"`, `firmId opal-capital`.
**`exp` = `iat` + N minutes, where N is the run's sized length + 5 and never more than 60.** Sized: the census (about 10 minutes
in round 1), the journey, and hop (e)'s bound of 40 polls 30 s apart (20 minutes). The token is memory-only; the key read is
reported after the fact through `0.0.0_AB_MSTR~DELL2`. Client reach: exactly `49financial`, by the row LIST on every clamped surface.

## 3. The act (executor `0.7.0_AE_CloudOps~TV2`; this seat holds no key)

0. Open the NEVER-2 ledger entry FIRST. Read EVERY live worktree's `.open_deploys/` (`git worktree list --porcelain`, then
   `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator. An open
   entry naming `irpt-status`, `opal-ticket-api`, `irpt-ycharts-generate` or `irpt-export-render` other than this run's is a STOP.
1. **Prechecks, before any write.**
   - `irpt-status` live CodeSha256 starts with `6idtFvAm`; anything else is a STOP that names the apply still owed.
   - `opal-ticket-api` live CodeSha256 starts with `W03VREoM`; anything else is a STOP (the id check would not be the one signed).
   - `reread_27.py` reads `READ27 27/27`.
   - **The refusal vocabulary.** With NO token, one GET of the finished-report route for a made-up `REQ-` id is expected 401. It
     shows nothing about codes, so the vocabulary is read at the first authenticated refusal in the run: if a refusal's reason
     reads as an INTERNAL string (for example `ANALYSIS_REPORT_NOT_READY`) and not a public code, the run records it and treats
     `ANALYSIS_REPORT_NOT_READY` and `REPORT_BUNDLE_ABSENT` as not-ready for this run. `R2_RUN/REPORT_READ_REFUSALS.md` (PROPOSED)
     is the table; this run is what confirms or corrects it.
2. Write the row, read it back, mint the token.
3. **The live census, v2.2's, unchanged,** with the ALL-origin token, BEFORE any hop: the 27 formerly-MORE_THAN_ONE routes resolve
   to `49financial` only; ticket CREATE admits a `49financial` target only; one data-refresh route is refused. Anything else is a
   STOP (cleanup per step 8).
4. **The journey, hops (a)-(d):** upload the synthetic input, file the Analysis Request ticket for `49financial`, claim it, submit
   the analysis. The request id is the one the service issues (the submission's answer, else the one new row in the firm's request
   list). The value the runner sent is recorded as `idempotency_token` and never read or stored.
5. **Hop (e), the oracle:** poll the finished-report read (`GET /api/scoped/investor-reporting/analysis/<REQ id>/sections`,
   `selected_tenant=49financial`), the read the ticket's own link performs since portal `7bb81fa897`. MET when a non-refusal 200
   carries the report for THAT id with at least one section. Polled only on not-ready codes, at most 40 polls 30 s apart. The bound
   reached is recorded NOT-READY, never a pass; then ONE further read names why, without widening anything: the job's own status
   route with the same token if the journey has one, else it is recorded as not read. Every other refusal is terminal at once.
6. **The report-route arms, then hops (f) and (g).**
   - Arm 1: POST the journey ticket's `/report` with the malformed id `sar1b-000000000000000000000000`: expected 400,
     `code INVALID_REPORT_REQUEST_ID`, nothing written.
   - Hop (f): POST the issued `REQ-` id: expected 200, stored. **A 400 here on the issued id is BRANCH B of the R2-rr-2 pair at
     once** (CTO half @51c5e7538b, condition 3): stop, cleanup, a BLOCKING row, and the re-apply of the `5a36586b5f` build is
     routed to the CTO as that pair's rollback. The journey is not re-run around it.
   - Hop (g): GET the ticket, take `report_ref.request_id` FROM THE TICKET, and read the finished report for it by the hop (e)
     read. Recorded: status, the id echoed, the count of sections, the body's byte length, a sha256 prefix.
7. **The page, once (the first live render of the cell R2-pg-1):** if the DEV site serves the `7bb81fa897` build and a browser
   session can be opened for the filer WITHOUT a new credential (the token set as the page's session, no password, no login-route
   change), open Ticket Center on DEV, press Open report on the journey ticket, and record ONLY: the canvas colour, whether the
   panel shows the report's sections or the waiting sentence, and the section count. No screenshot enters the repository. If the
   session cannot be opened that way, record `PAGE-NOT-RENDERED` with the reason; it is a row, not a failure of the run.
8. **Cleanup, in this order (the D2-S20 fix):** complete the journey ticket and the old test ticket `TCK-20261009-67ab7f27` (only
   if it reads `in_progress` and assigned to the filer; otherwise recorded as found); WAIT until the token's `exp` has passed;
   then delete the row and read it back ABSENT with ConsistentRead. The proof prints the `exp`, the later delete time and the
   absent read. The ledger closes only after this, on every branch.
9. **The zero-call read, with its positive control:** over `iat`..`exp`, count the filer's address in the data-refresh Lambda's
   log group, printing the streams searched; 0 streams searched is VOID. The control is the same filter over
   `/aws/lambda/opal-ticket-api`, which must find the filer. Only streams > 0, control >= 1 and matches == 0 is ZERO-CALLS-PROVEN.
10. Trace to the executor's folder; this seat copies identical bytes into `R2_RUN/`. Statuses, codes, ids, counts, byte lengths and
    hash prefixes only: no report contents, no figures, no account ids.

## 4. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-users-v2` row `USER#tckt-fwd1-testfiler-20261009@opal.invalid` | created, deleted after `exp` | delete + ConsistentRead ABSENT; never before `exp` |
| `opal-tickets`: ONE new ticket (49financial, `analysis_request`) | created, claimed, `report_ref` set, completed; mail: CREATE and CLAIM attempt the same notices round 1's runs 3 and 4 attempted. **Not re-read by this seat:** which addresses those notices resolve to for an internal filer's ticket (an internal distribution list on CREATE is possible). The executor records every `WE_*` line the two calls log; a `WE_CLIENT_SENT` to any address that is not the filer's `.invalid` address is a STOP before hop (d) | completed in cleanup; a ticket is never deleted |
| `opal-tickets` `TCK-20261009-67ab7f27` | `in_progress -> completed`, only if assigned to the filer | none needed (a test ticket); its malformed `report_ref` stays |
| IRPT, firm `49financial`: one upload, one accepted request, one generated report, their retained artifacts | created by the journey, as in round 1 run 4 | none: accepted records are immutable by design. They are synthetic-input test artifacts under `49financial`'s tenant, named `[TEST TCKT_VNEXT FWD-1]` |
| the vendor (YCharts) generation behind `irpt-ycharts-generate` | ONE report generation is requested | none; it is one vendor call of the kind the product makes. Round 1 never reached it (irpt-export-render ran 0 times), so this is its FIRST exercise from this project |
| data-refresh | in the radius; expected zero calls | step 9, with the positive control |
| every other firm | nothing: the census proves one firm before any hop | STOP + cleanup |

No IAM, code, route or Terraform change. No `kms:Decrypt` grant for any seat principal.

## 5. Branches (all signed)

- **A.** Every hop met, both arms as expected, hop (g) returns the report: FWD-1 goes to the CVO at L9 on the trace.
- **B.** A 400 from the report route on the issued id: section 3 step 6, the R2-rr-2 pair's Branch B.
- **C.** Hop (e) ends NOT-READY or on a terminal refusal: recorded with its code; hops (f) and (g) are UNREACHABLE; cleanup. The
  run is a RESULT, FWD-1 stays not realized, and the code names the next cell.
- **D.** Any STOP in steps 0-3: nothing of the journey runs; cleanup if the row was written.

## 6. What must hold before a run order cites this pair

1. The runner is `deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py` at a pin where `rn-safety` and `rn-arms` pass
   (TO-R2-rn1 AMENDMENT 2: token expiry by argument, cleanup in step 8's order, the precheck, the zero-call control, the arms).
   At signing they FAIL: the merged runner @de661bb225 still mints a 2-hour token and deletes the row first. **No run under this
   pair with that runner.**
2. Portal DEV CI for `7bb81fa897` reads green, or the order says the page step (7) is skipped and why.
3. The CTO half matches this text.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 4 and branches A-D, on the conditions of section 6.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
