# NEVER-WIDEN -- COO HALF: the `opal-gateway` serves the absent-note wording under a field filter (`HVST-ce-5`, round 91, workstream S29-WORDING-SERVE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-17 ~20:1xZ UTC. **Authority:** the CTO's round-90 analysis (`ledger/ROUND_ANALYSIS.round90.md` @307764abfe, msg 7721) item 5 ("ce-5: serve ce-3's wording through a gateway release under its own pair, with site Z told first"); `HVST-ce-3` merged `b77e08e198`.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`: cut a release branch FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read from `infra/aws/ec2/EC2_MANIFEST.json`, from the instance and from `/opt/opal-gateway/.deployed_commit`; if they differ, STOP; the last report is `efcc8ae19f`, site Z's `TO-OG-ap-36` on our `1753c741d9`), carry onto it ONLY the two files of `HVST-ce-3` taken from its merge `b77e08e198` (`infra/aws/ec2/opal-gateway/app/harvest_research.py`, `infra/aws/ec2/opal-gateway/tests/test_ce3_parts_absent_wording.py`), prove `git diff --name-status <live> <release>` lists exactly those two paths, run the gateway tests, deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set, `DEPLOY_BASE_REF=<the live commit>` under the stale-base guard), then read `KMB_US_Equity` and a control on the served tool before and after.

## WHAT THIS CHANGES IN THE WORLD (named)

- **One text changes, in one case.** `harvest_get_research`, when the caller passes a non-empty `fields` argument, every requested dossier field cites a report listed in `MISFILED_REPORTS`, and none is left to serve, says in `parts_absent.dossier` `the requested dossier field(s) <names> cite a misfiled report excluded from the security (see misfiled_fields_excluded)` instead of `every dossier field cites ...`. With no `fields` argument the sentence is exactly as today. **No served value, key or field changes.**
- **After `HVST-ce-4` no KMB field cites a listed report** (its dossier was rebuilt without them), so no live read triggers the new sentence; the proof of the sentence is the offline test, and the live reads prove the release did nothing else. The issuer states this plainly: this release serves a wording whose live trigger no longer exists; it is cut because the CTO ruled it (msg 7721 item 5), and it may be batched with another gateway change that is due rather than restart the host for it alone.
- **The service restarts:** a restart of `opal-gateway`, which serves every MCP tool for every principal on every box, about a minute; the seat states the window (start and end, UTC) in the deploy ledger entry.
- **Not touched:** any S3 object, any other tool's code, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner.

## THE RISK AND ITS CONTROL

The live gateway moves under other fabrics' releases (it moved three times since 2026-10-16). So the release is cut on the live commit read at the cut; `git show b77e08e198^1:<harvest_research.py>` must equal `git show <live>:<harvest_research.py>` (md5 `6d9e0dd38166b82943d6834a0ce482b5` at `efcc8ae19f`, read by the issuer); if they differ, STOP, carry nothing, tell the issuer. A second control: the stale-base guard (`DEPLOY_BASE_REF` equal to the live commit).

## BOTH BRANCHES

- **Branch D (the reads and the counts PASS):** the deploy stands; the manifest records the new `deployed_commit` with the previous in `previous_deployed_commit`.
- **Branch F (a read differs, `/health` fails, the tool-name count differs, or the diff lists a path outside the two):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` (read at the start and printed in `ce5_before.out`), read `/health` 200 and the tool-name count equal to the count before; the order stays `pending`; otherwise report the failure with the read.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the two-path diff and the `<merge>^1` equality printed.
- **C-2.** A deploy ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2), naming the one service, the restart window and `previous_deployed_commit` as the rollback.
- **C-3.** The tests pass on the release branch before the deploy: `test_ce3_parts_absent_wording`, `test_cd1_dossier_misfiled`, `test_cc1_model_basis`, `test_cc2_research_misfiled`, `test_cc3_ticker_shaped_never_exact_on_name`, `test_og_gt1`, `test_og_gt3`, `test_og_gt4`.
- **C-4.** No Terminal, queue or Bloomberg use; and NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`: it can OOM the 1.8 GB host; fix pending).
- **C-5.** The served reads run through the gateway as an Opal principal and are recorded verbatim with `as_of` and `source_keys`.
- **C-6.** The MCP tool-name count and `/health` are read BEFORE and AFTER, on both branches, and are equal.
- **C-7.** KMB and the control `CPA_US_Equity`: `harvest_get_research` with `fields` `["fund_of_record","last_stated_position"]` is read before and after; every returned field entry and key is equal (the `content_sha256` and the `source_keys` are equal).
- **C-8 (host owner told first).** After the cut and before the deploy the seat writes `ce5_hostowner_note.out` (release commit, the two paths, the intended window) and tells the issuer; the issuer sends it to site Z through `0.0.0_AB_MSTR~DELL1` and sends GO; the deploy waits for that GO and for the host owner's answer; an in-flight release on the host in the window is a STOP.
- **C-9 (the commit reaches the shared lineage).** Right after the deploy the issuer asks `0.0.0_AB_MSTR~DELL1` to push the release ref and tells site Z to land it on its gateway lineage.

## ROLLBACK

Redeploy `previous_deployed_commit` from `EC2_MANIFEST.json` through the same script; no data is written by the act.

## WHAT THIS DOES NOT COVER

Any other gateway change at HEAD; a silver or gold rebuild; the corpus-wide `fund_form` object.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
