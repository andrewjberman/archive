# CORRECTION -- the round-22 census (v1) undercounted; v2 supersedes it (2.0.0_SA_COO~MI, 2026-10-19 ~16:05Z)

**What was wrong.** `breakdown_real_20261019.json` (read 14:53:37Z) and the files derived from it (`GATEWAY_SURFACE_CENSUS_20261019.json`, `GATEWAY_GRANTS_20261019.json`, `COVERAGE_*_20261019.json`) were taken by `host_breakdown.py` in a fresh process that imported only `app.admin_gateway_breakdown`. The served process registers the `ENABLED_INTEGRATIONS` onto the shared `mcp` when `app/server.py` is imported (line 91), before it computes the page's data. The fresh process never did, so every integration-registered tool was missing. The round-22 decomposition (R22.1, R22.2 ruling 2) and the close message called this "the data the /gateway page renders"; for the integration tools it was not.

**How it was found.** Round 23's first look at the residual rows found `schwab_query`, `mdpf_get_aum_metrics`, `etfs_get_positioning` named by catalog rows but absent from the census, while this seat's own connector lists them. `integrations/schwab/integration.py:1171` registers `schwab_query` at registration time.

**The fix.** `host_breakdown.py` now reads the env the way systemd does (one pair of surrounding quotes stripped; the first attempt left `"ycharts` and `blackdiamond"` unregistered, 12 channels) and calls `integrations.register_enabled(tools.mcp, ENABLED_INTEGRATIONS)` before `_compute()`. The v2 read is `breakdown_real_20261019_v2.json`, 16:02:52Z, ssm command `0b455a1e-c194-416d-94cd-e508236dea03`, 59016 bytes, registered: blackdiamond 1, globgrph 2, opal_discover 2, opal_portal 2, portal_index 6, schwab 5, ycharts 6.

| | v1 (wrong) | v2 |
|---|---|---|
| channels | 7 | 14 |
| kinds | bucket 5, store 1, native 1 | bucket 5, store 1, integration 7, native 1 |
| tools | 103 | 127 |
| tools with no catalog index | 48 | 60 |
| member-b tools (coverage gate) | 94 | 104 |
| rows with no served read_tool | 106 | 91 (all carry gap_owner NFRA_OPLGTW) |
| harvest channel | 14 tools, 14 member b | unchanged |

**What stands.** The harvest battery (16 cases, 14 tools; PASS 10, EMPTY-CORRECT 4) and the harvest coverage result (14 member b) are unchanged: harvest has no integration tool. The 12 criteria and the four scripts are unchanged.

**What does not stand.** The 103 and 7 figures, "no integration channel today", "94 member-b" and "106 rows" in the round-22 record. The v1 files stay in place as the record of the error; use the `_v2` files.
