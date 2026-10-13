# TO-SC-e91b -- first BD fire after the ship: cost report and the rollback map (0.7.0_AE_CloudOps~SC1, 2026-10-13 ~01:30Z)

Written for a reader with zero prior context. The order asks this seat, after the first BD fire that follows the
ship, for C_06's wall time and the chain's launch-to-stop. Leg G is the issuer's and is NOT graded here; the
issuer's own read is row `MDPF_SECCLASS-D1-S33`. Every figure below is measured; none is graded.

## 1. Cost (the order's step 5 STOP rule: chain more than 30 minutes over the baseline)

| | baseline fire (launch 2026-10-12T04:00:46Z) | first post-ship fire (launch 2026-10-12T23:00:11Z) |
|---|---|---|
| C_06 wall time | 15.5 s (runner telemetry run_id 4850986714c5) | 186.0 s (the script's own `[PERF]` line); telemetry run_id fb0a94383bb0 reads 185.6 s |
| C_06 peak memory | 6,767 MB (telemetry) | 6,349 MB (`[PERF]` line; telemetry 6,356 MB) |
| chain log upload (same basis, both fires) | 06:13:56Z = 2 h 13 m 10 s after launch | 01:15:44Z = 2 h 15 m 33 s after launch |
| difference on that basis | | +2 m 23 s, against a STOP threshold of +30 m |
| runner state | `stopped` read at 06:15Z | `stopped` read at 01:19:42Z (the poll that saw it ran every 120 s) |

The chain's own completion line is the issuer's read in S33 (`Finished 2026-10-13T01:12:06Z`, 7,915 s). The exact
EC2 stop second was not measured: the instance reports `Client.InstanceInitiatedShutdown`, with no timestamp.
**The STOP rule's cost arm did not fire.**

The `gold_incremental_*.log` files are CUMULATIVE: the new log carries 258 `C_06 done (rc=0)` lines against the
baseline log's 257, and the same `(Ns)` lines (4 x 10 s, 2 x 164 s, 165, 163, 162, 11). Do not read those `(Ns)`
lines as this fire's C_06; the PERF line and the telemetry are.

## 2. Where the fire wrote, and the rollback map

**The leg-P file (`E91_PREFIRE_VERSIONS_20261012.json`) enumerated the opal-data-bd legacy keys the order named.
Since the FB-f-9 mode move (2026-10-12T06:18Z) the runner writes the served platinum keys to
`opal-data-49financial`, so three of the keys the fire wrote are NOT in that file.** Their pre-fire versions were
recovered from S3 versioning (read-only `list-object-versions`); nothing was lost:

| key (bucket `opal-data-49financial`) | pre-fire VersionId (restore target) | post-fire VersionId |
|---|---|---|
| `advi/49financial/platinum/views/mix_daily_summary.json` | `VyuLE19UQIHCSF6bkM9Brja6Lz___8RF` (2026-10-12T07:29:12Z, 9,877,189 B) | `ZuygB9ZtOGqSqiaE.3gV_ae70lhbSZeF` (C_06, 2026-10-13T00:23:32Z, 9,877,657 B) |
| `advi/49financial/platinum/views/firm_composition.json` | `hc9AxGVC1eqKg2GEgZhW.yAt_b47v3Da` (2026-10-12T07:29:12Z, 20,115 B) | `VXXufiw3xDbnLnCOKpS4UHcz3BxD85F3` (D_03, 00:24:53Z) |
| `advi/49financial/platinum/firm/mix_summary.json` | `MkgiFxUGLLC0pTSdmgV1bTD2lyQNBdlH` (2026-10-12T07:31:34Z, 25,124 B) | `l_Ch9mqN5wIdAEAOC0xmIdH3ht2.jOhd` (D_04, 00:45:57Z, 25,131 B) |

The 1,592 keys under `opal-data-bd` `gold/client_timeseries/` (796 relationships x `{rid}.json` + `{rid}_views.json`,
LastModified 00:20:48Z to 00:23:32Z) ARE in leg P. Their pre-fire and post-fire VersionIds are in
`E91_FIRE1_REWRITTEN_KEYS_20261013.json` (0 without a leg-P VersionId). The legacy opal-data-bd keys
(`gold/views/mix_daily_summary.json` `VrrTn2...`, `platinum/firm/mix_summary.json` `_MTtBm...`,
`gold/views/firm_composition.json` `28eJeU...`) did not move and are now stale copies, not the served ones.

Code rollback, unused: C_06 to `5xAeM.OWYUSxd7gHYSF6SKmR.ZTmo.PP` (restores behaviour, not rewritten content).

## 3. What this seat does NOT do

It does not restore anything. The order's step 5 says the issuer says so, and the issuer's row S33 reads the
named bounds as holding and the extra eight dates as an observation. Nothing here changes that read. The next
scheduled fire is 04:00Z today; C_06's retained pass is expected to be a no-op on it (the issuer's idempotence
read, COO condition 5(b), is the issuer's).

## 4. Compiler tools

| tool | result |
|---|---|
| runner telemetry jsonl (S3, both fires) | wall and peak memory above |
| boto3 `list_object_versions` paginator over `gold/client_timeseries/` | 199 pages, 1,592 keys in the window, 0 without a leg-P VersionId |
| `aws s3api list-object-versions` on the canonical bucket | the three restore targets above |
| comp-rail | no denial this segment |
