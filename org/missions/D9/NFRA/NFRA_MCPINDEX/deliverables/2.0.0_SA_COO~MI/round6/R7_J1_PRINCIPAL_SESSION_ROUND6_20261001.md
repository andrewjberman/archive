# r7.J1 re-grade material -- the issuer's principal-session asks after MX-r-8 served (2.0.0_SA_COO~MI, 2026-10-01 ~12:5xZ)

**For:** MX-v-7 J1 (the r7.J1 RE-GRADE at L9 by 3.0.0_SA_CVO~O). This is MATERIAL, not a grade.
**Round-5 baseline:** `deliverables/2.0.0_SA_COO~MI/round5/R7_J1_PRINCIPAL_SESSION_20261001.md`. That run read
`catalogued: false` for the BD fees question.

**Served state at the asks:** opal-gateway `-latest` git-ref `e3567ce5f788f45195bec065f4d2fc5a68a38cd3`, uploaded
2026-10-01T12:36:17Z (MX-r-8, train slot 4). PHASE B read-back was in flight with worker ~22 at the time of the asks.

**Principal:** this seat's `opalgateway` MCP connection (Andrew Berman, an admitted Opal principal; the OPAL_INTERNAL
scope). Its tool list refreshed during the session and now lists `blackdiamond_list_fees` and `etfs_get_positioning`,
so this is a principal session whose tool list postdates the release.

## The asks

| ask | catalogued | first match | next_tool |
|---|---|---|---|
| `what fees did Black Diamond charge` | **true** | `blackdiamond_fees` (channel `silver_datasets`, firm-scoped, SERVE-WITH-CAVEAT, 4 caveats) | **`blackdiamond_list_fees`** (`kind: mcp_tool`) |
| `Schwab positions` | **true** | `schwab_dim_position`, then `schwab_dim_balance` (both `silver_datasets`, firm-scoped) | **`schwab_query`** |

On both silver matches, `served_written_at` reads `claim: absent` with error class `silver_row_has_no_s3_key`. That is
honest: there is no S3 key to HEAD, and nothing is invented.

## The tool call -- `blackdiamond_list_fees(scope="49financial")`, newest partition

- `status` ok. `as_of` 2026-09-29. `source_as_of` 2026-09-29. `as_of_field` trade_date. Source `opal-data-bd/silver/fees`.
- **Denominators:**
  - rows_matched 22,853; rows_returned 200 (truncated, row_cap 200);
  - duplicate_transaction_ids 632;
  - partitions read 1, empty 0, absent 0.
- **Totals for 2026-09-29** (basis: `transaction_fee` and `account_fee` only, after de-duplicating on `transaction_id`):
  - rows_deduplicated 22,221;
  - **transaction_fee 63.43**;
  - account_fee 0.0.
- No row content and no account identifier is recorded here.

## What remains for J1

The same figure (transaction_fee 63.43 for 2026-09-29) and as-of, compared against the source object read BY VersionId.
That is MX-v-7 AC1's record (`deliverables/0.9.0_WK_NFRA_MCPINDEX~22/THREAD_RERUN_round6.json`), cut after MX-r-8 drains.

**Route clause, as measured:** discover names `blackdiamond_list_fees` for the BD fees question through a principal
session. Round 5's FAIL condition no longer holds on the served gateway.
