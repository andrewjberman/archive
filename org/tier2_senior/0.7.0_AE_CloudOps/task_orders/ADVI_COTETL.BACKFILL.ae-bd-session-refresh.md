<to_id>ADVI_COTETL.BACKFILL.ae-session</to_id>
<project>ADVI_COTETL</project>
<title>Refresh the cot BD session (idle-dead) via the cot-exporter EC2 cot_bd_session_fetch.py -- the GATING dependency for the assets_dim build + the full backfill</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (decompose of CVO scope cb62104b1; Andrew-direct "do all")</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- GO: gating dependency -- goes FIRST, before DS Work A/B can run. NOT COT-launch-gating (launch is technical+display-ready, awaiting Andrew user-list). -->

<context>
The stored BD session is IDLE-DEAD (keepalive 401, token-mint empty {} -- ~5h idle past the 30-60min TTL; the 20h expires_at is NOT the real limit). ALL live cot work (DS's assets_dim build, the backfill pulls, the lookback probes) needs a fresh session. CVO scope cb62104b1 (org/tier1_exec/3.0.0_SA_CVO/ADVI_COTETL_assets_dim_and_backfill_scope_20260622.md) sec 4.
</context>

<the_work>
Refresh the cot BD session via the cot-exporter EC2 `cot_bd_session_fetch.py`: start the EC2 + SSM the session-fetch -> a fresh session lands in SM `blackdiamond/cot/session`. Verify the new session is live (keepalive 200, token-mint non-empty) BEFORE signaling DS. firm-sep cot (cot-exporter EC2, cot SM path -- never the bd session).
</the_work>

<acceptance_criteria>
1. Fresh cot BD session in SM blackdiamond/cot/session; keepalive 200 + token-mint non-empty (verify, don't assert).
2. Firm-separated: cot-exporter EC2 + cot SM path only; bd untouched.
3. SIGNAL DS (0.4.0_DS_ClientPlatform) the moment the fresh session is live -> unblocks Work A/B. RAVC me + CVO.
4. Note the session-TTL reality (30-60min idle) so DS sequences its pulls promptly after the refresh (or you re-refresh if DS's work spans the TTL).
</acceptance_criteria>
