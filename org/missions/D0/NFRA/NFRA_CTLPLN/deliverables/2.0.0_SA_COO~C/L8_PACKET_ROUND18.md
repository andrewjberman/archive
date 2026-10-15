# NFRA_CTLPLN round 18 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~11:2xZ)

The one round-18 order is `complete` (issuance `94d3dc6d0e`, decomposition `NFRA_CTLPLN_DECOMP.round18.md`; worker branch merged `3f4730b5d3`; flip `ad277385a0`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 18` reads `verdict=MAY-CLOSE`, `orders=24 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL. Inputs for the analysis: `ROUND18_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cell, order and the issuer's own re-run

| cell | merge | issuer re-run (in the worker tree @6780e32c13) |
|---|---|---|
| `CT-ah-1` | `3f4730b5d3` | `ROUND18-BATCH arms=3/4 skipped=1 ok=True`; `--real`: `ROUND18-BATCH arms=4/5 skipped=1 ok=True` and `SAFE-COMMIT-SPARSE exit=0 tip_moved=True folders=7 green=True`; `WORKTREE-GC-PRESERVE arms=9/9 ok=True`; proof instance VALID (rc=0) |

Changed files: `.tools/worktree_gc.py`, `.tools/tests/test_round18_batch.py`, the proof instance, `INVESTIGATION_v1.md`. `wk-provision.sh` is unchanged: the round-17 base set already held what `safe-commit.sh` needs.

## 3. Real runs of the outcomes

- **safe-commit green in a sparse worktree (ruling 1):** the worker's own worktree was cut by `wk-provision.sh` (17 s, 108 MB) and ran `safe-commit.sh` for single-file commits of a modified and a new `.py`, a modified `.md`, a new `.json` and a new `.txt`, all green. The one folder added was `org/surprise_channel`, to read the row schema; none was needed for `safe-commit.sh`. The issuer re-ran the `--real` arm, which cuts a second sparse worktree and removes it.
- **S9126, absolute path (ruling 2):** the issuer ran `python .tools/worktree_gc.py --check-removable C:/Users/AndrewBerman/Desktop/ajb_wk/rbndv2-10` (read only, another seat's worktree), with and without a trailing slash. Both read `NOT-REMOVABLE UNSTARTED own=0`, where round 17 read `SKIP IN USE`. The removal of `ctlpln-105` used `--go --only` and read `PRESERVED ... preserve/wk-NFRA_CTLPLN-105-20261015T111725Z c9b2d097a9 (2 path(s))`, `removed=1 failed=0`.
- **A link kept as a link (ruling 3):** the junction arm ran for real: the preserve commit holds `120000 blob junc`, none of the target's files, and the target survives the removal. The symlink arm is SKIPPED with WinError 1314.
- No UI is touched, so no screenshot.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (open call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-27` waits on Andrew's "another time".

## 5. Rows this round minted

`W105-S1` to `W105-S8`, all OBSERVATION, INERT, `UNDER_INVESTIGATION`. Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`.

## 6. Not measured here

`safe-commit.sh` on deletions, renames, directory pathspecs, binary files, files outside the sparse cone, merges and amends in a sparse worktree; `--go` without `--only` on the real repository (never run, CTO ruling 4); a symlink in the preserve step; the PRD FWD grade table (the CTO's coverage read governs).
