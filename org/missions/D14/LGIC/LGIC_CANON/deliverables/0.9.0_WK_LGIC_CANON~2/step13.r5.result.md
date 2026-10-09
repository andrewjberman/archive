# LGIC_CANON.TO-CN-q-1 -- step 13 re-run, registry rows (0.9.0_WK_LGIC_CANON~2, 2026-10-09)

Practice wave: `workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/contract.json`, 184 rows, 184 names
(`node_type` + `current.name.value`), run through `python lib/opal_naming.py census --names FILE` with no card file.

## Before

`census --names` rc=3: `CENSUS: STOPPED on the first RAISE after 5 judged (0 carded, ruled=0): names S3Key 'blackdiamond/49f/session-trigger-mode.json'`.
To meet every RAISE at once (the census stops on the first), `grade()` was called on all 184 names: **9 RAISE** (8 S3Key, 1 IAM_ROLE).

## Every RAISE met, and the row added for it

All nine rows are in `infra/logic/registry/name_rulings.json` (rows #119 to #127 (0-based, as the census prints them), appended; no existing row changed).
Why not `key_rulings.json`: the census reads only `name_rulings.json`, keyed (name, type), and a `--names` line has no bucket; see surprise row
`LGIC_CANON-D1-W2-S1`.

| # | type | name | RAISE | row added | what the repository says |
|---|------|------|-------|-----------|--------------------------|
| 1 | S3Key | `blackdiamond/49f/session-trigger-mode.json` | K3: not a tier | canonical `blackdiamond/49financial/state/session-trigger-mode.json` | copied from the `key_rulings.json` row for (opal-data-bd, this key); `grade()` of the canonical reads CONFORMANT |
| 2 | S3Key | `config/ticker_lookup.json` | K1: `config` is neither a source nor a tier | none_owed | copied from the `key_rulings.json` row (reference table; tier decided when ADVI_FIRMBKTS moves opal-data-bd) |
| 3 | S3Key | `config/yahoo_safe_tickers.txt` | K1 | none_owed | `docs/architecture/ADVI_TICKID_PRICING_DIVERGENCE_ADDENDUM.md:51,77,126` -- a ticker reference list, same class as row 2; bucket not read |
| 4 | S3Key | `platinum/advisors/{*}/positions.json` | K4a: `{*}` is not an entity partition | none_owed | `exec-summary-generator/exec_summary/template_library.py:75-76` builds the key for a read; `trigger_eval.py:11` marks it future; no writer found |
| 5 | S3Key | `platinum/clients/{*}/concentration.json` | K4a | none_owed | served by `opal-partners-data/lambda_function.py:1450-1456`; routed by `shared-advisor-router/index.mjs:37` |
| 6 | S3Key | `platinum/clients/{*}/mix_timeseries.json` | K4a | none_owed | `lambda_function.py:1439-1446`; `index.mjs:37` |
| 7 | S3Key | `platinum/clients/{*}/summary.json` | K4a | none_owed | `lambda_function.py:1424-1436` (PII, through the Lambda); `index.mjs:33` (S3-direct blocked) |
| 8 | S3Key | `platinum/clients/{*}/views.json` | K4a | none_owed | no reader or writer found in infra or lib; only the contract row R-0130 records it |
| 9 | IAM_ROLE | `planted-system-without-a-row-49financial-ingest-role` | R1.f: `planted` in no vocabulary | none_owed | contract row R-0184: planted fictional name, "not claimed to exist in AWS"; adding `planted` to `systems.json` would invent a system |

For rows 4 to 8 the answer is none_owed, not a canonical address: the `{*}` is a run-time id, the partition form would change a key that served pages read by exact
key (a served-output act), and no file in the repository decides the new spelling or bucket. No address was invented.

## After

`python lib/opal_naming.py census --names <the 184 names>`: rc=0, last line:

`CENSUS: COMPLETE 175 judged + 0 carded + 9 ruled (live 0+0+0 of 0 nameable, repo 0+0+0 of 0) ruled=9`

0 `CENSUS RAISE` lines. `python -m pytest lib/tests -q -p no:cacheprovider`: 199 passed, 1 skipped (the base's count).

## AMENDMENT 1 (2026-10-09, issuer 2.0.0_SA_COO~B1): planted row removed

Row 9 above (IAM_ROLE `planted-system-without-a-row-49financial-ingest-role`, contract row R-0184, evidence instrument `planted (no instrument reaches a fictional name)`)
was REMOVED from `infra/logic/registry/name_rulings.json` under AMENDMENT 1: a plant is fictional by construction and the registry carries no row for it.
Step 13's population now excludes the wave's self-declared plants (183 names). The other 8 rows (S3Key) stand unchanged. The final run's last line is in the
proof instance (Q1R5-AC1), re-run after this commit.
