# IRPT Y75 release-5b cleanup result — Amendment 2

The pinned cleanup denominator was exactly seven `irpt-requests` keys and two `opal-data-irpt` keys.

The mandatory readback gate ran from keys file v3 at `4bcebfcb09` before the first delete and returned:

- `body_sha256_match`: `true`
- `owner_is_advisor`: `true`
- `acting_principal_is_filer`: `true`

The three owner subchecks (`firm`, `principal_class`, and derived `label`) were also all `true`. The comparison ran in memory and emitted no identity value.

All seven named `irpt-requests` rows existed before deletion and read `NOT_FOUND` afterward. Both named S3 object versions existed before deletion and read `NOT_FOUND` afterward. An independent readback returned `DDB_LEFT=0` and `VERSIONS_LEFT=0`. The bounded tenant sweep found zero extra rows.

No raw identity value was written or printed. The email-shaped-string count across the files written for this run is zero. Ledger `irpt-y75-amend2-cleanup-laptop-20261009` is closed with every leg proven.
