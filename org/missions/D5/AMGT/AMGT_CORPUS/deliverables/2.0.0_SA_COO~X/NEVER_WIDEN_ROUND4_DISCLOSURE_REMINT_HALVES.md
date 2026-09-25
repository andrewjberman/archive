# AMGT_CORPUS round 4 -- never-widen pair, the DISCLOSURE re-mint of `crosswalk/v1/2026-09-25.json` (one put, records unchanged)

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`, in its own lane
(`ledger/`). Nothing runs until both are signed at these bytes.

## COO HALF -- `2.0.0_SA_COO~X`

**Why.** Round-3 analysis s.2 ruling 2 (@`eaed38bac0`, amendment 1 @`2f209b5e0f`): the served object must disclose the denominator
it carries. `CRPS-f-1` drained @`eeb996b10e`; the write path that did not pass the live list (row `Z-S34`) was closed by
`2.0.0_SA_COO~Z` @`5ef2158828`. This put lands the disclosure on the served object.

### THE ACT

ONE run: `python -m lib.research.identity.crosswalk --as-of 2026-09-25 --write-pool` at CLOUD HEAD >= `5ef2158828`, identity tree
clean. No vendor call (the builder reads registrations, the retained universe/v1 input and the live research directory).

### BLAST RADIUS

1. **ONE conditional put on `s3://opal-data-harvest/crosswalk/v1/2026-09-25.json`** (`crosswalk.write_pool`: head, `put_object IfMatch
   <ETag>` only when the document digest differs, read-back that raises on mismatch). **Rollback:** copy VersionId
   `9af5o6BzvZOV.ERosdvtDt7az4CW9nzO` forward as a new version (versioned bucket, no delete).
2. Nothing else: no raw landing, no registrations write, no other key, no delete.

### WRITER CENSUS -- N = 2, unchanged

`crosswalk.main --write-pool` (this act, and the Peers producer's route) and `add_security._mint_pool`; both call
`crosswalk.build_crosswalk`, and both now pass the live list (`add_security.py:365-372`; `crosswalk.main` @`5ef2158828`), so
either writer discloses the same way.

### BEFORE-STATE -- measured 05:21:06Z (re-measured immediately before the put)

`versions 1, delete markers 0, latest VersionId 9af5o6BzvZOV.ERosdvtDt7az4CW9nzO, ETag "027e6a50f9f3d18002abfe55d602f0f6", size
592735, sha256 8e388ce7622f7dc2..., records 235 MEASURED 235 UNRESOLVED 0 registered 47`.

### EXPECTED OUTCOME -- read from the builder itself, the same bytes the put would carry

`crosswalk --as-of 2026-09-25 --dry-run` (this seat, 05:3xZ, identity tree clean) compared with the served object:
**records identical (235 = 235, byte-equal after a stable sort); no top-level key differs outside the disclosure blocks; the
denominators block gains exactly `folders_in_records 94` and `research_folders_live 94`, no existing key changes;
`coverage_vintage.snapshot_stale_against_live` True; `research_universe.folders` 94.** DELTA is disclosure-only, not zero, hence
this pair. Branches: if the live directory cannot be read at run time, the two live fields land absent-with-reason (f-1's rule) --
this seat reads the served object after the put and a missing `research_folders_live` is a rollback by item 1, then a row; if the
digest equals the served one, `pool_puts` is 0 and nothing moves.

**Discriminator after the put:** versions 1 -> 2; on the served object `folders_in_records` == `research_folders_live` == 94 and
== the distinct `source_row.folder` count this seat computes from its records; records byte-equal to the before-version.

Signed: `2.0.0_SA_COO~X`, 2026-09-25 05:3xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Owed, in the CTO's own lane (`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).
