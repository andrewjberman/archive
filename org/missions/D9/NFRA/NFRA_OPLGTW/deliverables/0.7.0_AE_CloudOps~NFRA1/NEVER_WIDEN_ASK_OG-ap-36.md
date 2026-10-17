# NEVER-WIDEN ASK -- `OG-ap-36` (amendment A3 re-draft) -- the round-41 fifth batched gateway release: the windowed client tools run off the event loop and convert only the account's rows, the served prefix is listed once per page, the deploy writes the release sha to the host, and a refusal's reason is no longer nulled at the tool boundary

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-36.round-41-fifth-batched-release.md` with its amendments A1 to A3 (GO for this re-run: msg 35494).
Release: `release_sha` = `b6bef4424482e78c6607935dca6a861582e2acc1`, cut on the live ref `base_sha` = `9d5b7125571520b977401634a01935924f4c9787` (the `OG-ap-34` release), from `trunk_sha` = `6f17348437a793c1f6fecadd4511d32796482ef3`; `measured_release_sha` = `948e8b47cc626fe194383d04dfb6944edac1ae0b` (where the memory records were measured). Record: `ap36_release.json`. Release tree `C:/tmp/og-rel-batch6`, branch `rel-nfra-oplgtw-batch6`. Phase A is read-only on the estate: nothing was deployed or applied; the host measurements ran in scratch folders that were removed.
**This ask SUPERSEDES the first ask (sha256 `10fc9646e5`, release `948e8b47cc`) and its three halves; they are not edited.** History: Phase A on trunk `58bb50256e` STOPPED on two measurements (row `Z-S370`); `OG-en-23` repaired them (the re-run passed all five, release `948e8b47cc`); the addendum's CT1 run then STOPPED on the busy word (row `Z-S372`: the refused second call's `absent_reason` read null at the tool boundary); CTO decisions 35484, 35485, 35489 and 35492 ordered the mapping cut now as a trunk cell, `OG-en-24`, and a proportionate re-run. This release is `948e8b47cc` plus that cell.

## 1. The diff, by file (`git diff 9d5b712557 b6bef44244`: 9 files, 1254 insertions, 20 deletions)

- **Against the measured release `948e8b47cc` the delta is exactly two files** (`git diff 948e8b47cc b6bef44244`): `app/client_core.py` (ONE hunk, three changed lines: `OG-en-24` makes `_answer` keep the adapter's own `absent_reason` when the adapter sends no `_absent_reason`; before, `meta["_absent_reason"]`, which is None for the 49F adapter, overwrote it) and the new `tests/test_og_en24.py` (209 lines). The other seven files are byte-equal to the first release's.
- `app/tools.py`: `OG-en-21` (`client_get_transactions` and `client_get_fees` become `async` and run the read in a worker thread by `anyio.to_thread.run_sync`) and the POSITION move of `harvest_get_published_analysis` landed by `OG-ap-33`. 8 hunks, all attributed (`ap36_attr.json`): 4 to `OG-en-21`, 4 to the position move. The name is imported once and defined and registered once.
- `app/client_core.py` and `app/client_adapter_bd49f.py`: `OG-en-22` (`Ctx.partition_keys` lists the served prefix once per call), `OG-en-23` (`Ctx.read_account_rows`: the 49F-prefix fence and the account test run in Arrow before any conversion; only the account's rows are converted), and now `OG-en-24`.
- `deploy-to-ec2.sh`: `OG-db-2` (the PREFLIGHT block) and `OG-db-3` (the release sha written to `/opt/opal-gateway/.deployed_commit`). `bash -n` clean; `--preflight-only` prints `PREFLIGHT OK`.
- Tests (5): `test_og_en21`, `en22`, `en23`, `en24`, `db3`.
- NOT in the release: `app/destructive_ops.py` (same lines as the live one, as a multiset: one allowlist line is reordered), the harvest files, `DATA_CATALOG.yaml`, `EC2_MANIFEST.json`, Terraform, `family_depth.py`, `admin_people_access.py`, `partner_roster.json`, `silver_families.json`. **Seam note:** `app/harvest_research.py` now differs between the live ref and trunk (AMGT_HARVST HVST-cc-2 and HVST-cd-1: the misfiled-report exclusion). It is not in this release (the order bars the harvest files); `tools.py` uses three names from it (`harvest_get_research`, `harvest_get_filing_analysis`, `harvest_get_peers_and_scores`) and all three exist in the live module, so the taken `tools.py` runs against the live harvest file unchanged.
- Test results (release tree): the eleven window test files (`test_og_en13`, `en15`, `en17` to `en24`, `test_og_cl2`) 37 passed in both orders. The full suite: 1045 passed, 74 failed; at the live ref in a second tree: 1030 passed, 74 failed. The sets differ in two names, as for `948e8b47cc`: `test_blackdiamond.py::test_mx_t13_tool_registered_safe` fails at the live ref and PASSES in the release; `test_og_db3.py::test_ogdb3_ac03` is new and fails in the release tree only (it reads git history for a worker commit on `deploy-to-ec2.sh`, which the release branch cannot hold; it passes on trunk). The failing set is identical to the `948e8b47cc` run's. The host-shaped zero-read import check passes as before.

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` stays 103).
- `client_get_transactions` and `client_get_fees` run in a worker thread, so the gateway's other routes (health included) answer during a page; the served prefix is listed once per call; the fence and the account test run in Arrow and only the account's rows are turned into Python; the deploy writes the host marker. The answers are unchanged row for row (below).
- **What `OG-en-24` changes, named plainly.** The reason a tool answer gives for an empty or refused result is no longer nulled at the tool boundary. Eight codes now surface where the core dropped them: `window_read_busy`; `no_partition_at_as_of` (on the five tools that refuse so); from the 49F adapter `no_candidate_for_last4`, `account_not_in_partition`, `no_model_assignment_49f` and `no_fee_rows_in_window`; from the Cottonwood allocation adapter `no_model_assignment` and `model_not_in_roster`. The Orion, Eclipse, SmartX, Schwab and Commonwealth answers are unchanged. No row is added or removed and no reach changes; only the reason, which the adapter already set, is no longer replaced by null. A caller that read a null reason as "nothing to report" now reads the reason.
- The 429 limit, the browser exemption roster and the allocation weight unit are NOT changed.
- **Pages equal the live code's** (the first release's six-page record; `OG-en-24` touches no read path): rows, sha256, cursors, `partition_rows` and `fence_excluded` equal on 6 of 6 pages (`PAGE_HASHES_OG-ap-36.json` is untracked and git-excluded). Re-compared on this release in the CT1 run: 6 of 6 again.
- **Memory and speed (`MEM_GATE_OG-ap-36.json`, measured on `948e8b47cc`; NOT re-run, because this release differs from it only by the one `_answer` hunk above, which is not on the read path).** Six-page chain: RSS before 103.4 MB, after pages 1 to 6 243.7, 254.9, 256.4, 278.6, 280.3, 271.0 MB; median growth **1.7 MB** (limit 20); host peak 41.6 percent (limit 75); first page 2.09 s (limit 45); the live code's chain median 2.4. Plateau (the whole chain twice, 334 partitions each): net growth **25.9 MB** (limit 50), host peak 42.6 percent, longest page 2.1 s. First page: live **29.75 s**, candidate **1.93 s**. Health during one full page: 5 probes, longest **0.033 s**; the live code held the loop **29.5 s**.
- **CT1 on THIS release (`CT1_CONCURRENT_OG-ap-36.json`; a fresh process on the host through the candidate's own async wrapper).** Solo: one first page, 1.9 s, 36 rows. Pair under the REAL 15 s gate wait (the second call started 0.3 s after the first): the first call returned rows equal to its solo run; the second waited for the gate and then returned rows equal to the solo rows (done at 2.67 s): `waited_then_equal_solo`. Pair under a 0.5 s gate wait (a scratch-process override of the module constant; no file changed): the first call equal to its solo run; the second answered **`window_read_busy`**, carried in `absent_reason`, with `retry_after_seconds` 0.5. `/health` probed every 0.05 s through both pairs: 93 probes, longest **0.078 s**, all 200. Process RSS 106 to 108 MB before, 247 to 252 after the solo call, 266 to 299 after a pair (a pair of first pages adds 20 to 47 MB, under the plateau's 50). The six pages' `partition_rows` and `fence_excluded` equal the live code's: 6 of 6 (both counts are 0 on `fence_excluded`, so that count was equal but not exercised).
- **Honest limit:** the measurements ran in fresh processes. The service's own long-lived process is read back in Phase B for 30 minutes; the service has served zero organic window calls in earlier read-backs, so the service heap over a full window call stays unmeasured (row `Z-S338`). A page of about 2 s gives a health probe few ticks (5 at the 0.5 s interval of the memory record; 93 at 0.05 s in CT1). The host marker is new state on the host.

