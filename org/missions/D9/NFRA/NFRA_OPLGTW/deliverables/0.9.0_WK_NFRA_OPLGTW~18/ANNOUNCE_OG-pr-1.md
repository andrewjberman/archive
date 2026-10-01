# ANNOUNCE -- OG-pr-1 PHASE A (0.9.0_WK_NFRA_OPLGTW~18), no AWS write

## Files

| file | what |
|---|---|
| `infra/aws/terraform/opal-gateway/gateway-read-secrets.tf` | three metadata-only `data "aws_secretsmanager_secret"` blocks; ONE `aws_iam_role_policy.gw_gateway_read_secrets` named `${var.name}-gateway-read-secrets` on `aws_iam_role.gw.id`; one statement, `secretsmanager:GetSecretValue`, Resource = the three `.arn` references; no secret-version resource |
| `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~18/create_gateway_read_secrets.py` | boto3, us-east-1, creates the three secrets; values built in memory; prints only ARNs and pair counts; refuses (exit 2, nothing created) if any of the three names exists; `--dry-run` touches no AWS API |

## The three names and their grade()

| name | `lib/opal_naming.py grade(name, "SECRET")` |
|---|---|
| `gateway/transcripts/bearer` | CONFORMANT |
| `gateway/mail/bearer` | CONFORMANT |
| `gateway/principals/rosters` | CONFORMANT |

Bearers: `secrets.token_hex(32)` each. Rosters JSON `{"master_admin": "<tid>/<oid>", "write_capable": "<tid>/<oid>,..."}`
built from the Part D file: **roster pair counts master 1, write 2** (script `--dry-run`, 4 of 4 values GUID-shaped and
distinct). No value printed or written to a repo file.

## Readings

- `pr.AC1.sh` on the worktree: `secret data sources: 3`, `actions named: ['secretsmanager:GetSecretValue']`, `resource
  statements 1`, `RESULT: PASS`, exit 0.
- `comp-iam gaps`: Total 36 missing / 297 deny-present / 1 coverage-unknown / 3 resource-mismatch. None concerns
  `secretsmanager:GetSecretValue` on a gateway/* secret; the 3 `opal-gateway-role` rows are test-file S3 reads
  (`opal-mcp-audit`), unrelated to this order. The new grant is explicit, so it adds no gap.
- Plan: a plain or `-target` plan in the worktree stops first on two unset required variables
  (`mcportal_owner_key_claim`, `mcportal_owner_key`) and then on an untracked build artifact
  (`mcportal-grant-writer-deps.zip`); recorded as row `NFRA_OPLGTW-Z-W18-S1`. In a scratch mirror under `.scratch/planmirror`
  (placeholder variable values, dummy build files) the plan reached the EXPECTED refusal: three errors
  `reading Secrets Manager Secret (gateway/<name>): couldn't find resource`, one per new data source. This also reads
  that none of the three secrets exists today. `terraform plan` is read-only; `safe-apply` was not invoked (it gates
  `apply` only).

## Rollback per key

- Grant: remove `gateway-read-secrets.tf` (or the one role policy) and apply; the policy is separate from every core
  gateway grant.
- Secrets: `aws secretsmanager delete-secret --secret-id <name> --recovery-window-in-days 7` for each of the three
  names (restorable inside the window).

## Needed for PHASE B (see row W18-S1)

The targeted `safe-apply` must be fed the two required variable values and the `.build` artifacts; the issuer rules how.
