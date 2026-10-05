# HVST-as-1b -- THE collection run, LAUNCHED 2026-10-05 01:44:37Z (`2.0.0_SA_COO~H`)

**Pair:** COO @30ed1c8b83 + CTO @138b152f2a (5 conditions). **Gate:** OPEN (`as-1b.gate.out`). **Word:** Andrew @441338fdf7,
call 1. Before launch, 0 harvest processes were running (census 01:44Z).

| leg | pid | publishers | runtime root | checkpoint / stop file | state at 01:46Z |
|---|---|---|---|---|---|
| sa_barrons | 36868 | sa, then barrons | `.runtime/opal-data-harvest` | `r46_sa_barrons_checkpoint.json` / `R46_STOP_SA_BARRONS` | RUNNING: UNIVERSE 191 |
| ft | 35680 | ft | `.runtime/opal-data-harvest-ft` (new) | `r46_ft_checkpoint.json` / `R46_STOP_FT` | **STOPPED at job 1: `sign_in_refused`** (stored 0) |
| bbg | 27676 | bbg | `.runtime/opal-data-harvest-bbg` | `r46_bbg_checkpoint.json` / `R46_STOP_BBG` | RUNNING: UNIVERSE 191 |
| wsj | 37540 | wsj | `.runtime/opal-data-harvest-wsj` | `r46_wsj_checkpoint.json` / `R46_STOP_WSJ` | RUNNING: UNIVERSE 191 |

All four ran `python -m lib.opal_data_harvest.backfill_driver ... --auto-resume-transient 2`, detached. Full argv and pids are in
`.runtime/harvest-backfill/r46_launch.json`; output in `.runtime/harvest-backfill/r46_<leg>_run.{out,err}`.

**ft (CTO condition 3):** the fresh ft root has no session (the round-35 root went with the removed `wk-hvst-r32-92` worktree),
so the first job was refused sign-in. The leg waits for Andrew's hand-solved sign-in. After that, the SAME run resumes from its
checkpoint (CTO condition 1): `--clear-stop ft` on a new invocation of the same checkpoint. It is not re-run before then.

**Kill path (CTO condition 5):** create `.runtime/harvest-backfill/R46_STOP_<LEG>`; the leg ends after its current job.

**Report (CTO condition 4):** per leg, concluded jobs out of 191, plus `publisher_universe_verdicts` over the window's run
records, at each drive tick and at close.

## UPDATE 2026-10-05 ~01:5xZ: the ft hand sign-in ask is WITHDRAWN (issuer)

MSTR~Z (msg 29383) asked for Andrew's exact sign-in steps. Read first, the record answers that a hand sign-in cannot carry this
leg:
- **The evidence** (round 37 `HVST-aj-4`, row Z-W92-S20, `task-orders/AMGT_HARVST.TO-HVST-aj-4.ft-keepalive-run.md` record face):
  two hand-solved ft sessions died at about 75 min and at 24 min. The second got a 401 `sign_in_refused` 24m04s after the
  sign-in, despite keep-alive page loads every ~3.3 min, all logged in.
- **What the leg needs:** a 191-name ft leg runs for hours, so it would need repeated hand sign-ins. Each resume after a fresh
  sign-in would stretch condition 1's "same run". The unattended re-sign-in depends on an hCaptcha solver: the NopeCHA Token API
  is discontinued (row Z-W92-S18), and any other solver is a vendor use needing Andrew's word.
- **FWD-7 does not need ft:** its declared set needs to be NON-EMPTY, so ONE publisher whose concluded jobs cover all 191 names
  is enough.

**Ruling:** the ft leg of this run stays at its `sign_in_refused` stop (0 of 191 concluded) and is reported as such (CTO
condition 4). No hand sign-in is asked. Whether ft is collected at all, and by what sign-in route, is Andrew's call for a
later word.
