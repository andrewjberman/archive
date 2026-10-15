# CB-ci-4 -- rule R4 (name to household, then the fingerprint inside it, within the window)

Full record: `R4_RECORD.json` in this folder. Links: `C:/dev/_cotbkf_match_20261015/R4_LINKS.csv` (outside the repository, 110 rows, sha256 `9f8f8abb9eef1311c46b8f9590e71e16c96d42c0b3a2c93f0f5afdbfbad5973e`). Counts only; no name, token or hash of one is in this file.

| Stage | Result |
|---|---|
| Control: matched accounts run with their own link hidden (471) | 358 unique household; 353 right, 5 wrong; 2 multi; 111 no hit |
| Control: DETERMINISTIC | 341, right 341, wrong 0 (guard not applied) |
| Control: CANDIDATE / NONE | 13 / 117 |
| Derived window (471 served pairs) | band +/-14 days about median -14 (lo -28, hi 0), 96.6% inside |
| Real: unmatched accounts (1,062) | no household 836; multi 0; via name 137; via client_line 89 |
| Real: tier | DETERMINISTIC 11; CANDIDATE 99; NONE 952 |
| Yield over the 219 reachable | DETERMINISTIC 10 (11 active); CANDIDATE 85 (98 active) |

Against the research: the control reaches 358 households, not 138 (0 wrong), so the household stage is not reproduced
(5 wrong). The real run reaches 94 households (137 accounts) by name, against 59. The client-line route reaches 89 accounts,
34 of which touch a reachable account, against 39, and yields no CANDIDATE. Surprise rows ADVI_COTBKF-D1-W175-S1 to S4.

Names: read in memory, keyed-hashed under a per-run salt that was never stored; scratch holding values was deleted.
