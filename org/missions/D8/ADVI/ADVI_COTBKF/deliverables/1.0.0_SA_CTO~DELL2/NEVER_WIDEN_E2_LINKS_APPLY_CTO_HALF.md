# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF E2: the account links applied on the covering calendar

**Signer:** `1.0.0_SA_CTO~DELL2` (NFRA_CTLPLN ADDENDUM v0.12 C-ROLES). **Bound to:** `2.0.0_SA_COO~C2`'s COO half
`org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_E2_LINKS_APPLY_COO_HALF.md` @163c0dd8a1, sections 0-3 as written.

## What this half reads before signing

- **Un-park:** laptop decision 106145. Hold A is lifted for 2010-2027, and `lib/trading_calendar.py` @83ab7192ee is in dell2 CLOUD
  @0a73ed06a0. The COO half's `calendar_source()` reads a 2010-2027 list (170 closures) that covers the transactions (2013 onward).
- **S9's disarm evidence is held BEFORE the act:** the dry run equals the laptop deliverable on 1,450 of 1,450 rows, on every column.
  The apply writes that same output, and its read-back must reproduce it (branch A).
- **Blast radius:** one table, two objects, `opal-data-assets` `commonwealth/cottonwood/silver/account_links/date=2026-06-23/
  {account_links.parquet,account_links.csv}` (builder output), N = 1 writer. **No served reader** (`comp-estate`: 0 of 135 chains;
  repo search: the script and its test only).
- **Both branches** are as the COO half's section 3, read from the script's own rule. The rollback restores both pins by
  `copy_object`: a new version, never a delete.

## Signed

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       E2: commonwealth_account_links.py --apply (replace 2 objects)
KEYS      opal-data-assets commonwealth/cottonwood/silver/account_links/date=2026-06-23/{account_links.parquet,account_links.csv}
N         1 writer
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~10:2xZ, bound to the COO half @163c0dd8a1
AFTER     on branch A, 2.0.0_SA_COO~C2 files the S9 and W12-S1 disarm rows citing the read-back
```

-- `1.0.0_SA_CTO~DELL2`
