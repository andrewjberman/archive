# OG-ap-31 Phase A -- state at the STOP (0.7.0_AE_CloudOps~NFRA1, 2026-10-16 ~21:3xZ)

GO msg 35256: trunk_sha `de8078d5453795eb7d6e4c1507882f247d7be8e9`. Order read whole at HEAD. No deploy, no apply, nothing written to any bucket or table.

## Step 1 -- the live ref (read, not assumed)
- `services.opal-gateway.deployed_commit` at HEAD = `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` (the S3 ref and the host agree).
- Host md5 walk (SSM, `ap31_host_md5.json`): 139 expected files (git blobs of the live ref), 141 on the host (the two staged `app/refs` files, both equal to trunk blobs): 139 equal, 0 differ, 0 missing, 0 unexplained extra. Dashboard excluded by grain.
- `.env` names only: 65 keys, `MUSE_CLIENT_ID` is not a key.
- `tools_list_before` (`ap31_toolslist.json`): registry 103; `tools/list` to a master_admin stand-in 103; `/health` 200.
- `iam get-role gateway-49f-blackdiamond-live-read-role` resolves.
- Extra read (booleans and a count only, `ap31_roster.json`): `MASTER_ADMIN_EMAILS` holds 1 entry, `andrew@opalinvest.com`; the other two roster addresses the order names are not members. Row Z-S322.
- `comp-schedule --drift`: NOT run in Phase A (the order says "at the act"); it is a Phase B pre-act read.

## Step 2 -- the re-cut (`C:/tmp/og-rel-batch3`, branch `rel-nfra-oplgtw-batch3`, at the live ref)
- Attribution (`ap31_attr.py` -> `.json`): 4 app files, 44 hunks, 44 attributed to OG-en-13 / OG-en-15 / OG-en-14 / MX-c-24, 0 unattributable.
- Seams (`ap31_seams.py` -> `.out`/`.json`): 51 distinct seams over 84 importer edges; 4 STOP-class edges, each checked by imported name (`ap31_seamcheck.py`): 0 of 7 names unsatisfied at the base.
- Take (`ap31_take.py`): 17 files whole from trunk (4 app, 13 tests); 12 differ from the live ref.
- Tests (`ap31_tests.out`): the 13 files, 103 passed forward and 103 passed reversed. Whole suite: release 74 failed / 1020 passed; live ref 78 failed / 978 passed; failing only in the release: 0.
- Host-shape import check (`ap31_hostshape.json`): 6 of 7 import with 0 reads, with and without `lib/opal_naming.py`; `server` needs the host `.env` at import (also true at the live ref).

## The naming gate
- First release-commit attempt REFUSED: `NAMING ERROR ... KeyError: 'interval_form'` (the live ref's `lib/opal_naming.py` and `org/standards/NAMING_SCHEMA.json` are an inconsistent pair). Nothing overridden.
- 27 gate-input paths laid from trunk as an UNCOMMITTED overlay (`ap31_overlay.json`, the OG-ap-28 precedent); second attempt under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL`: `NAMING-GATE: PASS 0 graded`. No registry file in the diff, so no prelude commit.
- Release commit `4be300110ec912ac8c11a1663403e41eea45117c`, parent `bf9d23b518`, 12 files.

## State left for Phase B
- The overlay (27 uncommitted paths) sits in `C:/tmp/og-rel-batch3`; Phase B restores them to the live ref's bytes before the deploy tree's clean check.
- `C:/tmp/og-live-bf9d` is a pristine detached tree at the live ref (baseline test run); removable.
- Rollback: redeploy the base `bf9d23b518`.
