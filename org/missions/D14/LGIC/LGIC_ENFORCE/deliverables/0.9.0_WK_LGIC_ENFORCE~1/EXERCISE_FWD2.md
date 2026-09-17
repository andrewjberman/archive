# EXERCISE_FWD2 -- FWD-2 on a real resource (LGIC_ENFORCE EN-x-1)

Written by 0.9.0_WK_LGIC_ENFORCE~1 on LGIC_ENFORCE.TO-EN-x-1, base CLOUD @c6d652a6dc.

## What was done

**The resource.** On a practice copy (`git worktree add -b prac-lgic-enforce-x1 .worktrees/prac-lgic-enforce-x1 HEAD`),
`infra/aws/terraform/shared-infra/lgic-enforce-fwd2-resource.tf` declares ONE resource,
`aws_sqs_queue.lgic_enforce_fwd2`. Its `name` is `module.opal_name_lgic_enforce_fwd2.name`, a second instance of
`infra/aws/terraform/modules/opal_name` called with system `advi`, scope `49financial`, function `fwd2-exercise`
and kind `queue`. The module renders `advi-49f-fwd2-exercise-queue`. `lib/opal_naming.py grade()` reads that name
CONFORMANT as an `SQS_QUEUE`, and the same name comes out of `name("advi", "49financial", "fwd2-exercise", "queue")`.

**Why `advi`.** The issuer relayed Andrew's steer: LGIC aims at the MDPF, ADVI and IRPT pipelines, so the system
token comes from one of those, spelled as `infra/logic/registry/systems.json` spells it. The registry lists `mdpf`,
`advi` and `irpt`, and all three grade CONFORMANT with this scope, function and kind. `advi` was chosen because
`opal-data-49financial`, the bucket whose fence this exercise pairs the name with, is the ADVI pipeline's per-client
gold bucket (`infra/aws/terraform/shared-infra/s3-49financial.tf:1-6` @c6d652a6dc). An ADVI resource scoped to
49financial is therefore the pipeline that actually lives behind that fence. The firm is `49financial`, as the order says.

**The same row.** The fence in `s3-49financial.tf:118-123` @c6d652a6dc takes its principal pattern from
`module.opal_name.fence_patterns["49financial"]`. The queue takes its scope slot from
`module.opal_name_lgic_enforce_fwd2`'s `scope_short["49financial"]`. Both are rendered into
`modules/opal_name/generated_locals.tf` from the one `49financial` row of `infra/logic/registry/scopes.json`
(`"short": "49f"`): the pattern is `arn:aws:iam::313476888478:role/*-49f-*` and the name is
`advi-49f-fwd2-exercise-queue`.

**The plan (the `before` state).** `terraform init -input=false -lockfile=readonly -plugin-dir=<shared tree>/infra/aws/terraform/shared-infra/.terraform/providers`
ran against the real S3 backend. Every module source is local and the provider came from the local cache, so
nothing was downloaded. Then `plan -lock=false -input=false -out` (rc 0) and `show -json` (rc 0) ran from the practice
copy with `SAFE_APPLY_TERRAFORM=C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/terraform.exe` (Terraform v1.9.8).
`Plan: 7 to add, 0 to change, 0 to destroy.` Of 239 resource changes, 7 are not no-op. One is
`aws_sqs_queue.lgic_enforce_fwd2` create, name `advi-49f-fwd2-exercise-queue`. The other six are the three
fence-probe roles and their policies, which `lgic-enforce-fence-probes.tf` still declares at @c6d652a6dc; see row
LGIC_ENFORCE-W1-S20. **Nothing was applied**, and safe-apply was not run. The `.tf` was then committed on the scratch
branch: that commit is `before` (104f092d69).

## What could not be done: the `after` commit

Step 2 changes 49financial's short form in `scopes.json` (`49f` -> `f49`) and regenerates. On the practice copy that
one-line change was made. `python lib/opal_naming.py validate` then refused the registry, rc 1:

    REFUSED scopes.json[0].short: 'f49': NAMING_SCHEMA.json firm_forms gives '49f'
    VALIDATE: REFUSED 1 refusal(s), 9 warning(s)

`python lib/opal_naming.py generate --out ...` refused with the same cause, rc 1
(`ERROR: the registry is refused (1 refusal(s))`). The short form is pinned a second time, in
`org/standards/NAMING_SCHEMA.json:112-113` @c6d652a6dc (`"firm_forms": [ {"key": "49financial", "short": "49f"}`),
and `lib/opal_naming.py:287-288` refuses any `scopes.json` short that differs from it. That file is outside this
order's `<paths>`. So no regeneration could be produced and no `after` commit exists. The change was restored
byte-for-byte, the practice copy was left clean and removed with `git worktree remove`, and the scratch branch
`prac-lgic-enforce-x1` stays in place at 104f092d69. Row LGIC_ENFORCE-W1-S19 (BLOCKING, on X1-AC3) carries this.

`new_short` below is the short form the order asked for and the validator refused. `after` is null because no such
commit exists.

```json
{"resource": {"address": "aws_sqs_queue.lgic_enforce_fwd2", "name": "advi-49f-fwd2-exercise-queue"}, "plan_json": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/fwd2_plan.json", "registry_row": "49financial", "scratch_branch": "prac-lgic-enforce-x1", "commits": {"before": "104f092d691d38f059be0c26b46361e8d067f0db", "after": null}, "new_short": "f49"}
```
