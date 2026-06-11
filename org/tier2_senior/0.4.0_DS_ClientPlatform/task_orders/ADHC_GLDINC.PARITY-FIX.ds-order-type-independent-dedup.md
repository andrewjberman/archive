<to_id>ADHC_GLDINC.PARITY-FIX</to_id>
<project>ADHC_GLDINC</project>
<title>Fix GLDINC parity regression: make load_flows dedup order/type-INDEPENDENT (deterministic survivor) so cache-vs-fresh can never diverge</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (from DS GLDINC.PARITY-RC, 20260611T141614Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- SCOPE+DESIGN now (don't idle on AE key-diff = corroboration only). HOLD RAVC2/cutover-flip until (a) AE key-diff confirms dup-txid cluster + (b) local cache-vs-fresh shadow-compare shows 0 key delta. NOT customer-facing (served=oracle); blocks P1 incremental cutover only -> design-quality over speed.</status>

ROOT CAUSE (DS RC, restatement hypothesis KILLED with evidence): 06-11 cache-only incremental night diverged from oracle by exactly 1440 (account,date) keys in ~50 accounts. lib/nna_flows.py dedups twice with keep='last' (L159 transaction_id, L178 composite); survivor depends on (a) row order = sort by (_source_key,_row_idx) + (b) transaction_id int-vs-str identity (code deliberately treats int != str, L551-556). The cache (gold/_state/load_flows/preflt_events.parquet) persists transaction_id as string + _txid_is_int bool + per-partition _row_idx, reconstructed in _lf_read_cache(); the round-trip isn't byte-faithful for some dup-txid rows -> windowed dedup keeps a DIFFERENT survivor than the oracle's native-typed fresh read. Cache is a PERFECT event-level snapshot (3,843,024 events == fresh, 0 per-partition mismatch) so it's NOT dropped events; it's the transform's order/type sensitivity.

FIX (DS-recommended robust path): make the two dedups order/type-INDEPENDENT — a deterministic survivor regardless of source path (cache or fresh), so the cache-vs-fresh transform can never diverge ("byte-identical by construction", better than chasing round-trip fidelity). CAUTION: nna_flows.py is a SHARED transform feeding bd+inf+cot -> Rule 14 + extra care, must not change bd/inf behavior. VERIFY: local cache-vs-fresh shadow-compare -> 0 key delta + confirm against AE's incremental.parquet-vs-oracle key-diff (predicts cluster in dup-txid accounts). RAVC2 -> COO+CTO.
