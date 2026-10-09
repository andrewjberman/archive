# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 42, CB-ap-2: deploy the cot price writer and its registry file

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-09 ~14:4xZ**
**Act:** `0.7.0_AE_CloudOps~CB2` writes TWO keys in `opal-data-cot` `code/gold/` (CTO ADDENDUM 14 @9a98e3b0a1):
- the writer, through `.tools/safe-deploy.sh`;
- the registry file, by one `put-object` of the exact blob bytes.

## 1. Blast radius -- exactly two keys

| key | prior | new bytes | new sha256 |
|---|---|---|---|
| `code/gold/build_canonical_prices_v2.py` | VersionId `4M4XPMtc2JCbbWi22WuxrVIaicQqPzy6` (2026-06-12T20:07:45Z, 28,290 B) | repo HEAD file (CB-an-1 + CB-ap-1, drained @ba35c04d1c and @7ae9de1d21) | `3ac0a502798b53827cb7b63d8a0f876648a2950611434cb5991cf109f97f6682` |
| `code/gold/scopes.json` | **none: MINTS** (`head-object` 404 at ~14:4xZ) | git blob `261c0cf8adf46ade84fefd1144092c5665df7477` of `infra/logic/registry/scopes.json` | `13947f7f2b35c6c9ed403e6c21ba87d1abd00156c06a50dcd37cdd69dedeaade` |

- The applier re-reads each key before its write: the writer's VersionId must be unchanged, and `scopes.json` must still be 404.
- The deploy tool's printed key list holds exactly these two keys, or the act STOPS.
- If the repo file at HEAD differs from the sha256 above when the applier runs, the act STOPS. A later commit to the writer is not
  covered.

## 2. Rollback

- **Writer:** `copy-object` from `?versionId=4M4XPMtc2JCbbWi22WuxrVIaicQqPzy6`.
- **`scopes.json`:** delete the key this act minted (it had no prior version). That deletes only what this act created.
- The bucket is versioned, so the writer's prior is kept.

## 3. Writers and readers of the named property

- **Writers of `code/gold/`:** `safe-deploy.sh` and this act's one `put-object`. There is no scheduled writer.
- **Readers:** the cot gold run's code sync (`gold_dispatch.sh`:497-498). The writer runs only on a MANUAL silver-prep (CB-aj-1 census:
  0 scheduled writers), so **no scheduled output changes from this deploy.**
- **The registry copy becomes a second place the scopes live.** It is pinned to blob `261c0cf8...`.
  - When the repo's `scopes.json` changes, the deployed copy is stale until re-deployed.
  - The writer's `source_firm` resolution then reads the pinned scopes, which is safe: a scope missing from the pin reads `absent`,
    never the own firm.
  - The re-deploy on a registry change is a carried item for the CTO to place, not a rider here.

## 4. Proof and closure

- `pytest data/cot/scripts/gold/tests/test_canonical_prices_source_firm.py`: 8 passed on the issuer's run at ~14:4xZ (39 across the
  gold suite). The applier re-runs it after the read-back of both sha256 values.
- **D2-S62 closes** when the next manual silver-prep's census (`commonwealth_cot_price_rewrite.py --source-firm-only`) reads
  `source_firm=cottonwood` on every row with `BREACH=0` (ADDENDUM 14). That is the issuer's watch item, under the silver-prep's own
  pair.
