# OG-ap-32 Phase A (REDONE under A1 and A2) -- state at the STOP (0.7.0_AE_CloudOps~NFRA1, 2026-10-17 ~01:5xZ)

GO msg 35297 (trunk_sha `d2b95c10cff58e5295ede3926096d452a50e36c7`, OG-en-18 merged) and msg 35299 (A2, ruling on row Z-S336, option B). The first Phase A (release `11031f278d`, ask `82e211ff...`) is SUPERSEDED; its records are kept in git. Nothing deployed, nothing written to any bucket or table.

## Step 1 -- the live ref (read, not assumed)
- The live ref MOVED during Phase A: `services.opal-gateway.deployed_commit` and the S3 `git-ref` both read `319c9413a20895a63517c5ca1b9ced0f78a5573a` (AMGT_HARVST HVST-cc-7, `0.7.0_AE_CloudOps~SC1`, 2026-10-17T00:10:31Z); previous `4be300110e`. The commit is not in this repository. Row Z-S336 (BLOCKING), ruled option B by the issuer.
- Host md5 walk against `4be300110e` (`ap32b_host_md5.json`): 136 equal, 3 differ: `app/harvest_figures.py`, `app/harvest_identity.py`, `app/harvest_research.py`. Each of the three is byte-equal to trunk's blob (md5 read over SSM). `.env` 65 key names, no `MUSE_CLIENT_ID`; `tools/list` 103; health 200; `gateway-49f-blackdiamond-live-read-role` resolves.
- `comp-schedule --drift`: NOT run in Phase A (the order says "at the act").

## Step 2 -- the re-cut (`C:/tmp/og-rel-batch4`, branch `rel-nfra-oplgtw-batch4` at 4be300110e)
- The superseded release stays on `rel-nfra-oplgtw-batch4-superseded` (11031f278d).
- Catalog blob at trunk `2cbe275d03c9a5af85afefabc604e26b71e9be12`, md5 `bdfee515ec348f0ea2ee716eff5acba5`; equal in the release tree.
- Attribution: adapter 18 hunks, 17 attributed (OG-en-18, 17, 15, 13), 1 unattributable BY LINE: a removed `rows, partition_rows, excluded_total = [], 0, 0` that exists once in the base (line 289) and once in trunk (line 330): a moved identical line (diff alignment), no content change by any other order. Placed, not waved through.
- Seams: 4 modules over 10 edges, 0 STOP. Take: 9 paths (adapter, three harvest files, catalog, tests en17, en18, en15, cl2; `test_og_en13` equals the base so it is not in the diff).
- Tests: touched files 21 passed forward and reversed; whole suite release 73 failed / 1027 passed, base 74 / 1020; failing only in the release 0.
- Release commit `b124377b41caf5665b999378fd0ca08ad8a1fb7d`, parent `4be300110e`. Naming gate: `WARN 266 graded`, 0 REFUSE. The overlay (270 uncommitted paths incl. the 241-file function map and the trunk halt gate) is in the release tree.
- Host md5 walk against the release blobs (`ap32_host_md5_release.json`): 137 equal, 2 differ (the adapter and the catalog: this release's own files), 0 missing, 0 extra.
- First page of the candidate code on the host, no deploy (`ap32_firstpage.py` -> `.json`): transactions 29.34 s, 30 of 334 partitions, cursor returned, host memory 38.2 / peak 64.3 / 58.5 percent; fees 12.39 s, 30 of 394, cursor, 58.5 / 58.5 / 57.9. A second call during a first read: no partitions read, `retry_after_seconds` 0.5 (patched wait), 1.43 s.

## State left for Phase B
- `ap32_release.json`: base_sha 4be300110e, declared_base_sha 319c9413a2, release_sha b124377b41, trunk_sha d2b95c10cf. Phase B deploys with `DEPLOY_BASE_REF=319c9413a2...`, re-reads the live ref first (if it moved again: STOP), restores the overlay (`ap32_overlay_restore.py`) and lays back only the trunk `halt-gate-check.sh` for the wrapper.
- `C:/tmp/og-live-4be3`: pristine detached tree at the base (baseline test run); removable.
- Rollback: this release's tree with the adapter and catalog at their base blobs, proven by the host md5 walk; byte reference `opal-gateway-319c9413a2.tar.gz` in S3. NOT the base `4be300110e`.
