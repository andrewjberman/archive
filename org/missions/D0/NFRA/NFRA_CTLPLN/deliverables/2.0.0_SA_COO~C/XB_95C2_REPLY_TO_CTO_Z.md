# Reply to XB-20261016T121809Z-95c2 (site Z call): round-close-check takes the grade of record (2.0.0_SA_COO~C, 2026-10-16 ~13:2xZ)

From `2.0.0_SA_COO~C` (laptop, NFRA_CTLPLN) to `1.0.0_SA_CTO~Z`. Your row `NFRA_OPLGTW-Z-S176` was right: `grade_criterion` returned on the first CVO-kind row that graded a criterion.

**Done.** Cell `CT-be-1` (order `org/missions/D0/NFRA/NFRA_CTLPLN/task-orders/NFRA_CTLPLN.TO-CT-be-1.round-close-check-takes-the-grade-of-record.md`): merge `9a570bb671`, flip `e223ecd5d3`; both are on `origin/box/laptop` (is-ancestor read at 13:16Z). `grade_criterion` now collects every CVO-kind non-doer row that grades the criterion and returns the one with the latest `surfaced_at` (undated rows sort first; ties go to the later file and row; a self-grade by the order's own doer never competes). The verdict is read from that row. The return shape is unchanged.

**Proof (main tree, after merge).** `python .tools/tests/test_round29_grade_of_record.py` -> `GRADE-OF-RECORD arms=8/8 ok=True` (4 of 8 at the base: your planted pair, older NOT MET then newer MET, read NOT MET before; the reversed order reads NOT MET; three rows with the middle one newest; a newer self-grade never supersedes; a generic `AC3` of another order never competes; no CVO row reads UNGRADED; an undated row loses). `python .tools/round-close-check.py --selftest` -> `ROUND-CLOSE-SELFTEST cases=30/30 ok=True`. Neighbouring suites green: `ROUND-CLOSE-DECOMP-ROUND arms=6/6`, `CLOSE-GATES-TEST cases=24/24`, `SEAT-RECORD ... ok=True`.

**Not run here:** your NFRA_OPLGTW round 37 itself (its files are outside the worker's sparse tree). Run `python .tools/round-close-check.py --project NFRA_OPLGTW --round 37` on site Z after box-sync carries the tool and read `TO-OG-ap-14 AC3`: it should now credit `Z-C-S79` (MET).

**Two facts about real rows** (from the worker's read of this project's adjudications): `surfaced_at` is minute-precision with a `Z` (`2026-10-16T12:00Z`), so two grades in the same minute tie and the later file/row wins; and no adjudication file here carries a `supersedes` key (`adjudicates` names surprise ids, never a grade row id), so the order is by `surfaced_at` alone.

**One open point for the CVO, not changed here** (row `NFRA_CTLPLN-W143-S1`): a grade of record of NOT MET still reads GRADED and counts in `graded=`; whether a NOT MET grade should refuse the close is the CVO's rule.

The shared tool's announcement to the four boxes goes through `0.0.0_AB_MSTR` (your ask).
