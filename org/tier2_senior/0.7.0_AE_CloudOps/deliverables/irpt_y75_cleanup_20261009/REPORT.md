# IRPT Y75 release-5b cleanup result

The pinned cleanup denominator was exactly seven `irpt-requests` keys and two `opal-data-irpt` keys.

The mandatory readback gate ran before the first delete and returned:

- `body_sha256_match`: `true`
- `owner_is_advisor`: `false`
- `acting_principal_is_filer`: `true`

Because one boolean was false, the runner stopped immediately. It issued zero DDB delete calls and zero S3 delete calls. The cleanup result contains an empty `results` array. The sweep was not run because it follows the delete gate; its stored value is the no-op placeholder `0` and is not a claim that the wider tenant contains no matching rows.

No raw identity value was written or printed. The email-shaped-string count across the files written for this run is zero. Ledger `irpt-y75-release5b-cleanup-laptop-20261009` is closed as a refused no-op with no world mutation.
