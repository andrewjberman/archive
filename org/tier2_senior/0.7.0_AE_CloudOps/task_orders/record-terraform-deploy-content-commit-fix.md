<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC-RECORD-TF-DEPLOY-CONTENT-COMMIT</id>
    <title>record-terraform-deploy.sh — preserve content-commit lineage in lambda-source-map.json last_deployed_commit field</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>0.7.0_AE_CloudOps (self-authored per ADHC-INF-UAD-ORPHAN Phase 2 ratify by COO; route via 2.0.0_SA_COO for scope-project assignment)</issued_by>
    <issued_date>2026-05-13</issued_date>
    <status>staged</status>
    <priority>P1 — recurrence prevention for the orphan reconciliation failure mode AE 0.6.1 empirically observed during v1.7.54 bundle apply (sweep commit overwrote content commit on uad-daily, required manual restore in 2071a8ace). Sized ~30-60 min.</priority>
    <estimated_effort>~30-60 min — single-file logic change in two language paths (Python + Node.js), commit, smoke test on next inf-pipeline deploy</estimated_effort>
    <dual_owner>0.4.0_DT_ClientPlatform (CI hygiene consult only; primary lane AE 0.7 for infra/aws/lambda/ci/)</dual_owner>
  </metadata>

  <references>
    <ref type="parent_to">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/inf-unified-account-dim-daily-orphan-reconcile.md (ADHC-INF-UAD-ORPHAN) Phase 2 ratify by COO 2026-05-13</ref>
    <ref type="empirical_failure">AE 0.6.1 v1.7.54 ship RAVC2 2026-05-13T18:45Z: `record-terraform-deploy.sh` swept all Lambdas' last_deployed_commit to sweep commit 743323ff6, overwriting AE 0.7's Branch A backfill bc4759ad0 on uad-daily. Manual restore in commit 2071a8ace.</ref>
    <ref type="source_bug">infra/aws/lambda/ci/record-terraform-deploy.sh lines 145, 188 — unconditional `cfg['last_deployed_commit'] = commit_sha` (= HEAD/sweep commit) for every Lambda matching `tf_file.startswith(tf_prefix)`, regardless of whether the Lambda's artifact actually changed in this deploy.</ref>
    <ref type="parent_finding">ADHC-INF-UAD-ORPHAN Phase 0 forensic: content-commit provenance must be traceable from source map to git log. Current implementation loses provenance whenever a sweep-commit happens between content-commit and apply.</ref>
  </references>

  <context>
    record-terraform-deploy.sh runs AFTER every terraform apply on a pipeline, sweeping the source map's last_deployed_commit field for ALL Lambdas in that pipeline to HEAD (which by construction is the sweep commit itself, since record-terraform-deploy.sh commits the source-map JSON edits). This works correctly when EVERY Lambda in the pipeline was rebuilt + applied in this deploy. But it breaks provenance when:

    (a) A Lambda's source was last edited in commit X, then several commits later a different Lambda's source change triggers a sweep + apply. The first Lambda's last_deployed_commit gets bumped to the sweep commit even though its content (= commit X content) hasn't changed.

    (b) Manual or out-of-cycle content commits to a Lambda's source dir don't generate per-Lambda content-commit attribution; the next apply's sweep commit becomes the entire pipeline's "last_deployed_commit."

    Empirical: ADHC-INF-UAD-ORPHAN Phase 0 traced the failure to docstring update commit 0a6a842dc (2026-05-07) authoring legitimate content that didn't reach last_deployed_commit until manual recovery 6 days later.

    The correct semantic: `last_deployed_commit` = most-recent commit touching the Lambda's source directory whose content corresponds to the currently-deployed artifact. Computable via `git log -1 --format=%H -- <source_dir>` at deploy time.
  </context>

  <objective>
    Replace the unconditional `last_deployed_commit = sweep_commit_sha` in record-terraform-deploy.sh (both Python and Node.js paths) with a per-Lambda content-commit lookup:

    ```
    for each Lambda in pipeline:
        content_commit = `git log -1 --format=%H -- <source_dir>`
        cfg.last_deployed_commit = content_commit
        cfg.last_deployed_at = apply_timestamp
    ```

    This preserves content-commit provenance regardless of how many sweep commits occur between content edits and apply.
  </objective>

  <phase id="1" when="before-write">
    <run>comp-iam service N/A (this is a CI/build script, not a Lambda)</run>
    <expect>SKIP — comp-* tools don't model CI scripts.</expect>
    <if_mismatch>N/A</if_mismatch>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Add a helper function `get_content_commit(source_dir)` that returns `git log -1 --format=%H -- <source_dir>` for the given Lambda's source directory (relative to workspace root). Handle the empty/error case (git log returns nothing if no commits touch the dir) by falling back to current HEAD.</description>
      <expect>Single bash helper before update_source_map(), used inside both Python and Node.js JSON-tool paths.</expect>
      <if_mismatch>If get_content_commit fails for a Lambda, fall back to HEAD-style commit_sha so deploy doesn't break; log the warning.</if_mismatch>
    </step>
    <step>
      <description>Modify lines 145 (Python) and 188 (Node.js) to use the per-Lambda content commit instead of pipeline-level sweep commit.</description>
      <expect>For each Lambda being updated, compute its source_dir's content commit and write that to last_deployed_commit. last_deployed_at remains the apply timestamp (correct as-is).</expect>
      <if_mismatch>If JSON-tool integration breaks (Python heredoc + Node.js heredoc pattern), surface to COO with proposed alternative.</if_mismatch>
    </step>
    <step>
      <description>Update the docstring at lines 24-25 to reflect new semantics: "Sets last_deployed_commit = the most recent commit touching that Lambda's source directory."</description>
      <expect>Docstring matches new behavior; preserves the existing "last_deployed_at = current UTC timestamp" line.</expect>
      <if_mismatch>N/A — docstring only.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Test on a no-op deploy: run record-terraform-deploy.sh on inf-pipeline with the current state (no Lambdas changed since v1.7.54). Expect: each Lambda's last_deployed_commit gets set to its own content commit (NOT the sweep commit).</description>
      <expect>uad-daily's last_deployed_commit should stay as bc4759ad0 (unchanged from current). Other Lambdas may shift to their own content commits — that's the expected correction.</expect>
      <if_mismatch>If a Lambda's content_commit lookup returns the wrong value or is empty, debug + fix.</if_mismatch>
    </step>
    <step>
      <description>Run terraform plan on inf-pipeline post-record: expect 0-diff (no last_deployed_commit changes that would force a Lambda redeploy; source map field is metadata only, not consumed by Terraform).</description>
      <expect>0-diff confirms the field change is metadata-only and doesn't trigger any Lambda update.</expect>
      <if_mismatch>If 0-diff plan shows Lambda diffs, the field IS being consumed somewhere — surface before commit.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: record-terraform-deploy.sh's Python path (line ~145) and Node.js path (line ~188) BOTH use per-Lambda content-commit lookup, not the pipeline-level sweep commit.
    AC2: Empirical test on a no-op deploy shows each Lambda's last_deployed_commit reflects its own most-recent content commit (verify via spot-check on 3+ Lambdas).
    AC3: Next-deploy regression check: on next inf-pipeline apply (real deploy of some Lambda), verify the deployed Lambda's last_deployed_commit reflects ITS content commit, AND non-deployed Lambdas in the same pipeline retain THEIR pre-existing content commits unchanged.
    AC4: Docstring updated to match new semantics.
    AC5: Session log entry with empirical evidence + commit hash.
    AC6: MCP RAVC2 close to COO with empirical-deploy verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <none reason="record-terraform-deploy.sh is a CI script; comp-* tools don't model it. Smoke-test on a no-op deploy is the validation surface."/>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - `infra/aws/lambda/ci/record-terraform-deploy.sh` — pipeline-agnostic; affects all AE lanes (0.5.0, 0.6.0, 0.6.1, 0.7.0) on every deploy. Coordinate via MCP-batch to all AE peers + DT before merging (CI hygiene change).

    NO PORTAL/DS IMPACT:
    - No portal frontend impact.
    - No DS impact (silver/bronze script lanes don't consume last_deployed_commit).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure CI metadata change. No Lambda code changes. No data semantics change. No silver/bronze partition reprocess.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. record-terraform-deploy.sh modification (single commit, single file).
    2. Session log with empirical-deploy verification.
    3. RAVC2 close to COO.
  </deliverables>

  <ravc>
    AE 0.7 RAVC2s to COO post-AC1-6 PASS. COO ratifies → loop close. CTO scope-project assignment via COO (per CTO architectural-discipline framing — likely scoped to a discrete ADHC project code).
  </ravc>
</task_order>
