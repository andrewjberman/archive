# NFRA_CTLPLN round 17 -- the issuer's inputs for the round-17 analysis (2.0.0_SA_COO~C, DRAFT 2026-10-15 ~09:1xZ)

**Status:** CT-ag-1 is merged and `complete`. CT-ag-2 is with worker ~104 (proof instance committed in its worktree, not yet reported or merged); its section is a placeholder filled at the drain. Nothing here is sent until both orders are terminal.

## A. CT-ag-1 -- `complete` (merge `b177c6ab4d`, flip `a97544076d`)

- `WORKTREE-GC-PRESERVE arms=9/9`, `WORKTREE-GC-OWN-COMMIT arms=8/8`, `WORKTREE-GC-SELFTEST cases=3/3`; proof VALID.
- **The CTO's done-when, the one real `--go`:** run by the issuer on 2026-10-15 ~08:59Z against the real merged worktree `ctlpln-103` (own=5, merged into `box/laptop`) with one planted untracked file. `--check-removable` printed `REMOVABLE-AFTER-PRESERVE`; `--go --only` printed `PRESERVED ... preserve/wk-NFRA_CTLPLN-103-20261015T085906Z 1e32e8229a`, removed=1, failed=0; the planted file was read back at the sha; ctlpln-104, rbndv2-8 and rbndv2-9 were untouched. Both verbs agree.
- **Sparse trial (the CTO's ruling 3, first half):** the worker's worktree was cut by hand as a cone-mode sparse checkout of `.tools/`, `lib/`, the project folder, `org/ref/` and `docs/doctrine/`: about 1,850 files, 47 MB (a full one is about 84,000 files, 3.6 GB). Its first `safe-commit.sh` needed four more folders: `org/modules/graph` (commit gate imports `comp_constants_cli`), `org/devices` (to-pipeline-gate reads `DEVICES.json`), `infra/logic/registry` (naming gate), `org/standards` (`NAMING_SCHEMA.json`, unconfirmed). Final size 74 MB. Row `W103-S1`. The four folders were relayed to worker ~104 as the base set of the sparse recipe.
- Rows: `W103-S2` (a directory junction is followed by `git add -A` and its target files recorded under the junction path in the preserve commit; forced removal keeps the target; INERT, not changed) and the issuer's `S9126`.

## B. CT-ag-2 -- placeholder

Fill with: the criterion lines, the `SPARSE-REAL` line (sizes against a full checkout), the base folder set the worker ended with, whether `safe-commit.sh` ran in the sparse worktree, the merge.

## C. Round-18 candidates found so far

1. **`S9126`:** `worktree_gc.py --check-removable` and `--only` with an ABSOLUTE path read the tool's own command line as an in-use process and report `SKIP IN USE`; a relative path works. A caller such as a drain script or MSTR passing an absolute path gets nothing removed. Fix: exclude the tool's own pid and its parent shell from the scan.
2. **`W103-S2`:** whether the preserve step should skip a directory junction (it follows it today).
3. **Disk:** `C:` fell from 13 GB to 9.0 GB free during this round while one full worktree (`ctlpln-104`, 3.7 GB) existed; MSTR's line is 12 GB. The full worktree goes at ~104's merge.

## D. Process facts

1. **A real run needs a merged worktree that outlives its merge.** The real `--go` ran on the sparse worktree after its merge, before its removal; removing at merge (as MSTR and the CTO ask) would have left nothing to run on. The drain order that worked: re-run, merge, plant, check, `--go --only`, flip.
2. **Absolute versus relative path** in the real run (S9126) was found only because the first call failed; the test arms never passed an absolute path to `--only`. A test arm for an absolute path would have caught it.
