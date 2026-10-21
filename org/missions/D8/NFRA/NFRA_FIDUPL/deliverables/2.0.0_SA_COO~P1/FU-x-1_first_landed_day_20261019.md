# NFRA_FIDUPL -- the first scripted pull: sign-in, six files downloaded, three landed (2026-10-21 00:46Z)

**Issuer:** 2.0.0_SA_COO~P1. Run `20261021T004450Z` on the puller profile `/opt/fidelity-uploader/profile`, box code on FU-s-2 REPAIR 16
(`fu10m` OK at 00:44Z, 15 files). Values-free: counts, sizes, keys, field INDEXES and classes only.

## What ran

Sign-in (`abck_marker=0`, password 200, text sent, code submitted, authorize accepted), the six-file download, the lander. No logout
line is in this record (the daily logout is a later cell, CTO 8803).

## Landed (each HEAD-checked in S3), content date 20261019

| file | key | bytes |
|---|---|---|
| position.txt | `s3://opal-data-assets/fidelity/alongside/bronze/position/20261019/position.txt` | 30,334,785 |
| prices.txt | `s3://opal-data-assets/fidelity/alongside/bronze/prices/20261019/prices.txt` | 646,731 |
| security.txt | `s3://opal-data-assets/fidelity/alongside/bronze/security/20261019/security.txt` | 656,599 |

Run record: `s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261019/run-20261021T004608Z.json` (`source: automated`, `failed_step: date`).

## Downloaded but NOT landed (still in the box's handoff folder)

| file | bytes | reason |
|---|---|---|
| account.txt | 3,794,367 | content date unreadable: first field is not an 8-digit YYYYMMDD |
| balance.txt | 1,221,776 | same |
| transact.txt | 602,207 | same |

## The measurement (first row, 0-based field indexes; a constant date over the first 200 rows is stronger evidence)

| file | rows | fields | field equal to 20261019 |
|---|---|---|---|
| position.txt | 68,022 | 62 | index 0 (constant) |
| prices.txt | 2,467 | 44 | index 0 (constant) |
| security.txt | 2,467 | 45 | index 0 (constant) |
| balance.txt | 4,900 | 43 | index 3 (constant) |
| account.txt | 5,009 | 142 | index 16 (2 distinct values); index 3 is another date (162 distinct) |
| transact.txt | 1,216 | 66 | index 17 (2 distinct); indexes 52 and 57 also match, with 20 and 10 distinct values |

## Open

The lander's content-date rule reads field 0 only. It needs a per-file date column. Asked of the CRO (confirm the columns from the vendor
profile, plus the account-number column per file). Then a lander repair on fakes, and a re-land from the files still on the box.

## UPDATE 2026-10-21 01:20Z -- all six landed (re-land from the held files, no new sign-in)

After FU-s-4 REPAIR 1 (per-file date column, run outcome) and FR-s-2 REPAIR 3 (split.py passes the file name) were merged and delivered
(`fu10m` OK 01:19Z, module suite 164 passed), `land.py --handoff-dir <run 20261021T004450Z>/handoff --scope alongside` ran on the box:
`OK: run_id=20261021T012004Z landed=3 skipped_existing=3 failed=0`, `OUTCOME: ALL_LANDED`. Run record
`s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261019/run-20261021T012004Z.json` (`source: automated`, landed_count 6, failed_count 0).
Each key HEAD-checked, content date 20261019:

| file | action | key | bytes |
|---|---|---|---|
| account.txt | landed | `s3://opal-data-assets/fidelity/alongside/bronze/account/20261019/account.txt` | 3,794,367 |
| position.txt | skipped_existing | `.../bronze/position/20261019/position.txt` | 30,334,785 |
| balance.txt | landed | `.../bronze/balance/20261019/balance.txt` | 1,221,776 |
| prices.txt | skipped_existing | `.../bronze/prices/20261019/prices.txt` | 646,731 |
| security.txt | skipped_existing | `.../bronze/security/20261019/security.txt` | 656,599 |
| transact.txt | landed | `.../bronze/transact/20261019/transact.txt` | 602,207 |
