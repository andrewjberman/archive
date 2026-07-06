# VERIFY #21 -- target: INF_B_00.canonical_holdings.py

- is_real: **True**
- confidence: **confirmed**
- corrected_severity: high

## Reasoning
CONFIRMED real defect; traced a concrete triggering path and reproduced every step empirically on pandas 2.3.3.

DTYPE CHAIN (all cited lines verified in code):
- household_id is a canonical silver ID column coerced to nullable Int64 (data/inf/scripts/silver/_orion_api_silver_lib.py:243-269, coerce_silver_ids). .set_index/.to_dict on it (INF_D_05 lines 238-241) yields Python-int dict values.
- INF_D_05 line 248 `holdings['household_id'] = holdings['account_id'].map(hh_map_str)` maps str->int; the instant ANY holdings account_id is absent from the dim, pandas injects NaN and upcasts the whole column to float64. Line 249 `.notna()` filters rows but does NOT restore dtype -> mapped['household_id'] stays float64. No int re-coercion exists before use.
- Line 261 `.unique()` -> numpy.float64 (9001.0). Line 328 f-string -> key `platinum/clients/9001.0/top_holdings.json`. Line 323 `int(hh_id) if str(hh_id).isdigit() else hh_id`: '9001.0'.isdigit() is False, so int-coercion is skipped and numpy.float64 (a float subclass) is json.dumps'd as `9001.0`. Empirically confirmed: partial coverage->float64 dot-zero keys+body; 100% coverage->int64 clean keys (the silent broken<->clean flip).

TRIGGER REACHABLE (refutation attempts failed):
- Producer INF_B_00.canonical_holdings.py builds gold/canonical/holdings from silver/api_dims/positions_mv (accounts holding positions) joined only with accounts_v2 — never against silver/api_dims/household. So holdings' account universe is NOT a subset-guaranteed match to the household dim; one account with a position but no household row (new account / two-independent-silver-chain timing skew) upcasts the entire column, poisoning ALL clients at once.
- Not guarded: line 250 `if mapped.empty` only catches the ALL-unmapped case, not partial.
- Sibling protection verified: INF_D_06.client_timeseries.py:365 does `hd['household_id'].astype(str)` before its map (keys stay clean clients/9001/); INF_D_05 astype(str)'s account_id only (line 245), never household_id. On a broken run INF_D_05 emits clients/9001.0/top_holdings.json while siblings emit clients/9001/..., so the portal (integer id) 404s Top Holdings while the chain exits 0 logging 'uploaded'.

SEVERITY: corrected to high (flag said critical; critical is defensible). Near-certainly fires on daily full runs, silent (rc=0 false success), breaks the served Top Holdings panel for every client via portal 404. Held just below critical because blast radius is one panel (detail/composition/timeseries/cash_drag use other scripts that handle household_id correctly), the underlying MV data is correct (key-path/serialization defect, not financial-number corruption), it is fully recoverable, and self-heals on any 100%-coverage run. Fix: coerce after the map, e.g. mapped['household_id'] = mapped['household_id'].astype('Int64') (or .astype(str) to match INF_D_06) after line 249.
