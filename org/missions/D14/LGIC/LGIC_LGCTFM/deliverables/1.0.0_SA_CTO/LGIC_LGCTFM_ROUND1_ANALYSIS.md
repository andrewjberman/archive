# LGIC_LGCTFM -- ROUND 1 ANALYSIS (L10)

`1.0.0_SA_CTO`, 2026-09-18 ~03:2xZ. On `3.0.0_SA_CVO`'s L10 slug 97792, L8/L9 committed @`d701ba7c14`; issuance on
decomposition v1.1, drained by `2.0.0_SA_COO~G` and reported at 97780. **First round of this project, so every outcome
is graded here for the first time.**

## THE HAND-OFF RECONCILED, AND THAT IS WORTH SAYING FIRST

`3.0.0_SA_CVO` re-measured the issuing lane's numbers before grading anything against them and they were exact: **14
order files, 84 criteria declared, exactly 14 carrying `judgment="true"`, one per order, no order missing one and none
with two**, every `<expected_criteria>` matching its own declarations, all 14 status words complete. This seat measured
the same set independently before routing and got an exact match in both directions.

**That is the first hand-off tonight that survived a re-measurement**, and it survived it because the issuing lane
PARSED the ids from the order faces rather than retyping them -- explicitly citing this seat's own `S25R4-AC5` error as
the reason. Two earlier hand-offs did not survive the same check.

## OUTCOME VERDICTS -- 10 of 10 graded, every outcome carried by at least one cell

Cell coverage measured from the order faces: FWD-1 five cells, FWD-2 one, FWD-3 three, FWD-4 three, FWD-5 one, FWD-6
two, FWD-7 two, FWD-8 two, FWD-9 one, FWD-10 one. **No outcome is uncovered.** All 14 criteria PASS.

| outcome | bar | verdict | why |
|---|---|---|---|
| FWD-1 one contract for a named subject | EXERCISED, run on the first real subject | **REALIZED** | run on `blackdiamond`/`49financial` twice; the contract exists, 184 rows / 179 tensions, read by seats other than its author |
| FWD-2 every fork named with its one job | EXERCISED, first run over a subject carrying known forks | **REALIZED** | `LT-e-2` settled the hard half with a NEGATIVE that cannot be faked -- a zero-hit search showing the engine never opens `FORK_CONTROLS` at all, so the seeds are not the control pairs |
| FWD-3 desired beside current, reproducible | EXERCISED, reproduced by a NON-AUTHOR | **REALIZED** | `LT-v-1`'s reproduction was done by a slot that wrote none of the engine -- 20 of 184 callable rows re-derived exactly, all five verdict kinds spanned |
| FWD-4 a typed, ranked list ANDREW HAS READ | EXERCISED, **Andrew has read the list** | **APPLIED, NOT REALIZED** | the card was delivered to him at ~00:36Z and he has not read it. This seat adjudicated on his unavailability @`662d53b793` under his own ~23:5xZ word, and **an adjudication on his behalf is not his read** |
| FWD-5 a flow picture regenerated after an edit | EXERCISED, contract edited and picture regenerated | **REALIZED** | `LT-r-1` |
| FWD-6 the work plan comes out of the run | EXERCISED, **a real migration's decomposition cut from it** | **NOT REALIZED** | `LT-p-1` and `LT-s-2` PASS and the plan exists, but no migration decomposition has been cut from it. The bar names an act no round-1 cell performed |
| FWD-7 the run MARKS the subject; a planted change is refused | EXERCISED, a planted change refused | **REALIZED** | `LT-x-2`'s mutant still refuses -- and **stops naming `ADVI_FIRMBKTS`**, which is the opposite of what a shaped-to-trip string would need; the DEC-9 marks are in the registry at `53d59778a1`, an ancestor of HEAD |
| FWD-8 a second run shows what moved | EXERCISED, two runs compared | **REALIZED** | two real waves on a live subject with a committed diff: CLOSED 0, OPENED 1, UNCHANGED 179 |
| FWD-9 same subject, same pin, same answer | EXERCISED, **with its own negative control fired** | **REALIZED** | `LT-d-1`'s determinism suite, its negative control fired |
| FWD-10 the instrument moves nothing | EXERCISED, measured after the first real run | **REALIZED** | `LT-x-1`, re-handed; nothing in the cloud and nothing served moved |

**Round summary: REALIZED 8 of 10; APPLIED-not-realized 1 (FWD-4); NOT REALIZED 1 (FWD-6).** The project is NOT CLOSED.

⛔ **FWD-4 AND FWD-6 ARE NOT FAILURES OF THIS ROUND AND MUST NOT BE RE-CUT AS IF THEY WERE.** Each bars on an act
outside the engine: a human READ, and a real migration's decomposition. The instrument is built and exercised; what is
missing is a use of it. Cutting more engine cells would move neither.

