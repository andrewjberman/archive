# ANDREW-DIRECT 2026-09-30 ~20:2xZ -- to 2.0.0_SA_COO~RV, in session

**Verbatim:** *"do not modify the existing daily etfs pull for Positioning"*

**Context:**
- RIV-m-1 measured both home funds JOIN_BLOOMBERG (merged `5b837f5024`).
- PRD v0.3 C-HOME-PRODUCER says the old pull "stops writing that fund in the same window".
- This seat had just asked `1.0.0_SA_CTO~Z` (20:20Z) to rule the stop's scope, because the pull also lands Bloomberg's
  capture-forward derived scalars, which this pipeline's request does not carry.

**What it binds (verbatim scope, not widened):**
- `integrations/bloomberg/pipeline/etf_constituents_pull.py` is NOT modified by ETFS_RIVALS. Its IDVZ and PFOE output keeps
  landing as today.
- The same holds for the Positioning ETF leg `etf_daily_pull.py`. Neither appears in any ETFS_RIVALS order's `<paths>`.

**Consequence, recorded, not resolved here:**
- IDVZ and PFOE holdings will have two landings: the Positioning pull (`bbg/<as-of>/constituents/`) and this pipeline's
  Bloomberg channel (`bloomberg/etfs/bronze/holdings/`).
- C-HOME-PRODUCER's "never two producers of one fund's holdings" is superseded for these two funds by Andrew's word.
- `1.0.0_SA_CTO~Z` owns any PRD addendum that reconciles the contract text.

**Answered in the same turn, Andrew-direct:** *"Anything we do for this would have to be additive"*

- RIV-b-1's leg in `scheduled_daily_pull.cmd` is ADDITIVE.
  - Check `b-1.AC3` proves every one of the vehicle's 394 lines at `2e38c030f4` survives, in order.
  - The leg is new lines after `:prune`, gated OFF, with its own rc variables and codes 90-97.
  - It stands.
- The rule for the rest of ETFS_RIVALS: the Positioning pull's scripts and the vehicle's existing lines are never edited; the
  only permitted form is new lines, new files and new legs.
- RIV-d-3's enabling line (`set "RIVALFUNDS_BBG_LEG=1"` inside the new leg) is a new line in the new leg, so it is additive.
