# NFRA_OPLGTW.TO-OG-c-2 -- result: deployed, replayed, 11 of 11 criteria PASS

**Worker:** `0.9.0_WK_NFRA_OPLGTW~4` (cold re-hand) | **Branch:** `wk-nfra_oplgtw-1-4c` (worktree `/c/tmp/wk-oplgtw-1-4c`, cut
from `CLOUD` @15f94697aa) | **Spec:** PRD C3/C6 @f0aa50dbc0 | **Decomposition:** v1 @8768f46770, cell `OG-c-2` |
**Status:** 11 of 11 criteria PASS by output; both ledger entries CLOSED.

This file replaces the 2026-09-15 refusal (branch `wk-nfra_oplgtw-1-4b`). That run's vendoring and pin were neutralized
on CLOUD @93b595bc5b and are redone here.

## 1. Replayed date, keys and VersionIds

**D_r = 2026-09-15**, one event per master, invoked RequestResponse with one attempt and no retry.

| master | object | key | VersionId |
|---|---|---|---|
| 08242234 | run manifest | `schwab/08242234/meta/conversions/20260916T190956Z-270202fe.json` | `b9CJ36knmcuIAVOKGS8AUTHVkFCicaJj` |
| 08242234 | **closure record** | `schwab/08242234/meta/complete/date=2026-09-15.json` | `k9L6O5yamDXLpnuytSlsYfONV_sO7eHK` |
| 08335338 | run manifest | `schwab/08335338/meta/conversions/20260916T191106Z-cdcf8453.json` | `uqu579S2Xp8KKKtwQBCFyptj_HL.0Agf` |
| 08335338 | **closure record** | `schwab/08335338/meta/complete/date=2026-09-15.json` | `ReevhBJRXCWNerbIirOWCfJG5G_Ewqc1` |

Details for each record:

- **Status and guard:** status `qualified`; `validate_closure` returns qualified with 0 findings; `write_guard: conditional`.
- **Writes:** exactly 1 version was written per object after its invoke, and there are 0 delete markers.
- **Conversions:** `converted=0` on both runs, so every bronze key was skipped as idempotent or as a hole.
- **Previous marker versions (rollback reference):** 08242234 `MyJhWqfwSw4W6KyZ507Yr8yxbKxQN9gA`, 08335338
  `y.rRwBm9VIgqlfJZtrg1Ee4zmFFhMr7.`.
- **Rollback:** per G-B s.6, run `delete-object` on each of the four VersionIds above.
- **G-B condition 3, branch a:** `write_guard: conditional` shows the runtime's botocore sends the conditional headers.
  The version was not readable before A1 (`deploy/pre_deploy.json`).

## 2. What was done, in order (commits LOCAL on `wk-nfra_oplgtw-1-4c`)

1. **Un-staging commit, d7ce5f59fc.**
   - `infra/aws/terraform/opal-assets/emitter.tf` was restored to the bytes of `2740e4de8f^` (blob 277df8b907).
   - The file was written with `git show 2740e4de8f^:<path> > <path>` rather than `git checkout ... --`, because this
     worker's standing rules forbid `checkout --`. The resulting blob is identical.
2. **Vendoring and pin, df06cbadbb.**
   - Vendored 11 of 11 modules byte-equal to `1f03a3f209`, with CR 0.
   - Moved `silver_build_commit.schwab` from 5c7b2a9a6b to 1f03a3f209.
   - commit-gate: clean for 2 of 2.
3. **Pre-upload plan:** 210 resource_changes, 1 changed (the schwab function; `OPAL_BUILD_COMMIT` only).
4. **Deploy ledger opened, 58a95125c1:** `nfra-oplgtw-og-c-2-producer`, committed with the pre-upload plan and
   `deploy/pre_deploy.json`.
