# LGIC_NAMING.TO-LN-l-3-r2 -- the cross-bucket scoring -- result

**Worker:** `0.9.0_WK_LGIC_NAMING~6` | **Branch:** `wk-lgic-naming-2-6b` | **Base:** `CLOUD` @8de38d4a930d33ab56335961bf22d114cba6702b | **Cell:** `LN-l-3` (round 2)

**The bar:** the branch printed `wk-lgic-naming-2-6b`, and `test -d org && test -d .tools` printed `TREE-OK`. Every path the order names was present at the base.

**Premises re-grounded:**
- `n5-reader.tsv` is LN-l-2 round 2's committed answer (3fecf3a37f), 7 rows.
- `check_ln_r2.py` `l3_key()` reads round 1's `fixed_inputs/N5_KEY.json`, as the order states.
- The decomp pin 32795c348c and the PRD pin 2706014705 resolve, and each carries its file.

## Acceptance (verbatim outputs)

| id | invocation | deciding output | verdict |
|---|---|---|---|
| L3R-AC1 | `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py l3-correct` | `CONFORMING ADDRESSES: 6  CORRECT: 6  WRONG: 0` / `VERDICT: PASS-ALL-READ-RIGHT`, rc=0 | PASS-by-output, 6 of 6 |
| L3R-AC2 | `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py l3-control` | `NEGATIVE CONTROLS: 1  MARKED DOES-NOT-FIT: 1` / `VERDICT: PASS-CONTROL-FLAGGED`, rc=0 | PASS-by-output, 1 of 1 |

`<WS>` = `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6b`. The shell reached the same directory by its Git Bash form, `/cygdrive/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6b`.

The order has no judgment criteria. Each criterion ran once and did not time out.

## Deliverable

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n5-reader-score.md` holds:
- the checker's output, verbatim;
- the WRONG lines, of which there are none;
- all 7 addresses, each with its label and its expected roles.

## Surprises

None filed. Every premise the order names held, and both invocations produced their named result.

## Proof

`LGIC_NAMING.TO-LN-l-3-r2.layout-scoring.proof_of_spec.json` beside this file, validated with
`python .tools/proof-of-spec-check.py <instance> L3R-AC1,L3R-AC2` before the `complete` flip.
