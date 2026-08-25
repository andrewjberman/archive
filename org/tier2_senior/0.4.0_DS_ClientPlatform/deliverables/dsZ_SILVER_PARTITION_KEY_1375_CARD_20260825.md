# `:1375` — THE SILVER PARTITION KEY IS THE OPERATION CLOCK

**Author:** `0.4.0_DS_ClientPlatform~Z` (site Z) · **Carded:** 2026-08-25T02:20Z
**File:** `infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:1375`
**Status:** OPEN — **NOT for tonight.** Real defect, non-urgent, order-dependent.

---

## THE DEFECT

```python
:1375  f"{SILVER_ROOT}{S3_HOLDINGS_PREFIX}/{run_date}.parquet"
:1293  run_date = event.get("run_date") or now.date().isoformat()
```

The silver holdings partition is named for **the day the Lambda ran**, not the day the data is
as-of. Andrew, 2026-08-24 ~23:0xZ, verbatim:

> *"it is fine to track metadata of when we've updated data or performed operations on it, but that
> is a very different figure than the actual data 'as of' provenance timestamp."*

Every downstream consumer treats the filename as the provenance stamp — `resolve_as_of` in
`etf_positioning_gold.py` selects partitions by it. **It is correct only when the capture day equals
the data day**, which is why it has never been visible. Finding: `1.0.0_SA_CTO~Z` (msg 6917), root
cause pinned by `0.7.0_AE_CloudOps~Z`.

## ⛔ WHY IT WAS **NOT** FIXED ON 2026-08-25 — THREE MEASURED REASONS

### 1. It could not have delivered the item it was dispatched for
```
bbg/ prefixes existing 02:16Z:      bbg/2026-08-20/   bbg/2026-08-21/     <- NO 08-24
silver/holdings/2026-08-24.parquet: EXISTS, 21,073 B, 187 rows, all four funds
```
Gold needs **both** sides at one as-of. Silver was already at 08-24; the absent side was **bbg**.
No value written at `:1375` can create `bbg/2026-08-24/`. And because `run_date` **equalled** the
provider date that night, a derived key would have resolved to `2026-08-24` — *the name it already
had*. A live-data change over 73 partitions producing a byte-identical outcome.

### 2. The obvious form is not writable — `data_as_of` is multi-valued per partition
```
silver/holdings/2026-08-24.parquet   data_as_of:
   2026-08-24  114 rows  (pfde, pfoe)
   2026-08-21   73 rows  (divz, idvz)
   DISTINCT VALUES IN ONE FILE: 2
```
`data_as_of` is a **per-row** field the per-fund-as-of ruling explicitly permits to differ by fund.
One file cannot take two names. **Any re-key must first declare a rule for the multi-valued case** —
that rule is the deliverable, not the keystroke.

### 3. ⛔ ORDER-DEPENDENT, AND THE DISPATCHED ORDER IS THE HARMFUL ONE
Found by `3.0.0_SA_CVO~Z` (msg 7056): applying `:1375` **before** the as-of value fix propagates
would **split** the 187-row partition, sending 73 TrueShares rows into a partition named
`2026-08-21` — **a date their data is not from.** That manufactures the exact
right-looking-data-under-the-wrong-date defect the Z-S31 guard exists to refuse.

## THE SAFE ORDER

1. **TO-7 as-of fix** — DEPLOYED 2026-08-25T00:09:54Z. TrueShares rows now take the sheet's own
   `Date`. ✅
2. **Confirm a full scheduled partition is single-valued** on `data_as_of`. *(Predicted single-valued
   post-fix — `2.0.0_SA_COO~Z` measured both TrueShares captures same-day-stamped, **n=1**. Not
   established.)*
3. **Then** re-key, with a declared rule for the multi-valued case that step 2 may still surface.

## ⭐ AND THE FIX MAY BELONG AT THE READER, NOT HERE

A partition **named for the run** is an honest *operation* stamp — which is precisely what Andrew
said is fine to track. The defect is that `resolve_as_of` **reads that name as provenance**. The
filename is not lying; the reader is asking it a question it never claimed to answer.

That points the remedy at the **consumer**: select on the per-row `data_as_of` **column** (correct
since TO-7) rather than on the **filename**. Blast radius: one selector, versus a naming convention
73 historical partitions follow and which interacts with the `(date, key)` dedup.

**This fork is unresolved and belongs to `1.0.0_SA_CTO~Z`.** It is the third instance in one night of
one field serving two intents (Rule 24(iii)) — after `is_cash` (skip-the-pull vs render-as-class) and
`run_date` (partition key vs provenance stamp).

## RELATED, SAME NIGHT

- **Z-S31** — the `run_date` fabrication guard, `@e692db801c`, committed and **not deployed**;
  hazard armed on the running bytes.
- **Z-S35/36** — `@0c03c359f2`, the `is_cash` intent split; deploy stopped by its author over three
  aggregations keying the raw flag, block later lifted (no display harm measured).
- **The 04:00Z L1 re-run** — scheduled at exactly local midnight (UTC-4). Measured margin: **zero
  seconds**; a fire at 03:59Z resolves as-of `2026-08-21` again.
