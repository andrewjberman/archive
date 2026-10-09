# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-ax-2: cot gold redeploy (writer + B_00 + two beside-files)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~17:2xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 3779
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R50_COT_GOLD_REDEPLOY_COO_HALF.md`, **blob 2186cd1adc**
(@ea3b5ad9f8). Rulings executed: ADDENDA 18, 19, 21, 22, 22.1 and 23.

## Read

- **4 keys in `opal-data-cot/code/gold/`:**
  - 2 beside-files MINT FIRST (`ticker_overrides.py`, `legacy_addresses.json`) by exact-blob `put-object`;
  - then the writer and B_00 by `safe-deploy`.
  - `scopes.json` is unwritten; its deployed version is `7ChC4J0G`.
- **The diff census is limited to the named changes:**
  - writer: input resolution, `source_firm`, keys from the pinned registry, fail-closed overrides;
  - B_00: firm from `scopes.json`, no runtime `opal_naming`.
- **Import closure is `missing=0`** against the 16-key `lib/` listing.
- **Rollback:** the scripts are copied back from their prior VersionIds. The minted files are never deleted by a seat (Andrew's act), and they are inert to the
  prior scripts.

## Conditions

1. **The write set is the UNION of every tool's printed key list (ADDENDUM 18 wording),** and it equals exactly these 4 keys. The minted keys still read 404 and the
   prior VersionIds are unchanged immediately before each write; a miss means STOP.
   - Order: 1 and 2 before 3 and 4.
   - The applier is `0.7.0_AE_CloudOps~CB2`, with the ledger opened BEFORE the first write.
2. **Proof on the FETCHED SERVED files,** in a scratch worktree with no `lib/opal_naming`:
   - each of the 4 sha256 values read back;
   - the fail-closed tests: scopes-absent, overrides-absent and legacy-absent each STOP with 0 rows;
   - a synthetic rps day runs with no ImportError;
   - the written-key census equals the pre-change writer's, with no new key class under FIRMBKTS's `historical_prices`;
   - the import-closure read prints `missing=0`.
3. **No scheduled output moves.** The writer runs on a manual silver-prep, and B_00's `_ff_worker` path is unreached (rps empty). The first manual silver-prep after
   this is D2-S62's closing census (`source_firm=cottonwood`, `BREACH=0`, resolved paths printed).
4. **An infeasible condition as worded means STOP and ask** (ADDENDUM 18).

**Verdict: GIVEN** for exactly these 4 keys under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
