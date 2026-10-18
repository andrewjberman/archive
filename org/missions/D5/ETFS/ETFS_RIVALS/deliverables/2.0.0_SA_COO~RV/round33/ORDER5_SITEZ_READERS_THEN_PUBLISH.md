# ORDER 5 (Andrew-direct): the readers replay, then publish the held-tr layer -- ORDER 3 act 3 under BOTH signed halves

**From:** `2.0.0_SA_COO~RV`. **To:** `0.0.3_BG_BBGTerminal` (site Z). **Both never-widen halves are signed:** COO half in
`round32/ORDER3_SITEZ_HELDTR_PULL_REPLAY_PUBLISH.md` @859e4e8799; CTO half
`org/missions/D5/ETFS/ETFS_RIVALS/ledger/NEVER_WIDEN_ORDER3_HELDTR_PUBLISH_CTO_HALF.md` @98d4271685 (binds the per-fund table
74cd181a, off git). Its condition 1 is act 1 below. Deploy ledger `etfs-rivalfunds-heldtr-publish-20261018` is OPEN (L1 readers,
L2 publish, L3 the next page build). Authority: Andrew, "Yeah I want all those completely filled", "now".

Script: `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py`, at or after the commit carrying this
file (it adds the `readers` act and a byte compare in `publish`).

## Act 1 -- readers (reads only; CTO condition 1)

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py readers . C:/opal-elev/rvht1 C:/opal-elev/rvrd
```
It rebuilds `dramatic_move.detect` (no web lookup, no write) and `price_series.series` over 2025-10-15..2026-10-16 through two
overlays, without and with the layer. Exit 3 and `VERDICT: STOP` = a new dramatic-move candidate on a date the layer holds: then
STOP, publish nothing, send the STOP lines back. Measured on dell1: an empty layer reads 0 new, 13 of 13 funds' curve counts equal,
exit 0; a planted control (one held-tr close at 4x on 000270 KS Equity, 2026-09-16) reads `NEW ON A LAYER DATE (STOP) 1`, exit 3.
Reply with the VERDICT line, the first line, and the per-fund table (counts only, no prices).

## Act 2 -- publish (the SERVED act), only when act 1 exits 0

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py publish . C:/opal-elev/rvht1
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py publish . C:/opal-elev/rvht1 --apply
```
The first line must read `objects in layer 256 | new 256 | present-and-equal 0 | present-and-different 0` (a DIFF line or
REFUSED: stop and send it back). The second writes each new object to its live uri and reads each back. Reply with both summary
lines. No delete, ever (rollback is Andrew's act, CTO half C-1 of order 2's pattern).
