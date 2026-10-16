# NEVER-WIDEN -- COO HALF: the `opal-gateway` serves the three D1-S29 fixes (`HVST-cc-7`, round 88, workstream S29-SERVE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-16 ~16:5xZ UTC. **Authority:** the CTO's round-87 analysis (`ledger/ROUND_ANALYSIS.round87.md`) rulings on `D1-S29` as corrected by ERRATUM 1 (msg 6780) and ERRATUM 2 (msg 6843); the close condition of `REMEDIATION_v19` (the surfacing seat reads each defect on the SERVED data).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, after `HVST-cc-1`, `-2` and `-3` are merged (`006828d8d5`, `44a1048df9`, `0ce056da15`): cut a release branch FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read from `infra/aws/ec2/EC2_MANIFEST.json` and the instance), carry onto it ONLY the six files of the three cells, prove the diff against the live commit lists exactly those six paths, run the gateway tests, deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set, `DEPLOY_BASE_REF` as the script requires), then read the three names on the served tools and write `cc7_served.out`.

## WHAT THIS CHANGES IN THE WORLD (named)

- **Three read tools change what they serve, for every caller of the gateway:**
  - `harvest_get_fundamentals(kind="model")`: every served figure gains two keys, `basis` (the producer's value, or None) and `figure_claim` (None except for `IS_DIL_EPS_CONT_OPS`, whose claim says it is NOT the reported diluted EPS). Additive; no existing key is removed or reordered.
  - `harvest_get_research`: the response gains `misfiled_reports_excluded` (a list, `[]` for every security but KMB) and KMB's `research_reports` no longer holds `fbd50086c4065785` and `1a3b56044db679a5`, which the response names with their reason. A key's `denominator_note` gains a sentence only when something is excluded or attached.
  - `harvest_resolve_security`: a query that is 1 to 5 capital letters (with an optional `.` or `-` and 1 to 2 letters) matching no ticker slot and found only as the start of a company NAME answers `candidates` where it answered `exact`. Measured live: `PG` answers `exact` PG&E today; `PCG`, `PG&E`, `Kimberly Clark`, lowercase `visa` are unchanged.
- **The service restarts:** a restart of `opal-gateway` on `i-07dccb1615503ac99` (the instance named in the last release record `mq_pf9_bundle_only_gateway_release`), which serves every MCP tool of the gateway for every principal; a brief interruption is the cost.
- **Not touched:** any S3 object, any other tool's code, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner.

## THE RISK THE ACT CARRIES AND ITS CONTROL

HEAD of `box/dell1` holds gateway changes of other seats that are not released. A deploy from HEAD would ship them. So the order cuts the release on the LIVE base and proves by `git diff` that only the six paths differ; any other path stops the act. This is the whole control and it is checked on the seat's output (`cc7_before.out`), not on its word.

## BOTH BRANCHES

- **Branch D (the three served reads PASS):** the deploy stands; the issuer asks `4.0.0_SA_CRO~DELL1` (the surfacing seat) to read the three names itself; the manifest records the new `deployed_commit` with the previous one in `previous_deployed_commit`.
- **Branch F (any served read FAILS, the health check fails, or the diff lists a path outside the six):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` from `EC2_MANIFEST.json` (read at the start and printed in `cc7_before.out`), read `/health` 200 and the tool-name count before and after equal (127 at the last release record), and the order stays `pending`; otherwise the failure is reported to the issuer with the read.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the six-path diff printed.
- **C-2.** A deploy ledger entry is open at the start and closed at the end (NEVER-2), naming the one service; a half-landed deploy is finished in-session or rolled back and escalated.
- **C-3.** The gateway tests listed in the order pass on the release branch before the deploy.
- **C-4.** No Terminal, queue or Bloomberg use (C-i stands; this act does not touch Bloomberg).
- **C-5.** The served reads are run through the gateway as an Opal principal and recorded verbatim; a read answered from a cache is not a read (the seat prints each response's `as_of` and `source_keys`).

## ROLLBACK

Redeploy `previous_deployed_commit` from `infra/aws/ec2/EC2_MANIFEST.json` through the same script; no data is written by the act, so nothing else needs undoing.

## WHAT THIS DOES NOT COVER

A silver rebuild for KMB; adding Procter & Gamble or `KIMBERA MM` to the universe; the `modelSheet.ts` label; any other gateway change at HEAD.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
