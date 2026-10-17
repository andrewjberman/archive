# NEVER-WIDEN ASK -- `OG-ap-32` -- the round-40 batched gateway release, repaired (one code-only deploy of `opal-gateway`)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-32.round-40-batched-release.md` as amended (A1 `887e203b8c`, A2 `a31880f508`). GO for this Phase A: msg 35297 (the first Phase A, release `11031f278d` and its ask `82e211ff...`, is SUPERSEDED and was never sent to the halves).
Record: `ap32_release.json` in this folder: `base_sha` 4be300110ec912ac8c11a1663403e41eea45117c (the commit the release is CUT on), `declared_base_sha` 319c9413a20895a63517c5ca1b9ced0f78a5573a (the live ref, read from the manifest at HEAD and the S3 git-ref), `release_sha` b124377b41caf5665b999378fd0ca08ad8a1fb7d, `trunk_sha` d2b95c10cff58e5295ede3926096d452a50e36c7.
Phase A is READ ONLY against the world: nothing is deployed, applied or written to any bucket or table. The release is one commit on the local branch `rel-nfra-oplgtw-batch4` in `C:/tmp/og-rel-batch4`.

## 1. The diff, by file (cut on 4be300110e, 9 files, 867 insertions, 137 deletions)

**The cut-on fact (Amendment A2, ruling on row Z-S336).** While Phase A was open, another seat (`0.7.0_AE_CloudOps~SC1`, AMGT_HARVST HVST-cc-7) deployed `319c9413a2` to the same host at 2026-10-17T00:10:31Z. That commit is not in this repository. This release is cut on its parent `4be300110e` and takes the three harvest files that changed whole from trunk. The live host copies of those three files are byte-equal to trunk's (md5 read over SSM), so this release carries exactly what is live. The deploy declares `DEPLOY_BASE_REF=319c9413a2...` (the live ref), under the stale-base guard, after the host md5 walk below.

