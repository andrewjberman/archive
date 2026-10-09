# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 34, CB-ah-3: as-traded re-mint of the three FWD-3 tables

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: DRAFT, NOT GIVEN.** Section 3 is filled from CB-ah-2's build and signed then.
**Act:** `0.7.0_AE_CloudOps~CB2` overwrites three served keys with the tables built at `price_basis=as_traded` (CTO ADDENDUM 8 ruling;
ADDENDUM 9 @cf58046f35 cuts the rebuild).

## 1. Blast radius -- exactly three keys, overwritten; nothing else

The bucket is `opal-data-assets`. Versioning was read `Enabled` at ~11:1xZ (`get-bucket-versioning`). The prior versions below were read
by `head-object` at ~11:1xZ.

| table | key | prior ETag | prior VersionId | prior size | prior LastModified |
|---|---|---|---|---|---|
| daily_returns | `commonwealth/cottonwood/silver/daily_returns/date=2026-06-23/part-00000.parquet` | `c024c607273cfc65a2cce816b3965b43` | `rIUTpGUAPNG.rsDWrxpRbnJCmu6NFaXJ` | 1,646,994 | 2026-10-09T08:09:26Z |
| account_day_value | `commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/part-00000.parquet` | `365b2e8ef9092f6fee0335778fb4fbcb-7` | `PcSspTWz8xsreGMTF_coYhbqifk4preA` | 58,027,322 | 2026-10-09T08:09:27Z |
| month_grades | `commonwealth/cottonwood/silver/month_grades/date=2026-06-23/part-00000.parquet` | `88c025b57840efa8f92694b35cdbf481` | `Y15sJCiA1KM.CksHSitFlsnqkI56N_34` | 428,972 | 2026-10-09T08:09:28Z |

The applier re-reads these versions immediately before the write. If any one differs, it stops: something else moved the key.

**Writers of the named property:** 1. The only writer of these three keys is `commonwealth_fwd3_serve.py --apply` (the round-29 mint
@476f970245 and this act). No scheduled producer writes them.

**Readers:** 0. The CTO's reader gate (ADDENDUM 9) grants none until this rebuild is graded.

## 2. Rollback per key

For each key, copy the prior VersionId above back as the current version:
`s3api copy-object --copy-source opal-data-assets/<key>?versionId=<prior VersionId>`. Then `--verify` against the round-29 build
(`.scratch/advi_cotbkf/fwd3_serve`) reads `match=True`. No key is deleted.

## 3. The build to apply (filled from CB-ah-2; empty = not given)

- build commit / run_commit: `<from CB-ah-2>`
- `--hold-cusips`: **`05613L3H2,95000U2D4,651639AX4`.**
  - Basis: CB-ah-1 classes the writer `cross_firm` (drained @248cb44fa0; issuer re-run matches), and CTO ADDENDUM 9 holds the served
    `bd_txn_price` objects from the rebuild until they are re-sourced.
  - Issuer read of the repo: the store's prices for these CUSIPs (1.0188 / 0.9804 / 0.9037) are the constants in 49 Financial's
    `data/black_diamond/scripts/silver/scoped_price_exceptions.json`. `data/cot/scripts/gold/build_canonical_prices_v2.py:22-24` states
    that cot does not run that inject.
  - Their holding-days build BLANK, with reason `HELD_SOURCE_UNDER_REVIEW`.
- price input `.scratch/advi_cotbkf/r34_price_input.parquet` sha256: `<from CB-ah-2>`
- per table, rows and content hash from `--dry-run`: `<from CB-ah-2>`
- ABSENT list (reason `REGRESSED_UNDER_<rule>`): `<from CB-ah-2>`
- **Both branches covered:** the round-28 four months come back graded, or stay ABSENT under the new reason. Either is admitted, and the
  dry run prints which.

## 4. Conditions

- CB-ah-1 drained, with its class read by the issuer. CB-ah-2 drained VALID. The issuer's real run of CB-ah-2's AC1 and AC2 matches the
  worker's.
- The CTO half signed against the same section-1 versions and section-3 hashes.
