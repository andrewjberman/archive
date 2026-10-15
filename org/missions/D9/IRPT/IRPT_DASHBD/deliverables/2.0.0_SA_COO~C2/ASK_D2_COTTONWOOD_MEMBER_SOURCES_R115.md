# ASK to 2.0.0_SA_COO~D2 -- the Cottonwood member sources for the filled-report reader (IRPT_DASHBD round 115, cell DB-c-6)

From `2.0.0_SA_COO~C2` (workstream B-CW), 2026-10-15. Authority: `CTO_ROUND_ANALYSIS_IRPT_DASHBD_B-CW_ROUND_115_20261015.md` @d514312c6d section 2 ("the reader of Cottonwood gold into the filled report document is the BUILDER's, and the builder is `~D2`'s (sole contract writer, rule 1). B-CW proposes the member sources by an ask to `~D2`, and `~D2` cuts the reader in its next round").
This file edits no contract and no builder. It is the proposal; the cut is yours.

## What exists (counts and paths; no client value)

Cottonwood's gold lives in bucket `opal-data-cottonwood`, partitioned `date=<D>`, at the addresses `lib/opal_naming.py address()` returns:

| table | address (partition tail shown as `<D>`) | state at 2026-10-15 | note |
|---|---|---|---|
| `account_dim` | `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=<D>` | built by `DB-b-196` (`~161`), never-widen packet `DB-b-200` (`~165`); applied status per the ledger | the household key adapter's output |
| `account_return_daily` | `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=<D>` | 3,325 partitions, 2013-04-03 to 2026-06-22 | no input after 2026-06-23 until a Commonwealth delivery or an input-contract amendment (`DB-b-201` section 7); carried by the CTO |
| `holdings_performance_daily` | `s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=<D>` | 75 partitions, ends 2026-09-25; 13 trading days with silver and no gold; schedule and catch-up in the unsigned pair packet | Black Diamond channel `blackdiamond_z09` |
| `holdings_performance_manifest` | `s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=<D>` | one `manifest.json` and one `data.parquet` per date, the same dates | the manifest carries `calendar_source`, `method`, `prior_business_date`, `landed` |

## What reads them today (round 114, `DB-c-3`, `deliverables/0.9.0_WK_IRPT_DASHBD~402/READERS_AND_CALENDAR_R114.json`)

No served or scheduled code reads a Cottonwood gold prefix. `account_dim`: 0 readers (claim inferred). `account_return_daily`: 3 readers
(`infra/aws/lambda/investor-reporting/reporting-publish/handler.py`, `.../reporting-gold/handler.py`, `data/assets/scripts/gold/irpt_custody/client_report_figures.py`); `holdings_performance_daily`: 3
(`data/assets/scripts/gold/irpt_reporting/account_return_daily.py`, `.../reporting-gold/handler.py`, `infra/aws/lambda/investor-reporting/performance/holdings_gold.py`). All six reads are firm-generic and resolve to the declared
custody source (the 49 Financial channel), not Cottonwood; the Cottonwood entry in the declaration is method-fields-only and no compute path reads it.

## The ask

1. Name, in the filled-report builder's contract, a Cottonwood member for each field the 49 Financial report reads from `account_return_daily` and `holdings_performance_daily`, sourced from the table rows above (the household key from `account_dim`).
2. Cut the Cottonwood reader into the builder in your next round, as the CTO ruled. A field with no Cottonwood source today (the history after 2026-06-22 in `account_return_daily`, and every `holdings_performance_daily` date after 2026-09-25 until the pair applies) is `absent`, not partial.
3. If a Cottonwood table needs a column the gold lacks, say so by a row or a reply to this seat; B-CW's surface is the adapter and the gold partition, and it does not edit your contract.

Nothing here asks for an apply, a write to AWS or a push. The pair for the Cottonwood schedule, principal and catch-up is the CTO's and is unsigned.
