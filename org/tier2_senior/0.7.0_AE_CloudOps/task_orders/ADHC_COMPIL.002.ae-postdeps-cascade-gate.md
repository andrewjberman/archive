<task_order>
  <metadata>
    <id>ADHC_COMPIL.002.ae-postdeps-cascade-gate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>B</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL.md §5 (commit 172470a8)</prd_ref>
    <effort>1–2 weeks</effort>
    <gates_on>None — independent of ADHC_COMPIL.001 and .003</gates_on>
    <gates_for>ADHC_COMPIL.004 (prd-evidence-check.sh stretch — gates on .003, not this TO)</gates_for>
    <sequence_note>Complete ORNREN.002 + ADVI_INFLEC TO-B obligations before starting. This TO has no time gate.</sequence_note>
  </metadata>

  <objective>
    Add a comp-pipescript postdeps enforcement gate to bd-gold-dispatch.sh and
    inf-gold-dispatch.sh so split-cascade reruns abort automatically when a
    required upstream script is missing from the partial chain.
    Prevents AUAGAP.002-class incidents (split rerun skipping required intermediate).
  </objective>

  <scope>
    Modify bd-gold-dispatch.sh and inf-gold-dispatch.sh:

    Gate behavior (--chain partial):
    1. For each script in the partial chain, run: comp-pipescript postdeps <script>
    2. Compute union of all required upstream scripts.
    3. If any required script is NOT in the partial chain:
       - Exit non-zero.
       - Print clear error listing missing scripts.
       - Print a suggested corrected command.
    4. If partial chain is complete (all required scripts present): proceed as today.

    Override: --no-deps-check flag
    - Bypasses the gate (for emergency debug / isolated re-emission cases).
    - Appends a bypass entry to org/compiler-tools-log.md:
      format: [ADHC_COMPIL.002] BYPASS: <timestamp> | <dispatcher> | <chain> | <operator>
    - Must NOT suppress the log entry — it's the accountability trail.

    --chain full: unchanged behavior (full chain by definition includes everything — no gate needed).

    Both dispatchers get identical gate behavior:
    - bd-gold-dispatch.sh: BD gold chain partial reruns
    - inf-gold-dispatch.sh: INF gold chain partial reruns

    Do NOT modify the gate logic to distinguish "required upstream" from "required parallel sibling"
    — treat them identically per PRD §10 Q2 (simpler is correct for v1).
  </scope>

  <acceptance_criteria>
    1. bd-gold-dispatch.sh --chain partial B_00 B_03 (when C_00 is a required
       intermediate) → exits non-zero with error listing C_00 + suggested command.
    2. bd-gold-dispatch.sh --chain partial B_00 B_03 C_00 (complete set) → proceeds normally.
    3. bd-gold-dispatch.sh --chain partial B_00 B_03 --no-deps-check → proceeds AND
       appends bypass entry to org/compiler-tools-log.md.
    4. bd-gold-dispatch.sh --chain full → unchanged behavior (no gate check).
    5. Same three behaviors (AC1–AC3) confirmed for inf-gold-dispatch.sh.
    6. Unit test fixture: AUAGAP.002 reproduction — partial chain that originally
       missed C_00 is caught by the gate (exits non-zero). Fixture committed.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT modify --chain full behavior — full chain does not need the gate.</rule>
    <rule>Do NOT allow --no-deps-check to suppress the org/compiler-tools-log.md bypass entry.</rule>
    <rule>Do NOT start this TO before ORNREN.002 dispatch wiring is complete.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">bd-gold-dispatch.sh: gate + --no-deps-check flag</deliverable>
    <deliverable type="code">inf-gold-dispatch.sh: same</deliverable>
    <deliverable type="code">AUAGAP.002 reproduction fixture (test)</deliverable>
    <deliverable type="document">Session log with AC verification output</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC exit codes, bypass log entry, fixture pass confirmation</deliverable>
  </deliverables>
</task_order>
