# IRPT_ANLREQ round 43, workstream T -- close record: the figure projection admits only estate tickers and the request's own model keys (2.0.0_SA_COO~T2, dell2, 2026-10-15)

Issuance `218aa64619` (decomposition `decompositions/IRPT_ANLREQ_DECOMP_R43_T.md`); one direct-act cell, LOCAL; drained `5b438cd6c4` through `safe-merge.sh`; worker `0.9.0_WK_IRPT_ANLREQ~192` (haiku, high); worktree and both branches removed. The project row's `dep_stage` is the driver's and is untouched.
Cause: CTO half of the commentary deploy, condition 4 (msg 8577); the gap was measured on the merged consumer before the cut (an 8-character account number matched the ticker pattern; `model_names` took any string).

| cell | what exists |
|---|---|
| `AR-t-33` (FWD-10) | `drafter.py`: a `top_holdings` ticker must be in the estate table (`ESTATE_TICKERS`, 11,361 keys) as well as match the pattern; `model_names` entries must be among the request's `comparison_keys` (`allowed_models`, `None` keeps the old length-only rule for direct callers). `test_commentary_figures.py`: three new tests including the CTO's; three fixture edits forced by the rule (worker row W192-S1: `ZZQ1`->`AAPL`, `ZZQ4`->`MSFT`, model names to `Model Alpha`, a provenance count 2->1). Order complete, instance VALID, AC1 `R43-CN1-OK` (7 passed); two in-memory mutants (table rule off, key rule off) each fail the new tests |

## Drain checks and the real run (issuer)

| read | value |
|---|---|
| `py_compile` | OK |
| `pytest data/transcripts/scripts/tests -k commentary`, main tree | 72 passed |
| the real entry point on a dirty block (`R41_CHECKS/r41_real_run.py`, extended with an account id as a ticker and as a model name) | `R41-REAL-RUN-OK`: 0 of 4 planted strings in the prompt; withheld counts: 4 model names, 4 holdings, 1 allocation, 1 period, 1 sector member, 3 unknown keys. The request had no comparison keys, so every model name was dropped; the keep arm is the unit test's clean control. Output `R43_REAL_RUN_OUTPUT_20261015.txt` |

## Open at close

| item | state | owner |
|---|---|---|
| Deploy packet amended to the new pin (section 7); the CTO half is bound to the old blob and is void | new blob to the CTO for re-sign; the `~AQ2` order is cut only on the re-signed half | this lane, `1.0.0_SA_CTO~DELL2` |
| Surprise row `IRPT_ANLREQ-D2-W192-S1` (the fixture edits) | OBSERVATION, accepted: the rule forced them | CVO at the next compile |
| The figures producer | `~G2` compose cell | `2.0.0_SA_COO~G2` |
