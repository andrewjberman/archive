# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-ao-1: deploy the cot gold `_ff_worker` carry-forward stamp

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~14:1xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 3426
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R41_FF_WORKER_DEPLOY_COO_HALF.md`, **blob a864375d1e**
(commit 3089cde892). Ruling it executes: ADDENDUM 13 item 2 @9326a48990.

## Read

- **ONE key gets one new version:** `s3://opal-data-cot/code/gold/B_00.canonical_holdings.py`.
  - prior `BMqu7SNC...`, sha256 `6dbf6a86...`;
  - new `45fbbd92...`.
- **The prior served bytes equal the repo file before round 39,** so the deploy moves exactly round 39's +25/-1 inside `_ff_worker` (@88e7452955).
- **The path is unreachable for cot today** (`schwab/silver/rps/` empty, measured against a positive control). No scheduled gold output changes.
  - When it is reached, carried prices are stamped (`price_basis`, `price_source_date`, `source_firm`), and a foreign-firm price is not carried.
  - Both branches are covered.
- Rollback is a copy of the prior VersionId. Nothing is deleted.

## Conditions

1. **The applier re-reads the prior VersionId and sha256 immediately before the write,** and any change means STOP. It re-prints the diff, and any line outside
   `_ff_worker` means STOP.
2. **`safe-deploy.sh` is run so that it writes this ONE key and no other.** The applier prints the invocation's planned key list before the write, and any second
   key means STOP. The ledger is pinned and committed per leg; the applier is `0.7.0_AE_CloudOps~CB2` (@5ff94852a6).
3. **The proof runs against the SERVED bytes:** the object is fetched back, its sha256 must equal `45fbbd92...`, and `test_b00_ff_carry_claim.py` imports THAT file,
   not the repo copy. The ledger prints the import path.
4. **The next scheduled cot gold run is read for an unchanged output fingerprint** on one date, which confirms the path stayed unreached. Any change is a row.

**Verdict: GIVEN**, for this one key under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
