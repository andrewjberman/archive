<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-b8.resident-host-brand-listing-dell2</id>
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
comp-adversary: RUN -- a listing that changes nothing: no write, no restart, no file read beyond names, sizes and sha256 of the brand directory's own files; the trap is listing the wrong root, so the root is READ from the unit's ExecStart and printed, never typed
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R8.md</decomp_doc>
<owned_cells>YCD-d-8</owned_cells>
<decomp_context>Row IRPT_YCDGEN-D2-S3: one listing of the resident host's brand spec and logo (CTO round-8 analysis @fe73849335 section 2).</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only listing on the resident host i-0167fd745ad906a66: which package root the service runs, and which brand files
    that root carries under ycharts/research/brand/, each with its size and sha256.
  </objective>

  <the_act>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~G2, 2026-10-11): AC2's expect admitted a bare integer, which the proof gate refuses as thin
    (your row on TO-APPLY-b8 AC2). AC2 now reads the first line that is either a BRAND line with its sha256 or the
    BRAND-DIR-ABSENT line. The act and the bounds are unchanged.
    1. One SSM send-command (AWS-RunShellScript) on i-0167fd745ad906a66 that only READS:
       - print the resident unit's ExecStart line, and from it the running package root, as a line `ROOT=<path>`;
       - `ls -l <root>/ycharts/research/brand/`;
       - `sha256sum <root>/ycharts/research/brand/*`, each printed as a line `BRAND <sha256> <file name>`.
       If the brand directory does not exist under that root, print `BRAND-DIR-ABSENT <path>` and stop: that is the finding.
    2. Save the command's full output as BRAND_LISTING_HOST.txt in your deliverables folder irpt_ycdgen_b8/, with the SSM
       command id and the instance id on its first line.
    3. Message 2.0.0_SA_COO~G2 the file path. No write, no restart, no install, no other host and no other directory.
  </the_act>

  <bounds>ONE instance, ONE read-only command. No write to the host, no service restart, no IAM, no secret read, no file content beyond names, sizes and sha256.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_b8/IRPT_YCDGEN.TO-APPLY-b8.resident-host-brand-listing-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-8">The listing names the running root.<invocation>grep -m1 '^ROOT=' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_b8/BRAND_LISTING_HOST.txt</invocation><expect>^ROOT=/</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-8">The listing states the brand directory's files or its absence.<invocation>grep -m1 -E '^(BRAND [0-9a-f]{64} |BRAND-DIR-ABSENT )' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_b8/BRAND_LISTING_HOST.txt</invocation><expect>^(BRAND [0-9a-f]{64} |BRAND-DIR-ABSENT )</expect></criterion>
  </proof_of_spec>
</task_order>
