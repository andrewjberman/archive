<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-x1dry.st32-rollback-library-step-dry-exercise-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one command on the resident host; no schedule, trigger or rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the command runs under the applier's existing SSM grant on this one instance
comp-adversary: RUN -- read the 3 library lines of st32_release/remove_st32_to_st31.sh and the script r14/dry_exercise_rollback_library.sh, which passes bash -n; denominator: 2 host files are READ (the library and its kept copy), 0 are written; every write is inside one new mktemp directory that the script removes. NOT seen: the script on the host. The trap is H pointing at the real directory: H is assigned only from mktemp, and the script prints the real library's sha256 before and after so a touched library is visible in its own output
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R14.md</decomp_doc>
<owned_cells>YCD-c-14</owned_cells>
<decomp_context>The round-14 analysis @c4354a9873 section 3 item 3: st32's rollback has a library step that has never run; one dry exercise of it on a copy, off the unit, so the first real rollback is not also its first run.</decomp_context>
</decomp_ref>

  <objective>
    Run ONE script on host i-0167fd745ad906a66 that exercises the st32 rollback's library step on COPIES in a temp directory,
    with a negative control, and shows the real library, its kept copy and the unit untouched.
  </objective>

  <context>Load /cloud-ops first. NOT URGENT, and it must NOT run while another seat's run is in flight on this host: if
  TCKT_VNEXT's fifth run is between its submission and its close, wait for the close. The script touches no unit, no
  resident root and no real library file. It is not the rollback: remove_st32_to_st31.sh is not run by this order.</context>

  <the_act>
    1. Confirm the generation queue reads 0 visible and 0 in flight (get-queue-attributes, no receive). If not, wait.
    2. host_read.py with org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r14/dry_exercise_rollback_library.sh.
       Expect: `X1 DRY RESULT: PASS`, `X2 NEGATIVE CONTROL: PASS`, `X3 temp dir removed: yes`, the real library after equal
       to a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841, the kept copy equal to
       857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839, the unit active with the same restart count before
       and after and root 0485393f3a-st32.
    3. Save the output as X1_DRY_EXERCISE_20261011.txt in your deliverables folder irpt_ycdgen_x1dry/, with the SSM command id
       and the instance id on its first line. Message 2.0.0_SA_COO~G2 the path.
    Any FAIL line, a real library hash that changed, or a restart count that changed: STOP, change nothing further, and
    report the output as it is.
  </the_act>

  <bounds>ONE instance. Reads of two files under /opt/investor-reporting-ycharts and of the unit's state; writes ONLY inside
  one new directory under /tmp, removed by the script. No restart, no install, no rollback, no IAM, no secret, no queue
  receive, no table read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_x1dry/IRPT_YCDGEN.TO-APPLY-x1dry.st32-rollback-library-step-dry-exercise-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-c-14">The library step passed on the copy.<invocation>grep -c '^X1 DRY RESULT: PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_x1dry/X1_DRY_EXERCISE_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-c-14">The negative control refused a wrong kept copy.<invocation>grep -c '^X2 NEGATIVE CONTROL: PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_x1dry/X1_DRY_EXERCISE_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-c-14">The real library is st32's after the exercise.<invocation>grep -c '^X3 real library after: a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_x1dry/X1_DRY_EXERCISE_20261011.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
