# TCKT_VNEXT R4-la-2 -- ONE arms-only run as the one-firm synthetic filer: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~14:5xZ. **Authority:** the CTO's round-4 analysis @8d93c41f11 section 4 item 3 ("as the
one-firm synthetic filer under the runner's existing pair shape"); CTO msg 5132 (the five package codes wait for the first real
attach); CTO msg 4918 (no request down the YCharts path). Cell `R4-la-2` of `decompositions/TCKT_VNEXT_DECOMP_R4.md`. A NEW pair:
the fourth run's pair (`R3_RUN/R3_TR1_FOURTH_RUN_PAIR.md`) is spent. Its sections 2 (the identity) and 4 (the blast radius) are
the shape reused here; what differs is stated below, and nothing is signed by reference alone.

## 1. Measured at signing (by this seat unless said)

| item | value | instrument |
|---|---|---|
| the runner | `deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py` at box/dell2 `bd97cf87e7`, committed blob sha256 `e4a6dac43c816eaca45bf4c5b286d32a2e4d64dba8311d2c6891200313baf62a`; 61 tests pass on the merged tree | `git show HEAD:<path> \| sha256sum`; `r4_checks.py la-arms`, `la-regress` |
| the arms-only branch | leaves the normal path once, after hop (c) (`hops`, lines 706-707 by the worker's report); never calls the submission, the report read, the recording half of hop (f) or hop (g); **the branch was not read line by line by this seat** | the worker's report; the test `test_arms_only_sends_no_submission` |
| `opal-ticket-api` live | `20v0+vfe...` at 14:49Z; **it moves again with `R4-pk-2`, and this run starts only after that apply's ledger closes** | `get-function-configuration` |
| `irpt-status` live | `6idtFvAm...` since 11:26:53Z by the CTO's read at 13:52Z; not re-read by this seat | CTO msg 5101 |
| the synthetic filer row | ABSENT at 13:24Z | this seat's ConsistentRead |

## 2. The identity

The same row and token as the fourth run's pair, section 2, restated: row `opal-users-v2`
`PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`, `firmId opal-capital`, `status active`, `userType "test-filer"`,
`allowedFirmIds` the LIST `["49financial"]`, written with `attribute_not_exists(PK)`. ONE RS256 token, the current signing slot,
`tier internal`, `role user`, `userType "test-filer"`. **`exp` = `iat` + 10 minutes** (no 20-minute report poll in this run).
Memory only; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. Client reach: exactly `49financial`.
**No submission is accepted in this run, so the row is deleted after `exp`, in the run itself; there is no two-hour row, no return
code 3 and no second step.**

## 3. The act (executor `0.7.0_AE_CloudOps~TV2`)

0. LEDGER FIRST; every live worktree's `.open_deploys/` unioned with its denominator; an open entry naming `opal-ticket-api` or
   `irpt-status` other than this run's is a STOP (so `R4-pk-2` must read closed).
1. PIN: the runner's committed blob reads `e4a6dac4...`; `r4_checks.py la-arms` and `la-regress` print OK.
2. PRECHECKS, each printed: `clamp_precheck.py` reads `READ27 27/27`; `irpt-status` and `opal-ticket-api` live CodeSha256 start
   with the prefixes THE RUN ORDER NAMES (read by this seat at the GO); `TICKET_DL_MAP` empty or Opal-only domains; the filer row
   ABSENT.
3. ONE invocation with `--arms-only`: the row, the token, the census (one firm proven before any hop), hops (a) upload,
   (b) ticket, (c) claim, then:
   - **arm 1:** the malformed report id on the claimed ticket; expected 400 `INVALID_REPORT_REQUEST_ID`, and the ticket's
     `report_ref` still absent on a re-read;
   - **arm 2:** ONE POST to the package door as the filer with a syntactically complete synthetic body; expected 403, and the
     ticket's `package` still absent on a re-read.
   Then cleanup: both tickets completed; the row deleted after `exp` and read back ABSENT; the zero-call read at `exp` + 300 s.
4. After the process exits the executor reads and records: the return code; both arms as served (status and code); the two
   re-reads; the trace's `mode` and `submission` fields (`ARMS_ONLY`, `NOT_SENT`); what was left under `49financial` by id (one
   upload, two completed tickets); every `WE_DL_*` and `WE_CLIENT_*` line for the run's tickets as tokens and counts; its own
   ConsistentRead of the row ABSENT; **and that the trace's hop list holds NO entry for hops (d), (e), (g) and no recording
   half of (f)**. That, the `NOT_SENT` field and the test `test_arms_only_sends_no_submission` are the evidence that no request
   went down the generation path. An invocation count of `irpt-ycharts-generate` is NOT that evidence: in run 4 this seat
   counted 3 invocations of it at 11:18:43Z-11:18:54Z, BEFORE the 11:19:00Z submission, so the upload hop calls that function too.

## 4. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-users-v2` row `USER#tckt-fwd1-testfiler-20261009@opal.invalid` | created; deleted after `exp` | delete + ConsistentRead ABSENT; never before `exp` |
| `opal-tickets`: ONE journey ticket and the census's one ticket (49financial) | created, claimed, completed. `report_ref` and `package` are NOT set: both arms are refusals | completed in cleanup; never deleted |
| IRPT, firm `49financial`: ONE upload | created | none: an upload record is immutable by design; listed by id. **No analysis request is created** |
| the vendor (YCharts) and the generation queue | **NOTHING**: no submission is sent. The upload hop does invoke `irpt-ycharts-generate` (as in every earlier run); it queues no generation | the trace read of step 4 |
| mail | CREATE logs `WE_DL_UNCONFIGURED` while the map is empty; CLAIM attempts one client notice to the filer's `.invalid` address | read after the run; `WE_DL_SENT` with the map read empty is a BLOCKING row |
| data-refresh | in the radius; expected zero calls | the zero-call read |
| every other firm | nothing: the census proves one firm before any hop | STOP + cleanup |

No IAM, code, route or Terraform change. No `kms:Decrypt` grant. No identity but the filer's.

## 5. Branches (all signed)

- **A.** Both arms answer as expected (400 with the code; 403), both re-reads absent, return code 0, the row ABSENT. The two
  refusals are EXERCISED LIVE for the first time.
- **B.** Arm 1 answers anything else. A RESULT: the served status and code recorded, a BLOCKING row; arm 2 still runs (the runner's
  coded choice); return code 1 after cleanup.
- **C.** Arm 2 answers 2xx (`PACKAGE_DOOR_ADMITTED_THE_FILER`): a BLOCKING and ARMED row at once, reported to the CTO before
  anything else; the executor records the ticket's `package` as stored and does not try to remove it. Any other non-403 answer is
  a RESULT recorded as served.
- **D.** Any STOP in steps 0-2, or the runner's own precheck or census stop. Nothing of the journey runs; the row, if written, is
  deleted after `exp`.
- **E.** The trace holds a hop (d) entry, or `submission` reads anything but `NOT_SENT`: a BLOCKING row; the run is reported as
  having broken its own bound, and the request id, if one was issued, goes to the CTO at once.

ONE run. No retry. The package route's five coded 409s are NOT exercised by this run and are not claimed.

## 6. What must hold before a run order cites this pair

1. `R4-pk-2`'s apply has reported and its ledger entry is closed.
2. The CTO half matches this text.
3. This seat re-reads `irpt-status`, `opal-ticket-api`, the precheck and the filer row at the GO and writes the values in the order.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 4 and branches A-E, on the conditions of section 6.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
