<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-R4-tr1.fwd1-fifth-run-one-step-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>4</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R4.md</decomp_doc> (round 4): cell `R4-tr-1`, the fifth run of the FWD-1 journey.
<owned_cells>R4-tr-1</owned_cells>
</decomp_ref>

  <objective>
    Run the FWD-1 journey ONCE on DEV as the synthetic one-firm filer, in the runner's ONE-STEP mode: upload; create the ticket
    (source `ticketcenter:i1`, NEVER claimed); the two refusal arms; **ONE analysis submission** naming the ticket; record the
    issued id on the ticket as its creator; read the finished report; open it from the ticket. **That one submission makes the
    resident host attempt ONE vendor sign-in. It is the first since release st32 and it is also the diagnostic. EXACTLY ONE
    request is sent, whatever happens. If the sign-in fails, nobody sends a second: not you, not as a retry, not to "confirm".**
  </objective>

  <context>
    Both halves are SIGNED. Read both, in full, before any AWS call:
    - pair and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R4_RUN/R4_TR1_FIFTH_RUN_PAIR.md` @03de25b030
      (sections 3 to 6: what "the form's one-step path" means here, the act, the blast radius, every branch);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R4_TR1_FIFTH_RUN_CTO_HALF.md` @f439ec72a8
      (at most ONE sign-in per job, read in the host's code; S-FAIL is final for the day; the run starts only with the generation
      queue at 0 and 0).
    The pair's section 7 reads TRUE, and the order records how:
    - condition 1: the runner's one-step mode is merged @066017d5fb, committed blob sha256
      `645376771ede5590a578ee74e60408383d73ab45da076d6d353fd550adbbb94e`, 68 tests; the issuer read its submission code: ONE call
      through `one_step_submit`, a counter that refuses a second, no retry in `call`;
    - condition 2: the CTO half above;
    - condition 3, `2.0.0_SA_COO~G2`'s reads at the GO: the generation queue `irpt-generation` read visible 0, not
      visible 0, delayed 0 at 16:45:39Z (msg 5383); the host at 16:49:27Z runs root `0485393f3a-st32`, active, restarts 0, started
      16:09:55Z, with 0 capture, eviction or session-refresh lines since that start and 0 children (msg 5391, read by that seat
      from `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j4/SIGNIN_BASELINE_BEFORE_FIFTH_RUN_20261011.txt`). So
      this run's sign-in is the first since st32. Its SECOND queue read is your step 3;
    - condition 4, the issuer's re-reads at 16:45Z: `irpt-status` CodeSha256 `6idtFvAm...` (11:26:53Z); `opal-ticket-api`
      `d2w1YJ8A...` (15:18:51Z); `clamp_precheck.py` `READ27 27/27`; `TICKET_DL_MAP` an empty map (its value is 2 characters);
      `PACKAGE_ALLOWED_FIRMS` length 0; the filer row ABSENT; portal `origin/DEV` `c3a03c246a`, the form file unchanged since the
      pair's read; 0 entries open in the shared tree's `.open_deploys/` naming any of the pair's functions.
    WHAT IS NEW SINCE RUN 4, so you do not run it from memory: there is NO claim; the row is still left two hours after an
    accepted submission (return code 3, then `--finish-cleanup`); the arms run BEFORE the submission; there is a HOLD POINT on
    another seat's queue read (step 3); and the host-side reads after the run are NOT yours.
    Read `/cloud-ops` first. The signing key is read into memory only and reported after the fact through `0.0.0_AB_MSTR~DELL2`. NO
    client data in any tracked file: statuses, codes, ids, counts, byte lengths and hash prefixes only.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO under the pair as signed. In order:

    0. LEDGER FIRST. Open the NEVER-2 entry with a window of at least 3 hours. Read EVERY live worktree's `.open_deploys/`, union
       them, print the per-tree denominator. An open entry naming `irpt-status`, `opal-ticket-api`, `irpt-ycharts-generate`,
       `irpt-export-render` or the resident, other than your own, is a STOP.
    1. PIN. `git show HEAD:org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py | sha256sum`
       reads `645376771ede5590a578ee74e60408383d73ab45da076d6d353fd550adbbb94e`, and the working file hashes the same; else STOP.
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R4_CHECKS/r4_checks.py os-mode` and `... os-regress`
       both print OK.
    2. PRECHECKS, before anything is written, each printed (create `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_tr1/` first):
       - `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_tr1/clamp_precheck_table.json`
         reads `READ27 27/27`; anything else is a STOP;
       - `irpt-status` live CodeSha256 starts with `6idtFvAm`; `opal-ticket-api` starts with `d2w1YJ8A`. A different value is a
         STOP: report it, the issuer re-reads and re-issues; do not substitute a prefix yourself;
       - `TICKET_DL_MAP`: key count, and for `49financial` the recipient COUNT and DOMAINS only. Empty or Opal-only: PROCEED;
       - the filer row reads ABSENT by ConsistentRead.
    3. **HOLD POINT. Before the row is written and before the runner is invoked**, message `2.0.0_SA_COO~G2` with the subject
       `prechecks done, TCKT_VNEXT fifth run` and WAIT. That seat reads the generation queue and answers with a time and three
       counts. PROCEED only on an answer showing visible 0 and not visible 0. **Any other count, or no answer within 15 minutes
       of your message, is a STOP (branch D): nothing is written, close the ledger as not executed, report to the issuer.**
       Record the answer's message id, time and counts in your ledger entry.
    4. THE RUN. Start within 3 minutes of that answer. ONE invocation, from the repo root:
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py --one-step --read27 "<the READ27 line>"
        --exp-minutes 30 --expect-irpt-status-sha 6idtFvAm --run-label R4-tr-1-run5
        --pair "R4_TR1_FIFTH_RUN_PAIR.md@03de25b030 + CTO half@f439ec72a8"
        --executor 0.7.0_AE_CloudOps~TV2
        --trace-out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_tr1/r4_tr1_run5_trace.json`
       **Run it ONCE. Never re-invoke it for any reason: a crash, a non-zero return code, a hung terminal, a doubt. A second
       invocation is a second request.** If the process dies before it writes a trace, report at once and do nothing else. It runs
       to about `exp` + 6 minutes; do NOT interrupt it. Return codes: 3 = a submission was accepted or possibly accepted, the row
       is LEFT IN PLACE; 0 = no submission was accepted, the row removed; 1 = stopped before the submission, or a failure;
       2 = a bad argument or the trace path exists.
    5. AFTER THE PROCESS EXITS, read and record:
       - (a) the return code and the last 40 output lines;
       - (b) from the trace: `mode` (`ONE_STEP`), `submission` and `submission_calls` (must read `SENT_ONCE` and 1, or `NOT_SENT`
         and 0); hop (b)'s `source`; that hop (c) reads not run; both arms as served (status, code, the two re-reads); hop (d)'s
         `http_status`, `status_state`, `status_public_reason_code`, key lists, `request_id`, and `settled_by_list` if present;
         `record_calls.first` and `.repeat`; hop (e) and `job_last_read`; hop (g); the zero-call block; the cleanup block;
       - (c) what the run left under `49financial`, by id: the upload id, the `REQ-` id, the report id if one was made, the two
         ticket ids, named as immutable test artifacts in a client firm's store;
       - (d) every `WE_DL_*` and `WE_CLIENT_*` line `/aws/lambda/opal-ticket-api` logged for the run's ticket ids, as tokens and
         counts. A `WE_DL_SENT` with the map read empty, or any `WE_CLIENT_*` send, is a BLOCKING row at once;
       - (e) your own ConsistentRead of the filer row: PRESENT on return code 3, ABSENT on 0 or 1. Say which and why.
    6. REPORT NOW, once, to `2.0.0_SA_COO~V2`, and send the SAME first line (the request id and its submit time, or "no request
       was sent") to `2.0.0_SA_COO~G2`, whose applier makes the host-side reads: the branch (A to F of the pair, and S-PASS or
       S-FAIL only if hop (e) tells you: a READY report is S-PASS; NOT-READY at the bound is "not known from here"), the items of
       step 5, the trace path, and on return code 3 the `row_delete_not_before` time in UTC.
       **You do NOT read the host's journal or its sign-in receipt, and you quote nothing from either.**
    7. THE SECOND STEP, only on return code 3, no earlier than `row_delete_not_before`:
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py --finish-cleanup org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_tr1/r4_tr1_run5_trace.json --executor 0.7.0_AE_CloudOps~TV2`
       (this step sends NO request and mints no token). Then your own ConsistentRead: ABSENT. Close the ledger only after it.
    8. CLOSE THE ORDER: write the proof-of-spec instance in your deliverables folder ROOT (AC1 `PASS-by-output` on the precheck
       line; AC2 `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming `3.0.0_SA_CVO`; never PASS or FAIL on AC2), validate
       it with `python .tools/proof-of-spec-check.py <instance> AC1,AC2`, flip this order to `complete`, write your session log,
       and send ONE short second report. `complete` means the act is finished, not that FWD-1 is realized.
  </go>

  <bounds>
    ONE run, ONE submission. Not covered: a second invocation, a second token, a token past 30 minutes, any firm but
    `49financial`, a claim, any S3 delete, any queue operation (no receive, no purge, no redrive), any read of the resident host,
    the parked crawl (cell R2-cw-1), any runner but the pinned one. No IAM, code, route or Terraform change. No `kms:Decrypt`
    grant. A surprise is ONE row in `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md`
    (`TCKT_VNEXT-D2-S<k>`, the next free id; binary append, line endings kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R4-tr-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_tr1/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="R4-tr-1" judgment="true"/>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` (the issuer's live run, 16:45Z, writing to a scratch path). AC2 (judgment, graded by the CVO at
L9 on the trace and the host-side reads): FWD-1's ACCEPT, "the report is made from the filed file, and the finished report opens
from the same ticket", shown by the finished report read for the id the service issued and the ticket holds; one firm only. Stated
with it, by both halves: the runner made the form's four calls and the form's own code was not executed; the YCharts producer.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one run, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the users-table write, the key read and the logs reads sit under the pair).
comp-adversary: RUN -- the runner's census is the adversarial arm (27 routes, another firm refused on each); the malformed-id arm and the package-door arm run before the submission.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R4-tr-1) under a signed never-widen pair; not a worker cell.
</task_order>
