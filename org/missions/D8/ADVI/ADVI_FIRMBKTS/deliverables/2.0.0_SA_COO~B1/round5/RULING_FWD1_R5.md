# RULING -- FWD-1's 11 disagreements named, each ruled or fixed (2.0.0_SA_COO~B1, 2026-10-13 ~06:5xZ)

Seat: the issuer rules everything inside its own decomposition (CLAUDE.md, canonical-drive obligation 7). Input: the CVO's
`D1-C-S29` (139 of 150 canonical locations agree on all four fields; the 11 do not: 8 table-grain choices, 3 unknown tables,
0 date conflicts) and the CTO's round-4 analysis section 3 item 1 ("name each, then fix it or rule it"). The 11 are named
below from `ANSWERS_A.json`, `ANSWERS_B.json` and `round4/READING_KEY.json` (printed by `round4/checks/r4_agree.py`; the
record is `FWD1_R4_DISAGREEMENTS.json` in this folder). The key's `table` is the mapping's own `dest.table`.

## The one rule every one of the 11 follows

The standard key grammar is `{source}/{scope}/{tier}/{table}/{partition}`. **The `table` is the ONE path component
immediately after the tier.** Everything after it is the partition. Read against the key, all 11 follow this rule and every
disagreement is a reader applying a different rule or declining to apply one: the grammar was stated to the readers, the
component rule was left implicit.

## The 11

| # | location (class) | key.table | reader A | reader B | disposition |
|---|---|---|---|---|---|
| 1 | `.../49financial/state/parity/canonical_lots/2026-10-09/scorecard.json` (`gold/_parity/canonical_lots/`) | `parity` | `canonical_lots` | `parity` | **RULED**: the table is the component after the tier (`parity`); `canonical_lots` is the partition level. Reader A took a deeper component. |
| 2 | `.../state/parity/holdings_lots/2026-10-09/scorecard.json` | `parity` | `holdings_lots` | `parity` | **RULED**, as 1. |
| 3 | `.../state/parity/account_gains/2026-10-09/scorecard.json` | `parity` | `account_gains` | `parity` | **RULED**, as 1. |
| 4 | `.../state/parity/positions_cube/2026-10-09/scorecard.json` | `parity` | `positions_cube` | `parity` | **RULED**, as 1. |
| 5 | `.../state/parity/load_flows/ss4c/2026-10-07/scorecard.json` | `parity` | `load_flows` | `parity` | **RULED**, as 1. |
| 6 | `.../state/parity/fee_rate_history/2026-06-15/scorecard.json` | `parity` | `fee_rate_history` | `parity` | **RULED**, as 1. |
| 7 | `s3://opal-data-inflection/advi/inflection/gold/hh_timeseries_anchors_INF_D_05/data.parquet` (`gold/cache/`) | `hh_timeseries_anchors_INF_D_05` | same | `unknown` | **RULED**: reader B declined; the component rule yields the key's value. No mapping change. |
| 8 | `s3://opal-data-49financial/advi/49financial/code/gold/lib/etf_classifier.py` (`code/`) | `gold` | `unknown` | `unknown` | **FIXED**: a code object has no obvious "table"; the rule now names it (the group directly under `code/`). Both readers answered `unknown`. |
| 9 | `s3://opal-data-inflection/advi/inflection/code/gold/lib/nna_coverage_excusals.json` (`code/`) | `gold` | `unknown` | `unknown` | **FIXED**, as 8. |
| 10 | `s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json` (`platinum/49financial/`) | `49financial` | `49financial` | `ownership_map` | **RULED**: the platinum tier is partitioned by firm slug; the component after the tier is `49financial`, the file name is never the table. Reader B took the file name. (Recorded as a mapping-design question for the CTO: a firm slug as a table name is the grain the PRD ratified; not changed here.) |
| 11 | `s3://opal-data-assets/orion/inflection/bronze/orion/2026-04-29/trn/Homepage Daily Transactions ... .csv` (`bronze/orion/`) | `orion` | `orion` | `trn` | **RULED**: the component after the tier is the source (`orion`); `trn` is a partition level. Reader B took the deeper directory. |

Count: RULED 9 (rows 1-7, 10, 11), FIXED 2 (rows 8, 9). No mapping row changes: the key's `table` is correct for all 11.

## The fix (one sentence, in the readers' face)

The readers' standing face gains the sentence "the table is the ONE path component immediately after the tier component ...,
never the file name and never a deeper directory; for an object under `code`, the group directly under `code/`". It is the
grammar's own definition made explicit, stated in `FB-h-1` and `FB-h-2` section 1a.

## Verification (the proof the rule holds)

Two fresh blind readers (`FB-h-1`, `FB-h-2`; the round-4 construction: a one-commit worktree holding only the list) answer
22 locations: the 11 above and 11 CONTROLS both round-4 readers got right (one per class, seeded). `r5_fwd1.py agree`
prints per field agreement and equality with the key for the 11 and the 11 apart. The read is graded by the CVO; the issuer
does not self-grade FWD-1.

## What this does not show

- The 11 are the canonical arm's disagreements at 150 locations; the arm's other 139 are not re-read (11 controls sample them).
- The legacy arm (0 of 150) is unchanged: legacy keys do not follow the grammar and no reader is asked to read them as if they did.
- The readers are subagents of the issuing session on one model; independence is by construction of the tree, as round 4.
- The face now carries the rule, so a reader that obeys it agrees by construction on grammar-conforming strings; the proof that the
  mapping's `table` is the right one for the classes in rows 8-11 is the CTO's ratification of the grain, not this read.
