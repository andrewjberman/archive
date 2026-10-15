# NFRA_CTLPLN round 15 -- the three workers stopped on the account's spend limit (issuer 2.0.0_SA_COO~C, 2026-10-15 ~00:5xZ)

At about 23:1xZ on 2026-10-14 workers `0.9.0_WK_NFRA_CTLPLN~97`, `~98` and `~99` each ended with an API error: "You've hit your monthly spend limit ... your weekly limit resets 1am (America/New_York)" (HTTP 429, model claude-haiku-5-5). It is an account limit, not a defect in any cell. No further worker is spawned until Andrew raises the limit or it resets (1am ET is 05:00Z); a spawn now would fail the same way.

State kept in the worktrees under `C:/Users/AndrewBerman/Desktop/ajb_wk/` (none is merged; nothing is lost):

| cell | worker | on its branch | missing |
|---|---|---|---|
| `CT-ae-1` | `~97` | one UNCOMMITTED file, `.tools/tests/test_kill_maint_planted.ps1` (the classifier exempts planted roots that inherit a worker worktree as their working directory; the worker was setting the launcher's working directory to the temporary folder) | the test passing, its commit, the proof instance |
| `CT-ae-2` | `~98` | `a781351eda` tool, `339622de5e` measure record, `ed74b1982d` three surprise rows (six inline holiday sets, not two) | the proof instance; the issuer's re-run |
| `CT-ae-3` | `~99` | `a3fe2e7707` the four repairs and `test_round15_batch.py`, `56eb1742fd` surprise row `W99-S1` (placement refusal) | the proof instance; the issuer's re-run |

Resume: when a spawn works again, continue each worker's work from its branch (a fresh worker of the same serial, told to read its branch log first), or the issuer re-runs the criteria of `~98` and `~99` itself if they already pass. The issuer builds nothing under a FULL lease.
