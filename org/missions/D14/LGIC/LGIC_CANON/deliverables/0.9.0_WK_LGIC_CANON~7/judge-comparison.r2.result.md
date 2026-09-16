# LGIC_CANON.CN-j-7-r2 -- judge-comparison -- result log

**Worker** `0.9.0_WK_LGIC_CANON~7` | **branch** `wk-lgic-canon-2-7` | **base** `7db18a4464` |
**artifact commit** `fe4cf74eb662e64a99cf42775bbf33c05edcf247` | **date** 2026-09-16

## 1. First act -- the bar

```
git rev-parse --abbrev-ref HEAD   -> wk-lgic-canon-2-7
test -d org && test -d .tools     -> TREE-OK
git rev-parse HEAD                -> 7db18a4464c44774f747f9ef0b43fb3a51fbc99c
```

Premises re-grounded against live state before any work: the three judge TSVs exist at the named paths
(13 / 13 / 7 data rows); `check_canon_r2.py` carries the repaired `j_reach` (it reads the `reach` column by
header and prints a `DISCLOSED:` line where the old whole-row scan would differ -- seen on `j5-reach` and
not on `j4-reach`, which is exactly what rows `LGIC_CANON-W5-S2` and `LGIC_CANON-S9` describe).

**One premise did NOT hold and is row `LGIC_CANON-W7-S4`:** the cell asks for E's divergence from C and D,
and the three judges did not judge one tree. See section 4.

## 2. Criteria, verbatim output

```
J7-AC1  python .../check_canon_r2.py j7-traced
        disagreement rows, denominator 6; rows tracing to no canon coordinate: 0
        NOTE: zero disagreement rows is NOT a pass -- the comparison must have run.
        VERDICT: PASS-J7-EVERY-DISAGREEMENT-TRACED                      rc=0

J7-AC2  python .../check_canon_r2.py j7-reach
        A-13's seven, denominator 7; named in the comparison: 7 ['R3', 'R8', 'R14', 'R15', 'R17', 'R19', 'R21']
        the comparison prints a NOT REACHED partition: True
        VERDICT: PASS-J7-SEVEN-RULE-REACH-PRINTED                       rc=0

J7-AC3  python .../check_canon_r2.py j7-blind
        judge pairs, denominator 6; pairs where one file names the other: 0 []
        VERDICT: PASS-J7-JUDGES-MUTUALLY-BLIND                          rc=0

J7-AC4  python .../check_canon_r2.py j7-e-vocab
        distinct verdict values in judge E's output, denominator 4: ['CONFORMS', 'DECLARED-EXCEPTION', 'UNDETERMINED', 'VIOLATES']
        of those, NOT carried by the canon E read (whole-word): 0 []
        a value E used that the canon does not carry means E did not get it from the canon
        VERDICT: PASS-J7-E-VOCAB-FROM-CANON                             rc=0

J7-J1   judgment="true" -- RECORDED, NO VERDICT. Graded at L9 by 3.0.0_SA_CVO.
```

Each was run twice: on the working copy and again on the committed bytes at `fe4cf74eb6` after the mutant
controls were restored. Identical verdicts and denominators both times.

## 3. Controls

**Mutant A** (first `DISAGREE` row's canon coordinates neutralised): `rows tracing to no canon coordinate: 1`,
`FAIL-J7-EVERY-DISAGREEMENT-TRACED`. **Mutant B** (the literal `NOT REACHED` broken, all seven ids left in
place): `named in the comparison: 7 [...]` with `FAIL-J7-SEVEN-RULE-REACH-PRINTED` -- the naming limb still
full while the partition limb fails, which is what isolates the two limbs. **Restore proven by bytes, not by
re-running the checker:** sha256 `f6ddbdbde90934254ff29d38d71e48cd6ce4b459782ff47b4569b75fb86508f7`, 20881
bytes, byte-identical to the pre-mutant copy, `git status --porcelain` empty on the path.

**Independent derivation** (removed from the proof instance because `controls` is a closed object and the
schema refused a third key -- recorded here instead, where it can still be read): every number in the
deliverable was computed from the three TSVs by a scratch Python parser in this worktree's `.scratch/`,
which shares no code with `check_canon_r2.py` and which the checker does not read. It agrees with the hand
reading on all of: 65 axis cells, 59 identical, 6 split at (row 2 A5), (row 3 A3), (row 4 A5), (row 5 A2),
(row 6 A2), (row 7 A1); reach per judge's own column C `[R14, R17, R19]`, D `[R14, R17, R19]`, E `[R14, R19]`;
E's per-axis roll-up A1 UNDETERMINED, A2 VIOLATES, A3 VIOLATES, A4 UNDETERMINED, A5 VIOLATES. The checker's
own `j4-reach` and `j5-reach` print the same 3 of 7 for C and D on a different instrument.

## 4. What the comparison found

- **C versus D:** 59 of 65 axis cells identical, 6 split, no plane split twice, every split adjacent on the
  canon's severity order. The six trace to four canon coordinates, two of them reached twice (D1/D3 are one
  R10 hole; D4/D5 are one unresolved firm-bucket identity). Nothing was adjudicated.
- **Reach:** C and D agree exactly, 3 of 7 reached (R14, R17, R19), 4 of 7 NOT REACHED (R3, R8, R15, R21).
  E, on the other tree, 2 of 7 (R14, R19). The second tree bought exactly one rule over round 1's: R17.
- **The arm:** E does not diverge -- 5 of 5 against round 1's judges A and B on the tree all three judged,
  on the same facts and registers. The deliverable states that answer WITH its three measured limits, because
  `J7-J1` asks that a no-divergence finding not be read as proof of agreement it did not test.

## 5. Rows filed

| id | class | standing | what |
|---|---|---|---|
| `LGIC_CANON-W7-S4` | OBSERVATION | INERT | The cell asks E-versus-C/D; C and D judged CN_TREE_INFLECTION (13 planes) and E judged CN_TREE_MDPF (7 planes), intersection zero, so that divergence has no denominator. Both comparisons delivered and labelled. |
| `LGIC_CANON-W7-S5` | OBSERVATION | INERT | `CN_SEVERITY.md` claims to be "the only thing that separates the two arms"; measured on the outputs the severity ORDER was exercised by neither arm (ranking statements C 0, D 0, E 0 against round 1's A 1, B 2). Bounds how the no-divergence finding may be read. |

Neither is ARMED, so neither carries a `disarm_owner`. Both are `UNDER_INVESTIGATION` for `3.0.0_SA_CVO` at L9.

## 6. Bounds honoured

No fixed input read-only file was edited (the two mutants ran on this worker's own artifact and were
restored to byte identity). Nothing outside `<paths>` plus this deliverables folder plus the order's own
`<status>` line was written. No push, merge, rebase, `checkout --` or `clean`. Scratch stayed in this
worktree's `.scratch/`.

## 7. Proof

`org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~7/LGIC_CANON.CN-j-7-r2.judge-comparison.proof_of_spec.json`
validated `VALID (rc=0)` with
`python .tools/proof-of-spec-check.py <instance> J7-AC1,J7-AC2,J7-AC3,J7-AC4,J7-J1`
before the `complete` flip. 4 of 4 mechanical criteria PASS by output; `J7-J1` recorded
`UNVERIFIABLE-BY-INSTRUMENT` for `3.0.0_SA_CVO` at L9.
