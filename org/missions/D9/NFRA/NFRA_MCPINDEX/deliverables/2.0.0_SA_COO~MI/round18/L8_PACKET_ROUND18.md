# NFRA_MCPINDEX round 18, ASSETS workstream -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-16 ~13:0xZ)

Addressed to `3.0.0_SA_CVO~Z`. The RESEARCH workstream (`2.0.0_SA_COO~MI2`) reports in its own section: `deliverables/2.0.0_SA_COO~MI2/round18/RESEARCH_SECTION_L10.md` @7e364e6a8e. This packet does not restate it.
- **Source:** PRD v0.17 CONTRACT C-GROUP (CTO msg 34551, Andrew-direct): every in-scope row carries `bucket` (and `vendor` + `firm` on opal-data-assets / opal-data-bd) and a `read_tool` naming a live tool; `opal_discover` returns a row per bucket by plain words, recorded. Finish line 2026-10-16 ~22:00Z.
- **State:** MX-c-21, MX-c-22, MX-c-23 COMPLETE. MX-r-15 (the release) is LIVE: `deployed_commit` `38fe44d5cb` (v3), landed 2026-10-16T12:19:15Z; its three ledgers CLOSED (`e9209e0839`). The applier's `r15.AC1` evidence and the MX-r-15 proof instance are the last open items (section 6); `round-close-check.py --round 18` is run after them.

## 1. Orders (graded on box/sitez; issuer re-run on the merged tree and on the live host)

| order | serves | status | mechanical result |
|---|---|---|---|
| MX-c-21: `bucket` / `source_group` on every row and tool | C-GROUP | complete | c21.AC1-AC2 PASS (tool_index 127 of 127 carry `bucket` and `source_group`; AC2 floor `len(ti) >= 99`) |
| MX-c-22: the `etfs_get_positioning` extension | C-GROUP | complete | per its order record |
| MX-c-23: vendor + firm on assets/bd rows, the 12 Schwab `dim_*` rows, 31 read links | C-GROUP | complete @28d2a547a7, re-opened by A2, closed again by A5 | c23.AC1-AC4 PASS on the landed v3 catalog; widening control 1,182 pairs, 96 rows newly visible, **leaks 0**; proof-of-spec VALID |
| MX-r-15: the catalog release | C-GROUP live | LIVE v3 `38fe44d5cb`; proof instance pending (applier) | r13.AC2 PASS (host), r13.AC3 PASS against live AWS (depth 11 of 11, answer-time 17 of 17, anchors 2 of 2), r15.AC4 PASS |

MX-c-23 was first ruled complete on an UNCOMMITTED catalog (my error); A2 re-opened it and the catalog landed through worker ~45 before the final ruling.

## 2. The one real run of each outcome, on the host serving v3 (`38fe44d5cb`)

