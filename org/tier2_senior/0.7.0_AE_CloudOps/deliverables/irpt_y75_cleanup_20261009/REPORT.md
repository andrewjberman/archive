# IRPT Y75 release-5b cleanup result — Amendment 1

The pinned cleanup denominator was exactly seven `irpt-requests` keys and two `opal-data-irpt` keys.

The mandatory readback gate reran from keys file v2 at `b2603a97c0` before the first delete and returned:

- `body_sha256_match`: `true`
- `owner_is_advisor`: `null`
- `acting_principal_is_filer`: `true`

The owner object has no email field, so Amendment 1 required an immediate stop. The result records only its field names (`advisor_id`, `firm_id`, `ownership_fingerprint`, `principal_class`, `principal_id`, `schema_version`) and the non-personal firm label. The runner issued zero DDB delete calls and zero S3 delete calls. The cleanup result contains an empty `results` array. The sweep was not run because it follows the delete gate; its stored value is the no-op placeholder `0` and is not a claim that the wider tenant contains no matching rows.

No raw identity value was written or printed. The email-shaped-string count across the files written for this run is zero. The Amendment 1 ledger is closed as a refused no-op with no world mutation.
