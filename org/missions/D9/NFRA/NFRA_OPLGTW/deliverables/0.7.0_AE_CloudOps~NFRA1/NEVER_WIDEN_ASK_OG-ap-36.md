# NEVER-WIDEN ASK -- `OG-ap-36` -- the round-41 fifth batched gateway release: the windowed client tools run off the event loop and convert only the account's rows, the served prefix is listed once per page, the deploy writes the release sha to the host

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-36.round-41-fifth-batched-release.md` with its amendment A1 (GO for the re-run: msg 35469).
Release: `release_sha` = `948e8b47cc626fe194383d04dfb6944edac1ae0b`, cut on the live ref `base_sha` = `9d5b7125571520b977401634a01935924f4c9787` (the `OG-ap-34` release), from `trunk_sha` = `caa31777489e84243b0f09dc02191132a7656b93`. Record: `ap36_release.json`. Release tree `C:/tmp/og-rel-batch6`, branch `rel-nfra-oplgtw-batch6`. Phase A is read-only on the estate: nothing was deployed or applied; the host measurements ran in scratch folders that were removed.
History: a first Phase A on trunk `58bb50256e` (release `e45922ef75`) STOPPED on two measurements (row `Z-S370`: the event loop starved up to 3.9 s during a page, limit 1 s; the four-page chain's median growth 27.7 MB, limit 20). `OG-en-23` is the repair; the limits were not relaxed; that record is kept as `MEM_GATE_OG-ap-36_run1_superseded.json` and this ask rests on the re-run only.

## 1. The diff, by file (`git diff 9d5b712557 948e8b47cc`: 8 files, 1043 insertions, 19 deletions)

- `app/tools.py`: `OG-en-21` (`client_get_transactions` and `client_get_fees` become `async` and run the read in a worker thread by `anyio.to_thread.run_sync`) and the POSITION move of `harvest_get_published_analysis` that `OG-ap-33` landed on trunk. 8 hunks, all attributed (`ap36_attr.json`): 4 to `OG-en-21`, 4 to the position move (the same lines leave one hunk and arrive in another). The name is imported once, defined and registered once; no live line is lost (the live lines absent from trunk's, as a multiset, are the 4 lines `OG-en-21` rewrote).
- `app/client_core.py` and `app/client_adapter_bd49f.py`: `OG-en-22` (`Ctx.partition_keys(prefix)` lists the served prefix once per call; `read_rows(..., key=None)`; the adapter takes the index once per call) and `OG-en-23` (`Ctx.read_account_rows`: the 49F-prefix fence and the account test run on the id column in Arrow, before any conversion to Python; only the account's rows are converted, with the same `json.loads(json.dumps(rows, default=str))`; a non-string id column takes the old path and returns the same triple; the adapter uses it when the ctx has it and otherwise runs the old code).
- `deploy-to-ec2.sh`: `OG-db-2` (the PREFLIGHT block) and `OG-db-3` (after the `tar -xzf` line, before the restart: the release sha is written to `/opt/opal-gateway/.deployed_commit`). `bash -n` is clean and `--preflight-only` prints `PREFLIGHT OK`.
- Tests (4): `test_og_en21`, `test_og_en22`, `test_og_en23`, `test_og_db3`.
- NOT in the release: `app/destructive_ops.py` (the trunk copy holds the same lines as the live one, as a multiset: one allowlist line is reordered; `tools.py` imports it and the seam is classified in-base), the harvest files, `DATA_CATALOG.yaml`, `EC2_MANIFEST.json`, Terraform, `family_depth.py`, `admin_people_access.py`, `partner_roster.json`, `silver_families.json`, and every other test file that differs live to trunk (`ap36_seams.json`: every other seam is in-base and identical to trunk).
- Test results (release tree): the ten window test files (`test_og_en13`, `en15`, `en17` to `en23`, `test_og_cl2`) 34 passed in both orders. The full suite: 1042 passed, 74 failed; at the live ref in a second tree: 1030 passed, 74 failed. The sets differ in two names, both stated: `test_blackdiamond.py::test_mx_t13_tool_registered_safe` fails at the live ref and PASSES in the release; `test_og_db3.py::test_ogdb3_ac03` is new and fails in the release tree only (it reads git history for a worker commit on `deploy-to-ec2.sh`, which the release branch cannot hold; it passes on trunk, 6 passed with `test_og_en23`). The other 73 failures are the same at both refs (`ap36_carried_failures.txt` is the re-run list of 74). The host-shaped zero-read import check passes as before (`server` needs `TENANT_ID`).

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` stays 103).
- `client_get_transactions` and `client_get_fees` run in a worker thread, so the gateway's other routes (health included) answer during a page. Today they run on the event loop and hold it for the whole page.
- The served prefix is listed once per call instead of once per partition; the fence and the account test run in Arrow, and only the account's rows are turned into Python. The answers are unchanged row for row: the six-page transactions chain of the candidate equals the live code's six pages on the row count and the sha256 of the canonical rows, with the same cursors (6 of 6; `PAGE_HASHES_OG-ap-36.json` is untracked and git-excluded).
- The deploy writes `/opt/opal-gateway/.deployed_commit` (the release sha).
- The reach is unchanged: the fence is still "the id is not null and starts with the 49F prefix", the account test is still equality, the denominators (`partition_rows`, `fence_excluded`) are still the partition's row count and the rows the fence drops; no tool argument is added.
- The 429 limit, the browser exemption roster and the allocation weight unit are NOT changed.
- **Memory and speed (the measurements, `MEM_GATE_OG-ap-36.json`; every run a fresh process on the host under the gateway role, candidate and live code staged in scratch folders, one windowed call at a time).**
  - Six-page chain: RSS before 103.4 MB, after pages 1 to 6 243.7, 254.9, 256.4, 278.6, 280.3, 271.0 MB; median page-to-page growth **1.7 MB** (limit 20); host peak 41.6 percent (limit 75); first page 2.09 s (limit 45). The live code's chain in the same run: 345.7, 335.2, 353.8, 356.2, 415.9, 380.7 MB, median growth 2.4, pages of 21.5 to 33.3 s.
  - Plateau (the whole chain twice in one process, 12 pages and 334 partitions each): RSS at the end of chain 1 217.5 MB and of chain 2 243.4 MB, net growth **25.9 MB** (limit 50); host peak 42.6 percent (limit 80); longest page 2.1 s (limit 55).
  - First page of the 13-month window: live code **29.75 s** (runs 29.41, 29.89, 29.75), candidate **1.93 s** (1.80, 2.27, 1.93).
  - Health during one full page through the candidate's own async wrapper (page 2.3 s): 5 probes of the event loop's `/health` handler, longest **0.033 s** (limit 1 s), all answered 200. The same probe against the LIVE code (the sync tool on the loop, page 29.8 s): 1 probe, longest **29.484 s**. The first Phase A (before `OG-en-23`) read 3.9 s on the candidate.
  - **Honest limit:** the measurements ran in fresh processes. The service's own long-lived process is read back in Phase B for 30 minutes; the service has served zero organic window calls in earlier read-backs, so the service heap over a full window call stays unmeasured (row `Z-S338`). A page of about 2 s means a health probe sees few ticks during it; the pass line (3 or more probes, longest under 1 s) is met with 5. The host marker is new state on the host.

