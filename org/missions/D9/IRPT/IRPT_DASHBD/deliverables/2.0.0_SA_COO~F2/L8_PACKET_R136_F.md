# L8 packet: IRPT_DASHBD workstream F-SHIP (~F2) round 136 -> 3.0.0_SA_CVO~IRPT

From 2.0.0_SA_COO~F2, 2026-10-16 ~22:1xZ. Issuance be99bf5767 (amended 6e39c73840); orders TO-DB-f-2201, TO-DB-f-2202, TO-DB-f-2203, all complete; the seven mechanical criteria PASS on the trunk by the issuer's re-run (DBF136-1-AC1, AC2, AC3; DBF136-2-AC1, AC2; DBF136-3-AC1, AC2). **Two judgment criteria are yours, on cell DB-f-2201:** `DBF136-1-J1` and `DBF136-1-J2`. Nothing here is served: the cells are code and text on the trunk; no AWS act was taken by anyone in this round.

## DBF136-1-J1 -- 20 sampled rows of the Inflection producer's output, from the ONE newest Orion snapshot

- **Drawn:** 2026-10-16T22:03:50Z, after every producer and the launcher were on the trunk, by `deliverables/2.0.0_SA_COO~F2/tools/sample_inflection_latest_snapshot.py`, seed 135, n 20, one forced rolled line. Read-only (GET requests only); nothing was written to S3.
- **Source:** the NEWEST snapshot only (`date=2026-10-16`); the other 154 partitions are cumulative earlier snapshots and were not read. Contract 0.5.1.
- **Figures file (untracked, git-ignored, this box):** `org/mcp/drive_ticks/J1_SAMPLE_INFLECTION_R136.json` (sha256 `da1e316f9320b42f...`, 25,890 bytes): per row the source values and the producer's 19 columns. **Committed form:** `J1_SAMPLE_INFLECTION_R136_HASHED.json` (sha256 `ee9848707ea98dde...`, 10,467 bytes): the day, the sha256 of the natural key (account, trade date, transaction description, symbol, units, amount) and the non-figure results.
- **Denominators printed on the ONE snapshot** (counts only): 1,521,297 rows; per status Complete 1,336,782, Pending 92,616, Rejected 90,783, Reversed 1,110, Pending Corporate Action 4, Inactive 2; Complete rows in non-unique natural keys 6,566 (3,017 keys: a duplicate key is a finding and is never sampled); Reversed keys derived from that snapshot 893; the producer's rows out 1,336,781 (the Complete lines less ONE offset of a Reversed original, `OFFSET_OF_REVERSED` 1); rolled rows out 2,010; **source lines emitted on more than one day: 0**.
- **S6 print** (the launcher's own `s6_report` on the same snapshot): "S6: 96 of 96 events carry an equal-amount Buy Exchange or Income Reinvested line on the same account and day (within 0.01)"; with_equal_amount_line 96, missing 0. This is the CTO's release criterion for the Inflection pair (96 of 96).
- **What to grade:** field by field, the 19 columns of each sampled row against its source row by the natural key, including that `business_date_claim` is `measured` exactly where `business_date` equals `trade_date` and `inferred` on the rolled line. The sample holds 1 rolled line and 19 measured lines.

## DBF136-1-J2 -- 20 sampled rows of the 49 Financial producer's output

- **Drawn:** by `tools/sample_49f_producer_rows.py`, seed 136, n 20, one forced rolled line, read-only. Contract 0.5.1.
- **Figures file (untracked, git-ignored):** `org/mcp/drive_ticks/J2_SAMPLE_49F_R136.json` (sha256 `09c3cba8dbae5cd8...`, 31,767 bytes). **Committed form:** `J2_SAMPLE_49F_R136_HASHED.json` (sha256 `8c5c6d22551f58c5...`, 10,942 bytes).
- **Denominators over the FULL domain** (the 49 Financial silver is a per-day table; every partition counts): 573 partitions; 3,354,885 rows; rows in non-unique natural keys 21,236 (10,027 keys, 0.633 percent); every partition holds a unique row; unique rolled rows 288 in 1 partition (the non-trading-day lines the producer rolls forward and stamps `inferred`).
- **What to grade:** as J1: the 19 columns against the source by the natural key (account, trade date, transaction code, symbol, quantity, amount), the per-row claim included; the sample holds 1 rolled (`inferred`) line and 19 `measured` lines.

## What the issuer did NOT establish

The new handler stage has never read a real 49 Financial `fact_trn` partition (tested against fakes; the signed packet's dry run is the first real read, and it writes nothing). The two samples exercise the PRODUCERS, not the handler. The twelve pre-existing failures of the gold Lambda's test directory (fakes lacking `as_of`) are carried, not fixed. The Inflection bundle pin is re-cut at the Inflection release.

-- 2.0.0_SA_COO~F2
