# pipeline-override: MDPF_CANON round 7 (decomposition v7, cell CN-j-1, drained @1c8ebf3e5d); the round-7 issuance @879feb7e99 is closed to new order files (ONE ISSUER PER ROUND), so the deploy of CN-j-1's publisher package, its environment stamp and one on-demand invoke ride one CloudOps ADHOC order, on the MDPF_CANON round-2, round-4 and round-6 precedents (ADHOC.canon-r2-publisher-layer-and-builder-grant, ADHOC.canon-r4-code-deploy, ADHOC.canon-r6-fold-deploy).
<task_order id="ADHOC.canon-r7-publisher-deploy">
<to_id>ADHOC.canon-r7-publisher-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-14</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 7 of MDPF_CANON; BEHIND the issuer's written GO and both pair halves -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-j-1: the publisher serves the category-views history leaf for each scope -- the publisher package rebuilt at a pin with its commit stamp, one on-demand invoke; the gold lambda, the gold package and the runner code tree are NOT touched</title>
<context>
Cell CN-j-1 (order `task-orders/MDPF_CANON.TO-CN-j-1.category-views-history-leaf.md`, merged `1c8ebf3e5d`) changes the publisher package in one product file and its tests:
- `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py`: per scope that has dated `category-views` gold, one more served key,
  `platinum/mdpf/<scope>/category-views-history.json` (`dates[]` plus the two Client aum arrays, `null` for an absent node, named `omitted[]`), assembled by `_publish_history_one` and reported in `history_rows`
  of the run manifest and the pointer, outside `results`, `expected`, `failed` and `all_present`.
- `tests/test_history_leaf.py` (new) and `tests/test_completeness.py` (three filters): not shipped.
The served bytes change only after D1. The never-widen pair is written on both halves: the COO half in
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/NEVER_WIDEN_PAIR_R7_J1_PUBLISHER.md` (moved from `round7/draft/` when it is signed) and the CTO half in
`org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R7_J1_PUBLISHER_CTO_HALF.md`. Read the pair first: sections 1a, 2, 4 and 5 are this order's package contents, acts, blast radius and every branch.

What this order carries beyond the round-6 shape (read these four lessons):
1. **The rebuild is not the cell alone.** The builder reads every member from the pin; at HEAD eight packaged modules besides `lambda_function.py` differ from the deployed bytes (`lib/opal_naming.py` 1,042
   lines; the registry files `systems`, `exemptions`, `reporting_policies`, `scopes`, `resources`; `NAMING_SCHEMA.json`; `MDPF_TAXSMA_DATA_CONTRACT.json`). The pair accepts that on stated evidence; this order
   RE-RUNS the comparison at the pin it is given and prints it (leg a).
2. **The publisher's pointer is unreadable in production** (`AccessDenied` on `_manifests/latest.json`, manifest `20261014T135048Z-2ca57833`): every run republishes every leaf, so the on-demand run rewrites the
   18 existing leaves with their own gold bytes. Their prior VersionIds are the baseline of leg c.
3. The artifact is S3-backed: `module "mdpf_publisher"` takes `s3_object_version` and `source_code_hash` (the object's `content-sha256` METADATA) from the CURRENT version of
   `s3://opal-313476888478-lambda-artifacts/opal-assets/opal-assets-mdpf-portal-publisher.zip`. The upload must happen BEFORE the plan, and its metadata must equal the zip's sha256 hex.
4. The environment stamp: `MDPF_PUBLISHER_COMMIT` (`mdpf_portal_publisher.tf:163`) must equal the FULL pin SHA actually built. This order is the one order authorized to move it.
</context>

