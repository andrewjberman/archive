# NFRA_CTLPLN round 17 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~09:3xZ)

Both round-17 orders are `complete` (issuance `db71ef26a1`, decomposition `NFRA_CTLPLN_DECOMP.round17.md`; flips `a97544076d`, `6d351f89b3`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 17` reads `verdict=MAY-CLOSE`, `orders=25 judgment=2 graded=2 ungraded=0 self_graded=0`, with `TREE orders counted by decomposition round: 2 (TO-CT-ag-1, TO-CT-ag-2)`. Pins are commits on `box/laptop`, LOCAL unless stated. Each cell carries the issuer's own re-run on the worker's branch. Inputs for the analysis: `ROUND17_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | merge | issuer re-run |
|---|---|---|
| `CT-ag-1` | `b177c6ab4d` | `WORKTREE-GC-PRESERVE arms=9/9 ok=True`; `WORKTREE-GC-OWN-COMMIT arms=8/8 ok=True`; `WORKTREE-GC-SELFTEST cases=3/3 ok=True` |
| `CT-ag-2` | `4f05cf168c` | `WK-SPARSE-PROVISION arms=7/7 ok=True`; `wk-provision.sh --self-test` `RESULT: 0 arm(s) failed of 8`; `SPARSE-REAL ... ratio=0.02 ... green=True` |

Every proof instance reads VALID on the committed state.

## 3. Real runs of the outcomes (the CTO's two done-whens)

- **The preserve step, one real `--go` (ruling 1):** run by the issuer on 2026-10-15 ~08:59Z against the real merged worktree `ctlpln-103` (own=5, merged into `box/laptop`) with one planted untracked file. `--check-removable` printed `REMOVABLE-AFTER-PRESERVE MERGED own=5; 1 path(s) would be preserved`. `python .tools/worktree_gc.py --go --only ../ajb_wk/ctlpln-103 --clean-hours 0` printed `PRESERVED wk-NFRA_CTLPLN-103 -> preserve/wk-NFRA_CTLPLN-103-20261015T085906Z 1e32e8229a (1 path(s))`, `removed=1 failed=0`. `git show 1e32e8229a:PLANTED_BY_ISSUER.txt` returned the planted line. The other worktrees (`ctlpln-104`, `rbndv2-8`, `rbndv2-9`) were untouched. Both verbs agreed. The preserve branch is left in place as the record.
- **Porcelain-only dirt (ruling 2):** the same worktree carried ignored test leftovers (`.comp-graph/`, `.scratch/`) and read removable, where round 16 read `NOT-REMOVABLE`. A second real run removed `ctlpln-104` (clean, merged): `CLEAN`, `removed=1 failed=0`.
- **The sparse worker checkout (ruling 3):** worker ~103 ran its whole cell in a hand-cut sparse worktree (47 MB, 74 MB after four folders were added; a full one is 3.6 GB). `SPARSE-REAL tracked_bytes_sparse=68134267 tracked_bytes_full=3636649180 ratio=0.02 du_sparse=105M green=True` for a real earlier cell run in a worktree cut by the new `wk-provision.sh`.
- No UI is touched, so no screenshot.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (open call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-27` waits on Andrew's "another time".

## 5. Rows this round minted

`W103-S1`, `W103-S2`, `W104-S1`, `W104-S2` (BLOCKING, ruled by the issuer: the `SKILL.md` byte budget; commit `43f9022522`), all INERT, plus the issuer's `S9126` (absolute-path self-match in `worktree_gc.py`). `W100-S1` and `W100-S2` are closed by `CT-ag-1`. Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`.

## 6. Not measured here

`safe-commit.sh` inside a worktree cut by the NEW `wk-provision.sh` (it ran in the hand-cut sparse worktree only); `--go` without `--only` on the real repository (never run); a symlink in the preserve step (symlink creation failed on this box, WinError 1314); the PRD FWD grade table, which the CTO's coverage read governs.
