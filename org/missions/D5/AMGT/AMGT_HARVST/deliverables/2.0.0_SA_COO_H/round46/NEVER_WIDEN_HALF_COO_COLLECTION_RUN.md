# NEVER-WIDEN -- COO HALF: THE collection run, one universe-scope run per publisher (round 46 HVST-as-1b)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-05 ~02:0xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:**
- Andrew-direct @441338fdf7, call 1: "ONE universe-scope run per publisher; no recurring cadence and no new mechanism";
- CTO ruling @a142505a06 (the rank's 191 names; conditions 1-3);
- round-45 analysis @4f01f5ab8d, ruling 1;
- decomposition section 59.

## THE PRE-RUN GATE: OPEN (`round46/as-1b.gate.py`, `as-1b.gate.out`; no publisher request)

1. **191/191 resolved:** every rank name carries `security_key` = the pool key, the declared-set join key, stamped on each job as
   `gold_security_key`. Identity coverage: company 191, ticker 191, sa_symbol 191 (TPG by issuer ruling, row Z-W94-S2).
2. **The sa bound, printed before the GO:** 191 x (200 + 20) = **42,020 requests at most, 9.7 days at 4,320/day.** The 89-name
   bound was 19,580. The 2026-01-01 floor stops most names far earlier: in the last backfill, 25 of 1,194 sa query-runs reached
   the old 25-page cap.
3. **Driver dry run, per publisher** (sa, ft, wsj, bbg, barrons): UNIVERSE 191, 191 PLAN lines, NETWORK CALLS 0.

## THE ACT

- **Four DETACHED drivers** (so they outlive a session) on the round-35 runtime roots (`.runtime/harvest-backfill/runtimes.json`).
  One collector runtime root holds one worker lock, so publishers that share a root run in one driver, in sequence:
  - **sa then barrons:** `.runtime/opal-data-harvest` (`--publishers sa barrons`; the driver runs sa first);
  - **ft:** a NEW root, `.runtime/opal-data-harvest-ft`. The round-35 ft root lived in the `wk-hvst-r32-92` worktree, which
    is gone (measured 02:0xZ), so ft has no live session. ft's last leg (`ft_full_run2`) ended at 3 pairs on an operator stop
    file. If the fresh session needs a hand-solved sign-in or challenge, the leg hard-stops (`sign_in_refused` or `bot_check`)
    and that is the reading; Andrew can solve it while present (round-37 aj-4);
  - **bbg:** `.runtime/opal-data-harvest-bbg`;
  - **wsj:** `.runtime/opal-data-harvest-wsj`.
- **Each driver runs:** `python -m lib.opal_data_harvest.backfill_driver --checkpoint .runtime/harvest-backfill/r46_<leg>_checkpoint.json
  --publishers <pubs> --runtime-root <root> --stop-file .runtime/harvest-backfill/R46_STOP_<LEG> --auto-resume-transient 2`.
  Output goes to `.runtime/harvest-backfill/r46_<leg>_run.{out,err}`.
- Pacing, caps and the floor stay as configured; nothing is raised for speed.
- **One run per publisher.** A leg ends on the driver's STOP statuses: bot_check, unclassified, account_or_harvester_unavailable,
  sign_in_refused, throttled and cooldown are hard stops. Transport errors and upstream 5xx are resumed by the driver itself,
  at most 2 times per leg, each recorded.
- A hard-stopped leg is NOT re-run on this word. It is reported. The CTO and Andrew decide whether a resumption is "the same
  run". A second run or a recurring cadence needs a new word.

## Writers and the write set, per publisher (N counted)

| property | writers | this act's writes |
|---|---|---|
| bronze `article` / `listing_hit` objects | the collector (this act is its only runner) | NEW keys only (`put_article_bronze` and the listing writers, never overwrite) |
| silver `article` / `listing_hit` | 3: `HarvestUploader` (this act, through the driver's upload after each job), `LegacyUploader` (not run), and round-45's re-derive act (done) | append through `silver_append` (`IfNoneMatch`; an unchanged record_hash is skipped) |
| run records (the declared set reads them) | the collector | one per job |
| gold (mention, daily, event, window) and served routes | not touched | the next gold rebuild moves them, under its own pair |

## What the run can and cannot claim

- **FWD-7:** a publisher enters the declared set only if its CONCLUDED jobs cover all 191 keys. In the last bbg backfill, 84 of
  89 pairs concluded (error 4, bot_check 1), so one non-concluding pair keeps a publisher out. That result is honest, and the
  half does not pre-judge it.
- **ft:** ft has needed a hand-solved challenge before (round-37 aj-4). If its leg hard-stops on sign-in or a challenge, that
  stop is the reading.
- **The 153 DERIVED sa symbols are unprobed** (ruling Z-W94-S2). A wrong symbol shows as a job that does not conclude.

## Rollback

Collection output is append-only. The served surfaces do not move until a later gold rebuild, which carries its own pair. A
stop file (`R46_STOP_<PUB>`) ends a leg after its current job.

Not covered: a second run, a raised cap or pacing, any publisher outside the five, or any write to gold or a served route.
