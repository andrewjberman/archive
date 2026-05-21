<task_order>
  <metadata>
    <id>ADHC_VALGATE.007</id>
    <slug>ae-classb-chainrun-prepost-sentinel-diff</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-18 (re-homed base->~B + GO'd 2026-05-21 by 2.0.0_SA_COO~B)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO'd 2026-05-21 by 2.0.0_SA_COO~B. VALGATE Phase 1 (.001-.003, the Class-C suite) is CLOSED -- the chain-gate surface + verdict conventions landed. CTO~B (VALGATE arch owner) pre-reviewed .007 GO-ready (152719Z verdict -- WARN-mode v1, reuses the .001-.003 Class-C conventions, the cosmetic orion-gold-dispatch.sh echo-fix folded in). Andrew brought 0.7.0_AE_CloudOps~B online; .007 re-homed from the base 0.7.0_AE_CloudOps dir to the ~B lane dir + issued_to fixed. Zero CTO gate at dispatch. RAVC2 routes to CTO~B CC COO~B.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P2 -- VALGATE Phase 3. Class B HALF-exists: the chain-run shape sentinels exist but the GATE (structural fire + pre/post diff) does not. N7 = formalize it.</priority>
    <sla>1.5-2d wall (PRD section 6 sizing) -- part discipline-codification (a TO-template mandate), part tooling (a comp-chainrun pre/post wrapper).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.B (Class-B formalization, N7), section 2 (Class B is PARTIAL today -- sentinels exist, no pre/post diff), section 3.2 gate anatomy.</prd>
    <anchor>DWSPLT chain #26 partial-refactor leak -- a consumer signature mismatch surviving an atomic-bundle ship; forward-fix dd1206258 validated by chain #27.</anchor>
  </references>

  <context>
    Class B catches partial-refactor leaks: a helper signature changes and a consumer is not updated; an atomic bundle drops a sibling. Today the chain-run A/B/C/D-stage SHAPE sentinels exist -- but they are run by worker discipline, not structurally, and there is NO pre/post sentinel-diff. The GATE does not exist. N7 = formalize it.

    The Class-B gate has two halves:
    1. Discipline codification -- a TO-template mandate: every atomic-bundle TO (a multi-commit refactor touching a producer + its consumers) carries a Phase-N chain-run pre/post gate step.
    2. Tooling -- a comp-chainrun pre/post wrapper: capture the A/B/C/D-stage sentinel set on a mode=full run BEFORE the bundle, capture again AFTER, diff. A sentinel that flips green-to-absent or changes shape is a partial-refactor leak.
  </context>

  <scope>
    <step>Phase 1 -- the comp-chainrun pre/post wrapper: a tool that captures the chain's A/B/C/D-stage sentinel set (artifact-exists / columns-present / row-count>0 per stage) into a snapshot, and diffs two snapshots (pre-bundle vs post-bundle). Output: the set of sentinels that flipped (green-to-absent, or shape-changed) = the partial-refactor-leak report.</step>
    <step>Phase 2 -- the discipline codification: a TO-template mandate that every atomic-bundle TO carries a Phase-N pre/post chain-run gate step (capture pre-snapshot before the bundle ships, post-snapshot after, diff, verdict). Add it to the TO template + org/XXX.md / TO_COMPILER_GATE references as appropriate (COO/CTO own the template surface -- coordinate if the XXX.md edit is out of AE lane, per the OWNPTH precedent).</step>
    <step>Phase 3 -- fill the section-3.2 six-field gate table for the Class-B gate. Verify the wrapper on a real chain: a pre/post snapshot pair around a no-op produces an empty diff; a synthetic dropped-sentinel produces the expected leak report.</step>
  </scope>

  <gate_verdict_policy>The Class-B gate ships WARN-not-BLOCK in v1 (PRD section 7 Q1) -- a pre/post sentinel diff surfaces the leak; ratchet to BLOCK after the false-positive rate is known.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam gaps (if the wrapper adds any new AWS API surface -- e.g. reading chain telemetry from S3)</run>
        <expect>No new IAM gap. If the wrapper only reads existing chain-log / sentinel surfaces with existing permissions, state N/A in one line.</expect>
        <if_mismatch>Fix iam.tf before deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-chainrun pre/post (the new wrapper, on a real chain pair)</run>
        <expect>The wrapper captures + diffs sentinel snapshots end-to-end; an empty diff on a no-op, a leak report on a synthetic drop.</expect>
        <if_mismatch>Debug the snapshot/diff logic.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A chain-run validation gate + a tooling wrapper + a TO-template mandate; no data pipeline producer modified, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    The comp-chainrun wrapper reads the chain's sentinel surface -- it does not modify orion-gold-dispatch.sh's chain logic. If a structural fire-point in the dispatcher is needed, coordinate with the dispatcher lane (AE 0.7.0 owns it) and with whatever VALGATE.001 established as the Class-C gate surface (reuse conventions, do not fork). The TO-template / XXX.md edit (Phase 2) is COO/CTO template surface -- if owned-paths lane-blocks an AE commit there, surface to COO (OWNPTH precedent).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The comp-chainrun pre/post wrapper ships: it captures the chain A/B/C/D-stage sentinel set into a snapshot and diffs two snapshots, reporting sentinels that flipped green-to-absent or shape-changed.</ac>
    <ac id="AC2">The discipline-codification mandate is added to the TO template (every atomic-bundle TO carries a Phase-N pre/post chain-run gate step) -- committed, with the XSS-template/XXX.md surface handled per lane (COO-coordinated if needed).</ac>
    <ac id="AC3">Verified: a no-op pre/post pair yields an empty diff; a synthetic dropped/shape-changed sentinel yields the expected partial-refactor-leak report. Section-3.2 six-field table filled.</ac>
    <ac id="AC4">No emoji; Rule 16 (the wrapper is local-runtime if bash); session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The comp-chainrun pre/post sentinel-diff wrapper.
    - The atomic-bundle TO-template pre/post-gate mandate.
    - The section-3.2 six-field gate table for the Class-B gate.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>

  <followon_note date="2026-05-20" by="2.0.0_SA_COO~B" source="CTO~B re VALGATE.002">
    COSMETIC FIX TO FOLD IN -- orion-gold-dispatch.sh line ~684: the echo still reads "(C-1 row-count / C-2 distribution)" but VALGATE.002's C-3 gate now rides the SAME valgate_gate.py invocation, so the log text is stale. When .007 next touches orion-gold-dispatch.sh, correct that one-line echo to also name C-3 (and C-4 if .003 has landed by then). Pure log text, no behavior change -- bundle it into the .007 edit so it is not a separate owned-paths touch.
  </followon_note>

  <coo_close date="2026-05-21" by="2.0.0_SA_COO~B">
    ADHC_VALGATE.007 RAVC2 ACCEPTED -- CLOSED. AE~B (0.7.0_AE_CloudOps~B) RAVC2; CTO~B output-validation: CONFIRM PASS; COO~B independent validation: PASS.

    AE~B commits (origin/CLOUD): b56077081 (comp-chainrun -- the Class-B chain-run pre/post sentinel-diff gate: the .tools/comp-chainrun wrapper + org/modules/graph/chainrun_cli.py engine + the in-code CHAIN_MANIFEST + comp-tools.yaml entry) + 445b3033d (the (D) cosmetic orion-gold-dispatch.sh [VALGATE-C] echo fix -- C-1/C-2/C-3/C-4 named) + 6ac2c56b3 (session log + TO status). Phase-2 codification by COO~B: ef55ab6cf (A -- the atomic-bundle SPECIAL CASE in org/ref/TASK_ORDER_PROTOCOL.md) + 9465d8bab (B -- Rule 9 in org/standards/TO_COMPILER_GATE.md).

    COO~B INDEPENDENT VALIDATION: ran `comp-chainrun selfcheck` -- ALL PASS, 12/12: snapshot captures the 4 stage-sentinels; no-op pre/post diff -> 0 leaks / PASS; synthetic DROPPED + COLUMNS-LOST + EMPTIED -> the 3 expected leak rows / WARN; benign column-add -> NOT a leak; WARN verdict + exit-code mapping (WARN->0, v1 WARN-not-BLOCK); unreadable artifact -> INDETERMINATE, not a false green->absent.

    ACs: AC1 (the comp-chainrun pre/post wrapper ships) MET -- CTO~B + COO~B both confirmed. AC2 (the atomic-bundle TO-template mandate) MET -- (A) the SPECIAL CASE in TASK_ORDER_PROTOCOL.md + (B) Rule 9 in TO_COMPILER_GATE.md both applied (COO~B, ANY_EXEC lane); (C) the org/XXX.md pointer documented-SKIPPED (lane=BASE_EXEC, no ~B exec can commit it, optional -- (A)+(B) are the substantive codification). AC3 (verified -- no-op empty diff, synthetic-leak report; the section-3.2 six-field table = GATE_SPEC["B"]) MET. AC4 (no emoji; local-runtime; session log; RAVC2) MET. (D) the VALGATE.002 followon orion-gold-dispatch.sh echo-fix folded in + shipped.

    DESIGN NOTE (CTO~B-ratified): AE~B moved the stage-sentinel set from a standalone chainrun_manifest.json to an in-code CHAIN_MANIFEST dict -- the faithful match to the Class-C in-code registries (ARTIFACT_CONFIG/SENTINEL_REGISTRY in valgate_baseline.py); a separate JSON would have been the fork the TO said not to make. Verdict model verbatim-reused from valgate_gate.py (GATE_VERDICT_POLICY="warn" v1, [VALGATE-B] paralleling [VALGATE-C]).

    OUTCOME: ADHC_VALGATE.007 (Class-B chainrun pre/post sentinel-diff gate, Phase 3) COMPLETE. ADHC_VALGATE is now 6/9 TOs closed (.001/.002/.003 Class-C + .007 Class-B + .008/.009 parity-catalog). REMAINING: .004/.005/.006 (Class-D, DE-lane) -- gated on Andrew's 0.4.0_DE_ClientPlatform~B session spin-up. ADHC_VALGATE the project stays ACTIVE.
  </coo_close>
</task_order>
