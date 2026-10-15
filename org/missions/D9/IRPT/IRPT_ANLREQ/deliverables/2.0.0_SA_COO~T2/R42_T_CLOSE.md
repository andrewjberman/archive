# IRPT_ANLREQ round 42, workstream T -- close record: the commentary Lambda's POST line can now be read (2.0.0_SA_COO~T2, dell2, 2026-10-15)

Issuance `169654b4a9` (decomposition `decompositions/IRPT_ANLREQ_DECOMP_R42_T.md`); one direct-act cell, LOCAL; drained `128caf4ac8` through `safe-merge.sh`; worker `0.9.0_WK_IRPT_ANLREQ~191` (worker-light, haiku, high); worktree and both branches removed.
The project row's `dep_stage` is the driver's and is untouched.

| cell | what exists |
|---|---|
| `AR-t-32` (FWD-10) | `lambda_handler.py` sets its module logger to INFO (one line after `LOG = ...`); `test_commentary_logging.py` (2 tests, no `caplog.at_level`, no level set on `lh.LOG` in the test) proves the level and the POST line. Order complete, instance VALID (rc 0), AC1 `R42-LG1-OK` (2 passed) |

## Drain checks and the one real run (issuer, 2026-10-15 ~19:0xZ)

| read | value |
|---|---|
| `py_compile` | OK |
| `pytest data/transcripts/scripts/tests -k commentary`, main tree | 69 passed (includes the test the worker's sparse tree could not run: its row `W191-S1` is a cone fact, as `W190-S4` was) |
| the real handler under runtime-style logging, `r42_real_run.py` (root logger WARNING, one printing handler, nothing else set) | `R42-REAL-RUN-OK`: stage `draft_posted`; the runtime handler wrote `commentary draft stored ...` and `COMMENTARY-POST ... outcome=POSTED status=200 code=-` |
| control arm, the same run with the module logger's level undone in memory | stage `draft_posted`, the runtime handler wrote **0** lines: the production symptom (the live run of 17:00:52Z logged no application line) reproduced exactly |

## What this does and does not claim

- Claims: with this change, a deployed run writes the `COMMENTARY-POST` line, so `post_census.py --live` can count it.
- Does not claim: that the deployed function has it. The change is in the repository only; the Lambda changes at the deploy cell, together with the figures change (`AR-t-31`).
- Does not claim: that the 17:00:52Z draft reached the ticket. Unread; the front door is needed.

## Open at close

| item | state | owner |
|---|---|---|
| Deploy of `drafter.py`, `entry.py` and `lambda_handler.py` (WORLD) | not cut; needs the CTO half of a pair, an applier, and a change-management entry; waits only on the figures producer's contract being settled enough to ship the consumer | this lane, then `0.7.0_AE_CloudOps` |
| The figures producer and placement | `~G2` round 8 compose cell; `AR-g-54` | `2.0.0_SA_COO~G2` |
| Why the resident refused to package the stored draft (`ReportRefused`, `CurrentAuthorityRefused`) | source read `AR-y-357` | `2.0.0_SA_COO~Y2` |
| Surprise row `IRPT_ANLREQ-D2-W191-S1` | a cone fact | CVO at the next compile |
