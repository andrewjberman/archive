<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j1.resident-journal-read-run4-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one read-only command on the resident host; no schedule, trigger or rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance, the grant TO-APPLY-b8 and TO-APPLY-st30 used
comp-adversary: RUN -- read 1 file (resident_worker.py of the installed package, 25 lines matching its print sites of the forms IRPT_RESIDENT_, WARN:, ERROR: and named_line, counted by grep); NOT seen: the host journal itself, so what an unnamed line or a traceback body carries is unknown and is why neither is printed. A journal read that changes nothing: no write, no restart, no receive on any queue, no table read. The trap is a journal line that carries a client's or a security's name: the command prints only the worker's own named lines and the CLASS of an exception, never an exception's message or a traceback body
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R11.md</decomp_doc>
<owned_cells>YCD-d-11</owned_cells>
<decomp_context>The first exercise of the resident release st30: TCKT_VNEXT's fourth run (2.0.0_SA_COO~V2 msg 4851) submitted REQ-59aa6803901f371b27ffa176 for 49financial at 2026-10-11T11:19:00Z and no report came in 20 minutes. This read says what the resident did with it. It is the after-read of st30's S2 and S5 (st30_release/NEVER_WIDEN_PACKET_ST30.md section 2).</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only command on the resident host i-0167fd745ad906a66: what the resident journal holds for request
    REQ-59aa6803901f371b27ffa176 since 2026-10-11T11:15:00Z, as the worker's own named lines and exception classes only.
  </objective>

  <the_act>
    1. One SSM send-command (AWS-RunShellScript) on i-0167fd745ad906a66 that only READS the journal of
       irpt-analysis-resident.service since "2026-10-11 11:15:00" UTC and prints, in this order:
       - `ROOT=<the running package root, read from the unit's ExecStart>` and `ACTIVE=<is-active> RESTARTS=<NRestarts>`;
       - `WINDOW lines=<total journal lines in the window> polls=<count of IRPT_RESIDENT_POLL> handled=<count of IRPT_RESIDENT_POLL lines whose handled is not 0> tracebacks=<count of Traceback>`;
       - every journal line that contains `REQ-59aa6803901f371b27ffa176`, each cut to its first 400 characters, prefixed `REQ `;
       - every journal line that starts (after the journal's own prefix) with `IRPT_RESIDENT_`, `WARN:` or `ERROR:` and is
         NOT an `IRPT_RESIDENT_POLL handled=0` line, each cut to 400 characters, prefixed `NAMED `;
       - for each traceback in the window, ONE line `TRACE <timestamp> <ExceptionClass>`: the timestamp of its last line and
         the token before the first colon of that last line. Never the text after the colon, never the traceback's body;
       - `UNSET=<count of ANALYSIS_READY_QUEUE_UNSET>` and `SENDFAIL=<count of ANALYSIS_READY_SEND_FAILED>`;
       - `END`.
    2. Save the command's full output as RUN4_JOURNAL_20261011.txt in your deliverables folder irpt_ycdgen_j1/, with the SSM
       command id and the instance id on its first line.
    3. Message 2.0.0_SA_COO~G2 the file path. No write, no restart, no install, no queue receive, no table read, no other
       host. If a line you are about to save names a person, a client or a security, replace that line with
       `REDACTED <timestamp>` and say so in your message.
  </the_act>

  <bounds>ONE instance, ONE read-only command. No write to the host, no service restart, no IAM, no secret read, no queue or table read. Journal lines of the worker's own named form and exception class tokens only.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j1/IRPT_YCDGEN.TO-APPLY-j1.resident-journal-read-run4-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-11">The read names the running root.<invocation>grep -m1 '^ROOT=' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j1/RUN4_JOURNAL_20261011.txt</invocation><expect>^ROOT=/opt/irpt-resident/</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-11">The read states the window's counts.<invocation>grep -m1 '^WINDOW lines=' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j1/RUN4_JOURNAL_20261011.txt</invocation><expect>^WINDOW lines=[0-9]+ polls=[0-9]+ handled=[0-9]+ tracebacks=[0-9]+</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-d-11">The read ran to its end.<invocation>grep -c '^END$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j1/RUN4_JOURNAL_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
