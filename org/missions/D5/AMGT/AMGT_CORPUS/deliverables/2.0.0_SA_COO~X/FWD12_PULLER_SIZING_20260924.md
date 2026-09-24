# FWD-12 -- sizing the figures pull for the 22 added mnemonics before the round-3 cut (option 4, 2026-09-24 ~17:3xZ)

Design read only; no vendor call, no code. Andrew's per-use word for this pull is GIVEN (record @`16ee7f6373`, CTO R-70
confirms; R-16 V3: "asked at the cut"). R-21 binds the HOW: a deterministic, re-runnable, scripted producer, one run.

## The population of fields -- the 22, enumerated (the fold brief VIII-4, verified against today's bytes)

`docs/briefs/amgt-corpus-dossier-fold-brief-20260924.md` VIII-4 measured the corpus mnemonic sets against
`integrations/bloomberg/research/model_block_pull.py` (header 18 + history 23 + forecast 5 = 46 field names today):

- shared core, NOT in the pull (16): `EQY_SH_OUT_TOT_MULT_SH EQY_RAW_BETA BEST_DIV_YLD BS_CASH_NEAR_CASH_ITEM
  BS_TOTAL_LIABILITIES IS_ADJUSTED_GROSS_PROFIT IS_ADJUSTED_OPERATING_INCOME BEST_EBIT BEST_NET_INCOME BEST_CAPEX
  BEST_ESTIMATE_FCF IS_COMP_EPS_ADJUSTED BEST_BPS NET_INCOME EQY_DPS IS_DIL_EPS_CONT_OPS`
- extended ratio set, NOT in the pull (6): `PX_TO_FREE_CASH_FLOW GROSS_MARGIN EBITDA_TO_REVENUE RETURN_ON_CAP
  RETURN_ON_INV_CAPITAL RETURN_ON_TANGIBLE_ASSETS`

Verified this seat, read-only: all 22 are still absent from the puller's three field lists at HEAD, and every one of the 22
sits in today's typecast artifact (`research-model-typecast/scope=all-workbooks/698d1cf5d9f417cb.json`, 96 workbooks with
mnemonics of 120 read) -- so the entitlement question is answered by the team's own sheets, as the brief says.

## The mechanism the cell builds and runs once

1. `model_block_pull.py`'s field lists gain the 22 (history fields into `HIST_FIELDS`, `BEST_` estimates into
   `FORECAST_FIELDS`, ratios into `HIST_FIELDS`), each with its basis text as the module already keeps per mnemonic
   (Bloomberg's own definition beside every number); a fixture test proves the request lists carry exactly 46 + 22.
2. ONE run of the existing producer over the RESOLVED keys (53 today; the 40 more after round 3's induction), through its
   own raw landing family and conditional puts (the module's C-RAW-BEFORE-DERIVED path), read-back recorded: securities
   requested / landed / field errors per mnemonic, with `bloomberg_calls` printed.
3. The dossier's Model rows (composed by `dossier.py` from the typecast + the block) then carry figures for the 22 instead of
   ABSENT-with-reason; FWD-13's census re-run shows the ABSENT count fall by exactly the fields the block now serves per name.

Surfaces: the puller is `integrations/bloomberg/` (the Bloomberg lane's file; the RESAPP round's rk cells edited it under
`0.9.0_WK_AMGT_RESAPP` workers) -- the cut names the owner and takes its `<paths>` grant explicitly; the dossier side is this
project's. Never-widen: the block's raw landings are bronze (write-once, not served); the Model tab's SERVED figures are the
RESAPP adapter's read and take the pair there if the adapter's output moves.

## Honest size and risk

One cell, two workers' worth of work at most: the field-list change plus its test is an hour; the run over 53 names is bounded
by the DAPI (the existing pull already handles 34 names daily). Risk: a mnemonic the DAPI refuses for an entitlement or a
non-servable field -- the module already records refusals per candidate in `row_mnemonics.json` (its own docstring), so a
refusal is a printed row, never a silent gap. The word is spent by that ONE run; a second run needs its own word.
