# NEVER-WIDEN ASK -- `OG-ap-34` -- the round-40 fourth batched gateway release: the 49F window pages back with a cursor, newest first, memory flat

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-34.round-40-fourth-batched-release.md` (GO for Phase A: msg 35327).
Release: `release_sha` = `9d5b7125571520b977401634a01935924f4c9787`, cut on the live ref `base_sha` = `d3ae88be463d88c6f4ea22fb297659bf44f43758` (the rollback tree of `OG-ap-32`), from `trunk_sha` = `d9364e3e9c98eb4e5ea21151f67c54c229885cc2`. Record: `ap34_release.json`. Release tree `C:/tmp/og-rel-batch5`, branch `rel-nfra-oplgtw-batch5`. The Phase A act is read-only on the estate: nothing was deployed or applied; the memory gate ran in a scratch folder on the host that was removed.

## 1. The diff, by file (`git diff d3ae88be46 9d5b712557`: 9 files, 652 insertions, 123 deletions)

- `app/client_adapter_bd49f.py` (live blob `6b7b825ec8`): the live blob is the parent of `OG-en-17`'s commit and the trunk blob is `OG-en-20`'s, so the diff is exactly the work of `OG-en-17` (cursor paging, newest partition first), `OG-en-18` (an account's rows kept per partition, pages of 30, one windowed read in flight), `OG-en-19` (each page ordered by trade date, newest first, stable) and `OG-en-20` (`mallopt(M_ARENA_MAX, 2)` once at import, 8 read workers). 21 hunks: 20 attributed to those commits line by line, 1 is a moved identical line (`ap34_attr.json`).
- `app/refs/DATA_CATALOG.yaml`: taken WHOLE at `trunk_sha`, blob `2cbe275d03c9a5af85afefabc604e26b71e9be12` (live `b81c48aa3c`). `2.0.0_SA_COO~MI`'s half `NEVER_WIDEN_CATALOG_R21_20261016.md` is signed on exactly this blob.
- Tests (7): `test_og_en13`, `en15`, `en17`, `en18`, `en19` (new), `en20` (new), `test_og_cl2`.
- NOT in the release: `deploy-to-ec2.sh`, `EC2_MANIFEST.json`, any Terraform, `tools.py`, `destructive_ops.py`, the eight other app files that differ live to trunk (`ap34_seams.json`: 2 seams, both resolved: the adapter is in the take list, `client_core.py` is identical to trunk). The three harvest files are live and equal to trunk's, so they are not in the diff.
- Test results (release tree): the seven taken test files, 25 tests, pass in both orders. The full suite: 1030 passed, 74 failed; at the live ref in a second tree: 1017 passed, 83 failed. Every one of the 74 also fails at the live ref (named in `ap34_carried_failures.txt`, none in a taken test file); they are carried. The host-shaped zero-read import check passes as for `OG-ap-32` (`ap34_hostshape.json`; `server` needs `TENANT_ID`, the same as before).

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` stays 103).
- A 13-month transactions or fees request returns the newest slice of up to 30 dated partitions (8 read in flight, an account's rows kept per partition, the arena cap) plus a `next_cursor`; a caller pages back through the window with `to_date` = the cursor.
- Rows within a page are ordered by trade date, newest first, where the base served oldest first. Across pages the cursor moves back by partition date.
- One windowed read runs at a time per process; a second answers `window_read_busy` after 15 s.
- The catalog gains `depth_kind` and `measured_at` on 39 depth claims and moves two definition anchors and three provenance lines, with no row, tool, visibility or value change.
- NOT changed: the 429 limit, the browser exemption roster, the allocation weight unit.
- **Memory (the gate, `MEM_GATE.json`).** The candidate code ran in a FRESH process on the host under the gateway role, the transactions chain for the one test account, 13-month window, one call at a time, four pages, 8 read workers, `MALLOC_ARENA_MAX` unset (the code caps arenas itself). RSS before the first page 102.4 MB; after pages 1 to 4: 369.7, 362.9, 339.4, 329.0 MB; median page-to-page growth over pages 2 to 4 **-10.4 MB** (limit 20); host used 28.2 percent idle, 45.9 percent at the peak (limit 75); wall seconds per page 30.4, 22.0, 24.1, 34.1 (first page limit 45). **Honest limit:** the gate ran in a fresh process, not in the service's own long-lived process, which Phase B measures (`memory_basis` `service` where the stand-in can reach it); `mallopt` caps only arenas created after the call; four pages are not the whole 12-page window, so the full chain is measured in Phase B under the 80 percent stop; the first page's working set (about 270 MB above the idle process) is real and is returned only partly (370 to 329 MB); the host has 1846 MB and no swap, with the service itself at about 150 MB.

## 3. The order of acts (Phase B)

1. Re-read the live ref (`d3ae88be46`), the `.env` (65 keys, `MUSE_CLIENT_ID` absent), host memory, the gateway worker count (1 process, `--workers 1`) and the host md5 walk; else STOP.
2. Ledger `nfra-oplgtw-gateway-release-batch5` opened, entry AND sentinel committed first; the live ref's tarball sha256 recorded in it.
3. Restore the gate overlay (section 7) to the live ref's bytes; deploy from `C:/tmp/og-rel-batch5` through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d3ae88be46`; no `HALT_OVERRIDE`.
4. Read back against the triggers (section 6); on any trigger redeploy the rollback tree and file an ARMED row naming `2.0.0_SA_COO~O`.
5. The served read `CODE5_SERVED.json` (five arms), one call at a time, host memory sampled every 0.25 s, stopped at 80 percent; runbook 7.2 and the manifest standing clauses at the close; ledger closed; report.

## 4. Both branches

- A window within one page: complete, `next_cursor` null.
- A window beyond a page: `window_partial` true and a `next_cursor`; following it reads every dated partition once.
- A second windowed call in flight in the same process: `window_read_busy` after 15 s.
- An unreadable partition: the call is refused (fail closed); no partial answer is built.
- A stale base (the live ref moved) at Phase B: the wrapper's stale-base guard refuses, nothing is deployed, Phase A is re-cut.

## 5. Rollback

The pre-deploy content: this release tree with `app/client_adapter_bd49f.py` and `app/refs/DATA_CATALOG.yaml` set back to their blobs at the live ref (`6b7b825ec8`, `b81c48aa3c`) and the tests back to their live blobs, redeployed through the same wrapper. It is PROVEN by a host md5 walk equal to the pre-deploy walk (`ap34_host_md5.json`: 139 of 139 files equal, 0 differ, 0 missing, 0 unexplained). The live ref's S3 tarball `ec2/opal-gateway/opal-gateway-d3ae88be46.tar.gz` (size 895333 bytes) has sha256 `764f565cffef310156c85a4c31ad972d10615f0fbc0c732c8fa8fceca3f8b236` (the same bytes as `opal-gateway-latest.tar.gz` today); it goes into the ledger beside its size. The base of an older ref is NOT the rollback target.

## 6. Triggers (any one: redeploy the rollback tree at once, file an ARMED row)

Health not 200 within 60 s; a tool of the 27 not answering; the `.env` key count not 65; `tools/list` changing from 103; host md5 differing beyond the released paths; host memory above 85 percent during the read-back; a first page over 55 s.

## 7. Gate lines and the overlay disclosure

The release commit, under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only, printed **0 REFUSE and 0 WARN**; **179 RAISE** lines, all one cause: the key-rulings reader could not load (`ModuleNotFoundError: opal_lambda_map`, a module outside the sparse cone), so no key is graded from a row (the `OG-ap-32` shape). No registry prelude was needed. The naming gate's inputs (270 paths: 255 added, 15 modified, including the trunk `halt-gate-check.sh`) were laid from `trunk_sha` as an UNCOMMITTED overlay in the release tree (`ap34_overlay.json`); none is in the release commit; Phase B restores every one to the live ref's bytes before the deploy tree's clean check.

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` `9d5b7125571520b977401634a01935924f4c9787` and this ask's sha256.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` `9d5b7125571520b977401634a01935924f4c9787` and this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` `9d5b7125571520b977401634a01935924f4c9787` and this ask's sha256.
