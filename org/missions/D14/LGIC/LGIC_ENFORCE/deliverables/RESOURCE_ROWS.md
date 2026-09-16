# RESOURCE_ROWS -- the resource-to-system rows (LGIC_ENFORCE EN-r-4, round 2)

**Cell:** LGIC_ENFORCE `EN-r-4` (PRD v1.2 DEC-1 candidate E13; `1.0.0_SA_CTO` ruling 97177), task order
`LGIC_ENFORCE.TO-EN-r-4-r2`, written by `0.9.0_WK_LGIC_ENFORCE~1` on branch `wk-lgic-enforce-2c-1`, cut from
CLOUD @`68644b3c19`. Every file and line cited below is read at that base.

## 1. What this cell does

`infra/logic/registry/resources.json` carries `{name, type, system, evidence}` rows. `lib/opal_naming.py`
`grade()` reads a row ONLY when a resource's own tokens resolve no system (GRADING_RULE R1.d/R1.e, `_slots`):
with a row, the `{system}` placeholder is filled with the row's system and the name is graded as usual;
without one, the placeholder stays and the verdict is unchanged (OUT-OF-PATTERN, per grade.placeholder).
`validate()` refuses a row with a missing/extra/empty field, a repeated `(name, type)`, a `system` outside
`systems.json` (or `opal`), a `type` the grade does not take, or a name whose own tokens already resolve a
system (a redundant row).

## 2. The population and what it covers

The fixed input `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/RESOURCE_GAPS.json`
holds 48 IAM_ROLE gaps (49financial 14, inflection 27, cottonwood 6, demo 1) whose canonical form at the cut
carries `{system}`. **30 of the 48** get a row here, each citing the Terraform file (and, for two, an S3
write target or a sibling Terraform root) that names the resource's owning system without guessing:

- **etfs** (3): the two `*-etf-ownership-daily-role` roles (inf, cot) each write ONLY to
  `opal-data-etfs/daily/{firm}/` per their own file's WRITE-OUT MODEL comment; `cot-satellites-registry-producer-role`
  cites `ETFS_SATELLITES.TO-6-AE` and `POSN_ASTTAX.TO-V2-1` (both D4/etfs projects) and writes the satellites
  registry the Positioning page's SATELLITES mode reads.
- **mdpf** (3): `wsb-49f-model-aua-daily-role` and `wsd-49f-partner-held-etf-daily-role` are declared inside
  the `mdpf-pipeline` Terraform root (not `bd-pipeline`), not the 49f firm's own root; `cot-rebalancer-runner-role`
  cites `WSE_COTMDL.WS5`, PRD `docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md` -- a Cottonwood-into-
  Model-Portfolios fold-in project.
- **advi** (24): `bd-silver-merge-role` (`ADVI_BDAPIMIG P1 D2`), `demo-transform-runner-ec2-role`
  (`ADVI_DEMOV1`), `cot-exporter-ec2-role` and `cot-gold-layer-ec2-role` (the whole `cot-pipeline/iam.tf`
  file's own header names its governing PRD as `docs/architecture/ADVI_COTETL.md`), and 20 `inf-pipeline`
  roles each citing one of `ADVI_INFETL.LAMBDA-DIMS`, `ADVI_INFINGE`, `ADVI_INFSHIP`, `ADVI_INFNNA` or
  `ADVI_ORIAPI` directly in their own file's header or section comment (all `PORTAL.ADVISOR_INTELLIGENCE`
  projects, D2). Every citation is quoted in the row's `evidence` field.

**18 of the 48 get NO row** -- listed in the fenced json below with the reason no owner could be named
without guessing. Every one of them is either (a) a per-firm ETL role whose own Terraform section carries
no product/system citation at all (a bare work-order number like `W2.1`, or "kept from previous config"),
(b) cites a project code that is not a `systems.json` PRODUCT/VENDOR/PLATFORM_SUBSYSTEM (`AUDIT-008.PERM`,
`OPAL_VENDORPROVENANCE.BR1-AE`), or (c) has no Terraform declaration in the tree at this base at all
(`bd-merge-daily-lambda-role`, `bd-pipeline-task-role` -- present in the LGIC_NAMING round-2 LIVE census,
absent from every `.tf` file this worktree can read; a live-only name with no repo-side attribution).
No placeholder here is guessed from its function-word tokens (e.g. "gold-layer", "exporter" do NOT imply a
product) -- CLAUDE.md Rule 22a and the cell's own instruction ("no owner nameable" gets no row, never a guess).

## 3. Not attempted: MDPF/ADVI/IRPT resources beyond the fixed population

