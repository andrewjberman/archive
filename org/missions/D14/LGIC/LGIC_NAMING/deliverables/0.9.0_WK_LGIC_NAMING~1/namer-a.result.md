# LGIC_NAMING.TO-LN-e-1-r3 -- namer A, round 3, in a clean-context seat -- result

**Worker (seat operator):** 0.9.0_WK_LGIC_NAMING~1 | **Branch:** wk-lgic-naming-3-1 | **Base:** 6705066c68d253c2c8c6559916141fd6ce1ccc79 (NAMING_SCHEMA.json v1.7 there)

**The blind party** was a `claude -p` session with no tools. `blind_seat.py run e1` (fixed input `deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/blind_seat.py`) ran it once. The printed line was:

```
SEAT: OK cell=e1 rows=18 session=11cdb5f4-3285-4f8a-961e-f8795c4c1756 base=6705066c68 Q1='unknown' Q2='unknown'
```

- Seat folder: `C:/Users/AndrewBerman/AppData/Local/Temp/opal_blindseat_r3_e1_lhkou35j`. It was outside the workspace and in no repository. It held 0 files before and after the run, and no CLAUDE.md sat up its parent chain (`e1.seat.json`).
- Prompt: sha256 `5dbd254833e4fc538099f692b7f62c02c774f2e15bc1f0902b4594cda956d0fe`, 47426 bytes.
- Reply text: sha256 `47cda3fa748659b73c43e9b6e254ad243ca2ca63423ee6820c74ff260a78d1bc`. The session took 1 turn, returned rc 0 with is_error false, and ran 2026-09-15T07:11:44Z to 07:12:32Z.

**Output:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-namer-a.tsv` names 18 of 18 items, with 0 RAISE. The seat's five files are under `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/seats/e1.*`. No file was written or edited by hand. `git check-attr` reads `binary: set` on `e1.prompt.txt`, from the root `.gitattributes` rule `exercises/r3/seats/** binary`.

**A measured fact, not graded here:** round 3's reply is byte-identical to round 2's. `sha256sum` gives `47cda3fa...d1bc` for both `exercises/r3/seats/e1.answer.txt` and `exercises/r2/seats/e1.answer.txt`, and `diff` of the two `n3-namer-a.tsv` bodies (the `#` header lines removed) exits 0. Only the prompt changed: 29825 bytes at round 2 (v1.6 plus the seed) and 47426 bytes at round 3 (v1.7 plus the three registry files). LN-e-3 and 3.0.0_SA_CVO decide what this means.

## Criteria (mechanical; the checker's output grades them)

| id | invocation | deciding output | rc |
|---|---|---|---|
| E1T-AC1 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e1-seat` | `SEAT CONDITIONS: 10  HELD: 10  NOT HELD: []` / `VERDICT: PASS-CLEAN-SEAT` | 0 |
| E1T-AC2 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e1-canary` | `CANARY ANSWERS: 2 of 2  WORKSPACE-ONLY FACTS IN THE REPLY: 0 of 2` / `VERDICT: PASS-CANARY-BLIND` | 0 |
| E1T-AC3 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e1-named` | `ITEMS: 18  NAMED (a RAISE is an answer): 18  MISSING: []` / `VERDICT: PASS-ALL-NAMED` | 0 |
| E1T-AC4 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e1-v17` | `BASE: 6705066c68...  NAMING_SCHEMA.json version there: v1.7` / `VERDICT: PASS-BRIEFED-ON-V17` | 0 |

## Surprise filed

- `LGIC_NAMING-W1-S7` (OBSERVATION, INERT). The order names this file, `namer-a.result.md`, beside the instance. That path already held round 2's result for the complete order TO-LN-e-1-r2 (written @eaafb46486, amended @e8490dcbfb). Writing it as ordered replaces round 2's record at HEAD. The round-2 instance pins the file to eaafb46486, so that pin still resolves to round 2's bytes. Nothing else was changed.

Row LGIC_NAMING-S15 discloses i05, so nothing was done about it. Whether the two namers agree is for LN-e-3 to measure; this worker does not grade it.
