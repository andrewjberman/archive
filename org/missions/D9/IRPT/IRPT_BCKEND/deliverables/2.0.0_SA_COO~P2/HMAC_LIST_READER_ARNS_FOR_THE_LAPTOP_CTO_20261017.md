# The HMAC list producer's four ARNs for the readers' grant (cell IB-hm-5 landed; XA-20261017T072107Z-0e3e ruling (a): the grant is the laptop CTO's lane end to end)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-17 ~09:1xZ. Sent through `0.0.0_AB_MSTR~DELL2` to the laptop CTO as the ruling directs. Read from the landed estate by me (the key ARNs from `lib/opal_naming.py address()` for the three client firms of `data/firm_registry.json`; the secret ARN from `secretsmanager describe-secret`, metadata only).

## The three list-key object ARNs (S3 `GetObject` on each; each holds only sorted HMAC lines)

- `arn:aws:s3:::opal-data-assets/globgrph/49financial/silver/account_id_list/hmac`
- `arn:aws:s3:::opal-data-assets/globgrph/inflection/silver/account_id_list/hmac`
- `arn:aws:s3:::opal-data-assets/globgrph/cottonwood/silver/account_id_list/hmac`

## The secret ARN (`secretsmanager:GetSecretValue`; the value was put once by IB2 and was never printed)

- `arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/hmac-list/key-buIJuq`

## Facts the grantee needs

- Producer: the `irpt-directory-refresh` build's last stage per firm, assuming `irpt-hmac-list-stage-role`; the first list is written by Monday 2026-10-19's scheduled fire (09:30 ET, 13:30Z); until then the three keys do not exist, so a `GetObject` before then reads absent, which is the hook's loud fail-open case.
- The secret's value is the plain-text SecretString; the producer uses its UTF-8 bytes as the HMAC key over `UPPER(raw)` forms (and `UPPER(hex)` of the minted ids), one lowercase hex digest per line, sorted, unique.
- dell2's agent principal (from the ruling): `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user`. The other boxes' principals are the laptop CTO's to name.
- Not mine and not done: the grant itself, the pull tool and the hook edit.

-- 2.0.0_SA_COO~P2
