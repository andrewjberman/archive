# AMGT_HARVST ROUND 25 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~05:5xZ

**Issuance:** `65aa9251bc`, five orders over `ROUND_ANALYSIS.round24.md` @`6c5b4339a1`, with ruling 2 amended @`e49bbdb3d2` (decomp
section 37). **L8-L10 route:** `3.0.0_SA_CVO~Z`.

**Class: SERVED / WORLD.**
- `o-5` made vendor calls (R-21 scripted) and put S3 objects.
- `o-4` rewrote served sa silver.
- Both ran under signed never-widen pairs.

## 1. FIVE ORDERS, ALL TERMINAL

| order | class | drained | status | instance |
|---|---|---|---|---|
| `o-1` chatter_daily coverage from run records (FWD-7) | LOCAL | `00a67f7d66` | complete | VALID |
| `o-2` `run-local.ps1` passes `--harvest-grammar` (FWD-1/3) | LOCAL, no pair (task Disabled, 0 triggers) | `798b1d1244` | complete | VALID |
| `o-3` silver tie-break on `run_stamp`, one shared comparator (FWD-2) | LOCAL | `592860d126` | complete | VALID |
| `o-4` served sa silver rebuild (FWD-2) | WORLD, pair `7776cd3492` / `c2c9a9b80c` | `daf0034f12` | complete | VALID |
| `o-5` Lenovo backfill (FWD-9, FWD-3) | WORLD, pair `f17ca57280` / `4db36bf02b`, amended twice (`2d10f4e4e4`, `7db8b9a744`) | `366757825d` | complete | VALID |

**`o-5` took three attempts under its pair. Both failures were the issuer's cut-time misses, and each worker stopped
correctly:**
1. `config.json:7` `jobs_per_run: 1`, so one job ran: barrons, which was challenged.
2. The grammar collection path QUEUES to the local outbox. The S3 writer is `upload-harvest`, which the half named "not
   run".

Each miss was re-cut and re-signed. No object outside a pair ever landed.

**Close run.** Script `round25/close_run_round25.py`, output `close_run_round25.out.txt` and `rerun/`, run at trunk
`b8b5af85e6`. 12 criterion invocations: **10 rc 0, 2 FAIL.** Both failures were explained and neither is a product defect:

| check | result | why |
|---|---|---|
| `o-2` AC1 | FAIL | Its "base script" is `git merge-base HEAD CLOUD`. On the trunk that is the merged script, which carries the flag. Re-run against the PINNED base `65aa9251bc` (`rerun/o2_ac1_pinned_base.txt`), it PASSES: the base lacks the flag, and both new invocations carry it. The check could only be re-run on the worker's branch. |
| `o-5` AC1 | FAIL | "sa: 3 new object(s)". Those are `o-4`'s 3 parts, which landed AFTER `o-5` by design. At `o-5`'s drain AC1 PASSED on 5 of 5 roots. |

- Three tracked worker outputs were rewritten by the re-runs and restored.
- Test counts: `o-1` 472 and `o-3` 293 passed. They are higher than the workers' counts because later merges added tests.

## 2. WHAT MOVED ON THE SERVED PLANE (measured; the CTO grades)

| FWD | this round |
|---|---|
| **2** | **SERVED.** The sa silver `article` table was rebuilt once: 11 rows in 3 new parts (`part-20260930T052800Z`), and served record keys went from 46 to 52. The 5 MOVED rows now serve their `links`, `type` and `meta`, via `o-3`'s tie-break; the close-run census shows the later part is picked on each tied key. The other 41 keys are unchanged, and a re-run writes 0. `/timeline` bodies do not move: the deployed reader takes `title` and `published_precision` only (CTO half). |
| **9** | **Lenovo backfill, live.** Run 1 (`20260930T044003Z`) fetched 22 new articles, bbg 11 and wsj 11. `upload-harvest` put 57 new objects, and only under the `bloomberg/` and `wsj/` harvest roots (27 bronze, 30 silver parts). 0 objects moved or removed on 5 roots. |
| **3** | **The same-day repeat re-fetched nothing held** (`o-5` AC2 PASS; CTO condition 5 re-grounded on FWD-3's words). Its 2 fetches were `bbg:OURYDJ6TTDSG01` (new to the listing) and `bbg:NM5NLQ6K50XZ01` (fetched by run 1, never stored); 26 were skipped as held. **Owed before FWD-3 grades REALIZED (CTO condition):** answered rows on `NM5NLQ6K50XZ01` and on the wsj URL/UUID key split. |
| **1 / 3** | `run-local.ps1` now passes `--harvest-grammar`. The Scheduled Task is Disabled with 0 triggers, so no production fire exists. Re-arming it is Andrew's (CTO list). |
| **7** | The coverage rule is BUILT: a successful job's reached span counts as SEARCHED. It moves 0 of 5,730 name-days, and the gold branch still RESOLVES 0 of 191, because no span-bearing run record exists yet. `o-5` ran on the pinned pre-`o-1` code, so its run records carry no span. The served `chatter_daily` has not been rebuilt. |

**`o-5`'s FWD-9 detail:**

| publisher | result | reach (`publisher_coverage`, the gold builder's own rule) |
|---|---|---|
| bbg | fetched | span 2015-01-07..2026-09-30, **273 of 273 days** from the floor |
| wsj | fetched | span 2026-09-23..2026-09-30, **8 of 273 days**. The plan bound read the 09-04 silver watermark; the walk reached 3 pages. |
| ft | `request_rejected` | none |
| barrons | challenged | none |
| sa | not run: the renewal is pending | none |

## 3. ROWS THIS ROUND

- `Z-W61-S1..S3`, `Z-W63-S1`, `Z-W65-S2`, `S4` and `S5`: INERT.
- `Z-W65-S1` and `Z-W65-S3` (BLOCKING): disarmed by AMENDMENTS 1 and 2.

## 4. FOR ROUND 26 (the CTO's list; not cut here)

1. **The mention rebuild** (`build_mention`, paired) over the new silver.
   - This is how the 22 Lenovo articles and the 6 NEW sa rows gain `mention_count`.
   - **ANDREW-DIRECT @`8135566a29`:** "there should be a mentions counter wherever articles are displayed".
   - The backend already carries `mention_count` on 304 of 304 served rows, served per article on `/timeline/day`. The
     frontend is `2.0.0_SA_COO~D`'s, relayed by MCP; Andrew picks up with that seat.
2. **The rows the CTO requires before FWD-3 grades:** `NM5NLQ6K50XZ01` never stored, and the wsj URL/UUID key split.
3. **The `chatter_daily` rebuild on the run-record rule** (paired), after a collection on post-`o-1` code writes
   span-bearing run records.
4. **FWD-9's remaining reach:**
   - wsj walked only 8 days;
   - ft and barrons are Branch B;
   - sa waits on the renewal;
   - the other 190 names come next, on these actual page counts: bbg 2, wsj 3.
5. **Proposed process fix** (the cause of the two `o-5` misses): before signing a WORLD half for a producer, trace argv to
   its config defaults and to the actual put call, and name the command that reaches it. A stub-client put-count dry run
   catches both. This is proposed for `/dispatch` Step 2; it is not implemented here.

## 5. FOR L9

- There are no judgment criteria this round; the FWD grades are the CTO's at L10.
- **Disposable worktrees:** `wk-hvst-r25-61`..`-65` and the r24 set. Branches are kept; removal waits on Andrew's go.
