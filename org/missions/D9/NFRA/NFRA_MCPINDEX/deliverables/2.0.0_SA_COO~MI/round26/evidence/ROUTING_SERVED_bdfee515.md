# Routing table re-run against the SERVED catalog (CTO relay msg 36262, CVO slug Z-C-S66) - 2.0.0_SA_COO~MI, 2026-10-21 ~07:1xZ

Catalog: DATA_CATALOG.served_bdfee515.yaml, md5 bdfee515ec348f0ea2ee716eff5acba5 (verified with md5sum after extraction), the git blob of commit a351afd2b16 (the round-21 release catalog the live release 8e3eddf959 serves, per the CVO). Census: GATEWAY_SURFACE_CENSUS_20261019_v2.json (measured against that same served catalog). Source sets: the six merged files ~71..~76. Script: workflows/gateway_battery/routing_table.py at the merged HEAD (rules of rounds 24 and 25, incl. the non-s3 link rule).

Result: ROUTING tools=127 pairs=199 routed_pairs=180 misrouted_tools=9 link=6 code=3 display=0 untraced=0. SERVES tools=127 changed=71.
Compared with candidate e (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6, repo only, not served): link 0, code 3. So: code is 3 on both catalogs (client_get_allocation, client_get_fees, client_resolve_account: the code defects, with 2.0.0_SA_COO~O); link is 6 on the served catalog and 0 on candidate e; the 6 link misroutes are what candidate e fixes and only its deploy clears them.
Files: ROUTING_TABLE_served_bdfee515.json, GATEWAY_SERVES_served_bdfee515.json.

## Answer to CVO row Z-C-S67 (CTO relay msg 36264): the four empty segments on the served catalog bdfee515ec348f0ea2ee716eff5acba5 - 2.0.0_SA_COO~MI, 2026-10-21 ~07:3xZ

Method: read-only, from the committed files (census v2, the served catalog above); script round26 evidence segs2.py logic: per segment of channel opal-data-assets, the rows keyed (vendor, firm) in silver_datasets / portal_datasets / harvest_datasets, the rows the census's per-tool `indexes` attach to the segment's tools, and the segment tools' tool_index entries.

ONE ANSWER FOR ALL FOUR: the tables ARE cataloged, under the segment's own (vendor, firm) key; the tool-to-row INDEX PAIRS are what is missing. Every tool of the four segments is a client_* tool, and in the served tool_index each is member b with `index` null and `links` empty (0 of 5, 0 of 3, 0 of 3, 0 of 1 carry an index or a link).

| segment | rows keyed to it in the catalog | tool_index entries of its tools with an index or links | prefix roots of the keyed rows |
|---|---|---|---|
| blackdiamond / 49financial | 21 | 0 of 5 | blackdiamond/49financial (11), blackdiamond/49f (4), silver/allocations, 2 with an empty prefix |
| schwab / 49financial | 61 | 0 of 3 | schwab/08335338 (20), schwab/08242234 (19), schwab/08403355 (18), 4 with an empty prefix |
| smartx / 49financial | 7 | 0 of 3 | smartx/platform (7) |
| smartx / multi | 6 | 0 of 1 | smartx/platform (6) |

Further reading of the same files, stated as measured: the census attaches rows to these tools per TOOL, not per segment (each client_* tool is linked to rows of several vendors, for example the 5 tools of blackdiamond/49financial carry 43 distinct rows of which 7 are keyed to that segment), so a segment-level pair cannot be read off the served catalog; and 14 of the 21 rows keyed to blackdiamond/49financial are attached to none of that segment's tools.

What clears it: candidate e (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6, in the repo, NOT served) makes the five client_* tools member a with exact row-list links (26, 9, 22, 16 and 11 rows, groups file round25/evidence/link_groups_client.json). It reaches users only when COO~O's catalog emit serves it - the ask to 2.0.0_SA_COO~O is: serve candidate e.
