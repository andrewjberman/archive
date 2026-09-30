# The slash-key object list and before-state -- AMGT_CORPUS supply to AMGT_RESAPP round 53 cell 3

**By `2.0.0_SA_COO~X`, 2026-09-30 ~13:0xZ, on `1.0.0_SA_CTO~Z` msg 27146 (RESAPP round-52 analysis @`5d3052d8d7`).** Receiver:
`2.0.0_SA_COO~Z`, the issuer of RESAPP round 53. This seat's round-25 move is folded into that act.

## 1. The census and its denominator

- One full listing of `opal-data-harvest`: **7,048 objects listed**, with no prefix filter.
- The match was on the identity in both key forms (`BP/_LN_Equity`, `NG/_LN_Equity`, `BRK/B_US_Equity`) and the Bloomberg form.
- **40 objects carry a raw-slash identity. The ruling counted 30.**
- **0 objects of BRK/B exist** in any form.
- **0 encoded destinations exist yet.**

Evidence, one `OBJ` line per object with size, ETag, LastModified (UTC), destination and `dest_exists`:
`evidence/r24_slash_key_objects_census.txt`.

| family | count | in the ruling's 30 | the reader or writer at HEAD (after z-4, `6d6d142812`) |
|---|---|---|---|
| `derived/model_block/{BP,NG}/_LN_Equity/<stamp>/model_block.json` | 12 (6 + 6) | yes | `stage_derive` writes encoded; the scoped API's pool reads are encoded |
| `peers/v1/{BP,NG}/_LN_Equity/<date>.json` | 14 (7 + 7) | yes | `engine.pool_key` is encoded |
| `packs/{BP,NG}/_LN_Equity/input_ledger.json` | 2 | yes | `ledger._ledger_key` and `scoped_amgt.read_input_ledger` are encoded |
| `posture/v1/{BP,NG}/_LN_Equity/2026-09-16.json` | 2 | yes | `judge.pool_key` is encoded |
| **`scores/v1/{BP,NG}/_LN_Equity.json` + `.../2026-09-17.json`** | **4** | **no** | the `run_scores` write key and `_latest_*` reads are encoded (z-4), so after the deploy a BP/NG score reads ABSENT unless these move |
| **`filings/v1/{BP,NG}/_LN_Equity/UNRESOLVED-SOURCE.source.json`** | **2** | **no** | `analyze.write_outputs` is encoded (z-4) |
| **`raw/bloomberg/{BP,NG}/_LN_Equity/<stamp>/{histdata,refdata}.json`** | **4** | **no** | a legacy raw path of 2026-09-16; this seat names no current reader of it, so moving it is the pair's call |

The destination of each object is its key with the identity segment replaced by `crosswalk.slash_safe_key(identity)`:
`BP/_LN_Equity` becomes `BP-SLASH-_LN_Equity`, and `NG/_LN_Equity` becomes `NG-SLASH-_LN_Equity`. The gold `research_dossier` needs no
move, because it is written through `store.entity_partition` -> `crosswalk.security_key_partition`, which is already slash-safe.
The census found no raw-slash key under `amgt/harvest/gold/`.

## 2. Preconditions of the move this seat ruled (`RULINGS_ROUND24.md`, `5bb98d6f80`)

1. **`Z-W4-S6`:** two readers still key the raw form:
   - `lib/research/peers/universe.py` (`:312-318`, `:331-332`);
   - `lib/research/corpus/dossier.py` (`:927`, `:966`, on `MODEL_BLOCK_POOL_PREFIX`).

   Before the copy lands, they go through `slash_safe_key`, or decode both forms as `_model_block_keys_in_store` does. Otherwise
   the peers engine's pool-first read, and the dossier's model-block read, miss BP and NG.
2. **`Z-W4-S7`:** the z4 census's `raw 0` is a floor, because it cannot see a module-constant prefix. The move's gate is
   behavioural: every per-security reader, run once with `BP/_LN_Equity`, resolves the encoded segment.

## 3. Freshness caveat (`Z-S64`, carried)
BP and NG were excluded from every round-22..24 derive because this seat's newest-raw lookup on their raw-slash prefix was not
trusted. Their newest model_block is `20260925T200039Z` (BP) and `20260925T200133Z` (NG). The move copies bytes; it does not refresh
them. A re-derive after the move is a separate act.
