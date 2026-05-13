<task_order>
  <metadata>
    <id>ADHC_DRIFTD.VAL</id>
    <slug>ae-historical-incident-sweep</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>DRIFTD.001 + .002 + .003 both commits in two-commit bundle SHIPPED + AC PASS on each (.001 + .003 joint RAVC2; .002 separate RAVC2)</dispatch_unblock_condition>
    <project_code>ADHC_DRIFTD</project_code>
    <priority>P1 — Phase 2 acceptance gate; empirical proof the 3-TO bundle eliminates manual backfill on the 3 incident-commit regression test set; closes ADHC_DRIFTD v0.1 scope</priority>
    <sla>~30min wall; ships immediately after DRIFTD.001 + .002 + .003 commits land</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DRIFTD.md §4 Phase 2 + §6 TO-VAL + §8 acceptance criteria 1-5 (regression test set)</ref>
    <ref type="project_json">org/projects/ADHC_DRIFTD.json</ref>
    <ref type="parent_finding">ADHC_DRIFTD PRD §8 — 3 historical incidents (inf-uad-daily v1.7.54 + 2 smartx Lambdas TO-3) become regression test set; sweep verifies zero manual backfills needed under fixed logic</ref>
    <ref type="sibling_to">ADHC_DRIFTD.001 (record-terraform-deploy.sh content-provenance fix; Commit 1)</ref>
    <ref type="sibling_to">ADHC_DRIFTD.002 (build-and-upload.sh source-map parity check; Commit 2)</ref>
    <ref type="sibling_to">ADHC_DRIFTD.003 (record-terraform-deploy.sh gitLogJson escape fix; Commit 1)</ref>
    <ref type="empirical_test_set">3 incident commits + sweep commits: (1) inf-pipeline v1.7.54 sweep 743323ff6 vs uad-daily content commit bc4759ad0; (2) smartx-pipeline IAM sweep 9a67e7034 vs ingestion-pipeline content commit 144493642; (3) smartx-pipeline IAM sweep 9a67e7034 vs ec2-autostart content commit f46a3682e</ref>
    <ref type="parity_test_set">DS-base 144493642 (source-map files-array gap); known-good post-fix HEAD state (parity-clean)</ref>
    <ref type="changelog_test_set">Synthetic quote-in-subject commit (constructed for empirical test); known-good ASCII-clean commits (no-regression)</ref>
  </references>

  <context>
    DRIFTD.VAL is the Phase 2 acceptance gate for ADHC_DRIFTD v0.1. After DRIFTD.001 + .002 + .003 ship in the two-commit bundle, this TO runs the fixed logic against the 3 historical incidents from 2026-05-13 + the source-map parity test cases + the gitLogJson escape test cases. Pass = ADHC_DRIFTD v0.1 closed; project moves to monitoring state.

    The 3 incidents become the canonical regression test set for future ADHC_DRIFTD versions; any future change to record-terraform-deploy.sh or build-and-upload.sh in this surface area should re-run DRIFTD.VAL to confirm no regression.

    Sweep covers three orthogonal test surfaces (one per TO):
    1. **Content-provenance regression (DRIFTD.001):** dry-run record-terraform-deploy.sh against 3 incident sweep commits; verify each Lambda's last_deployed_commit matches AE manual backfill value (bc4759ad0 + 144493642 + f46a3682e) without manual intervention.
    2. **Source-map parity regression (DRIFTD.002):** dry-run build-and-upload.sh against DS-base 144493642 pre-fix state; verify ERROR + halt; dry-run against HEAD; verify clean pass.
    3. **gitLogJson escape regression (DRIFTD.003):** synthetic commit with quote-in-subject + comprehensive escape coverage; verify CHANGELOG.json writes succeed with correct escaping.

    All three sweeps run as a single TO scope; one RAVC2 closes Phase 2 + ADHC_DRIFTD v0.1.
  </context>

  <objective>
    Run the 3-TO regression test sweep against historical incident commit graph. Confirm:

    1. DRIFTD.001 fix reproduces correct last_deployed_commit for all 3 historical Lambdas without manual backfill
    2. DRIFTD.002 fix fires correctly on 144493642 gap state + passes silently on HEAD parity-clean state
    3. DRIFTD.003 fix produces valid CHANGELOG.json for synthetic quote-in-subject commit + comprehensive escape coverage
    4. No-regression on legitimate single-Lambda content-touch case (DRIFTD.001 doesn't over-fire)
    5. No-regression on parity-clean builds (DRIFTD.002 doesn't over-fire)
    6. No-regression on ASCII-clean commit subjects (DRIFTD.003 preserves existing CHANGELOG.json schema)

    Single RAVC2 close on Phase 2 → ADHC_DRIFTD v0.1 scope complete.
  </objective>

  <scope>
    <action>Run sweep tests; no file modifications. Sweep is empirical validation only.</action>
    <output>Session log with full evidence table (test name → expected → actual → pass/fail) covering all 6 acceptance criteria.</output>
  </scope>

  <phase id="1" when="before-write">
    <run>Verify DRIFTD.001 + .002 + .003 commits both shipped + AC PASS on each per RAVC2 evidence trail</run>
    <expect>Commit 1 (DRIFTD.001 + .003) + Commit 2 (DRIFTD.002) both on origin/CLOUD; AC1-8 PASS on .001 + .002 + .003 RAVC2s</expect>
    <if_mismatch>If any prior TO failed AC, do NOT run DRIFTD.VAL; surface to COO + cascade-block</if_mismatch>
  </phase>

  <phase id="2" when="sweep-execution">
    <step>
      <description>Sweep 1 — DRIFTD.001 content-provenance regression. Dry-run record-terraform-deploy.sh logic against 3 incident sweep-commit states: (a) inf-pipeline v1.7.54 sweep 743323ff6, (b) smartx-pipeline IAM sweep 9a67e7034. For each affected Lambda in the source map, verify the derived content_commit matches the manual backfill value: bc4759ad0 (uad-daily) + 144493642 (ingestion-pipeline) + f46a3682e (ec2-autostart).</description>
      <expect>3-of-3 incidents reproduce correct last_deployed_commit values matching AE manual backfills WITHOUT manual intervention. Sibling Lambdas under shared tf_prefix that weren't content-touched keep their prior last_deployed_commit unchanged.</expect>
      <if_mismatch>Any mismatch = DRIFTD.001 fix is incomplete; reopen .001 + RAVC2 fail. Halt VAL execution; surface to COO.</if_mismatch>
    </step>
    <step>
      <description>Sweep 2 — DRIFTD.002 source-map parity regression. (a) Dry-run build-and-upload.sh against DS-base 144493642 pre-fix state (synthetic checkout or git-show-based reconstruction): verify parity check fires ERROR + halt with actionable message identifying append_non_model_today.py. (b) Dry-run against HEAD (post-fix state, source map updated): verify parity check passes silently and build proceeds.</description>
      <expect>(a) ERROR + halt on known-gap state; (b) silent pass on parity-clean HEAD.</expect>
      <if_mismatch>Either failure = DRIFTD.002 fix is incomplete; reopen .002 + RAVC2 fail. Halt VAL execution.</if_mismatch>
    </step>
    <step>
      <description>Sweep 3 — DRIFTD.003 gitLogJson escape regression. (a) Construct synthetic commit with subject `fix "edge case" in foo` (literal quote characters). Run record-terraform-deploy.sh logic against it; verify CHANGELOG.json entry written with correct escaping `"subject": "fix \"edge case\" in foo"`. (b) Comprehensive escape coverage: synthetic commits with backslash, newline-attempt (if achievable via git), control char. Verify each writes correctly OR is rejected loud (not silent skip).</description>
      <expect>(a) Quote-in-subject writes with correct escape; (b) All JSON-unsafe chars handled defensively.</expect>
      <if_mismatch>Any failure = DRIFTD.003 fix is incomplete; reopen .003 + RAVC2 fail. Halt VAL execution.</if_mismatch>
    </step>
    <step>
      <description>Sweep 4 — No-regression on legitimate cases. (a) DRIFTD.001 no-regression: simulate a real Lambda content change + apply → verify the changed Lambda's last_deployed_commit gets updated to its content commit; sibling Lambdas unchanged. (b) DRIFTD.002 no-regression: build against parity-clean HEAD; verify hook passes silently and build proceeds normally. (c) DRIFTD.003 no-regression: ASCII-clean commit subjects (existing CHANGELOG.json entries) round-trip parse cleanly under new logic; no schema drift.</description>
      <expect>All 3 no-regression cases pass; fixes don't over-fire on legitimate input.</expect>
      <if_mismatch>Any over-fire = fix is too aggressive; surface to COO with specifics for debug.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="evidence-table">
    <step>
      <description>Compile evidence table: 6 acceptance criteria × pass/fail × empirical evidence (commit hash, output snippet, dry-run result). Session log entry under org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-13/ (or next-day if VAL fires across midnight UTC).</description>
      <expect>Complete evidence table; no PASS without empirical proof.</expect>
      <if_mismatch>Insufficient evidence = re-run sweep with better instrumentation; do not RAVC2 close on incomplete proof.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: DRIFTD.001 sweep — 3 historical incidents reproduce correct last_deployed_commit values (bc4759ad0 + 144493642 + f46a3682e) without manual backfill; sibling Lambdas under shared tf_prefix unchanged.
    AC2: DRIFTD.002 sweep — DS-base 144493642 pre-fix state produces ERROR + halt with actionable message; HEAD parity-clean state passes silently.
    AC3: DRIFTD.003 sweep — quote-in-subject synthetic commit produces valid CHANGELOG.json with correct escaping; comprehensive escape coverage handles backslashes + newlines + control chars defensively.
    AC4: No-regression on legitimate single-Lambda content-touch case (DRIFTD.001 fix); parity-clean builds (DRIFTD.002 fix); ASCII-clean commit subjects (DRIFTD.003 fix).
    AC5: Evidence table compiled in session log with empirical proof for all AC1-4 entries.
    AC6: ADHC_DRIFTD v0.1 phase moves to "Phase 2 COMPLETE" in project JSON; project status moves to "monitoring" or "complete" per COO + CTO concur.
    AC7: MCP RAVC2 close to COO with full evidence table + project-level v0.1 close signal.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>Verify DRIFTD.001 + .002 + .003 RAVC2 evidence trail before sweep; do not run VAL on incomplete prior bundle</phase_1>
    <phase_2>Empirical sweep is the validation; no comp-* tools apply (CI scripts not modeled)</phase_2>
    <phase_3>Post-VAL: update ADHC_DRIFTD.json status + phase fields; COO + CTO co-sign close</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - None (VAL is sweep execution only; no file modifications)

    COORDINATION:
    - No portal/DS/DE impact
    - AE peers FYI-only post-close (project complete; canonical regression test set established)
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure validation sweep. No code changes; no data changes; no reprocess.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-13/ (or next-day) with full evidence table covering AC1-5
    2. ADHC_DRIFTD.json updates: status → "complete" or "monitoring"; phase → "Phase 2 COMPLETE" + close-out date
    3. MCP RAVC2 close to COO with evidence table + v0.1 close signal
    4. Cleanup: delete absorbed standalone TO `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/record-terraform-deploy-content-commit-fix.md` (folded into DRIFTD.001 + .003; canonical TOs now own the scope)
  </deliverables>

  <ravc>
    AE 0.7 RAVC2 to COO post-AC1-7 PASS. COO ratifies + relays to CTO for project-level v0.1 close co-sign. Project JSON updates committed by COO post-CTO co-sign.
  </ravc>

  <notes>
    **Dispatch hold:** dispatch_held=true until DRIFTD.001 + .002 + .003 RAVC2s ALL pass. COO unblocks dispatch by sending MCP to AE 0.7 with "DRIFTD.VAL dispatch unblocked; proceed sweep."

    **Phase 2 acceptance:** ADHC_DRIFTD v0.1 scope = DRIFTD.001 + .002 + .003 + .VAL. All 4 must PASS AC for v0.1 to close. Future versions (v0.2+) extend if empirical edge cases surface.

    **Memory entry candidate post-VAL close:** 3-incident-day pattern as architectural-priority promotion signal — links to feedback_phase0_audit_before_phase1_authoring + feedback_prd_authoring_gold_consumer_column_audit per CTO PRD §10 cross-reference.

    **Author identity for commit (project JSON updates):** post-VAL close, COO commits project JSON updates under `--author="2.0.0_SA_COO <2.0.0_SA_COO@opal.agent>"`.
  </notes>
</task_order>
