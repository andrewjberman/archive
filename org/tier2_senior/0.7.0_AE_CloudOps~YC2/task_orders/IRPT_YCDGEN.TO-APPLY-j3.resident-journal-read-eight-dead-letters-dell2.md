<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j3.resident-journal-read-eight-dead-letters-dell2</id>
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
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance, the grant TO-APPLY-j1 used
comp-adversary: RUN -- read 1 prior output of the same form (irpt_ycdgen_j1/RUN4_JOURNAL_20261011.txt, 22 lines by wc, 0 redacted) and the 8 request ids and send times of the laptop's inventory @f2053cfdd8; NOT seen: how far back the host journal reaches, which is why the read prints its oldest line first and why a short journal is a finding and not a failure. A read that changes nothing: no write, no restart, no receive on any queue, no table read. The trap is a line that carries a client's or a security's name: only the worker's own named lines and the CLASS of an exception are printed
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R13.md</decomp_doc>
<owned_cells>YCD-a-13</owned_cells>
<decomp_context>The reconciliation packet for the eight dead-lettered generation jobs (CTO round-13 analysis @7fa981f907 section 3 item 1). A job record holds no reason, so the cause of each failure, if it is anywhere, is in the host journal of 2026-10-07 to 2026-10-09. This read looks for it.</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only command on the resident host i-0167fd745ad906a66: what the resident journal holds, from 2026-10-07 18:00 UTC
    to 2026-10-09 17:00 UTC, for eight request ids, as the worker's own named lines and exception classes only.
  </objective>

  <the_act>
    The eight ids: REQ-ef7b39c548d08cbb4822f7cc REQ-8966d24ffefa1c28269ef26c REQ-1f8b4cc4682f2d929cc70215
    REQ-3d76e5b49dae4f91db1694b0 REQ-9d59d4d2334f841152914569 REQ-f7ddede91f98562412314b6e REQ-448d42480cadd873fa74c3cf
    REQ-4b5155ac2ea9467ab771b414
    1. One SSM send-command (AWS-RunShellScript) on i-0167fd745ad906a66 that only READS the journal of
       irpt-analysis-resident.service and prints, in this order:
       - `OLDEST <timestamp of the first line the journal holds for the unit>`: if it is later than 2026-10-07 18:00 UTC the
         window is only partly covered, and the read says so with `COVERAGE PARTIAL from <that timestamp>`; else `COVERAGE FULL`;
       - `WINDOW lines=<journal lines in the window> tracebacks=<count of Traceback in the window>`;
       - for each of the eight ids, `ID <id> lines=<count of journal lines in the window that contain it>`, then each such
         line cut to its first 400 characters, prefixed `REQ `;
       - every journal line in the window that contains `retained_for_retry`, cut to 300 characters, prefixed `RETAINED `
         (these lines carry a class and a closed code and no request id; the issuer matches them to an id by time);
       - for each traceback in the window, ONE line `TRACE <timestamp> <ExceptionClass>`: the timestamp of its last line
         and the token before the first colon of that last line. Never the text after the colon, never the body;
       - `END`.
    2. Save the command's full output as DEAD_LETTER_JOURNAL_20261011.txt in your deliverables folder irpt_ycdgen_j3/, with
       the SSM command id and the instance id on its first line. If the output is larger than SSM returns in one answer,
       have the command write nothing on the host: split the read into two sends by date and say so on the first line.
    3. Message 2.0.0_SA_COO~G2 the file path. No write, no restart, no install, no queue receive, no table read, no other
       host. If a line you are about to save names a person, a client or a security, replace that line with
       `REDACTED <timestamp>` and say so in your message.
  </the_act>

  <bounds>ONE instance, read-only journal commands only. No write to the host, no service restart, no IAM, no secret read, no queue or table read. The worker's own named lines and exception class tokens only.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j3/IRPT_YCDGEN.TO-APPLY-j3.resident-journal-read-eight-dead-letters-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-a-13">The read states how far back the journal reaches.<invocation>grep -m1 -E '^COVERAGE (FULL|PARTIAL from )' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j3/DEAD_LETTER_JOURNAL_20261011.txt</invocation><expect>^COVERAGE (FULL$|PARTIAL from [0-9])</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-a-13">Each of the eight ids has its count line.<invocation>grep -c -E '^ID REQ-[0-9a-f]{24} lines=[0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j3/DEAD_LETTER_JOURNAL_20261011.txt</invocation><expect>^8$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-a-13">The read ran to its end.<invocation>grep -c '^END$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j3/DEAD_LETTER_JOURNAL_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
