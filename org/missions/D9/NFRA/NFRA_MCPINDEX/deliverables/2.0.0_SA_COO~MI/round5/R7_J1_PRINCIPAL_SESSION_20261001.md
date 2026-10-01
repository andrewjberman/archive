# r7.J1 material -- the issuer's principal-session asks on the live gateway (2.0.0_SA_COO~MI, 2026-10-01 ~07:5xZ)

**Order:** `NFRA_MCPINDEX.TO-MX-r-7.bd-release.md`, item 6 and criterion J1. J1 is judgment, graded at L9 by
3.0.0_SA_CVO~O and never self-graded. This file is MATERIAL, not a grade.

**Served state at the asks:**
- opal-gateway live 05e3eff563, deployed 07:13:52Z (ledger `nfra-mcpindex-r5-bd-release` CLOSED 7/7).
- r7.AC1 and r7.AC2 re-graded PASS on CLOUD @1232c96dc7.

**Principal:** this seat's `opalgateway` MCP connection. `whoami` reads Andrew Berman (Andrew@opalinvest.com), an
admitted Opal principal.
- This session's tool list was loaded before the deploy, so `blackdiamond_list_fees` is not callable from it. A fresh
  session is needed for the tool call itself.
- `opal_discover` is callable and answers live.

## The asks, verbatim results

| subject | catalogued | matches | next_tool named |
|---|---|---|---|
| `what fees did Black Diamond charge` | **false** | 0 | none: "not catalogued: no dataset in the catalog answers it for this principal" |
| `ETF positioning` (control) | true | 1 (`platinum/etfs/positioning_data.json`, opal-internal, SERVE-WITH-CAVEAT) | **`etfs_get_positioning`** (MX-t-10, shipped in this release) |

The catalog home reports `app/refs/DATA_CATALOG.yaml` version 0.4.

## What this says for J1

- **The ETF half of the release is routed end to end.** Discover names the new tool for its question class.
- **The BD half is NOT routed.** The tool is served and its in-process call succeeds (worker ~21: outcome ok, as_of
  2026-09-29, 1 of 1 partition, rows_matched 22853). But discover does not name it, because `opal_discover` never reads
  the catalog's `silver_datasets` section, where the `blackdiamond_fees` row sits (row Z-W21-S22, ruled in Z-S70).
- J1's clause "the route discover gave names that tool" is therefore UNMET for Black Diamond on the live gateway, as
  measured.
- The repair is an enrichment item for the round-5 analysis. It repeats the Schwab catalog-row shape (CTO msg 27367).

## Not done here

- A `blackdiamond_list_fees` call through a principal session. It needs a fresh MCP session whose tool list postdates
  07:13Z.
- A figure-and-as-of comparison against the source object read by VersionId. The in-process material is in the
  worker's proof instance (`deliverables/0.9.0_WK_NFRA_MCPINDEX~21/`).
