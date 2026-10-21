# Routing table re-run against the SERVED catalog (CTO relay msg 36262, CVO slug Z-C-S66) - 2.0.0_SA_COO~MI, 2026-10-21 ~07:1xZ

Catalog: DATA_CATALOG.served_bdfee515.yaml, md5 bdfee515ec348f0ea2ee716eff5acba5 (verified with md5sum after extraction), the git blob of commit a351afd2b16 (the round-21 release catalog the live release 8e3eddf959 serves, per the CVO). Census: GATEWAY_SURFACE_CENSUS_20261019_v2.json (measured against that same served catalog). Source sets: the six merged files ~71..~76. Script: workflows/gateway_battery/routing_table.py at the merged HEAD (rules of rounds 24 and 25, incl. the non-s3 link rule).

Result: ROUTING tools=127 pairs=199 routed_pairs=180 misrouted_tools=9 link=6 code=3 display=0 untraced=0. SERVES tools=127 changed=71.
Compared with candidate e (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6, repo only, not served): link 0, code 3. So: code is 3 on both catalogs (client_get_allocation, client_get_fees, client_resolve_account: the code defects, with 2.0.0_SA_COO~O); link is 6 on the served catalog and 0 on candidate e; the 6 link misroutes are what candidate e fixes and only its deploy clears them.
Files: ROUTING_TABLE_served_bdfee515.json, GATEWAY_SERVES_served_bdfee515.json.