Andrew-direct msg 96910 ("LGIC is aimed at the MDPF, ADVI and IRPT pipelines") is the reason the fixed
48-gap population already skews toward `mdpf`/`advi`/`etfs` evidence (24 of 30 rows are `advi`). The cell's
text also invites rows for "MDPF, ADVI and IRPT resources... wherever evidence names the owner" beyond the
fixed `RESOURCE_GAPS.json` population; no such population is fixed anywhere this round (unlike the 48
gaps), and building one would mean a fresh Terraform/census sweep for other `{system}`-placeholder names
outside this order's population -- out of this cell's bound (no acceptance criterion reads it, and R4-J1
grades what is here, not what could be added). Not done; recorded rather than silently skipped.

```json
{
 "population": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/RESOURCE_GAPS.json",
 "rows": 30,
 "placeholders": [
  {"name": "bd-allocation-checker-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:152-155,169-171 @68644b3c19 -- section 2 names no product; tag is System='BDPipeline' (the Terraform module's own name, not a systems.json system)"},
  {"name": "bd-allocation-processor-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:769-772 @68644b3c19 -- section 7, 'dedicated -- replaces shared lambda-execution-role', names no product or system"},
  {"name": "bd-daily-trigger-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:21-24 @68644b3c19 -- section 1 names no product or system, only the Lambdas it triggers"},
  {"name": "bd-exporter-ec2-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:334-338,352-355 @68644b3c19 -- section 5 names the EC2 instances it serves, not a product; tag System='BDPipeline'"},
  {"name": "bd-gold-detail-generator-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:710-713 @68644b3c19 -- section 6, 'Already managed -- kept from previous config', no product or system named"},
  {"name": "bd-gold-eventbridge-step-functions-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:888-891 @68644b3c19 -- section 8, 'Already managed -- kept from previous config' (planned Step Functions migration), no product or system named"},
  {"name": "bd-gold-layer-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:280-281,292-295 @68644b3c19 -- tag is System='BDGoldLayer' (the pipeline stage's own name), no systems.json product cited"},
  {"name": "bd-gold-step-functions-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:828-831,845-848 @68644b3c19 -- section 8, 'Already managed -- kept from previous config'; tag System='BDGoldLayer', no systems.json product cited"},
  {"name": "bd-merge-daily-lambda-role", "type": "IAM_ROLE", "why": "no aws_iam_role (or any resource) named bd-merge-daily-lambda-role exists anywhere under infra/aws/terraform/ at CLOUD @68644b3c19 (checked the whole tree, not just bd-pipeline/); it is a LIVE-only name in the LGIC_NAMING round-2 census with no repo-side attribution to read"},
  {"name": "bd-pipeline-task-role", "type": "IAM_ROLE", "why": "same absence as bd-merge-daily-lambda-role: no Terraform declaration anywhere in the tree at this base; LIVE-only, no evidence names an owner"},
  {"name": "bd-processor-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/bd-pipeline/iam.tf:210-213 @68644b3c19 -- section 3, 'Used by: bd-price-update', no product or system named"},
  {"name": "inf-assets-trigger-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/iam.tf:879-883 @68644b3c19 -- section 5c cites project 'AUDIT-008.PERM', which is not a systems.json PRODUCT/VENDOR/PLATFORM_SUBSYSTEM row; naming a system from it would be a guess"},
  {"name": "inf-bronze-complete-emitter-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:1-5 @68644b3c19 cites 'TO OPAL_VENDORPROVENANCE.BR1-AE', a vendor-data-provenance migration project, not a systems.json product/vendor/platform-subsystem row"},
  {"name": "inf-exporter-ec2-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/iam.tf:490-493 @68644b3c19 -- section 4 (work order W2.4), no product or system named"},
  {"name": "inf-gold-layer-ec2-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/iam.tf:69-72 @68644b3c19 -- section 1 (work order W2.1), no product or system named"},
  {"name": "inf-gold-layer-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/iam.tf:333-336 @68644b3c19 -- section 2 (work order W2.3), 'Used by: inf-portal-publisher, inf-portal-advisor-publisher, inf-client-detail', no systems.json product cited"},
  {"name": "inf-gold-trigger-lambda-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/inf-pipeline/iam.tf:386-389 @68644b3c19 -- section 3 (work order W2.2), no product or system named"},
  {"name": "cot-session-scheduler-role", "type": "IAM_ROLE", "why": "infra/aws/terraform/cot-pipeline/schedule-et.tf:1-44 @68644b3c19 -- an Andrew-direct session-anchor scheduling change (DST-safe 4:30pm ET), no systems.json product/vendor/platform-subsystem cited"}
 ]
}
```
