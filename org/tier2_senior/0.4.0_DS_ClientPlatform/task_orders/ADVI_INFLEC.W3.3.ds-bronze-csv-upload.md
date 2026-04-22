<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w3.3-bronze-upload</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <completed>2026-04-22</completed>
    <completed_by>0.4.0_DS_ClientPlatform~A</completed_by>
    <evidence>22 CSVs in s3://opal-data-inf/bronze/orion/2026-04-21/ (18 TRN incl duplicates, 2 AUM, 1 SlickGrid). Q2 2024 absent — gap_manifest.json status=open (was closed 2026-04-22 per COO action per ~C log).</evidence>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Upload Inflection Orion CSV exports (provided by Andrew from `C:\Users\AndrewBerman\Downloads\infl_raws\`) to `s3://opal-data-inf/bronze/orion/{YYYY-MM-DD}/` per Phase 1 manual bootstrap. This unblocks the first silver run. Blocked on W0.1 (Andrew Q2 2024 re-download + any prior CSVs available).
  </objective>

  <context>PRD §5.3 Phase 1. Andrew has manually downloaded Inflection CSVs historically. Until `inf-exporter` is live (W2.8), all bronze ingestion is manual. DS coordinates with Andrew to identify the full set of available CSV files, uploads them to the correct S3 prefix, verifies row counts match source.</context>

  <compiler_tools_mandate>
    Phase 3:
    <run>aws s3 ls s3://opal-data-inf/bronze/orion/ --recursive | head -30</run>
    <expect>TRN, AUM, accounts CSVs present for available date range. Q2 2024 window absent or partial (per W0.1 status).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W0.1 (Andrew Q2 2024 re-download). At minimum, upload whatever CSVs are currently available to unblock W3.4 first silver run. Q2 2024 backfill lands as a second upload when Andrew has the data."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All available Orion CSVs uploaded to `bronze/orion/{YYYY-MM-DD}/` per date.
    2. S3 ls shows files present; row count logged per file.
    3. Q2 2024 status documented: absent (waiting W0.1), or partial if some available.
    4. Session log with upload manifest + S3 ls output.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">s3://opal-data-inf/bronze/orion/ (data-only S3 write)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Coordinate with Andrew for CSV source files.</requirement>
    <requirement id="2">Upload path: `bronze/orion/{YYYY-MM-DD}/{filename}.csv` — date from file metadata.</requirement>
    <requirement id="3">No code changes — data upload only.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with upload manifest.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT invent CSV row structure — upload as-is from Andrew's source files.</rule>
  </do_not>
</task_order>
