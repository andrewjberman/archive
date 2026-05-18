<task_order>
  <metadata>
    <id>MDPF_ASSETS.001</id>
    <slug>dsa-49f-blackdiamond-book-custody-cutout-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. Phase 0 investigation, read-only, no gate. Andrew brought up DS~A for the MDPF_ASSETS Phase-0 trio -- start on boot.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF_ASSETS Phase 0 (WS-E). The 49F non-model AUA is a frozen ~$272M plug; this audit is the empirical basis for replacing it. Phase 0; ends in a finding brief, NO implementation.</priority>
    <sla>~4-6h wall -- a Black Diamond book audit + the cutout enumeration + the brief.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.1, 1.0.0_SA_CTO, 3406a2edd) -- section 3.4 (49F non-model AUA = certified_aua - model_aua - Σ custody cutouts), section 4 WS-E, section 6.2 Phase 0, section 6.3 seed MDPF_ASSETS.001.</prd>
    <superseded_brief>docs/briefs/smartx-non-model-live-derivation-20260513.md -- the BD-`certified_aua`-minus-model approach; this TO's audit is the WS-E starting point + the cutout-layer refinement that supersedes it.</superseded_brief>
    <known_cutout>PRD section 3.4 -- the known cutout is ~$70M of Fidelity-custodied assets tracked in Black Diamond, EXCLUDED from Opal advised AUA.</known_cutout>
    <enterprise_total>49F enterprise total (`certified_aua`) -- live daily at s3://opal-data-bd/gold/aua_certification/{date}.json (BD pipeline).</enterprise_total>
  </references>

  <context>
    The Model Portfolios page's non-model 49F AUA has been a frozen ~$271.2M plug since 2026-01-05 (the upstream 49F CSV died 2025-12-26). MDPF_ASSETS WS-E replaces it with a real daily figure: non_model_aua(49F) = certified_aua(49F) - model_aua(49F) - Σ excluded-custody cutouts. Phase 0 (this TO) is the audit that enumerates the cutouts and confirms the derivation is sound BEFORE any pipeline is built. This is investigation only -- it produces a finding brief, not code.
  </context>

  <scope>
    <in_scope>
      - Audit the 49 Financial book as represented in Black Diamond: enumerate the account/custody structure, identify which assets are Opal-advised vs not.
      - Confirm the ~$70M Fidelity-custodied cutout EMPIRICALLY -- locate it in the BD book, report the actual current figure and how it is identified (custodian field / account-type / tag).
      - Enumerate ALL other clean custody-based or account-type-based cutouts -- assets in the 49F BD book that should NOT count toward Opal advised AUA. For each: the dollar magnitude, the identifying attribute, and the rationale.
      - Assess the section-3.4 derivation feasibility: is `certified_aua - model_aua - Σ cutouts` a clean, daily-computable identity given what BD exposes? Identify any gap (e.g. model_aua not separable in the BD book, cutouts not machine-identifiable).
      - Document the data source + access path for each input (so the WS-E Phase-1 build TO can be scoped off concrete paths).
    </in_scope>
    <out_of_scope>
      - Building the non_model_aua(49F) pipeline -- that is the WS-E Phase-1 build TO, authored after this Phase-0 brief.
      - Re-deciding AUA certification methodology -- BD `certified_aua` stays the 49F enterprise system-of-record (PRD section 1.4).
      - Inflection non-model AUA (PRD section 7 Q3 -- that surfaces under MDPF_ASSETS.003).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="grounding the audit">
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/aua_certification/ | tail -5</run>
        <expect>Recent daily aua_certification/{date}.json partitions present -- the live certified_aua source for the section-3.4 identity.</expect>
        <if_mismatch>If the path is empty or stale, note it in the brief -- the certified_aua input freshness is a WS-E Phase-1 dependency.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_02.client_performance (or whichever BD gold script the audit finds carries the 49F account/custody breakdown)</run>
        <expect>The BD gold script's I/O surface -- READS/WRITES -- to ground which artifact carries the account-level custody detail. If no BD gold script models the custody breakdown, the audit is a direct Black-Diamond-platform investigation -- state that in one line.</expect>
        <if_mismatch>Record the actual artifact/path the audit relies on in the brief.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Read-only investigation; produces a finding brief, no script modified, no artifact written.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Read-only investigation of the BD pipeline's 49F book + the certified_aua artifact -- no edit, no concurrent-edit hazard. The WS-E Phase-1 build TO (authored after this brief) will carry the cross_domain_coordination block vs the BD pipeline per PRD section 6.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The ~$70M Fidelity-custodied cutout is confirmed empirically -- the actual current figure + the identifying attribute (custodian/account-type/tag) by which it is machine-separable, reported with evidence.</ac>
    <ac id="AC2">A complete enumeration of custody-based / account-type cutouts in the 49F BD book -- each with dollar magnitude, identifying attribute, and exclusion rationale. "Fidelity only, no others found" is an acceptable result IF the audit was exhaustive and says so.</ac>
    <ac id="AC3">The section-3.4 derivation (certified_aua - model_aua - Σ cutouts) feasibility is assessed -- clean/daily-computable, or the specific gaps named (e.g. model_aua not separable, a cutout not machine-identifiable).</ac>
    <ac id="AC4">A finding brief committed under docs/briefs/ presenting AC1-AC3 + the concrete data sources/paths for each section-3.4 input.</ac>
    <ac id="AC5">Session log with the Compiler Tools section reproducing the mandate runs. RAVC2 to COO. The TO completes when the brief + escalation/handoff are delivered -- "complete" means the audit is done, not that the pipeline is built.</ac>
  </acceptance_criteria>

  <deliverables>
    - docs/briefs/mdpf-49f-nonmodel-custody-cutout-audit-20260518.md -- the WS-E Phase-0 finding brief.
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO -- the brief is the input to the WS-E Phase-1 build TO.
  </deliverables>
</task_order>
