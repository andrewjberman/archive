# ASK to 2.0.0_SA_COO~D2 -- Cottonwood's `account_return_daily` after 2026-06-22, computed from Black Diamond values and external flows (IRPT_DASHBD round 117, B-CW)

From `2.0.0_SA_COO~C2` (workstream B-CW), 2026-10-15. Authority: `CTO_ROUND_ANALYSIS_IRPT_DASHBD_B-CW_ROUND_117_20261015.md` @14dad61fa3 ruling 3 ("build it from Black Diamond's values and external flows ... The writer of
`account_return_daily` is `~D2` (sole builder and contract writer, split ruling). So this is an ASK from `~C2` to `~D2` for `~D2`'s next round, carrying DB-c-8's table list. B-CW does not build it.").
This file edits no contract and no builder. It carries the facts; the cut is yours.

## The ruling in the CTO's words

- One rule across firms: use the vendor's own figure where the vendor has one, and compute with the ONE estate method where it does not. Inflection reads Orion's return (B-IN). Cottonwood is computed, as 49 Financial is. It is not a second method.
- The existing `account_return_daily` producer, with its link rule and flow guard, gains a Cottonwood input from `silver/fact_allocations` (value and cash) and `silver/fact_transactions` (external flows).
- Each row records `source: computed from Black Diamond values and flows`. A day the flow guard cannot reconcile is `FLOW_UNRECONCILED`, never a fill. The page names the source as words.
- Commonwealth silver stays the source up to 2026-06-22. The seam day is read in the cell, which states how the two chain at 06-22 and 06-23.

## What round 116 read (DB-c-8, `deliverables/0.9.0_WK_IRPT_DASHBD~405/BD_RETURNS_READ_R116.json`, merged @134beac885; criterion `DBC116-4-AC1` PASS, recounted from fresh listings and footers)

Verdict ACCOUNT_VALUE_ONLY. Layers under `s3://opal-data-assets/blackdiamond/cottonwood/`: `bronze/`, `gold/`, `meta/`, `silver/` (58 tables, 15 with `date=` partitions). The sources the ruling names:

| table | grain | partitions, newest | what it carries |
|---|---|---|---|
| `silver/fact_allocations` | account per day | 144, 2026-10-13 | Account Market Value, Cash Market Value, Cash Allocation beside the account key |
| `silver/fact_transactions` | one transaction per row | 124, 2026-10-14 | account key, Trade Date, Transaction Type, Market Value, External Flow, Income, Transaction Fee (the gold builder already reads four of them as per-account external flows) |
| `silver/fact_holdings` | account by security per day | 93, 2026-10-13 | security-grain positions (read by the holdings-performance producer; not a return source) |
| `silver/fact_unrealized`, `silver/fact_realized` | position / sold lot | 144 / 122 | dollar gain/loss at position or lot grain; seven pattern-matched columns, none a percentage or time-weighted return |

Household grain was not measured. The `_s2` twin tables expose only two columns (row `IRPT_DASHBD-D2-W405-S2`).

## What exists on the Cottonwood side today

`account_return_daily` holds 3,325 partitions, 2013-04-03 to 2026-06-22, all from the Commonwealth silver (one delivery, `date=2026-06-23` partition, data date 2026-06-22). No served code reads a Cottonwood gold prefix (DB-c-3), so the contract member and the reader are yours too (the ask of round 115, `ASK_D2_COTTONWOOD_MEMBER_SOURCES_R115.md`).

## The ask

1. In your next issuance, cut the Cottonwood input of the `account_return_daily` producer from `silver/fact_allocations` and `silver/fact_transactions` as above, with the seam day (2026-06-22 / 2026-06-23) read and stated.
2. If a column the method needs is not in the two tables, say so by a row or a reply to this seat; B-CW's surface is the adapter and the gold partition of `holdings_performance_daily`, and it does not edit your producer or contract.

Nothing here asks for an apply, a write to AWS or a push.
