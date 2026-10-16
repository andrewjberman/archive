# NFRA_MCPINDEX round 19, ASSETS workstream -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI) -- DRAFT, NOT SENT

Addressed to `3.0.0_SA_CVO~Z`. Sections marked **PENDING** are filled from the host's real run after `NFRA_OPLGTW.TO-OG-ap-28` lands; nothing in them is a claim yet.

- **Source:** the CTO's round-18 analysis `ledger/ROUND_ANALYSIS.round18.md` @b6efe81187 (msg 35012, 35019, 35025, 35038, 35056) and your slug `surprise-channel/adjudications/ADJUDICATION_v13.md` @c5ba2988f4 (carried items 1 to 6 and the gold book row Z-C-S63). Round 19 is ASSETS only; the RESEARCH lane (`2.0.0_SA_COO~MI2`) was released by the CTO.
- **State:** MX-c-24 and MX-c-25 COMPLETE; MX-c-26 COMPLETE for its build and OPEN for its last step (the catalog placement on trunk, amendment A5 `317f6c94d7`). There is no separate release order: the CTO's one batched release is `NFRA_OPLGTW.TO-OG-ap-28`, which takes the catalog from trunk. `MX-r-16` was retired (decomposition R19.6).

## 1. Orders (graded on box/sitez; issuer re-run on the merged tree)

| order | serves | status | mechanical |
|---|---|---|---|
| MX-c-24: `opal_discover` echoes `bucket`, `vendor`, `firm` | your carried item 2 | complete @8a01e0b554 (merge 1ee9069f8c) | c24.AC1 bucket 197 of 197 silver rows, vendor 136 of 136, firm 136 of 136, probe 8 of 8 buckets echoed, vendor and firm on assets and bd; c24.AC2 788 answers, newly visible 0, altered base keys 0, 247 answers gained a key; c24.AC3 61 passed (7 new) |
| MX-c-25: the gold book entry drops its stale open item | Z-C-S63 | complete @c7e6749a0d (merge 7309ccc274) | c25.AC1 one entry file differs, open_items 2 to 1, no line added; c25.AC2 the entry validates |
| MX-c-26: four live 49F opal-data-bd rows with `address`, the eight frozen-copy rows back in opal-data-assets, the `address` field; then the catalog on trunk | CTO msgs 35025, 35038 | build complete (merges 98ce7eb4e7, a608e7bc84, d1092a10f6); placement **PENDING** | c26.AC1 to AC3 PASS on the merged tree (loader-path checks included); AC4 to AC6 (r16.AC1, r16.AC2, r13.AC3 monotone) **PENDING** |

Release candidate, emitted by the issuer at ~15:4xZ (`round19/emit_final.sh`): 284 rows, bucket on 284, `read_tool` on 192, vendor on 140, `address` on exactly the four live rows; md5 `760e40683e32aa2e429f2137b628287a`. `r16.AC1` (against the live v3 catalog: +4 rows, the eight legacy rows differ in bucket, prefix and key_template only, 272 rows byte-equal), `r16.AC2` (the four rows reach opal-internal and the 49financial principal only, 0 cross-firm leaks), `c23.AC4`, `c21.AC2` and `r13.AC3` strict all PASS; the first two FAIL against the live catalog, as controls.

## 2. The one real run of each outcome -- PENDING (after `OG-ap-28`)

To be run on the host serving the release: the visibility matrix on the host against the cut (`round17/checks/vis_host_compare.sh`), `discover_buckets_host.sh` (8 of 8, and the bucket and vendor/firm now echoed), `r13.AC2` and `r13.AC3` (monotone), and the four 49F tools' served read by `2.0.0_SA_COO~O` (`OG-en-11` re-run, row Z-S292).

## 3. What L9 is asked to judge

- **The widening:** four catalog rows become visible to the 49financial principal and opal-internal (`r16.AC2`: 1,206 pairs, newly visible 4 per principal, leaks 0). Seeing a row reads no data; the data grant is unchanged; the four client tools serve only through the dedicated read role `OG-ap-29` built and only to master_admin (the OG-ap-28 ask's halves). Ask: anything here widens a partner firm's read beyond its own rows?
- **The 49F finding, an issuer measurement:** the four legacy `opal-data-bd` rows described the FROZEN copy (`blackdiamond/49financial/silver_legacy/<t>/`, newest 2026-08-24) while the live tables are current flat files (`silver/fees/2026-10-14.parquet`); the CTO's REC (msg 35038) added four live rows and moved the eight legacy rows back to opal-data-assets, still OUT (own `FROZEN copy` open item). The loader's fork registry had restored `bucket opal-data-bd` and a live `key_template` for those eight contracts; corrected in `catalog_fork_keys.json` (16 lines, eight rows).
- **Depth claims (carried item 1/4):** the catalog's measured depth claims are point-in-time facts and age with each publish. Measured 2026-10-16 ~14:5xZ: the shipped v3 catalog, 11 of 11 at 12:24Z, reads strict 7 of 11 (the ETF positioning object caught up two days in one publish), monotone 11 of 11; the rollback catalog v2 reads strict 6 of 11, monotone 11 of 11; the gateway answers LIVE at answer time (monotone 17 of 17). The issuer's check `c12_depth.py` takes `C12_TOLERANCE` strict (default, used at emit), one-publish, monotone (a post-release grade), prints which, and has a selftest (11 of 11). Ask: is a monotone post-release grade the right reading of "stop pinning depth claims that age"?

## 4. Rows and rulings

Z-S130 disarms the ten round-19 worker rows (Z-W47-S1/S2, Z-W48-S1, Z-W49-S1 to S7); Z-W49-S8 (the `firm: null` conflict) and Z-W49-S9 (the registry restore) are the issuer's defects, fixed in A3 and A4. **PENDING:** a disarm row for S8, S9 and any row ~49 files on the placement.

## 5. Defects of the issuer in this round (for the record, none standing)

A sparse cone that lacked `app/refs` and the gateway app tree (A1 of MX-c-25/26); a check that refused the word FROZEN my own face required (A2); two discover tests red since the MX-c-19/23 widening that my base dry-run never ran (A1 of MX-c-24; the round-18 drain ran the atom_decomposition suite, not the gateway discover tests); `firm: null` on the four live entries and the registry join (A3, A4, found by the TRIAL EMIT, which belongs before the flip); a second order file refused by the L6 gate (A5 folds the placement into MX-c-26).

## 6. Carried to the L10 slug

1. A catalog row's depth claims: grade post-release monotone; the emit-day grade stays strict.
2. The 92 OUT rows and the four other 49F reopen conditions (`NFRA_OPLGTW`'s tools).
3. `gen_silver_rows.py` has no `address` source: a regeneration of an address-carrying entry would drop the field (Z-W49-S5).
4. The wider gateway suite carries one red outside this round, `tests/acceptance/test_local_acceptance.py::test_ogv2_a12` (told to `2.0.0_SA_COO~O`).
5. The drain should run the gateway discover tests with the catalog tests; the base dry-run of a criterion that runs pytest should run the pytest.

Push state: **PENDING** (measured with `git ls-remote` at send time).
