<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-R2-tr1.fwd1-thread-rerun-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R2.md</decomp_doc> (round 2): cell `R2-tr-1`, the FWD-1 thread re-run.
<owned_cells>R2-tr-1</owned_cells>
</decomp_ref>

  <objective>
    Run the FWD-1 journey ONCE, end to end, on DEV, as the synthetic one-firm filer, with the repaired runner: upload, file the
    Analysis Request ticket, claim, submit the analysis, read the FINISHED REPORT for the id the service issued, record that id on
    the ticket, and open the report from the ticket. Then clean up in the signed order. One run, one token, firm `49financial` only.
  </objective>

  <context>
    Both halves are SIGNED. Read both, in full, before any AWS call. They bound everything you may do:
    - pair and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_TR1_THREAD_RERUN_PAIR.md` @9e9e6e62f3
      (steps 0-10, the blast radius, branches A-D);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R2_TR1_THREAD_RERUN_CTO_HALF.md` @49c17cb50e
      with AMENDMENT 1 @1d7677aa98 (an empty distribution-list map is PROCEED) and AMENDMENT 2 @a65bb46697 (the mail lines are
      read AFTER the run, not between hops; the half covers the runner at 2d2b309be9), six conditions, and the CTO's msg 4164
      (the zero-call verdict rule). Read the half at a65bb46697.
    The runner: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py` at box/dell2 `2d2b309be9`,
    sha256 `10f1abb93c81bb0aa05e9a08f3357e28f24ebc60a7fccbf7edcaf983fa449557`. It is NOT round 1's runner: token expiry, the cleanup
    order, the irpt-status precheck, the report-route arms and the zero-call read are built in. Do not edit it. Do not use
    `sa_r1b_run.py`.
    Refusal table (PROPOSED; this run confirms or corrects it): `deliverables/2.0.0_SA_COO~V2/R2_RUN/REPORT_READ_REFUSALS.md`.
    Read `/cloud-ops` first. The signing key is read into memory only, and that read is reported after the fact through
    `0.0.0_AB_MSTR~DELL2`. NO client data in any tracked file: statuses, codes, ids, counts, byte lengths and hash prefixes only.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO under the pair as signed. In order:

    0. LEDGER FIRST. Open the NEVER-2 entry before anything else. Then read EVERY live worktree's `.open_deploys/`
       (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union
       them and print the per-tree denominator. An open entry naming `irpt-status`, `opal-ticket-api`, `irpt-ycharts-generate` or
       `irpt-export-render` other than your own is a STOP.
    1. PIN. `sha256sum` of the runner reads `10f1abb9...9557`; anything else is a STOP. Run
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_CHECKS/r2_checks.py rn-safety` and `... rn-zero`:
       both print OK.
    2. PRECHECKS, before the row is written (print each read):
       - `opal-ticket-api` live CodeSha256 starts with `W03VREoM` (the runner does not check this one; you do). Else STOP.
       - `irpt-status` live CodeSha256 starts with `6idtFvAm` (the runner checks it too, by `--expect-irpt-status-sha 6idtFvAm`).
       - CTO condition 1: one `get-function-configuration` on `opal-ticket-api`; parse `TICKET_DL_MAP`. Record the key count and,
         for the row `49financial` resolves to (its own key, else `*`), the recipient COUNT and each DOMAIN, never an address. The
         issuer read it at 05:4xZ with 0 keys. Empty, or every domain Opal's own: PROCEED. Any other domain: STOP.
       - `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py` reads `READ27 27/27`.
    3. THE RUN. One invocation, from the repo root:
       `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py --read27 "<the READ27 line>"
        --exp-minutes 45 --expect-irpt-status-sha 6idtFvAm --run-label R2-tr-1
        --pair "R2_TR1_THREAD_RERUN_PAIR.md@9e9e6e62f3 + CTO half@a65bb46697"
        --executor 0.7.0_AE_CloudOps~TV2
        --trace-out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r2_tr1/r2_tr1_trace.json
        --close-ticket TCK-20261009-67ab7f27`
       45 minutes = the census, the journey and hop (e)'s 20-minute bound, plus 5. The runner waits until the token's `exp` has
       passed before it deletes the row, so the process runs about 45 minutes whatever the journey does. DO NOT interrupt it during
       that wait: an interrupt leaves the row in place. If it is interrupted anyway, the row stays until `exp`, then you delete it
       and read it back ABSENT with ConsistentRead, and say so.
       The `--trace-out` file must not exist beforehand (the runner refuses an existing file, rc 2).
    4. AFTER THE RUN, read and record (these are yours; the runner does not do them):
       - (a) the runner's rc and its last 30 output lines;
       - (b) from the trace: each hop's result, both report-route arms, the zero-call block's three numbers per group and its
         verdict, `token_exp`, `row_deleted_at`, the absent read;
       - (c) CTO condition 5: the request id, the report id (if one was made) and the upload id left under `49financial`;
       - (d) CTO condition 3 and AMENDMENT 1: every `WE_DL_*` and `WE_CLIENT_*` line `/aws/lambda/opal-ticket-api` logged for the
         run's ticket ids over `iat`..`exp`, as tokens and counts (no address beyond its domain). A `WE_DL_SENT`, or a
         `WE_CLIENT_SENT` to any address that is not the filer's `.invalid` address, is a BLOCKING row filed at once;
       - (e) the refusal vocabulary: quote the first refused answer's reason code exactly as served, and say whether it is a public
         code (`NOT_FOUND`, `NOT_READY`, ...) or an internal string (`ANALYSIS_REPORT_NOT_READY`, ...);
       - (f) the ConsistentRead of the filer row, ABSENT, run by you after the process exits, independent of the runner's own read.
    5. THE PAGE (pair step 7), only if the run ended branch A. If a browser session can be opened for the filer on the DEV site
       WITHOUT a new credential, open Ticket Center, press Open report on the journey ticket, and record ONLY the canvas colour,
       whether the panel shows report sections or the waiting sentence, and the section count. The token is expired by now, so in
       practice record `PAGE-NOT-RENDERED: token expired before the page step` unless you can do it inside the token's life from a
       second shell while the runner waits. No screenshot enters the repository. PAGE-NOT-RENDERED is a row, not a failure.
    6. Close the ledger only after 4(f) reads ABSENT. Report ONCE to `2.0.0_SA_COO~V2`: the branch (A, B, C or D), the items of
       step 4, the trace path and pin, and the measured push state of your commits.

    BRANCHES (the pair's, all signed):
    - A: every hop met, both arms as expected, hop (g) returns the report.
    - B: the report route answers 400 on the ISSUED id (`BRANCH_B_ISSUED_ID_REFUSED`). Do NOT re-run and do NOT roll anything back
      yourself: report at once; the re-apply of the previous ticket build is routed to the CTO under the R2-rr-2 pair.
    - C: hop (e) ends NOT-READY or on a terminal refusal. That is a RESULT. Record the code; do not re-run, do not widen the read.
    - D: any STOP in steps 0-2, or the runner's own prechecks or census stop. Nothing of the journey runs.
    ONE run. A second run needs a new GO.
  </go>

  <bounds>
    Not covered, by the CTO half: a second token, a token past 60 minutes, any firm but `49financial`, any S3 delete, the parked
    crawl (cell R2-cw-1), the old runner. No IAM, code, route or Terraform change. No `kms:Decrypt` grant. Never
    `aws lambda update-function-code`. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (`TCKT_VNEXT-D2-S<k>`, the next free id;
    append in binary mode, CRLF kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R2-tr-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="R2-tr-1" judgment="true"/>
</proof_of_spec>
AC2 (judgment, graded by the CVO at L9 on the trace): FWD-1's ACCEPT, "the report is made from the filed file, and the finished report
opens from the same ticket", shown by hop (e) and hop (g) reading the finished report for the id the service issued and the ticket
holds; one firm only; the row removed after `exp`.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one run, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the users-table write, the key read and the logs reads sit under the pair; the issuer read describe-log-streams on the data-refresh group as this box's identity, 3 streams returned).
comp-adversary: RUN -- the runner's census is the adversarial arm (27 routes, another firm refused on each) and both report-route arms run before the id is recorded.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R2-tr-1) under a signed never-widen pair; not a worker cell.
</task_order>
