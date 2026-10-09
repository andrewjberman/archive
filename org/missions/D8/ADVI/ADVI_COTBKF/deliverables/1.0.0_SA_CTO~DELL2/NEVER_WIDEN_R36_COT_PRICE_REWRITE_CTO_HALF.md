# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-aj-2: rewrite 38 cot price keys without the 49F rows

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~13:2xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 3342
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R36_COT_PRICE_REWRITE_COO_HALF.md`, **blob b280844d80**
(commit 2f2f1e52aa). Ruling it executes: ADDENDUM 10 @6d764d8db2 (REWRITE, not delete).

## Read

- **38 keys get one new version each.** Every prior version is kept, and nothing is deleted. Rollback is a copy of each prior VersionId.
- **1,734 rows are removed and 0 re-priced.** `other_rows_identical=True` on 38/38, and the schema is equal.
- **Writers of `silver/prices/`: 7 in code, 0 scheduled.** The one cot writer runs only on a manual silver-prep. The cot code mirror in the bucket is BLIND.
- **The bonds branch is taken: the three bonds go UNPRICED.** No price is better than another firm's price: a 49F row in Cottonwood's store is the cross-firm
  NEVER itself, so leaving the rows "until a source exists" keeps the breach live. The FWD-3 serve already holds them (988 account-days).

## Blast radius the COO half does not name -- condition 3 closes it

The cot gold chain reads the latest version. Its next run moves Cottonwood's gold values for the three bonds. This half covers that move only as stated in condition 3.

## Conditions

1. **The applier re-reads each prior VersionId immediately before its write,** and any change means STOP. It applies the files as built, with each sha256 printed
   against the manifest and no rebuild. `0.7.0_AE_CloudOps~CB2` is the applier (@5ff94852a6). The ledger is pinned and committed per leg.
2. **Before the first write, the cot code mirror (`code/gold/` in `opal-data-cot`) is read, one object at a time.** Any writer of `silver/prices/`, or any reader of
   another firm's price input, means STOP. The BLIND is closed in the ledger.
3. **Before the first write, the ledger cites the gold chain's code line that values a holding with no price on a date.**
   - If it marks the holding missing, NaN or excluded with a reason: proceed. The ledger names the count of gold account-days the next run moves for the three bonds.
   - If it values the holding at 0, or carries a stale price forward without a flag: STOP. That is a served-output change this half does not cover.
4. **The next manual silver-prep is read for the three CUSIPs.** 0 rows from any 49F input must hold. A re-injection reopens D2-S52 as BLOCKING.
5. **Old-version deletes stay Andrew's act.** They are not part of this pair.

## RULING on row W64-S1 (the bonds' price source)

- **Source order:**
  1. Cottonwood's OWN custodian-reported price for the bond, from the cot tree, carrying a basis field (`custodian_reported`);
  2. otherwise the bond stays UNPRICED, with reason `NO_FIRM_OWNED_SOURCE`.
- **Never another firm's price, and never a non-bond-specific proxy.**
- One measurement cell in the next round reads whether the cot tree carries such a price for 05613L3H2, 95000U2D4 and 651639AX4. A hit re-enters them as their own
  delta under its own pair.

**Verdict: GIVEN**, for the 38 keys exactly, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~13:4xZ, `~C2` msg 3380-ish and `~CB2`, row D2-S60 @f550170df0): condition 2's reading -- GO

**Condition 2 reaches only a writer BEYOND this half's own census.** The census already names the one cot writer, `build_canonical_prices_v2.py`, which runs only on
a manual silver-prep. Reading the condition literally would refuse the act this half signs.

**Measured by `~CB2`:**
- 107 mirror objects were read one at a time. Exactly 1 writer was found, and it is the named builder's deployed copy. Scheduled writers: 0. Readers of another firm's
  prices: 0.
- **The BLIND is CLOSED.** Condition 2 is MET, and D2-S60 is disarmed by this amendment.

**Condition 3 is MET in the ledger (leg C2):**
- `B_00.canonical_holdings.py`:689/702 gives NaN on a price miss, and there is no `fillna(0)` on price or market_value.
- The next gold run moves 99 account-days on one account (95000U2D4) to NaN, about 2.46M of market value withdrawn. That is the whole move, and it is covered.

**One hazard is surfaced, and it is NOT this act's: `_ff_worker` (:1339-1378).** It is an UNFLAGGED stale-price carry-forward.
- It is unreachable for cot today, measured: `schwab/silver/rps/` is empty, against a positive control.
- If that prefix ever fills, it would carry the removed bond prices forward with no claim field.
- **COTBKF enrichment item (with ADDENDUM 11.2's cell):** the carry-forward stamps `price_basis: carried_forward` and the source date on every row it fills, or it
  skips any asset whose last price came from a non-firm source. It is a code change under COTBKF's own pair, not a rider on this rewrite.

**GO: `~CB2` writes the 38 keys now** under conditions 1, 4 and 5.

-- 1.0.0_SA_CTO~DELL2
