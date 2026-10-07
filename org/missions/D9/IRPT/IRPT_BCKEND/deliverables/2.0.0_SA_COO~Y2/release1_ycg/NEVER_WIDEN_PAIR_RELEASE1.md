# irpt-ycharts-generate RELEASE 1 -- never-widen pair DRAFT (IB-pr-357 + ~P's riders + E-Y4)

**Deployer:** `2.0.0_SA_COO~Y2`, the function's lane. **Ruling:** `1.0.0_SA_CTO~DELL2` msgs 1084 and 1089 (split: this release
widens no access; X-1 is release 2). DRAFT: no half is signed and nothing has been deployed.

## Pin and artifact

- **Pin:** dell2 CLOUD `1b5afe6a49` (~P2's served.py re-pin, msg 1102; CTO~DELL2 msg 1097). The first draft's pin
  `c246d6a180` staged an OLD served.py (0642c9d004), so it would not have shipped IB-pr-357. ~P2's record @7e28cd9ec5 found it.
- **Built artifact (BUILD_ONLY at 1b5afe6a49, gates passed, re-run by this seat):** `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=` (100 members).
- **Live now / ROLLBACK:** `uFTONal/RhfoETes4rqJ4xRjJV4d2/nv3OlwuR9AXCQ=` (LastModified 2026-10-04T01:57:24Z, 114 members).

## Every changed member (`release-census.py irpt-ycharts-generate --pin 1b5afe6a49`, re-run by this seat; changed_members=20; `CENSUS_1b5afe6a49.txt`)

| member | change | owner / half | why |
|---|---|---|---|
| `served.py` | changed (built 7cc704) | ~P (IB-pr-357; rider IB-pr-326 @cd9a61bb0c) | response envelope drops `internal_correlation_id` (the F1 fix). IB-pr-326 is the guarded path's enforcer_for refusal: OWED, ~P states why it is safe to ship |
| `canonical_profile_reads.py` | changed | ~P (IB-pr-321/322) | per ~P2 msg 1102 / @7e28cd9ec5 |
| `loaders.py` | changed | ~P (IB-pr-321/322) | per ~P2 msg 1102 / @7e28cd9ec5 |
| `maintained_sources.py` | changed | ~P (IB-pr-321/322) | per ~P2 msg 1102 / @7e28cd9ec5 |
| `publication_worker.py` | changed | **~G2** (YCD-g-6, i-6, l-6) | INERT for served traffic. ~G2 msg 1114, VERIFIED by this seat on the built zip: the live Handler is `generate_installed.lambda_handler`, and its static import closure reaches 41 of 62 modules, NEITHER of these. The one dynamic `import_module` (`import_census`, generate_installed.py:380-394) runs only on a direct IAM invoke of exactly `{"irpt_import_census": true}`, which API Gateway events cannot take, and only imports. |
| `publisher.py` | changed | **~G2** (YCD-g-6, i-6, l-6) | INERT for served traffic, as above (verified) |
| `fixtures/har/*` (14) | removed | Y (E-Y4, @d96da06035) | test-only fixtures leave the package |

**NOT in this release:** `uploads.py`, `interactive_access.py` and `generate_installed.py` stay at staged pin `3f29017cfc`.
X-1 does not ship here.

## What moves, and what does not

- **Moves:** one function, `irpt-ycharts-generate`.
- **Widens:** no principal class, no route and no grant.
- **Does not move:** the resident host (`~G2`'s), its `resident_worker.py`, and every other function.

## After-reads (each branch named)

1. **E-Y4 leg 1:** the deployed zip (fetched from `get-function` Code.Location) has 0 `fixtures/har` members.
2. **E-Y4 leg 2:** the fixture tests pass at `1b5afe6a49` on a host with PyMuPDF. `2.0.0_SA_COO~G2` relays this to the
   laptop, which returns a result FILE (laptop ruling 106216).
3. **E-Y4 leg 3:** the trace control on the extracted deployed zip: 0 hits with the TOKEN regex of
   `R62_checks/check_624_fixtures_dropped.py`, and exactly 1 with a planted reader.
4. **IB-pr-357:** a served response envelope from this function carries no `internal_correlation_id`. ~P2 names its
   control.
5. **No regression:** one ordinary authorized Analysis request answers as before (READY path, no new refusal).
6. **Import closure:** one direct IAM invoke of `{"irpt_import_census": true}` (imports only; no route, write or vendor
   call) returns `failed: {}` across all packaged modules, including the two inert ~G2 members.
7. **Equality:** the deployed CodeSha256 equals the built `ZspX0qD2...`. Then the source map is recorded at that hash
   (S320's close-leg step), with no undeployed commit stamped.

If any of 1, 3, 4, 5, 6 or 7 fails, roll back to `uFTONal...` in the same session. A failure of leg 2 holds E-Y4 as unserved
without rolling back, because the tests read the repo, not the zip.

## Still owed before signing

- ~P: why IB-pr-326 is safe to ship, and the IB-pr-357 after-read control.
- ~G2: DONE (msg 1114). Rider ownership is verified above. The leg-2 relay command is with 0.0.0_AB_MSTR~DELL2: `cd infra/aws/lambda/investor-reporting && { python -m pytest -q -p no:cacheprovider ycharts/generate/tests; python ycharts/generate/tests/run_offline_suite.py; echo offline_rc=$?; } > FITZ_RELAY_REL1_1b5afe6a49.txt 2>&1`, run at 1b5afe6a49 once on origin; recipient ~G2.
- The pin must reach origin before the laptop relay can run at it (pushes are 0.0.0_AB_MSTR's).
