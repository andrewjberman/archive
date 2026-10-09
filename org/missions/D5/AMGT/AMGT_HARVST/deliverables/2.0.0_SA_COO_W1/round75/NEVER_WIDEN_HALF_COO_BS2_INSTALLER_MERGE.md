# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-130-r75` @40978c53b9 (`HVST-bs-2`) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~02:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed). Under
`1.0.0_SA_CTO~DELL1` msg 1267, a merge that lands in `lib/opal_data_harvest` is a site-Z deploy under a never-widen pair, and
`1.0.0_SA_CTO~Z`'s half is signed before the merge.
**Why a pair for a merge:** this file lands on site Z's shared tree at its next box-sync, and site Z's producers run from
that tree.

## THE ACT

One merge of branch `wk-AMGT_HARVST-130-r75` @40978c53b9 into `box/dell1` through `.tools/safe-merge.sh`, and nothing else.
CLOUD takes it at the integrator's box-sync, and site Z takes it at its own box-sync.

## WHAT THE BRANCH CHANGES (read at signing, `git diff 462f80e03e 40978c53b9`)

- `lib/opal_data_harvest/install-cycle-schedule.ps1`: +10 -1. The param block gains `[string]$Publishers = ''`. When the
  parameter is bound, names split on commas are checked against `bbg`, `wsj`, `barrons`, `sa` (the runner's `PUBLISHERS`,
  `cycle_runner.py:25`). Any other name prints `REFUSED: unknown publisher <name>`, and an empty list prints
  `REFUSED: no publishers`; both `exit 1` before anything is planned or registered. Given names append
  ` --publishers <names>` to the action's arguments. When the parameter is not bound, the arguments are unchanged.
- `deliverables/0.9.0_WK_AMGT_HARVST~130/`: AC1.out to AC3.out and the proof instance. These are records only.
- Re-run by this issuer on the branch 2026-10-09 ~02:3xZ: AC1 `--publishers bbg wsj barrons`; AC2
  `REFUSED: unknown publisher ft`, rc 1; AC3 the default ACTION still ends `STOP"`, then WORKDIR. `proof-of-spec-check`
  VALID rc 0.

## BLAST RADIUS

- **What may change behaviour:** only a person or seat that RUNS this installer, and only when it passes `-Publishers`. No
  process imports or loads a `.ps1`. The r47 backfill (`backfill_driver`), the collector and gold do not read it.
- **Writers of the scheduled task `Opal Data Harvest - Continuous Cycle`, N = 1:** this installer. The task is ABSENT on
  site Z per `br-3`'s close (@ef68288dee) and ABSENT on dell1 (read at signing). So no registered task's action changes
  because of this merge.
- **Reachable new state:** an installer run with `-Publishers` registers a task whose runner cycles only the named
  publishers. That run is HVST-bs-3's act, with its own order to `0.7.0_AE_CloudOps~Z` against a PINNED checkout. This
  merge registers nothing.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a. The branch head is still 40978c53b9.** A newer head is a new pair.
- **C-b. Re-run on the merged tree, before the close:** AC1, AC2 and AC3 as above, plus `-Plan` with no other argument
  printing `REGISTERED NOTHING (plan)`. The installer is never run without `-Plan` here.
- **C-c.** A ledger entry is opened before the merge and closed after C-b (NEVER-2).

No collection-leg condition: the file is not on any running leg's import path. Round-74 placement 1 holds a merge only while
a leg runs FROM THE TREE BEING MERGED INTO, and no leg runs from dell1's tree.

## BOTH BRANCHES

- **C-b holds:** `bs-2` closes, and the merge commit becomes the PIN for `bs-3`, sent to `0.7.0_AE_CloudOps~Z` through
  `0.0.0_AB_MSTR~DELL1`.
- **C-b fails, or the merge conflicts in the `.ps1`:** the merge is reverted in the same session with a new commit (never a
  rebase), the revert is read back by the same `-Plan`, and `bs-3` stays held.

## ROLLBACK

`git revert -m 1 <merge>` on `box/dell1`. The integrator carries it to CLOUD and site Z as it carried the merge. No served
key and no scheduled task depend on the file until `bs-3` runs.

## EXCLUDED

No task registration. No runner, collector or backfill run. No change to `cycle_runner.py`, `backfill_driver.py`,
`config.json` or the collector pointer. No S3 write.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~Z`'s half