## 3. The order of acts (Phase B)

1. Re-read the live ref (`9d5b712557`), the `.env` (65 keys, `MUSE_CLIENT_ID` absent), host memory, the gateway worker count (1 process), the host md5 walk and the marker's absence; else STOP (a host base other than `9d5b712557` is a STOP: the CTO's hold on the dell1 release `1753c741d9` rests on it).
2. Ledger `nfra-oplgtw-gateway-release-batch6` opened, entry AND sentinel committed first; the live ref's tarball sha256 recorded in it.
3. Restore the gate overlay (section 7) to the live ref's bytes; deploy from `C:/tmp/og-rel-batch6` through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=9d5b712557` under the stale-base guard; no `HALT_OVERRIDE`.
4. Read back against the triggers (section 6); the marker is read and PRINTED (CT2), and on any rollback its absence is printed (`test -e` false).
5. The served read `CODE6_SERVED.json` (the eight arms, with the page equality also on `partition_rows` and `fence_excluded`), the 30-minute service read-back every 60 s with the count of `/mcp` window calls served (zero is said in those words); runbook 7.2 and the manifest standing clauses; ledger closed and its CLOSED time sent to `1.0.0_SA_CTO~Z` for dell1; report.

## 4. Both branches

- A window within one page: complete, `next_cursor` null. A window beyond a page: `window_partial` true and a `next_cursor`; following it reads every dated partition once.
- A second windowed call in flight: `window_read_busy` after the 15 s gate wait, now carried in `absent_reason` (it queues on the gate in a worker thread, not on the loop; a page of about 2 s means the second call usually waits and is then served).
- A ctx without `partition_keys` or `read_account_rows` reads as before; a partition absent from the index answers empty. An unreadable partition refuses the call (fail closed). A stale base at Phase B is refused by the wrapper and Phase A is re-cut.

