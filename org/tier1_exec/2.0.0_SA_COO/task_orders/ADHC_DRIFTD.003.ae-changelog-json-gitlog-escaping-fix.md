<task_order>
  <metadata>
    <id>ADHC_DRIFTD.003</id>
    <slug>ae-changelog-json-gitlog-escaping-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADHC_DRIFTD</project_code>
    <priority>P2 — same-day empirical incident (SMARTX_NONMDL TO-3 ship; bun JSON.parse failed on commit subjects with unescaped quotes; CHANGELOG.json write silently skipped; AE 0.7 captured stack trace in session log; not user-visible but breaks audit trail integrity)</priority>
    <sla>~30min wall; ship as part of Commit 1 of two-commit bundle (paired with .001 on shared file record-terraform-deploy.sh)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DRIFTD.md §3.3 + §6 TO-3 + §8 acceptance criterion 3</ref>
    <ref type="project_json">org/projects/ADHC_DRIFTD.json</ref>
    <ref type="parent_finding">ADHC_DRIFTD PRD §2.3 — record-terraform-deploy.sh gitLogJson build via shell-string-concatenation + bun JSON.parse validation fails on unescaped " in commit subjects; CHANGELOG.json write skipped silently; audit trail incomplete</ref>
    <ref type="empirical_failure">AE 0.7 SMARTX_NONMDL TO-3 ship 2026-05-13: bun JSON parse error on gitLogJson during record-terraform-deploy.sh execution; stack trace in session log; CHANGELOG.json content unchanged from v2.0.0 state despite v2.1.0 ship (will backfill post-fix)</ref>
    <ref type="source_target">.tools/record-terraform-deploy.sh gitLogJson construction block — shell-string-concatenation of git log --pretty output piped through bun -e 'JSON.parse(process.argv[1])'</ref>
    <ref type="sibling_to">ADHC_DRIFTD.001 — shared file record-terraform-deploy.sh; ship in same Commit 1 of two-commit bundle</ref>
    <ref type="sibling_to">ADHC_DRIFTD.002 — independent file build-and-upload.sh; Commit 2</ref>
    <ref type="sibling_to">ADHC_DRIFTD.VAL — Phase 2 validation sweep includes quote-in-subject empirical test</ref>
  </references>

  <context>
    record-terraform-deploy.sh constructs a `gitLogJson` string via shell-string-concatenation from `git log --pretty=format:"%H %s"` output, then pipes through `bun -e 'JSON.parse(process.argv[1])'` to validate before writing to CHANGELOG.json. When a commit subject contains an unescaped `"` character (or other JSON-unsafe characters like `\`, control chars, newlines), `bun JSON.parse` fails, the script silently skips the CHANGELOG.json write, and the audit trail is incomplete.

    AE 0.7 SMARTX_NONMDL TO-3 ship 2026-05-13 observed this empirically: bun JSON parse error logged in session, CHANGELOG.json unchanged from v2.0.0 state despite v2.1.0 ship. Backfill pending this TO's fix.

    Fix per PRD §3.3 + CTO Q2 ratify: replace shell-string-concatenation with structured JSON construction using Python `json.dumps` (or equivalent escaping pathway in Node.js if Node path is also affected). `json.dumps` correctly escapes ALL JSON-unsafe characters (quotes, backslashes, newlines, control chars) — defensive against future commit-subject characters beyond the empirically-observed quote case.

    CTO Q2 ratify: normalize ALL JSON-unsafe chars (one-shot defensive fix; zero added complexity vs targeted quote-only fix).
  </context>

  <objective>
    Replace shell-string-concatenation gitLogJson construction in record-terraform-deploy.sh with structured JSON build:

    ```python
    # Pseudocode
    import json, subprocess
    git_log_records = []
    for line in subprocess.check_output(["git", "log", "--pretty=format:%H\t%s", ...]).splitlines():
        sha, subject = line.split("\t", 1)
        git_log_records.append({"sha": sha, "subject": subject})
    git_log_json = json.dumps(git_log_records)  # python json.dumps handles ALL JSON-unsafe chars correctly
    ```

    Use NUL `\0` as field separator paired with `git log -z --format=...` (git's well-established robust-separator pattern; zero collision risk with any commit content including auto-generated commit subjects that may contain tabs). Validate via `json.loads` round-trip before write. Per CTO 2026-05-13 advisory: NUL preferred over tab because (a) `git log -z` is the canonical robust pattern, (b) edge-case auto-generated commit subjects from tooling can contain tabs, (c) NUL has zero collision risk, (d) Python `s.split('\0')` is identical complexity to `s.split('\t')`.

    Apply same logic to Node.js branch if affected (likely same construction pattern).

    Single commit, paired with DRIFTD.001 on shared file. AC1-5 PASS gates RAVC2 close.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/record-terraform-deploy.sh gitLogJson construction block — replace shell-string-concatenation with structured JSON build via Python json.dumps (and Node.js equivalent if applicable)</file>
    </files>
  </scope>

  <phase id="1" when="before-write">
    <run>comp-blast record-terraform-deploy (already run for .001; reuse evidence)</run>
    <expect>Downstream consumer enumeration covered by .001 Phase 1. SKIP rerun.</expect>
    <if_mismatch>N/A.</if_mismatch>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Locate gitLogJson construction block in record-terraform-deploy.sh (Python branch + Node.js branch if both have it). Identify the shell-string-concatenation + bun JSON.parse validation pattern.</description>
      <expect>Block identified in both branches OR confirmed Python-only.</expect>
      <if_mismatch>If gitLogJson is only in one branch, scope reduces to single-branch fix.</if_mismatch>
    </step>
    <step>
      <description>Replace shell-string-concatenation with structured JSON build using Python json.dumps (or Node.js JSON.stringify on a proper object array, not a constructed string). Use NUL `\0` field separator paired with `git log -z --format=...` (git's canonical robust-separator pattern; preferred over tab per CTO 2026-05-13 advisory because some auto-generated commit subjects from tooling may contain tabs; NUL has zero collision risk).</description>
      <expect>git log output parsed line-by-line into structured records; json.dumps (or JSON.stringify) produces correctly-escaped JSON string with ALL JSON-unsafe chars handled (quotes, backslashes, newlines, control chars).</expect>
      <if_mismatch>If json.dumps round-trip fails on synthetic edge-case commit, debug escaping pathway.</if_mismatch>
    </step>
    <step>
      <description>Round-trip validate: json.loads(json_string) before write; assert deserialized records match in-memory list. Fail loud + halt write on validation failure.</description>
      <expect>Round-trip validation succeeds on parity-clean inputs; fails loud (not silent skip) on construction error.</expect>
      <if_mismatch>If round-trip fails on legitimate input, escaping pathway is wrong — debug.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Synthetic commit empirical test: create synthetic commit with subject containing `"` character (e.g., `git commit -m 'fix "edge case" in foo'`), run record-terraform-deploy.sh logic against it. Verify CHANGELOG.json write succeeds with correctly-escaped entry.</description>
      <expect>CHANGELOG.json contains the quote-in-subject entry with proper escaping (e.g., `"subject": "fix \"edge case\" in foo"`).</expect>
      <if_mismatch>If write fails or escaping is wrong, debug + fix before commit.</if_mismatch>
    </step>
    <step>
      <description>Comprehensive escape test: synthetic commits with backslash, newline (multi-line subject if git supports), control char, mixed cases. Verify each writes correctly.</description>
      <expect>All JSON-unsafe chars handled by json.dumps; CHANGELOG.json valid in each case.</expect>
      <if_mismatch>If any char class fails, fix pathway (likely missed branch in defensive escape).</if_mismatch>
    </step>
    <step>
      <description>No-regression on commits with simple ASCII subjects: verify existing CHANGELOG.json entries (pre-fix) round-trip parse cleanly under new logic; no schema change.</description>
      <expect>Existing entries unaffected; schema preserved.</expect>
      <if_mismatch>If schema drift detected, surface to COO before commit.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: record-terraform-deploy.sh gitLogJson construction uses structured JSON build (Python json.dumps or equivalent), NOT shell-string-concatenation. Both Python and Node.js branches updated if both have the pattern.
    AC2: Synthetic commit with quote-in-subject (e.g., `fix "edge case" in foo`) produces valid CHANGELOG.json entry with correct escaping.
    AC3: Comprehensive escape coverage: backslashes, newlines (if achievable), control chars, mixed cases — all handled correctly via json.dumps defensive escaping.
    AC4: Round-trip validation (json.loads on json.dumps output) gates write; fails loud (not silent skip) on construction error.
    AC5: No-regression on ASCII-clean commits: existing CHANGELOG.json schema preserved; no entries lost or modified.
    AC6: AE 0.7 backfills missing v2.1.0 CHANGELOG.json entry post-fix (separate manual recovery; not part of TO scope but logged as cleanup).
    AC7: Session log captures empirical-test verification + commit hash + AC1-5 evidence.
    AC8: MCP RAVC2 close to COO with empirical-test verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-blast record-terraform-deploy (covered by DRIFTD.001 Phase 1; SKIP rerun)</phase_1>
    <phase_2>bash -n syntax check; python -m py_compile on inline Python; ds-precommit-check.py AST validation if Python heredoc; empirical synthetic-commit dry-run BEFORE commit</phase_2>
    <phase_3>DRIFTD.VAL Phase 2 validation sweep includes quote-in-subject empirical regression test</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - .tools/record-terraform-deploy.sh — shared with DRIFTD.001; ship in same Commit 1 of two-commit bundle to avoid merge conflict
    - Independent of DRIFTD.002 (build-and-upload.sh in Commit 2)

    COORDINATION:
    - No portal frontend impact
    - No DS impact
    - AE peers FYI-only (CI hygiene fix with regression test in DRIFTD.VAL)
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure CI audit-trail fix. CHANGELOG.json missing v2.1.0 entry will be backfilled manually post-fix; not a code or data change.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. .tools/record-terraform-deploy.sh gitLogJson construction block replacement (Python branch + Node.js branch if applicable)
    2. Commit 1 of two-commit bundle: DRIFTD.001 + DRIFTD.003 (this file) on shared file record-terraform-deploy.sh — single commit under 0.7.0_AE_CloudOps author
    3. CHANGELOG.json v2.1.0 entry backfill (manual recovery post-fix; separate from TO scope)
    4. Session log with empirical-test verification + AC1-8 evidence
    5. MCP RAVC2 to COO post-AC1-8 PASS (single RAVC2 covers .001 + .003 since same commit)
  </deliverables>

  <ravc>
    Joint RAVC2 with DRIFTD.001 — both ship in same Commit 1, single RAVC2 to COO covers both. COO ratifies + relays to CTO for architectural-fidelity co-sign on PRD §3.3 + §6 TO-3 implementation. DRIFTD.VAL fires post-bundle commit.
  </ravc>

  <notes>
    **Per CTO Q2 ratify (COO co-sign):** normalize ALL JSON-unsafe chars via json.dumps defensive escaping. CTO rationale: "one-shot defensive fix; zero added complexity vs targeted quote-only fix." Future-proof against backslashes, newlines, control chars beyond the empirically-observed quote case.

    **Per CTO 2026-05-13 advisory (cosign message, ADHC_DRIFTD bundle):** field separator updated from tab `\t` (original draft) to NUL `\0` paired with `git log -z --format=...` (canonical robust pattern). CTO marked the change as "not redline-worthy" but structurally safer; AE 0.7 dispatch hadn't started yet so incorporated as free update. Zero implementation cost (Python `s.split('\0')` identical complexity to `s.split('\t')`); zero collision risk with any commit content including auto-generated commit subjects.

    **Two-commit bundle ship plan** (per COO Q3 routing decision):
    - Commit 1: DRIFTD.001 + DRIFTD.003 (this file) on shared file .tools/record-terraform-deploy.sh
    - Commit 2: DRIFTD.002 on independent file .tools/build-and-upload.sh

    **CHANGELOG.json backfill note:** AE 0.7's v2.1.0 ship today did NOT write to CHANGELOG.json due to the bug this TO fixes. Post-fix, AE 0.7 should manually backfill the v2.1.0 entry to CHANGELOG.json (one-shot recovery; not gated as AC).

    **Author identity for commit:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` per agent commit identity protocol.
  </notes>
</task_order>
