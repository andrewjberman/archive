# NEVER-WIDEN -- COO HALF: HVST-bs-3, FWD-18's continuous cycle runner registered at log-on on the site Z box, bbg, wsj and barrons, from a pinned checkout of c1be67f53c

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~02:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s site-Z half (owed; offered in its bs-2 half
@8630dee4ff, "this seat signs its site-Z half when asked"). **Actor:** `0.7.0_AE_CloudOps~Z`, by order
`task-orders/AMGT_HARVST.TO-HVST-bs-3.the-runner-activated-on-bbg-wsj-barrons.md` (@c7909af157).

## THE ACT

On the site Z box, the order's steps 1 to 3, once:
1. `git worktree add --detach <workspace-parent>\harvest-runner-pin-c1be67f53c c1be67f53c`.
2. `install-cycle-schedule.ps1 -RepoRoot <pinned> -Publishers bbg,wsj,barrons -Plan`, read.
3. The same command without `-Plan`, once; then `Start-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle'`, once.

## THE PIN

c1be67f53c is the merge of HVST-bs-2 into `box/dell1` (ledger `harvst-bs2-installer-merge-20261009` CLOSED). It carries
`cycle_runner.py` from HVST-br-2 (drained @5a2d54eb4a) and the installer from HVST-br-3 (drained @ef68288dee) and HVST-bs-2.
The pinned checkout moves only by an explicit re-pin, never by box-sync (round-74 placement 1(a)).

## BLAST RADIUS

- **One scheduled task is created:** `Opal Data Harvest - Continuous Cycle`, at log-on of the site Z box's interactive user,
  with no time limit, IgnoreNew, and 3 restarts at 5 minutes. Its action is
  `python -m lib.opal_data_harvest.cycle_runner --state-dir ... --runtime-root ... --stop-file ... --publishers bbg wsj barrons`,
  and its working directory is the pinned checkout. Today it is ABSENT on site Z (read by `1.0.0_SA_CTO~Z` at 02:4xZ).
- **What the runner writes:** per cycle, one record under `<pinned>\.runtime\harvest-cycle\state\cycles\<publisher>\`.
  Through `backfill_driver` and the collector, it writes the same bronze and silver keys the collector writes on a manual leg
  of those three publishers, from the floor of the publisher's last completed cycle. On the first cycle that floor is
  yesterday, UTC.
- **Writers of those publishers' silver, N = 1:** the collector. This act adds a second CALLER of it (the runner), not a
  second writer. r47 runs sa only. Whether a manual leg of bbg, wsj or barrons is running is NOT read by this seat (it is a
  site-Z process list); C-c reads it at the act.
- **Not reached:** sa (r47 runs it, and sa joins on r47's completion, a separate act); the FT (not an allowed name); gold
  (built only by its own rebuild acts); `config.json` and the collector pointer.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** `git -C <pinned> rev-parse HEAD` reads c1be67f53c (a positive control: the same command on the shared tree reads
  something else, or the same hash with a dirty status shown).
- **C-b.** The `-Plan` read in step 2 shows ACTION ending `--publishers bbg wsj barrons`, and WORKDIR is the pinned path.
- **C-c.** No `backfill_driver` or collector process is running for bbg, wsj or barrons (process list with a positive control).
  The r47 sa leg MAY be running: it uses its own runtime root and checkpoint.
- **C-d.** A ledger entry is opened by the actor before step 3 and closed at acceptance or at rollback (NEVER-2).

## BOTH BRANCHES

- **Acceptance (order step 4):** for each of bbg, wsj and barrons, the first `*.cycle.json` with `"completed": true` and
  `started_at` after step 3, with no one at the box after step 3. A recorded refused sign-in is a result, and that publisher's
  cycles go on. The order closes on the CVO's grade of those records (AC3).
- **A cycle record shows a failure class that repeats without end, or the runner touches anything outside its three
  publishers:** rollback.

## ROLLBACK

Create the stop file (the runner ends between jobs), then `Unregister-ScheduledTask -TaskName 'Opal Data Harvest - Continuous
Cycle' -Confirm:$false`, and read the task back ABSENT. Bronze and silver objects already written stay: the collector's own
idempotent keys, which a later manual leg would also write. The pinned checkout is left in place for the record.

## EXCLUDED

No sa. No FT. No change to the disabled task `Opal Data Harvest - Local Publications`. No gold. No pointer move. No
re-collection beyond the runner's own floor.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~Z`'s site-Z half
