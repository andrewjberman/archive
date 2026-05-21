<task_order>
  <metadata>
    <id>YALP_MDSRC.F6</id>
    <slug>dsa-fred-bloomberg-residue-merge-spec</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics~A</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — stimulus-scan reallocation (0.2.0_DS~A idle since F4 completed). Q1-independent. The concrete next FRED implementation step; F4 explicitly flagged this as the integration decision to spec. Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the FRED implementation's integration step. F4 deliberately emitted a SEPARATE FRED artifact to avoid a dual-writer; F6 specs how that artifact and the Bloomberg residue combine into the page's consumed shape. Feeds v0.4 + the F5 deploy's downstream.</priority>
    <sla>~1-2 effort-days — a spec; no production code (a reference merge implementation is optional, see scope).</sla>
  </metadata>

  <references>
    <f4_build_note>docs/briefs/mdsrc-f4-fred-ingestion-build-note-20260520.md (f42c2ab1a) — F4 (your prior TO). F4's pull emits json/macro/macro_data_fred.json (51 FRED indicators) as a SEPARATE artifact — NOT macro_data.json (which yang-generate-macro owns; co-writing it would be a dual-writer). F4 flagged the FRED-vs-Bloomberg-residue MERGE as the integration decision for v0.4 — F6 is that spec.</f4_build_note>
    <f1_brief>docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md — F1's Bloomberg->FRED mapping: ~50 FRED-migratable indicators + the documented non-FRED residue (international/licensed series FRED cannot serve at adequate timeliness).</f1_brief>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md — no dual-writers; the merge must have ONE clear producer of the page's consumed artifact.</standard>
  </references>

  <context>
    The Macroeconomics page consumes macro_data.json (today: all 79 indicators, Bloomberg-pkl-sourced via yang-generate-macro). F4 built a FRED pull emitting a separate macro_data_fred.json (the 51 FRED-migratable indicators). For the page to actually SERVE FRED data, the FRED artifact and the Bloomberg residue (the ~28 indicators FRED cannot serve) must combine into the shape the page reads — without a dual-writer. F6 specs that merge: who produces the merged artifact, how the two sources reconcile, and the cutover. This is the integration decision F4 flagged for v0.4.
  </context>

  <scope>
    <in_scope>
      Specify the FRED-vs-Bloomberg-residue merge:
      - PRODUCER: which single component produces the page's consumed macro artifact post-migration — options to evaluate: (a) yang-generate-macro reads macro_data_fred.json + the Bloomberg residue and writes the merged macro_data.json; (b) a new small merge step; (c) the FRED pull writes the merged artifact directly. Recommend one, with the dual-writer-avoidance reasoning.
      - RECONCILIATION: per-indicator, which source wins (FRED for the 51 migratable; Bloomberg for the ~28 residue); how the boundary is encoded; what happens to an indicator present in both.
      - SHAPE: confirm the merged artifact matches the exact shape MacroTimeSeriesModal + the heatmap consume today (no frontend change) — coordinate the field/shape contract.
      - CUTOVER: the safe sequence to switch the page from all-Bloomberg to FRED+residue — staged or atomic; the rollback; how to verify no indicator regresses.
      - The non-FRED residue list named explicitly (from F1) — these stay Bloomberg; confirm their producer is unaffected.
      Deliverable: a committed merge spec. A reference merge implementation is OPTIONAL — if authored, it is DS-authored + AE-deployed (infra/aws/lambda is AE lane); the spec is the required deliverable.
    </in_scope>
    <out_of_scope>
      - Deploying anything — F5 (AE) deploys the FRED pull; any merge code is a later AE-deployed step.
      - Re-doing the F1 mapping or the F4 pull — those are done; F6 consumes them.
      - The yield-curve / macro-timeseries staleness fixes (F2/F3) — separate, done/in-flight.
      - Frontend changes — the merge matches the existing consumed shape; no FE work.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before"><step><run>comp-pipescript io yang-generate-macro + comp-routes behaviors for the macro_data.json serving path</run><expect>The current producer's I/O + the serving path — anchor the merge-producer recommendation in compiler-confirmed fact.</expect><if_mismatch>Fall back to a source read + document.</if_mismatch></step></phase>
    <phase id="2" when="before commit"><step><run>.tools/ds-commit-gate.sh — only if a reference merge implementation .py is authored; else documented-N/A.</run><expect>If code authored, all three checks exit 0.</expect><if_mismatch>Fix before handoff.</if_mismatch></step></phase>
    <phase id="3" when="after"><step><run>(none) — the spec is the deliverable.</run><expect>Checked by the ACs.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    F6 feeds v0.4 (the FRED-architecture section) and the F5 deploy's downstream. If F6 recommends a merge-code step, that is a later DS-author/AE-deploy TO — flag it, do not build it here. Coordinate the consumed-shape contract with whoever owns the Macroeconomics page artifacts. RAVC2-CC-CTO carries it into v0.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The merge PRODUCER specified — one recommended option, with explicit dual-writer-avoidance reasoning (one clear producer of the page's consumed artifact).</ac>
    <ac id="AC2">The per-indicator RECONCILIATION specified (FRED wins for the 51; Bloomberg for the ~28 residue; boundary encoding; both-present handling) + the merged-artifact SHAPE confirmed to match what the page consumes today.</ac>
    <ac id="AC3">The CUTOVER sequence specified — staged/atomic, rollback, per-indicator no-regression verification.</ac>
    <ac id="AC4">Deliverable: a committed merge spec (e.g. docs/briefs/mdsrc-f6-fred-bloomberg-merge-spec-20260521.md), pushed + push-confirmed on origin/CLOUD. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The FRED-vs-Bloomberg-residue merge spec (committed, push-confirmed).
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT introduce a dual-writer — the merge must have ONE clear producer of the page's consumed artifact (Third-Party Data Integration Standard).</rule>
    <rule>Do NOT deploy or commit infra/aws/lambda code — if a reference merge implementation is authored, it is DS-authored / AE-deployed, flagged as a later TO.</rule>
    <rule>No emojis in the spec, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
