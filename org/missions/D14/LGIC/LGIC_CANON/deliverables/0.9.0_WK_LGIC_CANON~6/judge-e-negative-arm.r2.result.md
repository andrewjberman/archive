# LGIC_CANON.CN-j-6-r2 -- result (cell CN-j-6, round 2, judge E, the negative arm)

**Worker:** `0.9.0_WK_LGIC_CANON~6` · **Branch:** `wk-lgic-canon-2-6`, cut from CLOUD at `49b4a5b74a`.

## Premises re-grounded

- `org/` and `.tools/` both present in the worktree (TREE-OK).
- `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/` did not exist before this cell; created here.
- The task order file at HEAD (`org/missions/D14/LGIC/LGIC_CANON/task-orders/LGIC_CANON.CN-j-6-r2.judge-e-negative-arm.md`)
  carries no `SEVERITY ORDER` phrase and none of the canon's five axis-verdict words -- confirmed both by direct
  read and by the checker's own `j6-noseverity` subcommand before any work began.
- No other judge's file (`judge-c.tsv`, `judge-d.tsv`) exists anywhere in this worktree; none was read.

## What was done

Read `org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_TREE_MDPF.md` (round 1's
MDPF tree, unchanged, 7 storage planes P1-P7 plus the section-2 credential-read fact and the section-3 compute
fact) and `infra/logic/02_DOCTRINE.md` (the canon, v1.1) in full. Judged each of the 7 planes on all 5 axes
(A1 INGESTION, A2 BUCKET STRUCTURE, A3 NAMING, A4 COMPUTE, A5 FORMAT) using only the canon's own closed axis
vocabulary (`CONFORMS`, `DECLARED-EXCEPTION`, `DEPARTS-RECOMMENDED`, `UNDETERMINED`, `VIOLATES`) -- no ranking
of those words against each other was used to decide any cell; the task order's own brief carries no severity
order and none was consulted. Wrote
`org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-e.tsv` (header `plane A1 A2 A3 A4 A5 rules
reach why`, 7 data rows), citing at least one canon rule per row and, where the canon's own census already
named the exact plane (by matching object count or address), citing that census line directly (R4's
`opal-data-mdpf/mdpf/bronze/ 830`; R5's `opal-data-assets/gold/ 502` and `portal/gold/ 415`; R6's 13-object
`opal-data-portal-v2/platinum/mdpf/{...}/`). Verdict summary across the 7 planes x 5 axes (35 cells):
`CONFORMS` 4, `DECLARED-EXCEPTION` 2, `VIOLATES` 8, `UNDETERMINED` 21, `DEPARTS-RECOMMENDED` 0.

## Criteria: baseline and after

| id | before this file existed | after |
|---|---|---|
| J6-AC1 | `FAIL-J6-EVERY-AXIS-JUDGED` (MISSING INPUT: no `judge-e.tsv`) | `PASS-J6-EVERY-AXIS-JUDGED` -- denominator 7, 0 rows short an axis |
| J6-AC2 | `FAIL-J6-EVERY-VERDICT-CITES` (MISSING INPUT) | `PASS-J6-EVERY-VERDICT-CITES` -- denominator 7, 0 rows uncited |
| J6-AC3 | n/a -- reads the task-order file, not this artifact; already `PASS-J6-SEVERITY-WITHHELD` before any work | `PASS-J6-SEVERITY-WITHHELD` (unchanged; confirms the brief stayed clean) |

As a sanity check only (not part of this cell's own acceptance, and not self-graded here), `j7-e-vocab` --
CN-j-7's actual measurement of whether E's verdict values are the canon's own words -- was also run against the
committed artifact: `PASS-J7-E-VOCAB-FROM-CANON`, all 4 distinct values used (`CONFORMS`, `DECLARED-EXCEPTION`,
`UNDETERMINED`, `VIOLATES`) occur whole-word in the canon E read.

## Mutant control

Two mutants, each on the committed file, each restored before the next:

- **Mutant A** -- blanked P1's A3 cell. `j6-axes` read `FAIL-J6-EVERY-AXIS-JUDGED`, denominator 7, 1 row short
  (`P1 ...`). Fired as expected.
- **Mutant B** -- replaced every `R<digit>` token in P1's row with the literal `RULE` (all 9 columns). `j6-cites`
  read `FAIL-J6-EVERY-VERDICT-CITES`, denominator 7, 1 row uncited (`P1 ...`). Fired as expected.

Restored from the pre-mutant copy after each; the restored file's sha256
(`08ff82ebef281e1143993426fd8ac4f7bdeb6227885ee2b2314832a22d501e1c`) is identical to the file as committed at
`8f82074af9`, and `git status --porcelain` on the path is empty after restore.

## Determinism

All three criteria (`j6-axes`, `j6-cites`, `j6-noseverity`) run twice in immediate succession on the restored,
committed bytes: identical verdict lines and denominators both times.

## Choices this worker made, for the record (not asked, since a worker cannot ask)

- The credential read (tree section 2, the Orion JWT) and the compute facts (tree section 3, the Lambda and EC2
  node) are not separate "planes" in the tree's own section-1 table, so they were folded into the nearest plane
  each bears on (P1's A1 for the credential read; every gold-tier plane's A4 for the compute ambiguity) rather
  than invented as extra rows.
- P6 (three firms under one row) reads `VIOLATES` on A2 as a single word, because two of the three firms carry
  no register entry and the canon's own R6 census tags this exact address `VIOLATED-LIVE`; the narrower,
  CONDITIONAL carve-out for 49financial's `category-views.json` (X7) is named in the `why` cell rather than
  changing the single verdict word, since the axis-verdict vocabulary is closed to one value per cell and
  `j7-e-vocab` checks each cell as a single whole-word match against the canon.
- P3 (the empty, correctly-homed gold plane) reads `CONFORMS` on A2 from the address alone (bucket + tier match
  R5), while every other axis on P3 reads `UNDETERMINED` because no object exists there to test format, the
  full key, or a compute transition.

## Rows filed

None. Nothing reached this worker from outside the canon or the tree; no fixed input was defective; no path
outside the grant was needed.
