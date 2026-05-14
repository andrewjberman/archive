<task_order>
  <metadata>
    <id>ADHC_DRIFTD.002</id>
    <slug>ae-build-upload-source-map-parity-check</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADHC_DRIFTD</project_code>
    <priority>P1 — same-day empirical near-miss (DS-base 144493642 added file to source_dir without source-map files-array registration; AE 0.7 caught manually at TO-3 pre-build review; would have caused ImportError at runtime on Step 6 invocation if uncaught)</priority>
    <sla>~1-1.5h wall; ship as Commit 2 of two-commit bundle (independent file build-and-upload.sh)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DRIFTD.md §3.2 + §6 TO-2 + §8 acceptance criterion 2</ref>
    <ref type="project_json">org/projects/ADHC_DRIFTD.json</ref>
    <ref type="parent_finding">ADHC_DRIFTD PRD §2.2 — DS-base commit 144493642 added append_non_model_today.py to Lambda source_dir but did NOT register file in source-map files array; AE 0.7 caught at TO-3 pre-build review; would have caused silent exclusion from Lambda zip + ImportError at runtime</ref>
    <ref type="empirical_failure">DS-base 144493642 (SMARTX_NONMDL TO-2; smartx-ingestion-pipeline source dir); AE 0.7 caught manually; ~15min recovery time pre-build; if uncaught, would have surfaced as ImportError on Step 6 invocation post-deploy</ref>
    <ref type="source_target">.tools/build-and-upload.sh — Lambda zip build script; reads source-map files array to determine zip contents; no current pre-build parity check between source_dir listing (truth) vs files array (manifest)</ref>
    <ref type="sibling_to">ADHC_DRIFTD.001 + .003 — shared file record-terraform-deploy.sh; Commit 1 of two-commit bundle. This TO ships in Commit 2.</ref>
    <ref type="sibling_to">ADHC_DRIFTD.VAL — Phase 2 validation sweep includes parity-check regression test against 144493642</ref>
  </references>

  <context>
    build-and-upload.sh reads the source-map files array to determine what to include in the Lambda zip. Files present in source_dir but absent from the files array are silently excluded from the zip — Lambda runtime then ImportErrors on first invocation if any of those files are imported.

    DS-base 144493642 (2026-05-13 SMARTX_NONMDL TO-2 ship) added `append_non_model_today.py` to the smartx-ingestion-pipeline source_dir but did NOT register the file in the source-map files array. AE 0.7 caught the gap manually at TO-3 pre-build review and updated the source map before zip creation. Without the manual catch, the Lambda would have been deployed without the new file, and Step 6 invocation would have ImportError'd at runtime.

    Detection gap: no automated pre-build parity check between source_dir listing (truth) and files array (manifest). The fix is a structural pre-build hook that compares the two and halts on mismatch in either direction.

    PRD §3.2 specifies bidirectional check:
    - Files in source_dir but absent from files array → ERROR + halt (force DS to register)
    - Files in files array but absent from source_dir → ERROR + halt (stale manifest)
    - Configurable ignore list (hardcoded defaults per CTO Q1 ratify): __pycache__, *.pyc, tests/, README.md
  </context>

  <objective>
    Add pre-build parity check hook to .tools/build-and-upload.sh that:

    1. Reads source-map files array for the Lambda being built
    2. Lists actual files in source_dir (recursive, respecting ignore list)
    3. Compares the two sets
    4. ERROR + halt zip creation on either-direction mismatch
    5. Hardcoded ignore-list defaults: __pycache__, *.pyc, .pytest_cache, .git, tests/, README.md, *.md
    6. Per-Lambda override available via source-map optional `parity_ignore` array (future-proof; not required for v0.1 if hardcoded defaults cover empirical cases)

    Single commit, single file. AC1-5 PASS gates RAVC2 close.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/build-and-upload.sh — add `check_source_map_parity()` function called pre-zip; halt with ERROR + actionable message on mismatch</file>
    </files>
  </scope>

  <phase id="1" when="before-write">
    <run>comp-blast build-and-upload</run>
    <expect>Downstream consumers of build-and-upload.sh enumerated. SKIP if comp-* doesn't model CI scripts.</expect>
    <if_mismatch>N/A — CI script.</if_mismatch>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Add `check_source_map_parity(source_dir, files_array, ignore_list)` helper function in build-and-upload.sh. Walks source_dir recursively, builds set of actual files (relative paths), compares to files array set. Returns 0 on parity-clean; ERROR + halt with actionable message on mismatch.</description>
      <expect>Helper covers both directions (extra files in source_dir, missing files from source_dir). Ignore list excludes well-known build artifacts.</expect>
      <if_mismatch>If shell-set-comparison logic gets unwieldy, surface to COO with proposed Python helper alternative.</if_mismatch>
    </step>
    <step>
      <description>Hook helper into build-and-upload.sh pre-zip phase. Call BEFORE the zip creation step; halt with non-zero exit if parity check fails. Error message must specify Lambda name + missing/extra files + which side has the discrepancy.</description>
      <expect>Build halts on mismatch with clear actionable error. Parity-clean Lambdas build normally.</expect>
      <if_mismatch>If hook integration breaks existing Lambdas, debug + fix before commit; do not ship partial.</if_mismatch>
    </step>
    <step>
      <description>Hardcoded ignore-list defaults: __pycache__, *.pyc, .pytest_cache, .git, tests/, README.md, *.md (per PRD §6 TO-2 + CTO Q1 ratify "hardcoded defaults for first-cut simplicity"). Per-Lambda override via source-map optional `parity_ignore` array — implement plumbing but don't require entries for v0.1.</description>
      <expect>Ignore list applied during walk. Per-Lambda override readable but optional.</expect>
      <if_mismatch>If a legitimate file gets ignored by default list, surface as edge case + adjust before commit.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Dry-run against DS-base 144493642 commit state (smartx-ingestion-pipeline source_dir with append_non_model_today.py present + files array NOT yet updated). Verify parity check ERROR + halt with specific actionable message identifying append_non_model_today.py as the discrepancy.</description>
      <expect>Empirical reproduction of the gap; check halts the build pre-zip with correct error.</expect>
      <if_mismatch>If check doesn't fire on the known-gap commit, the algorithm is wrong — debug + fix before ship.</if_mismatch>
    </step>
    <step>
      <description>No-regression check on parity-clean Lambdas: run build against current HEAD state (post-144493642 fix, source map updated). Verify check passes silently and build proceeds normally.</description>
      <expect>Parity-clean Lambdas build without hook interference.</expect>
      <if_mismatch>If hook fires on parity-clean Lambdas, the check is over-strict — likely ignore-list edge case. Debug + fix.</if_mismatch>
    </step>
    <step>
      <description>Empirical test of reverse-direction (files array entry pointing to nonexistent file in source_dir): synthetic test case manually constructed; expect ERROR + halt with "stale manifest" message.</description>
      <expect>Bidirectional check works on both error modes.</expect>
      <if_mismatch>If only one direction halts, fix the missing branch before commit.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: build-and-upload.sh has new pre-zip `check_source_map_parity()` hook that halts build on mismatch in either direction (extra files in source_dir; missing files from source_dir).
    AC2: Dry-run against DS-base 144493642 commit state empirically reproduces the source-map files-array gap with ERROR + halt + actionable message identifying append_non_model_today.py.
    AC3: No-regression on parity-clean Lambdas: existing build chain unaffected; hook passes silently when source_dir matches files array.
    AC4: Hardcoded ignore-list defaults: __pycache__, *.pyc, .pytest_cache, .git, tests/, README.md, *.md (per CTO Q1 ratify). Per-Lambda override plumbing via source-map optional `parity_ignore` array — implemented but optional.
    AC5: Reverse-direction check (files array entry for nonexistent source_dir file) also fires correctly with "stale manifest" error.
    AC6: Session log captures empirical-test verification on 144493642 + commit hash + AC1-5 evidence.
    AC7: MCP RAVC2 close to COO with empirical-test verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-blast build-and-upload (downstream consumer enumeration; SKIP if comp-* doesn't model CI scripts)</phase_1>
    <phase_2>bash -n syntax check; empirical dry-run against DS-base 144493642 commit state BEFORE commit</phase_2>
    <phase_3>DRIFTD.VAL Phase 2 validation sweep includes 144493642 regression test</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - .tools/build-and-upload.sh — pipeline-agnostic CI script; affects all AE lanes on every Lambda build
    - Independent of DRIFTD.001 + .003 (which share record-terraform-deploy.sh); ships in Commit 2 of two-commit bundle

    COORDINATION:
    - No portal frontend impact
    - No DS impact runtime-wise, BUT: DS authors who add files to Lambda source_dir without source-map registration will now hit halt at build time → DS workflow correction (positive). Surface to DS-base FYI post-ship so they know the next time they touch a Lambda source dir, they need to register files in source map.
    - AE peers (0.5.0/0.6.0/0.6.1) FYI-only — script change affects their future Lambda builds with empirical regression test in DRIFTD.VAL
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure CI build-time check. No Lambda code changes. No data semantics change. No reprocess required.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. .tools/build-and-upload.sh modification (new check_source_map_parity() helper + pre-zip hook integration + hardcoded ignore list)
    2. Single commit under 0.7.0_AE_CloudOps author; Commit 2 of two-commit bundle (DRIFTD.001 + .003 in Commit 1 on shared record-terraform-deploy.sh; this TO Commit 2 on independent build-and-upload.sh)
    3. Session log with empirical-test verification on 144493642 + AC1-7 evidence
    4. MCP RAVC2 to COO post-AC1-7 PASS
  </deliverables>

  <ravc>
    AE 0.7 RAVC2 to COO post-AC1-7 PASS. COO ratifies + relays to CTO for architectural-fidelity co-sign on PRD §3.2 + §6 TO-2 implementation. DRIFTD.VAL fires post-bundle commit.
  </ravc>

  <notes>
    **Per CTO Q1 ratify (COO co-sign):** ignore list hardcoded for v0.1 simplicity; per-Lambda override plumbing exists but is optional. Future ADHC_DRIFTD v0.2 can promote to required configuration if empirical edge cases surface.

    **DS coordination note:** post-ship, DS-base (and any DS authoring Lambda source_dir files) will need to update source-map files array when adding files. Send FYI to DS-base post-deploy that workflow now enforces this structurally; reference CLAUDE.md Rule 4 (source-map authoritative).

    **Two-commit bundle ship plan** (per COO Q3 routing decision):
    - Commit 1: DRIFTD.001 + DRIFTD.003 on shared file .tools/record-terraform-deploy.sh
    - Commit 2: DRIFTD.002 (this file) on independent file .tools/build-and-upload.sh

    **Author identity for commit:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` per agent commit identity protocol.
  </notes>
</task_order>
