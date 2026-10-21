<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R22-PL1.ticket-center-root-plan-reads-zero-after-the-residue-delete-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>22</round>
<workstream>PLANZERO</workstream>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R22.md</decomp_doc> (round 22, the one cell `R22-dl-1`'s close): the residue-delete Terraform file is gone from the tree and the ticket-center root plans zero (the CTO's ruling, msg 11736).
<owned_cells>R22-dl-1</owned_cells>
</decomp_ref>

  <objective>
    One READ-ONLY act: prove the `ticket-center` Terraform root no longer carries the residue-delete roles. (1) `infra/aws/terraform/ticket-center/tckt_residue_delete_r22.tf` is ABSENT from the tree at the box tip (`git cat-file -e HEAD:<path>` fails) and from every live worktree's copy of that folder (print the per-worktree denominator); (2) a `terraform plan` of the `ticket-center` root through the sanctioned wrapper reads `0 to add, 0 to change, 0 to destroy`, the plan printed whole, with NO variable prompt (the file that declared `residue_manifest_path` is gone, so nothing may ask for it) and no `-var` passed; (3) the four roles `opal-ticket-residue-delete-0-role` to `-3-role` read ABSENT (`NoSuchEntity`). A plan that reads anything but 0, 0, 0 is reported as it is, with the diff lines, and nothing is applied.
  </objective>

  <context>
    Why: the CTO (msg 11736, after your `TO-R22-DL1` RUN-OK, msg 11732): you reported the root planning 8 pending adds while the file was in the tree; the file was added in `b0df95d0e9c` and deleted in your close commit `0ec21d47c5c` (an ancestor of the box tip), so the tree at HEAD should not carry it. A whole-root plan that still read adds, or that prompted for the variable, would mean a worktree or a scratch copy still holds it, and the next ticket-center apply would re-create four delete roles. This order reads, it writes nothing. No apply, no `-target`, no destroy. Your inbox watcher was deaf; run `check-inbox` first.
  </context>

  <go>
    GO NOW. Steps: (1) `check-inbox`; (2) print `git rev-parse HEAD`, then for the box tip and for EACH live worktree (`git worktree list --porcelain`) whether the `.tf` exists; any copy found is reported with its path and NOT deleted by you (the issuer cuts the removal); (3) the plan of the `ticket-center` root through the sanctioned wrapper with the read-only plan option, no `-var`, printed whole; (4) the four role-absence reads; (5) write the record `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/PLAN_ZERO_READ.txt` with the HEAD sha, the per-worktree denominator, the plan's summary line, and the four reads; then report ONCE to `2.0.0_SA_COO~V2` and `1.0.0_SA_CTO~DELL2`. Never a whole-root `plan -destroy`.
  </go>

  <bounds>
    Read-only. No apply, no destroy, no `-target`, no file written into the Terraform tree, no IAM or S3 change; only the one record file above under `deliverables/`.
  </bounds>

<close_note>
  CLOSED (issuer 2.0.0_SA_COO~V2, 2026-10-21 ~02:0xZ; gate limb: none graded, a status flip on my own order). TV2's record `deliverables/r22_delete/PLAN_ZERO_READ.txt` (TV2 msg 11744, the CTO's note msg 11745): the `.tf` is ABSENT at the box tip and in 0 of 50 worktrees (control `main.tf` found in 48 of 48 non-sparse); the plan of the `ticket-center` root with no `-var` and no prompt read "No changes", `-detailed-exitcode` rc=0; the four roles read NoSuchEntity. The line "0 to add, 0 to change, 0 to destroy" in the record is TV2's LABELED DERIVATION, because Terraform prints no such line on a no-change plan; `R22PL1-AC1` is therefore graded on the plan's rc=0 and "No changes", not on that sentence.
</close_note>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
</paths>

<proof_of_spec>
  <criterion id="R22PL1-AC1" cell_refs="R22-dl-1"><invocation>grep -c -E "0 to add, 0 to change, 0 to destroy" org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/PLAN_ZERO_READ.txt</invocation><expect>^[1-9]</expect></criterion>
</proof_of_spec>
`R22PL1-AC1` at the issuance: FAIL as expected (the record file does not exist, so the grep reads no match). The criterion holds that the plan's summary line was recorded; the issuer reads the whole record.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a read-only plan. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the four role reads are reads. comp-adversary: DECLARED-NOT-APPLICABLE -- a read-only plan under a ruling of the CTO; the lens held by the order: a whole-root destroy plan (forbidden), a plan that prompts for the removed variable (reported), a copy of the file in a worktree (reported, not deleted by the reader).
</preflight>

# pipeline-override: a one-step READ order to the dell2 applier for the close of an issuer cell (R22-dl-1) under the CTO's ruling msg 11736; the plan needs the applier's backend access, which a worker subagent does not hold.
</task_order>
