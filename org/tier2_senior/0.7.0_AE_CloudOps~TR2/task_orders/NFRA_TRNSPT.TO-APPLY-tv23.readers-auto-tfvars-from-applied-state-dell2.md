<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-tv23.readers-auto-tfvars-from-applied-state-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>LOCAL</risk>
<proof_genre>DEPLOY</proof_genre>
<round>23</round>
<workstream>readervars</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R23.md</decomp_doc>
<owned_cells>TR-tv-23</owned_cells>
<decomp_context>Round 23 cell TR-tv-23 (CTO round-23 analysis @b8a07a7e17, item 2; rows D2-S17 and D2-S20). The order IS the GO. It applies nothing: DELTA=0 is the proof, and a verified DELTA=0 needs no pair (CTO ruling in the analysis, section 3).</decomp_context>
</decomp_ref>

  <objective>
    Put the reader-trust value of the transcripts Terraform root in git, read from applied state, so no applier ever types it again:
    a committed `readers.auto.tfvars`, the variable left with NO default, the header of `readers.tf` stating the applied state, and a
    plan of the reader resources that shows 0 changes. NOTHING is applied.
  </objective>

  <context>
    Your own row NFRA_TRNSPT-D2-S17: this root cannot be planned without a value for `second_reader_trust_principal_arns`
    (`readers.tf:15`, no default), and you supplied it from applied state in a tfvars file outside the repo. The CTO's ruling (analysis
    section 3): "A committed `readers.auto.tfvars`, holding exactly the applied value. The value is READ from applied state (the role's
    live trust policy), never typed; the commit cites `CTO_RULING_NFRA_TRNSPT_FWD5_WIPED_SILVER_READER_HOLDERS_20261009.md`. The variable
    keeps NO default in the `.tf`, so a tree without the file still refuses to plan. ... Proof: a plan of the reader resources shows 0
    changes; DELTA=0 needs no pair." Row D2-S20: "`readers.tf`'s header states the applied state, in the commit of item 2".
    KNOWN OBSTACLE: `infra/aws/terraform/.gitignore:5` ignores `*.auto.tfvars`. The ruling is a COMMITTED file.
  </context>

  <the_act>
    1. READ, live: `aws iam get-role --role-name teams-global-transcripts-second-reader-role` -- the trust policy's principal ARNs (the
       issuer read exactly one at 2026-10-11T06:27Z: the IAM user Opal_Terminal). If any OTHER variable of this root has no default and
       no committed value, STOP and report it by name: this order covers one variable.
    2. WRITE `infra/aws/terraform/transcripts/readers.auto.tfvars`: `second_reader_trust_principal_arns = [ ... ]` holding exactly the
       ARNs step 1 read, in the order read, plus a comment header: the value is READ from applied state, the time of the read, the
       ruling's file name above, and that a change to it is a commit under a pair carrying Andrew's C-READERS word. Nothing else in the
       file.
    3. `.gitignore`: add ONE negation line for this one path beneath line 5's pattern, so the file is tracked. Do not un-ignore the
       pattern for any other root. Print `git check-ignore -v` for the path before and after.
    4. `infra/aws/terraform/transcripts/readers.tf`: the variable block is UNCHANGED (no default). Edit only the comment header: its
       second line says the readers are "NOT APPLIED -- plan only"; state the applied state instead (applied 2026-10-09T09:55Z under
       ledger nfra-trnspt-a18-second-reader-laptop-20261009, 3 added and 1 changed; the trust value lives in `readers.auto.tfvars`).
       No resource, local or variable line changes.
    5. PROOF, no apply: with NO `-var` and no tfvars outside the repo, `terraform plan` (through the root's usual plan path; never a
       bare `terraform apply`) targeted at the reader resources -- `aws_iam_role.second_reader`, `aws_iam_policy.second_reader`,
       `aws_iam_role_policy_attachment.second_reader` and the silver reader's role, policy and attachment -- must read `No changes`.
       Print the plan's summary line. A non-zero plan = STOP, commit nothing of steps 2 to 4, report the diff lines.
    6. NEGATIVE CONTROL: with the tfvars file moved aside, the same plan must be REFUSED by terraform (`No value for required variable`).
       Print the error line, then put the file back.
    7. Commit steps 2 to 4 in ONE commit under your own author line, its message citing the ruling's file name.
  </the_act>

  <bounds>
    - NO apply of any kind. No resource, role, policy or key policy changes; a plan that is not 0 changes stops the order.
    - The value is never typed from memory or from this order: it is what step 1 reads.
    - No transcript text. Names, ARNs, dates and counts only.
  </bounds>

  <paths>
    infra/aws/terraform/transcripts/readers.auto.tfvars
    infra/aws/terraform/transcripts/readers.tf
    infra/aws/terraform/.gitignore
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- nothing is applied; no schedule is touched.
comp-iam: RUN -- the value written is who may assume the second-reader role; it is read from the role's live trust and the proof is a 0-change plan of both reader roles, so the git value and the applied value are shown equal, not assumed equal.
comp-adversary: RUN -- a typed value that differs from applied state (step 1 reads it, the check re-reads it live); the negation line un-ignoring other roots' tfvars (one path only, check-ignore printed); a plan that passes only because a stray tfvars outside the repo still supplies the value (step 5 names NO -var and step 6 is the negative control); a default slipped into the variable (the check refuses it). BLIND: other roots that read this variable -- there should be none; the applier says so or names them.
lane: the paths block.
</preflight>

<proof_of_spec>
  <criterion id="TR23-tv23-AC1" cell_refs="TR-tv-23"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/r23_checks.py tv23</invocation><expect>R23-TV23-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states step 1's read, the two `check-ignore` lines, step 5's plan summary line and step 6's refusal line.
  Dry-run before the act: `R23-TV23-FAIL absent: infra/aws/terraform/transcripts/readers.auto.tfvars` -- FAIL as expected.

<expected_criteria>TR23-tv23-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: step 1's principals (count and ARNs), the check-ignore lines, the plan summary line, the negative
    control's error line, the check line, the commit hash and the measured push state. Write the proof instance; leave the status flip
    to the issuer. Then stay available: the mail pull's re-apply (NFRA_TRNSPT.TO-APPLY-mp23, STAGED) follows on its own GO.
  </report>
</task_order>
