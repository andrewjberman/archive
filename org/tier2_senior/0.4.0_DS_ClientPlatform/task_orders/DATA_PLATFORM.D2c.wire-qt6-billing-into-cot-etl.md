<to_id>DATA_PLATFORM.D2c</to_id>
<project>DATA_PLATFORM</project>
<title>D2c wire qt6 "BI Billing" into cot_bronze_ingest.py as a 6th ingested table -- closes the Cottonwood Books fee_earning_aua/implied_revenue=0 gap</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS-lead; owns cot_bronze_ingest.py's bronze layer)</assigned_to>
<consult>Andrew (DATEMODE coordination -- cot_bronze_ingest.py is the DATEMODE-HELD file, his PRD thread); 0.7.0_AE_CloudOps (deploy)</consult>
<verify>3.0.0_SA_CVO (verify the 6th table lands + reconciles against the qt6 fee-probe finding)</verify>
<issued_by>PROPOSED by 0.4.0_DS_ClientPlatform (COO-directed 2026-07-08, following the D2b/D2c fee-resolution finding); PENDING 2.0.0_SA_COO issue+register AFTER Andrew DATEMODE coordination</issued_by>
<issued_date>2026-07-08</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: proposed-not-built</status>
<!-- SCOPE ONLY per COO 2026-07-08 GO: "SCOPE it as a proposed TO but do NOT build yet; it touches cot_bronze_ingest.py which is the DATEMODE-HELD file (Andrew's PRD), so it needs coordination -- I'll sequence D2c after I confirm the DATEMODE-coordination with Andrew." DO NOT implement against this TO until COO flips status to active/issued. -->

<objective>
Wire BD DataMining queryTypeId=6 ("BI Billing" -- the real management-fee CHARGE query type, see data/black_diamond/API/domains/datamining/QUERY_TYPES.md + findings/2026-07-08_mgmt_fee_resolution.md) into cot_bronze_ingest.py as a 6th ingested table, so posted fee charges flow into cot bronze/silver/gold and close the Cottonwood Books tab's fee_earning_aua/implied_revenue/distribution=0 gap.
</objective>

<the_work>
- ADD a 6th table entry to cot_bronze_ingest.py's TABLE_QUERY_TYPE / TABLE_DATE_MODE dicts (queryTypeId=6, table name TBD e.g. "billing"; grain is Account x Month, NOT a snapshot -- date-mode choice needs care, likely Custom with a lookback wide enough to catch a quarterly cycle, mirroring the realized/transactions 14d-restatement-window pattern but probably wider given quarterly billing).
- PROVISION a persisted qt6 template selecting the Fees measure (id 55, mappedColumn biFees) + identifying dims (AccountID/Account Number/Account Name) + Date-level dims (Return Date/Month/Year) -- the DS probe template (templateId 242684, data/black_diamond/API/domains/datamining/endpoints/payloads/qt6_fee_probe_full_trace.md) is the proven-working seed; re-provision or reuse per the standard cot_bronze_ingest persisted-template pattern (Andrew 2026-06-09 convention: scheduled runs tap a persisted template by id, no create-per-call).
- LAND to forwardfill_v2/{table}/ following the existing 5-table pattern -- the silver engine (merge-daily-incremental.py) should pick it up with ZERO code change if silver column == to_snake_case(BD mappedColumn), per the existing D2/cot_bronze_ingest architecture.
- CONFIRM the billing CYCLE handling: qt6 rows are Account x Month with mostly-zero Fees except in the actual billing month -- decide whether silver/gold should store all rows (sparse) or filter to nonzero (Silver = dedup+dtype only per Rule 17, NO business-row-filtering -- so silver keeps sparse rows; gold decides what's useful).
- WIRE the new fee data into the Cottonwood Books gold computation (fee_earning_aua/implied_revenue/distribution) -- the actual consumer-side fix that closes the visible gap. Scope this as its own gold-layer sub-task once bronze/silver land.
</the_work>

<acceptance_criteria>
1. qt6 added as cot_bronze_ingest.py's 6th table, DATEMODE-coordinated with Andrew's PRD thread (this TO does not proceed to build until COO confirms that coordination).
2. A persisted qt6 template (Fees + identifying dims) provisioned + proven via a scheduled-pattern dry run.
3. Bronze lands to forwardfill_v2/billing/ (or agreed table name); silver picks it up per the existing zero-code-change pattern (Rule 17 -- dedup+dtype only, no field slimming).
4. Cottonwood Books tab fee_earning_aua/implied_revenue/distribution reflect real qt6 data (the actual consumer fix -- may be a separate follow-on gold TO if scoped that way).
5. CVO verifies the 6th table's served output reconciles against the $1,006,622.12/618-account finding (findings/2026-07-08_mgmt_fee_resolution.md) for the same window.
6. RAVC2 COO + Andrew (DATEMODE thread) before any build work starts.
</acceptance_criteria>
