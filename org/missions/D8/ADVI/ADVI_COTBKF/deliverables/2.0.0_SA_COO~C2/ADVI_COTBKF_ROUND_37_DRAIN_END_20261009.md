# L8 drain end -- ADVI_COTBKF round 37

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~13:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB37ak1-AC2)

Round 37 was cut as one issuance @13d195e908 (`fanout: 1 of 1 chains, cap 8`) on the CTO's W64-S1 ruling. That ruling, made in the
CB-aj-2 CTO half @a614350d84 (msg 3346), says each bond is priced from Cottonwood's own custodian price, or else stays UNPRICED.

| order | item | worker | state |
|---|---|---|---|
| CB-ak-1 | does Cottonwood's own data carry a custodian price for the three bonds | ~65 | complete @3c00ecf3c3 (rule commit b4764d4fa0 first), drained @2e3b52b23b |

## The real run, shared tree, after the drain

```
BOND-CUSTODIAN-PRICE bonds=3 custodian_reported=0 trade_only=1 none=2
```

The issuer's run matches the worker's.

## What the round found

| CUSIP | class | detail |
|---|---|---|
| 95000U2D4 (Wells Fargo 4.15% 2029) | `trade_only` | one `by` row on 2022-06-08 (qty 25,000, amount 25,156.69 -> 1.006268 per unit); 1 of 988 held account-days covered; 0 position rows |
| 05613L3H2 (BNP Paribas) | `none` | 0 held days, 0 rows in any source |
| 651639AX4 (Newmont 2.8% 2029) | `none` | 0 held days, 0 rows in any source |

- **All 988 held account-days belong to the Wells Fargo bond** (2022-06-08 .. 2026-05-15). BNP Paribas and Newmont are held by no
  Cottonwood account in the Commonwealth delivery. Their 49F rows sat in Cottonwood's price store with no Cottonwood holder.
- **By the CTO's source order, all three stay UNPRICED** (`NO_FIRM_OWNED_SOURCE`). The one trade price is a single trade-date print,
  not a custodian-reported series.
- Sources checked:
  - Commonwealth silver transactions: 1,416,497 rows.
  - Commonwealth silver positions: 469 rows.
  - cot silver canonical prices: 11,291,021 rows, 0 keyed by these CUSIPs.
  - cot gold holdings: 133 objects, 1,515,703 rows.

**One finding for the CTO (unmeasured, not ruled here).**
- The cot GOLD holdings carry 86 rows for the Wells Fargo bond labelled `bd_snapshot`, dated 2026-06-08 .. 2026-10-08. The worker's
  rule excluded them by the `bd` token.
- Cottonwood's own pipeline is a Black Diamond session (`cot-bd-session-daily-et`, `BD_FIRM_ID=cottonwood` in `ssm.tf`). So `bd_` on a
  cot gold row may name the Black Diamond PLATFORM serving Cottonwood's own accounts, not the separate bd firm.
- If so, these rows are Cottonwood's custodian-reported price, but only from 2026-06-08. That is after the held window ends
  (2026-05-15), so they cover none of the 988 days either way.
- The label ambiguity itself (`bd_` = platform or firm) is the open question for the cross-firm guard.

**Disclosure (row W65-S1).** Run 1 missed the vendor buy code `by`, and the worker widened the code list. The rule text is unchanged
and run 2 is recorded. The worker also corrected the order's own assumption that the 988 days spread across three bonds.

**Rows:** W65-S1 (INERT). ARMED: 0.

**Round-close check:** REFUSED until CB37ak1-AC2 is graded.
