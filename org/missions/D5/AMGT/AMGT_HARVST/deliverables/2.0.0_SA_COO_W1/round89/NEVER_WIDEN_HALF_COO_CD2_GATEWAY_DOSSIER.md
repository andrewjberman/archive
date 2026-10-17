# NEVER-WIDEN -- COO HALF: the `opal-gateway` stops serving dossier fields built from a misfiled report (`HVST-cd-2`, round 89, workstream S29-SERVE-2)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-17 ~12:1xZ UTC. **Authority:** the CTO's round-88 analysis (`ledger/ROUND_ANALYSIS.round88.md` @07264722d8, msg 7491) item 1 ("The gateway release is under its own pair"); the CVO's grade that `D1-S29` (b) is NOT fixed (`ADJUDICATION_v82.md`); the close condition of `REMEDIATION_v19` (the surfacing seat reads the defect on the SERVED data).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, after `HVST-cd-1` is merged: cut a release branch FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read from `infra/aws/ec2/EC2_MANIFEST.json` and from the instance; if they differ, STOP), carry onto it ONLY the two files of `HVST-cd-1` (`infra/aws/ec2/opal-gateway/app/harvest_research.py` and `infra/aws/ec2/opal-gateway/tests/test_cd1_dossier_misfiled.py`), prove the diff against the live commit lists exactly those two paths, run the gateway tests, deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set, `DEPLOY_BASE_REF` as the script requires), then read `KMB_US_Equity` and a control security on the served tool and write `cd2_served.out`.

## WHAT THIS CHANGES IN THE WORLD (named)

- **One read tool changes what it serves, for every caller of the gateway:** `harvest_get_research` drops from `dossier_fields` and `continuation_fields` any field whose entry cites a report listed in `MISFILED_REPORTS` for that same security (today only the two Kimberly-Clark de Mexico files on `KMB_US_Equity`), and names the dropped fields in a new response key `misfiled_fields_excluded` (a list, `[]` for every security but KMB). A `denominator_note` gains a sentence only when a field is dropped. Additive for every other security; for KMB, `fund_of_record` and `last_stated_position` stop being served (the order's design choice: a field is dropped whole when any string in it names a listed report).
- **The service restarts:** a restart of `opal-gateway`, which serves every MCP tool of the gateway for every principal on every box; a brief interruption is the cost, and the seat states the restart window (start and end, UTC) in the deploy ledger entry.
- **Not touched:** any S3 object, any other tool's code, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner.

## THE RISK THE ACT CARRIES AND ITS CONTROL

HEAD of `box/dell1` holds gateway changes of other seats that are not released, and the live gateway moves under other seats' releases (it moved twice during round 88). A deploy from HEAD would ship what is not ours. So the release is cut on the LIVE base and the `git diff <live> <release> --name-only` lists exactly the two paths; any other path stops the act. A second control: `git show <HVST-cd-1 merge>^1:<harvest_research.py>` equals `git show <live>:<harvest_research.py>` (the live file is exactly the file `HVST-cd-1` started from); if not, STOP. Both are checked on the seat's output (`cd2_before.out`), not on its word.

## BOTH BRANCHES

- **Branch D (the served reads PASS):** the deploy stands; the issuer asks `4.0.0_SA_CRO~DELL1` (the surfacing seat) to read KMB itself; the manifest records the new `deployed_commit` with the previous one in `previous_deployed_commit`.
- **Branch F (a served read FAILS, the health check fails, the tool-name count differs, or the diff lists a path outside the two):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` from `EC2_MANIFEST.json` (read at the start and printed in `cd2_before.out`), read `/health` 200 and the tool-name count equal to the count before, and the order stays `pending`; otherwise the failure is reported to the issuer with the read.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the two-path diff printed and the `<merge>^1` equality printed.
- **C-2.** A deploy ledger entry is open at the start and closed at the end (NEVER-2), naming the one service, the restart window and `previous_deployed_commit` as the rollback; a half-landed deploy is finished in-session or rolled back and escalated.
- **C-3.** The gateway tests listed in the order pass on the release branch before the deploy.
- **C-4.** No Terminal, queue or Bloomberg use.
- **C-5.** The served reads are run through the gateway as an Opal principal and recorded verbatim; a read answered from a cache is not a read (the seat prints each response's `as_of` and `source_keys`).
- **C-6 (the CTO's condition on the last pair, carried).** The MCP tool-name count and `/health` are read BEFORE and AFTER, on BOTH branches, and must be equal; a different count after the deploy means a path outside the two shipped: Branch F, roll back.
- **C-7.** The control security's `dossier_fields` count and `continuation_fields` count are read before and after the deploy and are equal, and its `misfiled_fields_excluded` is `[]`.

## ROLLBACK

Redeploy `previous_deployed_commit` from `infra/aws/ec2/EC2_MANIFEST.json` through the same script; no data is written by the act, so nothing else needs undoing.

## WHAT THIS DOES NOT COVER

A silver or gold REBUILD that re-derives the KMB dossier without the misfiled reports (the true remedy; a later cell); adding `KIMBERA MM` to the universe; any other gateway change at HEAD.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
