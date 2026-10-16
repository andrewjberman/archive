# TCKT_MTADTA TO-MD-r2 item 2 -- what Andrew runs (prepared by 0.7.0_AE_CloudOps~TM1, 2026-10-16)

**WAITING ON ANDREW: consent.** Nothing below has been run by the seat. No tenant id, client id or token appears in this file.

## What was read first (both dry runs, 2026-10-16)
- `python data/m365_metadata/scripts/app/register_app.py` printed: one application `m365-metadata-trino-collector`, single tenant (`AzureADMyOrg`), ONE permission (`Office 365 Management APIs` / `ActivityFeed.Read` / `Role`), `graph_permissions` empty, secret id `m365-metadata/trino/api-credentials`. No call made.
- `python data/m365_metadata/scripts/app/start_subscriptions.py` printed three calls: `Audit.Exchange`, `Audit.SharePoint`, `Audit.General`. No `Audit.AzureActiveDirectory`. No call made.
- The credential container `m365-metadata/trino/api-credentials` and the key container `m365-metadata/trino/subject-key` exist with NO value (describe-secret shows no version).

## Which AWS identity
Run it as **`Andrew_Berman`** with his own AWS credentials (check first: `aws sts get-caller-identity --query Arn --output text` must end `user/Andrew_Berman`). Measured: `iam simulate-principal-policy` for `secretsmanager:PutSecretValue` on that one secret reads `allowed` for him (he is in `AdministratorAccessOpalCapital`); the secret has no resource policy. The script writes the secret JSON `{tenant_id, client_id, client_secret}` itself, so the secret value never passes through any seat.

## The commands (Git Bash, from the repository root)
1. Unified audit logging must be on (RUNBOOK step 1). In Exchange Online PowerShell: `Get-AdminAuditLogConfig | Select UnifiedAuditLogIngestionEnabled` must read `True`. If it reads `False`, stop and tell the issuer.
2. Your Graph token and tenant, in this shell only (one way to get them; any delegated Graph token of a Cloud Application Administrator works, and the seat did not test this route):
   `az login`
   `export M365_TENANT_ID="$(az account show --query tenantId -o tsv)"`
   `export M365_DELEGATED_TOKEN="$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv)"`
3. `python data/m365_metadata/scripts/app/register_app.py --apply`. It prints the application (client) id and the admin-consent URL; it never prints the secret.
4. Open the consent URL and grant admin consent yourself (Cloud Application Administrator). No other seat does this.
5. `unset M365_DELEGATED_TOKEN`, then tell `2.0.0_SA_COO~S1` you have consented. The seat then confirms `r2_check_r2.py app`, writes the subject key, starts the three subscriptions and waits for two scheduled fires.

## For your later read through the door (MFA session)
The group's invoke now needs `aws:MultiFactorAuthPresent`. Your device serials are `mfa/Andrew_Phone` and `mfa/Yang_Phone` (see surprise row D1-S9). With the six-digit code from your device:
`aws sts get-session-token --serial-number arn:aws:iam::313476888478:mfa/Andrew_Phone --token-code <code>`
then in the shell that will run the door script set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` from the `Credentials` block it returns (boto3 reads all three) and unset `AWS_PROFILE`. The session is temporary (12 hours by default).
