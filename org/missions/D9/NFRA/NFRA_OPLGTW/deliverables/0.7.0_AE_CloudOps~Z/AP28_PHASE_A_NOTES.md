# OG-ap-28 Phase A -- state at the STOP (0.7.0_AE_CloudOps~Z, 2026-10-16 ~16:50Z)

GO msg 35122: trunk_sha `066649b10fd44946faf7c28cf34fffe140344729`, mcportal_sha `59e802a4185a62129bf28ebb4df6eda9b70e03ff`. Order read at `06b2cc85eb` (A1 included).

## Step 1 -- the live ref (read, not assumed)
- `services.opal-gateway.deployed_commit` at HEAD = `d14445961dd6d04275ca8186372a4df4c4fcc5cc`; the S3 `git-ref` of `opal-gateway-latest.tar.gz` = the same.
- Catalog blob at trunk_sha: `b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3` (the value the GO names).
- mcportal: `59e802a418` present, origin DEV holds it (ls-remote), the live pin `c66ca82952` is its ancestor.
- `iam get-role gateway-49f-blackdiamond-live-read-role` resolves.
- NOT DONE in this Phase A: the SSM md5 read of the host against the live ref, the `MUSE_CLIENT_ID` names-only read and `tools_list_before`. They wait on the release being cut (they are Phase B's pre-act reads and AC2's inputs); a host read adds nothing to a release that cannot be committed.

## Step 2 -- the re-cut (C:/tmp/og-rel-batch2, branch rel-nfra-oplgtw-batch2 at the live ref; nothing committed on it)
- Attribution (`ap28_attr.py` -> `ap28_attr.json`): 21 candidate app files; for the 17 taken app files (the 16 modules plus catalog_gate) every live-to-trunk hunk is attributed to OG-en-4, 5, 6, 8, 9, 10 or 12 (0 unattributable); `client_adapter_eclipse.py`, `access_state.py`, `tier.py` and `portal_index` show 0 hunks; `tools.py` has 4 hunks no named order wrote and is NOT taken.
- Seams (`ap28_seams.py` -> `.out`/`.json`): 66 distinct seams over 169 importer edges; 6 edges print STOP-class and each was checked, not waved through:
  - `data_entitlement.py`, `tests/test_data_entitlement_guard.py` and `tests/test_og_en8.py` -> `tools.py`: AST of live and trunk equal modulo top-level order (171 of 171 nodes, 0 differing); the 4 hunks only move an import line and one function.
  - `tests/test_og_hv1.py` and `tests/test_query_v0_tool.py` -> `destructive_ops.py`: one line moves inside the `SAFE_TOOLS` frozenset; same elements.
  - `server.py` -> `yearinreview_view.py`: the import and the three names it uses exist identically at the live ref; the differing `_allowed` is untouched by this release.
- Take (`ap28_take.py`): 49 files whole from trunk (17 app/ref incl. the catalog whole, 32 tests), 9 named tests do not exist at trunk (listed in `ap28_take.json`), `deploy-to-ec2.sh` from the LIVE script with the one seventh key, the manifest with `mcportal_commit` the only changed line.
- Tests (`ap28_tests.out`): 169 run, 167 pass, 2 fail identically at the live ref (carried by name).
- Host-shape import check (`ap28_hostshape.py` -> `.json`): 18 of 18 modules import in a fresh interpreter with 0 reads, with and without `lib/opal_naming.py`; `server` needs the host `.env` at import (also true at the live ref) and imports under the tests' env fixtures.

## The STOP -- row NFRA_OPLGTW-Z-S301
The commit-time naming gate (ENFORCE) REFUSES 16 catalog literals. A probe branch (`rel-nfra-oplgtw-batch2-probe`, prelude commit `191eedf892` carrying the two registry files at trunk bytes) clears 12 and leaves 4 (`blackdiamond/49f-live/silver/<table>/`, S3Key, 'K3: 49f-live is not a tier'). No gate was overridden; no release commit, release_sha, `ap28_release.json`, ask or AC1 run exists.

## After A2 (msg 35140, ~17:05Z) -- second STOP, row NFRA_OPLGTW-Z-S303
- Prelude commit 1 (the two registry files, byte-equal to trunk, `GIT_COMMIT_AUTHOR_OVERRIDE=PLATFORM_LOGIC_DOCS`): committed on `rel-nfra-oplgtw-batch2`, `46be947ba9`.
- The four `blackdiamond_live_<t>.yaml` entry files (byte-equal to trunk), as one commit with the registry and as a second commit: REFUSED, 12 graded (per file: line 2 `silver/<t>/`, line 3 `blackdiamond/49f-live/silver/<t>/`, line 48 `49financial`). They are NEW at this base; MI's trunk commit was a pure rename of content already committed.
- The release commit on top of prelude 1: `CATALOG-EXEMPT admitted=12 refused=4`; the 4 are `DATA_CATALOG.yaml` `blackdiamond/49f-live/silver/{allocations,fees,transactions,unrealized}/` (K3, '49f-live' is not a tier). Exit 1.
- Nothing overridden beyond the two audited lane escapes the order names. No release_sha, ask or AC1 run. The probe branch `rel-nfra-oplgtw-batch2-probe` (`191eedf892`) is not the release.

## The deferred step 1 and 3 reads (COO msg 35151, ~17:30Z) -- done
- Host md5 walk against the live ref (`ap28_host_md5.py` -> `.json`, SSM): 139 expected files (git blobs of `d14445961d` over app, deploy, lib, requirements, allowlist), 141 on the host (the two staged `app/refs` files, both equal to trunk's blobs): 139 equal, 0 differ, 0 missing, 0 unexplained extra. Dashboard excluded by grain.
- `.env` names only: 64 keys, `MUSE_CLIENT_ID` is not a key, `BLACKDIAMOND49FLIVE_READER_ROLE_ARN` not yet a key (65 after the release); 9 keys end in `_READER_ROLE_ARN` (the order's "7" counts the six vendor keys plus the new one).
- `tools_list_before` (`ap28_toolslist.py` -> `.json`): registry 103; `tools/list` to a master_admin stand-in 103; health 200.
- IAM, simulated one resource per call on `gateway-49f-blackdiamond-live-read-role`: GetObject allowed on the four live prefixes, ListBucket with the prefix allowed, controls (`bronze/`, `silver_legacy/`) explicitDeny; bucket `opal-data-bd` exists.
- `NEVER_WIDEN_ASK_OG-ap-28.md` drafted with A1-A3 text; `release_sha`, the final `trunk_sha`, the four gate lines and the signatures are blank. Nothing committed on the release branch.
