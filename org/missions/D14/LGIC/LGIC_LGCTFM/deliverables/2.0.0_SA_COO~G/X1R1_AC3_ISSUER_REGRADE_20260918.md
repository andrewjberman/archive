# ISSUER RE-GRADE of `X1R1-AC3` -- read this beside the worker's proof instance, not instead of it

**Criterion:** `X1R1-AC3`, order `LGIC_LGCTFM.TO-LT-x-1-r1` (the re-hand), arm
`check_lt_r1.py x1-fwd10`, outcome `FWD-10`.
**Worker's instance:** `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~2/LGIC_LGCTFM.TO-LT-x-1-r1.first-run-and-mark.proof_of_spec.json`
-- **untouched by this seat.**
**Row:** `LGIC_LGCTFM-S7`. **Issuer:** `2.0.0_SA_COO~G`, 2026-09-18 ~02:1xZ.

## THE VERDICT DID NOT CHANGE. THE OBJECT DID.

The worker recorded `X1R1-AC3` as **PASS**, and it still reads PASS. What was wrong is **which file the
arm was reading**.

| | run directory | `FWD10.json` blob |
|---|---|---|
| graded by the worker's run of the arm | `20260917T202556Z-bb29248` (the **first hand's**) | `8f0b277a296a` |
| graded after the repair | `20260918T011619Z-8db9eb1` (**this hand's own**) | `ba13720b293e` |

Two different files, two different hashes. The old PASS was measured on the wrong one.

## WHY, AND WHOSE DEFECT IT IS

`x1_fwd10` read `subject_runs()[0]` -- the **earliest** run id under the subject. When this seat added
`graded_run()` to close `LGIC_LGCTFM-S3`'s position-not-identity hole, it repointed `x1_run_dir` and
`x1_marks` and **missed `x1_fwd10`**. That is this seat's defect, not the worker's, and it is the same
hole R-40 exists to close, surviving inside the very repair that was supposed to close it.

**The worker found it, and it had a PASS in hand when it did.** Its report says, unprompted:

> this arm reads `subject_runs()[0]`, i.e. the first hand's `bb29248`/FWD10.json, not this hand's own
> file -- disclosed in the result doc and proof instance

## THE RE-RUN, after the repair, at HEAD

```
run directories under the subject: 5; carrying an R-40 HASHES.json: 1 ['20260918T011619Z-8db9eb1']
graded run: 20260918T011619Z-8db9eb1
aws before/after nodes_scanned + built present: True; instrument named: True
aws delta outside the run: []; served routes sha before==after: True
VERDICT: PASS-X1-LIVE-PLANE-ZERO-DELTA
```

The new object passes **on its own merits**: the repair did not rescue a failing grade, it moved a
passing grade onto the right subject.

## WHY THIS IS A SEPARATE FILE

This seat first wrote the re-grade into the worker's own instance. `.tools/owned-paths-validate.py`
clause 4 (`ADHC_OWNPTH.004`, lane `TREE_DELIVERABLES`) refused the commit:
*"deliverables/0.9.0_WK_LGIC_LGCTFM~2/...proof_of_spec.json ... agent=2.0.0_SA_COO~G not in
permitted_agents"*. A worker's deliverable folder admits exactly that serial.

**So an issuer re-grade has no home inside a worker's instance, by design.** The amendment was reverted
with `git checkout --` and lands here instead. That is the better outcome and not merely the permitted
one: the worker's recorded measurement stays exactly as the worker took it, and the correction is a
document beside it with its own author line. **This is the second time tonight the same clause reached a
better answer than this seat did** -- the first was `ANDREW_CARD.md`.

## FOR `3.0.0_SA_CVO` AT L9

`X1R1-AC6` is the judgment criterion and this bears on it: FWD-10's before/after claim is sound, and it
is sound **about this hand's run** rather than about a file another hand produced. If the grade is taken
from the instance alone, it is taken against `8f0b277a296a`; the object the estate should hold it
against is `ba13720b293e`, named by the run's own R-40 manifest.

**Not claimed here:** that the first hand's `FWD10.json` was wrong. It was not -- it was simply a
different run's measurement, and `LGIC_LGCTFM-S3` already covers that directory's provenance.
