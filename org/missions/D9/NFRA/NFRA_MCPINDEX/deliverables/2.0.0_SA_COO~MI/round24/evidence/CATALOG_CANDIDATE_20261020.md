# DATA_CATALOG candidate, round 24 (NOT written to the live file)

The real emit was run and the tracked catalog restored (`git checkout`); nothing was placed. Reason: the diff against HEAD
holds changes beyond commit ef168640331 and the serves map, which the drain directive says to report, not write.

Emit command (root of the workspace, six group maps as round 21 emit_final.sh, plus the map):
`python workflows/atom_decomposition/emit_catalog_v02.py --serves-map GATEWAY_SERVES_map_used_20261020.json --group-map round18/assets_group_map.json
--group-map ~52/research_group_map_h1.json --group-map ~53/research_group_map_h2.json --group-map ~54/research_group_map_h3.json
--group-map ~55/research_group_map_p1.json --group-map round19/live_bd_group_map.json`  (rc=0; TOOL INDEX N=127 a=62 b=10 c=55;
SERVES-MAP tools applied 7 of 127; GROUP-MAP 177 of 177). Candidate: `DATA_CATALOG.candidate_20261020.yaml` md5 2bfc456e20600cdfacb6c7a6070961fb.

## Diff of the candidate against HEAD (a351afd2b16 catalog)

- built_at_git_head moves (a new HEAD).
- silver_datasets 201 -> 204: `dynamodb_dynamodb_etf_classifications`, `opal_data_harvest_root_amgt`, `published_analysis_scoped_api` (ef168640331). portal 5 and harvest 78 unchanged.
- tool_index: 127 tools both sides, 103 entries change. Members: b->a 52, b->c 42, a->c 1 (schwab_describe_dataset). Explained by members.yaml
  commits b3814dc2b31 (round 23 dispositions, never emitted) and ef168640331 (W3 links, 31 pending tools to a).
- NOT explained by ef168640331: (1) the round-23 commit b3814dc2b31 above; (2) 43 `definition` line refs move (e.g. client_get_allocation
  app/tools.py:1597 -> 1602) because the manifest's deployed_commit moved 4be300110e -> 13917ef993 (the emitter reads the tree at that commit).
- Serves (the map): client_get_allocation + orion/inflection, schwab/49financial; client_get_fees + blackdiamond/cottonwood, orion/inflection;
  client_resolve_account + blackdiamond/cottonwood, orion/inflection, - schwab/49financial. The other 4 tools carrying serves are unchanged.

## After (candidate catalog, prospective census)
ROUTING tools=127 pairs=209 routed_pairs=192 misrouted_tools=10 link=7 code=3 display=0 untraced=0; SERVES tools=127 changed=66.
COVERAGE channels=14 tools=127 rows=277 refusals=7 explained=94 (the 5 client_* tools, opal_describe, opal_discover).
Tests: workflows/atom_decomposition/tests + workflows/gateway_battery/tests: 511 passed.
To place: `round18/place_catalog.py` on the candidate, after the issuer accepts items (1) and (2).
