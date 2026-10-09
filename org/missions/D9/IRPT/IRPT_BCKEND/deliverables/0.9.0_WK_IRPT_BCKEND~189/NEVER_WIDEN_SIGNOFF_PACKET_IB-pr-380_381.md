# Never-widen sign-off packet -- IB-pr-380 + IB-pr-381: ONE release -- the runner states the source and carries source-removed entries TERMINATED; the refresh reads the served directory as its previous state and counts what the runner carried

Prepared by 0.9.0_WK_IRPT_BCKEND~189 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed, applied or run against a live write: BUILD_ONLY builds from a clean tree, offline replays, AWS reads only.
Files beside this packet: `IB93-1_directory_writers.json`, `IB93-1_release_replay.json`, `IB93-1_release_census.json`, `replay/` (the scripts). Models: `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380.md` (~188), `..._IB-pr-370.md` (~178).

**READ THIS FIRST (row IRPT_BCKEND-D2-W189-S1, BLOCKING, ARMED).** The release does what the ruling says, and it is proven on both real cases. But the served directory at BOTH firms has already lost the removed entry
(inflection since the 2026-10-06 build, cottonwood since 2026-10-07): the runner landed a build on every 09:40 ET fire, whatever the refresh's verdict said. A runner that carries from the *served* directory therefore has
nothing to carry. The after-read (`terminated_count` 1 AND the entry present in the served directory) needs ONE reconciling runner run per firm that carries from the last accounted-completion build, via the new
`--previous-key`. That run is a WORLD write of two keys per firm and is **Branch A step 2**; it needs its own ruling and was not run. Without it, this release is safe and changes the served bytes of nobody.

## The pin and the builds

- **Release pin P: `7f31bbfa4e06dfcb48af06fea3e20ea9f3606129`** (branch `wk-IRPT_BCKEND-189`). The history is `07dc601e48` (rule), `5aa352e6dd` (no new hand-kept firm-name table), `7f31bbfa4e` (unreadable source keys guarded); P is the last and contains all three.
  IB-pr-380's `8953eccfca` (the refresh rule) is an ancestor of P, so the refresh zip carries BOTH cells.