## 5. Rollback

The live ref's tree redeployed through the same wrapper, PROVEN by a host md5 walk equal to the pre-deploy walk (`ap36_host_md5.json`: 139 of 139 files equal, 0 differ, 0 missing, 0 unexplained). The live ref's S3 tarball `ec2/opal-gateway/opal-gateway-9d5b712557.tar.gz` sha256 and size are recorded in the ledger. **The rollback also removes the host marker `/opt/opal-gateway/.deployed_commit` in the same step** (the old deploy script does not write it; a marker naming the rolled-back release would be false). The base of an older ref is NOT the rollback target.

## 6. Triggers (any one: redeploy the rollback tree at once, remove the marker, file an ARMED row)

Health not 200 within 60 s; a tool of the 27 not answering; the `.env` key count not 65; `tools/list` changing from 103; host md5 differing beyond the released paths; host memory above 85 percent during the read-back (above 80 percent stops the chain); a first page over 55 s; `/health` slower than 5 s DURING a page; the marker not equal to the release sha; and the read-back's own: the service above its baseline by 700 MB, or a median growth over 20 MB per window call after the first.

## 7. Gate lines and the overlay disclosure

The release commit, under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only, printed **0 REFUSE and 0 WARN**; **2 RAISE** lines, one cause: the key-rulings reader could not load (`ModuleNotFoundError: opal_lambda_map`, outside the sparse cone). No registry prelude was needed. The naming gate's inputs (272 paths: 256 added, 16 modified, including the trunk `halt-gate-check.sh`) were laid from `trunk_sha` as an UNCOMMITTED overlay in the release tree (`ap36_overlay.json`); none is in the release commit; Phase B restores every one to the live ref's bytes before the deploy tree's clean check. The superseded release commits `e45922ef75` and `948e8b47cc` remain in the release branch's history under this one.

## 8. The three halves (re-sign on `release_sha` `b6bef4424482e78c6607935dca6a861582e2acc1`, citing CTO msg 35484 and the order's A3)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` `b6bef4424482e78c6607935dca6a861582e2acc1` and this ask's sha256.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` `b6bef4424482e78c6607935dca6a861582e2acc1` and this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` `b6bef4424482e78c6607935dca6a861582e2acc1` and this ask's sha256.
