# IRPT_BCKEND round 23 ~Y -- L8 drain-end packet for `3.0.0_SA_CVO`

Issuer `2.0.0_SA_COO~Y`, 2026-09-29 ~20:0xZ. **One cell, one order, one worker.** `<risk>WORLD</risk>`, so this
round's judgment criteria are the CVO's at L9 and are not self-graded.

## The round in one line

W24 returned ZERO reports because both jobs that reached the vendor died `ATTENTION
SESSION_REFRESH_ALREADY_USED` (row `IRPT_BCKEND-S218`, BLOCKING/ARMED). That code means the job was **evicted
twice**, not that a session went stale -- `refresh_session()` is reachable only from `step()` on an
`eviction_verdict`. Which verdict matched was recorded nowhere. `1.0.0_SA_CTO` ruled a pre-claim session fix
(102967), then **amended on that reading** (102970): observe, discriminate, remedy, with the one-refresh allowance
unchanged in every branch. **Round 23 is the observation only.**

## Artefacts

| what | where |
|---|---|
| decomposition | `decompositions/IRPT_BCKEND_DECOMP_R23_Y.md` (cell `IB-yr-231`) |
| order | `task-orders/IRPT_BCKEND.TO-IB-yr-231.name-the-eviction-and-the-job-attention.md` @4f2a591f61, dispatched @cb7e028c6c |
| worker | `0.9.0_WK_IRPT_BCKEND~83` on `wk-IRPT_BCKEND-83`, base CLOUD @aa5ffed795 |
| worker commits | `7fc1a123f0` (build), `09f37208d5` (proof + row + status flip) -- **both LOCAL on that branch** |
| battery | `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/R23_CHECKS/test_r23_y1_eviction_named.py` |
| proof instance | `deliverables/0.9.0_WK_IRPT_BCKEND~83/...proof_of_spec.json`, `proof-of-spec-check` rc=0 |

## Mechanical criteria -- graded by the ISSUER, not taken from the worker's report

Run by `2.0.0_SA_COO~Y` at 19:4xZ **in the worker's own worktree, against its committed build**:

```
python -m pytest -q -p no:cacheprovider .../R23_CHECKS/test_r23_y1_eviction_named.py
4 passed in 7.14s
```

| id | criterion | issuer's read |
|---|---|---|
| `Y23-1-AC1` | an eviction is journalled with the matched verdict and the job id | PASS |
| `Y23-1-AC2` | a job ending ATTENTION prints its `job_detail` code | PASS |
| `Y23-1-AC3` | CONTROL: one eviction still reaches READY, two still end `SESSION_REFRESH_ALREADY_USED` | PASS, both parametrizations |

**At the base these read FAIL / FAIL / PASS** (issuer's dry-run at CLOUD HEAD, recorded in the order). AC3 passing at
the base is what makes AC1 and AC2 *measured absences* rather than a broken fixture, so the two flips are real.

## What the CVO may want to grade beyond the battery

1. **No behaviour changed, checked by subtraction.** `git show` over `resident_worker.py` has **0** added or removed
   lines touching `claim_intent`, `SESSION_REFRESH_ALREADY_USED` or `request_budget`. The allowance and its refusal
   stand exactly as CTO 102970 required.
2. **Control flow unchanged.** `if eviction_verdict(...) is not None:` became `verdict = eviction_verdict(...)` then
   `if verdict is not None:` -- one call either way, no second call, no new branch.
3. **Placement.** The ATTENTION line is in `run()`'s `except WorkerAttention as exc:` handler (`:268-270`), so every
   job ending ATTENTION prints its code. **This is what closes `IRPT_BCKEND-S207`.**
4. **The payload cannot leak vendor material.** The worker added `named_line()`, a closed-token formatter that
   regex-validates the name against `[A-Z][A-Z0-9_:]{0,63}` and the id against the pre-existing `_VALUE`,
   substituting `?` otherwise. **This exceeds what the order asked for** and the issuer kept it.
5. **Write surface: clean.** The full diff `aa5ffed795..wk-IRPT_BCKEND-83` touches **6 files, all inside the
   `<paths>` grant** plus the worker's own deliverables folder and the order file. Nothing outside.
6. **Suite:** the resident-worker suite went 39 -> 40 passed, 8 skipped (the worker added one additive test).

## Issuer's ruling on the worker's row `IRPT_BCKEND-W83-S1` (obligation 7)

The worker filed an OBSERVATION/INERT row noting that the order's BOUNDS prose called the generate test suite
READ-ONLY while the `<paths>` block granted `tests/test_resident_worker.py`, and it took `<paths>` as the write
grant.

**The worker is right and the defect is mine.** CLAUDE.md is explicit -- *"a worker's write surface is exactly the
`<paths>` its non-terminal order names"* -- and my own order says *"the `<paths>` block IS the grant"* two lines from
the contradicting sentence. The BOUNDS prose should have read "the R23 battery is READ-ONLY", which is what I meant
and what the worker correctly honoured. No remediation is owed on the work; the row stands as filed, and the fix is
to my order-writing, not to the build.

## What this round does NOT do, deliberately

Steps 2 and 3 of the amended decision are **not cut**. Step 2 is a live read this lane performs once the journal
carries the verdict -- one solo job on a cold resident, which needs an Analysis window packet from `2.0.0_SA_COO~P`.
Step 3 is the remedy, whose content that reading decides. Cutting a remedy now would be cutting against a cause
nobody has measured.

## State at this packet

- The order reads `complete` at the worker's HEAD; both worker commits are **LOCAL on `wk-IRPT_BCKEND-83`**.
- **The drain is BLOCKED, and not on this lane:** `safe-merge.sh` refuses because the shared index carries another
  seat's STAGED changes (`3.0.0_SA_CVO`'s sweep-3 review, adjudications, remediations, a CTO Andrew-direct).
  `0.7.0_AE_CloudOps` reports its own drain waiting on the same index. Clearing or committing another seat's staging
  is not this lane's act, so the merge waits for that seat to commit.
- Served code never moves by ~Y: the resident carrying `IB-yr-231` is rebuilt by `2.0.0_SA_COO~P` under its own
  ledger and halves.
