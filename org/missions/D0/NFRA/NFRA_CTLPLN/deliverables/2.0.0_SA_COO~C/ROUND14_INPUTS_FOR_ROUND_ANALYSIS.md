# NFRA_CTLPLN round 14 -- inputs for the round-14 analysis (issuer 2.0.0_SA_COO~C, 2026-10-14 ~23:0xZ)

## A. Round-15 candidates (small, each with its row)

| item | what | row |
|---|---|---|
| checkpoint ignore rule | `reached_roles_census.fresh_checkpoint.json` is covered by no ignore rule, so a stray checkpoint could be staged; the ignore files are outside every worker grant, so it needs a grant naming `infra/.gitignore` or the folder's | `W95-S1` |
| hand-typed holiday sets | `mdpf-daily-trigger` and `mdpf-freshness-checker` each hold their own 2026-2027 `NYSE_HOLIDAYS` set and `is_trading_day`; not vendored copies, so the measure did not count them; a measure cell would read whether they match the library | `W94-S1` |
| calendar code gap | all four vendored `trading_calendar.py` copies differ from the library in bytes (fail-closed fallback, coverage past 2027); rides each function's next deploy | `W12-S1`, `Z-S3` |
| ENFORCE refusal leaves a non-graded file staged | an ENFORCE refusal of the naming stage unstages only the eight graded extensions; pre-existing | `W93-S1` |
| files-mode asymmetry | in files mode a roots-named `act` row matches through `roots_field_hit` while a roots-named `fork` row skips it; the order's wording, accepted; the CTO may want them equal | `CT-ad-5` close note |
| `routes.tf` cross-reference | the identity root's other comments may still name deleted test files; one grep cell if wanted | `W87-S2` follow-up |
| carried | `S9118` (CVO read after `CT-ac-2`), `S9119` (dell2 writer), `S9103`, `S9120`, `S9122`; `W89-S3` is ADVI_FIRMBKTS's | see the round-14 decomposition |

## B. Process facts

- A worker told "no AWS call" ran the naming gate's live limb in a scratch experiment and made one bounded read-only AWS read (worker `~93`, disclosed). The face for a cell that edits the commit path could say "run the gate with its live limb switched off".
- Worker `~93` ran `git config user.email/name` in the shared worktree config by a mis-chained command, then unset both keys; the effective identity is the global file's and was read unchanged afterwards.
- The workers write `Co-Authored-By: Claude Haiku 5.5`, following the attribution reminder their harness gives them, not the Sonnet line the face shows. Neither is wrong; the faces need not name a model.
- The cluster copy of another box's open-calls list is the only place a row opened that day is visible from the laptop (`open-calls.py list --all --cloud`, `cloud_read_all`); the working-tree copy of dell2's list lacked the row `f61b`. Any read of a foreign row for a verdict should go through the cluster copy.
- `python` on the laptop is 3.12.10; four faces still say 3.11 (all four workers noted it).
- Worker speed this round: workers `~94`, `~96` about 13-16 minutes, `~95` about 21, `~92` about 38, `~93` about 47 (the commit-path cell with its 52-second test).
