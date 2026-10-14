# IB-pr-526 -- holdings the IR cash rule would move, per firm (READ ONLY)

Base: 9f41eeeec9 (worker branch wk-IRPT_BCKEND-373). Record: IB188-2_holdings_class_count.json.
Source: each firm's newest ACCEPTED publication (current/manifest.json latest_date, then the v2 manifest and
its partition objects, each sha256-verified), counted in memory. Counts only; nothing written to AWS.

| firm | newest served date | SECURITY nodes | cash sub-class | already cash | would move (upper bound) | moving public tickers |
|---|---|---|---|---|---|---|
| 49financial | 2026-10-12 | 124,441 | 33 | 1 | 32 | SNOXX, SNSXX, SNVXX, SWVXX |
| cottonwood | 2026-10-08 | 15,455 | 257 | 4 | 253 | FDRXX, SWVXX, VUSXX (plus 206 Black Diamond-prefixed identifiers, withheld) |
| inflection | 2026-10-12 | 34,273 | 843 | 2 | 841 | FDRXX, SPAXX |

Canonical table (etf-classifications, scanned by the worker identity): 11,361 rows, 365 with sub_asset_class cash.

What the build cell needs to know:
1. would_move is an UPPER BOUND. The rule acts only on the canonical branch, but the served basis TABLE is also
   written by the bd-securities fallback (holdings_snapshot.py 983 and _classifier_basis 931-932). The snapshot
   does not separate the two branches. Fallback movers (basis NAME_ALIAS, unchanged by the rule): cottonwood 215,
   inflection 67, 49financial 0.
2. Money-market names with no canonical row stay fixed_income (bd_securities_fallback.py 54-55, 152-153): the
   rule does not change that layer.
3. Inflection's 67 and cottonwood's 9 cash-sub-class movers have no ticker-shaped display symbol; they are counted,
   not listed.
4. cottonwood's newest accepted date is 2026-10-08; the other two are 2026-10-12.
5. Not read: any canonical row per ticker, the fallback table, any holding value.

Rows filed: IRPT_BCKEND-D2-W373-S1 (basis not a canonical discriminant) and S2 (the worker identity can scan the
canonical table, which D2's grant did not expect) and S3 (cottonwood date gap).
