# irpt-ycharts-generate RELEASE 1 -- never-widen pair DRAFT (IB-pr-357 + ~P's riders + E-Y4)

**Deployer:** `2.0.0_SA_COO~Y2`, the function's lane. **Ruling:** `1.0.0_SA_CTO~DELL2` msgs 1084 and 1089 (split: this release
widens no access; X-1 is release 2). DRAFT: no half is signed and nothing has been deployed.

## Pin and artifact

- **Pin:** dell2 CLOUD `c246d6a180`. `git diff c246d6a180 HEAD -- ycharts/generate lambda-source-map.json` is empty (read
  ~21:0xZ), so HEAD builds the same package.
- **Built artifact (BUILD_ONLY, gates passed):** `SXaOShexFuPnQ9nc9Baglzwk2TXhJz46NkXtunJ0Pks=` (100 members).
- **Live now / ROLLBACK:** `uFTONal/RhfoETes4rqJ4xRjJV4d2/nv3OlwuR9AXCQ=` (LastModified 2026-10-04T01:57:24Z, 114 members).

## Every changed member (`release-census.py irpt-ycharts-generate --pin c246d6a180`; changed_members=20)

| member | change | owner / half | why |
|---|---|---|---|
| `served.py` | changed | ~P (IB-pr-357) | response envelope drops `internal_correlation_id` (the F1 fix) |
| `canonical_profile_reads.py` | changed | ~P | OWED: ~P2 names the order (msg 1089) |
| `loaders.py` | changed | ~P | OWED: ~P2 |
| `maintained_sources.py` | changed | ~P | OWED: ~P2 |
| `publication_worker.py` | changed | ~P | OWED: ~P2 |
| `publisher.py` | changed | ~P | OWED: ~P2 |
| `fixtures/har/*` (14) | removed | Y (E-Y4, @d96da06035) | test-only fixtures leave the package |

**NOT in this release:** `uploads.py`, `interactive_access.py` and `generate_installed.py` stay at staged pin `3f29017cfc`.
X-1 does not ship here.

## What moves, and what does not

- **Moves:** one function, `irpt-ycharts-generate`.
- **Widens:** no principal class, no route and no grant.
- **Does not move:** the resident host (`~G2`'s), its `resident_worker.py`, and every other function.

## After-reads (each branch named)

1. **E-Y4 leg 1:** the deployed zip (fetched from `get-function` Code.Location) has 0 `fixtures/har` members.
2. **E-Y4 leg 2:** the fixture tests pass at `c246d6a180` on a host with PyMuPDF. `2.0.0_SA_COO~G2` relays this to the
   laptop, which returns a result FILE (laptop ruling 106216).
3. **E-Y4 leg 3:** the trace control on the extracted deployed zip: 0 hits with the TOKEN regex of
   `R62_checks/check_624_fixtures_dropped.py`, and exactly 1 with a planted reader.
4. **IB-pr-357:** a served response envelope from this function carries no `internal_correlation_id`. ~P2 names its
   control.
5. **No regression:** one ordinary authorized Analysis request answers as before (READY path, no new refusal).
6. **Equality:** the deployed CodeSha256 equals the built `SXaOShex...`. Then the source map is recorded at that hash
   (S320's close-leg step), with no undeployed commit stamped.

If any of 1, 3, 4, 5 or 6 fails, roll back to `uFTONal...` in the same session. A failure of leg 2 holds E-Y4 as unserved
without rolling back, because the tests read the repo, not the zip.

## Still owed before signing

- ~P2: an order per member for its 5 riders, and the IB-pr-357 control (msg 1089).
- ~G2: the leg-2 relay command at `c246d6a180`.
