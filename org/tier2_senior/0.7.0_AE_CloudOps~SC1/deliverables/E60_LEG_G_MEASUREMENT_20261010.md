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

## AMENDMENT 1 -- AC2 run (2026-10-11 ~02:50Z), per CTO ruling `CTO_RULING_SECCLASS_E60B_LEG_G_ARM2_20261011.md` item 2

Order amended by `2.0.0_SA_COO~M1` (msg 3364, commit `5d3a5ccdf3` on branch `coo-m1-r19-e60ab`). Run from that
worktree root (`C:/dev/coo_m1_r19ab`, HEAD `5d3a5ccdf3`), once, rc=0. Script read before running: its only S3
write path (`_write_batch`) is replaced by an in-memory sink and `upload=False`; no key written, scratch or served.
Never production evidence. Output below; the INPUTS, DIFF, OLD/NEW and verdict lines are verbatim. The script's
per-module banner (the `=== Step 2 ===` header and the `Concentration: 9 top holdings`, `Mix periods: 5 quarterly
bars`, `Composition overridden with C_06 values: 7 classes` lines, printed once per code) is omitted, and its two
`Mix snapshot (C_06)` lines are shown prefixed by which code printed them:

```
INPUTS (read once, shared by both codes):
  s3://opal-data-bd/gold/views/mix_daily_summary.json  VersionId=6o1FOSbTRgA9hRzl7I5WyHcN3EyFH.RJ
  s3://opal-data-bd/gold/artifacts/firm_mix_views.json  VersionId=Sx4WcnNvPibbLL3HEyTmlSjfsKnjmLP.
  s3://opal-data-bd/gold/views/firm_composition.json  VersionId=n8RTGOFTMcy3jWGn4nQLzCx7dnQL56vk
  (old code) Mix snapshot (C_06): 8 classes, date=2026-10-08, total_mv=$2,014,814,865
  (new code) Mix snapshot (C_06): 8 classes published, 7 served, date=2026-10-08, total_mv=$2,014,814,865
DIFF: 903 leaf fields compared (union of both summaries); 6 differ; 0 outside top-level mix
  mix.Unclassified.market_value: old='<absent>' new=972621.3980307579
  mix.Unclassified.pct: old='<absent>' new=0.0004827348729204387
  mix.other.market_value: old=0.0 new='<absent>'
  mix.other.pct: old=0.0 new='<absent>'
  mix.unclassified.market_value: old=972749.9717244315 new='<absent>'
  mix.unclassified.pct: old=0.00048279868706826854 new='<absent>'
OLD top-level: unclassified=972,749.97 other=0.00  composition.mix.unclassified=972749.97
NEW top-level: Unclassified=972,621.40  composition.mix.unclassified=972749.97
E60-AB ok=True leaves=903 differing=6 outside_mix=0 old_mix_keys=['alternatives', 'cash', 'commodities', 'equity', 'fixed_income', 'other', 'structured', 'unclassified'] new_mix_keys=['Unclassified', 'alternatives', 'cash', 'commodities', 'equity', 'fixed_income', 'structured'] old_uncov=972,749.97 new_Unclassified=972,621.40
```

(Only the two "Mix snapshot" lines are condensed from the script's repeated per-module step banners.)

### Reading against the ruling's decision rule

- **AC2 reads `E60-AB ok=True`; it matches the issuer's base dry run** (leaves=903, differing=6, outside_mix=0).
- **Composition delta (the thing arm 2 asks about): appears under BOTH codes, i.e. not e60's.** On one input set the
  two D_04 versions produce byte-identical `composition`, `concentration`, `mix_periods` and `data_as_of`
  (0 of 903 leaves differ outside top-level `mix`). So the ref -> first-post-ship movement in `composition.other`
  (-18,990.72), `composition.unclassified` (+58.43) and `top_holdings` is an INPUT change between the two runs, not
  an effect of the e60 code. Per ruling item 2 this is the "delta appears under both" branch. **The close of arm 2
  is the CTO's to enter; this seat does not enter it.**
- **The $128 split (ruling item 3): appears ONLY under the new code, so by the rule it is e60's behaviour.**
  Old: top-level `unclassified` 972,749.97 = `composition.mix.unclassified` 972,749.97. New: top-level
  `Unclassified` 972,621.40 vs `composition.mix.unclassified` 972,749.97, a gap of 128.57.
  Mechanism, from the code's own docstring (`D_04...py:411-423`) and one read of the served files, NOT re-derived by a
  separate run: new `Unclassified = total - sum(canonical class market values)`, so it absorbs any gap between the
  C_06 snapshot's firm total and the classes. In the current served file (`5Ws3Q6...`, asof 2026-10-08):
  sum(top-level mix) = 2,014,814,865.45 vs sum(`composition.mix`) = 2,014,814,994.03 (diff 128.58, and
  `composition.total_market_value` = 2,014,814,994.02). In the first post-ship file (`fyP5Js...`, asof 2026-10-07)
  the same gap is -128.07 the other way. So the two input files disagree on the firm total by about $128 and the new
  code serves that residual in the `Unclassified` line by design; the old code did not surface it. Whether the
  residual belongs in `Unclassified` is the CTO's design call, not a measurement.

No rollback; hold and both rollback targets stay live; nothing written.

## Owed, and by whom

1. `1.0.0_SA_CTO~DELL1`: enter the arm-2 outcome from the AC2 diff above (composition: not e60's), and rule whether
   the $128 total-gap residual in the top-level `Unclassified` line is accepted or a new forward leg.
2. `2.0.0_SA_COO~M1`: e79 leg G is the issuer's and reads not-effective (23 securities still unclassified).
3. Leg G stays OPEN and the entry HELD; this seat closes neither until the CTO's entry in item 1.
