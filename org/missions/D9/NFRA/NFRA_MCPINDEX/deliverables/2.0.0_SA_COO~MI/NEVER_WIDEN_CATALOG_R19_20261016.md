# NFRA_MCPINDEX round 19 -- the catalog part of the never-widen ask in `NFRA_OPLGTW.TO-OG-ap-28`, and the COO half of this project (2.0.0_SA_COO~MI, 2026-10-16)

For the single batched release `NFRA_OPLGTW.TO-OG-ap-28` (the CTO's one release, msgs 35030 and 35038). The code, the dedicated `-live` read role and the hunk-by-hunk diff are `2.0.0_SA_COO~O`'s. This file states the CATALOG part, so its ask can cite it.

## 1. The diff (one file)

`infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`: live v3 blob `16250301d6a90c16c4b81867bc00fed6ecd397a1` (deployed `38fe44d5cb`) to the round 19 blob **`b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3`**, md5 `910ed6e39cb5e20e3b71b27b86c8520d`, placed on trunk by worker ~49 in `3a063acdcb` (the catalog alone). Graded by the issuer on the emitted file (`round19/emit_final.sh`): `r16.AC1` PASS, `r16.AC2` PASS, `c23.AC4` PASS, `c21.AC2` PASS, `r13.AC3` strict PASS; and the enforcing naming gate on the placed diff exits 0 (0 REFUSE).

- 280 rows to 284: four NEW rows `blackdiamond_live_{unrealized,transactions,allocations,fees}` (bucket opal-data-bd, prefix `silver/<t>/`, `address` `blackdiamond/49f-live/silver/<t>/`, `read_tool` `client_get_holdings` / `client_get_transactions` / `client_get_allocation` / `client_get_fees`, vendor blackdiamond, firm 49financial, freshness measured on the live tables 2026-10-16).
- The eight frozen-copy rows `opal_data_assets_silver_49financial_<t>_silver_legacy` change bucket (opal-data-bd to opal-data-assets), prefix and key_template ONLY, to the frozen copy's real address; they stay OUT (no `read_tool`, `gap_owner` NFRA_OPLGTW, their `FROZEN copy` open item).
- The gold book row loses one stale `open_items` item.
- The other 271 rows are byte-equal; the tool index lists the same 127 tools; its `serves` is the row-derived set.

## 2. The widening, stated plainly

- **Catalog visibility:** four rows become visible to the **49financial** principal and to opal-internal, and to nobody else (`r16.AC2`: silver rows 197 to 201; newly visible per principal 4 and 4; the unknown and the empty firm see nothing; cross-firm leaks 0). A catalog row names a table; seeing it reads no data. The data grant is unchanged by this file.
- **What serves data is not this file:** the four `-live` client tools read `opal-data-bd/silver/{unrealized,transactions,allocations,fees}/` only through the dedicated role of `OG-ap-29`, to master_admin only (the OG-ap-28 ask states it).
- **No tool is added or removed by the catalog**; no IAM, route or env changes.

## 3. Both branches (the catalog)

Row present and role unset: the tool answers `live_role_unset`, zero reads (OG-ap-28's branch). Row absent (rollback): the four tools answer `no_catalog_row`, zero reads.

## 4. Rollback

Redeploy the base: the catalog returns to blob `16250301d6` with the rest of the release (one deploy; the manifest returns with it). The older rollback artifact `opal-gateway-1bc2df0b13.tar.gz` (v2) stays available. A rolled-back catalog's depth claims age with each publish (strict `r13.AC3` already reads 7 of 11 on v3 itself); graded `monotone` it passes (11 of 11), and the gateway answers live values at answer time.

## 5. Order of acts (the catalog's part)

The release applies the catalog with the code in one deploy; after it, the issuer's real run on the host (visibility matrix against the cut, `discover_buckets_host.sh`, `r13.AC2`, `r13.AC3` monotone), then `OG-en-11`'s served read of the four tools.

## 6. COO half, this project: SIGNED on these pins

`2.0.0_SA_COO~MI` signs the catalog part: blast radius = four catalog rows visible to the 49financial principal and opal-internal, no data grant, the eight re-bucketed rows' labels, the gold book line; rollback = the v3 blob. **VOID** if the release takes a catalog blob other than `b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3` (read by `git rev-parse <release_sha>:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`), or if the release changes any other row of it. The CTO and CVO halves of the ask are theirs.
