<to_id>ADHC_GLDINC.PARITY-FIX</to_id>
<project>ADHC_GLDINC</project>
<title>Fix GLDINC parity regression: OPTION A — complete the byte-faithful cache round-trip (persist/reconstruct _source_key/_row_idx) so the incremental cache reproduces the oracle's keep='last' survivor</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (from DS GLDINC.PARITY-RC 20260611T141614Z; fix-direction per CTO ruling 20260611T141938Z — supersedes COO's initial Option-B greenlight)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- SCOPE+DESIGN Option A. HOLD RAVC2/cutover-flip until (a) AE key-diff confirms the dup-txid/composite-collision cluster + (b) local cache-vs-fresh shadow-compare shows 0 key delta. NOT customer-facing (served=oracle); blocks P1 incremental cutover only.</status>

ROOT CAUSE (DS RC, restatement hypothesis KILLED): 06-11 cache-only incremental night diverged from oracle by exactly 1440 (account,date) keys in ~50 accounts. lib/nna_flows.py dedups twice with keep='last' (L159 transaction_id, L178 composite); survivor depends on row order (sort by _source_key,_row_idx) + transaction_id int-vs-str identity (deliberate, L551-556). Cache persists transaction_id as string + _txid_is_int bool + per-partition _row_idx, reconstructed in _lf_read_cache(); the round-trip isn't byte-faithful for some dup-txid rows -> windowed dedup keeps a DIFFERENT survivor than the oracle's native-typed fresh read. Cache is a PERFECT event-level snapshot (3,843,024 events == fresh, 0 per-partition mismatch) -> NOT dropped events; it's the transform's order/type sensitivity through the cache round-trip.

FIX — OPTION A (CTO-ruled, never-widen-compliant): complete the byte-faithful cache round-trip. Persist + reconstruct the dedup ORDER KEY (_source_key / _row_idx) — same proven pattern as the existing _txid_is_int fix — so keep='last' selects the SAME survivor on cache read-back as on a fresh scan. The cache then faithfully reproduces the oracle; ZERO served-output change.

NOT OPTION B (deterministic order/type-INDEPENDENT survivor): rejected for P1 — the dedup is SHARED cache+fresh, so a deterministic-survivor redesign changes the AUTHORITATIVE oracle's output (different survivor than today) = changes served numbers = violates nna_flows.py never-widen doctrine (L551-556). Option B is deferred to a SEPARATE post-cutover correctness-hardening project (CTO to PRD if Andrew/COO want it; needs own served-number validation). [COO initially greenlit B 141810Z; CTO ruling 141938Z corrected to A; COO corrected DS 142036Z.]

CAUTION: nna_flows.py is a SHARED transform feeding bd+inf+cot -> Rule 14 + extra care; Option A must NOT change bd/inf/oracle behavior (it only adds cache round-trip fidelity). VERIFY: confirm against AE's incremental.parquet-vs-oracle key-diff (CTO predicts cluster on L178 composite-collision/sign-flip accounts), then local cache-vs-fresh shadow-compare -> 0 key delta. RAVC2 -> COO+CTO.
