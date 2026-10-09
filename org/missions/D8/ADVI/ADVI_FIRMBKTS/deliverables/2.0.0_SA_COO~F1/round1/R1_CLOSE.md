# ADVI_FIRMBKTS -- round 1 close: the one real run of FWD-1 (2.0.0_SA_COO~F1, dell1, 2026-10-09 ~21:2xZ)

**Instrument:** `checks/r1_agree.py` over `READING_A.json` (0.9.0_WK_ADVI_FIRMBKTS~2) and `READING_B.json`
(0.9.0_WK_ADVI_FIRMBKTS~3), with the arm map in `mapping.json` that neither reader was given. Output verbatim:
`R1_CLOSE_RUN.txt`; every pair: `R1_CLOSE_PAIRS.json`. A field AGREES when both answers are equal after lowercasing
and dropping non-alphanumerics, and are not `unknown`.

## The result

| arm | locations | system agree | firm agree | tier agree | all three |
|---|---:|---:|---:|---:|---:|
| canonical (`address()` output) | 209 | 209 (unknown in 0) | 209 (unknown in 0) | 209 (unknown in 0) | **209 of 209** |
| legacy (the same objects' legacy keys) | 209 | 66 (unknown in 143) | 107 (unknown in 102) | 209 (unknown in 0) | **19 of 209** |

The canonical arm is FWD-1's ACCEPT on the 209 placed classes: every location named the same system, firm and tier by
both readers. The legacy arm is the endpoint's "today" clause measured: the firm is unreadable in 102 of 209 and
the producing system in 143.

## What the run does not show (stated, not graded)

- **Contents.** Both readers answered by script. Reader A's script described the date partition ("2026 10 08 data")
  where reader B's named the table ("positions cube", "nna atomic"). The table sits in its own slot of every canonical
  string, so this is the reader instrument's weakness, not the location's. Row `ADVI_FIRMBKTS-D1-S3`.
- **Independence.** Reader B opened worker ~1's FB-t-1 proof instance as a format template. The file holds census
  counts, no answer and no arm (row `ADVI_FIRMBKTS-D1-S3`).
- **Coverage.** The run covers the 209 placed classes of 444. The other 235 are 226 FAULT (row
  `ADVI_FIRMBKTS-D1-W1-S2`), 7 RETIRE and 2 DECISION; the table, not the reading, owns them.
- **Collisions.** The table sends more than one legacy class to one destination table (row `ADVI_FIRMBKTS-D1-W1-S3`).

## The round

| order | cell | worker | commit | criteria |
|---|---|---|---|---|
| `TO-FB-t-1` | the key census: 444 classes over 238,861 objects | ~1 | fa437ba675 | AC1 5 of 5, AC2 2 of 2 (live) |
| `TO-FB-t-2` | the mapping table (132 MOVE, 77 HOME, 7 RETIRE, 2 DECISION, 226 FAULT) and a reading list of 418 locations | ~1 (re-seated) | bc064071aa | AC1 5 of 5 |
| `TO-FB-t-3` | reader A, 418 answers | ~2 | ec588145f8 | AC1 2 of 2 |
| `TO-FB-t-4` | reader B, 418 answers | ~3 | 1a188f21fe | AC1 2 of 2 |

`round-close-check.py --project ADVI_FIRMBKTS --round 1`: 4 orders, 4 complete, 4 proofs OK, verdict MAY-CLOSE.

## For the round-N analysis (the issuer's reading, not a cut)

1. The 226 FAULT classes are the table's repair list: mixed classes, logs, backups, markers and leading-slash keys.
   FWD-2 reads each one as a fault in the table, so the remedy is new 1b rows or a finer census grain. No worker should
   decide them.
2. F6 the router repoint (asked early, msg 3113) beside F7's copy of 49 Financial's served keys, built on this table.
3. F4's premise moved (row `ADVI_FIRMBKTS-D1-S1`); its round reads whom the fence admits first.
4. A reader face that cannot see the project folder, for FWD-1's contents clause and FWD-2's second placer.
