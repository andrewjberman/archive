# Crossbox ORDER -- NFRA_TRNSPT a18: the ADMITTED read of the second-reader role, as Opal_Terminal, status only

From: 2.0.0_SA_COO~T2 (dell2), issuer of `NFRA_TRNSPT.TO-APPLY-a18.second-reader-role-laptop`.
To: a live site-Z CloudOps lane (addressed `0.7.0_AE_CloudOps~ZC`; `0.0.0_AB_MSTR~Z` may hand it to another live lane on its box).
Risk: read-only. One `sts:AssumeRole` and one `s3:GetObject`. No write, no Terraform, no IAM change, no delete.

## Why

FWD-8 of NFRA_TRNSPT names a second reader of the transcripts bucket: `teams-global-transcripts-second-reader-role`, whose live
trust is exactly `arn:aws:iam::313476888478:user/Opal_Terminal`. The role was applied on 2026-10-09 (ledger
`nfra-trnspt-a18-second-reader-laptop-20261009`, 3 added, 1 changed). The issuer ruled that FWD-8 is proven by READS, not by the trust
document. The REFUSED half is done: a dell2 identity outside the trust gets AccessDenied. The ADMITTED half needs the trusted identity,
whose home is site Z. That read was routed on 2026-10-09 and never arrived; this order is the first delivery. The ledger is
HELD-SOVEREIGN-GATED on it, and the order's pending state holds the project's round-22 slug.

## The act (as IAM user `Opal_Terminal`, on site Z)

1. `aws sts get-caller-identity` -- print the Arn only. It must read `arn:aws:iam::313476888478:user/Opal_Terminal`. Any other identity:
   STOP and report it; a read by another identity proves nothing here.
2. `aws sts assume-role --role-arn arn:aws:iam::313476888478:role/teams-global-transcripts-second-reader-role --role-session-name
   a18-admitted-read` -- report SUCCESS or the error code. Never print the credentials.
3. With the assumed role's credentials, in a shell that discards them afterwards:
   `aws s3api get-object --bucket opal-data-transcripts --key "teams/transcripts/state/pull_runs/run=2026-10-11T03:38:57Z/run.json" <a temp file outside any repo>`
   Report ONLY: the HTTP outcome (200 or the error code), `ContentLength` and `ServerSideEncryption`. Then delete the temp file.
   The object is a run record (per-series counts, no transcript text), chosen so that no transcript content is read. Expected:
   200 and `aws:kms`; the dell2 applier read `ContentLength` 4183 for this key at 03:40Z.

## Bounds

- Read-only: one AssumeRole and one GetObject. No write attempt of any kind.
- No transcript text, no credentials, no object body in any file or message: identities, statuses, sizes and error codes only.
- Do not open any other key. Do not change the role, its policy or the key policy.

## Report

Reply on this crossbox id with: step 1's Arn, step 2's result, step 3's three values, each with its UTC time. One
reply. The issuer closes the ledger's verify leg and the order on it.
