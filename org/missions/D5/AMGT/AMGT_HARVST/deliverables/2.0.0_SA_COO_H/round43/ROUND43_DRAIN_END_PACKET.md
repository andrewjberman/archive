# AMGT_HARVST -- ROUND 43 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-04 ~01:3xZ

**Round:** the round-42 analysis enrichment list (@bad41f3f91, ruling 1, Z-C-S74). Decomposition section 56. One issuer
direct act. **Class: SERVED** (no route reads `chatter_window` yet). No collection ran.

## 1. The cell

| step | result | evidence |
|---|---|---|
| `HVST-ap-1` code | `window_tone.build_window_rows(..., security_keys=)`: every universe name gets its 3 rows, and a 0-mention name reads 0 / 0 / 0 / null. `build_window` and the dry-run CLI pass the universe keys. @5789ad3487 | `lib/research/harvest/window_tone.py` |
| plant | A universe name with 0 mentions reads three explicit zero rows. The test passes, and fails with the fix removed. A named-and-mentioned name's rows are unchanged by `security_keys`. `test_ak2_window_tone.py` 11 passed; lib/research/harvest 336 passed; ruff clean. | `round43/ap-1.plant.out` |
| served write | **WRITTEN.** Pair: COO @b964ccd5f0 + CTO @e91d53a7a9. Gate HOLDS; VERIFY on the written part HOLDS; written digest = gate digest. 618 -> 636 rows (212 x 3); gone 0, changed 0; 18 added, all explicit zeros on 8766_JP, BKRKY_US, EXPD_US, ICT_PM, KCDMY_US, ST_SP; recompute mismatch 0; tone null iff 0 voters. Part `chatter_window/date=2026-10-04/part-20261004T012303Z.parquet`. | `round43/gold_window_zero_act_20261004T012241Z.json` |

## 2. For the CVO

- **To grade:** FWD-17 "gold carries, PER NAME per window": every one of the 212 covered names now has its 30/90/365 rows. A name
  with no coverage reads an explicit zero (0 articles, 0 scored, 0 voters, tone null), never an absence.
- **Not served yet:** no route reads `chatter_window`; RESAPP's FWD-36 tone limb is with `2.0.0_SA_COO~Z`.
- **Surprise rows this round:** none.

Push: LOCAL.
