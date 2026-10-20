# TCKT_VNEXT round 22 -- the one delete pass for the fabric's synthetic S3 residue: never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-20. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R22-DL1` (staged). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Authority:** Andrew-direct 2026-10-16 ("you can delete synthetic and test files any time, i do not need an open call", `ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`); the CTO's msgs 11428 and 11434 (ONE pass for all fabric-written synthetic residue, a throwaway role, an exact key and VersionId list, no prefix, no wildcard, the Deny untouched, no console ask to Andrew) and the round-21 analysis (round 22 = the residue delete with a read-back).

## 1. What is deleted, bound to bytes
- **The manifest** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json`, blob `7f07b0b6d861446bcaa7e3b01d90653e1613276d`: exact `{bucket, key, version_id}` entries and nothing else. FINAL: 46 entries (4 in `opal-data-cottonwood`: the `TCKT_VNEXT` trade-form objects of `TO-R20-PROD3` and `TO-R21-RB1`, 31 bytes each; 42 in `opal-data-irpt`: the `IRPT_ANLREQ` run 4 to run 7d objects, from `2.0.0_SA_COO~Y2`'s list `synthetic_residue_delete_list_20261020.json`, its run 7b supplement and IB2's records `residue_7c.json` and `residue_7d.json`). Any later residue (`~Y2`'s FWD-9 and Multi-Comp runs after r34o) is a SEPARATE pass under its own pair addendum, never added to this manifest after signing. Each entry was read live from `list-object-versions` on its exact key: one version, no delete marker, so deleting the version leaves nothing behind; each was written by a fabric run that is named in the entry.
- **No prefix, no wildcard, no pattern**; the check refuses a key with `*`, `?`, `[`, `]` or a trailing `/`, and a `version_id` of `null`.
- Nothing is read or deleted by listing; the applier never lists a prefix to decide what to delete.

## 2. The mechanism, exactly (Terraform, `safe-apply`; no hand IAM)
A new file `infra/aws/terraform/ticket-center/tckt_residue_delete_r22.tf` and a copy of the manifest beside it, `tckt_residue_delete_r22.manifest.json` (byte-equal to the signed blob):
```
locals {
  residue = jsondecode(file("${path.module}/tckt_residue_delete_r22.manifest.json")).objects
  chunks  = { for i, c in chunklist(local.residue, 12) : tostring(i) => c }
}
resource "aws_iam_role" "tckt_residue_delete_r22" {
  for_each             = local.chunks
  name                 = "tckt-residue-delete-r22-${each.key}"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "tckt_residue_delete_r22" {
  for_each = local.chunks
  name     = "tckt-residue-delete-r22-${each.key}"
  role     = aws_iam_role.tckt_residue_delete_r22[each.key].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in each.value : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in each.value : o.version_id] } }
    }]
  })
}
```
- The manifest is cut into chunks of 12 objects, one role per chunk (IAM limits a role's inline policies to 10,240 characters in all; the draft's 28 IRPT keys alone are about 7,100). Each role allows ONLY `s3:DeleteObjectVersion`, ONLY on its chunk's exact object ARNs, ONLY for its chunk's version ids, and is assumable ONLY by `cloudops-dell2-agent-user`. (A version id is unique to one object, so the any-of condition names no pair the manifest does not carry.)
- The assume is `aws sts assume-role --role-arn arn:aws:iam::313476888478:role/tckt-residue-delete-r22-<i> --duration-seconds 900` (15 minutes), once per chunk; the temporary credentials are never printed or written to a file; each chunk's deletes run in its own session only.
- **The Deny is untouched.** `DenyS3DeletesOnProductionData` in `cloudops-dell-agent-deploy-policy` (v7 at the draft) is not edited, detached or worked around by any grant to the agent user: an assumed-role session is the role's permissions, which carry only the exact-version delete above.

## 3. Preconditions (each read by the applier before the apply; a failed one is a STOP, reported first)
1. The manifest blob equals this pair's; the HCL equals section 2 (blob printed); the pair's CTO half is signed.
2. Every manifest entry reads PRESENT at its version (`head-object --version-id`, 200), its key lists one version and no marker, and its head shows NO `ObjectLockMode`, no `ObjectLockLegalHoldStatus` ON and no retention (the manifest holds retained report PDFs: a lock or retention on any entry is a STOP, never a bypass).
3. The census of open ledgers naming the two buckets, `opal-ticket-api`, `opal-tickets` or `opal-users-v2` is clear in every live worktree; `~Y2`, `~IB2` and the CTO say none due or open (their fire windows), and no run of `~Y2` is in flight on the manifest's keys (run 7b terminal and its supplement merged).
4. The plan shows ONLY the adds of section 2 (`1 role + 1 policy per chunk of 12`: 2 x ceil(N/12) to add, 0 to change, 0 to destroy; 8 to add for 46 objects: four roles); any other resource or attribute is a STOP before apply.
5. The LGIC naming gate: a refusal of a name is a STOP (a missing registry row, never a hand-typed workaround); the applier reports it and waits.

## 4. The act and its read-back
Apply; assume the role (900 s); delete each manifest version by `aws s3api delete-object --bucket B --key K --version-id V` (a 204 each); read each ABSENT with the check's own reads (a 404 only; a 403 is not absence) and read each key's versions and markers empty; then `terraform destroy` of every role and policy (a plan of 0 to add, 0 to change, 2 x ceil(N/12) to destroy); read every role ABSENT (`NoSuchEntity`); read the Deny still in the deploy policy; read ONE non-manifest object in each bucket PRESENT (the control). No other delete, ever. If a step fails: STOP, destroy the role first, report the world as left.

## 5. Blast radius and rollback per key
| key | touched | rollback |
|---|---|---|
| each manifest object (one version, no marker) | permanently deleted | none: the objects are invented synthetic data written by named fabric runs (31 to a few hundred bytes), reproducible by rerunning the run |
| the throwaway roles and their policies | created, used, destroyed in one session | `terraform destroy` (run in the act); the role also expires with its 900 s session |
| everything else | nothing | -- |

## 6. The act's evidence
`R22_DELETE_RESULT.json` under `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/` and `r22_residue_delete_check.py` printing `RUN-OK (residuedelete)` beside its self-test `R22-RESIDUEDELETE-SELFTEST-OK`; a change-management ledger opened at the start and closed after the read-back.

## COO half -- SIGNED 2026-10-20 by `2.0.0_SA_COO~V2`
I read the four chunks' policy sizes (the IRPT chunks stay far under the 10,240-character limit), re-read every manifest key live (one version, no delete marker each; the 14 run 7c and 7d keys on 2026-10-20 ~22:1xZ, the 7b keys 2026-10-20 ~17:3xZ, my four earlier), read the Deny in `cloudops-dell-agent-deploy-policy` v7 and the census that no role holds a delete on these keys, and drafted the check (self-test OK). The CTO half is owed; the GO to `TO-R22-DL1` is an amendment citing this file's blob.
