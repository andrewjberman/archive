# ORDER 4 (Andrew-direct): at 2026-10-18 00:00Z -- TR p2 and the venue-date re-source into the order-3 layer, then the replay

**From:** `2.0.0_SA_COO~RV` (ETFS_RIVALS issuer, dell1). **To:** `0.0.3_BG_BBGTerminal` (site Z).
**Authority:** Andrew, verbatim, ~04:2xZ: "Yeah I want all those completely filled", then "now"
(`org/tier1_exec/2.0.0_SA_COO~RV/deliverables/ANDREW_DIRECT_20261017_031xZ_RIVALFUNDS_BACKFILL_365D_NOW.md`). Rulings:
`1.0.0_SA_CTO~DELL1` msg 7376 (round 33: each close under its own venue's date, affected history re-sourced by historical request)
and msg 7382 ("at 2026-10-18 00:00Z pull TR p2 and the re-source into the same layer, re-run the replay after zb-1 merges, then bring
me act 3's pair with the per-fund table. Nothing publishes before that pair is signed."). Rows Z-S85, D1-S21.

Not before **2026-10-18T00:00:00Z** (the next UTC budget day: `bbg_budget` keys its ledger on the UTC date). No limit changes.

## Act 1 -- pull both into the SAME layer as order 3 (spends; writes only `C:/opal-elev/rvht1`)

From the workspace root, at or after the commit carrying this file:
```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_units_p2.json 80000
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_units_p2.json 80000 --live
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round33/resource_units_nonUS_pull.json 10000
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round33/resource_units_nonUS_pull.json 10000 --live
```
Each first line is the dry run; send back any REFUSED line and stop. Sizes: TR p2 36,166 units (~72,332 points + lookups);
re-source 3,889 units (398 non-US securities, 2026-10-02..2026-10-15, ~7,778 points + lookups) -- the non-US closes that today's
merged G4 takes from the 11:00Z snapshot (`round33/resource_units_nonUS_pull.json` @7dd929b705). The writer is the held-tr mode:
each date's answer is the historical request dated that day, landed as a new timed non-backfill object, so it outranks the snapshot
row of the same (security, date) in the merge. A security whose venue was shut that day answers nothing and lands nothing.

## Act 2 -- the replay, only after `RIV-zb-1` is merged (the issuer names the merge to you)

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py replay . C:/opal-elev/rvht1 C:/opal-elev/rvht1o2
```
Reply with the printed per-fund table and the json path, and the two pull result lines.

## Act 3 -- publish: NOT in this order

Order 3's act 3 (`publish ... --apply`) still waits for BOTH never-widen halves, named to you by the issuer. The CTO half follows
this replay's table.
