# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 36, CB-aj-2: rewrite 38 cot price keys without the 49F rows

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-09 ~13:2xZ**
**Act:** `0.7.0_AE_CloudOps~CB2` writes ONE new version of each of the 38 keys below in `opal-data-cot` (CTO ADDENDUM 10, msg 3266:
REWRITE, not delete). Every prior version is KEPT. Deleting old versions is Andrew's act and is not part of this pair.

## 1. Blast radius -- exactly 38 keys in `opal-data-cot`, one new version each; nothing deleted

Versioning was read `Enabled` (~12:3xZ). Each key's current version equalled the one below when CB-aj-1 read it (~13:0xZ). The applier
re-reads each key immediately before its write, and stops on any change.

| key | prior VersionId | rows before -> after | 49F rows removed | new sha256 |
|---|---|---|---|---|
| `silver/prices/2026-04-14.parquet` | `fGDQqialTgvN2alIUQLhQABTfk5c3Bxu` | 10105 -> 10102 | 3 | `59651c7e4fc1fbf3d7222113838d51d5ee03fe71276f959861858ca367dd58f7` |
| `silver/prices/2026-04-16.parquet` | `caXhQHwomxRDe9Avx41lKomKbjCUA00b` | 10124 -> 10121 | 3 | `3696ffee3e7c2172cec2bb8479ee481501ebfb2a696a7f618fe78937793c4ea4` |
| `silver/prices/2026-04-17.parquet` | `czKjJFbHforLgeJ3tM.JRH.7pEPmSGGk` | 10125 -> 10122 | 3 | `2ccae09a8e96e39a9d65b74e812c9d87111397074fcf7eca54d09355725b52e7` |
| `silver/prices/2026-04-20.parquet` | `TwJXQ8zV8U1euL1jTwACFuvZEgqnqkgH` | 10126 -> 10123 | 3 | `0fcd104f9c70519f111b58bda853544166f013c3d1b6cb119b796c230640776d` |
| `silver/prices/2026-04-21.parquet` | `JrzcHd773qTIxPW3jNoUHIhU2Y3C2DbD` | 10126 -> 10123 | 3 | `2625f32554a10e7560097dcb3855dc9b908e326cf28a54c54737840ad901b009` |
| `silver/prices/2026-04-22.parquet` | `B9X2y1p8EsDlUOusorKGhkn3qSOeDoiY` | 10133 -> 10130 | 3 | `287ffa41639b61c9fcb294392b12cb67b5b9acf13123f74968fc3c429b33a2cb` |
| `silver/prices/2026-04-23.parquet` | `mbuwkdfSEll7X0Yx5t6pdJeG9KBJysgU` | 10140 -> 10137 | 3 | `0fe7879fda275a7af7ef18645c69d62528f24d90daadc0aae15e2a855d94d624` |
| `silver/prices/2026-04-24.parquet` | `1OjAMbv9YEv37QyU3Khj0TnW_c8pL0lP` | 10147 -> 10144 | 3 | `5308673bad47e01dc6fcb7587ee3f3f42e1bf49c6a8b95cee8d9e1d46d442614` |
| `silver/prices/2026-04-27.parquet` | `c0lMrA7E8g0jvaP7TP600MzuD_njTuHY` | 10185 -> 10182 | 3 | `1f28ae1612c8f2318be85155b30c5cda625cdf231909083d51d565fb2ce7fe29` |
| `silver/prices/2026-04-28.parquet` | `Tbx52ptIPheS6rKNBMrARmKccpBbukVf` | 10259 -> 10256 | 3 | `e6668839bc35b7b2c4ec992d435dbff2197578b6768e5f0b74479afb8b0f204a` |
| `silver/prices/2026-04-29.parquet` | `YXLvMjhF.D9otcpUaG1XX66GxgGXcogj` | 10259 -> 10256 | 3 | `7ba2c50a963e37ae1ce39211dc533e877776cd185b3f746fbeca52ed14655a74` |
| `silver/prices/2026-04-30.parquet` | `1D08jFPxSuw81TApuiflaJpu0H9zxzWF` | 10265 -> 10262 | 3 | `4de6006c3123e5e575f26c5b9eedbca4048b7759afa2d73f7e184db22a3da81e` |
| `silver/prices/2026-05-04.parquet` | `oFkYK5EB2qpexVPxkI62k6EnJGU6h4G.` | 10268 -> 10265 | 3 | `25cc51cdc118dfdc0c807a4bbcf448abff8652a706e47e4dcd05e83f82e8ffb8` |
| `silver/prices/2026-05-05.parquet` | `IIFfnW_OUH95tN3CBrrft6llJid3Sjgk` | 10275 -> 10272 | 3 | `7d4f10ef40c474f15cddb8e2f6c3623594ab85041393cc17f46011448f48a44f` |
| `silver/prices/2026-05-06.parquet` | `LfA2PCtbhI3dV_HQ7m7P.ETkkjZKWJI1` | 10278 -> 10275 | 3 | `bd9bc76a5fa7b145c6e5afc54a8cf8571f99da15f2836687da385966a8fcf2a7` |
| `silver/prices/2026-05-07.parquet` | `be1xbPwTSUP2wcyyV0QApVAM98ck5NT6` | 10283 -> 10280 | 3 | `f09b229f250698a3a95114aed053eefe3b0464dfd986eaccf215ab60f6c9221d` |
| `silver/prices/2026-05-08.parquet` | `SIZGSKhey.dOZ.qhZ4hXTPTW.IvHW03J` | 10298 -> 10295 | 3 | `a5feb27d086814b69e460f50c7e738be98d3bb87afc9433e62aa53e48cae4048` |
| `silver/prices/2026-05-11.parquet` | `nAhHmfBH6B63S7KEBwELRBAJLQmccimq` | 10296 -> 10293 | 3 | `11bf5d57c18c63230c0334c5c18658f63261c10a9ee535eb376f776236a5902a` |
| `silver/prices/2026-05-12.parquet` | `kp7_FU6rA95cy3TNTA8BnDE_HafFHEZw` | 10298 -> 10295 | 3 | `8258b43832b7f39eb82660d964c62a0703786d1fb0e26cc634cf7d5729616c2a` |
| `silver/prices/2026-05-13.parquet` | `KdVXRL7Y60Dt72QV_9ZjxDwoRecBJLq4` | 10308 -> 10305 | 3 | `820429192342ebae6ee7b585d4babff82979861c84a5c1886b80a0b086bb2d5a` |
| `silver/prices/2026-05-14.parquet` | `.pQnItAObcRxj9jUM0NU_ozL_znuX7SP` | 10315 -> 10312 | 3 | `5b0508db1f8f63fcab5824af98d6b75cc0d9c0b9a0d163612e4298f7269f0078` |
| `silver/prices/2026-05-15.parquet` | `mD..bqASta3ohrSMbzcoifq6d4mNJ4.0` | 10320 -> 10317 | 3 | `1d1fb1f276b50768406da763d5e75224ac2b6afbd8cc00ee1b15ee9563f667d8` |
| `silver/prices/2026-05-18.parquet` | `qQe.cCm5J.T1IhQdwJQcEkszX6RsMaXP` | 10323 -> 10320 | 3 | `09632d0e50a6696c0f0b1e0f06c7ca580119bd10f207096f50d0626f4ae0e02a` |
| `silver/prices/2026-05-19.parquet` | `OcIgOhsAFa8HUCSGLUfuuW_2Q9S_bK.W` | 10329 -> 10326 | 3 | `3e3c9b66117628275f68095afe49ce16454c29c5573b98d8b69aa56575bae424` |
| `silver/prices/2026-05-20.parquet` | `8GdsjITbs_y0cE4_rRIgOanVzzlSOOYX` | 10361 -> 10358 | 3 | `efd827d5700e917895da5de8f155fc6a540259e4493d24a78d1558954552968f` |
| `silver/prices/2026-05-21.parquet` | `pIjx7aGqJlvyUfrMHhufKKxoo40TC9wR` | 10393 -> 10390 | 3 | `c871006c9e1402ffd53aa2db6d4c509f4ef8d398c742e7ef3710238805794107` |
| `silver/prices/2026-05-22.parquet` | `zwXI4yS8.ZJ1oSmcfziLQ2a4sM3.uZyf` | 10394 -> 10391 | 3 | `a3d0997b26fd94522b223e4775ee8e81a042c64c0b92d7bfc48d2e235d9a18bb` |
| `silver/prices/2026-05-25.parquet` | `D.Fx79yUNPIOuldA9S3dfuVq_SQaDh0.` | 10393 -> 10390 | 3 | `9ccc7e83bc909637fba94a56c6cb2d64a24ff4be7ca3482c42f4c06e1909ed5e` |
| `silver/prices/2026-05-26.parquet` | `yX9Gx8AYTtK61H8uYTzk.DSyVpGHXkH1` | 10397 -> 10394 | 3 | `bc1b90ea9da15059febb48bb88b659108f02240b0b2d9a913d300f5813dfa182` |
| `silver/prices/2026-05-27.parquet` | `5FxAH5L9g4O8xSSERPMZWb.aWux75hvL` | 10398 -> 10395 | 3 | `373b5dcf2f10ffa5332b650d2a0065cddfbd7a641cf96c3dc46dd02d9cbe4a41` |
| `silver/prices/2026-05-28.parquet` | `93CqOKffS4POLtg3xfXcDAspkGsaWFpV` | 10405 -> 10402 | 3 | `d645ac0cd046e3f8525940f89a2fda8f7d51855e987c40e0095f852e4004e706` |
| `silver/prices/2026-05-29.parquet` | `vNaVF9blcQ_5EkZ.UA_DertoV9HNWjRJ` | 10416 -> 10413 | 3 | `1c839003e1d6860f0fa3c0e54d9927e9cbbcf621522655860bca5f2984fd552d` |
| `silver/prices/2026-06-01.parquet` | `PVpSfIr7tjSHRJPRW.MpKXNMAsG1eJcx` | 10417 -> 10414 | 3 | `ec65fe8820f74f5a99112ccf230564e912aca549802edc1a7b4de8578ce74007` |
| `silver/prices/2026-06-02.parquet` | `lhV2qus.hrLyOQdGD3osNxRmQqnlWlEc` | 10423 -> 10420 | 3 | `c6f973ff51c3fc9b5ab6f62153f83dceb0cbe1a0977be10c084a70177d35ee71` |
| `silver/prices/2026-06-03.parquet` | `cPBbHdli7nnIv3Hrs5_ZlmjCfV5sWxt8` | 10429 -> 10426 | 3 | `8596205f3516ae0da9b7106b702c1e3679c155e93a262b542147ca788142f0ef` |
| `silver/prices/2026-06-04.parquet` | `6KSd_Co.aCVO0k0JtTTQbSzhS1wFO6tw` | 10443 -> 10440 | 3 | `c92c0279cb0e7394a020c44d47e2430b42bc6667ae1b8dbcd861b17bb3a660bf` |
| `silver/prices/2026-06-05.parquet` | `gphtVrpZ0ZTLVuWuYEPPG01tsyusehuO` | 10464 -> 10461 | 3 | `005775aed4ece252fe3b5f864f1dd8f3f79c8070f8276ecd1f936bc652285267` |
| `silver/prices/canonical_prices.parquet` | `5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc` | 11291021 -> 11289398 | 1623 | `51a1f1f7e19a0ce3d8332484dd53aec431f061d51b1279c9dc020990a17087fa` |

