# OG-ap-32 Phase A -- state at the STOP (0.7.0_AE_CloudOps~NFRA1, 2026-10-17 ~00:2xZ)

GO msg 35294: trunk_sha `2161dab1031bb7378666e6a239d563b5e53d6c86`. No deploy, no apply, nothing written to any bucket or table.

## Step 1 -- the live ref (read, not assumed)
- `services.opal-gateway.deployed_commit` at HEAD = `4be300110ec912ac8c11a1663403e41eea45117c`; the S3 `git-ref` of `opal-gateway-latest.tar.gz` = the same; host md5 walk (SSM, `ap32_host_md5.json`): 139 of 139 equal, 0 differ, 0 missing, 0 extra.
- `.env` 65 key names, `MUSE_CLIENT_ID` not a key; `tools/list` 103 (registry 103), health 200 (`ap32_toolslist.json`); `iam get-role gateway-49f-blackdiamond-live-read-role` resolves.
- Host memory at the read: 300 MB used of 1846 MB (25.7 percent as 1 - available/total), no swap, 2 vCPU.
- `comp-schedule --drift`: NOT run in Phase A (the order says "at the act"); a Phase B pre-act read.

## Step 2 -- the re-cut (`C:/tmp/og-rel-batch4`, branch `rel-nfra-oplgtw-batch4`, at the live ref)
- Catalog blob at trunk: `git rev-parse 2161dab103:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` prints `2cbe275d03c9a5af85afefabc604e26b71e9be12` (as the order requires); md5 `bdfee515ec348f0ea2ee716eff5acba5`.
- Attribution (`ap32_attr.py`): `app/client_adapter_bd49f.py`, 14 hunks, 14 attributed to OG-en-17, OG-en-15, OG-en-13; 0 unattributable.
- Seams (`ap32_seams.py`): 2 distinct modules over 4 edges, 0 STOP-class.
- Take (`ap32_take.py`): 5 files whole from trunk (1 app, the catalog, 3 tests); all 5 differ from the live ref.
- Tests: touched files 15 passed forward and reversed; whole suite release 74 failed / 1023 passed, live ref 74 failed / 1020 passed, failing only in the release 0.
- Host-shape import check: 6 of 7 import with 0 reads.
- HOST MEMORY MEASURE (`ap32_memplan.py`, read-only, 8 partitions, abort at 60 percent): 7.8 MB per transactions partition and 9.2 MB per fees partition retained; projection for a 60-partition page +469 and +551 MB (about 55 and 59 percent host used); two pages in flight about 85 to 100 percent; no process-wide limit in the code.

## The naming gate
- First release-commit attempt REFUSED: `function-map folder missing: C:\tmp\og-rel-batch4\infra/aws/lambda/ci/function-map/` (the trunk naming gate reads it; it exists only at trunk, 241 files). Nothing overridden.
- The overlay now holds 270 paths from trunk (255 added, 15 modified; `ap32_overlay.json`) including the folder and the trunk `halt-gate-check.sh`; second attempt under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL`: `NAMING-GATE: WARN 169 graded`, 0 REFUSE. No registry file in the diff, so no prelude commit.
- Release commit `11031f278d092e5c79ec7d865891024c967160d8`, parent `4be300110e`, 5 files.

## State left for Phase B
- The overlay (270 uncommitted paths) sits in `C:/tmp/og-rel-batch4`; Phase B restores them to the live ref's bytes (`ap32_overlay_restore.py`), then lays ONLY the trunk `halt-gate-check.sh` back for the wrapper, as at OG-ap-31.
- `C:/tmp/og-live-4be3` is a pristine detached tree at the live ref (baseline test run); removable.
- Rollback: redeploy `4be300110e`.
