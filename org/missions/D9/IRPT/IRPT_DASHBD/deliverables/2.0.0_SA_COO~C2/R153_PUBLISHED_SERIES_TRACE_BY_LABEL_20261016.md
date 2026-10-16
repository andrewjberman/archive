# Published-series trace for the three named clients, by LABEL -- 2.0.0_SA_COO~C2, 2026-10-16 ~22:0xZ

Asked by CTO msgs 9754 and 9817; ids supplied by `2.0.0_SA_COO~D2` by broker under `XA-20261016T213506Z-8db5` (RULED yes) and `RULING_9794_TRACE_ACCOUNT_IDS_20261016.md`. Conditions kept: no account id in this file, a commit, a message or a surprise row; labels only; each id used only against its own firm's prefix; read-only S3 `get`/`list`. Claim word: MEASURED unless marked.

| label | published? | days | first / last day | history scope | unreported trading days | income | optional class keys |
|---|---|---|---|---|---|---|---|
| cottonwood-client-1, account 1 | yes (manifest and series present) | 61 | 2026-07-10 / 2026-10-14 | PARTIAL_HISTORY | 3 (2026-08-19, 2026-09-24, 2026-09-25) | claim `absent` | none of class_value, class_weight, class_names |
| cottonwood-client-1, account 2 | yes | 61 | 2026-07-10 / 2026-10-14 | PARTIAL_HISTORY | the same 3 | claim `absent` | none |
| 49financial-client-1 (BEYER, traced earlier today) | yes | 257 | 2025-10-08 / 2026-10-15 | FULL (the constant PARTIAL at `account_return_daily.py:1355` was replaced by `~D2`'s derivation) | stated per series | n/a here | none (0 of 6,954 series) |
| inflection-client-1, accounts 1 and 2 | NO: `irpt/inflection/platinum/` holds `holdings/` and `holdings_qa/` only; `reporting/` returns 0 objects; the two directory ids match 0 of 1,110 keys under `platinum/` | 0 | none | none | none | none | none |

## What it says

- **Cottonwood:** both accounts are served. The data starts 2026-07-10 (`first_data_date` equals the first series day), so the page's "where the data starts" and the three-day unreported sentence both have real inputs; `calendar_source` is `fallback_2010_2027` (the fallback calendar). A client that still shows empty on the Performance tab after DB-b-309 is NOT explained by absence in the series.
- **Inflection:** the empty Performance series is the measured, expected PATH A state: the firm publishes holdings but no reporting series. The Performance tab must say so in words (worded absent), not stay blank; that is covered by the DB-b-309 template worded states and `~D2`'s panel cells.
- **49 Financial:** unchanged from the earlier trace: the empty page Andrew saw was the Global refusal, not absence.

## Instrument notes (so the numbers carry their limits)

- Cottonwood published series are keyed `account=z<custodian>/`; the directory's `acc_...` ids match 0 of 1,878 published objects and 0 of 1,004 `account_dim` rows, so the mapping needed `~D2`'s handler (`_published_map`); I did not re-derive it. The custodian forms came from `~D2` (msg 9922) and were used only here, in memory.
- Counts are over the full listing (Cottonwood 1,878 objects over 2 pages; Inflection platinum 1,110 objects), not a first page. The Inflection zero is a prefix read of the one `reporting/` path `~D2` also read; a zero there says "no object under that prefix", and the sibling `platinum/` listing is the control that the bucket was reachable (1,110 objects).
- Vintage: series as_of 2026-10-14 (Cottonwood), 2026-10-15 (49 Financial); read 2026-10-16.
