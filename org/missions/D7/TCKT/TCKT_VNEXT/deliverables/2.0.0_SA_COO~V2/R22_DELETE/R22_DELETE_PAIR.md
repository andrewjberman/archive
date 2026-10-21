# TCKT_VNEXT round 22 -- the one delete pass for the fabric's synthetic S3 residue: never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-20. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R22-DL1` (staged). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Authority:** Andrew-direct 2026-10-16 ("you can delete synthetic and test files any time, i do not need an open call", `ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`); the CTO's msgs 11428 and 11434 (ONE pass for all fabric-written synthetic residue, a throwaway role, an exact key and VersionId list, no prefix, no wildcard, the Deny untouched, no console ask to Andrew) and the round-21 analysis (round 22 = the residue delete with a read-back).

## 1. What is deleted, bound to bytes
- **The manifest** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json`, blob `2e8786cc4219b02a8148c480ae90a9b339ef953d`: exact `{bucket, key, version_id}` entries and nothing else. **RE-CUT 2026-10-21 (the CTO's ruling, msg 11699, after TV2's STOP at the first delete, `deliverables/r22_delete/stop_at_delete_step.md`): 42 entries, ALL in `opal-data-irpt`** (the `IRPT_ANLREQ` run 4 to run 7d objects from `2.0.0_SA_COO~Y2`'s list `synthetic_residue_delete_list_20261020.json`, its run 7b supplement and IB2's records `residue_7c.json` and `residue_7d.json`; each read live: one version, no delete marker). The 4 `opal-data-cottonwood` trade-form objects (31 bytes each) are NOT in this pair: they are recorded in `R22_COTTONWOOD_RESIDUE_RECORD.json` (blob `bf48a75374e2a78e436367f842bc1c548299cf34`) and no act of this order deletes them. Why: the `opal-data-cottonwood` bucket policy carries `DenyForeignFirmPrincipals` (a Deny of `s3:*` to every principal outside a 10-entry `ArnNotLike` allow-list) and `DenyRestrictedWriteExceptBreakglass` (a Deny of `s3:PutObject*`, `s3:DeleteObject*` and `s3:RestoreObject` to everyone but `role/cloudops-cot-restricted-breakglass-role`); the throwaway role is on neither list (TV2's first delete returned AccessDenied), the Deny and its allow-list are never edited, and the census of 2026-10-20 found no principal on the allow-list holding `s3:DeleteObjectVersion` on those keys (only the two admin users hold it, and the break-glass role holds none), so they stay as recorded synthetic residue, an act for Andrew (the CTO lists it). **The `opal-data-irpt` bucket policy as read live 2026-10-21 ~01:2xZ: ONE statement, `DenyInsecureTransport` (Deny `s3:*` when `aws:SecureTransport` is false); versioning Enabled; no object-lock configuration.** The role's calls go over HTTPS, so that statement does not apply.
- **No prefix, no wildcard, no pattern**; the check refuses a key with `*`, `?`, `[`, `]` or a trailing `/`, and a `version_id` of `null`.
- Nothing is read or deleted by listing; the applier never lists a prefix to decide what to delete.

## 2. The mechanism, exactly (Terraform, `safe-apply`; no hand IAM)
A new file `infra/aws/terraform/ticket-center/tckt_residue_delete_r22.tf` ONLY (no copy of the manifest is placed in the Terraform tree: the naming gate refuses a hand-kept carrier of firm names there, and `org/` is outside its declaration domain). The manifest is read from its repository path through a variable the applier passes identically to the plan, the apply and the destroy (the absolute path of `R22_DELETE_MANIFEST.json` in the workspace, byte-equal to the signed blob):
```
variable "residue_manifest_path" {
  type = string
}
locals {
  residue = jsondecode(file(var.residue_manifest_path)).objects
  chunks  = chunklist(local.residue, 12)
}
resource "aws_iam_role" "residue_delete_0" {
  name                 = "opal-ticket-residue-delete-0-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_0" {
  name = "opal-ticket-residue-delete-0-policy"
  role = aws_iam_role.residue_delete_0.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[0] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[0] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_1" {
  name                 = "opal-ticket-residue-delete-1-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_1" {
  name = "opal-ticket-residue-delete-1-policy"
  role = aws_iam_role.residue_delete_1.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[1] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[1] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_2" {
  name                 = "opal-ticket-residue-delete-2-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_2" {
  name = "opal-ticket-residue-delete-2-policy"
  role = aws_iam_role.residue_delete_2.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[2] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[2] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_3" {
  name                 = "opal-ticket-residue-delete-3-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_3" {
  name = "opal-ticket-residue-delete-3-policy"
  role = aws_iam_role.residue_delete_3.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[3] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[3] : o.version_id] } }
    }]
  })
}
```
- Names are the naming gate's own form (a role ends `-role`, a policy `-policy`; four explicit chunk blocks, since a templated name raises "the tokeniser cannot place a character"): `opal-ticket-residue-delete-0-role` to `-3-role` and the policies `-0-policy` to `-3-policy`. Tested against `naming-gate.py --diff --enforce` before this pair: `NAMING-GATE: PASS 8 graded`, every name CONFORMANT, no registry row needed (TV2's first STOP, `stop_at_precondition5.md`, was the names `tckt-residue-delete-r22-{x}` and a manifest copy inside the Terraform tree).
- The 42 entries fill chunks 0 to 3 (12, 12, 12, 6). A manifest of more than 48 entries is not this pair.
- The manifest is cut into chunks of 12 objects, one role per chunk (IAM limits a role's inline policies to 10,240 characters in all; the draft's 28 IRPT keys alone are about 7,100). Each role allows ONLY `s3:DeleteObjectVersion`, ONLY on its chunk's exact object ARNs, ONLY for its chunk's version ids, and is assumable ONLY by `cloudops-dell2-agent-user`. (A version id is unique to one object, so the any-of condition names no pair the manifest does not carry.)
- The assume is `aws sts assume-role --role-arn arn:aws:iam::313476888478:role/opal-ticket-residue-delete-<i>-role --duration-seconds 900` (15 minutes), once per chunk; the temporary credentials are never printed or written to a file; each chunk's deletes run in its own session only.
- **The Deny is untouched.** `DenyS3DeletesOnProductionData` in `cloudops-dell-agent-deploy-policy` (v7 at the draft) is not edited, detached or worked around by any grant to the agent user: an assumed-role session is the role's permissions, which carry only the exact-version delete above.

## 3. Preconditions (each read by the applier before the apply; a failed one is a STOP, reported first)
1. The manifest blob equals this pair's; the HCL equals section 2 (blob printed); the pair's CTO half is signed.
2. Every manifest entry reads PRESENT at its version (`head-object --version-id`, 200), its key lists one version and no marker, and its head shows NO `ObjectLockMode`, no `ObjectLockLegalHoldStatus` ON and no retention (the manifest holds retained report PDFs: a lock or retention on any entry is a STOP, never a bypass).
3. The census of open ledgers naming the two buckets, `opal-ticket-api`, `opal-tickets` or `opal-users-v2` is clear in every live worktree; `~Y2`, `~IB2` and the CTO say none due or open (their fire windows), and no run of `~Y2` is in flight on the manifest's keys (run 7b terminal and its supplement merged).
4. The plan shows ONLY the adds of section 2 (`1 role + 1 policy per chunk of 12`: 2 x ceil(N/12) to add, 0 to change, 0 to destroy; 8 to add for 42 objects: four roles); any other resource or attribute is a STOP before apply.
5. The LGIC naming gate: a refusal of a name is a STOP (a missing registry row, never a hand-typed workaround); the applier reports it and waits.

## 4. The act and its read-back
Apply; assume role 0 (900 s) and **test ONE delete first: the manifest's FIRST entry, then read it ABSENT; if it returns AccessDenied or anything but a 204 and an ABSENT read, STOP with every other entry untouched** (a second gate beyond the role's Allow is exactly what stopped the first attempt); then assume each role (900 s) and delete each remaining manifest version by `aws s3api delete-object --bucket B --key K --version-id V` (a 204 each); read each ABSENT with the check's own reads (a 404 only; a 403 is not absence) and read each key's versions and markers empty; then destroy every role and policy by a `terraform plan -destroy -target=` of EXACTLY the eight resources of section 2 (never a whole-root destroy plan; the apply of the destroy is the targeted plan only; a plan that names any other resource is a STOP) -- (a plan of 0 to add, 0 to change, 2 x ceil(N/12) to destroy); read every role ABSENT (`NoSuchEntity`); read the Deny still in the deploy policy; read ONE non-manifest object in each bucket PRESENT (the control). No other delete, ever. If a step fails: STOP, destroy the role first, report the world as left.

## 5. Blast radius and rollback per key
| key | touched | rollback |
|---|---|---|
| each manifest object (one version, no marker) | permanently deleted | none: the objects are invented synthetic data written by named fabric runs (31 to a few hundred bytes), reproducible by rerunning the run |
| the throwaway roles and their policies | created, used, destroyed in one session | `terraform destroy` (run in the act); the role also expires with its 900 s session |
| everything else | nothing | -- |

## 6. The act's evidence
`R22_DELETE_RESULT.json` under `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/` and `r22_residue_delete_check.py` printing `RUN-OK (residuedelete)` beside its self-test `R22-RESIDUEDELETE-SELFTEST-OK`; a change-management ledger opened at the start and closed after the read-back.

## COO half -- SIGNED 2026-10-20 by `2.0.0_SA_COO~V2`, RE-SIGNED 2026-10-20 on the naming amendment and RE-SIGNED 2026-10-21 on the irpt-only re-cut; the earlier signing was on the naming amendment (section 2: gate-conformant names, no manifest copy in the Terraform tree; the CTO re-signs his half on this blob)
I read the four chunks' policy sizes (the IRPT chunks stay far under the 10,240-character limit), re-read every manifest key live (one version, no delete marker each; the 14 run 7c and 7d keys on 2026-10-20 ~22:1xZ, the 7b keys 2026-10-20 ~17:3xZ, my four earlier), read the Deny in `cloudops-dell-agent-deploy-policy` v7 and the census that no role holds a delete on these keys, and drafted the check (self-test OK). The CTO half is owed; the GO to `TO-R22-DL1` is an amendment citing this file's blob.
