# AMGT_HARVST -- the lifted collection run, planned READ-ONLY (input to the round-45 analysis), `2.0.0_SA_COO~H`, 2026-10-04 ~23:2xZ

**Word:** Andrew-direct @441338fdf7 call 1, relayed by CTO~Z msg 29227: "ONE universe-scope run per publisher; no recurring
cadence and no new mechanism". The runs enter the round-45 analysis's enrichment list after FWD-12 grades DONE.
**CTO condition 1 @16eb97eae5:** no collection run until the ar-1 silver write is verified. No task order is cut here,
because round 45 is frozen. Nothing in this plan made a network call to a publisher.

## 1. What the existing driver would run

`python -m lib.opal_data_harvest.backfill_driver --dry-run` (`r46-collection.driver_dryrun.out`, NETWORK CALLS: 0):
- **UNIVERSE:** 89 names (`config.json` `universe_source` = RESAPP `universe.json`, the 2026-09-10 Asset Management corpus
  read).
- **PLAN:** 445 jobs, 89 x 5 publishers, sa first, one (publisher, name) job at a time.
- **BUDGET:** 4,320 requests/day per publisher. That is the pacing limit (15 s minimum + 10 s jitter); there is no daily cap.
- **Caps in force:** `max_listing_pages` sa 200 (round 45 ar-2), bbg/ft/wsj/barrons 25; `candidate_limit` 20; backfill floor
  2026-01-01 (the listing stops at the floor first). The bound for sa: 89 x (200 + 20) = 19,580 requests, about 4.5 days at
  the pacing limit. That bound is reached only if every name pages to 200. In the last backfill, 25 of 1,194 sa query-runs hit
  the old cap of 25 (aq-4).

## 2. THE FINDING: this run cannot make FWD-7 servable

FWD-7's served rank (`gold` source) needs a NON-EMPTY declared publisher set. `chatter_axis.publisher_universe_verdicts`
admits a publisher only when its CONCLUDED jobs in the window cover **EVERY** security key of the universe the generation
ranks, keyed by each job's `gold_security_key`.
- **The rank's universe:** `universe/v1/2026-09-16.json` in the pool, **191** names (`read_universe_names`).
- **The driver's universe:** **89** names. Their one-pager `bloomberg_ticker` resolves for **32** (57 UNRESOLVED). Mapped to gold
  keys (`<ticker>_Equity`), those 32 reach **30 of the 191**. **161 of 191** rank names are outside the driver's universe.
- **So a run over the driver's universe concludes jobs for at most ~30 of 191 rank keys.** Every publisher exits as
  `PER_NAME_TRIALS_ONLY`, the declared set stays EMPTY, and the `--source gold` flip still HOLDs.
- **Caveat:** the 30 is measured by ticker mapping. The collector stamps `gold_security_key` from its own input entry
  (`worker.py:467`), which this read did not trace. But no mapping can reach a name the driver does not run: at least 102 of
  the 191 names lie outside its 89-name universe.

**The call this needs (the CTO's, at the round-45 analysis):** what "universe-scope" means for this run.
- **(a) The run covers the RANK's universe, 191 names.** The driver's `universe_source` and its identity resolution move to
  the pool universe; that is a config change plus a resolution check. It is not a new mechanism.
- **(b) The run covers the driver's 89 names as built.** FWD-7 then stays HELD after the run, and the runs serve only the
  other 8 collection outcomes.

## 3. What each run writes (for its never-widen pair)

- bronze `article` and `listing_hit` objects per publisher (append, never overwrite);
- silver `article` / `listing_hit` through `upload-harvest` (one of the 3 silver writers named in the ar-1 COO half);
- a run record per run (the declared set reads these).

Gold and the served routes move only at the next gold rebuild, under its own pair.
