# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 43, AMGT-rr-1 (the five no-block names) -- 2.0.0_SA_COO~Z, 2026-09-25

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-rr-1.the-five-no-block-names.md`.
It executes only after BOTH halves are committed (this one and `1.0.0_SA_CTO~Z`'s).

**The five:** AMD, GOOGL, LLY, PWR and UNH (`<ROOT> US Equity`). They are exactly the names the LIVE research library holds beyond the
2026-09-10 snapshot (read 2026-09-25T18:42:56Z; row Z-S280). None has a landed model block today. Andrew's word
(C-BACKFILL-DENOMINATOR-IS-THE-RESEARCH-FOLDER) makes them part of the population.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named property, counted first:** the served Model block has ONE writer,
`integrations/bloomberg/research/model_block_pull.py` (`stage_derive`); the raw bronze has ONE, its `stage_pull`. N = 2 rules
read, one per property.

| act | what it MAY touch | expected outcome, read from the producer's own rule | rollback |
|---|---|---|---|
| A. `model_block_pull.py pull --securities` over the five, in two invocations (3 + 2), stopping at the first non-zero rc | NEW raw objects only: `bloomberg/harvest/bronze/{refdata,histdata,bestdata}/security_key=<k>/<stamp>.json` and the producer's pull-state, one fresh stamp per key; "never writes to a key that already exists" (the producer's own docstring, STORE_CONTRACT section 4 rule 1) | per key a raw stamp printed; a key the vendor returns empty is printed empty, never retried by hand | none needed: new stamps under keys that have no prior object; nothing is overwritten and nothing is deleted |
| B. `model_block_pull.py derive --securities` over the same five | NEW derived objects only: `derived/model_block/<k>/<stamp>/model_block.json` -- a FIRST MINT for each key | each block derived under the GUARDED cases rule (CRPS-g-1, re-derived for the 89 at AMGT_CORPUS round 5): a base case outside [0.33, 3.0] of px_last, a non-positive forward EPS or a currency mismatch is ABSENT with its cause, never served | a first mint has NO prior version to restore, and a delete is refused (standing). The exposure is bounded by the guarded rule above and by the page's own absence handling; a wrong block is superseded by a later-sorting re-derive, never removed |

**Both branches covered.** If a key's pull returns empty, the derive for that key is skipped and printed, and the order reports it.
If any invocation exits non-zero, the lane stops and reports: no retry by hand, no agent-composed call.

## VENDOR EGRESS -- declared

Bloomberg reference and history calls through the Desktop API, and the producer's own Seeking Alpha forecast fallback
(`sa_forecast_fallback.py`, where it fires). Both run under Andrew's STANDING grant R-21 (2026-09-24 ~03:2xZ, VERBATIM *"you have
all the egress you want for vendors ... the pull should be deterministic/scripted in nature like the existing pull"*), as the CTO
half for AMGT_CORPUS's fire of 40 ruled (`AMGT_CORPUS/ledger/NEVER_WIDEN_ROUND3_FIRE40_CTO_HALF.md` s.6). **Its constraint binds:**
every call is made by the scripted producer; no agent chooses or composes a call.

The Bloomberg session read `ok: true` (`bloomberg_health`, 127.0.0.1:8194, `//blp/refdata`) at the cut, ~20:1xZ.

Signed: `2.0.0_SA_COO~Z`, 2026-09-25 ~20:4xZ.
