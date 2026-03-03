This is a Pattern 0 pre-implementation alignment thread for the Books tab (Stream D) of the AdvisorIntelligence completion PRD.

The Books tab has four levels:
  L2: Advisor book (all of this advisor's relationships — default landing for non-admin users)
  L3: Relationship/client view (one client's full detail)
  L4: Account + holdings + lots + performance + tax (deepest view, with lot-level drill-down)

Knowledge source: 0.4.0_DS_ClientPlatform — describes WHAT data currently flows out of the advisor-publisher Lambda and what L4 data exists in the gold layer (scripts 03, 05b, 06) but is NOT yet published. DS must surface the gap between what is available in gold vs what is currently in the S3 publisher output.

Layout proposer: 0.4.2_RD_AdvisorIntelligence — proposes the visual layout for each level (L2/L3/L4), identifies component reuse opportunities, flags any layout constraint that affects what fields DS needs to add to the publisher.

Wiring specifier: 0.4.0_DE_ClientPlatform — reviews DS's gap list and RD's layout, identifies TypeScript interface additions needed, confirms component reuse opportunities, and flags any API endpoint changes required.

Deliverable: a markdown design brief at docs/architecture/advisor_intelligence/books_tab_design_brief.md covering:
  1. L2 advisor book layout (sections with data field mappings)
  2. L3 relationship view layout
  3. L4 account + holdings view with tax summary and lot drill-down
  4. Component reuse opportunities
  5. Publisher data gaps DS must close before RD implements
The final agent turn (DE) must write the design brief path and a structured summary of what changed in the agreed contract.
