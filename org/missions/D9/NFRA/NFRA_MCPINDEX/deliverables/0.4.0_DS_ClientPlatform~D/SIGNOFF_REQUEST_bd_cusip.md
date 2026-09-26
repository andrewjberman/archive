# SIGN-OFF REQUEST -- NEVER-1 never-widen, `holdings_lots` cusip correction

Requested by `0.4.0_DS_ClientPlatform~D` under `NFRA_MCPINDEX.TO-MX-s-2` step 2.
Halves owed: `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`. **Nothing served has moved. It will not move
until both halves are recorded in THIS file.**

## RECOMMENDATION FROM THE REQUESTER: DO NOT SIGN YET

I am required to write this file and I am writing it, but the measurement says the act it
authorises cannot succeed today. Signing now would spend a never-widen sign-off on a rewrite that
reproduces the same numbers.

- `silver/bd_assets_dim.parquet`, the bridge B_01 joins on, is frozen at **2026-04-14T20:44:16Z**,
  and its own input `silver/bd_assets.parquet` is frozen at **2026-04-14T20:09:23Z**. Rewriting a
  partition re-runs the same join against the same bridge.
- The upstream download has failed **69 consecutive runs since 2026-06-23** on one BD portal login
  timeout. Until that is repaired the bridge cannot be made current by any act in this lane.
- **Sign once the bridge is current.** Then the blast radius below is the right one and the rewrite
  is worth its risk.

## WHAT THE ACT WOULD TOUCH

Re-run `data/black_diamond/scripts/gold/B_01.holdings_lots.py` for the partitions listed below and
PUT each result back to its own key. No key outside this list is written. No object is deleted.

- Bucket `opal-data-bd`, prefix `gold/timeseries/holdings_lots/`
- Partitions dated on/after the bridge freeze 2026-04-14: **73**
- Total partitions under the prefix: **99** (the 26 dated before 2026-04-14 are OUT of scope)

### Both branches of the outcome, read from the producer's own rule

NEVER-1 requires the expected outcome to be read from the producer's rule at signing and BOTH
branches covered. B_01's rule is at `:284-292`: it builds `cusip_map` from the bridge, drops
`'' / nan / None / CASH`, and fills a row's cusip from `asset_id` only when the existing value is
absent or nullish.

- **Branch A, bridge still frozen:** the map is the same 10,937 asset_ids, so every filled and every
  null cusip resolves identically. **Expected delta: 0 rows changed.** The only movement is the
  object's LastModified and VersionId. This is today's branch.
- **Branch B, bridge current:** at most **1,798** of the 6,988 non-cash null rows on the latest
  partition could gain a cusip -- an UPPER bound measured by ticker, while B_01 joins on `asset_id`,
  so the two keys can disagree. **A floor of nulls is permanent regardless:** 1,037 of the bridge's
  10,937 assets carry no cusip at all, and 15,185 of the 22,173 nulls are cash by design.

### Writers of the property being changed

NEVER-1: count the writers first. **N = 1.** `B_01.holdings_lots.py` is the only producer that
writes `cusip` into `gold/timeseries/holdings_lots/`. It reads the bridge at run time, so its output
is a function of the bridge's vintage, not of this order.

### The manual path creates a reachable state the schedule does not

B_01 rewrites ONLY the current week's partition: **1 of 73** partitions were rewritten in the last 24h. The other **72** in scope have not been touched since their own week and will NOT self-correct when the bridge is fixed. So the split is:

- **1 partition(s) self-correct** on the existing nightly schedule once the bridge is current -- they need no manual rewrite and no sign-off at all.
- **72 partition(s) are frozen** and only a manual re-run reaches them. That manual path is what this sign-off is for.

### Rollback, per key

`opal-data-bd` versioning is **Enabled**, verified live, so every key rolls back to the VersionId below
with a single `copy_object` from that version. No backup copy is needed and none is made.

