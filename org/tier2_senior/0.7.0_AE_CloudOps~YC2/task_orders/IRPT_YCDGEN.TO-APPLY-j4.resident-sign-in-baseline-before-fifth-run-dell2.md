<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j4.resident-sign-in-baseline-before-fifth-run-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one read-only command on the resident host; no schedule, trigger or rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance, the grant TO-APPLY-j1, j3 and st32 used
comp-adversary: RUN -- read 1 prior output of the same count (irpt_ycdgen_st32/D2_V1_INSTALL_20261011.txt, its NO SIGN-IN line read 0 lines and 0 children at 16:10Z, with a positive control of 5 on the j1 record reported by the applier); NOT seen: the journal since 16:10Z, which is what this read is for. A read that changes nothing: no write, no restart, no receive on any queue, no table read. The trap is a count taken over a window that starts after the unit's own start: the window is the unit's ActiveEnterTimestamp, printed
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R13.md</decomp_doc>
<owned_cells>YCD-d-13</owned_cells>
<decomp_context>The after-read of st32 at the moment before its first sign-in: TCKT_VNEXT's fifth run (pair @03de25b030 and @f439ec72a8) starts only when this host has made no capture since st32 started. 2.0.0_SA_COO~V2 writes this read's three values into the run order (its msg 5381).</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only command on the resident host i-0167fd745ad906a66: the running root, when the unit started, and how many
    journal lines since that start name a capture, an eviction or a session refresh. URGENT: another seat's run order waits
    on it.
  </objective>

  <the_act>
    1. One SSM send-command (AWS-RunShellScript) on i-0167fd745ad906a66 that only READS, and prints in this order:
       - `AT <date -u +%Y-%m-%dT%H:%M:%SZ>`;
       - `ROOT=<the running package root, read from the unit irpt-analysis-resident.service's ExecStart>`;
       - `ACTIVE=<is-active> RESTARTS=<NRestarts> START=<ActiveEnterTimestamp>`;
       - `SIGNIN_LINES=<count of journal lines of the unit since START that match, case-insensitive, capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED>` (the same pattern as st32's V1);
       - `CHILDREN=<count of node or chromium child processes of the unit's MainPID>`;
       - `POLLS_60S=<count of IRPT_RESIDENT_POLL in the last 60 seconds> TRACEBACKS_SINCE_START=<count of Traceback since START>`;
       - `LIBRARY=<sha256 of /opt/investor-reporting-ycharts/ycharts_session.js>`;
       - `END`.
       If SIGNIN_LINES is not 0, also print each matching line cut to 300 characters, prefixed `LINE `, with any line that
       names a person, a client or a security replaced by `REDACTED <timestamp>`.
    2. Save the command's full output as SIGNIN_BASELINE_BEFORE_FIFTH_RUN_20261011.txt in your deliverables folder
       irpt_ycdgen_j4/, with the SSM command id and the instance id on its first line.
    3. Message 2.0.0_SA_COO~G2 the file path AND the seven printed lines, at once. No write, no restart, no install, no queue
       receive, no table read, no other host.
  </the_act>

  <bounds>ONE instance, read-only commands only. No write to the host, no service restart, no IAM, no secret read, no queue or table read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j4/IRPT_YCDGEN.TO-APPLY-j4.resident-sign-in-baseline-before-fifth-run-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-13">The read states the running root.<invocation>grep -m1 '^ROOT=' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j4/SIGNIN_BASELINE_BEFORE_FIFTH_RUN_20261011.txt</invocation><expect>^ROOT=/opt/irpt-resident/[0-9a-z-]+$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-13">The read states the count of sign-in lines since the start.<invocation>grep -c -E '^SIGNIN_LINES=[0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j4/SIGNIN_BASELINE_BEFORE_FIFTH_RUN_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-d-13">The read ran to its end.<invocation>grep -c '^END$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j4/SIGNIN_BASELINE_BEFORE_FIFTH_RUN_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
