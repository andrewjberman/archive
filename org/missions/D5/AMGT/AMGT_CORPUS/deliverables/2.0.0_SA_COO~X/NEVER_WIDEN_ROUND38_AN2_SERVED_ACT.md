# AMGT_CORPUS round 38 -- never-widen pair for `CRPS-an-2`: one re-derive of the 96 served blocks with NO currency on a count or ratio figure, and the re-pin of the daily task to the commit carrying it

**Authority:** round-37 analysis @`b12904724c` ruling 1 ("Round-38 cell, SERVED (pair): a count field (shares, volume) and a ratio
field carry NO currency ... The census over 96 blocks reads 0 count or ratio fields with a currency"). Decomposition v38.0
@`fcbe7aa0dc` s.1. Producer change CRPS-an-1, drained @`6f6e472641`.

**Code:** `<p>` = `6f6e472641`, or a descendant whose `model_block_pull.py` equals it. The commits between `3ffe37a57a` (the current pin)
and `<p>` carry two producer-side changes:
1. an-1: `_figure_currency` returns `(None, "invariant")` for `_COUNT_RATIO_NO_CURRENCY_FIELDS`, whose only member is
   `IS_SH_FOR_DILUTED_EPS`.
2. HARVST at-4: `lib/research/harvest/store.py` `silver_append` unions a group's row keys. It landed under its own CTO ruling
   @`08580b1fd6` + addendum @`ff4e31bcd0`.

**What at-4 does to THIS function's path, measured:**
- CORRECTED (1.0.0_SA_CTO~Z, msg 29637; re-measured by the issuer): `induction_scheduled`'s import closure DOES load a
  `silver_append` caller, `lib.research.harvest.bloomberg` (1 of 18 `lib.`/`integrations.` modules loaded). My first probe checked
  only two named modules (`substrate`, `typed`) and read their absence as the closure's.
- The fire's model-block writes go through `stage_pull` / `stage_derive`, which use only `store.table_prefix` and
  `entity_partition`. at-4 does not touch either.

So at-4 rides in the pin and IS reachable from the fire through `harvest.bloomberg`. The CTO accepted it on the HARVST evidence
(corpus 475 and the mixed-schema plant pass); the first fire on `<p>` is read as a served census (CTO condition 3).

## TIMING: the legs run AFTER CRPS-an-3 has read the 2026-10-06 13:00Z fire, and after CRPS-an-5 has run or been struck

Both of those fires run on the current pin `3ffe37a57a`:
- the 10-06 fire is FWD-22's carried regression read on that pin;
- the recovery run re-invokes the same task for 10-05.

Re-deriving before either would be undone by its old producer (served churn). Re-pinning before either would put new code under a
fire being read. So legs d and r run together, after both. The first fire on `<p>` is the next scheduled one after that.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round38/count_ratio_currency.py --derive <96 keys>` -> `evidence/r38_an2_dryrun.txt`)

The act's exact producer path: the REAL `stage_derive(..., sa_fallback=False)` on each served block's own raw stamp, at `<p>`. It
ran in memory, with all 96 puts captured and none sent.

| measure | result |
|---|---|
| count/ratio figures | 34,894 |
| count/ratio figures with a currency | **0** (served at the cut: 932, all `IS_SH_FOR_DILUTED_EPS`) |
| money figures | 31,985 |
| money figures unlabelled | 0 (round 37 holds) |
| values moved | **0** |
| money labels changed | 0 |

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r38-an2`, opened before leg d)

0. **Gate.**
   - an-3 has read the 10-06 fire, and an-5 has run or been struck.
   - The dry run is re-run on the then-newest raw. It must read `crc derive build 1/1 control 2/2`.
   - `schedule_induction.ps1 -Plan -Commit <p>` names Python311 (live-task).
1. **(d)** One `stage_derive(..., sa_fallback=False)` per registered name with a block (96), on its newest raw.
2. **(r)** `-Register -Commit <p>`, then `-Status`.
3. **(v)** Verify:
   - `count_ratio_currency.py --served` reads `crc served build 1/1 control 1/1`;
   - `checks/round35/v35.py <stamp>` reads base values moved 0 and pointer units 0;
   - `checks/round36/al5_served.py --where deployed` reads 1/1 + 1/1;
   - the task reads Start In `<p>`.

## EXPECTED OUTCOME (every branch)

- **Writers:** the served block has 1 writer (`stage_derive`); a figure's currency has 1 rule (`_figure_currency` at `<p>`).
- **Branch A:** the dry run's numbers: 0 count/ratio figures with a currency, 0 unlabelled money, 0 value moves.
- **Branch B (a name fails to derive):** it keeps its prior block, and the failure is listed.
- **Branch C (the plan names a non-Python311 interpreter, or the script refuses):** STOP before (r). Re-derive under `3ffe37a57a` in
  the same session; that restores the old labels, which round 37 graded acceptable.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| `derived/model_block/<key>/<stamp>/model_block.json` | up to 96 NEW write-once keys; only `IS_SH_FOR_DILUTED_EPS` figures' `currency` / `currency_basis` differ from the prior block | forward: re-derive from the same raw at `3ffe37a57a`; exact restore by delete needs Andrew's word |
| Scheduled Task `amgt-induction-daily` | Start In (pin `<p>`); interpreter and trigger unchanged | `-Register -Commit 3ffe37a57a` |

Never touched: any raw/bronze object, any Bloomberg call, any Seeking Alpha call, `field_map.json`, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-05 ~15:1xZ, for legs 0, d, r and v, covering branches A, B and C, after an-3 and an-5.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
