# NEVER-WIDEN -- COO HALF: the first served `chatter_window` part (FWD-17, round 42 HVST-ao-1)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-04 ~00:0xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:** the round-41 analysis ruling 2 (@98f36bf49a) under Andrew's card 2 (@9fe6e6f111). Decomposition section 55
(issued @fa23c32afc).

## WHAT THIS HALF SIGNS: A RULE, NOT A DIGEST

The act (`round42/gold_window.act.py`) re-runs the dry run before writing and recomputes the written part afterwards. It
also requires the written part's digest to equal the dry run's.

**THE RULE** (`round42/gold_window.signing.py`: the builder's own `build_window` through a capturing client, then EVERY row
recomputed independently from the served mention snapshot and the score store, from FWD-17's words):
- before: `chatter_window` holds 0 parts (a first mint; nothing served is replaced);
- 3 rows (30/90/365) per security of the mention snapshot that is in the universe file (`round33/securities.universe.r33.json`);
- `window_end` is the last trading day before the as-of date, on every row;
- every row equals the independent recompute on `articles_total`, `scored`, `voters` and `tone` (MISMATCH 0; tone within 1e-12);
- `tone` is null exactly when `voters` == 0 (never 0.0 at 0 voters).

**Measured at signing (2026-10-03 23:56Z, 0 puts; `round42/gold_window_signing.out` / `.json`):** parts before 0; mention
read 31,042 rows, scores 13,224; window_end 2026-10-02 (Friday); built 618 rows on 206 securities, 496 with tone, 122 null;
mismatch 0; window_end wrong 0; tone-null-not-iff-0-voters 0; shape bad 0. RULE HOLDS.
**The plant, on real data and in the test:** 40 windows have scored > 0 and voters 0 (all-neutral), and every one serves
tone null (e.g. AIG 90-day, ATO 365-day, BBSE3 30-day). The unit plant
`test_ak2_window_tone.py::test_i_all_neutral_name_is_voters_zero_tone_none_in_every_window` passes (`round42/ao-1.plant.out`).

**Writers of `chatter_window` (N = 1):** only `lib.research.harvest.window_tone.build_window` (`write_gold`, never-overwrite
conditional put + read-back). No scheduled producer runs it.

## BLAST RADIUS

- Exactly 1 new part, `amgt/harvest/gold/chatter_window/date=<as-of>/part-<stamp>.parquet`. Nothing else is written;
  nothing is deleted or overwritten.
- No route reads `chatter_window` yet. RESAPP's chatter route will read it in RESAPP's own cell, so nothing served moves today.
- One act, once. A second run needs a new half.

## BOTH BRANCHES

- **The rule holds before AND after the write, and the written digest equals the dry run's:** done. The act record
  `round42/gold_window_act_<stamp>.json` names the part.
- **The rule fails BEFORE the write:** STOP, nothing written.
- **The rule fails on the WRITTEN part:** ROLLBACK. A first mint has no BEFORE rows, so an EMPTY newer part is written through
  `write_gold` (never-overwrite) and a reader sees no windows, as before. Nothing is deleted.

## EXCLUDED

No other table, no silver or bronze write, no collection, no deploy, no portal change.

## VERDICT: SIGNED (COO), pending the CTO half
