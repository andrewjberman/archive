# AMGT_HARVST -- ROUND 47 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-06 ~02:4xZ

**Round:** the round-46 analysis enrichment list (`ledger/ROUND_ANALYSIS.round46.md` @585391af7f). Decomposition section 60, with
amendment 1 (60.1, at-4) and amendment 2 (60.2, at-5). **Class: SERVED + WORLD** (at-4 touches every silver writer; the collection run
is publisher egress on Andrew's word).
**Drained on the CTO's ruling @69ce080222 (row Z-S89):** all four legs stay stopped; drain on what has concluded.

## 1. The cells

| cell | result | evidence |
|---|---|---|
| `HVST-at-1` | **COMPLETE.** Worker ~95 @7d2166a180 + @a567807afa; landed @23baacf0e1. One listing silver_append per source per pass. AC1 8/8. AC2: silver prefix reads old 100 against new 1; wall time 84.04 s against 0.91 s; rows identical 200/200. Proven live: 92 stranded sa objects uploaded in one pass. | `task-orders/AMGT_HARVST.TO-HVST-at-1.batched-listing-upload.md` record face; `round47/checks/at-1.AC2.py` |
| `HVST-at-2` | **DONE.** bbg and wsj were stopped by their stop files and resumed 07:25:46Z from their own checkpoints; sa resumed after its old-path upload ended. | tick log; record face of at-1 |
| `HVST-at-4` | **DONE.** `store.silver_append` gives every row of a date group the union of the group's keys (pyarrow 24 takes columns from the first row). Plants 4/4, mutant fails; mixed narrow/wide prefix test 2/2. Landed with at-1 @23baacf0e1 on the CTO's word @08580b1fd6 + addendum @ff4e31bcd0. Damage census: 0 dropped columns measured. | `round47/at-4.dropped_columns_census.out/.json` |
| `HVST-at-5` | **DONE.** Andrew-direct "Yes I do" (record `ANDREW_DIRECT_20261005_163xZ_HARVST_ADD_RESEARCH_NAMES.md`): the run universe widened 191 -> 234. Adds 40 of the 56 approved research resolutions (16 were already held as fund names) + Quanta, AIA, Hitachi. The 191 identity records are identical. Merged @1685d149fa after PARITY CLOSED; legs relaunched 17:27Z from their own checkpoints. | `round47/at-5.widen_universe.py`; decomposition 60.2 |
| `HVST-at-3` | **DONE (this drain).** The per-leg report below. | `round47/at-3.per_leg_report.py/.out/.json` |

## 2. The collection run at drain (all legs STOPPED)

| leg | concluded of 191 | of 234 | added 43 | stop reason (checkpoint) |
|---|---|---|---|---|
| sa | 9 | 9 | 0 | `upstream_unavailable` (shared driver, 14:07Z); `account_or_harvester_unavailable` = SA account HTTP 402 (parallel root, 01:12Z) |
| barrons | 130 | 145 | 15 | `bot_check` 01:32Z (65 `listing_empty_200` soft blocks over the run, row Z-S88) |
| ft | 0 | 0 | 0 | `sign_in_refused` (held, Andrew-direct @b023b75324) |
| bbg | 104 | 104 | 0 | `bot_check` 01:41Z (second challenge; no second clear) |
| wsj | 154 | 154 | 0 | `bot_check` 01:32Z |

- `publisher_universe_verdicts` over the 191: every publisher **out**, so the **DECLARED SET is EMPTY**.
- Job records of this run: 502. Andrew asked for sa to run in its own parallel leg at the 200-page cap ("yes do SA and try 200 page
  cap"). Its first job met the 402.
- **Resume conditions (CTO @69ce080222):** a leg resumes only once Andrew hand-solves its challenge while present, from its own
  checkpoint. sa resumes only once the account endpoint answers 200.

## 3. For the CVO

- **To grade:**
  - the at-4 column-union fix (plants, plus the 0-damage census);
  - the at-1 batched upload (AC2);
  - the at-5 widening, against Andrew's word and the 16 already-held names.
- **The collection outcomes:** graded on the per-leg report above. No publisher reaches the declared set.
- **Open for the round-47 analysis:**
  - the machine-wide block (Z-S89) and how a resume is staged;
  - the SA account state;
  - barrons soft blocks (Z-S88);
  - the stale pool universe (191 against the 234 run universe), which RESAPP carries to its round 72 with the owner of
    `build_universe.py`;
  - driver upload-timeout handling (Z-S87).
- **Surprise rows this round:**
  - Z-S87 (upload timeout);
  - Z-W95-S1 and Z-W95-S2 (column rounds; first-row columns, disarmed by at-4);
  - Z-S88 (barrons soft blocks; CTO ruling 29759);
  - Z-S89 (the hard block; CTO ruling @69ce080222).

Push: read at send time.
