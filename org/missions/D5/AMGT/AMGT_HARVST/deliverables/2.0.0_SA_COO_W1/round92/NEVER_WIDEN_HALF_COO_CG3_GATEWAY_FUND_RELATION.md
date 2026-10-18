# NEVER-WIDEN -- COO HALF: the `opal-gateway` serves `fund_relation` in `research_reports[]` and the absent-note wording under a field filter (`HVST-cg-3`, round 92, workstream FUNDREL-RELEASE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~01:1xZ UTC. **Authority:** the CTO's round-91 analysis (`ledger/ROUND_ANALYSIS.round91.md` @9bdb466396, msg 7773) item 1 and his cut of `cg-3` (msg 7775: "`REPORT_FIELDS` gains `fund_relation`; ce-5's two files ride the same release; one gateway release, under its own pair, with site Z told first and the stale-base guard on the live commit; released after the silver lands so the field is never served empty"); `HVST-ce-3` merged `b77e08e198`; `HVST-cg-4` merged `290f2e9e6d`; `HVST-cg-2` (the silver rewrite: 3 parts, 353 rows, written 2026-10-18 01:00Z to 01:01Z, read back and re-read by the issuer; its ledger close is a start condition of this order).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`: cut a release branch FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read from `infra/aws/ec2/EC2_MANIFEST.json`, from the instance and from `/opt/opal-gateway/.deployed_commit`; if they differ, STOP; the last report is `d077cef04333500595a7a531ebddc2f43e5f8789` on base `efcc8ae19f`, site Z's batch 7 closed 2026-10-18 00:02:10Z, scratch ref `origin/rel-nfra-og-live-d077cef043`), carry onto it ONLY three files taken from `290f2e9e6d` (`infra/aws/ec2/opal-gateway/app/harvest_research.py`, `infra/aws/ec2/opal-gateway/tests/test_ce3_parts_absent_wording.py`, `infra/aws/ec2/opal-gateway/tests/test_cg4_report_fund_relation.py`), prove `git diff --name-status <live> <release>` lists exactly those three paths and that the `harvest_research.py` diff is exactly two hunks, run the gateway tests, deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set, `DEPLOY_BASE_REF=<the live commit>` under the stale-base guard), then read KMB, CPA, UNH and the five proof names on the served tool before and after.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is what `harvest_get_research` serves in each `research_reports[]` entry. **N = 1 writer** of that entry: `infra/aws/ec2/opal-gateway/app/harvest_research.py::_research_reports` (lines 258-295), `rec = {f: row.get(f) for f in REPORT_FIELDS}` at lines 288 and 292 (the second is the `attached_from` path), the only code that builds an entry. That rule is read: an entry carries exactly the keys of `REPORT_FIELDS` plus `part` (and `attached_from`).

## WHAT THIS CHANGES IN THE WORLD (named)