## 3. The order of acts (Phase B)

1. Re-read the live ref (`9d5b712557`), the `.env` (65 keys, `MUSE_CLIENT_ID` absent), host memory, the gateway worker count (1 process) and the host md5 walk; else STOP.
2. Ledger `nfra-oplgtw-gateway-release-batch6` opened, entry AND sentinel committed first; the live ref's tarball sha256 recorded in it.
3. Restore the gate overlay (section 7) to the live ref's bytes; deploy from `C:/tmp/og-rel-batch6` through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=9d5b712557` under the stale-base guard; no `HALT_OVERRIDE`.
4. Read back against the triggers (section 6); on any trigger redeploy the rollback tree, remove the marker, and file an ARMED row naming `2.0.0_SA_COO~O`.
5. The served read `CODE6_SERVED.json` (eight arms, including health during a page, the marker equal to the release sha, and pages equal to the live code's row for row), the 30-minute service read-back every 60 s with the count of `/mcp` window calls served; runbook 7.2 and the manifest standing clauses; ledger closed; report.

## 4. Both branches

- A window within one page: complete, `next_cursor` null.
- A window beyond a page: `window_partial` true and a `next_cursor`; following it reads every dated partition once.
- A second windowed call in flight: `window_read_busy` after 15 s (in the service the call now runs in a worker thread, so the second call contends on the gate instead of queueing on the loop).
- A ctx without `partition_keys` or `read_account_rows` reads as before (the adapter falls back to the old code); a partition absent from the index answers empty.
- An unreadable partition refuses the call (fail closed); a stale base at Phase B is refused by the wrapper and Phase A is re-cut.

## 5. Rollback

The live ref's tree redeployed through the same wrapper, PROVEN by a host md5 walk equal to the pre-deploy walk (`ap36_host_md5.json`: 139 of 139 files equal, 0 differ, 0 missing, 0 unexplained). The live ref's S3 tarball `ec2/opal-gateway/opal-gateway-9d5b712557.tar.gz` sha256 and size are recorded in the ledger beside the entry. **The rollback also removes the host marker `/opt/opal-gateway/.deployed_commit` in the same step**: the old deploy script does not write it, and a marker naming the rolled-back release would be false. The base of an older ref is NOT the rollback target.

## 6. Triggers (any one: redeploy the rollback tree at once, remove the marker, file an ARMED row)

Health not 200 within 60 s; a tool of the 27 not answering; the `.env` key count not 65; `tools/list` changing from 103; host md5 differing beyond the released paths; host memory above 85 percent during the read-back (and above 80 percent stops the chain); a first page over 55 s; `/health` slower than 5 s DURING a page; the marker not equal to the release sha; and the read-back's own: the service above its baseline by 700 MB, or a median growth over 20 MB per window call after the first.

## 7. Gate lines and the overlay disclosure

The release commit, under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only, printed **0 REFUSE and 0 WARN**; **7 RAISE** lines, all one cause: the key-rulings reader could not load (`ModuleNotFoundError: opal_lambda_map`, a module outside the sparse cone), so no key is graded from a row (the shape of `OG-ap-34`). No registry prelude was needed. The naming gate's inputs (272 paths: 256 added, 16 modified, including the trunk `halt-gate-check.sh`) were laid from `trunk_sha` as an UNCOMMITTED overlay in the release tree (`ap36_overlay.json`); none is in the release commit; Phase B restores every one to the live ref's bytes before the deploy tree's clean check. The superseded first release commit `e45922ef75` remains in the release branch's history under this one.

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` `948e8b47cc626fe194383d04dfb6944edac1ae0b` and this ask's sha256.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` `948e8b47cc626fe194383d04dfb6944edac1ae0b` and this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` `948e8b47cc626fe194383d04dfb6944edac1ae0b` and this ask's sha256.
