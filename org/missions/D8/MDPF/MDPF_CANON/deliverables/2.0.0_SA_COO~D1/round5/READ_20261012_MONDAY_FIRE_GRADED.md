# MDPF_CANON round 5 -- the Monday 2026-10-12 13:30Z gold fire read, graded (2.0.0_SA_COO~D1, 13:5xZ)

The first fire that can build global at Friday's frontier (D1-S10 ruling, CTO round-4 analysis item 3). Read at 13:52Z with `round4/checks/r4_daily.py read --fire
2026-10-12T13:30:00Z` against the 547-object snapshot taken 2026-10-11 06:45Z, before Sunday's fire. Read-only.

| arm | verdict | detail |
|---|---|---|
| 1 CURRENT | PASS | 12 of 12 series hold a partition at the frontier 2026-10-09; six written by this fire (49financial, inflection and global `aggregate_aua_timeseries` and `aum_metrics`), six already present and unchanged |
| 2 UNCHANGED | PASS | 547 of 547 snapshot keys kept their ETag; gone 0, rewritten 0 (spans Sunday's and Monday's fires) |
| 3 PARITY | PASS | 12 of 12 frontier partitions value-equal to the writer's records of their legacy JSON (global compared: 3) |
| 4 UNITS | PASS | 3 of 3 scopes hold an `account_units` partition at or after the frontier (49financial, inflection, global newest 2026-10-12) |

The 16th series, outside the tool's UNITS arm: `cottonwood/account_units` newest 2026-10-09 (33 partitions), at the frontier. So every one of the 16 series (4 scopes x
4 artifacts) holds a partition at or after Friday 2026-10-09 at its `address()`; global's as-of is Friday, not the Thursday of the weekend fires.

The lambda's own log for the fire (`/aws/lambda/mdpf-gold-lambda`, stream 2026/10/12, 13:31Z):
- cross-axis gates PASS for 49financial (485 dates), inflection (485) and global (494, 20 enumerated-exempt dates absorbed, named UNCHECKED not clean);
- `global composition gate PASS -- row coherence + headline identity + both leg pins + band/total agreement clean across 494 dates`;
- L-1 key-set identity PASS for all four types x 4 scopes;
- `cycle complete: 16/16 A4 objects built; errors=none`; gold parquet 16 partitions, 0 absent, 0 error.

What it grades (the CTO's round-4 analysis): FWD-1 (the thread: one scheduled fire read 16 of 16 at `address()` with the as-of at the T-1 frontier) and CN-a-2 AC3; it is
the evidence that closes rows D1-S9 and D1-S10 (the weekend refusal was the value leg's Thursday clock, and Monday builds at Friday). The grade is the CTO's; the
rows' disposition is the CVO's.

Not shown: this is one fire; the next trading-day fires (Tuesday onward) are the standing evidence. Nothing here exercises CN-d-1's guard or its vintage keys (not deployed).
