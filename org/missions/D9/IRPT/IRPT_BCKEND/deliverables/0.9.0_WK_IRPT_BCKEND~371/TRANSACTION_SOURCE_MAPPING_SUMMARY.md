# IB-pr-524 -- transaction sources of Cottonwood and Inflection mapped to account_activity_daily (READ ONLY)

Base: `3296b89477` (HEAD before the first commit). Record: [IB187-2_transaction_source_mapping.json](file:///C:/dev/wk-IRPT_BCKEND-371/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~371/IB187-2_transaction_source_mapping.json).

## The shape (19 columns)

Read from `ARROW_ACTIVITY` in [account_activity_lots.py](file:///C:/dev/wk-IRPT_BCKEND-371/data/assets/scripts/gold/irpt_reporting/account_activity_lots.py): firm, account_id, business_date, beginning_value, contributions, withdrawals, realized, unrealized_change, income, income_gross, income_fee_admin, income_withheld_tax, inkind_departure_gain, ending_value, identity_gap, rounding_allowance, method_version, coverage, schema_version.

The 49F source is one custody entry in [sources.json](file:///C:/dev/wk-IRPT_BCKEND-371/data/assets/scripts/gold/irpt_reporting/sources.json). The producer refuses any count other than one ([compute_local](file:///C:/dev/wk-IRPT_BCKEND-371/data/assets/scripts/gold/irpt_reporting/account_activity_lots.py), line 1040), and so does the [handler](file:///C:/dev/wk-IRPT_BCKEND-371/infra/aws/lambda/investor-reporting/reporting-gold/handler.py), line 222.

## Cottonwood (Black Diamond): can_produce_shape YES, 0 ABSENT

- Landed transactions: silver `fact_transactions`, 123 date partitions, 2026-03-09 to 2026-10-13. The legacy flat history holds the same 123 days.
- Lot tables: `fact_realized` (121 partitions) and `fact_unrealized` (143). Holdings: `fact_holdings` (92), the balance analogue.
- Columns come from `mirror_schemas.py` DECLARED: transactions 68 names, realized 15, unrealized 14, holdings 21.
- Mapped: AccountID, Income. The rest are derived. Withholding is the A_05 pair Expense x Tax Withholding. In-kind is Transfer In or Out with units.

## Inflection (Orion): can_produce_shape PARTIAL, 2 ABSENT

- Landed transactions: silver `fact_transactions`, 145 partitions, 2026-05-12 to 2026-10-13.
- The legacy flat history starts 2020-05-26 with 1656 files. This is a second span, recorded as a surprise row.
- ABSENT: `realized` (no lot feed in the Orion DECLARED set) and `inkind_departure_gain` (no in-kind type, no lot table).
- Derived from the transTypeId dictionary in [convert_transactions_to_silver.py](file:///C:/dev/wk-IRPT_BCKEND-371/data/inf/scripts/silver/convert_transactions_to_silver.py), lines 221-272. Balances come from `fact_positions` (`currentValue`, `costBasis`).

## Not measured

Value signs, vocabularies as data, and any row values. Account key spaces (the 49F key is padded to 10, Black Diamond carries a z09 prefix, Orion is int64). No object body and no row count was read.

## First cell a producer build needs

A custody declaration per firm (`sources.json` has only the 49F entry). It needs the silver transaction and lot prefixes from `address()`, plus the column names above. The producer reads one source today, so the first build is the multi-source read.

## Surprise rows (IRPT_BCKEND-D2-W371-S1 to S4)

Filed in [INVESTIGATION_v1.md](file:///C:/dev/wk-IRPT_BCKEND-371/org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md). They cover the Inflection span, the key spaces, the missing Orion lot feed, and the two Orion writers.
