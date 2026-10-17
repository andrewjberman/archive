# NEVER-WIDEN ASK -- `OG-ap-32` -- the round-40 batched gateway release (one code-only deploy of `opal-gateway`)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-32.round-40-batched-release.md`. GO for Phase A: msg 35294.
Record: `ap32_release.json` in this folder: `base_sha` 4be300110ec912ac8c11a1663403e41eea45117c (the live ref), `release_sha` 11031f278d092e5c79ec7d865891024c967160d8, `trunk_sha` 2161dab1031bb7378666e6a239d563b5e53d6c86.
Phase A is READ ONLY against the world: nothing is deployed, applied or written to any bucket or table. The release is one commit on the local branch `rel-nfra-oplgtw-batch4` in `C:/tmp/og-rel-batch4`.

## 1. The diff, by file (base..release, 5 files, 455 insertions, 115 deletions)

| file | change | order |
|---|---|---|
| `app/client_adapter_bd49f.py` | 14 hunks, 14 attributed, 0 unattributable (`ap32_attr.json`) | OG-en-17 (paging, cursor, newest first); the lines it rewrites were written by OG-en-15 and OG-en-13, already live |
| `app/refs/DATA_CATALOG.yaml` | taken WHOLE at blob 2cbe275d03c9a5af85afefabc604e26b71e9be12, md5 bdfee515ec348f0ea2ee716eff5acba5 (both read in the release tree) | `NFRA_MCPINDEX` re-emit (MI) |
| `tests/test_og_en17.py` | new, 231 lines | OG-en-17 |
| `tests/test_og_en15.py`, `tests/test_og_cl2.py` | changed (19 and 8 lines) | OG-en-17 |

NOT in the release: `tools.py`, `destructive_ops.py`, `deploy-to-ec2.sh`, `EC2_MANIFEST.json`, any Terraform, any registry file, any data copy. `ap32.AC1` reads the diff for all of these. The 11 other app files that differ between the live ref and trunk (`admin_people_access.py`, `family_depth.py`, `harvest_*.py`, the `refs/` files, the yearinreview files, `tools.py`, `destructive_ops.py`) belong to no named order and stay at the base.

The catalog, compared row by row with the live one: all 284 entity rows are content-equal (0 added, 0 removed, 0 changed); `tool_index` keeps its 127 entries and gains `depth_kind` and `measured_at` on 39 depth claims (39 and 39 where the base had 0); the only other changed top-level key is `built_at_git_head`. No row, tool, visibility or value changes. MI's half `NEVER_WIDEN_CATALOG_R21_20261016.md` is signed on this blob and void on any other.

