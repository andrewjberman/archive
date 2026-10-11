<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j6.fifth-run-receipt-named-leaves-dell2</id>
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
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance
comp-adversary: RUN -- the script was run locally on 1 synthetic receipt with 2 planted values (a cookie pair and a tokenised URL) placed in asked leaves: 0 of 2 printed, both shown as WITHHELD with a length and a hash; bash -n clean. Read j5's output for the leaf paths (120 leaves). NOT seen: the real values, which is what this read returns. The trap is a leaf whose value is not the closed word the receipt's whitelist promises: the script prints a value only if it is a boolean, a number or one short word of letters, digits, underscore, dot, colon and hyphen
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R14.md</decomp_doc>
<owned_cells>YCD-c-14</owned_cells>
<decomp_context>The fifth run's diagnosis (CTO msg 5525): IRPT_BCKEND's read-only cell IB141-1 names the receipt leaves that confirm or kill "a web firewall challenge" (2.0.0_SA_COO~P2 msg 5551); this seat reads them out. The receipt is the file j5 already read by shape; no new run.</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only script on host i-0167fd745ad906a66 that prints the named leaves of /opt/investor-reporting-ycharts/last-capture.receipt.json
    as closed words, booleans and numbers, and withholds anything else.
  </objective>

  <the_act>
    1. host_read.py with org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r14/fifth_run_receipt_named_leaves.sh.
       It writes nothing. It prints AT, RECEIPT (bytes and hash, to compare with j5's 3824 and c1157ec45071b41e), the ASK
       lines, STEPS, SHOWN and WITHHELD, END.
    2. Read the output before you save or send it. If the RECEIPT line's hash is not j5's, say so first: a different file is
       a different capture. If any ASK line shows something that is not a closed word, a cookie NAME, a boolean or a number,
       replace that line's value with REDACTED and say so. Do not open the receipt by any other command.
    3. Save the output as FIFTH_RUN_RECEIPT_NAMED_LEAVES_20261011.txt in your deliverables folder irpt_ycdgen_j6/, with the SSM
       command id and the instance id on its first line. Message 2.0.0_SA_COO~G2 the path and the ASK 1 to ASK 6 lines.
    No write, no restart, no install, no queue receive, no table read, no request, no sign-in.
  </the_act>

  <bounds>ONE instance, read-only. Nothing of the receipt leaves the host but what the script prints. No IAM, no secret read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j6/IRPT_YCDGEN.TO-APPLY-j6.fifth-run-receipt-named-leaves-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-c-14">The first asked leaf is answered.<invocation>grep -c '^ASK 1 | probe_pair.without_token_waf_action_class | ' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j6/FIFTH_RUN_RECEIPT_NAMED_LEAVES_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-c-14">The read states how many values it showed and withheld.<invocation>grep -c -E '^SHOWN=[0-9]+ WITHHELD=[0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j6/FIFTH_RUN_RECEIPT_NAMED_LEAVES_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-c-14">The read ran to its end.<invocation>grep -c '^END$' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j6/FIFTH_RUN_RECEIPT_NAMED_LEAVES_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
