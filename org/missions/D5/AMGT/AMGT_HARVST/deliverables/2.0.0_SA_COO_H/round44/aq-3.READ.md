# HVST-aq-3 -- FWD-7 read (round 44), `2.0.0_SA_COO~H` fork, 2026-10-04 ~18:1xZ

**FWD-7 DONE WHEN:** "the chatter ranks on the page are computed from the graded daily table, and a company named once in passing
in many articles no longer outranks one that was the subject of a few".

## VERDICT: FAIL

The served chatter rank is computed from a RAW article count, not from the graded daily table. Through the producer's own
`compute_chatter_axis`, a company named in passing in 6 articles outranks the subject of 2 (rank 1 vs rank 2). The graded branch
exists in code and ranks them correctly, but it is not the served source. On today's real data it would also HOLD.

## 1. The basis at HEAD (quoted; `aq-3.rank_basis.out`)

- The page's rank is served from a committed generation: `lib/research/api/scoped_amgt.py:5555`
  `read_rankings(rest[2], rest[3], ...)`. It passes the producer's order through ("there is no sort ... in this body").
- The producer picks its count function by source: `lib/research/metrics/chatter_axis.py:432` `"legacy": default_daily_article_counts,`,
  `:433` `"gold": gold_daily_mention_scores,`, and `:435` `DEFAULT_SOURCE = "legacy"`.
  - `legacy` reads the pool's raw article histogram (`:371` `pool_reader.window_read`): one article counts 1, whatever its grade.
  - `gold` reads the graded `chatter_daily` (`:411` `pool_reader.gold_window_read`) and scores by `signal_weight` (`declared_set_scores`).
- The deployed Lambda takes the source from its environment: `infra/aws/terraform/harvest/lambda_src/lambda_function.py:88`
  `SOURCE_ENV = "CHATTER_AXIS_SOURCE"`. When unset it returns `DEFAULT_SOURCE` (`:109`).
- DESIRED: `infra/aws/terraform/harvest/chatter-axis-schedule.tf:70` `chatter_axis_source = "legacy"`, wired at `:197`.
- TRENDING x CHATTER ranks on the as-of day's absolute count (`lib/research/metrics/movement_gate.py:352`).

## 2. Applied (read live)

- `amgt-resapp-chatter-axis` `CHATTER_AXIS_SOURCE=legacy` (LastModified 2026-09-24T05:09Z): DESIRED == APPLIED == legacy.
- Served `/lead-panel/rankings/trending/chatter` and `/breakout/chatter` (as_of 2026-10-04): status 200, `ranking_status` EMPTY,
  0 rows. The reason is "NO_SIGNAL_IN_WINDOW 191 of 191" (generation 20261004T100014Z-f64fa88f3357, vintage
  `pool:universe/v1/2026-09-16.json`). The legacy pool layout holds no article in the 30-day window for any of the 191 names, so the
  page serves no chatter rank at all today. The graded gold table holds 31,042 mention rows that this rank never reads.

## 3. The planted pair, through `compute_chatter_axis` (write_fn=None; `aq-3.rank_basis.json`)

A_PASSING is named in passing (tier D, signal_weight 0.1, a 6-name roundup) in 6 articles every day. B_SUBJECT is the subject
(tier A, 1.0) of 2 articles on the as-of day plus 1 on each of three earlier days. 10 fillers carry one tier-B article on the
as-of day. 12 names in all.

| source | TRENDING_CHATTER | A_PASSING | B_SUBJECT |
|---|---|---|---|
| **legacy (SERVED)** | COMPLETE | **1** | **2** |
| gold (graded) | COMPLETE | 2 | 1 |

BREAKOUT_CHATTER is EMPTY on both sources (BELOW_MIN_ABSOLUTE_JUMP), as the movement gate rules.

## 4. What a repair needs (no repair made here)

- **Selecting `gold` is the repair the code was built for.** It is one env flip in `chatter-axis-schedule.tf:70` plus an apply,
  under a fresh never-widen pair (the tf comment: "gold is selected by one env flip + apply under a fresh pair when 2b lands").
- **On today's real data that flip would HOLD.** The producer's own dry run with `--source gold` (`aq-3.gold_dryrun.out`, 0 writes)
  read state FAILED on both axes:
  - "HOLD: declared publisher set is EMPTY (no enabled publisher ran a universe-scope job that concluded in the window)";
  - window 2026-09-05..2026-10-04; POPULATION eligible 0, NOT_SEARCHED 191; STATES partial 363, no_coverage 5,367.
  The gold rank requires a declared publisher set derived from universe-scope collection runs that concluded in the window. No
  collection has run in the window, and collection is held on Andrew's word.
- So FWD-7 cannot be closed by a producer cell alone. Either (a) a universe-scope collection run lands (held on Andrew's word:
  "We will discuss internally on how to proceed with further data collection after review"), or (b) the CTO re-rules the
  declared-set eligibility contract (C-HV-RANK-DECLARED-SET) for a backfilled store. That is an ENDPOINT/contract question for
  `1.0.0_SA_CTO`. The source flip itself is a SERVED write under a pair either way.

Evidence: `aq-3.rank_basis.py` (ruff clean, py39), `aq-3.rank_basis.out`, `aq-3.rank_basis.json`, `aq-3.gold_dryrun.out`.
