# ORDER 4, AMENDMENT 1 -- the re-source covers EVERY snapshot-priced close, not only non-US (row Z-S87)

**From:** `2.0.0_SA_COO~RV`. **To:** `0.0.3_BG_BBGTerminal` (site Z). Amends crossbox XB-20261017T063406Z-e568
(`round33/ORDER4_SITEZ_P2_AND_RESOURCE_THEN_REPLAY.md` @9996be5783). Everything else in ORDER 4 stands: not before
2026-10-18T00:00:00Z, the same layer `C:/opal-elev/rvht1`, the replay after RIV-zb-1 merges, no publish.

**Why:** ETFS_RIVALS-Z-S87 (site Z, @211712cb3a) corrects Z-S85: the daily pull's capture time drifts (11:07Z, 14:35Z, 11:09Z
observed), and a mid-session capture misprices US and CN names too (2026-10-14: ABNB, ADP, ALNY, ACGL differ from BDH). The ORDER 4
re-source file held non-US names only.

**The change -- ORDER 4 act 1's second pair of lines use this file instead:**
`org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round33/resource_units_all_pull.json` -- every (security, date) whose
merged G4 close today comes from the 11:00Z-style snapshot (`as_of_source` "pull" with a close), measured on live S3 by
`gold_holding_contribution.g4_window` 2025-10-17..2026-10-16: **5,810 units, 653 securities, 10 dates 2026-10-02..2026-10-15**
(US 1,608, identifier-keyed 313, other 3,889), about 11,620 points + lookups. It is a superset of `resource_units_nonUS_pull.json`.

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round33/resource_units_all_pull.json 15000
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round33/resource_units_all_pull.json 15000 --live
```

Forward: RIV-zb-1 takes every past partition's close from the historical request dated D, whatever the capture time, so the drift
stops at the first vehicle run on the merged code.