- Totals: 1,734 rows removed (111 across the 37 daily files and 1,623 in the store); 0 re-priced. `other_rows_identical=True` on 38/38.
  Schema, column order, dtypes and pandas metadata are equal.
- Build: CB-aj-1 (~64, drained @370c142ec0). The issuer re-ran it at ~13:1xZ and got the same LAST line,
  `COT-PRICE-REWRITE keys=38 rows_removed=1734 rows_repriced=0 other_rows_identical=True bonds_priced=0/3 writers=7 scheduled=0`. The
  local files' sha256 were re-read against the manifest: all 38 equal.
- Files to apply: `.scratch/advi_cotbkf/cot_price_rewrite/<key>` (shared tree), applied as built.

## 2. Rollback per key

`s3api copy-object --copy-source opal-data-cot/<key>?versionId=<prior VersionId>` restores the prior bytes as the current version. No
version is deleted, so every rollback stays executable.

## 3. Writers and readers of the named property

- **Writers:** 7 code writers of `silver/prices/` in the repo (CB-aj-1 census, row W64-S2). One is in the cot tree:
  `data/cot/scripts/gold/build_canonical_prices_v2.py:624`. Six are in other firms' trees, with defaults to their own buckets.
  - **Scheduled writers: 0.** The live `opal-cot-gold-run` document (v10) names no price writer. The one cot builder runs only on a
    manual `gold_dispatch` silver-prep.
  - **BLIND:** the cot code mirror (`code/gold/` in the bucket) is not in the repo, and it was not read.
- **Readers:** the cot gold chain and this project's FWD-3 chain read the latest version.
  - The as-traded FWD-3 serve already holds the three bonds (988 account-days, `HELD_SOURCE_UNDER_REVIEW`), so this rewrite moves no
    served FWD-3 value.

## 4. Both branches of the bonds

The pre-written rule (CB-aj-1) re-prices a bond from a bond-specific Yahoo series, or removes its 49F rows with no replacement.
- **MEASURED:** no bond-specific series exists for 05613L3H2, 95000U2D4 or 651639AX4 (search empty, history empty, 6 calls per run). So
  this rewrite REMOVES their rows, and the three bonds read UNPRICED in cot's store.
- Row W64-S1 (BLOCKING) asks for a source ruling. A later source re-enters them as its own delta.
- If the CTO rules the bonds must not go unpriced before a source exists, this half is not used, and the rewrite waits.