| # | partition | versions today | current LastModified (UTC) | ROLLBACK VersionId |
|---:|---|---:|---|---|
| 1 | `2026-04-14.parquet` | 1 | 2026-04-14T22:18:23+00:00 | `RIB.Z.8_AKERkTA_LOdAwc1hhDPpXPYP` |
| 2 | `2026-04-15.parquet` | 1 | 2026-04-17T19:33:11+00:00 | `bVe5MYSnO2.N4FT6ta.7sn43pMWahgZM` |
| 3 | `2026-04-16.parquet` | 1 | 2026-04-20T04:20:42+00:00 | `ZIrG6UrWT7s4UEkPBu3dn9_L16k1lvsy` |
| 4 | `2026-04-17.parquet` | 1 | 2026-04-21T21:08:47+00:00 | `Y2UBnLIkHwmO5jbFCfcW0HfrztHEhx8P` |
| 5 | `2026-04-20.parquet` | 1 | 2026-04-22T20:00:37+00:00 | `BUP0....TMdrSefBSnisZTuAoS1ndlYW` |
| 6 | `2026-04-21.parquet` | 1 | 2026-04-23T04:26:14+00:00 | `l.bXyRM6v5fUkfO7APQxZEjVwU8uke17` |
| 7 | `2026-04-22.parquet` | 1 | 2026-04-24T04:26:06+00:00 | `U4O.vW0L.fkX2KdxzWWrus8gEkPTAxNl` |
| 8 | `2026-04-23.parquet` | 1 | 2026-04-27T04:26:11+00:00 | `8fgphV.f5vznC6AVvG03BNGmxsdhsSY.` |
| 9 | `2026-04-24.parquet` | 1 | 2026-04-28T04:27:08+00:00 | `kiLYh1pq_R.eiK4tfwK.yASQ5K2ziVBI` |
| 10 | `2026-04-27.parquet` | 1 | 2026-04-29T04:26:48+00:00 | `VNU2k5umgC_ShhqkddvsMmlywTJG6f5g` |
| 11 | `2026-04-28.parquet` | 1 | 2026-04-30T04:26:55+00:00 | `Qep1sU1hIBCCq2D63js0cnwJV0YybleV` |
| 12 | `2026-04-29.parquet` | 1 | 2026-05-01T04:26:17+00:00 | `cjWieuCGdP1f8PIYkBkbMbwMjkt3ipJQ` |
| 13 | `2026-04-30.parquet` | 1 | 2026-05-04T15:59:20+00:00 | `gIf91SXJkNIJ.MNqTZXrZ0X.iRvgGj7A` |
| 14 | `2026-05-01.parquet` | 1 | 2026-05-05T04:27:32+00:00 | `Z8.nRFkHSWFN0ST.H_oAMowwSCewB7z9` |
| 15 | `2026-05-04.parquet` | 1 | 2026-05-06T04:27:34+00:00 | `tnRMloviiDeWi62kKIEcdbX4mvzEespT` |
| 16 | `2026-05-05.parquet` | 1 | 2026-05-07T04:31:53+00:00 | `1wUPnP2YjNM0XK9XtGvy.GHXhvDfhhzQ` |
| 17 | `2026-05-06.parquet` | 1 | 2026-05-08T04:30:27+00:00 | `6g0b.vWuwnrVR1k6HjuFJmmQ93ciluCi` |
| 18 | `2026-05-07.parquet` | 1 | 2026-05-11T04:27:37+00:00 | `4S6wKU9I7CR121uDx88nLuSrDE08EIFz` |
| 19 | `2026-05-08.parquet` | 1 | 2026-05-12T19:16:59+00:00 | `IJ3qJuCIMpmOXEBcZZRnom.epAQGWMr4` |
| 20 | `2026-05-11.parquet` | 1 | 2026-05-13T04:27:44+00:00 | `W9k4xoZ1cQG9aKrrQTExFe.YSLLkfe.R` |
| 21 | `2026-05-12.parquet` | 1 | 2026-05-14T04:28:48+00:00 | `hKb2O6Y5ybL7w8bffI.8DVj4Vrk5e3JA` |
| 22 | `2026-05-13.parquet` | 1 | 2026-05-15T04:28:14+00:00 | `1D.WzeaNmda1PqHdxJm7O7yiji_lU8V3` |
| 23 | `2026-05-14.parquet` | 1 | 2026-05-18T04:28:20+00:00 | `lZgc1Vm4fx2t2q.OOL._J6hzvT6adANy` |
| 24 | `2026-05-15.parquet` | 1 | 2026-05-19T04:27:40+00:00 | `q30YTWT5.plHhAN_XYNpLoUemrwrINqs` |
| 25 | `2026-05-18.parquet` | 1 | 2026-05-20T04:27:52+00:00 | `JrABlUkRroeKaTjt1LXRy36WZtfCMPmn` |
| 26 | `2026-05-19.parquet` | 1 | 2026-05-21T04:28:18+00:00 | `1kdJP8UMpsdAhHxOT3nvjQ_rihC8KROv` |
| 27 | `2026-05-20.parquet` | 1 | 2026-05-22T04:28:45+00:00 | `E_AoMex_SNN1mkDJw3kEMRQmaw2H5YTv` |
| 28 | `2026-05-21.parquet` | 1 | 2026-05-25T04:34:06+00:00 | `t_B_XZ0vbY2SRePB5BQflVBvs0uXEUUb` |
| 29 | `2026-05-22.parquet` | 1 | 2026-05-27T04:28:14+00:00 | `JwMPvOLv_xOu2dJEThEn0w8M_WiT6NfC` |
| 30 | `2026-05-26.parquet` | 1 | 2026-05-28T04:21:08+00:00 | `yoJLLE0sE1LGjYbQMxCo0i5hP8jB._AT` |
| 31 | `2026-05-27.parquet` | 1 | 2026-05-29T04:28:38+00:00 | `7DSkW6QpARybwNZ5rNqO2k.7o.tXnU52` |
| 32 | `2026-05-28.parquet` | 1 | 2026-06-01T04:28:49+00:00 | `T3h4TyFTvjtkDsPVR9Nr6HzTVnMCuYwt` |
| 33 | `2026-05-29.parquet` | 1 | 2026-06-02T04:30:10+00:00 | `xSQdrvW1HuuEDBUfNhQrf0pjvQ30XHso` |
| 34 | `2026-06-01.parquet` | 1 | 2026-06-03T16:02:19+00:00 | `ZFSXFQnX7gwkVZEIx2_cDwzOd0fbED7d` |
| 35 | `2026-06-02.parquet` | 1 | 2026-06-04T04:31:46+00:00 | `xMg3R8xM6k.Rw0w4BwXdWcuaIjvBZaTO` |
| 36 | `2026-06-03.parquet` | 1 | 2026-06-05T04:37:04+00:00 | `ks3tvmQiAkDnxwiaEPmWMvzfjDVMPmjd` |
| 37 | `2026-06-04.parquet` | 1 | 2026-06-07T04:30:33+00:00 | `iUzqh3ml4kYAYcC84oAZPgnHc5TD5tlZ` |
| 38 | `2026-06-05.parquet` | 1 | 2026-06-09T04:30:05+00:00 | `6qJgrdsSy.4KVRwVKcTOgN72PYuyOht7` |
| 39 | `2026-06-08.parquet` | 1 | 2026-06-10T04:25:46+00:00 | `VUzIHRaY5ecLhNyMgU1XPgqZ23Ny36bN` |
| 40 | `2026-06-09.parquet` | 1 | 2026-06-11T04:25:28+00:00 | `J_IKzNShYQixExUqeCI8X8M3sTMQQCNq` |
| 41 | `2026-06-10.parquet` | 1 | 2026-06-12T04:27:53+00:00 | `Q1JpOj5KSrEybFDPo0T1fcRjPQX0RBgB` |
| 42 | `2026-06-11.parquet` | 1 | 2026-06-15T04:26:11+00:00 | `mOk7sRWGzg6Iu0TAdTbPz0ooB_.Qts84` |
| 43 | `2026-06-12.parquet` | 1 | 2026-06-16T04:25:59+00:00 | `hmU4Y2HlxDPaiOX5b4sPXruHr8e_RXAk` |
| 44 | `2026-06-15.parquet` | 1 | 2026-06-17T04:18:49+00:00 | `_e7WEbHH9PvvZld3gQhS.86rKfII7u11` |
| 45 | `2026-06-16.parquet` | 1 | 2026-06-18T04:27:27+00:00 | `SYkFKkHpuDyYRBsmeBEcQqvmPL5ep4aW` |
| 46 | `2026-06-17.parquet` | 1 | 2026-06-19T04:28:11+00:00 | `m.7of0UUov7cL57vFPFNcjMfukktZBw4` |
| 47 | `2026-06-18.parquet` | 1 | 2026-06-25T04:25:06+00:00 | `SMiScQEzc6akY6kF9CMPOXIwGAJ8IUrv` |
| 48 | `2026-06-24.parquet` | 1 | 2026-06-25T23:25:12+00:00 | `KwUAIOiLa4AP1qNoYC2mjIGCVO7Z5sr3` |
| 49 | `2026-06-26.parquet` | 1 | 2026-06-26T23:24:09+00:00 | `dxJJZK75AmTaTh5uoyv4O6ZGy8v_d9XP` |
| 50 | `2026-06-27.parquet` | 1 | 2026-06-27T23:24:26+00:00 | `tleIOK3Ypo9yDB5JUU0lirg9PrK0vitS` |
| 51 | `2026-06-28.parquet` | 1 | 2026-06-29T04:24:28+00:00 | `D2xUbnebmnhbUAIIyJiEWtc1n4mCf8kQ` |
| 52 | `2026-06-29.parquet` | 1 | 2026-07-02T04:26:29+00:00 | `1ymr10h0Tr4lIr_LBinFcw4aJWlfv9h7` |
| 53 | `2026-06-30.parquet` | 1 | 2026-07-02T15:38:09+00:00 | `luOqAVesRCPCqjDbIsctOK9N2foJNE81` |
| 54 | `2026-07-01.parquet` | 1 | 2026-07-02T17:08:54+00:00 | `KuVeyOR_2XExQJ1r7EzkEbTR1CxR.7f9` |
| 55 | `2026-07-02.parquet` | 1 | 2026-07-02T23:25:51+00:00 | `khwwKpENBImR8bqyPzhLURJJ7V0jIWAJ` |
| 56 | `2026-07-03.parquet` | 1 | 2026-07-03T23:25:16+00:00 | `umc4NvAA7vBXti9cXekXkpgTjjeTEK4m` |
| 57 | `2026-07-04.parquet` | 1 | 2026-07-04T23:25:35+00:00 | `.5QQCOuzn8oF4k.C4YRTYWEFLPUc3Qtm` |
| 58 | `2026-07-05.parquet` | 1 | 2026-07-05T04:24:57+00:00 | `PmCzvYBbWIhkyU88KMlH5L3iK_oPtG9H` |
| 59 | `2026-07-06.parquet` | 1 | 2026-07-06T23:24:58+00:00 | `QUvrMxqaVaZJK5IWDVXaFa6ku9n5M6Ew` |
| 60 | `2026-07-07.parquet` | 1 | 2026-07-07T23:26:28+00:00 | `qD.x8FuJKhP4YFJOPLkS1DCaoPLp1TYu` |
| 61 | `2026-07-08.parquet` | 1 | 2026-07-08T23:25:03+00:00 | `kR.5vnKzzxBMnDAVyeJMBcGFj8_efSZd` |
| 62 | `2026-07-09.parquet` | 1 | 2026-07-11T04:26:30+00:00 | `yKP8yqTxXI2ur6SZ3cMwHilp6BXbKYy_` |
| 63 | `2026-07-10.parquet` | 1 | 2026-07-18T23:25:40+00:00 | `Va7oCfNTekbP7_vXOmPr55QjwIS3JHiF` |
| 64 | `2026-07-17.parquet` | 1 | 2026-07-25T23:26:52+00:00 | `rmfjQ.qGcoMEJAksnEVFo92Z3QOuvF8u` |
| 65 | `2026-07-24.parquet` | 1 | 2026-08-01T23:26:27+00:00 | `r8DFrG77REl5LAAbxkjXtQL4kb5kdKiZ` |
| 66 | `2026-07-31.parquet` | 1 | 2026-08-08T23:29:52+00:00 | `um5LlXnfqImGU7N_2SEgNLpZfs3wxDgu` |
| 67 | `2026-08-07.parquet` | 1 | 2026-08-15T23:42:01+00:00 | `UnueQs0fx53Em0OQCnP2oMWLjrtBossb` |
| 68 | `2026-08-14.parquet` | 1 | 2026-08-22T23:43:10+00:00 | `Q2MNLi3QHvb1CC.xed06iuYVB15vy5BN` |
| 69 | `2026-08-21.parquet` | 1 | 2026-08-29T23:48:38+00:00 | `IHjv6Qb4SSCkfT5ykiLLuK7.VtIV_cIz` |
| 70 | `2026-08-28.parquet` | 1 | 2026-09-05T23:49:14+00:00 | `yVOoojN9V9cEdZ5CY8B_qyBtyeNhbGhd` |
| 71 | `2026-09-04.parquet` | 5 | 2026-09-12T23:50:57+00:00 | `aC_X10Neiwiz1gFBnEi2QnrSMHoS4VaB` |
| 72 | `2026-09-11.parquet` | 13 | 2026-09-19T23:52:17+00:00 | `jIFnWi1xf1qj0VTk2W8UEIy0Ct518QYo` |
| 73 | `2026-09-18.parquet` | 11 | 2026-09-25T23:55:58+00:00 | `h9YkSI9zxp.lEGqhFipygzexeqd.JKBT` |

## HALVES

| half | seat | verdict | at | note |
|---|---|---|---|---|
| never-widen | `1.0.0_SA_CTO~O` | UNSIGNED | -- | |
| never-widen | `2.0.0_SA_COO~O` | UNSIGNED | -- | |

Until both rows read SIGNED at these bytes, no partition above is rewritten.
