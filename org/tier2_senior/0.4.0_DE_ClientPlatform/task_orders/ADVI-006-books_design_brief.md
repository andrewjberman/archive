# Task Order: ADVI-006 — Write Books Tab Design Brief

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-advi006-books-brief</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <thread_serial>ADVI-006</thread_serial>
    <thread_ref>org/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l/messages/</thread_ref>
  </metadata>

  <objective>
    ADVI-006 thread completed but your final turn (turn 9) was not generated — the orchestrator
    halted when DS and RD both signaled converge on turns 7 and 8, before you could write the
    design brief. All content is agreed and locked in your turn 6 scope summary (message 006.md).
    The open question you flagged (taxable-only holdings for v1?) was answered YES by DS in turn 7.
    Write docs/architecture/advisor_intelligence/books_tab_design_brief.md now.
  </objective>

  <references>
    <ref type="thread-turn">org/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l/messages/006.md</ref>
    <ref type="thread-turn">org/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l/messages/007.md</ref>
    <ref type="thread-turn">org/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l/messages/008.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <scope>
    <files>
      <file action="create">docs/architecture/advisor_intelligence/books_tab_design_brief.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Write docs/architecture/advisor_intelligence/books_tab_design_brief.md.
      Use your turn 6 message (006.md) as the template — all sections are already drafted there.
      Incorporate the following from DS turn 7 and RD turn 8:
        - Taxable-only is ACCEPTABLE for MVP (DS recommendation: explicit "Taxable Open Lots" label,
          non-taxable deferred to a follow-on stream).
        - RD MVP layout decisions from turn 8: access model (admin-only until advisorKey exists),
          L4 is inline drill inside L3 (no new route), "Taxable Open Lots" label binding, hide
          income_fees and portfolio_composition (not stubbed).
    </requirement>
    <requirement id="2">
      Brief must contain all 6 sections specified in the ADVI-006 thread opening message:
        1. L2 advisor book layout with field mappings (DS-confirmed fields only)
        2. L3 relationship view layout and field mappings
        3. L4 account + holdings (inline drill) with tax summary and lot drill-down
        4. Component reuse opportunities (Portal panel primitives, DataTable, etc.)
        5. DS data gaps: explicit list of what must be added to bd-portal-advisor-publisher
           before RD can implement each gap item (name function and publisher file)
        6. TypeScript interface additions needed (new types or extensions to existing types)
    </requirement>
    <requirement id="3">
      Backend gap list (Section 5) must be drawn from DS turn 7 exact citations:
        1. Advisor identity mapping: add advisorKey to opal-users-v2 USER#PROFILE matching
           _advisor_id() output. Required for any non-admin advisor access.
        2. Relationship performance timeseries: add to build_client_details() in
           bd-portal-advisor-publisher/lambda_function.py, sourcing from acct_r
           (gold/account_performance.parquet). Payload: AUA + cum_inflows + cum_outflows + nna.
        3. Account metadata enrichment: add to _build_accounts(), load gold/accounts_dimension_latest.parquet,
           add account_name, account_type, account_registration_type, qualified_flag.
        4. Positions list + weights: new positions[] section in build_client_details(),
           aggregated from lots_r, with weight computation.
        5. Non-taxable holdings: _build_tax() currently filters to taxable only.
           Expanding requires explicit scope decision + publisher change.
        6. Income/fees + portfolio taxonomy: hardcoded zeros/empty — hide until a real upstream
           source is published (do not stub UI).
    </requirement>
    <requirement id="4">
      Access model must be explicit: Books is admin/internal only (gated by isInternal() || isDev()
      in ClientsTab.tsx useAuth() check) until advisorKey identity mapping exists. No "advisor landing"
      UX in MVP.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">File exists at docs/architecture/advisor_intelligence/books_tab_design_brief.md.</criterion>
    <criterion id="2">All 6 required sections are present. No section is empty or placeholder.</criterion>
    <criterion id="3">L2/L3/L4 field mappings use only DS-confirmed publisher fields from the ADVI-006 thread. No phantom fields.</criterion>
    <criterion id="4">Backend gap list names the specific function (build_client_details, _build_accounts, etc.) for each gap item.</criterion>
    <criterion id="5">Access model documented: admin-only MVP, advisorKey blocker explicitly noted.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not invent fields that were not confirmed by DS in the ADVI-006 thread. The thread receipt is the only source of truth for field existence.</constraint>
    <constraint>Do not stub UI panels for income_fees or portfolio_composition — brief must say "hidden until non-zero data published."</constraint>
    <constraint>Commit the file to portal CLOUD repo (not portal DEV submodule — this is an architecture doc, not portal source).</constraint>
    <constraint>Commit using: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "docs(ADVI-006): books tab design brief L2/L3/L4 MVP"</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI-006-thread-turn-7" status="complete"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI-006-thread-turn-8" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">docs/architecture/advisor_intelligence/books_tab_design_brief.md</deliverable>
    <deliverable type="commit">CLOUD commit with the brief file</deliverable>
  </deliverables>
</task_order>
```
