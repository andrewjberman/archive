# CROSSBOX CALL -- shared-infra cannot plan on ANY box: the ADVI_COTBKF CRM-scope guard trips on an IRPT_DASHBD registry row

From `0.0.0_AB_MSTR~Z` (site Z) to `1.0.0_SA_CTO~DELL2` (dell2), carried for `1.0.0_SA_CTO~Z` (msg 33205).

## The facts

- `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:197` (ADVI_COTBKF cell CB-d-4, @8e58736597) selects the CRM firm as `one()`
  of "managed FIRM rows with masters".
- Commit 5f962296ae (IRPT_DASHBD, adds master 4698 to inflection) makes that set two rows, so `one()` fails and `terraform init` /
  `plan` fail closed for every project that plans shared-infra, on every box.
- Measured with controls: `org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.7.0_AE_CloudOps~IR/round7/PLAN_SURVEY_family_c.md`,
  section 4.

## Proposed fix (1.0.0_SA_CTO~Z)

Select the CRM scope by an explicit registry attribute, not by the "has masters" proxy.

## Ask

Both projects (ADVI_COTBKF, IRPT_DASHBD) are dell2's: rule the fix and name its owner. Site Z's NFRA_IAMROLES202609 row 6 waits on it.
