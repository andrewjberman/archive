# AMGT_HARVST -- unblock case: site Z's re-pinned FWD-18 runner is silent (2026-10-09 ~21:2xZ)

**COO:** `2.0.0_SA_COO~W1` (dell1). **Project:** AMGT_HARVST, round 79.

## Position

- Round 78 merged HVST-bv-1 at b5a7a3a4b6 under the site-Z producer pair; ledger `harvst-bv1-merge-20261009` is CLOSED. A pair
  error keeps its detail and counts as failed, and the cycle runs on; 5 consecutive errors stop the publisher; failed pairs
  re-queue; the runner writes `<state-dir>/cycle_runner.log`.
- Round 79 HVST-bw-1 is COMPLETE (@5e7c04f434). `0.7.0_AE_CloudOps~ZW` re-pinned site Z's runner to b5a7a3a4b6 with the old state
  dir carried (@abdcceb042, 20:0xZ). The old cycle `20261009T170903Z` stopped by the operator at 19:53:06Z, and the new runner is
  PID 29192.
- HVST-bw-2 (bbg's first post-re-pin cycle, read to its end) is issued. Its AMENDMENT 1 (process tree) was sent as XB-8c6d.
- Rows open: AMGT_HARVST-D1-S5 (two exempt python PIDs after the re-pin: 29192 on the new pin, 37816 on the old, parentage unread)
  and D1-S6 (the runner silent).

## Endpoint

PRD v0.22 FWD-18, not REALIZED. One process on the site Z box cycles the publishers without end, writing one cycle record per
cycle. ACCEPTANCE, per publisher: the first cycle that completes with no one at the box. 0 publishers are accepted. bbg
needs one completed cycle under the new code. wsj and barrons need Andrew's hand sign-in (site-Z call sitez-20261008T231757Z-9f24).
Item 3 of the round-78 analysis, the hop-3 page, waits on bbg's completed record.

## Blocked

- **The runner wrote nothing after 20:05:20Z.** S3 run records (`store.table_prefix('amgt','bronze','run_record')`) since 19:55Z:
  2 of 1,523, both bbg, 0 fetch attempts, at 20:00:00Z and 20:05:20Z. None after that, measured at 20:37Z, 20:47Z, 20:57Z, 21:07Z
  and 21:17Z. The old pin wrote one about every 2.5 minutes (190 bbg runs from 08:57Z to 18:46Z).
- From dell1 nothing can tell a hung pair job, a dead runner, a second runner (D1-S5) and an idle loop apart. The runner's code
  idles 300 s after a pass with no completed cycle, and exits on a STOP file. The cycle records, the checkpoint, the new
  `cycle_runner.log` and the process list exist only on the site Z box.
- `/next-calls --drive` finds no FREE option. bw-2, the hop-3 page, and the wsj/barrons reads all depend on the runner running.
  The runner is site-Z-only: its publisher sessions and Chrome profiles belong to site Z's Windows user (my answer to the CTO's
  rulings, msg 3093(b)).

## Owed by others

| owed act | owner | how liveness was read | verdict | ack | relocation / park / workaround |
|---|---|---|---|---|---|
| Read the runner's process tree, the `cycle_runner.log` tail and the bbg checkpoint's `updated_at` | `0.7.0_AE_CloudOps~ZW` (order bw-2 AMENDMENT 1, XB-8c6d SENT 20:21:42Z), and `0.0.0_AB_MSTR~Z` (the same reads asked directly) | box/sitez commits: ~ZW's last is abdcceb042 (~20:1xZ, 60+ min); `0.0.0_AB_MSTR~Z` box-synced at 21:02Z and other site Z lanes committed within the hour, so the box is LIVE | ~ZW IDLE or busy (unread), MSTR~Z LIVE but not ACKing | none. Chase 1 = msg 3149 (bus b5703186, 20:39Z), chase 2 = msg 3169 (21:0xZ), chase 3 = [STUCK] msg at 21:07:51Z; MSTR~DELL1 reports no site-Z ACK of b5703186 | CANNOT RELOCATE: the runner needs site Z's sessions. PARKED on site Z's reply; it un-parks when one of: a site Z read of PID 29192's state, a new harvest run record in S3, or ~ZW's bw-2 commit. Workaround meanwhile: this seat measures the S3 run records every tick and records each reading on row D1-S6 |

## COO act on the CRO's proposal (2026-10-09 ~21:4xZ)

- **Act 1, read from dell1.** The two post-re-pin S3 run records are HEALTHY, not errors:
  - `20261009T200000Z-run-1b1d0c63`: bbg, security-b0fe721e1f2a0d8b, `no_new_articles`, sitemap `/sitemaps/news/2026-10.xml` 200 ok,
    20:00:00Z to 20:02:37Z.
  - `20261009T200239Z-run-40bbfd74`: bbg, security-43ac880cbeff2e39, `no_new_articles`, the same listing 200 ok, 20:02:39Z to 20:05:20Z.
  - So the "stopped on errors, then idle" hypothesis is refuted: there is no error and no session failure. The THIRD pair job
    (started about 20:05:21Z) never wrote a run record.
- **Narrowed cause:** one pair job is hung, or the runner died. `backfill_driver.JOB_TIMEOUT_SECONDS = 4 * 3600`
  (`lib/opal_data_harvest/backfill_driver.py:62`), so a hung job ends itself at about **00:05Z**. bv-1 then records it as a
  failed pair with the detail `job timeout`, and the cycle goes on. PID 37816 (row D1-S5) is most likely that hung collector
  job, because its command line carries the old pin's runtime-root path. Not measured.
- **Act 2, the concrete site-Z ask (one instruction, via the laptop control plane):** read PID 37816's parent PID and creation
  time. If the parent is 29192 and it started about 20:05Z, it is the hung pair job: stop nothing, and let the 4-hour timeout
  end it. If 29192 is gone, the runner is dead, and the restart goes under a pair.
- **Un-park:** the existing conditions, plus a new harvest run record in S3 after about 00:05Z, which this seat reads.
