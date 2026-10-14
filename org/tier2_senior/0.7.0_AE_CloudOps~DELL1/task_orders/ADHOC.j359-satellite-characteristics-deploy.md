# pipeline-override: J359 is a REMOTE JOB (/remote-drive; Andrew-directed 2026-10-14), not a registered project: no PRD, no decomposition, no tree. The deploy leg of its never-widen pair rides one CloudOps ADHOC order on the MDPF_CANON round-2, round-4, round-6 and round-7 precedents (ADHOC.canon-r7-publisher-deploy and its siblings in this folder).
<task_order id="ADHOC.j359-satellite-characteristics-deploy">
<to_id>ADHOC.j359-satellite-characteristics-deploy</to_id>
<issued_by>2.0.0_SA_COO~J1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-14</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (Andrew-directed; the portal promote of the same job waits on this order's served read)</priority>

<title>J359: cot-satellites-characteristics-producer serves the four scalars by the Models' method over the model sleeves, and returns over the holdings that have each window -- one function build at a pin, one read grant, a dry-run and ONE driven invoke, read back against the spec table</title>
<context>
The producer change is `data/assets/scripts/gold/build_satellites_characteristics.py` at commit `efb3f6550f` (branch `wk-remote-J359`, on origin by `git ls-remote origin refs/heads/wk-remote-J359`, tip `d7d9a9ed1a`). It reads one more input, `s3://opal-data-cot/platinum/satellites/registry.json`, so the function's role needs one read grant. The served key that moves is `s3://opal-data-cot/platinum/satellites/characteristics.json` and nothing else.

THE PAIR IS SIGNED. Read both first; their sections 1, 2, 3, 6a and 7 are this order's acts, blast radius, proofs, sequence and both branches:
- COO half: `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/NEVER_WIDEN_J359_SATELLITE_CHARACTERISTICS_COO_HALF.md` @`e1dfba9db8` (on `wk-remote-J359`);
- CTO half: `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_J359_SATELLITE_CHARACTERISTICS_20261014.md` @`2b6f842af2` (on `box/dell1`).
The COO half, the patch, the evidence scripts and the render screenshots live on the branch `wk-remote-J359`, not on `box/dell1`: `git fetch origin wk-remote-J359`, then `git show origin/wk-remote-J359:<repo-relative path>` to read any of them (they are all under `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/` and its `J359_evidence/`). The spec the numbers come from: `org/tier1_exec/4.0.0_SA_CRO/deliverables/J359_SATELLITE_FACTSHEET_EDITS_SPEC_20261014.md` (Andrew's words are inside it).

THE CTO'S THREE CONDITIONS (his message 5687), all binding on this order:
1. The CVO sequence is a STOP: this order's served read must be MET before the portal promote. You do not promote anything; you report the read to the issuer.
2. The served read prints the return windows for EVERY Bloomberg-sourced holding at the driven run's `bbg_as_of`, old rule against new. Any move is named with its cause; an unexplained move is Branch B.
3. No leg straddles tonight's 21:00Z dell1 restart.

What this order carries beyond the precedents (read these):
1. **The `.tf` is your lane, the producer is not changed by you.** The one IAM edit is `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/J359_evidence/registry_read_grant.tf.patch` (on `wk-remote-J359` @`e1dfba9db8`; sha256 `0d85fdc987b825c2...`; the full hash is in the COO half's header paragraph). `git apply --check` is clean against `box/dell1` at the time of writing. It adds ONE resource element, `.../platinum/satellites/registry.json`, to `Sid ReadSatellitesHoldings` (`s3:GetObject` only).
2. **The package moves more than the spec.** Four of five packaged members differ from the deployed manifest (COO half s.3 drift table, pin `102b2b29d3`). The pair accepts that on its measurements: only `compute_returns` could move this producer's output, and GLD's eight windows are identical under both rules at `bbg_as_of 2026-10-13`. THIS ORDER RE-RUNS THAT COMPARISON at the pin you build and at the driven run's `bbg_as_of` (condition 2).
3. The artifact is S3-backed: `module "cot_satellites_characteristics_producer"` (`satellites-characteristics-producer.tf:315`, source `../modules/yang-lambda`) takes the zip at `s3://opal-313476888478-lambda-artifacts/cot-pipeline/cot-satellites-characteristics-producer.zip`. Read live 2026-10-14: current VersionId `1Dw2S3IjFNtmZwZpbAE0p_3o_IMVtRrC`, `content-sha256` metadata `IQP6I8Exn60kZVcI1K8mnmGWModpgOe4UE+EbOFf54c=`, 182727 bytes; the function's `CodeSha256` is the same value. Read the metadata form the module and the last upload actually use, and match it.
4. The rule `cot-satellites-characteristics-producer-daily` (`cron(25 13 * * ? *)` ENABLED) is NOT changed and its target is NOT changed.
</context>

<scope>
1. Edit no source file EXCEPT `infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf`: the one resource element and the comment lines the patch carries. No other line of that file moves. The producer file is taken from `wk-remote-J359` as it is, never edited here. Open a deploy ledger (NEVER-2) in `org/critical_paths/change_management/` BEFORE the first act, slug `j359-satellite-characteristics-deploy-dell1-20261014`; name in it the function, the artifact key, the served key, its prior VersionId, the registry read grant, and the serving path (the scoped route `/api/scoped/satellites/characteristics.json`).
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. Both halves of the pair are SIGNED, read from the two files named in the context (a signature is a line in a commit by that seat).
   b. The clock (CTO condition 3): read the time. Start only if at least 90 minutes remain before 21:00Z; otherwise WAIT and start after the restart. No leg is left open across 21:00Z: if a leg cannot finish, roll back per section 4 before 21:00Z and report. The rule fires at 13:25Z daily; no act starts within 45 minutes before it or while the function is running (read its last invocation).
   c. `wk-remote-J359` is on origin at a tip carrying `efb3f6550f` (`git ls-remote`, then `git merge-base --is-ancestor efb3f6550f <tip>`). AMENDED 2026-10-14 ~18:5xZ by the issuer, on the AE seat's report (msg 5690): the pin IS `efb3f6550f` itself, as the pair names it; do NOT take the producer into `box/dell1`. The naming gate (LGIC_ENFORCE DEC-6) REFUSES the file's new S3 key literal `platinum/satellites/registry.json` on `box/dell1`, and its registered-legacy-address route needs a project home this remote job does not have; no override, no registry row inside this order's paths. `git fetch origin wk-remote-J359`, then build with `build_package.py --pin efb3f6550f` (an immutable commit in the object database is all the builder needs). Read the file AT THE PIN BY CONTENT: it contains `def sleeve_scalars`. The `.tf` patch alone is committed to `box/dell1`. The issuer owns landing the producer file on `box/dell1` afterwards; until then `box/dell1` holds the older producer bytes and the deployed package is ahead of it, which the ledger records.
   d. The five packaged members at YOUR pin equal the COO half's candidate column (print `git show <pin>:<path> | sha256sum` for each): `build_satellites_characteristics.py` `d09589cb...`, `etf_positioning_gold.py` `db672658...`, `etf_classifications_dynamodb.py` `92b64d97...`, `lambda_function.py` `76a19fea...`, `trading_calendar.py` `9bc467c6...`. A member that DIFFERS from that column is a STOP: report it, do not build (the pair signed those bytes, not others).
   e. No open deploy sentinel names `cot-satellites-characteristics-producer` or `platinum/satellites/` other than this order's own. Read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator. The registry producer's 13:15Z fire and the SH-t-24 / HEALGAP acts name nearby keys: read, do not assume.
3. **ORDER OF ACTS (the order is the safety):**
   a. **Before print.** Record: the function's `CodeSha256`, `LastModified`, `Role`, `Runtime`, `Layers`, `Timeout`, `MemorySize`; the artifact key's CURRENT version (expect `1Dw2S3Ij...`): DOWNLOAD that exact version's bytes, hash them, keep them as the rollback copy and attach the hash to the ledger; the rule (`cron(25 13 * * ? *)` ENABLED) and its target input; the role's policy `s3-read-three-inputs-write-satellites-characteristics` verbatim; the served key's CURRENT VersionId (today's at 13:26Z was `C8ZQnQw0ESDdnaIK8iq_f7OFbcW6tble`; read the one at the cut, it is the rollback pin) and keep its bytes locally; `registry.json`'s and `holdings.json`'s LastModified and `positioning_data.json`'s `data_as_of`. **The drift table:** for each member of the deployed sidecar `cot-satellites-characteristics-producer.BUILD_MANIFEST.json` `modules`, the manifest's sha256 against `git show <pin>:<path>`; EQUAL or DIFFERS, and the line stat of each DIFFERS member against `102b2b29d3`; report it. **The Bloomberg-sourced set:** from the served `characteristics.json` `tickers` block, every ticker whose `source` is `bbg` (today GLD only) and its served `returns`.
   b. **D1.** `python infra/aws/lambda/cot-pipeline/cot-satellites-characteristics-producer/build_package.py --pin <the pin> --out <a scratch path outside the repo>` (the package's own procedure; it refuses a moving ref); read its printed sha256 and the sidecar. Upload the zip to the artifact key with the `content-sha256` metadata form the module uses; read the new version back and compare the metadata with the zip's own hash BEFORE planning. Apply the patch (`git apply`), commit that ONE `.tf` file with `safe-commit.sh`, then ONE targeted plan on `module.cot_satellites_characteristics_producer` and `aws_iam_role_policy.cot_satellites_characteristics_producer_s3`. The plan must show exactly: the function's code change (`s3_object_version`, `source_code_hash`) and the one added `Resource` element of the policy, and NOTHING else. Any other attribute moving (a layer, the runtime, the role, the schedule, any other IAM statement): STOP, report, do not apply. Then `safe-apply` with the same targets. After the apply read back: the function's `CodeSha256` equals the zip's sha256; every module's sha256 in the new sidecar equals `git show <pin>:<path>`; the policy carries the `registry.json` element and no other change; the re-plan is clean (unscoped 0-diff).
   c. **D2, the dry-run.** Invoke the function ONCE with the event `{"dry_run": true}` and `--cli-read-timeout 0`. Read the response and the log: `rc 0`, "DRY RUN -- nothing written to S3", `OK: return coverage reconciles and every satellite has sleeves, 9 satellite(s)`. Read the served key's VersionId again: UNCHANGED. A refusal or an `AccessDenied` on `registry.json` is Branch B before any write: report; the grant is the first suspect.
   d. **D3, the ONE driven invoke.** Event `{}` (the scheduled event; no explicit `bbg_as_of`), `--cli-read-timeout 0`, ONCE. Read the response and the log. Then read the served key: the VersionId MOVED off the pin read in (a); `inputs.registry_as_of` is present; `method.renormalised` is true.
   e. **The served read (the acceptance, the CVO's step 3 and CTO condition 1).** Read the served `characteristics.json` by exact key and compare, per satellite, `fee`, `yield`, `duration` and `beta` with the spec table below, to the stated rounding, for the inputs the run read (`positioning_data_as_of` printed in `inputs`). If that as_of is NOT 2026-10-13, re-derive the table with `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/J359_evidence/oracle_check.py` over that day's `positioning_data.json` and compare with that, never with the table. Positive controls: Satellites 90 and 98 duration equal the served ULT model's duration and beta equals ULT's beta; Satellite 70 duration reads the class-share value (3.49 on 2026-10-13). Also: `tickers` block equals the pre-deploy served block for every ticker whose source is `positioning_data` (print the denominator); `coverage.weight_with_value` carries only `returns`; no key `contributors.scalar`.
      | Satellite | fee | yield | duration | beta |
      |---|---|---|---|---|
      | 15 | 0.17 | 4.15 | 3.49 | 0.80 |
      | 30 | 0.20 | 3.82 | 3.53 | 0.88 |
      | 40 | 0.23 | 3.50 | 3.59 | 0.92 |
      | 50 | 0.26 | 3.17 | 3.69 | 0.94 |
      | 60 | 0.29 | 2.84 | 3.86 | 0.95 |
      | 70 | 0.31 | 2.47 | 3.49 | 0.96 |
      | 80 | 0.33 | 2.10 | 2.50 | 0.96 |
      | 90 | 0.36 | 1.85 | 1.92 | 0.97 |
      | 98 | 0.36 | 1.85 | 1.92 | 0.97 |
   f. **CTO condition 2, the windows.** At the driven run's `bbg_as_of`, for EVERY ticker `source == bbg` in the served `tickers` block (today GLD), compute its return windows under the DEPLOYED rule (`etf_positioning_gold.py` at `102b2b29d3`) and under the pin's rule over the same history, as `J359_evidence/gld_probe.py` does for GLD at 2026-10-13 (generalize its ticker list and `as_of`; it is read-only). Print both side by side and the windows that moved. A window that moved is named with its cause (a closed market day for that ticker, C-GAP or C-MMF, read from the rule's own branch); a move with no named cause is Branch B. Also confirm the served ticker's `returns` equals the pin rule's output.
   g. **After print.** Re-read: the function configuration (only `CodeSha256`, `LastModified` changed), the artifact key's versions (one new version), the served key (one new version, its bytes saved beside the prior's), the rule and target (unchanged), the role's policy (one added element). Report every other difference; deploy NOTHING from that list.
4. **Rollback** if (b) shows an unexpected plan, (c) refuses, or (d)/(e)/(f) shows any delta beyond what the pair names: re-upload the saved prior zip bytes (hash in the ledger) to the artifact key with the same metadata form, revert the `.tf` (the patch reversed) and apply the same targets, read back the prior `CodeSha256`; restore the served key from its recorded prior VersionId by `copy_object` (a NEW version, never a delete) and read it back byte-equal to the saved copy; report. The scheduled 13:25Z fire after a rollback runs the prior code on the prior role grant and rewrites the key itself.
5. AMENDED 2026-10-14 ~19:0xZ by the issuer, on Andrew's addendum (spec @9aeef838d6, his words inside: rerun the producer so the numbers refresh): the ledger CLOSES carrying the driven invoke's request id, the served object's new LastModified and VersionId, and three read values from the served object: Satellite 90 duration and beta (1.92, 0.97 on 2026-10-13 inputs) and Satellite 70 duration (3.49). The read through the SERVED ROUTE (a cached copy still serving old numbers is not done) is the issuer's, after your report; do not close the ledger as "done" on the S3 read alone: close it with the S3 read and name the route read as the issuer's open leg. If the served object is still the 13:26:02Z one after the invoke, that is Branch B: report before anything else.
   Close the ledger. Report to `2.0.0_SA_COO~J1` with each criterion's output (the served read's table, the windows comparison, every VersionId), and the change after the fact to `0.0.0_AB_MSTR~DELL1`. DO NOT tell the portal DT seat anything: the issuer relays the served-read verdict.
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
  <expect>all five members equal the COO half's candidate column (a differing member = STOP before the build); the drift table lists DIFFERS only for the four members the pair names; every module's sha256 in the new sidecar equals the pin's blob</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the artifact upload read-back, the targeted plan, safe-apply -target, then the function configuration, the role policy and an unscoped plan read back</invocation>
  <expect>the new artifact version's metadata equals the zip's hash; the plan moves only the function's code and one added registry.json Resource element on the existing ReadSatellitesHoldings statement; CodeSha256 equals the zip's sha256; the unscoped re-plan is clean; the rule and its target unchanged</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the dry-run invoke with {"dry_run": true} then the served key's VersionId, then the ONE driven invoke with {}, then the served characteristics.json read against the table in scope 3e (or oracle_check.py over the run's positioning as_of), then the windows comparison of 3f</invocation>
  <expect>dry-run rc 0 and the served VersionId UNCHANGED; the driven invoke 200 with no FunctionError and the VersionId MOVED; all nine satellites' fee, yield, duration and beta equal the table to the stated rounding (or the re-derived table for the run's as_of); Satellites 90 and 98 equal ULT's served duration and beta; the tickers block equals the pre-deploy one for every positioning_data-sourced ticker; coverage carries returns only; for every bbg-sourced ticker the windows under the old and new rules are printed and any move is named with its cause</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the before and after prints, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger with the rollback pins (prior artifact version and hash, prior served VersionId and its saved bytes); only CodeSha256, LastModified and the one policy element differ; the clock respected (no leg open across 21:00Z); this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
