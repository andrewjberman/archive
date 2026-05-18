<task_order>
  <metadata>
    <id>MDPF_ASSETS.003</id>
    <slug>dsb-eclipse-inflection-model-aua-feasibility</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. Phase 0 investigation, read-only, no gate. Andrew brought up DS~B for this -- start on boot.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF_ASSETS Phase 0 (WS-C). WS-C is the largest genuinely-new pipeline piece (Eclipse portfolio holdings -> Inflection model AUA); this feasibility probe de-risks it. Phase 0; ends in a finding brief, NO implementation.</priority>
    <sla>~5-7h wall -- the largest of the Phase-0 trio: an Eclipse silver field-coverage probe + the section-7 Q2/Q3 questions + the brief.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.1, 3406a2edd) -- section 3.2 (per-partner model AUA, convergent schema), section 3.3 (ETF ownership decomposition + the look-through question), section 4 WS-C, section 6.3 seed MDPF_ASSETS.003, section 7 Q2 (ETF-position granularity) + Q3 (Inflection non-model AUA).</prd>
    <existing_feeder>ADVI_ECLDAT -- Phases 1-4 SHIPPED. data/orion/scripts/bronze/pull_eclipse_portfolios.py + silver/convert_eclipse_portfolios_to_silver.py + gold/INF_E_00.eclipse_model_portfolios.py; s3://opal-data-inf/silver/eclipse/ live.</existing_feeder>
    <convergent_schema>PRD section 3.2 -- every model-AUA feeder must converge to `(firmId, model_id, as_of_date, model_value, holdings[])`. WS-C must emit Inflection model AUA in this shape, tagged firmId=inflection.</convergent_schema>
  </references>

  <context>
    WS-C routes ADVI_ECLDAT's Eclipse portfolio ingestion (Inflection portfolios + per-Opal-model composition) into the MDPF canonical model-AUA schema. ADVI_ECLDAT already ships bronze + silver + the INF_E_00 gold script for Eclipse; WS-C is the gold layer that turns Eclipse portfolio holdings into Inflection model AUA. This is the largest genuinely-new pipeline piece in MDPF_ASSETS. Phase 0 (this TO) confirms BEFORE the build that the Eclipse data carries what model-AUA needs. Investigation only -- a finding brief, no gold script authored.
  </context>

  <scope>
    <in_scope>
      - Inspect the Eclipse silver (convert_eclipse_portfolios_to_silver.py output, s3://opal-data-inf/silver/eclipse/) and the INF_E_00.eclipse_model_portfolios.py gold script. Document what fields they carry: portfolio identity, per-Opal-model composition, model values, holdings, as_of dates, the partner/firm identity.
      - Assess coverage vs the PRD section-3.2 convergent schema `(firmId, model_id, as_of_date, model_value, holdings[])`: does the Eclipse silver carry every term, or are there gaps a WS-C gold layer must derive/fill?
      - PRD section 7 Q2 (look-through): confirm at what granularity the Eclipse holdings feed exposes ETF positions -- if an Inflection Opal-model holds an Opal ETF (DIVZ/IDVZ/PFDE/PFOE) as a line-item position, ETF attribution (section 3.3 held_inflection) is clean; if models are look-through to underlying securities, the ETF attribution needs a different derivation. Report which.
      - PRD section 7 Q3 (Inflection non-model): determine whether Inflection has non-model advised assets, and if so what the source would be. This may be a WS-C extension or a new workstream -- surface the finding, do not scope it here.
      - Document the concrete Eclipse silver paths/fields so the WS-C Phase-1/2 build TO can be scoped off them.
    </in_scope>
    <out_of_scope>
      - Building the WS-C Inflection-model-AUA gold layer -- that is the Phase-2 build TO, authored after this brief + after WS-A (the canonical schema) lands.
      - Modifying ADVI_ECLDAT's bronze/silver -- read-only inspection only.
      - The ETF ownership decomposition compute itself (WS-D.2).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="grounding the probe">
      <step>
        <run>comp-pipescript io INF_E_00.eclipse_model_portfolios</run>
        <expect>The Eclipse gold script's I/O surface -- READS (the Eclipse silver) + WRITES + any COLUMN GAPS. Grounds what the Eclipse gold tier already produces vs what WS-C model-AUA needs.</expect>
        <if_mismatch>If INF_E_00 is not modeled or the I/O differs from the ADVI_ECLDAT shipped state, inspect convert_eclipse_portfolios_to_silver.py + the silver artifact directly and record the actual fields in the brief.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-inf/silver/eclipse/ | tail -5</run>
        <expect>The live Eclipse silver partitions -- the artifact the field-coverage assessment reads.</expect>
        <if_mismatch>If empty/stale, note the ADVI_ECLDAT silver freshness in the brief -- it is a WS-C dependency.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Read-only investigation; produces a finding brief, no script modified, no artifact written.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Read-only inspection of ADVI_ECLDAT's shipped Eclipse bronze/silver/gold -- no edit, no concurrent-edit hazard. ADVI_ECLDAT keeps its own project code (PRD section 6.1 boundary ruling); this TO does not re-parent it. The WS-C Phase-2 build TO (authored after this brief + after WS-A) carries the cross_domain_coordination block vs ADVI_ECLDAT per PRD section 6.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The Eclipse silver + INF_E_00 field inventory is documented -- portfolio identity, per-Opal-model composition, model values, holdings, as_of dates, firm identity -- with the concrete paths/fields.</ac>
    <ac id="AC2">Coverage verdict vs the PRD section-3.2 convergent schema (firmId, model_id, as_of_date, model_value, holdings[]): every term mapped to an Eclipse-silver field, OR the specific gaps named that a WS-C gold layer must derive.</ac>
    <ac id="AC3">PRD section 7 Q2 answered: the granularity at which the Eclipse holdings feed exposes ETF positions -- line-item (clean attribution) vs look-through-to-underlying (needs a different derivation) -- stated with evidence.</ac>
    <ac id="AC4">PRD section 7 Q3 surfaced: whether Inflection has non-model advised assets + the candidate source, framed as a finding (WS-C extension vs new workstream) -- NOT scoped/built here.</ac>
    <ac id="AC5">A finding brief committed under docs/briefs/ presenting AC1-AC4 + the concrete Eclipse-silver paths for the WS-C build TO.</ac>
    <ac id="AC6">Session log with the Compiler Tools section reproducing the mandate runs. RAVC2 to COO. "Complete" = the feasibility is determined, not that the gold layer is built.</ac>
  </acceptance_criteria>

  <deliverables>
    - docs/briefs/mdpf-eclipse-inflection-model-aua-feasibility-20260518.md -- the WS-C Phase-0 finding brief.
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO -- the brief is the input to the WS-C Phase-2 build TO.
  </deliverables>
</task_order>
