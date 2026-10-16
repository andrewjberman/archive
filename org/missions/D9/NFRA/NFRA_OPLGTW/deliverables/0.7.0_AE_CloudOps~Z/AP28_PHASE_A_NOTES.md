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

## A3 GO (msg 35164, ~17:31Z) -- Phase A finished
- New `trunk_sha` `858e9275589e51f0f15d8c55462125c7152f621c` (holds the CRO's `ca679b6560`); catalog blob still `b81c48aa3c`. Between the old and the new trunk only four files changed: `app/harvest_research.py`, its test, `legacy_addresses.json` (+40 lines) and `lib/research/aifill/contract.py`; the take is byte-unchanged.
- Seam rerun (`ap28_seams_nt.out`): one NEW STOP-class edge, `tests/test_og_gt4.py` -> `app/harvest_research.py` (trunk's CC-2 change, not in the take). Satisfied by the base file: `test_og_gt4` passes against it (`ap28_tests.out`).
- Branch recreated from the live ref (the old one kept as `rel-nfra-oplgtw-batch2-prelude-old`; the probe branch kept as `...-probe`). Prelude `2dc919cf26` (the two registry files at the NEW bytes, `PLATFORM_LOGIC_DOCS`), release `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` (`CLOUD_OPS_OR_ETL`): **exit 0, `NAMING-GATE: WARN 46 graded`, 0 REFUSE, `CATALOG-EXEMPT admitted=12 refused=0`**. The four entry files are not carried (A3).
- `ap28_release.json` written with full shas; the ask finalized with `release_sha` and the gate lines (4 RAISE-EXISTING for the `49f-live` prefixes, 8 RAISE for the `silver_legacy` prefixes, both printed as WARN-class).
- Release tree state after the commit: the overlay (30 gate-input files laid from trunk, uncommitted) and the untracked test support stay in `C:/tmp/og-rel-batch2`; Phase B restores the overlay's non-bundle files before the deploy tree's clean check.

## PHASE B (GO msg 35174, 2026-10-16 ~17:49Z) -- done except arm e4
- Step 1 re-reads at the GO: live ref `d14445961d` (manifest and S3 git-ref), host `.env` 64 keys, `MUSE_CLIENT_ID` absent, the seventh key absent, host md5 139 of 139 (`ap28_host_md5_phaseb.json`), role resolves, `nfra-oplgtw-grants-ap29` CLOSED. One stale `gateway-release-p21` sentinel exists in an old worktree's HEAD (`wk-r18-45b`); the p21 ledger is CLOSED in the main tree (2026-10-16T01:18:45Z), so it is not a release in flight.
- Ledger `nfra-oplgtw-gateway-release-batch2` opened first (entry AND sentinel committed by the tool). ONE deploy, 17:56:00Z, `safe-ec2-deploy.sh` from `C:/tmp/og-rel-batch2`, `DEPLOY_BASE_REF=d14445961d`, no HALT_OVERRIDE: base guard EQUAL at both checkpoints, DEPLOYMENT COMPLETE, rc 0 (`ap28_deploy.out`). The tree's HEAD moved to the wrapper's manifest commit `e99939f5b0` above `bf9d23b518`.
- Read-back against the triggers (C6): health 200, host md5 139 of 139 vs the release blobs (`ap28_host_md5_after.json`), `.env` 65 keys with the seventh key and no `MUSE_CLIENT_ID`, registry 103, `tools/list` 103 before and after (same measure), 27 of 27 tools (`ap28_served27.json`). No trigger fired; no redeploy.
- The arms (`ap28_arms.json`; the harness is read-only and was run 9 times in total while I corrected its OWN defects -- a wrapper that did not accept a keyword, a wrong tool-lookup, the account choice -- never the host or the release; the earlier outputs are not committed): e12, e5, e6, e8, e9, e10 TRUE; **e4 FALSE** (row Z-S305). `CODE2_SERVED.json` is assembled by `ap28_served_build.py` from the four records.
- e12: 34, 2, 7 and 2 rows on the four `-live` tools, every first source key in `opal-data-bd` (catalog row), `as_of` the newest dated file, the assumed role `gateway-49f-blackdiamond-live-read-role` on all four (the allocation tool also reads the assets-copy profile table through the legacy 49f role, as designed); an unprofiled non-admin refused with 0 S3 client requests.
- e10 is in-process (a real bearer needs a table write the order forbids); its limits are stated in the record.
- Standing clauses (shared tree): `EC2_MANIFEST.json` deployed_commit `d14445961d` -> `bf9d23b518`, mcportal pin, 3 of 10 checksums moved (host-controlled), release_note; runbook 7.2 names the new release.

## AC3 evidence (A5, COO msg 35189, ~18:50Z) -- captured, NOT committed
- File: `W/CVO_AC3_BODIES_OG-ap-28.json` (29897 bytes, sha256 `0db2c9b8be28aeac23a6cea7c6dae9cf659f7617f0ab12545a827dd198e59fe6`, read 2026-10-16 ~18:5xZ from the live release `bf9d23b518`). It is untracked and excluded locally (`.git/info/exclude`), never `git add`ed: it holds client positions, so the CVO reads it on this box.
- Per-capture rows: 49F BD live holdings 34, transactions 2, allocation 7, fees 2 (one account, shown `****<last4>`); an EMPTY news window 0 rows with `coverage_floor`; a chatter answer 10 rows with `trading_days_behind_t1`.
- Masking was minimal: numbers, tickers, CUSIPs, security ids and dates are as served. Withheld: the account's vendor id (the ref is `****<last4>`), 7 `portfolio_name` fields (a registered person name), and any e-mail, phone or person-name-shaped value (0 found besides those). A search of the final file for the name tokens of the first capture finds none.
- Two host runs, disclosed: the first capture carried the allocation's `portfolio_name` (a person name) because my masking rule did not name that key; it was local and uncommitted, and the second run, with the key and a name-shape rule added, overwrote it. Read-only both times; no retry loop beyond that fix.
- Script: `ap28_ac3_capture.py` (committed; it contains no data).

## Evidence files committed (COO msg 35224, CTO msg 35222, ~19:2xZ)
- `ap28_arms_run1.json` .. `run8.json` (the eight earlier outputs of the read-only arms harness, kept so the trail of its OWN defects is on record; the ninth is `ap28_arms.json`) and `ap28_served27.json.raw.txt` (the raw output of the 27-tool served harness behind `ap28_served27.json`). Scanned first, counts only: 0 e-mail addresses, 0 phone numbers, 0 vendor account ids, 0 name-shaped values in all nine; one 8-digit run in `run4`, an SSM command-id UUID segment, not client data. This supersedes the earlier sentence that the earlier outputs are not committed. `CVO_AC3_BODIES_OG-ap-28.json` is untouched, untracked and git-excluded.
