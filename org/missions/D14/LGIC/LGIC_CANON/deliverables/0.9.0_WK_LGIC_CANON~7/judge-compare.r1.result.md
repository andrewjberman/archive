# LGIC_CANON.TO-CN-j-3 -- result (the judges' comparison, cell CN-j-3, round 1)

Worker: 0.9.0_WK_LGIC_CANON~7 (an L7 worker of 2.0.0_SA_COO~G) - branch `wk-lgic-canon-1-7b`, cut from CLOUD @91b11ff0c9
- worktree `/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-2` (a reused directory; its pre-existing
untracked `.scratch/` belongs to earlier workers and was neither read nor cited; this worker's scratch is `.scratch/j3/`).

The record L9 reads is `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-compare.md`. This file is the
run log beside the proof instance.

## Verdicts

Each criterion was run as the order names it, `cd <WS> && timeout 120 python
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py <sub>`, at HEAD
91b11ff0c9 with both answer files as drained (judge A @172b20639c, judge B @91b11ff0c9). The checker reads the two
answer files and the key and never reads judge-compare.md, so the results do not depend on this worker's writing.
**The checker exits 0 on every verdict. The VERDICT line decides, never the exit code.**

| criterion | output, verbatim | rc | result |
|---|---|---|---|
| J3-AC1 | `AXES: 5  SAME VERDICT: 5` / `VERDICT: PASS-J3-SAME-VERDICTS` | 0 | PASS by output |
| J3-AC2 | `CITATIONS DIFFER: A1  A=['R18', 'R9']  B=['R20', 'R9']` / `AXES: 5  SAME RULE SET: 4` / `VERDICT: FAIL-J3-CITATIONS-DIFFER` | 0 | **FAIL** |
| J3-AC3 | `CASE OFF THE KEY: J-N3  A=OUT-OF-PATTERN  B=OUT-OF-PATTERN  key=ALIAS` / `CASES: 3  BOTH JUDGES ON THE KEY: 2` / `VERDICT: FAIL-J3-CASES-OFF-KEY` | 0 | **FAIL** |
| J3-AC4 | `BASE A: 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae  BASE B: 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae  LEAKS: 0 of 2` / `VERDICT: PASS-J3-MUTUALLY-BLIND` | 0 | PASS by output |
| J3-J1 | judgment: the trace of every disagreement is judge-compare.md section 4 | -- | RECORDED; UNVERIFIABLE-BY-INSTRUMENT, graded at L9 by 3.0.0_SA_CVO |

## The order's state

Two mechanical criteria read FAIL, so the order's `<status>` is **not** flipped and stays `pending`. PRD DEC-2 sends
each disagreement back to CN-k-1 as a canon defect. Each one is filed as a single row:

- `LGIC_CANON-W7-S1`: J3-AC2. On axis A1 the rule sets are R9,R18 (judge A) and R9,R20 (judge B). BLOCKING, INERT.
- `LGIC_CANON-W7-S2`: J3-AC3. Both judges put J-N3 at OUT-OF-PATTERN; the key reads ALIAS. BLOCKING, INERT.

## What this worker read

- the two answer files (`judge-a.tsv` @537f49b8fd, `judge-b.tsv` @98ed3177ff) and the key `CN_JUDGE_NAMING_KEY.json`;
- `infra/logic/02_DOCTRINE.md` in full (576 lines). `git diff --stat 671925aecc 91b11ff0c9` on it is empty, so the
  canon these lines cite is the one both judges read at their base;
- `CN_TREE_MDPF.md`, and `CN_JUDGE_CASES.json` for the case names and node types;
- `check_canon_r1.py` lines 97-114 and 355-457, which show how the four results are computed;
- the key's own source: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` rule R3 (lines 168-173) and the
  section 9 worked case (line 368), read at the key's pin 3cc090827f. `git diff --stat 3cc090827f 91b11ff0c9` on the
  file is empty;
- `infra/logic/registry/scopes.json` lines 40-84, the `bd` alias row;
- channel row `LGIC_CANON-W5-S1`, and judge B's proof instance for its shape.

## Instrument limits, stated and not re-measured

- J3-AC4 reads each judge's base from the `# base` line that judge wrote into its own answer file
  (`check_canon_r1.py:107`, `tsv()`). It does not read the ancestry of the judges' branches. The instrument is the
  cut's, and this worker did not replace it.
- J3-AC2 compares only the `R<n>` ids in each row's third column (`check_canon_r1.py:362`). A rule named only in
  the reason column is not counted. Judge A names R20 for X1 in its A1 reason; its column carries R9,R18.
