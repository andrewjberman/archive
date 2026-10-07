# ACTIVITY_LOTS_LOCAL_RUN -- IRPT_DASHBD.TO-DB-b-35 (counts only)

Local run of `account_activity_lots.py` (method_version 1). S3 reads only; nothing written to S3. Record: `ACTIVITY_LOTS_LOCAL_RUN.json`.

| Quantity | Count | Note |
|---|---|---|
| trading days | 24 | 2026-09-01 .. 2026-10-05 |
| accounts in the sample | 100 | the named account plus 99 drawn (seeded) from a population of 7597 |
| account_activity_daily rows | 2182 |  |
| account_lot_realized rows | 726 |  |
| account_lot_unrealized_daily rows | 160549 |  |
| activity rows: MEASURED | 2161 | identity inside the rounding allowance |
| activity rows: GAP_ABOVE_ALLOWANCE | 20 | across 8 accounts |
| activity rows: NO_PRIOR_VALUE | 1 |  |
| activity rows: NO_LOTS / LOT_PARTITION_ABSENT | 0 | none on live data; both reached by test |
| reconciliation: account-windows tied term by term | 1 | the one named account; 7 terms printed by DB23-1-AC1 |
| sampled account-windows graded | 91 |  |
| sampled account-windows within one cent | 52 |  |
| sampled account-windows above one cent | 39 | reported in the record, never plugged |
| realized lots in the window | 726 |  |
| realized lots tied to their closing transaction | 726 |  |
| realized lots untied | 0 | reasons: none on live data |
| negative control: same lots against no transactions, untied | 726 | all NO_TRADE_FOR_ORDER |
| realized-lot partitions read (RLD vintage) | 24 | one partition per custodian day, 2026-09-01 .. 2026-10-05 |
| pre-2010 realized lots listed | 86 | dates kept, holding_trading_days null |
| pre-2010 open lots listed (sample) | 94 | first-seen rows deduplicated by lot |
| pre-2010 open lots on the end day, all accounts | 1282 | count only |
| builder-output rows | 3 | 3 addresses, 0 names (the cell creates no resource) |
