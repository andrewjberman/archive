# Session log -- 0.7.0_AE_CloudOps~TM1, TCKT_MTADTA.TO-MD-r1 (2026-10-16)

**archetype:** DEPLOY

## What was done
1. Preconditions: x1, x2, x3 merged (6a0514c418, b4a8bceea5, 703b40e3be), all three orders complete, eight repair checks print their OK tokens.
2. Ledger `tckt-mtadta-trino-root-apply-20261016` opened, then five legs added on the amendment (29ef973419); closed with all 10 legs proven.
3. Item 3: no authoritative office egress list in the estate; `office_ips` left empty. Row `TCKT_MTADTA-D1-S6`. The order's row id `...-WTM1-S<k>` is refused by `surprise-row-gate` (grammar `W<n>`), so the seat-row form was used.
4. Zips built (not committed). Layer: `list-layer-versions` denied; version 31 found by probe (`TCKT_MTADTA-D1-S8`); `layer.auto.tfvars` @8691d491db.
5. Plan 26 create, 0 destroy or replace, matching THE CELL. One gated apply, rc=0: 26 added, 0 changed, 0 destroyed.
6. First refusals read: REFUSED (the box identity, in `AdministratorAccessOpalCapital`, invoked both aliases; a fake multipart abort returned NoSuchUpload; the S3 simulation said explicitDeny). The issuer's amendment followed.
7. 7a MFA condition on the group invoke (plan 0/1/0, apply rc=0). 7b `Andrew_Berman` (2 MFA devices) added as the only member. 7c `aws lambda put-resource-policy` on both aliases (@46130e1cff `door_resource_policy.json`). 7d probe: AccessDenied on both aliases, rc=254.
8. Checks: `applied` R1-APPLIED-OK, `refusals` R1-REFUSALS-OK, `plan` R1-PLAN-OK exit=0, `mfa` R1-MFA-OK. Each run twice, identical.

## Not done, by the order
No object read or written, no secret value, no other group member, no alarm or notification resource, no push. The admin GetObject probe moves to MD-r-2.

## Things the reader should know
- The pre-amendment `refusals` check invoked both aliases once as the box identity (two real invokes, empty payload, before the Deny existed). The collector's own hourly rule also fires and fails at the empty credential secret (expected).
- The door Deny sits outside Terraform state; `door_resource_policy.README.md` states how to re-apply it.

## Compiler Tools
- `terraform plan / show -json` + `jq`: 26 creates listed by address; worked.
- `safe-apply.sh`: two applies, rc=0 each; worked.
- `deploy_ledger.py open / close-leg / close`: worked; it has no add-leg command, so the five amendment legs were appended to the sentinel JSON by hand in the tool's own schema and the tool read them back.
- `proof-of-spec-check.py`: first run INVALID on two enum values (`kind`, `deployed_state`), second run VALID rc=0.
- `comp-which "office egress ip addresses"`: returned a 4875-hit generic content search, no usable answer; native Grep found the candidates. Gap: no tool for "where does the estate record a network address".
- `terraform fmt -check`: read-only form used on `access.tf`, rc=0.
