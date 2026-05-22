<task_order>
  <metadata>
    <id>YALP_MDSRC.M2</id>
    <slug>ds-macro-data-contract-verify-channel-validation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- COMPLETE 2026-05-22 by 0.1.0_DS_MarketIntelligence. Verify-channel pass done: 80 CONFIRMED / 1 REWORK (idx 41 MARTSSM44X72USS 404 -> M1). Deliverables: docs/briefs/mdsrc-m2-validated-macro-contract-20260522.{md,tsv}. YCharts coverage of the 19 originating-body rows: 15 carried / 4 not (idx 1/4/5/29). RAVC2 to COO CC CTO. -->

    <!-- GATE CLEARED 2026-05-21 by COO: TO-M1 delivered + RAVC2'd (the 81-row macro data contract, commit d9f8cd2c7; docs/briefs/mdsrc-m1-macro-data-contract-20260521.{md,tsv}). M2's input now exists. Flipped staged->pending, dispatch_held->false, GO fired to 0.1.0_DS. -->

    <dispatch_unblock_condition>STAGED — gated on TO-M1 delivery. WS-C of YALP_MDSRC PRD v0.4 (6543894ce), PRD §6 "TO-M2". M2 independently validates the M1 macro data contract — verifier != author (R5), so M2's owner (0.1.0_DS_MarketIntelligence) is deliberately a DIFFERENT agent + a DIFFERENT pod than M1's owner (0.2.0_DS~A). COO flips M2 staged -> pending + fires the GO when M1 RAVC2s its contract. M2's load is sequential-after-M1 — by M1 delivery, 0.1.0_DS's V1 verification is expected complete.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — WS-C. The verify-channel pass that makes the macro contract trustworthy; Andrew's "cannot hallucinate" requirement.</priority>
    <sla>~1-2 effort-days — independent verification of ~91 source claims.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §6 TO-M2, §4 R5.</prd>
    <m1>YALP_MDSRC.M1 (0.2.0_DS~A) — the enumerated macro data contract. M2's input; delivered via M1's RAVC2.</m1>
    <verify_channel>.claude/skills/verify-channel/ — the verify-channel method (EXISTS / FRESH / SCALED / NOT-FROZEN; verifier != fixer; sharpest-test-binds).</verify_channel>
  </references>

  <context>
    M1 authors the macro data contract — ~91 indicators each mapped to a candidate authoritative source + a sourcing verdict. M1 does NOT self-certify. M2 is the independent verify-channel pass: confirm every source claim is real, not assumed. R5 — "cannot hallucinate" is the bar: no row ships CONFIRMED on an assumed source. Verifier != author — M2's owner is a different agent + different pod than M1's, deliberately.

    M2 is GATED on M1 delivery (sequential, not concurrent). On M1's RAVC2, COO flips M2 to pending + fires the GO.
  </context>

  <scope>
    <in_scope>
      - Independently validate every source claim in the M1 contract via the verify-channel method (EXISTS / FRESH / SCALED / NOT-FROZEN).
      - For each non-Bloomberg-verdict indicator: confirm the named series actually EXISTS at the named source, pull it live, and confirm recent values reconcile with the current Bloomberg value (within expected revision tolerance).
      - Output: a validated contract — every row either CONFIRMED (source verified live) or REWORK (claim failed verification — back to M1). Per indicator, state the deployable source verdict with evidence.
      - RAVC2 the validated contract to COO + CC CTO; route REWORK rows back to M1 (0.2.0_DS~A).
    </in_scope>
    <out_of_scope>
      - Authoring or fixing the contract — verifier != author. A failed claim returns to M1 as REWORK; M2 does not re-author it.
      - Implementing macro re-sourcing — M2 validates the contract; migration is downstream.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: verify-channel method — read actual source state (the live API/series), never TO-M1's self-report.
  Phase 2: sharpest-test-binds — a series that EXISTS but is FROZEN or scale-mismatched fails.
  Phase 3: decision-useful meta-gate — the validated contract states, per indicator, the deployable source verdict with evidence.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - GATED on M1 — M2 starts on M1's RAVC2 (the delivered contract). COO flips staged -> pending then.
    - Verifier != author (R5): M2 owner 0.1.0_DS_MarketIntelligence, M1 owner 0.2.0_DS_PortfolioAnalytics~A — different agent, different pod (independent verification). REWORK rows route back to M1.
    - No code/silver/bronze/gold/S3 changes — M2 produces a validated contract document. Auto-rule 4 N/A.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every non-Bloomberg-verdict row in the M1 contract independently verify-channel-validated; the source state read live, never from M1's self-report (Phase 1).
    - AC2 — sharpest-test-binds applied: a series that EXISTS but is FROZEN or scale-mismatched is failed, not passed (Phase 2).
    - AC3 — every row resolved CONFIRMED (verified live, with evidence) or REWORK (failed — routed back to M1); no row CONFIRMED on assumption.
    - AC4 — committed validated contract stating the deployable source verdict per indicator; session log Compiler Tools section; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