Seams: 2 distinct modules over 4 importer edges, 0 STOP-class (`ap32_seams.out`). Tests: the 3 touched files, 15 passed forward and 15 reversed (`ap32_tests.out`). The whole gateway suite in the sparse release tree: 74 failed, 1023 passed; at the pristine live ref: 74 failed, 1020 passed; failing only in the release: 0, failing only at the live ref: 0 (the same 74 carried by name, `ap32_full_*.out`; `test_og_ch1.py::test_ogch1_ac02` is among them, red at the base as the order says). Host-shaped import check, zero reads, with and without `lib/opal_naming.py`: 6 of 7 modules import; `server` needs the host `.env` at import, as at the live ref (`ap32_hostshape.json`).

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` is 103 before; AC2 requires 103 after). No Terraform. No deploy-script or manifest change at the release commit. No object or item is written to any bucket or table.
- **What one call now does.** A 13-month `client_get_transactions` or `client_get_fees` request returns the NEWEST slice of up to 60 dated partitions (`PAGE_PARTITIONS = 60`), read with 16 concurrent reads (`READ_WORKERS = 16`), plus `next_cursor` (the day before the oldest partition read, passed back as `to_date`; null at the end of the data). `window_partial` is true while a cursor remains. A caller pages back through the whole window (transactions about 334 partitions in 6 pages, fees about 396 in 7). The base read the same newest 60 and stopped with no way back.
- **A change in what an analyst sees.** Rows within a page are served NEWEST FIRST; the base served oldest first. Each next page's newest date is not later than the previous page's oldest. Exact-duplicate removal is as live since OG-en-15.
- **HOST MEMORY PLAN.** The page read holds the rows of ALL its partitions at once (`_read_partitions` returns the list for the whole page before the fence runs), and the host has 1846 MB, 2 vCPU and NO swap. Measured read-only on the host (`ap32_memplan.json`): reading the newest 8 partitions the same way and keeping the rows grows the process by 7.8 MB per transactions partition (11376 rows on average) and 9.2 MB per fees partition (4084 rows). Projected to 60 partitions: +469 MB (transactions) and +551 MB (fees), taking the host from 29.5 percent used to about 55 and 59 percent while the page is held; in-flight read buffers add a few points on top (the 8-partition sample peaked 6.8 points above its start, 4.2 of them retained). One page therefore stays under the 85 percent bound with margin. **TWO page reads in flight at once do not: about 85 to 100 percent.** The code has no process-wide limit (no semaphore or lock); the tools are master_admin only and the 429 limit is 120 per 60 s. The residual risk is two such calls overlapping on the live host. Phase B runs the page chain strictly one page at a time from one caller, samples host memory every 0.25 s (before, at the peak, after), and stops the chain at 80 percent before the next page. A cap on concurrent page reads is a code change and is not in this release; the halves decide whether to accept the residual risk.
- **Expected wall time (a prediction, not a measurement).** OG-ev-3 measured an effective 0.37 s per file for fees (396 files in 146 s) and 0.72 s per file for transactions (334 files in 240 s) at concurrency 16, because every `read_rows` call lists the whole prefix first (row Z-S328). A 60-file page is therefore about 22 s for fees and about 43 s for transactions. The order's `e1_cursor_first_page` arm requires the first page under 30 s: **transactions is predicted to miss it**, and would still sit inside the 60 s ALB idle timeout. Phase B measures it. The per-partition prefix listing is not in this release.
- The 429 limit, the browser exemption roster (host `MASTER_ADMIN_EMAILS` holds 1 entry, row Z-S322) and the allocation weight unit (null, not established, row Z-S313) are NOT changed.

## 3. The order of acts (Phase B, only on the issuer's GO naming all three halves at `release_sha`)

1. Re-read the live ref, the host `.env` (65 keys, `MUSE_CLIENT_ID` absent) and the host memory percent; any mismatch is a STOP.
2. Open ledger `nfra-oplgtw-gateway-release-batch4` (entry and sentinel first).
3. Restore the uncommitted overlay (section 7) except what the wrapper needs, then ONE deploy: `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=4be300110e...` from `C:/tmp/og-rel-batch4`, no `HALT_OVERRIDE`, under the stale-base guard.
4. Read back against the triggers; then the served read through the installed code (`CODE4_SERVED.json`, four arms); then the standing clauses and `ap32.AC2`.

## 4. Both branches

- A window within one page: the answer is complete, `window_partial` false, `next_cursor` null.
- A window beyond a page: `window_partial` true, `next_cursor` set, 60 partitions read; passing the cursor as `to_date` returns the next older slice.
- An unreadable partition in a page: the call refuses; no partial answer is built (the first failing read cancels the reads not yet started).
- An allocation or holdings call, a non-admin and the existing routes: unchanged.

## 5. Rollback

Redeploy the base `4be300110ec912ac8c11a1663403e41eea45117c` through the same wrapper (`DEPLOY_BASE_REF` set to the release commit for the reverse stale-base read). Code-only; no data, key or IAM undo exists or is needed. The base host md5 is recorded: 139 of 139 equal (`ap32_host_md5.json`).

## 6. Triggers (roll back AT ONCE, file an ARMED row naming `2.0.0_SA_COO~O`)

`/health` is not 200 within 60 s; a tool of the 27 added tools does not answer; the `.env` key count is not 65 or `MUSE_CLIENT_ID` appears; `tools/list` changes from 103; host md5 shows any file other than the 5 released paths differing from the release blobs; host memory above 85 percent during the paging read-back. A miss in an `e1` arm on wall time alone (transactions first page over 30 s) is graded FAIL as measured, a row is opened, and the issuer decides: it is not a rollback trigger.

## 7. Gates, tests and disclosures

- Live ref before this release: manifest `deployed_commit`, the S3 ref and the host agree on 4be300110e; host md5 139 of 139 equal, 0 differ, 0 missing, 0 extra; `.env` 65 keys, `MUSE_CLIENT_ID` absent; `tools/list` 103 (registry 103); health 200; host memory 25.7 percent used (1 - available/total) at the read; `gateway-49f-blackdiamond-live-read-role` resolves.
- The release commit under `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` (audited): `NAMING-GATE: WARN 169 graded`, 0 REFUSE; `CATALOG-EXEMPT admitted=0 refused=0 literals=154`; no prelude registry commit (0 registry files in the diff). The 169 RAISE lines are WARN-class: 15 on the adapter (`cursor`, `chosen`, `in_window`, `newest`, `next_cursor`, `window_partial`, `window_note` and one message string) and 154 on the catalog's own timestamps, series fields and anchors. One notice: `name_rulings.json could not be read (ModuleNotFoundError: opal_lambda_map); no name is graded from a row`. One WARN: `client-data-check: hashed account-id list ABSENT` (the 5 files hold code, tests and a catalog, no client data).
- **Uncommitted gate overlay (the OG-ap-28 and OG-ap-31 precedent, now with the two cures of row Z-S324).** The live ref's naming module and schema are an inconsistent pair, so 270 paths were laid from `trunk_sha` as an UNCOMMITTED working-tree overlay (`ap32_overlay.json`): `.tools/naming-*`, the trunk `.tools/halt-gate-check.sh`, `infra/logic/**`, `lib/opal_naming*`, the schema, `DIRECTIVES.yaml`, and `infra/aws/lambda/ci/function-map/` (241 files; the trunk naming gate reads that folder and refuses without it: `function-map folder missing`, first attempt, refused, nothing overridden). The release commit names its 5 paths explicitly and carries none of them. Phase B restores the overlay to the live ref's bytes before the deploy tree's clean check.
- The sparse cone holds `org/tier2_senior/0.7.0_AE_CloudOps~Z` (the CloudOps home folder the halt gate needs).

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed against this ask's sha256 and `release_sha` 11031f278d092e5c79ec7d865891024c967160d8.

### COO half (`2.0.0_SA_COO~O`)

To be signed against this ask's sha256 and `release_sha` 11031f278d092e5c79ec7d865891024c967160d8.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed against this ask's sha256 and `release_sha` 11031f278d092e5c79ec7d865891024c967160d8.
