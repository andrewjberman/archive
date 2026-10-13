# Call: two SERVED cells need a never-widen sign-off pair (CTO + COO) before they are cut (2.0.0_SA_COO~Q1, 2026-10-13)

Both cells change what the nightly Yahoo run writes or labels in the served price store, so CLAUDE.md section 5 (never move served output without a never-widen sign-off) applies. The COO has the builds ready to cut; the signature is the CTO's.

**Cell A -- wire the Yahoo incremental path into the nightly run.** `incremental_append.py`, `incremental_plan.py` and `incremental_equal.py` (DQ-t-48, merged @9de742d8f9) proved the incremental draw (last 5 trading days after backfill) equal cell for cell to a full draw on 50 of 50 names on a no-split day, plus one split arm refilled and equal. They are not called by `daily_draw.py` / `extend_frontier.py` yet. Wiring changes how many days the 22:30 ET run asks Yahoo for, and so which rows it rewrites in the per-CUSIP `prices.parquet` of the 326 planned names. Needed from the pair: blast radius (which keys, which rows) and the rollback per key.

**Cell B -- label Yahoo-sourced client prices UNVERIFIED until the porting test passes.** Andrew-direct 2026-10-13: a client price from Yahoo reads UNVERIFIED until it passes the porting test (returns, 5 sha256-drawn intervals, within 10 bps of Bloomberg `TOT_RETURN_INDEX_GROSS_DVDS`). Today no served field carries that label. Adding it changes a served column. Needed from the pair: the field name and its consumers (ADVI_COTBKF reads the store), so the label is read, not ignored. The porting test itself cannot run until Bloomberg draws it (3,195 cells, filed).

**REC:** sign Cell A as a pair (the proof exists); sign Cell B after the consumer list is printed. Neither is a vendor call. Until signed, the COO cuts neither.
