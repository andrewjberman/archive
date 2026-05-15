<task_order>
  <metadata>
    <id>ADVI_INFFIN.025</id>
    <slug>rd-books-fee-containers-summary-investigate-first</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RD 0.4.2 bench-clear post H3 FE patch close. Wave 2 dispatch parallel with DS lane.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Books tab fee containers + summary table missing; Andrew direct walkthrough</priority>
    <sla>~2-3h wall actual (~30min Phase 1 investigation + ~1-2h Phase 2 FE wire)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.6a + §3.6b (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ image #7: "missing some key things. I know on the frontend there should be a green and pink container at the top for fee paying and non fee paying accounts and values and etc as its done in 49" + "clearly we know the rates on all the accounts so not sure why that is not being populated in the fee summary table"</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Books tab → FEE SUMMARY panel + missing fee-paying/non-fee-paying header containers</ref>
    <ref type="49f_pattern">49F Books tab BookView green/pink container pattern (port source)</ref>
  </references>

  <context>
    Per COO Q3 routing decision: investigate rate-emit-gap FIRST before authoring fix. If rate already on gold emit, FE-only wire. If gap confirmed, cascade INFFIN.026 for DS rate-emit-augment.

    Two issues bundled:
    - §3.6a: Add green/pink fee-paying / non-fee-paying header containers (port 49F BookView pattern)
    - §3.6b: Populate Fee Summary table — Fee/Total(bps)/Split(bps) columns currently empty
  </context>

  <objective>
    Phase 1 investigate rate-emit on gold platinum artifact; Phase 2 port 49F green/pink header containers; Phase 3 wire Fee Summary table values (if rate available, else cascade INFFIN.026).
  </objective>

  <scope>
    <files>
      <file action="readonly_reference">portal FE 49F BookView component (port source)</file>
      <file action="modify">portal FE Inflection Books tab header (add green/pink containers)</file>
      <file action="modify">portal FE Inflection Books tab Fee Summary table component</file>
      <file action="readonly_reference">platinum/inflection/firm/{books artifact} — verify rate emit shape</file>
    </files>
  </scope>

  <phase id="1" when="rate-emit investigation">
    <step>
      <run>S3 inspect platinum Inflection books artifact: aws s3 cp s3://opal-data-inf/platinum/firm/{books artifact} - | head; search for rate / fee_bps / split_bps fields</run>
      <expect>Either: rate fields present on emit (Path A FE-only wire) OR rate fields absent (Path B cascade INFFIN.026 DS).</expect>
    </step>
    <step>
      <run>comp-pipescript io {books gold script} — confirm emit shape + identify rate source on backend if available</run>
      <expect>Backend rate source identified; emit gap quantified.</expect>
    </step>
  </phase>

  <phase id="2" when="§3.6a green/pink containers">
    <step>
      <run>Read 49F BookView component for green/pink fee-paying/non-fee-paying header pattern; verify Inflection partner data routes through same component</run>
      <expect>Component pattern identified; Inflection partner ID conditional rendering verified.</expect>
    </step>
    <step>
      <run>Port green/pink container shape to Inflection Books tab header; route Inflection partner data through same component</run>
      <expect>Headers render on Inflection Books tab matching 49F.</expect>
    </step>
  </phase>

  <phase id="3" when="§3.6b Fee Summary wiring">
    <step>
      <run>PATH A (rate emit present): wire Fee/Total(bps)/Split(bps) columns to read from platinum emit; populate Fee Summary table</run>
      <expect>Fee Summary table shows real BPS values.</expect>
    </step>
    <step>
      <run>PATH B (rate emit gap): author cascade TO INFFIN.026 for DS rate-emit-augment; current TO ships §3.6a only with cascade routing note for §3.6b</run>
      <expect>Cascade clean; no orphan FE wire.</expect>
    </step>
  </phase>

  <phase id="4" when="commit + RAVC">
    <step>
      <run>Visual smoke: Inflection Books tab green/pink containers + Fee Summary table populated (Path A) OR §3.6a only with cascade note (Path B)</run>
      <expect>Visual smoke evidence for Phase 1+2 + Phase 3 path.</expect>
    </step>
    <step>
      <run>49F regression: green/pink containers + Fee Summary unchanged on 49F</run>
      <expect>49F regression PASS.</expect>
    </step>
    <step>
      <run>safe-commit.sh per Rule 14a + Author identity RD 0.4.2</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 + state which Phase 3 path executed</run>
      <expect>Evidence-bearing close + path attestation.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Phase 1 rate-emit investigation findings documented
    AC2 (§3.6a): Green/pink fee-paying/non-fee-paying header containers render on Inflection Books tab matching 49F shape
    AC3 (Path A): Fee Summary table populated with real BPS values per account
    AC3 (Path B): Cascade INFFIN.026 TO authored for DS rate-emit-augment
    AC4: 49F regression PASS
    AC5: Inflection visual smoke PASS
    AC6: No emoji per CLAUDE.md
    AC7: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-pipescript io + S3 inspect; Phase 4 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: RD H3 FE patch close.
    PARALLEL-OK: All other INFFIN.019-028 sibs.
    POTENTIAL CASCADE: Path B spawns INFFIN.026 for DS lane.
    JOINT WITH .027: §3.6c Account NNA window-wiring is sister to this TO; .027 covers that scope.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-only Path A; Path B cascade for DS emit augment.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Phase 1 rate-emit investigation
    2. §3.6a green/pink containers
    3. §3.6b Path A wire OR Path B cascade
    4. 49F regression evidence
    5. RAVC2
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO + CC CTO + DT 0.4 on AC1-7 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Investigate-first discipline:** per COO Q3 routing + banked feedback `feedback_phantom_consumer_marker_pattern.md` + `feedback_anticipatory_patience_discipline.md` — empirical-first cheaper than authoring wrong fix-TO.

    **§3.6c Account NNA → .027:** keeping scopes split per surface concern (fee containers/summary vs window-wired NNA).

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
