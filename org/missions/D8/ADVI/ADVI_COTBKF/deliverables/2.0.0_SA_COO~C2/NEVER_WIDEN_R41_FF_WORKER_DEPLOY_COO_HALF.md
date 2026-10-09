# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 41, CB-ao-1: deploy the cot gold `_ff_worker` carry-forward stamp

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-09 ~14:1xZ**
**Act:** `0.7.0_AE_CloudOps~CB2` writes ONE new version of `s3://opal-data-cot/code/gold/B_00.canonical_holdings.py` through
`.tools/safe-deploy.sh` (CTO ADDENDUM 13 @9326a48990).

## 1. Blast radius -- one key, one new version; nothing deleted

| key | prior VersionId | prior sha256 | new sha256 |
|---|---|---|---|
| `code/gold/B_00.canonical_holdings.py` | `BMqu7SNCbx2f3bQ_Tr56xMBCvtMe3van` (2026-10-02T17:43:29Z, 65,249 B) | `6dbf6a86e734f514c92421e8e6ca9a9168bd8b6b90f742857f0f86d83c0d69a8` | `45fbbd921f026f9d4e30785e632c8f8e0feeb02730f033b96fd03b23da74c08d` |

**Census -- only the carry-forward members move.** The prior served bytes equal the repo file before round 39
(`git show 88e7452955^1:data/cot/scripts/gold/B_00.canonical_holdings.py`; issuer `diff -q` at ~14:1xZ: identical). The new bytes are
the repo file at HEAD. The deploy therefore moves exactly round 39's diff, +25/-1 lines, all inside `_ff_worker` (drained
@88e7452955). The applier re-prints that diff before the write and stops on any line outside `_ff_worker`.

## 2. Rollback

`s3api copy-object --copy-source opal-data-cot/code/gold/B_00.canonical_holdings.py?versionId=BMqu7SNCbx2f3bQ_Tr56xMBCvtMe3van`. The
bucket is versioned (read `Enabled` ~12:3xZ), so the prior is kept.

## 3. Writers and readers of the named property

- **Writers:** `.tools/safe-deploy.sh` (the DS deploy path). There is no scheduled writer of `code/gold/`.
- **Readers:** the cot gold run's code sync (`gold_dispatch.sh`:497-498). `_ff_worker` is reached only when `schwab/silver/rps/`
  holds data, and that prefix is empty today (CTO-measured against a positive control).
  - So **no scheduled gold output changes from this deploy today.**
  - When the prefix fills, carried prices carry `price_basis` / `price_source_date` / `source_firm`, and a foreign-firm price is not
    carried (NaN, never zero).
  - Both branches are covered: the path is unreached (output unchanged), or the path is reached (stamped output, the intended
    change).

## 4. Proof

The served object's sha256 is read back equal to `45fbbd92...d74c08d`, then
`pytest data/cot/scripts/gold/tests/test_b00_ff_carry_claim.py` (3 passed) drives the carry-forward on a synthetic day against those
bytes and reads the stamp. The live path is unreachable, so the proof is synthetic by design (ADDENDUM 13).
