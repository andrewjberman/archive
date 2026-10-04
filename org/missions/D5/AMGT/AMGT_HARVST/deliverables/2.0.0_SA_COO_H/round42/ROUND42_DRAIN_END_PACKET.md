# AMGT_HARVST -- ROUND 42 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-04 ~00:2xZ

**Round:** the round-41 analysis enrichment list (@98f36bf49a, ruling 2) under Andrew's card 2 (@9fe6e6f111). Decomposition
section 55 (issued @fa23c32afc). One issuer direct act. **Class: SERVED** (a new gold table; no route reads it yet). No
collection ran.

## 1. The cell

| cell | result | evidence |
|---|---|---|
| `HVST-ao-1` FWD-17 `chatter_window` | **WRITTEN.** Pair: COO @f0eb10b97d + CTO @d5d17b2d91. Gate HOLDS; VERIFY on the written part HOLDS; written digest = gate digest. Part `amgt/harvest/gold/chatter_window/date=2026-10-04/part-20261004T001638Z.parquet` (the table's first). 618 rows on 206 securities (30/90/365 each), window_end 2026-10-02 (Friday, T-1); 496 rows with tone, 122 null; 0 mismatch against an independent recompute from the served mention snapshot (31,042 rows) and the score store (13,224); tone null exactly when voters == 0. | `round42/gold_window_act_20261004T001627Z.json`, `gold_window_signing.out` |
| plant | The unit plant `test_ak2_window_tone.py::test_i_all_neutral_name_is_voters_zero_tone_none_in_every_window` passes (the file: 9 passed). On real data, 40 all-neutral windows (scored > 0, voters 0) serve tone null, e.g. AIG 90-day, ATO 365-day, BBSE3 30-day. | `round42/ao-1.plant.out`, `gold_window_signing.json` (`all_neutral_sample`) |

## 2. For the CVO

- **Judgment to grade on the written part:** does each row give the window's tone as FWD-17 states it (voters = non-neutral scored
  articles, tone = mean signed score over voters, null at 0 voters, never 0.0)?
- **Not served yet:** no route reads `chatter_window`. RESAPP's chatter route reads it in RESAPP's own cell (FWD-36's tone limb).
  Until then that route serves `tone` null with its reason.
- **6 universe securities have no row:** 212 in the universe file, 206 with rows. Read after the act: the 6 (8766_JP,
  BKRKY_US, EXPD_US, ICT_PM, KCDMY_US, ST_SP) have 0 mention rows in the served snapshot, so the builder has no population
  for them (its own rule: one row set per security PRESENT in the mention rows).
- **Surprise rows this round:** none.

Push: LOCAL.
