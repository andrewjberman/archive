# AMGT_HARVST ROUND 21 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~23:5xZ

**Issuance:** `95e703064d` (two independent chains over `ROUND_ANALYSIS.round20.md` @`4b8bd40242`; decomp section 33).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** LOCAL. Nothing served moved; the served rebuild is round 22.

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | deliver | drained | instance |
|---|---|---|---|---|
| `HVST-k-2` the updated-time census | LOCAL | `0e235142e3` | `9d523c8762` | VALID rc=0 |
| `HVST-k-1` the span rule plus the roundup guard | LOCAL | `85fe787f17` (after AMENDMENT 1 `c4f2fedc94`) | `88dbe4af64` | VALID rc=0 |

**`k-1` first FAILED AC2 at the ruled guard threshold 3** (rows `Z-W49-S1`/`S2`, BLOCKING):
- NVDA's served event went GONE, because all its members were guarded.
- AMZN reverted to 09-07, led by barrons.

The issuer re-ran the worker's AC2 at 3, 4, 5 and flag-only. Only 4 met every ruled intent. `1.0.0_SA_CTO~Z` RULED 4
(@`168acda05e`, msg 26783); the order was amended and the worker re-ran. Row `Z-W49-S5` records the disarm.

**Issuer self-correction:** the threshold re-runs overwrote the worker's committed `k1_ac2_result.json`, because the
script writes it. It was restored to its committed bytes before the amendment commit. The close run below was checked
for the same effect, and 0 tracked files changed.

**Both drains** met the append-only channel conflict. Each was resolved by row-id union: 0 same-id rows differed, and
`--continue` ran with 0 foreign paths.

## 2. THE CLOSE RUN (`round21/close_run_round21.out.txt`, trunk `88dbe4af64`)

- **Suite:** 228 passed.
- **`k-1` AC2 on trunk:** PASS. KEPT 5, CHANGED 3, MERGED 0, GONE 0.

  | security | new-rule event | articles | lead |
  |---|---|---|---|
  | 992_HK | 08-13..08-14 | 3 | -- |
  | AMZN | 09-06..09-07 | 5 | bbg's first report |
  | HD | 08-17..08-18 | 4 | -- |

  HD's 08-20 roundup (`co_mention_count` 4) is a guarded member.
- **`k-2` on trunk:** reproduces. Updated or modified time exists for:

  | publisher | articles with an updated time |
  |---|---|
  | barrons | 0 of 15 |
  | bbg | 0 of 19 |
  | ft | 0 of 14 |
  | sa | 5 of 46 |
  | wsj | 11 of 26 |

## 3. FOR THE CTO'S LEAD RULING (ruling 3 of round 20)

- HD's retitled barrons preview (`barrons:WP-BAR-0001875805`, `published_utc` 2026-08-17 16:24Z) carries NO updated time
  in silver or bronze, and neither does any barrons, bbg or ft article.
- By ruling 3's own branch, the one-day-early start is ACCEPTED AND DISCLOSED. Under the new rule, HD's event starts
  08-17.
- **Row `Z-W50-S1`:** the SERVED HD event today is bbg-led, on 08-18 only (since `part-20260928T210944Z`). The barrons
  lead appears in older parts and in the new-rule event, not in today's served one.

## 4. FOR L9

No judgment criterion this round.

One plausibility read is offered, and it is not graded here: under the new rule, is each of the 3 CHANGED events one
story about its own company, led by a headline that names it? The full member lists with guard status are in
`0.9.0_WK_AMGT_HARVST~49/k1_ac2_output.txt`.

**Worktrees now DISPOSABLE:** `wk-hvst-r21-49`, `wk-hvst-r21-50` (and the three listed in round 20). Branches are kept;
removal is on Andrew's go.
