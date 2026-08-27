<to_id>ADHC_GLDINC.PARITY-RC</to_id>
<project>ADHC_GLDINC</project>
<title>Root-cause GLDINC P1 parity regression (06-11: 3 byte-clean nights -> 98.17% exact, -1440 rows/-50 accts); load_flows incremental vs oracle</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (from AE morning-review RAVC2 anomaly-1, 20260611T132445Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project ADHC_GLDINC is complete; this TO was last touched 2026-06-11, predating the project close 2026-06-25. Closed as a record act, not a work verdict. Prior status: active -- QUEUED after NFRA_DTAFLP TO-1b (done) + TO-4. NOT an interrupt to the DTAFLP critical path. Blocks the GLDINC P1 INCREMENTAL CUTOVER (cutover_ready=false); served platinum = clean oracle full-recompute, so NOT customer-facing.</status>

FINDING (AE morning review): GLDINC night-4 06-11 _parity shadow-compare regressed from 3 prior byte-identical nights (06-08/09/10 exact=100%, max_abs=0) to exact=98.17%, row_delta=-1440 (77128 vs oracle 78568), max_abs=$19,500, implied_nna -$18.4M, total_inflow -$38.7M, acct_count -50. Scorecard doctrine: non-zero max_abs on a non-fallback night = STOP (not widen-tolerance). clean_night_counter held 0 (surface-probe field) but parity underneath regressed.

OWNER: data/*/scripts/gold/load_flows is DS-owned.
HYPOTHESIS to confirm-or-kill: a BD restatement caught by the oracle full-recompute but MISSED by the incremental watermark lookback (per memory feedback_bd_restatement_lookback_14d_standard -- if load_flows incremental lookback < BD restatement window, it silently misses a restatement of a 4-14d-old date, producing exactly this stale-but-looks-fresh shape concentrated in restated dates). AE is pre-pulling the incremental.parquet vs oracle key-diff to localize the 1440 missing keys -> will land to DS to accelerate RC. If hypothesis confirmed: fix = extend the incremental lookback to >=14d (BD-restatement standard) OR force-recent-days. RAVC2 -> COO + CTO. Rule 14 gates on any .py edit.
