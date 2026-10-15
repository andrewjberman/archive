# NFRA_CTLPLN round 17 -- the issuer's inputs for the round-17 analysis (2.0.0_SA_COO~C, DRAFT 2026-10-15 ~09:1xZ)

**Status:** both orders (CT-ag-1, CT-ag-2) are merged and `complete`; `round-close-check` reads MAY-CLOSE. Sent with `L8_PACKET_ROUND17.md` at the drain.

## A. CT-ag-1 -- `complete` (merge `b177c6ab4d`, flip `a97544076d`)

- `WORKTREE-GC-PRESERVE arms=9/9`, `WORKTREE-GC-OWN-COMMIT arms=8/8`, `WORKTREE-GC-SELFTEST cases=3/3`; proof VALID.
- **The CTO's done-when, the one real `--go`:** run by the issuer on 2026-10-15 ~08:59Z against the real merged worktree `ctlpln-103` (own=5, merged into `box/laptop`) with one planted untracked file. `--check-removable` printed `REMOVABLE-AFTER-PRESERVE`; `--go --only` printed `PRESERVED ... preserve/wk-NFRA_CTLPLN-103-20261015T085906Z 1e32e8229a`, removed=1, failed=0; the planted file was read back at the sha; ctlpln-104, rbndv2-8 and rbndv2-9 were untouched. Both verbs agree.
- **Sparse trial (the CTO's ruling 3, first half):** the worker's worktree was cut by hand as a cone-mode sparse checkout of `.tools/`, `lib/`, the project folder, `org/ref/` and `docs/doctrine/`: about 1,850 files, 47 MB (a full one is about 84,000 files, 3.6 GB). Its first `safe-commit.sh` needed four more folders: `org/modules/graph` (commit gate imports `comp_constants_cli`), `org/devices` (to-pipeline-gate reads `DEVICES.json`), `infra/logic/registry` (naming gate), `org/standards` (`NAMING_SCHEMA.json`, unconfirmed). Final size 74 MB. Row `W103-S1`. The four folders were relayed to worker ~104 as the base set of the sparse recipe.
- Rows: `W103-S2` (a directory junction is followed by `git add -A` and its target files recorded under the junction path in the preserve commit; forced removal keeps the target; INERT, not changed) and the issuer's `S9126`.

## B. CT-ag-2 -- `complete` (merge `4f05cf168c`, flip `6d351f89b3`)

- `WK-SPARSE-PROVISION arms=7/7`, `wk-provision.sh --self-test` `RESULT: 0 arm(s) failed of 8`, proof VALID.
- **The CTO's proof, real cell green in a sparse worktree with sizes:** `SPARSE-REAL tracked_bytes_sparse=68134267 tracked_bytes_full=3636649180 ratio=0.02 du_sparse=105M green=True`. A real sparse worktree of this repository ran the `CT-af-2` cell's test (`ROUND-CLOSE-DECOMP-ROUND arms=6/6`). `du_sparse` includes the nested portal worktree, a full 2163-file checkout the unchanged portal step creates.
- Base folder set: `.tools`, `lib`, the project folder, plus the four folders worker ~103 measured (`org/modules/graph`, `org/devices`, `infra/logic/registry`, `org/standards`), plus each `--order` path. `--full` needs a reason.
- The worker did not run `safe-commit.sh` inside a sparse worktree of its own (its worktree was full by the order). The evidence that it runs sparse is worker ~103's hand-cut worktree, whose commits all went through it after the four folders were added.
- **W104-S2 (BLOCKING, ruled by the issuer):** `/dispatch`'s `SKILL.md` is over its byte budget (33,198 at HEAD against 25,600) and the gate refuses any growth, so the worker's longer recipe text was refused. The issuer rewrote the recipe paragraph shorter, net -48 bytes (`43f9022522`). The file stays over budget; trimming it is nobody's cell.
- A second real use of the new tool: worker ~104's clean merged worktree was removed with `worktree_gc.py --go --only ../ajb_wk/ctlpln-104` (`CLEAN`, removed=1, failed=0); `C:` read 16 GB free afterwards (9.0 GB at ~09:08Z; other seats also write to that disk, so the rise is not all this removal).

## C. Round-18 candidates found so far

1. **`S9126`:** `worktree_gc.py --check-removable` and `--only` with an ABSOLUTE path read the tool's own command line as an in-use process and report `SKIP IN USE`; a relative path works. A caller such as a drain script or MSTR passing an absolute path gets nothing removed. Fix: exclude the tool's own pid and its parent shell from the scan.
2. **`W103-S2`:** whether the preserve step should skip a directory junction (it follows it today).
3. **Disk:** `C:` read 13 GB free at ~08:50Z and 9.0 GB at ~09:08Z while one full worktree (`ctlpln-104`, 3.7 GB) existed beside other seats' worktrees; MSTR's line is 12 GB. The cause of the drop is not measured here. The full worktree was removed at ~104's merge.

## D. Process facts

1. **A real run needs a merged worktree that outlives its merge.** The real `--go` ran on the sparse worktree after its merge, before its removal; removing at merge (as MSTR and the CTO ask) would have left nothing to run on. The drain order that worked: re-run, merge, plant, check, `--go --only`, flip.
2. **Absolute versus relative path** in the real run (S9126) was found only because the first call failed; the test arms never passed an absolute path to `--only`. A test arm for an absolute path would have caught it.
