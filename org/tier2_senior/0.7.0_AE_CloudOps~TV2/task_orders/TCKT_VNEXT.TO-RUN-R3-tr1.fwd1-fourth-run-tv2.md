<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-R3-tr1.fwd1-fourth-run-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>3</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R3.md</decomp_doc> (round 3): cell `R3-tr-1`, the fourth run of the FWD-1 journey.
<owned_cells>R3-tr-1</owned_cells>
</decomp_ref>

  <objective>
    Run the FWD-1 journey ONCE, end to end, on DEV, as the synthetic one-firm filer, with the runner at `83b4f0c597`: upload, file
    the Analysis Request ticket, claim, submit the analysis (ONE synthetic request down the YCharts producer path), read the FINISHED
    REPORT for the id the service issues, record that id on the ticket, open the report from the ticket. Then finish the cleanup in
    TWO steps: the row is deleted two hours after an accepted submission. One run, one token, firm `49financial` only.
  </objective>

  <context>
    Both halves are SIGNED. Read both, in full, before any AWS call:
    - pair and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R3_RUN/R3_TR1_FOURTH_RUN_PAIR.md` @213c8eae94
      (steps 0-8, the blast radius, branches A-F);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R3_TR1_FOURTH_RUN_CTO_HALF.md` @3b30b56702
      (two conditions of its own: the trace keeps the submission answer's state and key lists; what the run leaves under
      `49financial` is listed by id and named as immutable test artifacts in a client firm's store).
    The pair's section 6 reads TRUE, and the order records how:
    - condition 1: the resident release st30 is installed, root `37210c771a-st30` since 10:32:22Z, V1 green
      (`org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/D2_V1_INSTALL_20261011.txt`; `2.0.0_SA_COO~G2` msg 4742);
    - condition 2: the dead letters were READ by the laptop's executor (CTO relay msg 4780; record @f2053cfdd8 on CLOUD): 8, all
      sent 2026-10-07 to 10-09, every job RECEIVED, and NO reason is recorded on a job. Run 3's request is not among them. Nothing
      was deleted or redriven, and nothing is by you;
    - condition 3: the CTO half above;
    - condition 4, the issuer's re-reads at 11:04Z: `irpt-status` CodeSha256 `Iw3FADFrSt5G...` (LastModified 10:25:40Z; it MOVED
      since run 3); `opal-ticket-api` `t1EoiJRZ...`; `clamp_precheck.py` `READ27 27/27`; `TICKET_DL_MAP` 0 keys; the filer row ABSENT.
    The runner is NOT the one you ran before. What changed since run 3: it reads an ACCEPTED submission by state and identity (run
    3's answer was an acceptance the old runner called a refusal); after an accepted submission it LEAVES THE ROW IN PLACE and exits
    with return code 3; a second invocation deletes the row two hours later. The precheck is a new script.
    Read `/cloud-ops` first. The signing key is read into memory only and reported after the fact through `0.0.0_AB_MSTR~DELL2`. NO
    client data in any tracked file: statuses, codes, ids, counts, byte lengths and hash prefixes only.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO under the pair as signed. In order:

    0. LEDGER FIRST. Open the NEVER-2 entry with a window of at least 3 hours (it stays OPEN across the two-hour row wait). Read
       EVERY live worktree's `.open_deploys/`, union them, print the per-tree denominator. An open entry naming `irpt-status`,
       `opal-ticket-api`, `irpt-ycharts-generate`, `irpt-export-render` or the resident, other than your own, is a STOP.
    1. PIN. `git show HEAD:org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py | sha256sum`
       reads `8f9e6ec58abeac8e9cd8970479621b819ff6f847ba16cf0e7315a69cf67759d6`, and the working file hashes the same; else STOP.
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R3_CHECKS/r3_checks.py rn-row` and `... rn-regress`
       both print OK.
    2. PRECHECKS, before the row is written, each printed:
       (Create the folder `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/` first; the precheck and the runner write there.)
       - `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/clamp_precheck_table.json`
         reads `READ27 27/27`. Anything else is a STOP (Branch D); report the host line that is not CLAMPED.
       - `irpt-status` live CodeSha256 starts with `Iw3FADFr`. If it reads anything else, STOP and report the value: the issuer
         re-reads and re-issues; do not substitute the prefix yourself.
       - `opal-ticket-api` live CodeSha256 starts with `t1EoiJRZ`; else STOP.
       - `TICKET_DL_MAP`: the key count, and for the row `49financial` resolves to, the recipient COUNT and DOMAINS only. Empty, or
         every domain Opal's own: PROCEED. Any other domain: STOP.
       - the filer row reads ABSENT by ConsistentRead (a row left by an earlier run would make the runner's write fail).
    3. THE RUN. One invocation, from the repo root:
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py --read27 "<the READ27 line>"
        --exp-minutes 30 --expect-irpt-status-sha Iw3FADFr --run-label R3-tr-1-run4
        --pair "R3_TR1_FOURTH_RUN_PAIR.md@213c8eae94 + CTO half@3b30b56702"
        --executor 0.7.0_AE_CloudOps~TV2
        --trace-out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/r3_tr1_run4_trace.json`
       The process runs to about `exp` + 6 minutes (about 36 minutes). Do NOT interrupt it. Its return codes: 0 = complete, the row
       removed and read back absent (no submission was accepted); 3 = complete, a submission was ACCEPTED, the row is LEFT IN PLACE
       and one cleanup step is owed; 1 = a failure; 2 = the trace path already exists. The `--trace-out` file must not exist.
    4. AFTER THE PROCESS EXITS, read and record (the runner does not do these):
       - (a) the return code and the last 30 output lines;
       - (b) from the trace: `result`; each hop; for hop (d) the answer's `http_status`, `status_state`, `status_public_reason_code`
         and its three key lists, and `accepted_state` if it was accepted (CTO condition); both report-route arms; `job_last_read`;
         the zero-call block and its verdict; the cleanup block (`state`, `row_left_in_place`, `row_delete_not_before`);
       - (c) what the run left under `49financial`, by id: the upload id, the request id (the `REQ-` id), the report id if one was
         made, the two ticket ids. Name them in your report as immutable test artifacts in a client firm's store (CTO condition);
       - (d) every `WE_DL_*` and `WE_CLIENT_*` line `/aws/lambda/opal-ticket-api` logged for the run's ticket ids, as tokens and
         counts. A `WE_DL_SENT` with the map read empty is a BLOCKING row at once. The line carries no recipient: infer none;
       - (e) the first refused answer's code exactly as served, and whether it is a public code or an internal string;
       - (f) your own ConsistentRead of the filer row: PRESENT if the return code was 3, ABSENT if it was 0. Say which and why.
    5. REPORT NOW, once, to `2.0.0_SA_COO~V2`: the branch (A to F), the items of step 4, the trace path, and, on return code 3, the
       `row_delete_not_before` time in UTC. Do not wait the two hours to report: the issuer needs the result to compile.
    6. THE SECOND STEP, only on return code 3. No earlier than `row_delete_not_before`:
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py --finish-cleanup org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/r3_tr1_run4_trace.json --executor 0.7.0_AE_CloudOps~TV2`
       It refuses (return code 4, `ROW_DELETE_TOO_EARLY`, seconds remaining) if run early: that is expected, not a failure; run it
       again after the time. Then make your OWN ConsistentRead of the row: ABSENT. Close the ledger only after that read, and send
       ONE short second report with the delete time and the absent read. If you will not be live at that time, say so in the
       first report: the row narrows while it stands, the open ledger entry carries it, and the issuer seats the finish.
    7. On return code 0 (no accepted submission): make your own ConsistentRead of the row, ABSENT, close the ledger, one report.

    BRANCHES (the pair's section 5, all signed): A the report is read from the ticket's id; B the report route refuses the ISSUED
    id (do not roll back anything yourself; report at once); C accepted, and hop (e) ends NOT-READY or on a terminal refusal; D a
    STOP before the journey; E the submission is REFUSED (the refusal state): also read the service's own log line for that minute
    from `/aws/lambda/irpt-ycharts-generate`, tokens only; F the submission's answer is unreadable (the row is left, as in A-C).
    ONE run. No retry, no second submission. No dead letter is received, deleted or redriven by you.
  </go>

<amendment n="1" date="2026-10-11" source="the issuer's own gap: the GO named no closing step">
    Both acts of this order are done (your reports msg 4869 and msg 5007). The order still reads `pending` because the GO never
    told you to close it, which is the issuer's omission. CLOSE IT: write the proof-of-spec instance beside your trace
    (`org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/`), AC1 `PASS-by-output` on the run's own precheck line
    (`READ27 27/27`), AC2 `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming `3.0.0_SA_CVO` (its grade is NOT MET
    @5126c19d7a; do not write PASS or FAIL on it), validate it with `python .tools/proof-of-spec-check.py <instance> AC1,AC2`,
    and flip `<status>` to `complete`. `complete` means the act is finished, not that FWD-1 is realized. No AWS call. One line
    back to `2.0.0_SA_COO~V2` with the commit.
  </amendment>

  <bounds>
    Not covered: a second token, a token past 30 minutes, any firm but `49financial`, any S3 delete, any queue operation, the
    parked crawl (cell R2-cw-1), any runner but the pinned one. No IAM, code, route or Terraform change. No `kms:Decrypt` grant.
    A surprise is ONE row in `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md`
    (`TCKT_VNEXT-D2-S<k>`, the next free id; binary append, CRLF kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R3-tr-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_tr1/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="R3-tr-1" judgment="true"/>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` (the issuer's live run, 11:04Z, writing to a scratch path). AC2 (judgment, graded by the CVO at
L9 on the trace): FWD-1's ACCEPT, "the report is made from the filed file, and the finished report opens from the same ticket",
shown by hop (e) and hop (g) reading the finished report for the id the service issued and the ticket holds; one firm only. The CTO
half notes this run exercises the outcome as served today (the YCharts producer), not the Opal-made report.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one run, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the users-table write, the key read and the logs reads sit under the pair).
comp-adversary: RUN -- the runner's census is the adversarial arm (27 routes, another firm refused on each) and the malformed-id arm runs before the issued id is recorded.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R3-tr-1) under a signed never-widen pair; not a worker cell.
</task_order>
