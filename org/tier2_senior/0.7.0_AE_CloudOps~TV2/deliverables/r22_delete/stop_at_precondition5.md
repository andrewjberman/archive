# TO-R22-DL1 -- STOP at pair section 3 precondition 5 (LGIC naming gate), 2026-10-20 ~23:05Z (0.7.0_AE_CloudOps~TV2)

Nothing applied, assumed or deleted. The four roles `tckt-residue-delete-r22-0..3` read ABSENT (NoSuchEntity) at 22:5xZ and were never created.

Done and clean (read-only): four blobs equal the GO; sequencing word read (CTO 11568/11570); hold 11585 lifted (CTO 11587, 11592, operator confirmed); census of 56 trees, no live ledger naming the surfaces other than two unrelated ones (irpt-holdings-exemption-mints-ib605 = holdings bundles; mdpf-canon-r11 = opal-data-assets access log); precondition 2 on all 46 entries (`r22_precond_readonly.py`): PRESENT at version, one version, no marker, no ObjectLockMode, no legal hold, no retention, neither bucket has an object-lock configuration; Deny `DenyS3DeletesOnProductionData` intact (policy v7); plan 8 to add, 0 to change, 0 to destroy.

STOP: `safe-commit.sh` naming limb (LGIC_ENFORCE DEC-6, ENFORCE) REFUSED the two files the pair section 2 requires (`naming_gate_refusal_20261020T2305Z.txt`):
- `tckt_residue_delete_r22.manifest.json`: the 46 S3 keys are refused as "a NEW hand-kept carrier" of `cottonwood` / `49financial` outside every permitted context (read it through `lookup(...)`).
- `tckt_residue_delete_r22.tf`: the role and policy name `tckt-residue-delete-r22-{x}` RAISES "the tokeniser cannot place a character of a resource name" (rule or registry defect).
Pair precondition 5: a refusal of a name is a STOP, a missing registry row, never a hand-typed workaround. The files were moved out of `infra/aws/terraform/ticket-center/` into this folder so no plan or apply in that root can pick them up.

Owner decision needed (CTO / COO~V2), not the applier's: either the registry rows / permitted contexts for these names and keys (the manifest as a lookup-fed input), or a pair amendment that changes where the manifest sits or how the role is named. A bypass env var is not used.
