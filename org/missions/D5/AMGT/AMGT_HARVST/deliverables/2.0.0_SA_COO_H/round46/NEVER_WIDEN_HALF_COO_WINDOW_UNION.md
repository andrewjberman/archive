# NEVER-WIDEN -- COO HALF: `chatter_window` over the rank universe UNION RESAPP's covered set (round 46 HVST-as-2)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-05 ~01:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:**
- round-45 analysis @4f01f5ab8d, ruling 2 and enrichment item 2;
- RESAPP round-67 analysis @2db6fd3e3d, ruling 2;
- decomposition section 59.

## WHAT THIS HALF SIGNS: A BUILT DIGEST AND THE RULE THAT PRODUCES IT

**The act:** `round46/as-2.act.py`. It runs `window_tone build --securities-json round46/securities.union.r46.json --as-of 2026-10-04`
once.
- It refuses unless the gate (`round46/as-2.signing.py`) HOLDS AND the gate's built digest equals
  **`428298cfcde85c04ac77482c75015d3799753201b20fcce6c541e6f3f86fbde4`**.
- VERIFY runs the same rule on the WRITTEN part, plus written digest = gate digest.
- ROLLBACK writes the BEFORE rows back as a newer part (append, never overwrite).

**The build list** (`round46/as-2.build_union.py`) is the served list (212, `round33/securities.universe.r33.json`) UNION the
rank universe (191, pool `universe/v1/2026-09-16.json`) UNION RESAPP's covered set (95, `covered_security_keys()`):
- rank names not already served: 0;
- covered names not served: 21 (1299_HK, 939_HK, AMXB_MM, AZN_LN, BATS_LN, BNP_FP, CNR_CN, GSK_LN, IBE_SM, ISP_IM, KOFUBL_MM,
  NESN_SW, NOKIA_FH, OMAB_MM, ORA_FP, PWR_US, RIO_LN, SAN_FP, TTE_FP, UBSG_SW, VIVT3_BZ);
- served names outside rank and covered: 0, all kept;
- **union: 233.**

**`as_of`:** pinned to the served snapshot's own `as_of`, 2026-10-04. `window_end` is 2026-10-02 either way. Built with today's
date, the served rows differ only in `as_of` (636 of 636); pinned, they are byte-equal.

**THE RULE (round-43's explicit-zero rule, adapted):**
- built rows = 3 x 233;
- every served row is in the build and EQUAL on every field;
- an added name with 0 mention rows reads 0 / 0 / 0 / null; an added name WITH mentions must equal the independent recompute;
- every row equals the recompute, and tone is null exactly when voters = 0.

## Measured at signing (`round46/as-2.signing.out`, `.json`; PUTS SENT 0)

- **Before:** 2 parts; newest `chatter_window/date=2026-10-04/part-20261004T012303Z.parquet`, 636 rows.
- **Built:** 699 rows (233 x 3). **GONE 0, CHANGED 0.**
- **Added:** 63 rows on the 21 covered names. Added names with mentions: 0. Added rows that are not explicit zeros: 0.
- **Checks:** MISMATCH 0 against the independent recompute; tone null iff 0 voters (0 exceptions); shape ok.
- **RULE: HOLDS.**

## Writers of the served property (`gold/chatter_window`): N = 1

`window_tone.build_window`, run by this project's issuer acts (rounds 42, 43 and this one). No scheduled writer. RESAPP reads
the table; it never writes it.

## What moves

The 21 covered names gain their explicit zero rows ("no clear tone": articles 0, voters 0, tone null) in place of no row.
RESAPP's route then serves FWD-17's zero row for them instead of its "no table row" reason, and RESAPP round 68 re-reads c24.
Nothing else in the table moves.

## Rollback, per key

The act writes the BEFORE rows (636, digest recorded) back as a newer part, which serves them again. Nothing is deleted.

Not covered: any digest other than the one above, and any write besides the one `chatter_window` part (plus the rollback part).
