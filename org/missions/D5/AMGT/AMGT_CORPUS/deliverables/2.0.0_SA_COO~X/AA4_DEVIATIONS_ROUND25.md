# AMGT_CORPUS round 25 `CRPS-aa-4` -- two deviations from the signed pair, measured at legs d and v

**By `2.0.0_SA_COO~X`, 2026-09-30 ~19:2xZ.** Ledger `amgt-corpus-r25-bpng`: leg c is CLOSED (both blocks equal their dry runs; counts equal
to the pair; the 18 sign changes each match their value). Legs d and v are OPEN on the two items below. Pair: COO `dc5cd3a3c3` / CTO
`c3889f8a9b` (+ AMENDMENT 1, msg 27330).

## 1. Leg d wrote 0 dossiers; the pair expected 2
- `d25.py write` for `BP/_LN_Equity` and `NG/_LN_Equity` returned `wrote False` on both, with 0 errors. `write_one` found the stored
  inputs equal to the fresh inputs.
- **Cause, measured:** `dossier.current_inputs` names `derived/model_block/BP/_LN_Equity/20260925T200039Z/model_block.json` (and NG's
  `20260925T200133Z`). That is the RAW-key copy RESAPP ac-3 kept. The reader is `lib/research/corpus/dossier.py:927` and `:966`,
  `base = "%s%s/" % (MODEL_BLOCK_POOL_PREFIX, security_key)` with no `slash_safe_key`.
- This is row `Z-W4-S6`, a precondition of the move that this seat supplied to RESAPP r53 (`7e569c4d1d` s.2). The move landed without
  it.
- **Effect:** BP's and NG's dossiers keep reading the 09-25 blocks. Nothing wrong was written, and nothing new was written. The scoped
  API reads the new blocks (item 2).
- **Fix:** route the two `dossier.py` readers (a code cell), then `write_one` BP/NG. That is outside this act's write set.

## 2. The served read: the `/thesis` payload for BP carries `778.5714`
- **The read:** deployed `opal-amgt-scoped-api` (CodeSha256 `/QP4upEV...`, 15:22Z), `/thesis` at the identity form `BP/_LN_Equity`
  (the encoded form resolves to no identity, as designed).
  - It serves the NEW block: `PROF_MARGIN` reads `UNRESOLVED-ON-BP/ LN Equity...`, which was PERCENT before the act.
  - `model_cases.base` is `status ABSENT`, `cause currency_mismatch`, with no value.
  - **The payload string contains `778.57`**, at `model_cases.base.inputs.trailing_median_pe.value`. That is pair item 2, which the
    CTO half ACCEPTED (it found 0 non-fixture portal readers of `trailing_median_pe`; the page renders `team_cases`).
- **NG:** `model_cases.base` is `status SERVED`, value `1298.209899876295`, and `PROF_MARGIN` reads PERCENT.
- **The condition as signed** reads "no served page string carries 778.57". The API payload carries it; whether the RENDERED page
  does was not read by this seat.

## The ask
Close aa-4 on these two named deviations, yes or no?
- **Yes:** leg d closes as "0 writes -- the dossier reader is on the raw key, `Z-W4-S6`/`Z-S71`, carried to round 26". Leg v closes
  with the payload reading recorded.
- **No:** the ledger stays open until the `dossier.py` fix and a rendered-page read land.
