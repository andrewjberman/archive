# AMGT-hh-4 PRE-ACT RECORD (0.9.0_WK_AMGT_RESAPP~332), taken 2026-10-09T09:3xZ, before any write

Pair read whole: COO half sha256 e3c859ee5e2019ebcd4c9ac0727a37467b58226abbe7b953d1daa42ad542e6db ; CTO half sha256 e20ba4924cba0d71eca72740d488afc9691389f4a9b38c2e3d8982c7c944440b
(org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND83_HH4_{COO,CTO}_HALF.md).

CONDITION 1 (printed before step 1): `py -3.12 -c "import lib.research.filings.fetch, lib.research.filings.analyze"` -> IMPORT-OK rc=0 (worktree C:/tmp/r83-332 @277a451b25); anthropic 0.84.0.

r82_cut.py --crit AC1 (in-process, no write, --cache .scratch/r82_20f): ASML business=OK(91976) risk=OK(53968) mdna=OK(31578); 15 of 15; R82 CUT AC1: YES rc=0.

PBR_US_Equity HELD by the GO: no fetch, no write, nothing for PBR (not listed, not touched).

## Silver (ONE shared prefix, 3 parts) -- full rows in pre_silver_rows.txt
- 2026-09-22/part-20260922T033157Z.parquet  VersionId LyJe2lp_G2j7W9NNxTHAdK30iNs3le79  (808344 B, 13 rows; parser 1.0.0 rows for the four names)
- 2026-10-09/part-20261009T082333Z.parquet  VersionId k3bWqFRPQhvTephepe01vjYL0sPgTcky  (88598 B, 1 row: ASML parser 2.0.0, fetched 08:23:33Z, round 82's superseded row)
- 2026-10-09/part-20261009T082927Z.parquet  VersionId OCszrAitD5iLteDPEju6_3jpSm0H2fQs  (45084 B, 1 row: ASML prior row re-carried, parser 1.0.0, record_hash 8e8b3f33bb3d, fetched 08:29:27Z) -- ASML's CURRENT silver row.
Prior (current) silver row per name, record_hash[:12]: ASML 8e8b3f33bb3d (acc 000162828026011378, via the 082927Z part) ; BABA 3556dca9d0de (acc 000119312526231755) ; NU ddc31a976dd1 (acc 000129281426002166) ; SAP 37a6a4576da9 (acc 000110465926020058); the last three in the 09-22 part, parser 1.0.0.

## Per name prior VersionIds (latest) and attempt-state
| name | analysis VersionId | drafting VersionId | attempt-state key |
|---|---|---|---|
| ASML_NA_Equity | j8Na7vbstyVwylNkvcd.6qlvoITHieEF (2026-10-09T08:29:26Z, 93121 B) | iaClXu9ZJUkDAuxNqZleFTdx9ZVGio2R (2026-10-09T08:29:26Z, 13503 B) | EXISTS UNRESOLVED-SOURCE.json XCTQo1uW9rvomS3k12_BqMRLq4EFm81B (2026-10-09T06:20:48Z, 2338 B) |
| BABA_US_Equity | DmJ7NkDkRBbfQdX6DSA7KDsY1W.uEfVJ (2026-09-17T02:15:50Z, 286275 B) | VFL1upyKN4FJHsLUl4CbYX88uK04IACp (2026-09-30T19:48:26Z, 116539 B) | ABSENT (0 versions) |
| NU_US_Equity | 9TdrmvW.Tu6wyqOiby9bXSODRvSiHCEW (2026-09-17T02:27:44Z, 385571 B) | IOc9Qbp8uD5tBnmaW5nfsTr6dKxK9SH0 (2026-09-30T19:48:28Z, 103452 B) | ABSENT (0 versions) |
| SAP_GY_Equity | rmP1ek8s2AVOO.IMhvmk_3Snqx6vI3zF (2026-09-17T02:32:05Z, 252798 B) | qb9GzRTF0E9_nend.L7Sc_W0d_4b5BTR (2026-09-30T19:48:28Z, 88518 B) | ABSENT (0 versions) |

Full four-prefix listings (key, VersionId, LastModified, size, IsLatest) are pre_<KEY>.json beside this file (list_prefixes.py). Prefixes per name:
sec/harvest/silver/filing_source/ ; filings/v1/<KEY>/ ; drafting/v1/<KEY>. ; amgt/harvest/state/filing_attempt/security_key=<KEY>/.
filings/v1/<KEY>/ also holds a legacy <acc>.source.json (old grammar, VersionIds in the listings); a new write there is inside the prefix and is reported as a diff line.