| file | change | order |
|---|---|---|
| `app/client_adapter_bd49f.py` | 18 hunks: 17 attributed to OG-en-18, OG-en-17, OG-en-15, OG-en-13; 1 is one identical line moved inside `_window_read` (it occurs once in the base and once in trunk; `ap32_attr.json`) | OG-en-17 (paging, cursor, newest first), OG-en-18 (repair) |
| `app/harvest_figures.py`, `app/harvest_identity.py`, `app/harvest_research.py` | taken WHOLE from trunk; ALREADY LIVE on the host byte-equal; the widening adds nothing from them | AMGT_HARVST HVST-cc-7 (not this order's) |
| `app/refs/DATA_CATALOG.yaml` | taken WHOLE at blob 2cbe275d03c9a5af85afefabc604e26b71e9be12, md5 bdfee515ec348f0ea2ee716eff5acba5 (both read in the release tree) | `NFRA_MCPINDEX` re-emit (MI) |
| `tests/test_og_en17.py`, `tests/test_og_en18.py` | new (234 and 255 lines) | OG-en-17, OG-en-18 |
| `tests/test_og_en15.py`, `tests/test_og_cl2.py` | changed (27 and 8 lines) | OG-en-18 / OG-en-17 |

NOT in the release: `tools.py`, `destructive_ops.py`, `deploy-to-ec2.sh`, `EC2_MANIFEST.json`, any Terraform, any registry file, any data copy (`ap32.AC1` reads the diff for each). The catalog, compared row by row with the base: all 284 entity rows content-equal; `tool_index` keeps its 127 entries and gains `depth_kind` and `measured_at` on 39 depth claims; the only other changed key is `built_at_git_head`. MI's half `NEVER_WIDEN_CATALOG_R21_20261016.md` is signed on this blob and void on any other.

**Host md5 walk against the release (per-file denominator, `ap32_host_md5_release.json`).** 139 files expected from the release blobs over `app/`, `deploy/` and `lib/` (plus requirements and the allowlist), 141 on the host (the two staged `app/refs` files, both equal to trunk): **137 equal, 2 differ, 0 missing, 0 unexplained extra.** The two that differ are `app/client_adapter_bd49f.py` and `app/refs/DATA_CATALOG.yaml`: this release's own files, still at the base versions on the host. The three harvest files are among the 137 equal. No other host-versus-release difference exists.

Seams: 4 distinct modules over 10 importer edges, 0 STOP-class (`ap32_seams.out`). Tests: the 5 touched files, 21 passed forward and 21 reversed (`ap32_tests.out`). The whole gateway suite in the sparse release tree: 73 failed, 1027 passed; at the pristine base `4be300110e`: 74 failed, 1020 passed; failing only in the release: 0; fixed by the take: 1 (`test_blackdiamond.py::test_mx_t13_tool_registered_safe`); the other 73 are carried by name (`ap32_full_*.out`; `test_og_ch1.py` is among them, red at the base as the order says). Host-shaped import check, zero reads, with and without `lib/opal_naming.py`: 6 of 7 modules import; `server` needs the host `.env` at import, as at the base (`ap32_hostshape.json`, from the first Phase A; the app code is unchanged in kind).

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` is 103 before; AC2 requires 103 after). No Terraform. No deploy-script or manifest change at the release commit. No object or item is written to any bucket or table.
- **What one call now does.** A 13-month `client_get_transactions` or `client_get_fees` request returns the NEWEST slice of up to 30 dated partitions (`PAGE_PARTITIONS = 30`), read with at most 16 in flight (`READ_WORKERS = 16`), plus `next_cursor` (the day before the oldest partition read, passed back as `to_date`; null at the end of the data). `window_partial` is true while a cursor remains. A caller pages back through the window: transactions 334 partitions in about 12 pages, fees about 394 in about 14. The base read the newest 60 and stopped with no way back.
- **A change in what an analyst sees.** Rows within a page are served NEWEST FIRST; the base served oldest first. Each next page's newest date is not later than the previous page's oldest. Exact-duplicate removal is as live since OG-en-15.
- **One windowed read at a time per process (OG-en-18).** A second windowed call waits up to 15 s for the gate, then answers `window_read_busy` with `retry_after_seconds` 15 and reads nothing. Measured on the host with the candidate code in a new process (the service untouched; `ap32_firstpage.json`): with the wait patched to 0.5 s, a second call made while the first was in flight returned in 1.43 s with `retry_after_seconds` 0.5 and no `partitions_read`; the first call completed. (That run read the reason key as null; the adapter writes `window_read_busy` into `absent_reason`, and `test_og_en18` covers it. Phase B's arm records the key.)
- **HOST MEMORY PLAN, now measured.** Each partition task fences its rows and keeps only the requested account's rows, so memory is bounded by the 16 partitions in flight, not by the page (OG-en-18; the first design held all 60 partitions and was measured at +470 to +550 MB). First page of the candidate code on the host, host memory percent used (1 - available/total): transactions before 38.2, **peak 64.3**, after 58.5; fees before 58.5, peak 58.5, after 57.9. That harness process had itself read whole partitions to find an account (its baseline was 38 percent, against 25 to 30 for the service), so the service's own peak should sit lower. One page stays far under 85 percent. The residual risk is the gate: it is per process, so two gateway processes would each take one page. Phase B runs the page chain strictly one call at a time, samples host memory every 0.25 s, and stops the chain at 80 percent.
- **Measured first-page wall time (the order's arm wants under 30 s).** Transactions 29.34 s (30 partitions, 334 in the window, cursor returned); fees 12.39 s (30 of 394, cursor returned). Transactions sits 0.66 s under the line in that run, on the host with the harness's own memory load: **treat the transactions first page as at the threshold**, not comfortably inside it. The per-partition prefix listing (row Z-S328, about 0.4 of each 0.55 s) is not in this release. A miss on wall time alone is graded FAIL as measured, a row is opened and the issuer decides; it is not a rollback trigger.
- The 429 limit, the browser exemption roster (host `MASTER_ADMIN_EMAILS` holds 1 entry, row Z-S322) and the allocation weight unit (null, not established, row Z-S313) are NOT changed.

## 3. The order of acts (Phase B, only on the issuer's GO naming all three halves at `release_sha`)

1. Re-read the live ref (must still be `319c9413a2`, else STOP), the host `.env` (65 keys, `MUSE_CLIENT_ID` absent) and the host memory percent; the host md5 walk against the release blobs must show the same 2 differing files and no other.
2. Open ledger `nfra-oplgtw-gateway-release-batch4` (entry and sentinel first).
3. Restore the overlay (section 7) except the trunk `halt-gate-check.sh` the wrapper needs, then ONE deploy: `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=319c9413a20895a63517c5ca1b9ced0f78a5573a` from `C:/tmp/og-rel-batch4`, no `HALT_OVERRIDE`.
4. Read back against the triggers; the served read through the installed code (`CODE4_SERVED.json`, four arms); the standing clauses; `ap32.AC2`.

## 4. Both branches

- A window within one page: complete, `window_partial` false, `next_cursor` null.
- A window beyond a page: `window_partial` true, `next_cursor` set, 30 partitions read; the cursor as `to_date` returns the next older slice.
- A second windowed call while one is in flight: `window_read_busy`, nothing read.
- An unreadable partition in a page: the call refuses; no partial answer is built.
- Holdings, allocation, a non-admin and the existing routes: unchanged.

## 5. Rollback

The release is code-only, so the rollback is a redeploy of the pre-deploy content: this release's tree with `client_adapter_bd49f.py` and `DATA_CATALOG.yaml` set back to their base blobs (the three harvest files stay: they are live now). The tree is cut at the act and PROVEN by a host md5 walk equal to the pre-deploy walk (137 equal, the same 2 files). The byte reference for the live state is its S3 tarball `opal-gateway-319c9413a2.tar.gz` (895292 bytes, 2026-10-17T00:10:01Z, present). It is deployed through the wrapper with `DEPLOY_BASE_REF` set to this release commit. The base `4be300110e` is NOT the rollback target: it would revert the three harvest fixes. No data, key or IAM undo exists or is needed.

## 6. Triggers (roll back AT ONCE, file an ARMED row naming `2.0.0_SA_COO~O`)

`/health` is not 200 within 60 s; a tool of the 27 added tools does not answer; the `.env` key count is not 65 or `MUSE_CLIENT_ID` appears; `tools/list` changes from 103; host md5 shows any file other than the 4 released app/ref paths differing from the release blobs; host memory above 85 percent during the paging read-back.

## 7. Gates, tests and disclosures

- Step 1 (this Phase A): manifest `deployed_commit` and the S3 ref read 319c9413a2 (`ap32b_*`); `tools/list` 103, health 200, `.env` 65 keys without `MUSE_CLIENT_ID`; `gateway-49f-blackdiamond-live-read-role` resolves; host memory about 29 percent used at the step-1 re-read.
- The release commit under `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` (audited): `NAMING-GATE: WARN 266 graded`, 0 REFUSE; `CATALOG-EXEMPT admitted=0 refused=0 literals=154`; no prelude registry commit (0 registry files in the diff). The 266 RAISE lines are WARN-class: 22 on the adapter, 154 on the catalog, 90 on the three harvest files (names and timestamps in code the gate has not graded before). One notice: `name_rulings.json could not be read (ModuleNotFoundError: opal_lambda_map); no name is graded from a row`. One WARN: `client-data-check: hashed account-id list ABSENT` (code, tests and a catalog; no client data).
- **Uncommitted gate overlay (the OG-ap-28 and OG-ap-31 precedent, with the two cures of row Z-S324).** 270 paths laid from `trunk_sha` as an UNCOMMITTED working-tree overlay (`ap32_overlay.json`): `.tools/naming-*`, the trunk `.tools/halt-gate-check.sh`, `infra/logic/**`, `lib/opal_naming*`, the schema, `DIRECTIVES.yaml`, and `infra/aws/lambda/ci/function-map/` (the 241-file folder the trunk naming gate reads and refuses without: `function-map folder missing`, first attempt, nothing overridden). The release commit names its 9 paths explicitly and carries none of them. Phase B restores the overlay to the base's bytes before the deploy tree's clean check.
- The sparse cone holds `org/tier2_senior/0.7.0_AE_CloudOps~Z` (the CloudOps home folder the halt gate needs).

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed against this ask's sha256 and `release_sha` b124377b41caf5665b999378fd0ca08ad8a1fb7d.

### COO half (`2.0.0_SA_COO~O`)

To be signed against this ask's sha256 and `release_sha` b124377b41caf5665b999378fd0ca08ad8a1fb7d.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed against this ask's sha256 and `release_sha` b124377b41caf5665b999378fd0ca08ad8a1fb7d.