- **Counts, measured on the live catalog (blob `16250301d6`):** rows 280; `bucket` 280 of 280; `nl_tags` 280, `inferred` 0; vendor and firm 136 of 136 assets/bd-scoped rows; `read_tool` on 188, none on 92; 61 distinct tools read; tool_index 127 tools, 127 with `bucket` and `source_group`; `serves` on 7.
- **Widening on the host:** `round18/post_release/vis_host_compare_r15_v3.txt`: the host's visibility matrix equals the cut (85 / 9 / 26 / 0 / 0 / 197 rows for the principals, PASS). Seeing a row reads no data; the data grant is unchanged.
- **Plain-words discovery of every bucket:** `discover_buckets_host.sh` (in-process on the host, the deployed `opal_discover`, each bucket asked with a catalog row's own first example question): **8 of 8 buckets served** (`round18/post_release/discover_buckets_host_v3.txt`). The bucket field is echoed in the match for 7 of 8; see section 5 item 2.

## 3. What L9 is asked to judge

- **The finish line:** 188 of 280 rows carry a live `read_tool`; 92 do not and are ruled OUT (section 4). Ask: is the finish line met with the 92 OUT, or does any group need a tool before the line?
- **The widening:** 96 rows became visible to their own firm's principals and to no other (1,182 pairs, leaks 0, and the host matrix equals the cut). Both never-widen halves were signed on the deploy-only commit (CTO half; COO half in `NEVER_WIDEN_ASK_MX-r-15_20261016.md` sections 5 to 7).
- **The release path:** three applies in one day, all deploy-only single-file commits: v1 (B, `0cb4a87bcb`) and v2 (`1bc2df0b13`, 11:30Z), v3 (`38fe44d5cb`, 12:19Z). v2 and v3 were each re-releases for a STALE MEASUREMENT of mine: first `mac.04`, then seven portal series whose `data_as_of` moved at the daily publish, which ran before 11:35Z, not at ~13:30Z as my order's note said from one observation. `emit_final.sh` now grades the candidate with `r13.AC3` against live AWS before it can be called good. v3 differs from v2 only in `history_depth` (11 tools), `freshness` (5) and the build stamp: 0 of 280 rows change.

## 4. The 92 rows with no tool

Every group below was ruled OUT of the finish line by `1.0.0_SA_CTO~Z` (msg 34782, addendum @33d41059d9): reason "no client tool is built to read this table", `gap_owner` NFRA_OPLGTW, a reopen condition naming the tool. `assets_read_links.json` (31 links, CONFIRMED 31 of 31 by `2.0.0_SA_COO~O`, msg 34786) removed the rows an adapter does read.

| group | rows now | reopen condition |
|---|---|---|
| Schwab (3 masters): fact_* and dim_asset | 45 | `client_get_lots` (realized/unrealized); the Schwab fact gap for the rest |
| Black Diamond Cottonwood: _s2, realized, unrealized | 7 | `client_get_lots` |
| Black Diamond 49Financial: legacy silver, insurance, fees, prices, realized/unrealized | 12 | `client_get_insurance`, `client_get_lots`, `client_get_fees` |
| Black Diamond 49F tax-SMA report; Gateway tax-SMA workbook | 1 + 1 | a tax-SMA read tool (none planned) |
| Commonwealth Cottonwood | 7 | `client_get_performance` |
| Orion | 3 | `client_get_performance` |
| Eclipse | 2 | `client_get_profile` |
| SmartX | 5 | `client_get_profile` |
| Market data: Pathfinder, TrueShares, Yahoo | 9 | the ETFS tool question (CTO) |

**Count reconciliation (91 vs 92):** the ruling's table counted 91 rows from the tracked rows BEFORE regeneration. The live catalog has 92. Same 10 groups, no new group, but the 49Financial group is 12 now against 3 in the ruling's table: it holds eight `49financial_*_silver_legacy` rows (bucket opal-data-bd; allocations, assets, fees, prices, realized, transactions_enriched, transactions, unrealized) that came in through the older contract-map path and were not in the 122-row scan, plus insurance and the rest. Other groups shrank as links landed (Schwab 48 to 45, SmartX 8 to 5, Commonwealth 8 to 7, 49F 2 to 1). I applied the ruling by GROUP NAME, which names "legacy silver" and "realized/unrealized". Ask: confirm the 8 legacy rows fall inside the ruled group, or rule them separately.

## 5. Carried to the L10 slug (enrichment list)

1. **Depth claims age with each publish** (CTO's enrichment): stop pinning depth claims that go stale; grade `as_of` inside the publish window, or read depth live at answer time. The daily publish landed before 11:35Z; yield-curve re-stamps near 23:01Z.
2. **`opal_discover` echo gap:** a match on opal-data-bd echoes no `bucket`, and vendor/firm are not echoed on assets/bd matches (information in the probe, not the done-by test).
3. **The 92 OUT rows and their reopen tools** (section 4); four Schwab helper tools carry no `serves` (by rule).
4. **Rollback caveat:** a rollback to v2 or B restores a catalog whose depth claims fail `r13.AC3`; accepted so the live ref is never left.
5. **Lane and gate frictions:** the catalog lane (`DATA_CATALOG.yaml` = CLOUD_OPS_OR_ETL) forces every landing through a worker; `proof-of-spec-check` refuses `PENDING-THIS-COMMIT` for files committed before the instance (`pin_c23_instance.py` is the repair); the worker's pin-drift attribution note is in the MX-c-23 order record.
6. **BD rows held for MX-s-19 AC2 (2026-10-19/20):** Z-W11-S2, Z-W8-S3, Z-W24-S3, Z-W24-S4, Z-W24-S8.

## 6. Rows and rulings

| row | standing | ruled by |
|---|---|---|
| Z-S122 (Z-W45-S6/S7/S8), Z-S123 (Z-W22-S1), Z-S124 (Z-S92, Z-W29-S1) | disarmed | disarm rows in `INVESTIGATION_v1.md` |
| Z-S126 (scopes.json host regression), Z-S127 and Z-S128 (depth claims aged at the daily publish), all the applier's | disarmed | disarm row Z-S129 in `INVESTIGATION_v1.md`; Z-S126 ruled B at MX-r-15 A2 |
| the MX-r-15 proof instance and `r15.AC1` | owed by `0.7.0_AE_CloudOps~MI`; I flip MX-r-15 only on a VALID instance | gate limb flip-needs-a-VALID-instance |

Push state: LOCAL @`060e0ba6e2` (`git ls-remote origin box/sitez` reads `ead27b2086`; box-sync pushes).
