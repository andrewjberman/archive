# ANNOUNCE -- OG-al-1 PHASE A (0.9.0_WK_NFRA_OPLGTW~18), no AWS write

## The file

`infra/aws/terraform/opal-gateway/hx-capability.tf`: ONE `aws_lb_listener_rule.hx_capability` on
`aws_lb_listener.https.arn`; ONE `forward` action to `aws_lb_target_group.gw.arn`; ONE `path_pattern` condition with
exactly `/hx/transcripts/*` and `/hx/mail/*`. No catch-all, no other resource, no other file touched.

## The priority

**35.** Re-read live at authoring (`aws elbv2 describe-rules`, https listener `.../2904a0140214f982`): priorities
10, 20, 30, 31, 32, 33, 34 and default; none carries a `/hx/` pattern. 35 is free in the live listener AND unclaimed
by any `.tf` in `opal-gateway/` (priority grep: 10 20 30 31 32 33 34). It sits after every existing rule and no
existing rule matches `/hx/...`, so it shadows nothing and nothing shadows it.

## The name

An ALB listener rule carries no name of its own. `NAMING_SCHEMA.json` has no node type or kind for it
(`aws_lb_listener_rule` is in neither `tf_type_map` nor `tf_unmapped_own_name`; kind values end at `lb`/`cluster`;
tag values are listed under `not_covered`). `lib/opal_naming.py name()` refused every kind tried for a rule, so no
name and no `Name` tag are typed (the `ms-ingest.tf` rules' hand-typed `Name` tags are the pre-LGIC precedent, not
copied). No builder-refusal row is filed: nothing is named.

## Readings

- `al.AC1.sh` (the early read): `listener rules 1 ['hx_capability']; other resources []`,
  `path patterns ['/hx/mail/*', '/hx/transcripts/*']`, `action types ['forward']`, `RESULT: PASS`, `exit=0`.
- Targeted plan (`terraform -chdir=infra/aws/terraform/opal-gateway plan -input=false -lock=false
  -target=aws_lb_listener_rule.hx_capability`; `safe-apply` gates `apply` only and refuses a plan, so the terraform
  binary was called directly, read-only): **`Plan: 1 to add, 0 to change, 0 to destroy.`** Fed as OG-pr-1 A1:
  `TF_VAR_mcportal_owner_key_claim=sub`; `TF_VAR_mcportal_owner_key` read from the live grant-writer Lambda straight
  into the variable (never printed); `build_package.py --out .scratch/gw_al.zip` rc=0; the deps-layer zip is
  byte-identical to the main tree's (`cmp`). The planned rule shows listener, priority 35, forward to
  `opal-gateway-tg`, the two patterns; tags_all are the provider defaults only.
- `-lock=false` on a plan that writes nothing; no other `safe-apply` on `opal-gateway` was observed in flight by
  this worker (the issuer owns train ordering, C4).

## Rollback

Remove `hx-capability.tf` (or the one rule) and apply (targeted, 0 add / 0 change / 1 destroy); the two paths then
return to the Entra sign-in. Break-glass: `aws elbv2 delete-rule --rule-arn <hx_capability arn>`; Terraform state then
needs `terraform state rm aws_lb_listener_rule.hx_capability`.

## STOP

PHASE B (steps 4-6: ledger `nfra-oplgtw-hx-alb-rule`, targeted apply, `al.AC2.sh`) waits for the issuer's GO.