5. **Build.**
   - The first attempt exited rc=1 silently, before the zip (row W4-S10: `set -e` at the manifest-declaration probe).
   - The re-run with the script's documented `BAU_MANIFEST_SKIP=1` passed import-closure OK and printed
     SHA256 `v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`. The upload was VERIFIED as artifact version
     `7Db1UfM3EU_Z6q4cLQiV4wM3bYaAaFMF`.
   - The build rewrote `infra/aws/lambda/ci/lambda-source-map.json`, which is outside the grant (row W4-S7). **That file
     is left uncommitted in the worktree.**
6. **Post-upload plan** (`plans/plan_apply.json`): 1 changed row, adding `s3_object_version` and `source_code_hash` to the
   env change.
7. **safe-apply.**
   - The halt gate listed 18 routine messages to the issuer `2.0.0_SA_COO~O` and 0 `[STOP]`. They were reviewed, and
     the apply re-ran with `HALT_ACK=1`.
   - Result: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` rc=0 at 18:49:35Z.
8. **Readback.** CodeSha256 equals the built SHA256; `OPAL_BUILD_COMMIT` is 1f03a3f209; the function is
   Active/Successful. A post-apply plan reads `No changes.` with rc=0.
9. **Deploy ledger closed, 75da3e906a:** 2 of 2 legs.
10. **Hold check** at CLOUD HEAD 68bd819cd8 in the shared tree:
    - The hold paragraph is ABSENT. The order was amended @7c44a2cf82, and the replay is RELEASED on R-OG-4/R-OG-5.
    - The sign-off Half 1 s.6 and Half 2 s.E are re-signed on a four-object write set, with a zero-write dry run as STOP.
    - The replay below follows those released terms.
11. **Dry run, f148ec0f19** (`replay/dry_run.py` and `dry_run.json`):
    - Both masters: `silver_writes=0 missing_dims=0 missing_facts=0 errors=0 marker_dates=["2026-09-15"]`; the closure
      preview is qualified. Output: `DRYRUN: ZERO-WRITES`.
    - The wrapper's positive controls fired.
    - The replay ledger `nfra-oplgtw-og-c-2-replay` was opened and committed in the same commit.
12. **Before-snapshots:** silver (29 objects), markers, and the 49F `date=2026-09-15` keys (31).
13. **Replay:** 08242234 at 19:09:50Z, then 08335338 at 19:11:03Z.
14. **After-snapshots and readbacks.** The replay ledger was closed with 3 of 3 legs, committed with rows W4-S11/S12
    (b173871660).

## 3. G-B conditions, each with its measurement

| # | condition | measured |
|---|---|---|
| 1 | 08335338 write outside the burst and floor windows | written 19:11:03Z |
| 2/5 | every dispatch A2 caused: time, branch, command, chain log, before/after VersionIds | **1** dispatcher invocation (19:11:18Z); host `stopped` -> started; command `8e7e7614-e014-4342-ae4a-47b8bb7ac0d1`, SSM `Success`. **Branch W:** `gold/advi/_logs/chain_20260916T191146Z.log` (v `v46i6VrCC8vcbd4.1l49c88tS1GtV7aK`) reads `CHAIN START date=2026-09-15 ... stages=18` .. `CHAIN OK date=2026-09-15 wall=144.6s`. **30 of 31** `date=2026-09-15` keys re-PUT, 1 unchanged (`insurance/insurance_nav_current/.../data.parquet`); every before/after VersionId is in `replay/gold49f_date_d_before.json` / `_after.json`. The dispatcher's own verdict line reads `ERROR ... signature=UNKNOWN` for this run (row W4-S12). The host was `stopped` again at 19:24:32Z |
| 3 | botocore before A1 | version ABSENT (not readable without executing in the function); branch decided by the record: `write_guard: conditional` (a) |
| 4 | the day's 12:45Z floor `CHAIN OK date=<prev_trading_day>` and no live lock | `chain_20260916T124542Z.log` (v `znOeMrzHJT6Qr4Aw4u2Zy6ziTnE790CN`) last line `CHAIN OK date=2026-09-15 wall=135.2s`; the host was `stopped` at 19:03Z. SSM list-commands returned 0 even unfiltered, so it is NOT EVALUATED |
| 6 | 08242234 has no consumer | no dispatcher invocation between 19:09Z and 19:11:18Z |
| 7 | W-partial not left standing | not applicable: the branch was W (`CHAIN OK`) |

**49F reads, every call** (admitted by R-OG-4; listed in the evidence files):

- The `_logs/chain_20260916` listing, and 2 log gets (`T124542Z`, `T191146Z`).
- On each of 2 passes, 5 delimiter listings. Those listings name the `date=D` tables, and they are one level above the
  admitted keys (row W4-S11).
- On each pass, 24 `list-object-versions` calls on `<table>/date=2026-09-15/`.

Nothing was written to that bucket by this worker.

## 4. Criteria, run as the order writes them (`<WS>` = `/c/tmp/wk-oplgtw-1-4c`, HEAD b173871660)

| id | deciding output | rc | denominator |
|---|---|---|---|
| OGC2-AC1 | `VERDICT: PASS-OGC2-AC1` | 0 | 11 of 11 vendored modules EQUAL, CR 0 |
| OGC2-AC2 | `VERDICT: PASS-OGC2-AC2` (pin 1f03a3f209; live env 1f03a3f209) | 0 | 1 pin |
| OGC2-AC3 | `VERDICT: PASS-OGC2-AC3` | 0 | 210 resource_changes, 1 with an action; 7 families, 0 rows for the 6 others |
| OGC2-AC4 | `VERDICT: PASS-OGC2-AC4` (sentinel 58a95125c1 at 18:36:55Z < LastModified 18:49:30Z) | 0 | 1 entry, 1 sentinel, 1 function |
| OGC2-AC5 | `VERDICT: PASS-OGC2-AC5` (live = built `v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`) | 0 | 1 function, 1 build |
| OGC2-AC6 | `VERDICT: PASS-OGC2-AC6` (both halves SIGNED, cited @65e254cafe, before sentinel 58a95125c1) | 0 | 2 of 2 halves |
| OGC2-AC7 | `VERDICT: PASS-OGC2-AC7` | 0 | 2 records, 2 masters, date 2026-09-15 |
| OGC2-AC8 | `VERDICT: PASS-OGC2-AC8` | 0 | 2 records, 20 fields each, 0 findings |
| OGC2-AC9 | `VERDICT: PASS-OGC2-AC9` | 0 | 29 VersionIds across 2 records |
| OGC2-AC10 | `VERDICT: PASS-OGC2-AC10` | 0 | 29 silver objects across 2 masters |
| OGC2-AC11 | `VERDICT: PASS-OGC2-AC11` | 0 | 7 bucket values + 11 notification configurations + EventBridge flag, all MATCH |

**On AC6's grain:** the probe reads the sign-off at this worktree's HEAD, which is the 2026-09-15 two-half text
(@65e254cafe). The replay's released terms are the amended text at CLOUD (@7c44a2cf82 / @f81896bae3), which this branch
does not carry. Both carry both halves; the probe grades the former.

## 5. Rows filed by this run

| row | class | hazard | what |
|---|---|---|---|
| `NFRA_OPLGTW-W4-S10` | OBSERVATION | INERT | the estate build exits rc=1 silently for a package with no `declared_blobs`; this build used `BAU_MANIFEST_SKIP=1` |
| `NFRA_OPLGTW-W4-S11` | OBSERVATION | INERT | naming "every date=D key" needed 5 prefix listings per pass above the admitted keys |
| `NFRA_OPLGTW-W4-S12` | OBSERVATION | INERT | the dispatcher logs `ERROR signature=UNKNOWN` on a CHAIN OK run |

## 6. Left in the worktree, not committed

`infra/aws/lambda/ci/lambda-source-map.json`: the build's rewrite of the schwab entry's `artifact_sha256`. This path is
outside the grant (row W4-S7). At HEAD the map still carries the previous hash until its owner commits it.
