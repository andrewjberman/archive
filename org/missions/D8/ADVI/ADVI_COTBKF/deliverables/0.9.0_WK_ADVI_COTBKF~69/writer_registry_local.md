# CB-ap-1 writer registry local (0.9.0_WK_ADVI_COTBKF~69)

Registry file chosen: scopes.json
Repo path: infra/logic/registry/scopes.json (read only; the deploy cell CB-ap-2 ships it as a code/gold/ key beside the writer)
Blob id (git hash-object): 261c0cf8adf46ade84fefd1144092c5665df7477
sha256: 13947f7f2b35c6c9ed403e6c21ba87d1abd00156c06a50dcd37cdd69dedeaade

Why this file: the writer's resolution reads only per-scope key, class, bucket, aliases (spelling + planes) and pipeline_trees (dir + vendor).
All of these are in scopes.json (4 FIRM scopes of 14). NAMING_SCHEMA.json is not read; lookup() is not called. One file carries it; no BLOCKING row.

Writer: reads Path(__file__).parent / scopes.json only, slims to those fields; missing or unreadable -> WARN printed, every input `absent`.
No lib/ or infra/logic/registry path in the writer.

Removed: Step 5b share-class denomination check (32 lines, `canonical['source'] == 't1_transaction_observed'` filter). Unreachable: the writer
emits sources transaction_observed / linear_interpolation / yahoo_finance; the label t1_transaction_observed appears nowhere under data/cot/scripts/gold (Grep: no matches).
Suite before (base): data/cot/scripts/gold/tests 36 passed. After: 39 passed (36 + new f, g, h); no test reached the removed block.

Commits: f30ad987a6 (new assertions alone; g and h fail at base: 2 failed, 6 passed), 97d2788953 (change).

WRITER-REGISTRY file=scopes.json blob=261c0cf8adf46ade84fefd1144092c5665df7477 tests=8
