# AMGT-ii-3 PRE-ACT RECORD (0.9.0_WK_AMGT_RESAPP~336), taken 2026-10-09T11:3xZ, before any write

Pair read whole: COO half sha256 06255d9e14cb3f4aa83315c825203f81e8928c605030c49a94af61eca7c3c362 ; CTO half sha256 5fa2cc6e4272c3de812cccc519b5e03ab7b0edf725680a7aab189b31f91972c4
(org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND84_II3_{COO,CTO}_HALF.md).

CONDITION 1 (import check printed): `py -3.12 -c "import lib.research.filings.fetch, lib.research.filings.analyze, anthropic"` -> IMPORT-OK rc=0 (worktree C:/tmp/r84-336 @40d7df6702); anthropic 0.84.0.

CONDITION 8 (in-process fetch.build_source_object on the cached filing, no network, no write; cond8.py):
- BABA_US_Equity status RESOLVED language en parser 2.0.0 item_keys [business, risk, mdna] -> OK
- SAP_GY_Equity  status RESOLVED language en parser 2.0.0 item_keys [business, risk, mdna] -> OK
- PBR_US_Equity  status RESOLVED language en parser 2.0.0 item_keys [business, risk, mdna] -> OK
r84_language.py --crit AC1: 5 of 5 en, L2 negative control pt, YES.

CONDITION 10: `r83_pbr.py --crit AC1 --starts-only` -> P1-P4 PASS, R83 PBR AC1: YES (PBR business 'Exploration & Production' 58,860 chars; risk 69,278; mdna 'Consolidated Financial Performance' 42,490).

## Silver (ONE shared prefix, 7 parts) -- full rows in pre_silver_rows.txt
Prior (current) silver row per name, record_hash[:12]:
- BABA 3556dca9d0de (acc 000119312526231755), current via part-20261009T094719Z VersionId BIX9bZWdJ1pdURXj.rVrvUzuVsm59Uvl (round 83's rollback re-append; same content as the 09-22 part's row)
- SAP  37a6a4576da9 (acc 000110465926020058), 09-22 part (VersionId LyJe2lp_G2j7W9NNxTHAdK30iNs3le79), parser 1.0.0
- PBR  81bc74bf096a (acc 000129281426002168), 09-22 part, parser 1.0.0

## Per name prior VersionIds (latest) and attempt-state
| name | analysis VersionId | drafting VersionId | attempt-state key |
|---|---|---|---|
| BABA_US_Equity | yIcDOS4HT5Q6_gLfUt0lbYCj90Qm1tPR (2026-10-09T09:47:17Z, 286275 B; = round-83 rollback of DmJ7NkDk) | qUdrTs_2twkBesSoTueePYoDsVGcWite (2026-10-09T09:47:17Z, 116539 B; = rollback of VFL1upyK) | ABSENT (0 versions) |
| SAP_GY_Equity | rmP1ek8s2AVOO.IMhvmk_3Snqx6vI3zF (2026-09-17T02:32:05Z, 252798 B) | qb9GzRTF0E9_nend.L7Sc_W0d_4b5BTR (2026-09-30T19:48:28Z, 88518 B) | ABSENT (0 versions) |
| PBR_US_Equity | olR02tlq3ciXsCxp43HMXRR_8vOxGWkx (2026-09-17T02:29:52Z, 237900 B) | ZmdJB1hRO43_wa4IUJSwiNbMlVdsH0hn (2026-09-30T19:48:28Z, 100899 B) | ABSENT (0 versions) |

Full four-prefix listings (key, VersionId, LastModified, size, IsLatest) are pre_<KEY>.json beside this file (list_prefixes.py). Prefixes per name:
sec/harvest/silver/filing_source/ ; filings/v1/<KEY>/ ; drafting/v1/<KEY>. ; amgt/harvest/state/filing_attempt/security_key=<KEY>/.
filings/v1/<KEY>/ also holds a legacy <acc>.source.json; a new write there is inside the prefix and is reported as a diff line.
