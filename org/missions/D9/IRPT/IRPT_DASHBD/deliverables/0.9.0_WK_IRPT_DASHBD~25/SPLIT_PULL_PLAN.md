# SPLIT_PULL_PLAN -- TO-DB-b-44 (counts only)

Offline plan for FWD-8's split Black Diamond pull, built by `0.9.0_WK_IRPT_DASHBD~25`. Word: MSTR msg 1103, record @5ef6d33141.

- Record rows (closure segments): 2,299 = planned 2,299 + unmapped 0.
- Requests: 2,299 (one per account, 2,299 distinct accounts). Date ranges: 4,598 (two per request: segment start .. 2025-01-08 and 2025-01-10 .. segment end).
- Pull token: `split20261007`, a new `pull=` prefix. Prefixes already landed under the round-14 landing template: 1 (`20261004`).
- Landing keys: round 14's `_address(on, pull, bd_internal_id)` output, 2,299 of 2,299.
- Request bodies sha256: `6a5df93e586975a1442d17b4b37e553dc9f097e980e9794ca1a01477ef6d95de`.
- dry_run true, vendor_calls 0. Nothing was run; `run --go` and `sweep --go` are the issuer's.
- Offline tests: 11 passed.