- **Refresh function `irpt-directory-refresh`**: `release-census.py irpt-directory-refresh --pin P` -> built 5 members, live 5, `changed_members=1` -- `refresh.py` (built `5335860d318a`, live `ed3d0c881890`). The other four functions that name the
  directory tree: `irpt-directory-search` 0 changed (24 of 24), `irpt-holdings` 0 (35), `irpt-holdings-refresh-lambda` 0 (1), `irpt-status` 4 changed (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`, `served.py`) -- NOT this release:
  none is in the diff of 380/381 (earlier cells IB-pr-321/322/327/366).
  BUILD_ONLY from a clean tree at P (porcelain 0 lines before and after), built twice, byte-identical:
  `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-refresh` rc 0.
  **Built sha256 `6eOFTopG9nvfjpJFJxtBNAUL43pBmg0YvHv9sbErfsM=`** (hex `e9e3854e8a46f67bdf8e9245271b4134050be37a419a0d18bc7bfdb1b12b7ec3`, 46,619 bytes, 5 members). Kept zip removed; nothing uploaded; source map untouched.
- **Runner bundle `investor-reporting.tar.gz`** (`irpt_runner_bundle_uri` in `infra/aws/terraform/investor-reporting/directory/schedule.tf`, `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`):
  built offline with the mint's own deterministic builder (`safe_deploy_core.build_bundle_payload` over bundle `investor_reporting`), twice, byte-identical.
  **Built sha256 `2e3e6648312f5daad1da91f0c3aaeb4736a81b16cc9bb0dd4f43e5e93886b968`** (md5 = the ETag a verified upload must echo: `b0356a757b1ae92e3a4b46a847378315`, 112,575 bytes, 12 members). Changed member: ONE of 12,
  `directory_runner.py` (stamp `directory-runner-sha256`: built `9375a3eb4685`, live `21147de26795`, and the live blob equals the base commit's). Build path: the builder above. Deploy path (the applier's, DS lane, CLAUDE.md rule 13):
  `bash .tools/safe-deploy.sh data/assets/scripts/gold/investor_reporting/directory_runner.py`, which routes the member to `mint_bundle('mdpf','investor_reporting')` (upload with the sha stamps, head-object verifies ETag == md5 and every stamp).
  No Terraform change: the next SSM run fetches the object at the URI (`refresh.py` `runner_script`, `aws s3 cp`).

## What the release does

- **Runner (`directory_runner.py`, the only writer).** Every landing states `source_client_ids` (the client keys the source snapshot holds, in the refresh's key space). It reads the previous SERVED directory first (`latest.json` and the dated
  `directory.json` it names) and lands every previous entry that this build AND the source both lack as `TERMINATED` + `source_removed_on` (marker byte-for-byte the refresh's: `termination.effective_date` and a `capability_facts` string; no contract change,
  row D2-W188-S3). An entry still in the source but missing from the build is NOT carried. Unknown source carries nothing. A previous directory of another firm is refused; an unreadable previous refuses the landing; unreadable source keys omit the field and
  land only if no previous client is missing (otherwise refuse). `--previous-key` (one firm) carries from a named dated directory instead of the served one.
- **Refresh (`refresh.py`).** (c) When no manifest names a previous build -- inflection from a fire dated 2026-10-09, the 2026-09-25 manifest being the 11th trading day back -- the previous state is the SERVED directory (no false 294 additions); a firm with no served
  directory behaves as before. `terminated_count` and `terminated_new` are taken over the final entry set, so entries the runner already carried are reported. Reading chosen: only the ABSENCE of a previous manifest falls back; a manifest in window still wins, so a
  real delta since that build is still a delta.
- Tests: runner `-k terminated_carry_forward` 23 passed; directory `-k previous_state_served` 10 passed; directory suite 211 passed whole; runner suite 364 passed and 1 failed -- `test_holdings_rearm_trigger.py::test_rearm_trigger_live`, a live holdings guard red at base
  (row D2-W189-S3, BLOCKING). Rows S2, S4, S5: see the end.

## Writers of the served directory (the census, step (a); `IB93-1_directory_writers.json`)

**1 writer** of `investor-reporting/directory/<as_of>/directory.json` and `investor-reporting/directory/latest.json`:

1. `directory_runner.land (data/assets/scripts/gold/investor_reporting/directory_runner.py, run on the mdpf-daily-runner host i-02448edb624a7a7cf under role mdpf-daily-runner-ec2-role)` -- the only code that puts either key; the only role with
   `s3:PutObject` on the directory prefix (read live: inline policy `mdpf-runner-scoped`, Sid `IrptDirectoryFirmDestWrite`). Live versions: all 33 versions of the two keys in the three buckets (49financial 12, inflection 10, cottonwood 11, 0 delete markers) land 0-300 s
  after exactly one runner SSM command named `irpt directory refresh <firm> <date>`: **33 of 33 matched**.

Not writers: `irpt-directory-refresh` (live inline policy: `s3:PutObject` only on `_refresh/*`; it sends the SSM command and writes the verdict beside the artifact), the two schedules (09:30 and 09:40 ET) and driven invocations (they trigger the one writer),
the readers, the holdings publication, the keep-warm rule.
**The served inflection `as_of` 2026-10-08 after a failed refresh is the runner's own landing**: SSM command `cf33dc53` requested 13:40:43Z -> `latest.json` and `2026-10-08/directory.json` LastModified 13:40:52Z. The verdict is a later read of an artifact already served; the
refresh cannot roll it back and does not try. Writers of the named property: 1; N rules read: 1 (the runner's `land`).

## Real-case replay (`IB93-1_release_replay.json`; scripts in `replay/`, `python -I`, real source snapshots and real directories read from AWS, nothing written)

| firm | built runner, previous = served | built runner, previous = last accounted build (`--previous-key`) | built refresh on that landing | live refresh (`RbpsijC2...`) |
|---|---|---|---|---|
| inflection | carried 0 keys, landed 294, no marked entry | carried 1 key, landed 295, entry in the landed directory | READY (`REFRESH_COMPLETED_WITH_ADDITIONS`), `terminated_count` 1 | REFRESH_FAILED |
| cottonwood | carried 0 keys, landed 269 | carried 1 key (2 entries), landed 271 | READY (`REFRESH_COMPLETED_WITH_ADDITIONS`), `terminated_count` 1 | REFRESH_FAILED |

- Inflection's fire dated 2026-10-09 (read through the built refresh on the real bucket state): previous state FOUND (294 entries, from the served directory), 0 false additions, READY, `terminated_count` 0 on the unseeded served directory and 1 once seeded.
- Negative arm (the dropped key back in the SOURCE only): the runner carries nothing (held_in_source 1) and the refresh is REFRESH_FAILED at both firms for a 2026-10-08 fire (row S4 records what it is for 2026-10-09 at inflection).
- 49financial: NOT replayed -- the source principal `irpt-49f-directory-read-role` is AccessDenied to this seat (row S5). Its source keys were proven on a constructed frame, and the runner guards that computation (unreadable keys cannot stale or empty the directory).

## Branch A (released)

1. **The two artifacts land** (refresh zip; runner bundle). Effect on the served bytes: none by itself. The next scheduled runner run lands a directory that now states `source_client_ids` (about +7 percent of bytes) and carries from the served directory,
   which has nothing to carry at either firm; inflection from a fire dated 2026-10-09 stops reading false additions. Read on that unseeded landing (replay arm `unseeded_landing_*`): cottonwood READY with `terminated_count` 1 by the refresh's own in-memory carry at both fire dates, inflection READY with `terminated_count` 1 for a driven fire dated
   2026-10-08 and 0 for a fire dated 2026-10-09 (its previous state is then the served directory); in every case the entry is still NOT in the served directory (`carried_in_landed` false).
2. **The seeding run (needs a ruling; row S1).** One runner run per firm on the runner host, after the bundle is uploaded, not concurrent with a scheduled run:
   `python3 $R/directory_runner.py --firms inflection --upload --previous-key investor-reporting/directory/2026-09-25/directory.json` and the same for cottonwood with `.../2026-10-05/directory.json`
   (the two keys are the last accounted-completion builds, read with the live `last_manifest`; both exist, versioned). BLAST RADIUS per firm: the dated `directory.json` of the date the runner selects (today `2026-10-08` at inflection and `2026-10-07` at cottonwood, which OVERWRITES the existing key; if the
   source frontier has moved by then it is a NEW dated key) and `latest.json`. Four objects in two buckets, nothing else. Each landing adds the carried entry marked TERMINATED and `source_client_ids`; every other entry is the same build. After it, every later scheduled run carries the entry forward from the served directory
   with its first `source_removed_on`. Rollback per key by S3 version (live, re-read at packet time 2026-10-09T01:27Z): inflection `latest.json` `IYqf.x8WewTTcvKkxAzng.pnzpluzixY`, `2026-10-08/directory.json` `qYXlj1pZA2qavf2ZJb.hLGX6YGQ5d3av`;
   cottonwood `latest.json` `xWWAVr3R60LNikXNfX450gx7LHfiXWFW`, `2026-10-07/directory.json` `2c0mqQRRHGyS5e2lqj1Usl5Un_0550Gs`. The signed half must cover BOTH sub-branches (same-date overwrite and new-date key), or it is not signed.

## Branch B (rolled back)

- `irpt-directory-refresh`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-refresh.zip` version **`Ntv3Br2YU3utvESdPFCiTMkVVatmyzxY`** (43,778 bytes, written 2026-10-08T23:00:22Z), the zip whose `CodeSha256` is
  **`RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=`**. Re-read live at packet time: `get-function-configuration` CodeSha256 unchanged, LastModified 2026-10-08T23:05:45Z; the version is still the latest. Through the Terraform deploy path, never a console edit.
- Runner bundle: the live object version **`JITP9ecNeQyAnAmKo90oxqWyFemEqVaI`** (ETag `7de9bbd51be6919a1ee2beb9f69a8860`, 108,774 bytes, 2026-10-07T18:33:12Z); roll back by re-minting from the base commit's `directory_runner.py` (blob sha256 prefix `21147de26795`) or copying that version back over the key.
  The runner has no other state; the next SSM run fetches whatever the key holds.
- Seeded keys (if step 2 ran): restore the four S3 versions above, `latest.json` last. A rolled-back runner no longer carries, so a restored directory stays restored.
- No route, IAM, schedule or env change to revert.

## The replay arm for the applier (rerun step 4 before the ledger)

Against the artifacts actually in play: extract the zip to be uploaded and the bundle to be uploaded into empty directories, and the LIVE zip (`RbpsijC2...`) into a third; then, from the repo root with AWS reads and a scratch directory OUTSIDE the worktree:
`python -I replay/replay_refresh.py prev <built_zip_dir> <scratch>`; `python -I replay/replay_runner.py <bundle_dir> <scratch> <fire date>`; `python -I replay/replay_refresh.py run built <built_zip_dir> <scratch> <scratch>/refresh_built.json`;
`python -I replay/replay_refresh.py run live <live_zip_dir> <scratch> <scratch>/refresh_live.json`; `python -I replay/compose_replay.py <scratch> <pin> <out.json> <zip sha b64> <bundle sha> <live sha b64>`.
Stop the apply if any of: the `seeded` arm is not READY with `terminated_count` 1 and `carried_in_landed` true at BOTH firms; the live arm is not REFRESH_FAILED; the negative arm is not REFRESH_FAILED at both firms (2026-10-08 fire) with `carried_in_landed` false;
inflection's `fire_20261009` is not `previous_found` true and `false_additions` 0. Delete the scratch directory afterwards (it holds client entries).

## The after-read

A driven refresh READY at all 3 firms, read at each manifest's own `as_of_business_date` (`_refresh/<date>/manifest.json`, `delta.terminated_count`): `terminated_count` 1 at inflection and 1 at cottonwood, 0 at 49financial; the served `directory.json` of inflection and cottonwood each carries the entry
with `termination.indicator` TERMINATED. **Only after Branch A step 2.** Without it the refresh's in-memory carry can read `terminated_count` 1 (cottonwood always; inflection for a driven fire dated 2026-10-08) while the entry is absent from the served directory at both firms, so the last clause of the after-read fails.
49financial: the first landing with the new bundle must be read for `source_client_ids` present or its error type recorded (`carried_forward` in the dated directory.json), because its path was not replayed.

## Rows and the deadline

Rows: `IRPT_BCKEND-D2-W189-S1` (BLOCKING, ARMED: the served directory already lost the entry; the seeding run), `-S2` (a test pinned the old behaviour; changed on purpose), `-S3` (BLOCKING, ARMED: AC2's whole-suite clause meets a red live holdings guard), `-S4` (ARMED: the runner lands a build fault and the verdict
cannot gate it), `-S5` (size +7 percent; 49financial unreplayed; first landing of a new firm refused).
Deadline: cottonwood's served directory (as_of 2026-10-07) goes OVER_AGE on 2026-10-12, inflection's (2026-10-08) on 2026-10-13. The release is live by Friday 2026-10-09's close only if the applier has this packet's two halves signed today.
