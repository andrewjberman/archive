<task_order>
  <metadata>
    <id>ADHC_DRIFTD.001</id>
    <slug>ae-record-terraform-content-provenance-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADHC_DRIFTD</project_code>
    <priority>P1 — three-incident-day root cause; ~45min cumulative manual backfill cost today across inf-uad-daily + 2 smartx Lambdas; structural fix prevents recurrence on every future bundle apply</priority>
    <sla>~1-2h wall; ship as Commit 1 of two-commit bundle (paired with .003 on shared file record-terraform-deploy.sh)</sla>
    <absorbs>org/tier2_senior/0.7.0_AE_CloudOps/task_orders/record-terraform-deploy-content-commit-fix.md (P1 standalone TO drafted earlier 2026-05-13; folds verbatim into this DRIFTD.001 scope; do NOT ship from standalone path)</absorbs>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DRIFTD.md §3.1 + §6 TO-1 + §8 acceptance criteria 1+5</ref>
    <ref type="project_json">org/projects/ADHC_DRIFTD.json</ref>
    <ref type="parent_finding">ADHC_DRIFTD PRD §2.1 — 3 empirical incidents 2026-05-13 all share record-terraform-deploy.sh:145+188 unconditional sweep-commit-sha overwrite root cause</ref>
    <ref type="absorbed_to">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/record-terraform-deploy-content-commit-fix.md — standalone P1 TO drafted by AE 0.7 earlier 2026-05-13; this DRIFTD.001 absorbs its scope</ref>
    <ref type="empirical_failure_1">AE 0.6.1 v1.7.54 ship RAVC2 2026-05-13T18:45Z: record-terraform-deploy.sh swept all inf-pipeline Lambdas' last_deployed_commit to sweep commit 743323ff6, overwriting AE 0.7's Branch A backfill bc4759ad0 on uad-daily; manual restore in commit 2071a8ace</ref>
    <ref type="empirical_failure_2">AE 0.7 SMARTX_NONMDL TO-3 ship RAVC2 2026-05-13T19:20Z: opal-smartx-ingestion-pipeline + smartx-ec2-autostart last_deployed_commit swept to IAM commit 9a67e7034; manual backfill to 144493642 + f46a3682e in 25f00249c</ref>
    <ref type="source_bug">.tools/record-terraform-deploy.sh lines 145 (Python branch) + 188 (Node.js branch) — unconditional `cfg["last_deployed_commit"] = sweep_commit_sha` for every Lambda matching `tf_file.startswith(tf_prefix)`, regardless of whether the Lambda's artifact actually changed in this deploy</ref>
    <ref type="sibling_to">ADHC_DRIFTD.003 — same shared file (record-terraform-deploy.sh); ship in same Commit 1 of two-commit bundle</ref>
    <ref type="sibling_to">ADHC_DRIFTD.002 — independent file (build-and-upload.sh); ships in Commit 2</ref>
    <ref type="sibling_to">ADHC_DRIFTD.VAL — Phase 2 validation sweep against 3 historical incidents; runs post-bundle</ref>
  </references>

  <context>
    record-terraform-deploy.sh runs AFTER every terraform apply on a pipeline, sweeping the source map's last_deployed_commit field for ALL Lambdas in that pipeline to HEAD (which by construction is the sweep commit itself, since record-terraform-deploy.sh commits the source-map JSON edits). This works correctly when EVERY Lambda in the pipeline was rebuilt + applied in this deploy. But it breaks provenance when:

    (a) A Lambda's source was last edited in commit X, then several commits later a different Lambda's source change triggers a sweep + apply. The first Lambda's last_deployed_commit gets bumped to the sweep commit even though its content (= commit X content) hasn't changed.

    (b) Manual or out-of-cycle content commits to a Lambda's source dir don't generate per-Lambda content-commit attribution; the next apply's sweep commit becomes the entire pipeline's "last_deployed_commit."

    Empirical: 3 incidents same day 2026-05-13 (inf-uad-daily + 2 smartx Lambdas). All required manual backfill via `git log --follow -- <source_dir>` + sed/jq patch. ~10-15min per incident; ~45min cumulative manual cost in one day. Pattern is structural; ship priority promoted from "future cleanup" to P1.

    The correct semantic: `last_deployed_commit` = most-recent commit touching the Lambda's source-map `files` array contents (the truth of what's deployed). Computable via `git log -1 --format=%H -- <files...>` at deploy time.
  </context>

  <objective>
    Replace unconditional `cfg["last_deployed_commit"] = sweep_commit_sha` in record-terraform-deploy.sh (both Python and Node.js paths) with per-Lambda content-commit lookup:

    ```
    for each Lambda in pipeline:
        content_commit = `git log -1 --format=%H -- <files from source_map["files"] array>`
        if content_commit and content_commit != cfg["last_deployed_commit"]:
            cfg["last_deployed_commit"] = content_commit
        cfg["last_deployed_at"] = apply_timestamp  (unchanged behavior)
    ```

    This preserves content-commit provenance regardless of how many sweep commits occur between content edits and apply. Sibling Lambdas under shared tf_prefix that weren't actually content-touched keep their prior last_deployed_commit intact.

    Single commit, single file. AC1-6 PASS gates RAVC2 close.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/record-terraform-deploy.sh — line 145 (Python branch) + line 188 (Node.js branch) per-Lambda content-commit derivation; line 24-25 docstring update reflecting new semantics</file>
    </files>
  </scope>

  <phase id="1" when="before-write">
    <run>comp-blast record-terraform-deploy</run>
    <expect>Downstream consumers of record-terraform-deploy.sh enumerated. SKIP if comp-* doesn't model CI scripts; smoke-test is the validation surface.</expect>
    <if_mismatch>N/A — CI script.</if_mismatch>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Add helper function `get_content_commit(files_array)` (or `compute_content_commit(files_array)` per PRD §3.1) returning `git log -1 --format=%H -- <files...>` for the Lambda's actual source-map files list. Handle empty/error case (git log returns nothing if no commits touch the files) by falling back to current HEAD with WARN log entry.</description>
      <expect>Single bash/Python helper before update_source_map(), used inside both Python and Node.js JSON-tool paths.</expect>
      <if_mismatch>If get_content_commit fails for a Lambda, fall back to HEAD-style commit_sha so deploy doesn't break; log warning to stderr for audit trail.</if_mismatch>
    </step>
    <step>
      <description>Modify line 145 (Python) + line 188 (Node.js) to use per-Lambda content commit. Only write `cfg["last_deployed_commit"]` if derived content_commit differs from current value; otherwise no-op (sibling Lambda untouched).</description>
      <expect>For each Lambda being processed, compute its source_map.files content commit and write that to last_deployed_commit. last_deployed_at remains the apply timestamp (correct as-is).</expect>
      <if_mismatch>If JSON-tool integration breaks (Python heredoc + Node.js heredoc pattern), surface to COO with proposed alternative; do not ship partial fix.</if_mismatch>
    </step>
    <step>
      <description>Update docstring at lines 24-25 to reflect new semantics: "Sets last_deployed_commit = the most recent commit touching that Lambda's source-map files list."</description>
      <expect>Docstring matches new behavior; preserves the existing "last_deployed_at = current UTC timestamp" line.</expect>
      <if_mismatch>N/A — docstring only.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Dry-run against 3 historical incident-commit graphs (per PRD §8 AC1): re-run record-terraform-deploy.sh logic against (a) inf-pipeline v1.7.54 sweep-commit 743323ff6, (b) smartx-pipeline IAM commit 9a67e7034. Verify each Lambda's derived content commit matches AE manual backfill values (bc4759ad0 for uad-daily; 144493642 for opal-smartx-ingestion-pipeline; f46a3682e for smartx-ec2-autostart).</description>
      <expect>3-of-3 incidents reproduce correct last_deployed_commit without manual backfill. Sibling Lambdas under shared tf_prefix that weren't content-touched keep their prior last_deployed_commit unchanged.</expect>
      <if_mismatch>Any divergence: do NOT commit; surface to COO with empirical evidence + proposed alternative algorithm.</if_mismatch>
    </step>
    <step>
      <description>No-regression check on legitimate single-Lambda-tf-touch case: simulate a real Lambda content change + apply → verify the changed Lambda's last_deployed_commit gets updated to the content commit; verify no spurious updates on sibling Lambdas.</description>
      <expect>Update fires correctly on content-touched Lambda; no-op on siblings.</expect>
      <if_mismatch>If sibling Lambda gets updated despite no content change, the helper algorithm is wrong — debug + fix before commit.</if_mismatch>
    </step>
    <step>
      <description>terraform plan on inf-pipeline post-record verifies 0-diff (last_deployed_commit field is source-map metadata only; not consumed by Terraform).</description>
      <expect>0-diff confirms field change is metadata-only and doesn't trigger any Lambda update.</expect>
      <if_mismatch>If 0-diff plan shows Lambda diffs, the field IS being consumed somewhere — surface before commit.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: record-terraform-deploy.sh Python branch (line ~145) AND Node.js branch (line ~188) BOTH use per-Lambda content-commit lookup via git log on source-map files array; NOT the pipeline-level sweep commit.
    AC2: Dry-run against 3 historical incidents (inf-uad-daily v1.7.54 + opal-smartx-ingestion-pipeline TO-3 + smartx-ec2-autostart TO-3) empirically reproduces correct last_deployed_commit matching AE manual backfill values (bc4759ad0 + 144493642 + f46a3682e respectively).
    AC3: No-regression on legitimate single-Lambda-tf-touch case: content-touched Lambda gets correct update; sibling Lambdas in same pipeline keep prior last_deployed_commit unchanged.
    AC4: Docstring at lines 24-25 updated to match new semantics.
    AC5: Empty/error case handled — falls back to HEAD with WARN log; deploy never breaks on get_content_commit failure.
    AC6: terraform plan post-record verifies 0-diff (field is metadata only).
    AC7: Session log captures empirical-deploy verification + commit hash + AC1-6 evidence.
    AC8: MCP RAVC2 close to COO with empirical-deploy verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-blast record-terraform-deploy (downstream consumer enumeration; SKIP if comp-* doesn't model CI scripts — smoke-test is the validation surface)</phase_1>
    <phase_2>bash -n syntax check; python -m py_compile if Python helper added; ds-precommit-check.py AST validation if Python heredoc; empirical dry-run against one historical incident BEFORE commit</phase_2>
    <phase_3>DRIFTD.VAL Phase 2 validation sweep against 3 historical incidents (regression test set; separate TO post-bundle ship)</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - .tools/record-terraform-deploy.sh — pipeline-agnostic CI script; affects all AE lanes (0.5.0, 0.6.0, 0.6.1, 0.7.0) on every deploy
    - Shared with DRIFTD.003 (gitLogJson escaping fix) — both touch same file; ship as Commit 1 of two-commit bundle to avoid merge conflict
    - DRIFTD.002 (build-and-upload.sh parity check) — independent file; Commit 2 of bundle

    COORDINATION:
    - No portal frontend impact
    - No DS impact (silver/bronze script lanes don't consume last_deployed_commit)
    - AE peers (0.5.0/0.6.0/0.6.1) FYI-only — script change affects their future deploys but doesn't require their pre-merge sign-off (CI hygiene change with empirical regression test in DRIFTD.VAL)
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure CI metadata change. No Lambda code changes. No data semantics change. No silver/bronze/gold partition reprocess. Existing source-map last_deployed_commit values are corrected on next-deploy fire under fixed logic (or via DRIFTD.VAL retroactive sweep).
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. .tools/record-terraform-deploy.sh modification (Python branch line 145 + Node.js branch line 188 + docstring lines 24-25)
    2. Single commit under 0.7.0_AE_CloudOps author; bundled with DRIFTD.003 in Commit 1 of two-commit bundle (TO-1 + TO-3 ship together on shared file; DRIFTD.002 ships as Commit 2)
    3. Session log with empirical-deploy verification + AC1-8 evidence
    4. MCP RAVC2 to COO post-AC1-8 PASS
  </deliverables>

  <ravc>
    AE 0.7 RAVC2 to COO post-AC1-8 PASS. COO ratifies + relays to CTO for architectural-fidelity co-sign on PRD §3.1 + §6 TO-1 implementation. DRIFTD.VAL fires post-bundle commit (separate TO; regression test).
  </ravc>

  <notes>
    **Absorption note:** existing standalone TO at `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/record-terraform-deploy-content-commit-fix.md` (P1, AE 0.7 drafted) FOLDS into this DRIFTD.001. Do NOT ship from standalone path; canonical project-coded TO is this file. Standalone TO file remains on disk for git history reference; will be deleted on DRIFTD project close-out.

    **Two-commit bundle ship plan** (per COO Q3 routing decision):
    - Commit 1: DRIFTD.001 (this file) + DRIFTD.003 on shared file .tools/record-terraform-deploy.sh
    - Commit 2: DRIFTD.002 on independent file .tools/build-and-upload.sh
    - Both commits in single push; cleaner rollback granularity vs atomic-3 bundle
    - DRIFTD.VAL Phase 2 validation sweep runs against post-bundle state

    **Author identity for commit:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` per agent commit identity protocol.
  </notes>
</task_order>
