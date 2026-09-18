# LGIC_LGCTFM.TO-LT-v-1-r1 -- reviewer reproduction + Andrew card, round 1 result

Worker `0.9.0_WK_LGIC_LGCTFM~3`, slot 3, cell `LT-v-1`. This slot wrote no engine code this round
(`git log --format=%an -- lib/opal_lgctfm.py` names only `0.9.0_WK_LGIC_LGCTFM~1` and
`0.9.0_WK_LGIC_LGCTFM~2`), so this reproduction is a second, independent instrument on the engine's
own claims -- not a re-run by the author.

## What was reproduced

Source: the first real run's contract,
`workflows/legacy_transform/blackdiamond-49financial/20260917T202556Z-bb29248/contract.json` (184
rows, 179 tensions, `subject.key = 49financial`).

**Sample.** 184 of 184 rows carry a builder call the naming rules can answer, all through the single
`grade` builder (no other of `name`/`address`/`lookup`/`fence_patterns` appears in this run). The
sample of 20 spans all five `desired.verdict` kinds present in the contract (ALIAS 5, CONFORMANT 4,
NOT-GRADED 1, OUT-OF-PATTERN 5, RAISE 5) rather than picking the first or easiest 20 rows -- FWD-3's
own bar.

**Call.** Each sampled row's `desired.builder.args`/`kwargs` were fed to `lib/opal_naming.py`'s
`grade()` directly by this worker, fresh, outside the engine. 20 of 20 calls returned (or raised) the
same form the contract's `desired.form`/`verdict` already carried.

**Order.** The tension ranking rule, printed verbatim in the contract:

> order by irreversible, then client_facing, then live, then rules_colliding; object_count as tiebreak
> (08_TENSION_MAP.md s.0)

...was re-implemented independently from the four factor cells (never by importing the engine's own
sort key) and applied to all 179 tensions. The resulting order is identical to the contract's stored
order at every position (first divergence: none).

## Recorded

- `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/REPRODUCTION.json` --
  `contract`, 20 `results` rows (`row_id`, `fn`, `args`, `kwargs`, `got`, `expected`, `equal`), and the
  179-entry re-derived `order`.
- `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/ANDREW_CARD.md` -- the
  decision, the recommendation, the subject, the `ranking_rule` verbatim, and the top ten tensions by
  `tension_id` with their four factor values. This worker cannot deliver the card; the issuer carries
  it. Andrew's read of FWD-4 stays APPLIED until he has read it himself -- this result file is not a
  substitute.

## Mechanical criteria (this worker's own re-run before the proof instance)

- `V1R1-AC1` (`v1-reproduced`): PASS -- callable rows 184, sample required 20, sampled 20, reproduced
  20 of 20.
- `V1R1-AC2` (`v1-order`): PASS -- 179 tensions; reviewer order == rule order: True; contract order ==
  rule order: True.
- `V1R1-AC3` (`v1-not-author`): PASS -- authors of `lib/opal_lgctfm.py`: `0.9.0_WK_LGIC_LGCTFM~1`,
  `0.9.0_WK_LGIC_LGCTFM~2`.
- `V1R1-AC4` (`v1-card`): PASS -- ranking_rule verbatim in card: True; top tensions shown: 10 of 10.
- `V1R1-AC5`: judgment, no verdict from this worker. FWD-3's sampling-spans-kinds question and FWD-4's
  read-recorded-with-question question are both for `3.0.0_SA_CVO` at L9.