- **Every `research_reports[]` entry of every security gains one key, `fund_relation`**, with the value stored in its silver row: one of `holding`, `candidate`, `initiate`, `interest`, `template`, `unclassified`, `none`. After `HVST-cg-2` all 353 served reports carry a value (the issuer's read of the bucket, 2026-10-18 01:0xZ: `holding 121, candidate 14, initiate 2, interest 2, template 1, none 213`); an entry whose row predates the key would serve `null`. **No existing key or value changes** (`fund`, `fund_evidence`, `fund_absent_reason`, `period`, ... are served as before; the tuple keeps their order and `fund_relation` sits after `fund_absent_reason`); no gold value, no `parts_absent` sentence changes except the one below.
- **One text changes, in one case (the `ce-3` wording):** with a non-empty `fields` argument and every requested dossier field citing a listed misfiled report, `parts_absent.dossier` names only the requested fields it excluded; with no `fields` argument the sentence is as today. After `HVST-ce-4` no live read triggers it; its proof is the offline test.
- **Who reads it:** every principal of every box that calls `harvest_get_research`; the new key is additive; a consumer that asserts the exact key set of an entry would see one more key (none is known; the CTO's rule is that a consumer meaning "held" reads `fund_relation = holding` only).
- **The service restarts:** `opal-gateway` serves every MCP tool for every principal on every box, about a minute; the seat states the window (start and end, UTC) in the deploy ledger entry.
- **Not touched:** any S3 object, any other tool's code, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner, `fund_form`.

## THE RISK AND ITS CONTROL

The live gateway moves under other fabrics' releases (it moved four times since 2026-10-16). So the release is cut on the live commit read at the cut. **The equality guard:** `git show b77e08e198^1:infra/aws/ec2/opal-gateway/app/harvest_research.py` must equal `git show <live>:<same path>` (md5 `6d9e0dd38166b82943d6834a0ce482b5`, read by the issuer; site Z reports the file unchanged at `d077cef043`); if they differ, STOP, carry nothing, tell the issuer. **The release file:** `git show 290f2e9e6d:<harvest_research.py>` has md5 `596c299597067fe5a8afb8e3493a0ed9` (equal to the file at `HEAD` of `box/dell1` when the issuer read it, 2026-10-18 01:1xZ); between `b77e08e198` and `290f2e9e6d` the file differs by exactly the `REPORT_FIELDS` hunk (2 insertions, 1 deletion, read by the issuer), so the release file is the live file plus the `ce-3` hunk plus that one hunk, and `git diff <live> <release> -- harvest_research.py` must show exactly those two (print it). A second control: the stale-base guard (`DEPLOY_BASE_REF` equal to the live commit).

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch D (the reads and the counts PASS):** the deploy stands; the manifest records the new `deployed_commit` with the previous in `previous_deployed_commit`.
- **Branch F (a gold read differs, a `fund_relation` read differs from the expectation, `/health` fails, the tool-name count differs, or the diff lists a path outside the three or a hunk outside the two):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` (read at the start and printed in `cg3_before.out`), read `/health` 200 and the tool-name count equal to the count before; the order stays `pending`; otherwise report the failure with the read.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the three-path diff, the two-hunk diff and the `<merge>^1` equality printed.
- **C-2.** A deploy ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2), naming the one service, the restart window and `previous_deployed_commit` as the rollback.
- **C-3.** The tests pass on the release branch before the deploy: `test_ce3_parts_absent_wording`, `test_cg4_report_fund_relation`, `test_cd1_dossier_misfiled`, `test_cc1_model_basis`, `test_cc2_research_misfiled`, `test_cc3_ticker_shaped_never_exact_on_name`, `test_og_gt1`, `test_og_gt3`, `test_og_gt4`.
- **C-4.** No Terminal, queue or Bloomberg use; and NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`: it can OOM the host; the unit now has `MemoryMax 1400M`).
- **C-5.** The served reads run through the gateway as an Opal principal and are recorded verbatim with `as_of` and `source_keys`.
- **C-6.** The MCP tool-name count and `/health` are read BEFORE and AFTER, on both branches, and are equal.
- **C-7.** KMB, CPA and UNH: `harvest_get_research` with `fields` `["fund_of_record","last_stated_position"]` is read before and after; every returned gold field entry and key is equal (`content_sha256` and `source_keys` equal); the `research_reports[]` entries are equal except for the added `fund_relation`.
- **C-8 (the proof, CTO msg 7775 item 4).** After the deploy, `ADBE_US_Equity`, `SNPS_US_Equity`, `MNST_US_Equity` and `CLX_US_Equity` serve `fund_relation` `candidate` on the report that names a fund (`ML_FP_Equity` `template`; the control `UNH_US_Equity` `holding`), each recorded verbatim.
- **C-9 (host owner told first).** After the cut and before the deploy the seat writes `cg3_hostowner_note.out` (release commit, the three paths, the intended window) and tells the issuer; the issuer sends it to site Z through `0.0.0_AB_MSTR~DELL1` and sends GO; the deploy waits for that GO and for the host owner's answer; an in-flight release on the host in the window is a STOP.
- **C-10 (the commit reaches the shared lineage).** Right after the deploy the issuer asks `0.0.0_AB_MSTR~DELL1` to push the release ref and tells site Z to land it on its gateway lineage.

## ROLLBACK

Redeploy `previous_deployed_commit` from `EC2_MANIFEST.json` through the same script; no data is written by the act. The silver parts of `HVST-cg-2` stay (the old gateway ignores the column).

## WHAT THIS DOES NOT COVER

Any other gateway change at HEAD; the `fund_form` rebuild (`HVST-cf-3`, `-5`); a shared classifier of gold and silver (row `D1-S49`).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
