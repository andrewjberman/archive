# NEVER-WIDEN -- COO HALF, ADDENDUM 1 to the gold rebuild pair: widen the gold securities file 191 -> 212 (the 21 collector-universe names gold cannot carry today)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-01 ~12:1xZ. **Amends:** `round32/NEVER_WIDEN_HALF_COO_GOLD_REBUILD.md` @534a521e45
(CTO half @301f4321a8). **Pairs with:** `1.0.0_SA_CTO~Z`'s half of THIS addendum (owed).

## WHY

`HVST-af-3`'s census (row `Z-W90-S4`, drained @48ec92238a): 68 of 89 collector-universe names map to gold; the other 21
resolve through the estate crosswalk to canonical keys that the 191-row gold securities file
(`deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json`) does not carry, so gold can never show their depth
(FWD-14, Andrew's 50+/100+ bar): Adobe ADBE_US, Air Liquide AI_FP, Cadence CDNS_US, Celsius CELH_US, Clorox CLX_US,
Global Payments GPN_US, HEICO HEI_US, International Container Terminals ICT_PM, JD.com JD_US, MSCI MSCI_US, Manila
Electric MER_PM, Michelin ML_FP, MUFG 8306_JP, Nike NKE_US, Schlumberger SLB_US, Shopify SHOP_CN, SMFG 8316_JP,
Synopsys SNPS_US, Tokyo Electron 8035_JP, Tokio Marine 8766_JP, Zoetis ZTS_US.

**The file:** `round33/securities.universe.r33.json` = the 191 rows unchanged + 21 rows, each `key` / `security_key`
the CROSSWALK's canonical key (never synthesized), `company` and `aliases` from the collector universe row, `ticker`
the key's own form, `composite_figi` null, `ticker_aliases` empty. The act passes it as `HVST_GOLD_UNIVERSE`.

## THE WIDENED RULE (measured, 12:0xZ, 0 puts; `checks/gold_rebuild.signing.py` with `HVST_GOLD_UNIVERSE`)

- mention: 0 rows GONE; a previously served row may CHANGE only in `co_mention_count`, `co_mentioned_securities`,
  `is_roundup`, and only when its new `co_mentioned_securities` include one of the 21 added keys; any other change is a
  STOP. Measured: 885 changed, ALL in those fields (796 count+list, 89 count+list+is_roundup), ALL co-mentioning one of
  the 21; added 658 (292 for the 21 new names, 367 for existing names from silver since rebuild #1).
- daily: 0 rows GONE; changed rows only on securities with added mentions (OTHER 0) -- measured 1,190 changed, OTHER 0;
  added 5,754 (the 21 new securities' day rows + the as-of day).

The act script's VERIFY limb gains the co-mention allowance exactly as stated; everything else in the base half
(blast radius: 2 never-overwrite parts per rebuild; rollback: the BEFORE rows re-written as a newer part; up to 4
rebuilds to 2026-10-02 13:00Z) is unchanged.

## SERVED EFFECT, NAMED

The page can show 21 more names (their collected counts, from 0 upward as the backfill reaches them); 885 existing
mention rows list one more co-mentioned security. No count, tier, weight or score field of an existing row moves.

## VERDICT: SIGNED (COO), pending the CTO half of this addendum
