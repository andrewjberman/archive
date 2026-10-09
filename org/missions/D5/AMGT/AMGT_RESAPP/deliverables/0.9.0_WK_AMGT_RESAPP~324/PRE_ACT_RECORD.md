# AMGT-gg-2 PRE-ACT RECORD (0.9.0_WK_AMGT_RESAPP~324), taken 2026-10-09T08:2xZ, before any write

Pair read whole: COO half sha256 70015ac8cd24fc6a1665dbd85fd82c089a0b199d902dd988309505a7250a8f68 ; CTO half sha256 b0ba6f4b2a89b7c7d1832a0b9bb11068b50e556b5d1b73cf6634ad3a6b519a6f (org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND82_GG2_{COO,CTO}_HALF.md).

Condition 1: `py -3.12 -c "import lib.research.filings.fetch, lib.research.filings.analyze"` -> IMPORT-OK rc=0 (2026-10-09T08:18:38Z, worktree C:/tmp/r82-324 @dd762dcdb4); anthropic 0.84.0.
r82_cut.py --crit AC1 (in-process, no write, --cache = base checkout .scratch/r82_20f): ASML business=OK(91976) risk=OK(53968) mdna=OK(31578); 15 of 15; R82 CUT AC1: YES rc=0.

Prior silver (ONE shared part): sec/harvest/silver/filing_source/date=2026-09-22/part-20260922T033157Z.parquet VersionId LyJe2lp_G2j7W9NNxTHAdK30iNs3le79, 808344 B, 13 rows.
Prior silver row record_hash (matches round 81 prior_silver_rows.json sha256 b5f97a30093e..., rows verified equal by record_hash):
 ASML 8e8b3f33bb3d (acc 000162828026011378) ; BABA 3556dca9d0de (acc 000119312526231755) ; NU ddc31a976dd1 (acc 000129281426002166) ; SAP 37a6a4576da9 (acc 000110465926020058); all fetched_at 2026-09-22T03:31:57.788873Z, parser 1.0.0.

Per name prior VersionIds (latest):
| name | analysis key | analysis VersionId | drafting VersionId | attempt-state key |
|---|---|---|---|---|
| ASML_NA_Equity | filings/v1/ASML_NA_Equity/000162828026011378.analysis.json | WIU.oSeIh8NKMhy2DfqsJmRwGOusYTxs (2026-09-30T05:27:33Z, 93121 B) | FWeloN5.zr6pvN1NWUXScK5RakjwF1qV (2026-10-05T23:43:38Z, 13503 B) | EXISTS UNRESOLVED-SOURCE.json XCTQo1uW9rvomS3k12_BqMRLq4EFm81B (2026-10-09T06:20:48Z, 2338 B) |
| BABA_US_Equity | filings/v1/BABA_US_Equity/000119312526231755.analysis.json | DmJ7NkDkRBbfQdX6DSA7KDsY1W.uEfVJ (2026-09-17T02:15:50Z, 286275 B) | VFL1upyKN4FJHsLUl4CbYX88uK04IACp (2026-09-30T19:48:26Z, 116539 B) | ABSENT (0 versions) |
| NU_US_Equity | filings/v1/NU_US_Equity/000129281426002166.analysis.json | 9TdrmvW.Tu6wyqOiby9bXSODRvSiHCEW (2026-09-17T02:27:44Z, 385571 B) | IOc9Qbp8uD5tBnmaW5nfsTr6dKxK9SH0 (2026-09-30T19:48:28Z, 103452 B) | ABSENT (0 versions) |
| SAP_GY_Equity | filings/v1/SAP_GY_Equity/000110465926020058.analysis.json | rmP1ek8s2AVOO.IMhvmk_3Snqx6vI3zF (2026-09-17T02:32:05Z, 252798 B) | qb9GzRTF0E9_nend.L7Sc_W0d_4b5BTR (2026-09-30T19:48:28Z, 88518 B) | ABSENT (0 versions) |

Full four-prefix listings (key, VersionId, LastModified, size, IsLatest) are in pre_<KEY>.json beside this file. The silver prefix is shared by all names (one part today).
Listing prefixes per name: sec/harvest/silver/filing_source/ ; filings/v1/<KEY>/ ; drafting/v1/<KEY>. ; amgt/harvest/state/filing_attempt/security_key=<KEY>/.
Note: filings/v1/<KEY>/ also holds legacy <acc>.source.json objects (old grammar; analyze.write_outputs and fetch.persist no longer write it -- AMGT-rk-91). A new write there would be inside the prefix but unnamed; it will be reported as a diff line.