<scope>
1. Edit no source file EXCEPT `infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf`: the value of `MDPF_PUBLISHER_COMMIT` in the function's environment block and the comment line above it. No other line of that file
   moves. Open a deploy ledger (NEVER-2) BEFORE the first act, slug `mdpf-canon-r7-publisher-deploy-dell1-20261014` (or the day's date if later); name in it the artifact key, the function, the four new keys, the
   18 existing leaves, the `.tf` value, and the serving path (CloudFront `EVTSA9VEHNZVH`, `/api/general/*`, `public-data-router`, bucket `opal-data-portal-v2`).
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's written GO, a broker message from `2.0.0_SA_COO~D1` naming the pin, sent only after `ADHOC.canon-r7-gold-deploy`'s ledger is CLOSED (two acts never share one window). Without it this
      order WAITS: it is issued `staged` and stays so until that message; on it, flip the order's status field to pending and start. Both halves of the pair are signed (CTO half `9a492909b7`, which KEEPS D2, accepts the
      section 1a drift on the evidence that H8 reads the 18 leaves equal, and requires the runtime import read on D2 and the drift table re-run at the GO pin: legs (a) and (c) print them).
   b. The pin is an ancestor of origin's `box/dell1` (`git ls-remote`, then `git merge-base --is-ancestor`) and carries merge `1c8ebf3e5d`. Read `lambda_function.py` at the pin by content: it contains
      `_publish_history_one`.
   c. Both halves of the pair are SIGNED, read from the two files named in the context (a signature is a line in a commit by that seat). If the CTO half struck D2, leg c below is struck by the issuer's
      amendment commit and you do not run it.
   d. The clock: no act of D1 or D2 starts within 45 minutes before the 13:30Z gold fire or the 13:50Z publisher run, or while the gold lambda, the runner dispatch or the publisher is running (read the
      lambda's last invocation and the scheduler's `opal-assets-mdpf-portal-publisher-daily`). D1 and D2 therefore start after ~14:10Z and end before ~12:45Z the next day.
   e. The edge read: no CloudFront behaviour, function association or WAF rule names an individual `platinum/mdpf/*` leaf or limits the path to a fixed leaf list (read `aws cloudfront get-distribution-config
      --id EVTSA9VEHNZVH` for behaviours naming `general` or `mdpf`, the router's `index.mjs` rewrite, and the WAF `opal-cloudfront-protection`). A finding stops the order: the leaf would be unreachable and an
      edge change is ADVI_FIRMBKTS's (R2).
   f. No FIRMBKTS window act is in flight (read `org/critical_paths/.open_deploys/advi-firmbkts-*` and start only in a gap). This order touches NONE of the R2 surfaces (`shared-advisor-router`, the guard, the
      CloudFront behaviours, `data/mdpf/config/bronze_homes.json`, `firm-config.mjs`, the portal-auth WAF rider).
   g. No open deploy sentinel names `opal-assets-mdpf-portal-publisher` or `platinum/mdpf/` other than this order's own, and no `mdpf-gold-lambda` or `code/scripts/gold/` act is mid-flight (CN-h-1 and CN-l-1 ride
      their own order; two acts never share one window). Read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD
      org/critical_paths/.open_deploys/`), union them, print the per-tree denominator.
3. **ORDER OF ACTS (the order is the safety):**
   a. **Before print.** Record: the function's `CodeSha256` (expect `pj+Jat96t5dijB+0SQF918S1pi3AZBs1eQNvMXLYEJA=`), `LastModified`, `Role`, `Runtime`, `Layers` (expect
      `pandas-pyarrow-requests-layer:1`) and its full environment (`MDPF_PUBLISHER_COMMIT` prior value `e8994f23af282296037bd28bb539ac55cc9465dd`, `TAXSMA_ROLLOUT_SWITCH` ON). The artifact key's CURRENT version
      (expect `Deg26fXt..bp.9N3HB4sZKEu.MYLj4y2`, `content-sha256` `a63f896adf7ab797628c1fb449017dd7c4b5a62dc0641b3579036f3172d81090`): DOWNLOAD that exact version's bytes to a local file, hash it, and keep it
      as the rollback copy (attach the hash to the ledger). The schedule's input verbatim (`scheduler get-schedule`; expect `cron(50 13 * * ? *)` UTC, ENABLED, input `{}`). For each scope in
      `49financial inflection cottonwood global` and each of its existing leaves under `platinum/mdpf/<scope>/` (4, 4, 5 and 5 keys = 18): ETag, VersionId and a body hash, and the matching gold source key's
      ETag. The pointer `platinum/mdpf/_manifests/latest.json`: VersionId (expect `oWlJmSz46pAngbwHkQH6.oHmnZ50jv6D` or a later one) and its key set (expect `manifest_key`, `rows`, `run_id`, no
      `history_rows`). The dated `category-views` counts per scope under `portal/gold/mdpf/<scope>/category-views/` (denominators; expect 27, 26, 20, 22 or one more each). The four history keys: list the prefix
      `platinum/mdpf/<scope>/category-views-history` per scope; expect NO object (a positive control: the scope's own listing shows its existing leaves). **The drift table:** at the pin, for each member of the
      deployed sidecar `opal-assets-mdpf-portal-publisher.BUILD_MANIFEST.json` `modules`, compare the manifest's sha256 with `git show <pin>:<path>`; print EQUAL or DIFFERS per member and the line stat of
      each DIFFERS member against `e8994f23af`; report it to the issuer. A member that DIFFERS and is not in the pair's section 1a table is a STOP (report; do not build).
   b. **D1.** `python infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/build_package.py --pin <the pin> --out <a scratch path outside the repo>` (the package's own procedure; it refuses a moving
      ref), read its printed sha256 and the sidecar. Upload the zip to the artifact key with S3 object metadata `content-sha256` = the zip's sha256 hex (the method is CloudOps's logged practice for
      this module; the END STATE is the requirement: a new version of the key whose `content-sha256` metadata equals the sha256 of the bytes). Read the new version back and compare the metadata with
      the zip's own hash BEFORE planning. Edit the one `.tf` value to the FULL SHA the build resolved (the sidecar's `source_vintage.commit`), commit that one file with `safe-commit.sh`, then ONE targeted
      plan and `safe-apply` on `module.mdpf_publisher`. The targeted plan must show the function's code change (`s3_object_version`, `source_code_hash`) and the single environment value
      `MDPF_PUBLISHER_COMMIT` and nothing else; any other attribute moving (a `layers` line, the runtime, the role, the schedule, any IAM statement): STOP, report, do not apply. After the apply read back: the
      function's `CodeSha256` equals the zip's sha256 (base64 of the hex); the function's `MDPF_PUBLISHER_COMMIT` equals the full pin SHA, which equals the deployed sidecar's `source_vintage.commit`; every
      module's sha256 in the new sidecar equals `git show <pin>:<path>`; the re-plan is clean.
   c. **D2, the one on-demand invoke (struck if the CTO half struck it).** Read the schedule's input recorded in (a); the event is that input and nothing else (`{}`); use `--cli-read-timeout 0`. Invoke
      `opal-assets-mdpf-portal-publisher` ONCE. Read the response and the new run manifest. Then read the same 18 existing leaves and the pointer as in (a).
      The leg is met when: invoke 200 with no FunctionError; the new manifest's `all_present` is true, `missing_pairs` and `unexpected_pairs` are empty, `published` equals 18 (every pair, the pointer being
      unreadable); its `history_rows` carries exactly the four leaves, each `status` `published` (or `unchanged` if the pointer has become readable) with `omitted` empty and `n_dates` equal to that scope's dated
      count; the four keys now exist; every one of the 18 baseline leaves has the SAME data as before (compare with `_provenance` removed; the VersionId advancing is expected and listed; a changed data
      field is a finding: STOP, re-copy that key from its recorded VersionId, report, and file a BLOCKING row naming the key); the pointer's key set gained `history_rows` and nothing else.
      CTO HALF CONDITION (b): record in the ledger that the invoke ran under the function's own runtime (read `Runtime` from the configuration; python3.11 expected, which the local 3.14 run did not prove) and print the response's first lines; an import or runtime error in the response is Branch B: roll back per section 4. CONDITION (a): the 18-leaf comparison above includes the Tax-stamped leaves; any difference is a same-afternoon rollback from the saved prior zip.
      If the manifest has any `history_rows` row `error` or `verify_absent`: do NOT retry or loosen; file a BLOCKING row with the scope and the message, and report. If the invoke raises, or a 18-pair row is
      not `published` or `unchanged`: the same, and roll back per section 4.
   d. **D3, the edge hop (read-only).** For each scope, GET the public route `/api/general/mdpf/<scope>/category-views-history.json` through the portal's public host (read the host from the portal's own
      configuration, never type it) and record status, byte count and that the body parses as JSON with the declared keys. If the route answers 401 or 403 (a session is required), record that and stop this
      sub-leg: it is not a failure of D2 and the issuer reads the leaf through its S3 object. A 404 or a body that is not the leaf is a finding: report.
   e. **The acceptance is NOT a leg of this order.** The issuer runs `round7/checks/r7_history_readback.py read` on the D2 run (QA) and on the first SCHEDULED run after D1 (2026-10-15 13:50Z at the
      earliest). Nothing here waits for it.
   f. **After print.** Re-read: the function configuration (only `CodeSha256`, `LastModified`, `MDPF_PUBLISHER_COMMIT` changed), the artifact key's versions (one new version), the four history keys, the 18
      existing leaves, the pointer and the schedule (unchanged). Report every other difference from the before print; deploy NOTHING from that list.
4. **Rollback** if (b) shows an unexpected plan, or (c) shows any delta beyond what it names: re-upload the saved prior zip bytes (the hash attached in (a)) to the artifact key with metadata `content-sha256`
   `a63f896adf7ab797628c1fb449017dd7c4b5a62dc0641b3579036f3172d81090`, restore the `.tf` value and comment to `e8994f23af282296037bd28bb539ac55cc9465dd`, apply the same target, read back `CodeSha256`
   `pj+Jat96t5dijB+0SQF918S1pi3AZBs1eQNvMXLYEJA=`, and report. The four history keys are new: they are NOT deleted (a delete needs a human's word; nothing reads them until the Trend candidate lands); if one is
   wrong, the answer is a corrected build overwriting it. The 18 existing leaves are re-copied from their recorded VersionIds only if a data field differs. A manifest is write-once and inert; the pointer is additive
   (the prior code reads only `rows`). The previous artifact version `ZLaQC2nGuQ2hP72JpdTA4RWfciYhFoql` (2026-08-29) is NOT a rollback target.
5. Close the ledger. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf
infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/opal-assets-mdpf-portal-publisher.BUILD_MANIFEST.json
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_j_1.py" unit | tail -1 &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_j_1.py" seam | tail -1 &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_j_1.py" real | tail -1</invocation>
  <expect>ROUND 7 CN-J-1 UNIT: 6 of 6 arms, ROUND 7 CN-J-1 SEAM: 8 of 8 arms and ROUND 7 CN-J-1 REAL: 6 of 6 arms (the source deployed is the source graded; the real arm reads gold read-only)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>cd "$(git rev-parse --show-toplevel)/infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher" &amp;&amp; python -m pytest tests -q -p no:cacheprovider</invocation>
  <expect>19 passed, none failed (the publisher's own suite at the pin, against the eight drifted modules too)</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the artifact upload read-back, the targeted plan on module.mdpf_publisher, safe-apply -target, then the deployed sidecar and the function configuration read back</invocation>
  <expect>the new artifact version's content-sha256 metadata equals the zip's sha256; the plan moves only the function's code and the environment value MDPF_PUBLISHER_COMMIT; the function's CodeSha256 equals the zip's sha256; MDPF_PUBLISHER_COMMIT equals the full pin SHA and the sidecar's source_vintage.commit; every module's sha256 in the new sidecar equals the pin's blob; the re-plan is clean</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the one invocation of opal-assets-mdpf-portal-publisher with the schedule's recorded input, then the before and after reads of the 18 existing leaves, the new manifest, the pointer and the four history keys, then the edge GET of each leaf</invocation>
  <expect>invoke 200 with no FunctionError; all_present true, published 18, missing_pairs and unexpected_pairs empty; history_rows holds the four leaves published (or unchanged) with omitted empty and n_dates equal to each scope's dated count; the four keys exist; every one of the 18 baseline leaves has the same data apart from _provenance (VersionIds listed); the pointer gained only history_rows; the edge status of each leaf recorded (200 with the declared keys, or 401/403 recorded and the sub-leg stopped); or, if the CTO half struck D2, this criterion reads NOT RUN BY ORDER with the strike's commit named</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the before and after prints, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the function configuration differs only in CodeSha256, LastModified and MDPF_PUBLISHER_COMMIT; the schedule unchanged; the drift table printed and every DIFFERS member inside the pair's section 1a; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
