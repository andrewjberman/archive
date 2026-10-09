# Never-widen sign-off packet -- IB-pr-380: irpt-directory-refresh carries a source-removed entry forward TERMINATED

Prepared by 0.9.0_WK_IRPT_BCKEND~188 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed or applied: one BUILD_ONLY run from a clean tree, one offline replay,
AWS reads only. Census file: `IB92-1_refresh_census.json`. Replay file: `IB92-1_terminated_replay.json`. Model: `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-370.md` (~178).

**READ THIS FIRST (rows D2-W188-S1 and D2-W188-S2, both BLOCKING, ARMED).** The function released here implements the ruling and is proven on both real cases, but
(S1) it cannot make inflection or cottonwood READY in production until the directory runner states the source snapshot (`source_client_ids`) and carries the entry into the landed
`directory.json`, and (S2) a scheduled fire dated 2026-10-09 or later cannot see inflection's previous READY build at all. Applying this release alone does not change the live outcome.
Details under "Preconditions of the after-read".

## The pin and the build

- **Release pin P: `8953eccfcaa4d42b2e9968a1da55a1a649e46505`** (branch `wk-IRPT_BCKEND-188`). It follows `4864aee5e19850b9a64036706b261df9a074f26b` (first cut of the same fix; the real-case
  replay of that cut printed `terminated_count` 2 for cottonwood's ONE removed key because that key heads two entries, so the count moved to keys at P). Changed file in the function:
  `directory/refresh.py` only. Tests: `directory/tests/test_refresh_terminated.py` (not shipped).
- **Census at P** (`release-census.py irpt-directory-refresh --pin P`): built 5 members, live 5, `changed_members=1` -- `refresh.py` (built `70b4cce47817`, live `ed3d0c881890`), owned by P.
  `irpt-directory-search --pin P`: `changed_members=0` (24 of 24 identical). `lambda-source-map.json` is untouched (refresh.py is a `files[]` member of the source dir).
- **BUILD_ONLY from a clean tree at HEAD `3e5ffead16`** (porcelain 0 lines before and after; `refresh.py` in the zip is `70b4cce47817`, the blob P carries):
  `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-refresh` rc 0.
  **Built sha256 `xGc9a2m7MGwMEQxx5sVuiyz4qZjrR3TvYWrEpSGGtrg=`** (hex `c4673d6b69bb306c0c110c71e6c56e8b2cf8a998eb4774ef616ac4a52186b6b8`, 45896 bytes, 5 members).
  The kept `/tmp` zip was removed; nothing uploaded.

## The rule (CTO msg 1959, row D2-W187-S1) as built

- A client the previous build carried and the new build lacks is decided by the SOURCE SNAPSHOT THE BUILD READ (`source_client_ids`, the entry keys the source holds, in the key space
  `compute_delta` compares: `ids.client_id`, else `ids.relationship_id`), never by the build output.
- Absent from the build AND the source -> every entry of that key is carried forward into the new build marked `TERMINATED`, dated by the source snapshot that first lacked it
  (`source_removed_on`), and the build goes READY. A key still in the source, or a build that states no source (unknown is never read as absent), keeps the whole build REFRESH_FAILED, unchanged.
- An already-carried TERMINATED entry is carried again with its first `source_removed_on` and is not counted as new (`terminated_new` 0).
- `terminated_count` (keys carried) and `terminated_new` are in the manifest delta and in the Lambda log line `irpt-directory-refresh firm=<id> terminated_count=<n> terminated_new=<n> reason=<code>`;
  the handler's result row carries `terminated_count`. Reason codes are unchanged: a marking that moved ACTIVE to TERMINATED is the existing eligibility change.
- Row D2-W188-S3: the contract has no `source_removed_on` field, so the date is `termination.effective_date` plus a `capability_facts` marker; a carried entry validates against the schema.

## Real-case replay (`IB92-1_terminated_replay.json`, python `-I`, offline, fire date 2026-10-08)

Inputs read from AWS: the previous READY build named by the live zip's own `last_manifest` (inflection 2026-09-25, 292 entries; cottonwood 2026-10-05, 270 entries), the latest landed build
(`latest.json`: inflection 2026-10-08, 294 entries; cottonwood 2026-10-07, 269), and the source snapshot the build read, loaded with the runner's own source adapter and minted with the production
opaque function (inflection 1026 source keys; cottonwood 1081). Source check: the one dropped key per firm is in 0 of the latest snapshot's keys and in 1 of 1 at the previous build's snapshot
(positive control); every build key is in the source.

| firm | built zip | live zip | negative arm (dropped id back into the source only, built zip) |
|---|---|---|---|
| inflection | READY (`REFRESH_COMPLETED_WITH_ADDITIONS`), `terminated_count` 1 | REFRESH_FAILED | REFRESH_FAILED |
| cottonwood | READY (`REFRESH_COMPLETED_WITH_ADDITIONS`), `terminated_count` 1 | REFRESH_FAILED | REFRESH_FAILED |

Also recorded: a build stating no source also stays REFRESH_FAILED at both firms. Raw extracts stayed in scratch outside the worktree and were deleted; only counts and reason codes are committed.

## Writers of the served directory (read in code and Terraform)

1. `data/assets/scripts/gold/investor_reporting/directory_runner.py` (host, `--upload`): writes `investor-reporting/directory/<date>/directory.json` and `latest.json` -- the ONLY writer of the served directory.
2. `irpt-directory-refresh` (this function): writes `_refresh/<date>/manifest.json` only (`s3:PutObject` on `_refresh/*`); reads the artifact; it cannot write `directory.json`.
3. Readers: `irpt-directory-search` and the other directory readers read `latest.json` and the dated `directory.json`. 2 writers of the directory prefix in total, 1 of the artifact.

## Branch A (released)

- `irpt-directory-refresh` carries the rule. With today's landed artifact (no `source_client_ids`) every inflection and cottonwood refresh is REFRESH_FAILED exactly as before (fail closed): no outcome
  moves. 49financial (not replayed): its last driven refresh was READY with no disappeared key, a path the rule does not enter, so `terminated_count` is 0 and the outcome is unchanged. The search function is unchanged (0 changed members).
- Once the runner states the source snapshot and carries the entry into the landed artifact (row S1's disarm), the refresh goes READY with `terminated_count` 1 at inflection and cottonwood and readers
  see the entry marked TERMINATED.

## Branch B (rolled back)

- `irpt-directory-refresh`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-refresh.zip` version
  **`Ntv3Br2YU3utvESdPFCiTMkVVatmyzxY`** (43778 bytes = the live CodeSize, written 2026-10-08T23:00:22Z), the zip whose `CodeSha256` is **`RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=`**.
  Read live this session (`get-function-configuration`, LastModified 2026-10-08T23:05:45Z): unchanged. A new upload makes a newer version, so rollback is a redeploy of THAT version through the
  Terraform deploy path, never a console edit. No route, IAM, schedule or data change to revert.

## The replay arm for the applier (before the ledger)

Rerun step 3 against the zips actually in play: unzip the LIVE zip (`RbpsijC2...`) and the zip to be uploaded into two empty directories; run
`python -I extract_inputs.py <live_zip_dir> <scratch_out_dir> 2026-10-08` from the repo root (AWS reads; scratch OUTSIDE the worktree), then
`python -I replay_zip.py live <live_dir> <scratch_out_dir> live_run.json` and `python -I replay_zip.py built <built_dir> <scratch_out_dir> built_run.json`
(scripts in `replay/`). Stop the apply if any of: built is not READY with `terminated_count` 1 at BOTH firms; live is not REFRESH_FAILED; the negative arm is not REFRESH_FAILED; the unknown-source arm is not REFRESH_FAILED.
Delete the scratch directory afterwards (it holds client entries).

## Preconditions of the after-read, and the after-read

Preconditions (both ARMED rows): (S1) the runner emits `source_client_ids` and the previous build's TERMINATED/source-removed entries in the landed artifact; (S2) the fire compares against the last READY build --
use a driven refresh with event `business_date` 2026-10-08 (a scheduled fire dated 2026-10-09 or later reads inflection's previous state as None: the 2026-09-25 manifest is the 11th trading day back).

After-read: a driven refresh READY at all 3 firms, read at each manifest's own `as_of_business_date` (inflection and cottonwood from their `_refresh/<date>/manifest.json`, `delta.terminated_count`):
`terminated_count` 1 at inflection and 1 at cottonwood, 0 at 49financial; the served `directory.json` of inflection and cottonwood each carries the entry with `termination.indicator` TERMINATED. Without the preconditions
the driven refresh at inflection and cottonwood stays REFRESH_FAILED and the after-read cannot pass.

## Deadline

cottonwood's served directory (as_of 2026-10-07) goes OVER_AGE on 2026-10-12, inflection's (2026-10-08) on 2026-10-13. The refresh release is necessary and not sufficient; the runner cell of S1 is on the critical path.
