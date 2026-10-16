# CT-bf-1 AMENDMENT 2 -- regression sweep, source priority

Denominator: 232 runs = 232 (project, round) pairs from `org/missions/D*/*/*/decompositions/*DECOMP.round<n>.md` over 9 tree
projects (the two `IRPT_CUSTDY_DECOMP.round7.addendum*.md` files are not round files and are excluded, as in every seating).
Each run: `python .tools/round-close-check.py --project <CODE> --round <n>`, timeout 120 s. Result in both sweeps: 0 timeouts,
0 non-zero exits. JUDGMENT lines: 177 criteria in each sweep, the same keys in both.

COMPARISON BASE: the CT-be-1 checker as merged, commit `9a570bb671` (`git show 9a570bb671:.tools/round-close-check.py`), copied
into the worktree for the baseline run and restored to the source-priority rule for the after run, both on the same real
trees on the same day. Not the pre-CT-be-1 tool at `833181d311`, and not the head-anchored code of AMENDMENT 1. Drift control:
the baseline rerun matches the earlier `SWEEP_BEFORE.txt` (the first seating's base) with 0 JUDGMENT and 0 ROUND-CLOSE
differences; only the line order of the file differs.

Files (this folder):

- `SWEEP_BASE_9a570bb671.txt` -- the baseline: the CT-be-1 checker at `9a570bb671`.
- `SWEEP_AFTER_SOURCE_PRIORITY.txt` -- the source-priority rule (committed @038bfea258).
- `SWEEP_CLASSIFIED_SOURCE_PRIORITY.txt` -- `sweep_compare.py` output: every changed line, with the source before and after.
- `sweep_runner.py`, `sweep_compare.py` -- the runner and the comparator (unchanged).
- Earlier seatings, kept as record: `SWEEP_BEFORE.txt`, `SWEEP_AFTER.txt`, `SWEEP_CLASSIFIED.txt` (head-anchored rule),
  `SWEEP_AFTER_FIRST_RULE.txt`, `SWEEP_CLASSIFIED_FIRST_RULE.txt`; `SWEEP_REPORT_AMENDMENT1.md` (the head-anchored report).

## Measured against the base (9a570bb671)

| measure | base | source priority |
|---|---|---|
| runs (projects) | 232 (9) | 232 (9) |
| JUDGMENT readings GRADED / UNGRADED / SELF | 116 / 61 / 0 | 116 / 61 / 0 |
| GRADED -> UNGRADED lines | -- | 0 |
| MET / NOT MET verdict changes | -- | 0 |
| changed JUDGMENT lines (any part) | -- | 5 |
| changed JUDGMENT lines whose grade of record changes SOURCE | -- | 5 |
| ROUND-CLOSE lines that differ | -- | 0 of 232 |
| ROUND-CLOSE verdict changes | -- | 0 |

Acceptance (AMENDMENT 2): zero GRADED->UNGRADED, zero ROUND-CLOSE verdict changes, zero MET / NOT MET reading changes. MET.

## The five changed lines (source only; the verdict is the same on both sides)

Each pair: the two competing CVO rows, id, source file, surfaced_at, verdict. The base picked the investigation row; the
rule picks the adjudication row, because an adjudication row always outranks an investigation row.

1. ADVI_COTBKF round 12, TO-CB-l-1, CB12l1-AC3 -- investigation `ADVI_COTBKF-D2-S24` (INVESTIGATION_v1.md, 2026-10-07T15:05Z,
   NOT MET) displaced by adjudication `ADVI_COTBKF-C-S17` (ADJUDICATION_v10.md, 2026-10-07T15:05Z, NOT MET).
2. ADVI_COTBKF round 53, TO-CB-ba-1, CB53ba1-AC2 -- `ADVI_COTBKF-D2-S81` (INVESTIGATION_v1.md, 2026-10-11T03:22Z, NOT MET)
   displaced by `ADVI_COTBKF-C-S44` (ADJUDICATION_v37.md, 2026-10-11T03:22:00Z, NOT MET).
3. ADVI_COTBKF round 61, TO-CB-bi-2, CB61bi2-AC2 -- `ADVI_COTBKF-D2-S102` (INVESTIGATION_v1.md, 2026-10-11T08:40:26Z, MET)
   displaced by `ADVI_COTBKF-C-S46` (ADJUDICATION_v39.md, 2026-10-11T08:40:26Z, MET).
4. ADVI_COTBKF round 66, TO-CB-bn-1, CB66bn1-AC2 -- `ADVI_COTBKF-D2-S115` (INVESTIGATION_v1.md, 2026-10-11T12:20:43Z, NOT MET)
   displaced by `ADVI_COTBKF-C-S50` (ADJUDICATION_v43.md, 2026-10-11T12:20:43Z, NOT MET).
5. ADVI_COTBKF round 71, TO-CB-bs-1, CB71bs1-AC2 -- `ADVI_COTBKF-D2-S122` (INVESTIGATION_v1.md, 2026-10-11T18:22:31Z, MET)
   displaced by `ADVI_COTBKF-C-S55` (ADJUDICATION_v48.md, 2026-10-11T18:22:31Z, MET).

What the five share: in each pair the adjudication row and the investigation row carry the same verdict and the same
surfaced_at (to the second, or to the minute). The base tie-break (the investigation rows are walked after the adjudication
rows) picked the investigation row. Two of the adjudication rows state the verdict outside `one_line`: `C-S44` in `world_is`
("CB53ba1-AC2 is NOT MET on the manifest damage"), and `C-S55` says its own `D2-S122` "is dismissed as a grade record" and
restates MET in the same row. Both are read as before; the checker's prose reading of an adjudication row is unchanged.

The stop condition in AMENDMENT 2 is not triggered: no MET / NOT MET reading changes, so the five source changes are listed
and not stopped on. They are filed as `NFRA_CTLPLN-W144-S5` (OBSERVATION, INERT) in
`org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md`, for the issuer's ruling on a source
change at a tie of surfaced_at.

## Not in this sweep

- The site Z trees (`NFRA_OPLGTW`) are not in this worktree's sparse checkout, so the site Z case itself is covered by the
  test's planted shape (arm a), not by a sweep run on the real tree.
