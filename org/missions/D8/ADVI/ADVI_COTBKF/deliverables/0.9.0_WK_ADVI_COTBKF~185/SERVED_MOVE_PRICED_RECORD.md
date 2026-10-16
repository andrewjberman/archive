# SERVED-MOVE control -- CB-cq-1 (round 95) -- NOT MEASURED

Worker: 0.9.0_WK_ADVI_COTBKF~185. Box: dell1. Record: [SERVED_MOVE_PRICED_RECORD.json](file:///C:/dev/wk-cotbkf-185/org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~185/SERVED_MOVE_PRICED_RECORD.json).

**Result:** `measured: false`. The control and the added-column counts were not produced.

**Stop point:** CB-cq-1 item 1 (provision the run data). The as-traded price basis reads a Yahoo close cache (`--yahoo-cache`, 3580 per-ticker files, pinned copy sha256 `5b4bb7db...`). That cache is not on dell1, not under any sibling worktree scratch, and not on S3. Its only producer is a yfinance pass, which is a vendor call the cell does not permit. No substitute was made.

**Not reconciled:**
- The served objects were last written 2026-10-09T12:41Z. The round-83 record names 728d223ddc as the served run_commit, while the CB-ah-3 record describes a held build at 6f70d5cc01bb written that day. The served run_commit was not read.
- The round-107 record says the round-68 builds were made without the hold list the cell gives as served.

**Channel rows filed:** `ADVI_COTBKF-D1-W185-S1` (BLOCKING, the missing cache) and `ADVI_COTBKF-D1-W185-S2` (OBSERVATION, the served write time against the records).

**Counts:** none. No account, name or dollar value is recorded.
