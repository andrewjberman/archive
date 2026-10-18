# NEVER-WIDEN ASK -- `OG-ap-39` (amendment A3) -- the round-42 seventh batched gateway release: the `absent_reason` codes documented in the client tools' served descriptions (`OG-en-28`) and the db3 test that reads the worktree (`OG-en-27`); no page-size change

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-39.round-42-seventh-batched-release-page-size.md` with its amendments A1 to A4 (GO for Phase A: msg 35608; GO for the RE-CUT: msg 35625).
Release: `release_sha` = `aa2efa2cf3dee82030c00f85425f686132adcf4a`, cut on the live ref `base_sha` = `4257a2aa42e5366270b3652f21dba90872dbb1e0` (dell1's `AMGT_HARVST` `HVST-cg-3` release, deployed 2026-10-18 at 02:06:03Z, its ledger `harvst-cg3-gateway-fundrel-release` CLOSED 2026-10-18T02:13:41Z), from `trunk_sha` = `23efa6e1f4f6873e66d812c6e8b0e1a0ba0ac0c4`.
**`harvest_research.py` (CT4, named):** the blob `574959b682d4a13a0a429c45fa00b77b6caa2ab5` (md5 `596c299597067fe5a8afb8e3493a0ed9`, 33817 bytes), the CTO-verified blob of the live ref `4257a2aa42` (msg 35603), is CARRIED UNCHANGED: the live ref's blob, the release's blob and trunk's blob are the same object. The release does not touch the file; Phase B reads the host md5 of `app/harvest_research.py` and prints it beside the blob's, and a mismatch is a rollback trigger.
**This ask SUPERSEDES the first cut `43a6659615` and its ask (sha256 `942adaf1e59e`; the COO half was signed on it (`49e5c88c20`); that signature is on the first cut's bytes, and no half is carried to this ask):** the CVO's row `Z-S385` found one docstring (the `client_get_fees` note) claiming an unmeasured zero ("the empty list is a true zero"); `OG-en-30` rewords it ("no fee rows were found in the source, not that the fees were nil"), and the release is re-cut on the new trunk; nothing else differs (the second file, `tests/test_og_db3.py`, is the same blob; the live ref and the harvest blob are the same).
**What changed since the order was cut:** the sweep `OG-ev-6` CHOSE 30 partitions per page (`PAGE_SWEEP.json`), so `OG-en-29` is superseded and this release changes NO page size; the take list is TWO files (amendment A3).

## 1. The diff, by file (`git diff 4257a2aa42 aa2efa2cf3`: 2 files, 15 insertions, 31 deletions)

- `app/tools.py` (`OG-en-28`): 5 hunks, 5 insertions and 5 deletions, ALL inside docstrings. The description of `client_resolve_account`, `client_get_holdings`, `client_get_transactions`, `client_get_allocation` and `client_get_fees` gains the `absent_reason` codes that tool can return (for example `window_read_busy`, `no_partition_at_as_of`, `no_model_assignment_49f`). **Proven, not asserted:** the syntax trees of the live file and the release file are EQUAL once the docstrings are blanked, and the two files carry the same 43 import statements: no code, no signature and no import moves.
- `tests/test_og_db3.py` (`OG-en-27`): 4 hunks, 10 insertions and 26 deletions; the test now reads the CURRENT text of the deploy script in the tree it runs in and consults no git history (the earlier version walked the history of the script and failed in a release tree).
- NOT in the release (the check counts them at 0): `client_adapter_bd49f.py`, `client_core.py`, `typed_scope.py`, `etfs_rivals_flow.py`, `destructive_ops.py`, `deploy-to-ec2.sh`, `deploy/opal-gateway.service`, `EC2_MANIFEST.json`, the catalog and `app/refs/`, Terraform, and `harvest_research.py` (carried).
- **A seam, stated:** the seam script classes one edge STOP: `app/tools.py` imports `app/destructive_ops.py`, which differs between the live ref and trunk and is not in the release. It is not a MISSING seam (the module is in the base), and the taken `tools.py` is code-equal to the live one (above), so no dependency moves; the applier read it as not a STOP and names it here so the signers can rule otherwise.
- Test results (release tree, then the live ref in a second tree): `test_og_db3` 3 passed; the seventeen window files (`test_og_en13`, `en14`, `en15`, `en17` to `en24`, `test_og_cl2`, `test_og_rv2`, `test_og_db3`, `test_og_en9`, `test_og_sv1`, `test_og_sv2`) 63 passed and 1 failed in BOTH orders, the one failure `test_og_sv1.py::test_ogsv1_ac01`, which reads a worker deliverable file (`0.9.0_WK_NFRA_OPLGTW~113/SV1_ROWS.json`) absent from both trees and fails the same way at the live ref (carried). The full suite: 74 failed and 1065 passed in the release tree; 75 failed and 1064 passed at the live ref; the two failing sets differ in exactly ONE test, `test_og_db3.py::test_ogdb3_ac03`, which FAILS at the live ref and PASSES in the release tree (the point of `OG-en-27`); nothing fails in the release tree that passes at the live ref. `bash -n deploy-to-ec2.sh` rc 0 and `--preflight-only` prints `PREFLIGHT OK`. The host-shaped import check: 5 of 6 modules import, `server` stops on a missing env var (the same as in earlier releases), 0 reads (run on the first cut; the second differs by docstring text only). The live ref's failing set is from the run on the same ref `4257a2aa42` made earlier the same day.

## 2. The widening, stated plainly

- NO new IAM, NO new env key, NO tool added or removed (`tools/list` stays 103 tools with the same 103 names), NO behaviour change: the answers are equal tool by tool (below). The reworded `client_get_fees` note tells a caller that an empty fee list means no rows were found in the source, not that the fees were nil.
- **The one thing a caller sees:** the descriptions of five client tools, served by `tools/list`, are longer by the `absent_reason` notes. A client that reads descriptions reads more text; no argument, no return shape and no refusal changes.
- **The 27-tool read, live code against candidate (CTO CT1, as for `OG-ap-38`):** each of the 27 tools in its own fresh process under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb` (`systemd-run --scope -p MemoryMax=1400M`, `oom_score_adj` 1000, wall limit 120 s), once on the live code and once on the candidate, one process at a time, the same fixed arguments (derived once on the live code); answers compared by the sha256 of their canonical JSON (hashes only, in the untracked `W/ap39_tool27.json`): **27 of 27 equal**; failed on both codes 0; answered on the candidate where the live code failed 0; answered on live and refused on the candidate 0; answers that differ 0. `tools/list`: the same 103 names; exactly 5 descriptions differ (the five client tools above).
- **Honest limits:** the measurements ran in guarded fresh processes, not in the service; the service has served zero window calls in earlier read-backs, so `Z-S338` stays open; the gateway unit's limits (MemoryMax 1400M and the rest) are NOT changed by this release.
- The 429 limit, the browser exemption roster, the page size (30) and the allocation weight unit are NOT changed.

