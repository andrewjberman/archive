# NFRA_MCPINDEX round 26 - state (2.0.0_SA_COO~MI, 2026-10-20 ~20:0xZ)

Orders: MX-z-1..4 complete and merged (77a12bb188d); proofs valid. round-close-check reads REFUSED only for the absent reviewer seat (broker down), as in round 25.
Done at the drain:
1 the 15 uncatalogued tables: 10 rows + 5 reasons (Z1) and the opal_describe row (Z4) are catalog entries; candidate e (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6) placed in the repo (1ade26b4602), NOT deployed (rides COO~O's release). Coverage 0 refusals, 94 explained; routing 300 of 300 routed, link 0, code 3.
2 the Eclipse copier: opal-assets-ingest-mirror (cron 13:05Z and 17:05Z) then opal-assets-silver-eclipse; owner OPAL_ASSETS; producer ADVI_ECLDAT; relay asked of the CTO (ferry 195434Z).
3 source checks: 4 store tools read through two clients (gateway + direct DynamoDB), all agree; the 33 graph and 9 integration tools have no second client in this session and stay FAIL source_unchecked with their reasons. Battery PASS 54 of 127 (round 25: 51); tool_battery.py route matcher now reads a source's table.
4 the 2 coverage refusals: closed by Z4 (opal_describe row, opal_discover c).
+ xref re-measure (CTO ferry 194313Z): coverage unchanged, 5,668 of 8,032 (XREF_REMEASURE_20261020.md).
Open: item 5, the per-vendor re-run of the routing script and the battery after batch16 (2026-10-21 06:00Z), two gateway calls at a time; the round closes after it. Sheets site HELD for Andrew; nothing uploaded.
