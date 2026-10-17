# IB-hm-8 worker notes -- 0.9.0_WK_IRPT_BCKEND~454

Scope: declare (no apply) the HMAC list stage role, its two-statement policy, the secret CONTAINER, and three environment keys on the directory refresh Lambda. Files: `infra/aws/terraform/investor-reporting/directory/hmac_list_stage.tf` (new) and one additive edit to `schedule.tf`.

## What was written
- `hmac_list_stage.tf`: two `opal_name` module blocks (system irpt, function hmac-list-stage, kinds role and policy); a `locals` block with the secret name literal `irpt/hmac-list/key` (no builder, graded CONFORMANT per the IB-hm-3 file), the three list firms read from `data/firm_registry.json` (kind client, each also tested against `module.irpt_scopes` FIRM class), the list-key URI map built from the builder's `address()` pattern, and the stage role ARN built from the account id and the role module's name; one `aws_secretsmanager_secret` (container, no version, no value); a trust document naming only `local.irpt_runner_role_arn`; a policy with two statements, `ReadTheOneHmacSecretOnly` (secretsmanager:GetSecretValue on the secret's ARN) and `PutTheThreeFirmListKeysOnly` (s3:PutObject on the three object ARNs derived from the URI map); the role and the role policy.
- `schedule.tf`: three keys added after `IRPT_DIRECTORY_SOURCE_ROLE_MAP`: `IRPT_HMAC_SECRET_ID`, `IRPT_HMAC_ROLE_ARN`, `IRPT_HMAC_LIST_URI_MAP`. No existing key changed.

## Checks
- AC1: FAIL once (trust Sid counted as a third policy statement), then PASS twice after the Sid was removed from the trust document. Output in `IBhm8_criteria_output.txt`.
- AC2: PASS twice. The three URIs equal the builder results for `49financial`, `cottonwood`, `inflection`.
- AC3: not run before the commit by construction (reads HEAD~1..HEAD). Run after the commit; result in the worker report.
- `terraform fmt -check -diff`: NOT RUN. `.tools/terraform.exe` is absent from the worktree.
- No `terraform init`, `plan` or `apply`. No AWS call. No secret value or key material in any file. `grep`-equivalent check: no `aws_secretsmanager_secret_version` resource in the root (AC1 arm passes).

## Finding of step 6 (host side, read only, NOT edited)
The host role's identity policy in `infra/aws/terraform/mdpf-pipeline/iam.tf` already holds one `sts:AssumeRole` statement for the 49 Financial source principal, Sid `IrptDirectory49fAssumeSourcePrincipal`, at lines 659-664, with Resource `arn:aws:iam::${local.account_id}:role/${module.irpt_49f_directory_read_role_name.name}`. The new stage role has no equivalent statement anywhere, so a separate cell would need to add one (for example Sid `IrptHmacListStageAssumeRole`, Action `sts:AssumeRole`, Resource = the stage role ARN built from `module.irpt_hmac_list_stage_role_name.name`) to make the host's assume explicit; whether a permission boundary or SCP needs it is not measured here.

## Oddities and deviations (for the record)
1. The order said derive the firm tokens from `module.irpt_scopes`. Its FIRM class holds four rows, including `demo` (kind demo). The three list firms need the registry kind filter, so the file reads `data/firm_registry.json`. Surprise row `IRPT_BCKEND-D2-W454-S1`.
2. The trust document carries no Sid, because AC1 counts every Sid in the file. principal_49f.tf does carry one. Surprise row `IRPT_BCKEND-D2-W454-S2`.
3. My first read of the order file returned the whole file, including its RECORD FACE. I did not use the RECORD FACE content for any decision.
4. The apply will change the directory refresh Lambda's environment map in place; the plan's read of that change belongs to the apply order.
5. AC3 and the status flip: AC3 cannot pass before the commit, so the proof instance records AC3 as UNCOMPUTABLE-BY-CONSTRUCTION naming the post-commit run. The TO stays `pending` in this commit; the issuer's AC3 run decides the flip.
