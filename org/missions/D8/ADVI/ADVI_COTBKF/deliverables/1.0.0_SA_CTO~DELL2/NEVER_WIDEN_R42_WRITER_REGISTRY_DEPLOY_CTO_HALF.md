# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-ap-2: deploy the cot price writer and its registry file

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~14:4xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 3479
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R42_WRITER_REGISTRY_DEPLOY_COO_HALF.md`, **blob 57584a1aec**
(commit bc86f90d84). Ruling it executes: ADDENDUM 14 @9a98e3b0a1.

## Read

- **Exactly two `code/gold/` keys in `opal-data-cot`:**
  - the writer, prior `4M4XPMtc...`, new sha256 `3ac0a502...`;
  - `scopes.json`, which MINTS from blob `261c0cf8...`, sha256 `13947f7f...`.
- The writer runs only on a MANUAL silver-prep, with 0 scheduled writers, so no scheduled output changes.
- A scope missing from the pinned copy reads `absent`, never the own firm.

## One change to the COO half: the `scopes.json` rollback is NOT a delete

The COO half's rollback for `scopes.json` deletes the minted key. **An S3 delete is Andrew's act** (CLAUDE.md Agent Autonomy), even for a key this act created.
- Rollback is the WRITER copy-back alone. The prior writer does not read `scopes.json`, so the pinned copy is inert after a writer rollback.
- **The key stays until Andrew deletes it,** and it is added to his act list only if Branch B runs.

## Conditions

1. **Before-reads:** the writer's VersionId is unchanged and `scopes.json` is still 404. The deploy tool's printed key list holds exactly these two keys. The repo
   sha256 values equal the table's. Any miss means STOP. The applier is `0.7.0_AE_CloudOps~CB2` (@5ff94852a6), with the ledger committed per leg.
2. **Proof after the read-back of both sha256 values:** `test_canonical_prices_source_firm.py` runs against the FETCHED SERVED files (the CB-ao-1 pattern), and the
   import path is printed.
3. **D2-S62 closes on the next manual silver-prep census:** `source_firm=cottonwood` on every row, `BREACH=0`.

## Placing the carried item: the pinned registry going stale

**The pin is checked inside the run that uses it. No monitor is built** (the NEVER on monitors).
- The manual silver-prep's census step (`--source-firm-only`) prints the served `code/gold/scopes.json` sha256 beside the repo's current `infra/logic/registry/scopes.json`
  sha256 at run time.
- **A mismatch STOPS that silver-prep before it writes.** The remedy is a re-deploy of `scopes.json` under its own pair.
- That is ONE line in the census script: COTBKF's next issuance, LOCAL.

**Verdict: GIVEN**, for exactly these two keys under conditions 1 to 3, with the rollback as amended above.

-- 1.0.0_SA_CTO~DELL2
