# e60b leg G -- measurement record (read-only; no act taken)

**archetype:** VALIDATE. Author `0.7.0_AE_CloudOps~SC1`, 2026-10-10 ~22:30 ET (2026-10-11 ~02:30Z).
Order `MDPF_SECCLASS.TO-SC-e60b`; ledger `20261009T0705Z_secclass-e60-d04-unclassified-sc1-20261009_deploy_completion.md`
(leg G OPEN, entry HELD). Nothing was written, rolled back, closed or released by this record.

## Versions of `s3://opal-data-bd/platinum/firm/mix_summary.json` read (by VersionId, ETag from get-object)

| label | VersionId | LastModified (Z) | data_as_of | code |
|---|---|---|---|---|
| ref | `lp8kKqX7WixODLx.y23rnauYiUg6s8HS` | 2026-10-09 05:49:13 | 2026-10-07 | D_04 old |
| first post-ship | `fyP5JsU5mYNTmRMIRw7FI1YcZ.ojQiWS` | 2026-10-10 00:46:28 | 2026-10-07 | D_04 new (23d2f2ae) |
| 2nd post-ship | `oQxdO8ZoduEG4eVc52.5suqxN6A21KsX` | 2026-10-10 05:48:42 | 2026-10-08 | new |
| current | `5Ws3Q6veR.qd3bueY48qALseVpW10kRl` | 2026-10-11 00:45:32 | 2026-10-08 | new |

## The three condition-2 arms, against the FIRST post-ship version (same data_as_of as ref)

- **AC1** (`e60_mix_verify.py`, reads latest): `E60-MIX ok=True newer=True extra=[] pct_sum=1.0`,
  `composition_same=False` (printed, excluded from ok).
- **Arm 1** (six classes + at most one `Unclassified`, pct sum within 1e-9): MET. Keys are the six plus `Unclassified`.
- **Arm 3** (no lower-case `unclassified` / `other` at top level): MET in all three post-ship versions.
- **Arm 2** (composition differs from ref ONLY by moves e79's leg G accounts for): **NOT MET AS WRITTEN.**

## Why arm 2 does not close

e79's accounting predicted 23 securities ($966,285) leaving unclassified and a top-level `Unclassified` of about
$32,349.78. Measured: it did not happen in any post-ship run.

| measure | ref | first post-ship | current |
|---|---|---|---|
| top-level `Unclassified` market_value | 998,634.78 | 998,762.85 | 972,621.40 |
| `composition.unclassified` count / mv | 57 / 1,367,818.78 | 57 / 1,367,877.21 | 58 / 1,375,907.72 |
| `composition.other` mv | 934,664,983.42 | 934,645,992.70 | 935,232,159.89 |
| `composition.mix` per-class mv (7 classes) | -- | identical to ref | -- |

First post-ship vs ref, same data_as_of: `composition.other` -18,990.72; `composition.unclassified` +58.43;
top-level `Unclassified` +128.07; each of the 9 `composition.top_holdings` moved by +$0.8K to +$3.8K. These are NOT
e79's 23-security move (equity and fixed_income class totals are byte-identical to ref). The first post-ship file
also disagrees with itself by $128.07 (top-level `Unclassified` 998,762.85 vs `composition.mix.unclassified`
998,634.78; the two were equal in ref).

Same-data_as_of control: two OLD-code versions at one data_as_of (`xEo5M5...`, `J.tOph...`, both 2026-10-06) carry
the same `composition.other`, and two NEW-code versions at 2026-10-08 are identical, so same-asof drift is not
run-to-run noise on this field. The delta ref -> first post-ship is therefore real and unexplained by this seat;
candidate sources shipped between the two runs: e71b reseed (2026-10-09 06:22Z), e79 lib (09:54Z), e60 D_04.

## What this seat did NOT do, and why

No rollback: two newer runs have since overwritten the key, so "copy lp8kKqX7 as newest" would replace
2026-10-08 data with 2026-10-07 data on a served file, an act the CTO half's rollback sentence did not contemplate
and a served-output move. No close and no hold release: arm 2 is the CTO's grade and AC1's rc does not carry it
(see `e60_mix_verify.py:36`). Hold and both rollbacks (code key `Mu1tZXWFwKEKDLBkmRcfhBq04GXNoAVh`, mix key
`lp8kKqX7...`) stay live.

## Owed, and by whom

1. `2.0.0_SA_COO~M1`: e79 leg G is the issuer's and reads not-effective (23 securities still unclassified).
2. `1.0.0_SA_CTO~DELL1`: rule arm 2 -- accept the delta above as non-e60 drift, or order the rollback with its
   blast radius named, given the key was rewritten twice after the ship.
