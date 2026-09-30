# IB-pr-213 -- edge role reads only public keys (row S132)

**Worker:** 0.9.0_WK_IRPT_BCKEND~69, worktree `C:/Users/AndrewBerman/Desktop/wk-irpt-p-69`, branch `wk-IRPT_BCKEND-69`.

## What was found

`aws_iam_role_policy.lambda_edge_secrets_logs` (`infra/aws/terraform/portal-auth/iam.tf`) granted
`secretsmanager:GetSecretValue` on the bare wildcard `arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:opal/auth/*`,
which covers every secret under that prefix including the two PRIVATE signing keys
(`opal/auth/jwt-private-key`, `opal/auth/irpt-render-jwt-private-key`).

Confirmed by direct read (native Grep, not comp-find, per the comp-tool rail) that the edge code reads exactly
two secret ids, both public keys:
- `JWT_PUBLIC_KEY_SECRET_ID = 'opal/auth/jwt-public-key'` -- `infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs:57`
  (imported by `infra/aws/lambda-edge/auth-validator-edge/index.mjs:78`)
- `RENDER_PUBLIC_KEY_SECRET_ID = "opal/auth/irpt-render-jwt-public-key"` -- `infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs:38`

No third secret id and no `private` name appears in `infra/aws/lambda-edge/auth-validator-edge/*.mjs`. The refusal
clause (edge code reading a secret beyond these two) does not fire.

## Build

Narrowed the `Resource` of the `GetSecretValue` statement to a two-element list, one ARN per public key, each with
the `-*` suffix (Secrets Manager's 6-character ARN suffix):

```
Resource = [
  "arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:opal/auth/jwt-public-key-*",
  "arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:opal/auth/irpt-render-jwt-public-key-*"
]
```

Every other statement in the file is untouched in substance. `terraform fmt` was run on the whole file per the
order's instruction and reformatted indentation on an unrelated pre-existing comment block (statement 1 of
`aws_iam_role_policy.auth_permissions`, whitespace only, no semantic change) -- expected fallout of running fmt on
the file rather than a hand-scoped diff.

## Plan (no apply)

`.tools/terraform.exe` does not exist in this worker's worktree (untracked binary, present only in the main
worktree -- filed as row `IRPT_BCKEND-W69-S1`). Substituted the winget-installed system `terraform.exe` on PATH.
`.terraform/` state was also absent (worktrees do not carry it); ran `terraform init -lock=false` first (read-only
backend/provider setup, no resource write), then:

```
terraform plan -lock=false -target=aws_iam_role_policy.lambda_edge_secrets_logs -no-color
```

Result: `Plan: 0 to add, 1 to change, 0 to destroy.` -- the single named resource,
`aws_iam_role_policy.lambda_edge_secrets_logs`, updated in-place:

```
  ~ resource "aws_iam_role_policy" "lambda_edge_secrets_logs" {
        id          = "lambda-edge-execution-role:lambda-edge-secrets-logs"
        name        = "lambda-edge-secrets-logs"
      ~ policy      = jsonencode(
          ~ {
              ~ Statement = [
                  ~ {
                      ~ Resource = "arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/*" -> [
                          + "arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/jwt-public-key-*",
                          + "arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/irpt-render-jwt-public-key-*",
                        ]
                        # (2 unchanged attributes hidden)
                    },
                    ...unchanged logs statement...
                ]
            }
        )
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

An un-targeted full plan in the same root (run only to corroborate "ONE in-place update") shows a SECOND,
pre-existing, unrelated drift on `aws_wafv2_web_acl.opal_cloudfront_protection` -- filed as row `IRPT_BCKEND-W69-S2`,
out of this cell's `<paths>`, not touched.

No `apply` was run at any point (per BOUNDS).

## Acceptance

`P21-3-AC1` -- ran `python "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r21/p21_3_ac1_edge_policy_source.py" .`:

```
edge reads ['irpt-render-jwt-public-key', 'jwt-public-key'] | GetSecretValue resources 2 ['arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:opal/auth/jwt-public-key-*', 'arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:opal/auth/irpt-render-jwt-public-key-*']
P21-3-AC1 PASS
```

## Surprises filed

- `IRPT_BCKEND-W69-S1` -- `.tools/terraform.exe` absent from this worker worktree; substituted PATH terraform for
  fmt/init/plan (never apply). OBSERVATION, ARMED (future worker on a fresh worktree hits the same absence),
  disarm_owner `2.0.0_SA_COO~P`.
- `IRPT_BCKEND-W69-S2` -- pre-existing, unrelated WAF drift (`aws_wafv2_web_acl.opal_cloudfront_protection`) surfaced
  by the corroborating full plan. OBSERVATION, INERT, carried for the portal-auth drift owner.
