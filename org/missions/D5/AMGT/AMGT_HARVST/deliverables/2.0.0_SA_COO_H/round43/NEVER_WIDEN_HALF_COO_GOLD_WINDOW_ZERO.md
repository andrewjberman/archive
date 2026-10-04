# NEVER-WIDEN -- COO HALF: `chatter_window` with explicit zero rows (FWD-17, round 43 HVST-ap-1)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-04 ~01:1xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:** the round-42 analysis ruling 1 (@bad41f3f91, Z-C-S74). Decomposition section 56; the builder change and its
plant @5789ad3487.

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

The act (`round43/gold_window_zero.act.py`) re-runs the dry run before writing, checks the written part, and requires the
written digest to equal the dry run's.

**THE RULE** (`round43/gold_window_zero.signing.py`: `build_window` with the universe keys through a capturing client, diffed
against the served part and recomputed independently):
- built rows == 3 x the universe (212 x 3 = 636);
- every served row is in the build and equal on every field (GONE 0, CHANGED 0);
- every added row belongs to a universe name with 0 mention rows and reads articles_total 0, scored 0, voters 0, tone null,
  scorer null;
- every row equals the independent recompute (MISMATCH 0); tone is null exactly when voters == 0.

**Measured at signing (0 puts; `round43/gold_window_zero_signing.out` / `.json`):** served part
`chatter_window/date=2026-10-04/part-20261004T001638Z` (618 rows) -> built 636; gone 0, changed 0, added 18, all on the 6
names (8766_JP, BKRKY_US, EXPD_US, ICT_PM, KCDMY_US, ST_SP); added-not-explicit-zero 0; mismatch 0; tone-null-iff-0-voters
holds. RULE HOLDS.
**Plant** (`round43/ap-1.plant.out`): a universe name with 0 mentions reads three explicit zero rows. The test passes, and
fails with the fix removed. lib/research/harvest: 336 passed.

**Writers of `chatter_window` (N = 1):** only `window_tone.build_window` (`write_gold`, never-overwrite + read-back).

## BLAST RADIUS

- Exactly 1 new part, `amgt/harvest/gold/chatter_window/date=<as-of>/part-<stamp>.parquet`. Nothing else is written; nothing
  is deleted or overwritten.
- No route reads `chatter_window` yet, so nothing served on a page moves.
- One act, once.

## BOTH BRANCHES

- **The rule holds before AND after the write, and the written digest equals the dry run's:** done.
- **The rule fails BEFORE the write:** STOP, nothing written.
- **The rule fails on the WRITTEN part:** ROLLBACK. The 618 BEFORE rows are written back as a newer part (never-overwrite), and
  the act record carries the digest-equality check. Nothing is deleted.

## EXCLUDED

No other table, no silver or bronze write, no collection, no deploy, no portal change.

## VERDICT: SIGNED (COO), pending the CTO half