## 3. The order of acts (Phase B)

1. Read every open gateway ledger first (the COO's C2: at this Phase A, 45 open sentinels, six of which mention the gateway: `nfra-mcportal-c17-gitstate-release`, `-c17r2-release`, `-cp2-release`, `-gw-release`, `-pc-release` and `-pf-bundle-release`, all opened 2026-10-10 to 2026-10-16 against bases the host has since left; none is in flight on the host; re-read at Phase B). Re-read the live ref (`4257a2aa42`; a manifest or host base other than it is a STOP), the `.env` (65 keys, `MUSE_CLIENT_ID` absent), host memory, the gateway at one process, the host md5 walk against `4257a2aa42` (139 of 139 at this Phase A), `NRestarts`, the marker, the unit limits.
2. Ledger `nfra-oplgtw-gateway-release-batch8`, entry AND sentinel committed first; the live ref's tarball sha256 recorded in it.
3. Restore the gate overlay (section 7); deploy from `C:/tmp/og-rel-batch8` through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=4257a2aa42` under the stale-base guard; no `HALT_OVERRIDE` (a halt-gate stop is reviewed and acked, never overridden).
4. Read back against the triggers (section 6); the marker, the unit limits and the `harvest_research.py` host md5 beside its blob are read and PRINTED.
5. The served read `CODE8_SERVED.json`: the 27-tool read UNDER THE GUARD (27 of 27), `served_notes` read from the INSTALLED code's tool registry in a fresh guarded process, the arms, the host clock (`chronyc tracking`) and `systemctl --failed` read and printed BEFORE the ledger closes, the 30-minute service read-back every 60 s with `NRestarts` 0 and the count of `/mcp` window calls served (zero is said in those words); runbook 7.2 and the manifest standing clauses; the ledger closed and its CLOSED time sent to `2.0.0_SA_COO~O`; report.

## 4. Both branches

- A client tool's answer is what it was; its description now lists the `absent_reason` codes the tool can return. A tool whose description is not read behaves as before.
- A stale base at Phase B is refused by the wrapper and Phase A is re-cut. The gateway restarts once at the deploy (one brief outage, as every release).

## 5. Rollback

**The live ref's tree, `4257a2aa42`** (dell1's `cg-3` release), redeployed through the same wrapper, PROVEN by a host md5 walk equal to the pre-deploy walk (`ap39_run1/host_md5_before.json`: 139 of 139 files equal, 0 differ, 0 missing). The live ref's S3 tarball `ec2/opal-gateway/opal-gateway-4257a2aa42.tar.gz` is 902884 bytes, sha256 `f59e4b4009cef1afa662f30bcd2caa821d33cf91641fba0fb97366c6f778d33f` (equal to `opal-gateway-latest.tar.gz`, git-ref metadata `4257a2aa42`); it goes into the ledger. The unit is NOT changed by this release, so the rollback changes no unit; it rewrites the marker to the live ref's sha, and the marker and the `harvest_research.py` md5 are read and printed.

## 6. Triggers (any one: redeploy the rollback tree at once, read the marker, file an ARMED row naming `2.0.0_SA_COO~O`)

Health not 200 within 60 s; a tool of the 27 not answering under the guard; the `.env` key count not 65; `tools/list` changing from 103 tools; host md5 differing beyond the released paths (`app/tools.py`); the host md5 of `app/harvest_research.py` not equal to the blob above; host memory above 85 percent during the read-back; `NRestarts` above 0; the unit limits no longer reported (1468006400, 1258291200, 300, cgroup 1468006400); the marker not equal to the release sha; the first window page over 15 s.

## 7. Gate lines and the overlay disclosure

The release commit, under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only, printed NO `REFUSE`, `BLOCKED` or `ERROR` line; one WARN-only commit-gate line: 7 non-ASCII lines in `app/tools.py`, the same 7 the live ref's `tools.py` carries (unchanged by this release); and the pre-commit `comp-pulse diff` advisory printed HOLD lines for OTHER files that share the basename `tools.py` (m365-mcp-gateway, the pydantic layers) citing a 2026-07-31 rename ledger line; the applier read the citation: it is not about this file. The naming gate's inputs (272 paths: 256 added, 16 modified, including the trunk `halt-gate-check.sh`) were laid from `trunk_sha` as an UNCOMMITTED overlay in the release tree (`ap39_run1/ap39_overlay.json`); none is in the release commit; the overlay was restored to the live ref's bytes before the tests (`git status` of the release tree reads 0 lines), and Phase B restores it again before the deploy tree's clean check.

## 8. The three halves (sign ONCE, on `release_sha` `aa2efa2cf3dee82030c00f85425f686132adcf4a`)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` `aa2efa2cf3dee82030c00f85425f686132adcf4a`, on the `harvest_research.py` blob `574959b682d4a13a0a429c45fa00b77b6caa2ab5` and on this ask's sha256.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` `aa2efa2cf3dee82030c00f85425f686132adcf4a` and this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` `aa2efa2cf3dee82030c00f85425f686132adcf4a` and this ask's sha256.
