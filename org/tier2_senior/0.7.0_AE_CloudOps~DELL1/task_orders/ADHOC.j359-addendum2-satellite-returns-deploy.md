# pipeline-override: J359 is a REMOTE JOB (/remote-drive; Andrew-directed 2026-10-14), not a registered project: no PRD, no decomposition, no tree. The deploy leg of its second never-widen pair rides one CloudOps ADHOC order, on ADHOC.j359-satellite-characteristics-deploy in this folder (the first pair's leg, closed 6/6) and the MDPF_CANON deploy precedents.
<task_order id="ADHOC.j359-addendum2-satellite-returns-deploy">
<to_id>ADHOC.j359-addendum2-satellite-returns-deploy</to_id>
<issued_by>2.0.0_SA_COO~J1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-14</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (Andrew-directed; start by 20:15Z or after the re-seat; the portal deletion waits on this order's served read)</priority>

<title>J359 addendum 2: cot-satellites-characteristics-producer serves each satellite's trailing returns as the sleeve-weighted realized returns of the underlying Opal models blended with GLD -- one function build at a pin, one read grant, a dry-run and ONE driven invoke, read back against the spec table</title>
<context>
THE PAIR IS SIGNED. Read both first; their sections 1, 2, 3, 6 and 7 (COO) and conditions C1 to C5 (CTO) are this order's acts, blast radius, proofs and branches:
- COO half: `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/NEVER_WIDEN_J359_ADDENDUM2_SATELLITE_RETURNS_COO_HALF.md` @`5500bce348`, sha256 `800adb5434b6225e01ff6c1b05a395f61d85f80f393b783a217cbeba318a0740` (on origin `wk-remote-J359b`; `git fetch origin wk-remote-J359b`, then `git show origin/wk-remote-J359b:<path>`);
- CTO half: `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_J359_ADDENDUM2_SATELLITE_RETURNS_20261014.md` @`675488ce32` (box/dell1).
The spec the numbers come from: `org/tier1_exec/4.0.0_SA_CRO/deliverables/J359_SATELLITE_FACTSHEET_EDITS_SPEC_20261014.md` addendum 2 @`0c6d3d2f94` (Andrew's words are inside).

THE BUILD: the producer `data/assets/scripts/gold/build_satellites_characteristics.py` at commit `7337fdfa6d` (origin `wk-remote-J359b`, `git ls-remote origin refs/heads/wk-remote-J359b` tip `5500bce348` carries it). Its one new S3 key literal is registered (legacy_addresses row `yang-platinum-model-portfolio-benchmarks`, @`724b84f846`), so the naming gate passes. The issuer owns landing the producer file on box/dell1 afterwards; YOU build at the pin and commit ONLY the `.tf` patch to box/dell1 (as in the first leg). The IAM edit is `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/J359_evidence2/benchmarks_read_grant.tf.patch` (sha256 `0391a7d9813e66ec9d649f3f2e742320e93344ef8259da501ea1b96a7d41d738`, one Resource element, `git apply --check` clean against box/dell1 at 20:00Z).

NOW DEPLOYED (read 20:01Z): function `CodeSha256` `mpFb3up8mjaS9cHDqlFdAXtIjePtRhJV1kXvCeBkewA=` (pin `efb3f6550f`), artifact key `cot-pipeline/cot-satellites-characteristics-producer.zip` VersionId `3yaAgYL1ZY9OElyISnHodcGLE7nn0TPo`, served `characteristics.json` VersionId `6z8c7qDDQTd2Q9k8qSoPpO78CxlsWAgZ` (18:57:08Z, 66835 B). Read the live ones at the cut: those are the rollback pins.
</context>

<scope>
1. Edit no source file EXCEPT `infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf`: the one element and its comment lines, from the patch. Open a deploy ledger (NEVER-2) in `org/critical_paths/change_management/` BEFORE the first act, slug `j359-addendum2-satellite-returns-deploy-dell1-20261014`.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. Both halves are SIGNED, read from the two files above.
   b. **The clock (CTO C3).** Start only if at least 45 minutes remain before 21:00Z (so, by 20:15Z); else WAIT until after the re-seat. No leg is left open across 21:00Z: if a leg cannot finish, roll back per section 4 before 21:00Z and report.
   c. `wk-remote-J359b` is on origin at a tip carrying `7337fdfa6d`. Build at that commit itself; do NOT take the producer into box/dell1.
   d. The five packaged members at the pin equal the COO half s.3 candidate column: `build_satellites_characteristics.py` `c2fa6061...`, `etf_positioning_gold.py` `db672658...`, `etf_classifications_dynamodb.py` `92b64d97...`, `lambda_function.py` `76a19fea...`, `trading_calendar.py` `9bc467c6...`. A differing member is a STOP: report it, do not build.
   e. No open deploy sentinel names `cot-satellites-characteristics-producer` or `platinum/satellites/` other than this order's (read `org/critical_paths/.open_deploys/` in EVERY live worktree; print the per-tree denominator).
3. **ORDER OF ACTS:**
   a. **Before print.** The function's `CodeSha256`, `LastModified`, `Role`, `Runtime`, `Layers`, `Timeout`, `MemorySize`; the artifact key's CURRENT version: DOWNLOAD that exact version's bytes, hash them, keep them as the rollback copy; the rule (`cron(25 13 * * ? *)` ENABLED); the role's policy verbatim; the served key's CURRENT VersionId, its bytes saved locally; `positioning_data.json` `data_as_of`, `model_portfolio_benchmarks.json` `data_as_of` and LastModified, `registry.json` and `holdings.json` LastModified. **The drift table:** each member of the deployed sidecar's `modules` against `git show <pin>:<path>`; expect SAME for four and DIFFERS only for the producer. **The Bloomberg-sourced set:** every `source == bbg` ticker in the served `tickers` block and its served `returns`.
   b. **D1.** `python infra/aws/lambda/cot-pipeline/cot-satellites-characteristics-producer/build_package.py --pin 7337fdfa6d --out <scratch outside the repo>`; read its sha256 and sidecar. Upload the zip to the artifact key with the `content-sha256` metadata form the module uses; read the new version back and compare the metadata with the zip's hash BEFORE planning. Apply the patch, commit that ONE `.tf` file with `safe-commit.sh`, then ONE targeted plan on `module.cot_satellites_characteristics_producer` and `aws_iam_role_policy.cot_satellites_characteristics_producer_s3`. The plan must show exactly the function's code change and the one added `Resource` element, and NOTHING else (CTO C1); anything more: STOP, report, do not apply. Then `safe-apply` with the same targets. After: `CodeSha256` equals the zip's sha256; every module's sha256 in the new sidecar equals the pin's blob; the policy carries the benchmarks element and no other change; the unscoped re-plan is clean.
   c. **D2, the dry-run.** Invoke ONCE with `{"dry_run": true}` and `--cli-read-timeout 0`: `rc 0`, "DRY RUN -- nothing written to S3", `OK: every satellite has sleeves and blended model returns, 9 satellite(s)`. The served VersionId UNCHANGED. A refusal or `AccessDenied` on the benchmarks object is Branch B before any write: the grant is the first suspect.
   d. **D3, the ONE driven invoke.** Event `{}`, `--cli-read-timeout 0`, ONCE. Read the response and log; the served VersionId MOVED off the one read at the cut; `inputs.benchmarks_as_of` present; `coverage` absent from every satellite.
   e. **The served read (the acceptance).** Read the served `characteristics.json` by exact key. Per satellite and window (1D, WTD, MTD, 1M, QTD, 1Q, YTD, 1Y), `returns` equals the table below to 2 dp for the inputs the run read (`inputs.benchmarks_as_of`, `inputs.bbg_as_of`). If those are NOT 2026-10-13, re-derive the table with `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/J359_evidence2/verify_producer_returns.py` over that day's objects and compare with THAT, never with the table. Also: `fee`, `yield`, `duration`, `beta`, `total_weight`, `sources` and the whole `tickers` block equal the pre-deploy served values (print the denominators); Satellites 90 and 98 `returns` equal the served ULT model's `returns[w].model`.
      | Satellite | g | 1D | WTD | MTD | 1M | QTD | 1Q | YTD | 1Y |
      |---|---|---|---|---|---|---|---|---|---|
      | 15 | 0.0803 | -0.01 | -0.01 | 0.51 | -0.91 | 0.51 | -0.47 | 0.46 | 1.93 |
      | 30 | 0.0698 | -0.01 | -0.03 | 0.56 | -0.93 | 0.56 | -0.44 | 1.72 | 3.42 |
      | 40 | 0.0593 | -0.01 | -0.06 | 0.60 | -0.96 | 0.60 | -0.40 | 3.01 | 4.95 |
      | 50 | 0.0488 | -0.01 | -0.09 | 0.65 | -1.00 | 0.65 | -0.36 | 4.33 | 6.51 |
      | 60 | 0.0383 | -0.01 | -0.13 | 0.69 | -1.03 | 0.69 | -0.32 | 5.68 | 8.10 |
      | 70 | 0.0294 | -0.02 | -0.17 | 0.75 | -1.12 | 0.75 | -0.43 | 6.66 | 9.61 |
      | 80 | 0.0204 | -0.02 | -0.21 | 0.82 | -1.21 | 0.82 | -0.55 | 7.66 | 11.14 |
      | 90 | 0 | -0.04 | -0.25 | 0.89 | -1.13 | 0.89 | -0.78 | 8.37 | 12.15 |
      | 98 | 0 | -0.04 | -0.25 | 0.89 | -1.13 | 0.89 | -0.78 | 8.37 | 12.15 |
   f. **CTO C2, the windows.** At the run's `bbg_as_of`, for EVERY `source == bbg` ticker in the served `tickers` block (today GLD), compute its windows under the DEPLOYED rule (`etf_positioning_gold.py` at `102b2b29d3`) and the pin's over the same history, as `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/J359_evidence/bbg_windows_probe.py` does (read-only; it takes the served characteristics file path); print both side by side and the windows that moved. A move not explained by a changed input is Branch B.
   g. **CTO C4, partial sleeves.** For each satellite and window, print `contributors.returns.windows[w].models` beside the satellite's registry sleeve codes (`registry.json` `books[].constituents[].book`). NAME every window built from fewer than all of its sleeve models: that is Branch A. It is Branch B only if a model present in the benchmarks object at the run is absent from `models`.
   h. **After print.** Re-read: the function configuration (only `CodeSha256`, `LastModified` changed), the artifact key's versions (one new), the served key (one new version, bytes saved beside the prior's), the rule and target (unchanged), the role's policy (one added element). Report every other difference; deploy NOTHING from that list.
4. **Rollback** if (b) shows an unexpected plan, (c) refuses, or (d) to (g) show any delta beyond what the pair names: re-upload the saved prior zip bytes to the artifact key with the same metadata form, reverse the patch and apply the same targets, read back the prior `CodeSha256`; restore the served key from its recorded prior VersionId by `copy_object` (a NEW version, never a delete), read back byte-equal to the saved copy; report.
5. Close the ledger carrying the invoke's request id, the served object's new LastModified and VersionId, and three read values: Satellite 90 `1Y` (12.15), Satellite 40 `YTD` (3.01) and Satellite 15 `1Y` (1.93) on 2026-10-13 inputs. The read through the SERVED ROUTE is the issuer's open leg: name it so. Report to `2.0.0_SA_COO~J1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`. DO NOT message the portal DT seat; the issuer relays the verdict.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf
infra/aws/lambda/cot-pipeline/cot-satellites-characteristics-producer/cot-satellites-characteristics-producer.BUILD_MANIFEST.json
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the five member sha256 at the pin printed beside the COO half's candidate column, then the drift table against the deployed sidecar, then the package build's printed sha256 and the new sidecar</invocation>
  <expect>all five members equal the candidate column (a differing member = STOP before the build); the drift table lists DIFFERS only for the producer; every module's sha256 in the new sidecar equals the pin's blob</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the artifact upload read-back, the targeted plan, safe-apply -target, then the function configuration, the role policy and an unscoped plan read back</invocation>
  <expect>the new artifact version's metadata equals the zip's hash; the plan moves only the function's code and one added benchmarks Resource element; CodeSha256 equals the zip's sha256; the unscoped re-plan is clean; the rule and its target unchanged</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the dry-run invoke, then the served key's VersionId, then the ONE driven invoke with {}, then the served characteristics.json read against the table in scope 3e, then the windows comparison of 3f and the partial-sleeve print of 3g</invocation>
  <expect>dry-run rc 0 and the served VersionId UNCHANGED; the driven invoke 200 with no FunctionError and the VersionId MOVED; every satellite's eight windows equal the table to 2 dp (or the re-derived table for the run's as_of); Satellites 90 and 98 equal ULT's served returns; scalars, total_weight, sources and the tickers block equal the pre-deploy ones; coverage absent; for every bbg-sourced ticker the old and new windows are printed and any move is named with its cause; every window built from fewer than all its sleeve models is named</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the before and after prints, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger with the rollback pins (prior artifact version and hash, prior served VersionId and its saved bytes); only CodeSha256, LastModified and the one policy element differ; the clock respected (no leg open across 21:00Z); the ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
