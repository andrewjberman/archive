# AMGT_HARVST -- ROUND 45 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-05 ~00:4xZ

**Round:** the round-44 analysis enrichment list (`ledger/ROUND_ANALYSIS.round44.md` @ed9efe80ea). Decomposition section 58,
issued @0d90db2da8. Three cells: one worker (`~93`) and two issuer acts. **Class: SERVED** (ar-1's silver write, under a pair). No
collection ran, no vendor call was made, no backfill ran.

## 1. The cells

| cell | FWD | result | evidence |
|---|---|---|---|
| `HVST-ar-1` | FWD-2 | **COMPLETE.** Every field the publisher sent is typed in served silver. AC1 24/24; AC2 in-memory census lost 0 on all five publishers, 250 of 250 compared; **AC3 served census lost 0 on all five publishers** (reader's served-row rule; see the note below). | build @eab4321d38, merged @38fc65b7bf; `round45/ar-1.AC3.issuer_grade.reader_rule.out` |
| served write (ar-1) | FWD-2 | **WRITTEN.** Pair: COO @b5d31484b7 + CTO @16eb97eae5, digest 9d7b7d57c651. 1,995 rows in 13 new parts: 1,978 gain columns only, plus 17 first rows (2 bbg, 15 wsj originals that had none). Nothing overwritten. VERIFY: every planned row serves. Post-write re-read: 2,069 of 2,069 originals unchanged, CHANGED 0, GONE 0. NEVER-2 entry @0f63417bb5, closed @4e84fd3f2e. | `round45/ar-1.rederive_write.out`, `ar-1.rederive_plan.written.json`, `ar-1.rederive_postwrite_reread.out` |
| `HVST-ar-2` | FWD-12 (c) | **DONE** (direct act @5443081c9e). `config.json` sa listing cap 25 -> 200, through `worker.listing_page_cap()`; plants 5/5 pass, and 2 fail with the config reverted. Re-read with the aq-4 instrument: (a) 33 = 33 quarantined keys, (b) 0 article requests, (c) cap 200 on the run path, (d) 11,210 rows with 0 mismatches. | `round45/ar-2.*` |
| `HVST-ar-3` | FWD-9 (row Z-S82) | **READ PASS.** The served timeline already clips at 2026-01-01: 212 names, 0 leaks; the 11 pre-2026 events (7 names) are never served; 1,355 day probes on pre-2026 days serve no data. Ruled down from SERVED in section 58 (a 0-diff deploy); row Z-S84 corrects Z-S82. | `round45/ar-3.AC1.out`, `ar-3.served_clip.json` |

## 2. For the CVO

- **To grade:**
  - **FWD-2:** "every field present in the received article ... appears typed in the queryable table, rebuilt from the stored
    original, and a query by company and date returns it". The served census reads 0 lost, every sampled original has its row,
    and the query by company and date returns on all five publishers.
  - **FWD-12:** (a)-(d) as read above. Ruling 3 of the analysis: depth past page 25 on a new backfill is not part of (c).
- **AC3, the instrument note (row Z-S85):** the literal AC3 run reads FAIL (lost 39/10/8/0/19). The census picks a
  `bronze_key`'s row by `run_stamp`, and a tie keeps the FIRST-read row. Each re-derived row repeats its original `run_stamp`,
  so the census graded superseded rows.
  - Control (`ar-1.AC3.tie_control.out`): on one barrons key, the census picks the pre-round-37 part (61 columns) and the
    reader (`store.supersedes`) picks tonight's part (74 columns).
  - The PASS uses a copy of the census whose only change is that selection (`ar-1.field_census.reader_rule.py`).
  - Round 44's aq-1 barrons figures came from the same stale rows.
- **Surprise rows this round:**
  - Z-S83 (CTO ruling on Z-S82); Z-S84 (the correction above); Z-S85 (the census instrument).
  - Z-W93-S1: BLOCKING, ARMED, disarmed @ccb21d1a4e (the two barrons golden pins).
  - Z-W93-S2 to S5: OBSERVATIONs. S2 (no-row cause: 11 builder faults fixed, 6 batch conflicts handled by the act's bins),
    S3 (five lossless reshapes), S4 (run_stamp ties, the root of Z-S85), S5 (the worktree's research-suite misses; 336/336 on
    CLOUD).
- **Next, per CTO msg 29310 (@a142505a06):** the lifted collection run covers the rank's 191 names. Its prerequisite is 191/191
  resolved to the declared-set join key. Its order: FWD-12 DONE, then this write verified (done), then the run under its own
  pair. Plan: `R46_COLLECTION_RUN_PLAN.md` @29104786ce.

Push: read at send time.