## THE THREE FINDINGS, and one of them reaches my own adjudication

`3.0.0_SA_CVO` filed these rather than folding them into verdicts, which is the right disposition and is why they are
actionable here.

**S10 -- two arms that can only pass where passing proves nothing.** `LT-x-1`'s `x1-r16` and `x1-footprint` are
BRANCH-RELATIVE: on the shared tree they print "paths changed on this branch: 0" and "commits touching the three
registries: 0" where the instance recorded 14 and 1. The other twelve reproduce identically off-branch, so it is these
two and not the checker. ⛔ **This is the INVERSE of the known repetition trap and a sharper statement of it than R-40
carries: R-40 says a check must bind to the object's identity; S10 says a check must also be RUNNABLE WHERE THE CLAIM
IS CONSUMED. An arm that passes only in the worker's own checkout certifies the checkout, not the work.** Round 2
re-cuts both against the shared tree.

**S11 -- three numbers naming no run, two of which disagree.** `P1R1-AC6` cites 1626 packages, `X1R1-AC6` cites 1074,
and `E3R1-AC6` grades 271 tensions and 1084 cells against a contract that now carries 179. **`E3`'s population no
longer exists anywhere.** `3.0.0_SA_CVO` graded E3 **PASS AT ITS OWN VINTAGE** and declined to grade it against R-40,
which this seat issued AFTER that cell ran. **That refusal is correct and I am ratifying it explicitly: a standing bar
binds the cuts that follow it, never the work that preceded it.** Applying R-40 retroactively would convert a rule into
a trap. The gap is the ROW, not the verdict, and round 2 carries the run-id.

**S12 -- `ANDREW_CARD.md` NAMES NO RUN, and this one reaches the adjudication I made on Andrew's behalf.** A run-id
regex over the card returns zero matches; it identifies its subject only as "graph built 2026-09-17 18:16 UTC".
**FIVE run directories exist under that subject, and one carries 180 tensions with `live == 2` where the others carry
179 and `live == 1`.** The card's 179-row order is the only thing pinning it away from that run, and nothing in the
card says so.

⛔ **MY ADJUDICATION IS AMENDED HERE RATHER THAN LEFT TO STAND ON THAT PIN.** What I verified was a specific run --
`contract.json` hashing `84d4d1e62b`, 179 tensions, `client_facing == 1`, `live == 1`, `irreversible == 0`. **That
measurement is unchanged and the adjudication's substance stands.** What was missing is that the CARD does not say
which run it ranks, so a later reader could bind it to the 180-tension run and get a different top-priority
population -- **`live == 2` there, which is exactly the "two rows" the card's recommendation wrongly claimed.** The
coincidence is worth naming: the card's wrong sentence is the RIGHT sentence for a DIFFERENT run under the same
subject. **A card that names no run cannot be checked against the run it ranks**, and round 2's card carries its run id
and contract hash on its face.

## ROWS: 16 items, 0 undispositioned, 9 graduated, FOUR DISARMS -- none taken on the row that asserts it

`W2-S1` is this seat's and disarms on **R-35**, verified by `3.0.0_SA_CVO` on the gate's own `_is_record_tree`: True
for the run directory's artifacts, False for `workflows/legacy_transform/run_home.py`, with a registry path as a
negative control. **The exemption reaches the minted run directory and deliberately not the engine-code tree above it,
which is what R-35 says and what a prefix exemption would have broken.** `W2-S2` disarms because R-36 fixed the enum
at its root rather than widening the vocabulary to admit the defect. `S3`'s cure was verified by RECOMPUTING all 8
declared hashes under the manifest's own instrument -- 0 mismatches, `MARK.json` tracked for the first time.

## WHAT ROUND 2 CARRIES

1. `S10`'s two branch-relative arms, re-cut to run where the claim is consumed.
2. `S11`'s run-ids on every number; `E3` is NOT re-graded against R-40.
3. `S12`: the card names its run id and contract hash on its face.
4. FWD-6's bar met by a REAL migration decomposition cut from the plan -- which is `LGIC_CANON`'s C6 practice wave, not
   another engine cell.
5. FWD-4 closes on **Andrew's own read**, whenever he gives it; my adjudication stands in the meantime and he may
   overturn any part of it.

## THE ROUND'S OWN HEADLINE, kept because the issuing lane wrote it and it is better than a clean summary

*"A slug that reads clean is worth less than one that says where it bent."* Three of that lane's checker arms were
defective and **all three were UNSATISFIABLE BY A CORRECT FIX** rather than merely blind. All three passed their
INJECTED self-tests, because a fixture written by the arm's author shares the arm's assumption. **The control it
derived is the mirror of the mutant test and is adopted estate-wide: before the cut, run the arm against a SIMULATED
CORRECT FIX and require PASS.** A mutant proves an arm can fail; this proves it can pass for the right reason.
