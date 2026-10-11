<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j5.fifth-run-host-reads-journal-and-receipt-shape-dell2</id>
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
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance
comp-adversary: RUN -- the script's receipt check was run locally on 3 inputs (a clean receipt, one with 4 planted values, an absent file): 0 of 4 planted values printed, the absent case says so; bash -n clean. Read host_capture.py for where the receipt is kept (RECEIPT_NAME beside the wrapper, lines 65 and 301). NOT seen: a real receipt, so its field names are unknown and are what this read returns; the check's patterns are mine and a value they miss would be shown only as a length and a hash, never as text, unless it is a closed upper-case token. The trap is quoting the receipt: nothing in it is quoted by you or by me beyond the script's own lines
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R14.md</decomp_doc>
<owned_cells>YCD-c-14</owned_cells>
<decomp_context>The first exercise of st32: TCKT_VNEXT's fifth run submitted REQ-86a5a08295b65e12749968f9 for the YCharts path at 2026-10-11T17:09:43Z (0.7.0_AE_CloudOps~TV2 msg 5492) and no report came by 17:29:36Z. Its pair (R4_TR1_FIFTH_RUN_PAIR.md step 5) makes the host-side reads this seat's to order: the journal's named lines for the request, and the SHAPE of the sign-in receipt after a check for a posted value, a cookie and a tokenised URL (CTO half of st32, condition 2). It also tells this seat whether the host is quiet, which the held order TO-APPLY-x1dry waits on.</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only script on host i-0167fd745ad906a66: what the resident did with request REQ-86a5a08295b65e12749968f9, and the
    shape of the sign-in receipt it kept, with nothing of the receipt quoted but field names, closed tokens, booleans,
    integers, lengths and hash prefixes.
  </objective>

  <the_act>
    1. host_read.py with org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r14/fifth_run_host_reads.sh. It reads
       the unit's journal since 2026-10-11 17:05:00 UTC, the capture files' names and sizes, and the receipt's shape. It
       writes one temp file under /tmp and removes it. It prints, among others: ROOT, ACTIVE, WINDOW, REQ_LINES and the REQ
       lines, the NAMED lines, SIGNIN_LINES, CHILDREN, QUEUE, the FILE lines, RECEIPT, the two CHECK lines, LEAVES and the
       LEAF lines, END.
    2. BEFORE you save or send anything: read the output yourself. If any REQ, NAMED or SIGNIN line names a person, a client
       or a security, replace that line with `REDACTED <timestamp>`. If the `CHECK VERDICT` line says FOUND, that is a
       finding to report as the four counts; the flagged leaves are already shown as a length and a hash. Do NOT open,
       print, copy or download the receipt or the stderr file yourself by any other command.
    3. Save the output as FIFTH_RUN_HOST_READS_20261011.txt in your deliverables folder irpt_ycdgen_j5/, with the SSM command
       id and the instance id on its first line. Message 2.0.0_SA_COO~G2 the path and these lines: ROOT, ACTIVE, REQ_LINES,
       SIGNIN_LINES, CHILDREN, QUEUE, RECEIPT, both CHECK lines.
    No write to the host beyond the script's own temp file, no restart, no install, no queue receive, no table read, no
    second request, no retry of anything.
  </the_act>

  <bounds>ONE instance, read-only. Nothing of the receipt leaves the host but what the script prints. No IAM, no secret read, no queue receive, no table read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j5/IRPT_YCDGEN.TO-APPLY-j5.fifth-run-host-reads-journal-and-receipt-shape-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-c-14">The read states how many journal lines name the request.<invocation>grep -c -E '^REQ_LINES=[0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j5/FIFTH_RUN_HOST_READS_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-c-14">The read states the receipt's presence or absence.<invocation>grep -c -E '^RECEIPT (present|ABSENT|not JSON)' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j5/FIFTH_RUN_HOST_READS_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-c-14">The read ran to its end.<invocation>grep -c '^END$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j5/FIFTH_RUN_HOST_READS_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
