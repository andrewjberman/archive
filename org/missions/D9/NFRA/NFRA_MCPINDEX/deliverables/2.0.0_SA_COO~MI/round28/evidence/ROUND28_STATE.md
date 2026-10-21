# NFRA_MCPINDEX round 28 - state (2.0.0_SA_COO~MI, 2026-10-21 ~16:4xZ)

Orders MX-l-1 and MX-l-2 complete, merged (724baff7d23), proofs valid; round-close-check REFUSED only for reviewer=ABSENT (broker down), as in rounds 25 to 27. The trunk catalog is untouched (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6, the value OPLGTW batch17's release check requires).

Built:
- MX-l-1: emit_catalog_v02.py --size-census FILE: each catalog row gains size: {class, claim measured, measured_at, newest_partition, rows, bytes, basis} by the ruled thresholds (8 MiB, 24 MiB, 1,000,000 rows), matched by entity; an unmeasured row says so with its reason (claim absent); a separate validate_size; no option = byte-identical output. 22 own tests; 110 pass in atom_decomposition.
- MX-l-2: workflows/gateway_battery/fwd26_grade.py (grade, ideal): the 12-question set graded on the first named folder and table; listing the bucket first fails; an _s2 folder fails; Schwab accepts any master folder; O3 grades not_served until candidate e is served. 11 tests.
- Row Z-W97-S1 (ARMED: the commit gate could not run the client-account-id check, the hashed list being absent on this box) is DISARMED by a NEW citing row (the gate forbids editing a row in place) after the issuer scanned the commit's added lines by hand: the only long digit runs are the threshold test values; no account identifier.

Next (drain, after the ledger of batch17 reads CLOSED, not before 2026-10-22 06:45Z): re-run size_census.py, emit with --size-census plus the same maps as candidate e, diff against the placed catalog (expected: the size mappings, the header line, the build head), place it under the audited override, and ask COO~O to serve it (whether opal_discover returns size is app code, COO~O's); grade the question set against the served index.
Carried, event-gated: routing and battery on candidate e; the per-vendor re-run after OPLGTW's next round; the 24 MiB line re-measure on OPLGTW FWD-23 proof (e). Sheets site HELD for Andrew.
