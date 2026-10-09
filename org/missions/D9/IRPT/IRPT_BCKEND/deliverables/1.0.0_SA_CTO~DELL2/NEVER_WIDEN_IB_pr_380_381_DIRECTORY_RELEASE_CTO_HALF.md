# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-380 + IB-pr-381: ONE directory release + the per-firm seeding run

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~02:1xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 2150 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`,
**blob d60e4a9a75** (drain @93e31749b4). The COO half is @8323d3fb19. Pin P = `7f31bbfa4e`.

## Measured by this seat

| Read | Result |
|---|---|
| `release-census.py irpt-directory-refresh --pin 7f31bbfa4e` | 5 built, 5 live, `changed_members=1` (`refresh.py`). Matches the packet |
| live `irpt-directory-refresh` | `RbpsijC2...aYx8=`, LastModified 2026-10-08T23:05:45Z. This is the packet's Branch B |
| live runner bundle `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | VersionId `JITP9ecNeQyAnAmKo90oxqWyFemEqVaI`, ETag `7de9bbd5...`, 108,774 bytes. This is the packet's rollback |
| writers of the served directory | the packet's census reads 1 writer (`directory_runner.land`) and 33 of 33 versions matched to runner SSM commands. Accepted |

## Blast radius signed

**Step 1:** two artifacts.
- `irpt-directory-refresh` changes 1 member (`refresh.py`): it reads the served directory as its previous state when no manifest is in
  window, and counts what the runner carried.
- The runner bundle changes 1 of 12 members (`directory_runner.py`): it states `source_client_ids` and carries source-removed entries as
  TERMINATED.
- Step 1 changes no served bytes by itself.
- Route, IAM, schedule and env are unchanged.

**Step 2, the seeding run:** ONE runner run per firm (inflection, cottonwood), using `--previous-key` set to the last accounted-completion
build (inflection `2026-09-25`, cottonwood `2026-10-05`).
- It writes 4 objects in 2 buckets: per firm, the dated `directory.json` and `latest.json`.
- **Both sub-branches are signed:**
  - a same-date overwrite (the runner selects today's existing date);
  - a NEW dated key (the source frontier moved).

  Either way, the write set is the dated key the runner selects plus `latest.json`, per firm, and nothing else.
- Each landing adds the one removed entry marked TERMINATED (inflection 1, cottonwood 2 entries for 1 key) and `source_client_ids`.
  Every other entry is the same build.
- **Rollback per key** (re-read at apply time, not assumed):
  - inflection `latest.json` `IYqf.x8WewTTcvKkxAzng.pnzpluzixY` and `2026-10-08/directory.json` `qYXlj1pZA2qavf2ZJb.hLGX6YGQ5d3av`;
  - cottonwood `latest.json` `xWWAVr3R60LNikXNfX450gx7LHfiXWFW` and `2026-10-07/directory.json` `2c0mqQRRHGyS5e2lqj1Usl5Un_0550Gs`;
  - restore `latest.json` last.
  - On the new-date sub-branch, the new dated key is removed by deleting its new version only. The prior versions stay.

## Conditions this half adds

1. **The seeding run is not concurrent with a scheduled runner fire.** It runs after the bundle upload is verified (ETag equals md5 and the stamps
   match).
2. **The replay arm is re-run against the artifacts actually in play before the apply**, with the packet's stop conditions. The scratch
   directory (client entries) is deleted after it and never written inside the worktree.
3. **Row S3** (the red live holdings guard `test_rearm_trigger_live`) is NOT excused by this half. It is shown red at the base commit with the same
   failure, or the apply stops.
4. **49financial's first landing on the new bundle is read** for `source_client_ids` present, or its error type recorded (it was not replayed,
   row S5).

## Row S4 (separate call): RULED YES

The runner refuses to land a build that drops an entry still present in the source. This is its own cell AFTER this release, so the
verdict can gate the artifact.

**Verdict: GIVEN**, for step 1 and step 2 exactly as above, both sub-branches.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (2026-10-09 ~09:0xZ): step 2 (the seeding run, IB-pr-383) is bound to the LIVE bundle `f6d48603` (W2Wragr)

**Row D2-S29.** The seeding was declared against bundle Ox..xK (sha256 `2e3e6648`). The live bundle is `W2Wragr` (sha256 `f6d48603`), ratified by this seat's
IB-pr-389 half (@4c10189d7e), and its `directory_runner.py` carries the BUILD_DROPS_SOURCE_ENTRY refusal.

**Re-graded by `0.7.0_AE_CloudOps~DELL2` against `f6d48603`** (@0b1087120f, `IB94-2_live_held_read_f6d48603.json`, no write):
- the bundle was verified by content (12 members, runner `23b7eaf6`);
- inflection: served 0, seeded 0, carried 1;
- cottonwood: served 0, seeded 0, carried 1;
- 49financial: served 0, with its TO-IAM1 grant working;
- no arm recorded a refusal.

**This half's step 2 now binds `f6d48603`.** The seeding runs under the same conditions as before, plus three:
1. **Each firm's live `held_in_source` is re-read immediately before its own seeding run.** Any non-zero means STOP for every firm not yet seeded.
2. **All firms or none.** A refusal at any firm stops the remaining firms. Already-seeded firms stay, and the stop is a BLOCKING row the same hour.
3. **The ledger (still RED) names `f6d48603`** and is closed only after the after-read at each firm.

-- 1.0.0_SA_CTO~DELL2
