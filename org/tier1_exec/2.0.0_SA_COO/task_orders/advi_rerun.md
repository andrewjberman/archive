# Task Order: ADVI Thread Re-run and Task Order Re-issue — 2.0.0_SA_COO

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-03-advi-rerun</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    ADVI-001, ADVI-002, and ADVI-003 were run with gpt-4o before prompt enrichment
    and produced low-quality contracts (unverified field names, placeholder colorMap
    values, missing geo_drill in cla_timeseries, books_tab_design_brief.md never written).
    Re-run all three as ADVI-004/005/006 under the proper system, then re-issue task
    orders split by thread serial. Immediate unblocked streams have already been issued
    directly by CTO — your job is the thread re-run sequence and post-receipt task orders.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="project">org/projects/ADVI.json</ref>
    <ref type="thread-knowledge">org/threads/THREAD_KNOWLEDGE.md</ref>
    <ref type="page-codes">org/projects/PAGE_CODES.md</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- PHASE 0 — Prerequisites before running any thread               -->
    <!-- ================================================================ -->
    <requirement id="P.1">
      O3 is SATISFIED. Agents have enriched prompts, tools-enabled threads (direct file
      read during run), and 84 v1 session logs accessible via logs/sessions/ fallback.
      Do NOT wait for new session logs before running ADVI-004 and ADVI-005.
      Run them now. ADVI-006 (Books) may wait until DS/DE/RD have multiple current
      session logs — it is the most complex thread and benefits from richer context,
      but 004/005 should execute immediately.
    </requirement>
    <requirement id="P.2">
      Before creating any staging script, verify the BESPOKE_TEMPLATE.sh exists:
        org/threads/staging/BESPOKE_TEMPLATE.sh
      All three staging scripts are based on this template.
    </requirement>

    <!-- ================================================================ -->
    <!-- ADVI-004 — Continuous NNA ADV + CLA timeseries alignment        -->
    <!-- Replaces ADVI-001 (superseded — see ADVI.json)                  -->
    <!-- ================================================================ -->
    <requirement id="T004.1">
      Create staging script: org/threads/staging/run-ADVI-004-adv-drill-cla-timeseries.sh
      Configuration:
        PROJECT="ADVI"
        THREAD_ID=""  (auto-assigned as ADVI-004)
        PARTICIPANTS="0.4.0_DS_ClientPlatform 0.4.0_DE_ClientPlatform 0.4.2_RD_AdvisorIntelligence"
        TURN_ORDER="round_robin"
        MODEL="gpt-5.2"
        MAX_TURNS_PER_AGENT=3
        TOOLS_ENABLED=true
    </requirement>
    <requirement id="T004.2">
      M1 context files to inject (copy into context/refs/):
        infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py
        portal/src/pages/AdvisorIntelligence/types.ts
        portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
        org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </requirement>
    <requirement id="T004.3">
      M4 inline briefing (add to CONTEXT.json inline field):
        "This is a re-run of a previous alignment thread that produced low-quality contracts.
        Three specific gaps must be resolved this time:
        (1) cla_timeseries must include geo_drill (city-level drill within each state) —
            it was missing from ADVI-001 despite being required by the PRD.
        (2) colorMap values must be actual portal color token names or hex values from
            the existing portal color system — not placeholder strings like '#green'.
            RD: read DistributionTab.tsx to confirm what color tokens are in use.
        (3) The NMNC/NMEC 12-month window rule proposed in ADVI-001 was not verified
            against the existing header_metrics.json CLA structure. DS must confirm
            how NMNC/NMEC is defined in the current gold layer output, not assume it."
    </requirement>
    <requirement id="T004.4">
      Opening message instructions:
        - DS goes first: read lambda_function.py and data_contract.xml before answering.
          Cite specific function names and field names from the file, not from memory.
        - DE: read types.ts before specifying TypeScript interfaces.
        - RD: read DistributionTab.tsx before specifying chart constraints.
        - M2 pushback: if any agent cites a field without naming the file it came from,
          the next agent must ask for the exact path before treating it as ground truth.
        - Final turn must produce a structured contract block with:
            adv_drill JSON schema (exact field names, types, nesting)
            cla_timeseries JSON schema (including geo_drill)
            colorMap spec with actual portal token names or hex values
            TypeScript interface names (DE confirms)
            S3 key / output location for each
            NMNC/NMEC classification logic (agreed definition, not assumed)
    </requirement>

    <!-- ================================================================ -->
    <!-- ADVI-005 — Advisors tab stacked bar + 1Y rolling flows          -->
    <!-- Replaces ADVI-002 (superseded — see ADVI.json)                  -->
    <!-- ================================================================ -->
    <requirement id="T005.1">
      Create staging script: org/threads/staging/run-ADVI-005-stacked-bar-rolling-flows.sh
      Configuration:
        PROJECT="ADVI"
        THREAD_ID=""  (auto-assigned as ADVI-005)
        PARTICIPANTS="0.4.0_DS_ClientPlatform 0.4.0_DE_ClientPlatform 0.4.2_RD_AdvisorIntelligence"
        TURN_ORDER="round_robin"
        MODEL="gpt-5.2"
        MAX_TURNS_PER_AGENT=3
        TOOLS_ENABLED=true
    </requirement>
    <requirement id="T005.2">
      M1 context files to inject:
        data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py
        portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx
        portal/src/pages/AdvisorIntelligence/types.ts
        org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </requirement>
    <requirement id="T005.3">
      M4 inline briefing:
        "DS must read script 10 before answering. The critical open question is whether
        inflows and outflows are tracked as SEPARATE fields in the source parquet data,
        or whether only net NNA is available and inflows/outflows must be derived.
        The stacked bar chart requires inflows and outflows as distinct values per advisor
        per period. If only net NNA exists, DS must flag this as a data gap and propose
        a derivation approach — do not silently agree to produce a field that does not
        exist in source data. M2: push back on any answer that does not cite the
        specific parquet column or script line that produces inflows vs outflows."
    </requirement>
    <requirement id="T005.4">
      Opening message instructions:
        - DS goes first: read script 10 and data_contract.xml. Name specific variable
          and column names from the file, not from memory.
        - DE: read types.ts and AdvisorsTab.tsx before specifying interfaces.
        - RD: read AdvisorsTab.tsx before specifying chart constraints.
        - Final turn must produce a structured contract block with:
            stacked_bar JSON schema (exact period keys, per-advisor field names,
            inflow/outflow encoding with sign convention or separate fields)
            rolling_1y JSON schema (date format, per-advisor series structure)
            TypeScript interface names (DE confirms)
            Period key names (exactly: qtd/ytd/1y/3y/max or confirmed equivalents)
            Any data feasibility caveats DS needs to flag
    </requirement>

    <!-- ================================================================ -->
    <!-- ADVI-006 — Books tab design brief                                -->
    <!-- Replaces ADVI-003 (superseded — see ADVI.json)                  -->
    <!-- ================================================================ -->
    <requirement id="T006.1">
      Create staging script: org/threads/staging/run-ADVI-006-books-tab-design.sh
      Configuration:
        PROJECT="ADVI"
        THREAD_ID=""  (auto-assigned as ADVI-006)
        PARTICIPANTS="0.4.0_DS_ClientPlatform 0.4.2_RD_AdvisorIntelligence 0.4.0_DE_ClientPlatform"
        TURN_ORDER="round_robin"
        MODEL="gpt-5.2"
        MAX_TURNS_PER_AGENT=3
        TOOLS_ENABLED=true
    </requirement>
    <requirement id="T006.2">
      M1 context files to inject:
        infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py
        portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx
        portal/src/pages/AdvisorIntelligence/types.ts
        data/black_diamond/scripts/gold/03_build_holdings_lots.py
        data/black_diamond/scripts/gold/05b_build_account_performance.py
        data/black_diamond/scripts/gold/06_build_client_tax_liability.py
        org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </requirement>
    <requirement id="T006.3">
      M4 inline briefing:
        "This is a Books tab design alignment. The previous run (ADVI-003) failed to
        produce its required deliverable: docs/architecture/advisor_intelligence/books_tab_design_brief.md
        The DE must write this file as their final turn. It is not optional.
        DS: read lambda_function.py before describing what currently flows through the
        advisor-publisher. Anchor every answer to a function name and output dict key.
        Distinguish between what is currently in the published JSON vs what is gold-layer
        only. The gap list (what is missing from publisher output) is the core deliverable."
    </requirement>
    <requirement id="T006.4">
      Opening message instructions:
        - DS goes first: read advisor-publisher lambda_function.py, scripts 03/05b/06,
          and data_contract.xml. For each level (L2/L3/L4) describe: what is currently
          published, what exists in gold but is NOT in publisher output, and what does not
          exist anywhere yet.
        - RD: propose visual layout per level referencing specific portal panel primitives
          and data fields DS named. Do not propose fields that DS did not confirm exist.
        - DE final turn: write docs/architecture/advisor_intelligence/books_tab_design_brief.md
          covering L2/L3/L4 layout with data field mappings, DS gap list, component reuse
          opportunities, and TypeScript interface additions needed. This file must exist
          after the thread or the thread has failed.
    </requirement>

    <!-- ================================================================ -->
    <!-- ADVI-004 and ADVI-005 run immediately in parallel.              -->
    <!-- ADVI-006 runs after DS/DE/RD accumulate multiple session logs.  -->
    <!-- ================================================================ -->
    <requirement id="SEQ.1">
      Run order:
        1. Run ADVI-004 and ADVI-005 immediately in parallel — O3 is satisfied by enriched
           prompts and tools access. No waiting for new session logs.
        2. After ADVI-004 and ADVI-005 receipts land and DS/DE/RD have multiple current
           session logs: run ADVI-006 (Books — the most complex thread, benefits from richer
           accumulated context before running).
    </requirement>

    <!-- ================================================================ -->
    <!-- POST-RECEIPT: Task orders COO issues after each thread           -->
    <!-- ================================================================ -->
    <requirement id="TO.1">
      After ADVI-004 receipt: issue 3 task orders referencing the receipt path.
      Each must include thread_serial and thread_ref in XML metadata.
        0.4.0_DS_ClientPlatform/task_orders/ADVI-004-adv_drill_cla.md
          Streams: A1 (adv_drill), A2 (cla_timeseries)
          Implement per receipt contract. Update data_contract.xml before signaling DT.
        0.4.0_DE_ClientPlatform/task_orders/ADVI-004-portal_types_wiring.md
          Streams: types.ts additions (AdvDrillResponse, ClaTimeseriesResponse per receipt),
          endpoint wiring updates in advisor-intelligence.ts
        0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-004-distribution_continuous.md
          Streams: C2 (ADV continuous NNA), C4 (CLA continuous stacked area)
          Blocked by DT Stream B1 deploy. Reference receipt for field names.
    </requirement>
    <requirement id="TO.2">
      After ADVI-005 receipt: issue 2 task orders.
        0.4.0_DS_ClientPlatform/task_orders/ADVI-005-rolling_flows_data.md
          Stream: A3 (stacked_bar + rolling_1y in advisor_rolling_flows.json)
          Implement per receipt. Update data_contract.xml before signaling DT.
        0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-005-advisors_tab.md
          Stream: 4C (stacked bar primary + rolling line secondary)
          Blocked by DT Stream B2 deploy. Reference receipt for field names.
    </requirement>
    <requirement id="TO.3">
      After DS completes A1+A2 and A3 (commits + data_contract.xml updates):
      Issue DT task orders for deploy streams B1 and B2.
        0.4.0_DT_ClientPlatform/task_orders/ADVI-004-deploy_b1.md  (publisher: adv_drill + cla_timeseries)
        0.4.0_DT_ClientPlatform/task_orders/ADVI-005-deploy_b2.md  (script 10 EC2 deploy)
      These are not thread-derived (no alignment needed for deploy-only tasks),
      but use the ADVI-004/005 prefix to trace back to the stream that produced the code.
    </requirement>
    <requirement id="TO.4">
      After ADVI-006 receipt and design brief written:
        0.4.0_DS_ClientPlatform/task_orders/ADVI-006-books_data_contract.md
          Stream: E (audit advisor-publisher, close L4 gaps)
        0.4.0_DE_ClientPlatform/task_orders/ADVI-006-books_wiring.md
          Stream: G wiring + auth gating (blocked by F deploy)
        0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-006-books_layout.md
          Stream: G layout per design brief (blocked by F deploy)
        0.4.0_DT_ClientPlatform/task_orders/ADVI-006-deploy_f.md
          Stream: F (advisor-publisher L4 deploy, blocked by DS Stream E)
    </requirement>
    <requirement id="TO.5">
      AE task order (not thread-derived, issue when DS A5 investigation is complete):
        0.7.0_AE_CloudOps/task_orders/advi_firmid_auth.md
          Stream: J (firmId auth refactor — not blocking completion)
    </requirement>

    <!-- ================================================================ -->
    <!-- MONITORING                                                        -->
    <!-- ================================================================ -->
    <requirement id="MON.1">
      On every session start: read ADVI.json to check thread_counter and thread statuses.
      Read task order files for pending items. Check agent session logs for status signals.
      Update ADVI.json thread entries to "complete" after verifying receipts in agent
      threads/ folders. This is COO responsibility — not automated.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">ADVI-004 and ADVI-005 staging scripts created and executed immediately — no O3 wait required.</criterion>
    <criterion id="2">ADVI-004 and ADVI-005 staging scripts created and run; receipts in all participant threads/ folders.</criterion>
    <criterion id="3">ADVI-006 staging script created and run; docs/architecture/advisor_intelligence/books_tab_design_brief.md exists after thread completes.</criterion>
    <criterion id="4">Per-thread task orders issued for each post-receipt stream with thread_serial and thread_ref in XML metadata.</criterion>
    <criterion id="5">ADVI.json updated: ADVI-004/005/006 entries added with status "complete" after receipt verification.</criterion>
    <criterion id="6">No agent implements A1, A2, A3 before their respective ADVI-004/005 receipts are confirmed. GATE is non-negotiable.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>ADVI-001/002/003 are superseded. Do not reference their receipts as binding contracts. Old staging scripts are deleted.</constraint>
    <constraint>All staging scripts use PROJECT="ADVI", MODEL="gpt-5.2", THREAD_ID="" (auto-assigned). Never hardcode thread IDs for project threads.</constraint>
    <constraint>ADVI-004 and ADVI-005 run immediately in parallel — O3 is already satisfied. ADVI-006 runs only after DS, DE, and RD have multiple current session logs (the most complex thread; richer context improves output quality).</constraint>
    <constraint>The books_tab_design_brief.md is a required thread deliverable, not optional. If the thread completes without DE writing it, the thread has failed and must be re-run.</constraint>
    <constraint>Do not issue Stream G (Books implementation) task orders until the design brief file exists at docs/architecture/advisor_intelligence/books_tab_design_brief.md.</constraint>
    <constraint>Commit all task orders and ADVI.json updates using:
      git commit --author="2.0.0_SA_COO &lt;2.0.0_SA_COO@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advi_a4_bell_curve_verify + advi_a5_users_v2_mapping" status="pending" note="Immediate task orders active — no O3 gate on ADVI-004/005"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="advi_i2_leaderboard_sort" status="pending" note="Immediate task order active — no O3 gate on ADVI-004/005"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="advi_c1/c3/h/i" status="pending" note="Immediate task orders active — no O3 gate on ADVI-004/005"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">3 staging scripts (run-ADVI-004-*.sh, run-ADVI-005-*.sh, run-ADVI-006-*.sh)</deliverable>
    <deliverable type="document">ADVI.json updated: ADVI-004/005/006 entries added as threads complete</deliverable>
    <deliverable type="document">Per-thread task orders (10 files across DS/DE/RD/DT/AE) issued post-receipt</deliverable>
    <deliverable type="document">docs/architecture/advisor_intelligence/books_tab_design_brief.md (produced by DE in ADVI-006)</deliverable>
  </deliverables>
</task_order>
```
