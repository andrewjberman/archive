# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 34, CB-ah-3: as-traded re-mint of the three FWD-3 tables

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN** (~12:2xZ @64b302f3a8; reinstated ~12:3xZ).

> Briefly marked superseded on CTO ADDENDUM 10 (the rebuild sequenced after the 38-key rewrite). The CTO then ruled, in msg 3271
> (CTO half GIVEN, `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R34_FWD3_ASTRADED_REMINT_CTO_HALF.md`), that the HELD bonds make this
> re-mint independent of the rewrite. The three bonds' holding-days are blank in this build, so no 49F row reaches a served value.
> The half stands as given, on the section-3 build, with the CTO's conditions:
> - re-read the 3 prior versions at write and STOP on change;
> - apply as built, with hashes printed;
> - the reader gate stays closed until the CVO grades;
> - a named row for each of the 5 ABSENT months;
> - a pinned ledger.
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

- **The build to apply is the ISSUER'S local build, applied as built and not rebuilt.**
  - Location: `.scratch/advi_cotbkf/fwd3_serve_r34_hold/` (`fwd3_manifest.json` beside the three tables).
  - Command: `commonwealth_fwd3_serve.py --build --data-dir .scratch/advi_cotbkf/r34 --out .scratch/advi_cotbkf/fwd3_serve_r34_hold
    --hold-cusips 05613L3H2,95000U2D4,651639AX4`.
  - It was built at `run_commit=6f70d5cc01bb2e196266799a657be6d0b2dc8a16` from the drained CB-ah-2 code (@6df94d0218).
  - The run_commit is part of the table content, so a rebuild at a later HEAD would move the hashes. The applier runs `--dry-run`
    and `--apply` against THIS `--out`, and never `--build`.
- Price input: `.scratch/advi_cotbkf/r34_price_input.parquet` sha256
  `c55d686e29d90df53a05fe79847cdc9b36032029dc77ee02152e89baf359e5e9` (CB-ah-2).
- `--hold-cusips`: **`05613L3H2,95000U2D4,651639AX4`.**
  - Basis: CB-ah-1 classes the writer `cross_firm` (drained @248cb44fa0; issuer re-run matches), and CTO ADDENDUM 9 holds the served
    `bd_txn_price` objects from the rebuild until they are re-sourced.
  - Issuer read of the repo: the store's prices for these CUSIPs (1.0188 / 0.9804 / 0.9037) are the constants in 49 Financial's
    `data/black_diamond/scripts/silver/scoped_price_exceptions.json`. `data/cot/scripts/gold/build_canonical_prices_v2.py:22-24` states
    that cot does not run that inject.
  - Their holding-days build BLANK, with reason `HELD_SOURCE_UNDER_REVIEW`.
- Per table, from the issuer's `--dry-run` (~12:1xZ; `manifest_hash_same=True` on all three):

| table | rows (before -> after) | content hash (after) |
|---|---|---|
| daily_returns | 1,691,729 -> 1,691,729 | `fa1c1303fd969ec59de423f63d5d84d2d9b7b0d2a5d1514f206ff1df02a8dede` |
| account_day_value | 21,102,041 -> 21,102,041 | `a94d3acce066e98d8d3fdad69c8e16f19d874df9192010ddf844b3c43103b6e8` |
| month_grades | 82,593 -> 82,593 | `66ea11a4434ae63d47246f980b216df2759edc4766427b31d8a2bfcc7a1d4ec0` |

- Held: 988 holding-rows / 988 account-days (the three bonds), reason `HELD_SOURCE_UNDER_REVIEW`.
- ABSENT list (5, reason `REGRESSED_UNDER_AS_TRADED`, `manifest_list_same=True`): 0QF878956 2022-03, 0QF878956 2022-08,
  B3S793726 2026-03, D49151054 2021-07, D49151054 2021-10.
- **Grades (issuer re-grade, matching CB-ah-2):**
  - MATCH/DIFF/UNGRADABLE goes 3,133/838/78,622 -> 3,678/293/78,622, with `regressions=5`, `movers_back=155` and `year_chain_same=True`.
  - The round-28 four ABSENT months come back MATCH.
  - SCHB / SCHZ on 2022-10-12 equal the round-31 evidence (41.94 / 44.93).
- **Both branches covered:** the round-28 four months come back graded (MEASURED: they do). The 5 new regressions read ABSENT under
  the new reason. Either outcome was admitted before the read.

## 4. Conditions

- CB-ah-1 drained, with its class read by the issuer. CB-ah-2 drained VALID. The issuer's real run of CB-ah-2's AC1 and AC2 matches the
  worker's.
- The CTO half signed against the same section-1 versions and section-3 hashes.
