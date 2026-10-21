# NFRA_MCPINDEX round 26 - report (2.0.0_SA_COO~MI, 2026-10-21 ~07:3xZ)

Orders MX-z-1..4 complete, merged (77a12bb188d), proofs valid. round-close-check reads REFUSED only for reviewer=ABSENT (the agent-comms broker is down; liveness lists no reviewer seat) - the condition the CTO ruled a tool condition in the round-25 analysis.

## Items of the CTO's round-25 analysis
1. 15 uncatalogued tables: 10 rows and 5 reasons written; candidate e (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6) is in the repo, NOT served. Coverage 0 refusals; routing on candidate e: link 0, code 3.
2. Eclipse copier named: opal-assets-ingest-mirror (cron 13:05Z, 17:05Z) then opal-assets-silver-eclipse; owner OPAL_ASSETS; producer ADVI_ECLDAT (relay asked, ferry 195434Z).
3. Source checks: 4 store tools read through two clients, all agree; 33 graph and 9 integration tools have no second client in this session and stay FAIL source_unchecked with their reasons. Battery PASS 54 of 127 (round 25: 51).
4. The 2 coverage refusals: closed (opal_describe row, opal_discover c).
5. Per-vendor re-run after batch16 (closed 06:44:45Z): below.

## Routing on the SERVED catalog (CVO Z-C-S66/S67, CTO relay)
Catalog bdfee515ec348f0ea2ee716eff5acba5: link 6, code 3. Candidate e: link 0, code 3. The four segments (blackdiamond/49F, schwab/49F, smartx/49F, smartx/multi) are cataloged under their own key; the tool-to-row index pairs are missing in the served tool_index (answer committed @67b4f3a606c). ASK TO 2.0.0_SA_COO~O: serve candidate e in its next catalog emit (the CTO ordered it, ruling @9af9c984db); after it is served the routing table is re-run on the new served md5 and committed with that md5.

## Per-vendor re-run after batch16 (runner 7, one call at a time, counts and codes only; PER_VENDOR_RUN_20261021.json)
Caveat first: the runner passed platform labels it chose (blackdiamond, schwab master numbers, orion, eclipse); the gateway refused several with platform_not_source_label, so those refusals may be input errors of this run, not tool faults - the label vocabulary the tools accept is not in their descriptions.
| firm / vendor | result |
|---|---|
| 49financial / blackdiamond | resolve answers no_candidate_for_last4 on the last four of account_id and ok(1) on the last four of bd_account_number (the resolve matches that column); holdings ok(2); allocation no_model_assignment_49f with weights; fees no_fee_rows_in_window; transactions account_not_in_partition; as_of 2026-10-16 = the unrealized newest. The xref was already shown unchanged in coverage (5,668 of 8,032). |
| 49financial / schwab | both masters refused platform_not_source_label; with no platform the Schwab leg answers no_resolve_source (ruling item 6, COO~O's code, still open). |
| 49financial / smartx | resolve ok(3), holdings ok(39), allocation ok(39), fees no_fee_source, transactions vendor_no_transactions; as_of 2026-10-20 = the newest. |
| cottonwood / blackdiamond | resolve ok(3), holdings ok(38), allocation ok(36 targets), fees ok(1), transactions ok(11); partition 2026-10-19 = the newest. |
| cottonwood / commonwealth | resolve ok(1), holdings 0 positions, allocation no_allocation_source, fees no_fee_source (ruling item 7), transactions ok(0); as_of 2026-06-23 = the newest partition, 83 trading days behind. |
| inflection / orion | firm served now (D1 landed): resolve ok(2), holdings ok(40), allocation ok(26); fees and transactions error tool_error_over_memory_cap (166,082,568 bytes against the 67,108,864 cap) - a NEW code finding for COO~O; as_of 2026-10-20 = the newest. |
| inflection / eclipse | resolve platform_not_source_label; the chain on the eclipse candidate: holdings vendor_no_holdings, allocation account_not_resolved, fees no_fee_source, transactions vendor_no_transactions (ruling item 5, COO~O). |
In every chain that returned data the answer's as_of equalled the newest partition read directly. The census numbers differ from the live listings on two tables (the 49F bridge newest 2026-10-20 by listing, the Eclipse newest 2026-10-20) because the census is older.

## Held / open
Sheets site HELD for Andrew (nothing uploaded). Catalog candidate e deploy: COO~O. Orion over-cap fees/transactions: new defect for COO~O. The graph and integration source checks remain FAIL source_unchecked with reasons.
