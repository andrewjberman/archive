<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-005-dt-schwab-bucket-design</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>investigation</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Audit the current Schwab bucket permissions and routing complexity, then design a
    streamlined structure that allows the BD gold pipeline to directly use Schwab RPS
    files for cross-validation without staging workarounds.

    This is an INVESTIGATION + DESIGN task. You produce a recommendation document.
    AE (0.7.0_AE_CloudOps) implements the bucket policy / Terraform changes based on
    your design. Do not attempt to modify bucket policies yourself.
  </objective>

  <background>
    The ADHC_HISTRY project is using Schwab RPS files (daily position snapshots) to
    cross-validate against BD's unrealized/realized tables and definitively reconcile
    positions. The current routing is unnecessarily complex because of over-restrictive
    permissions on `opal-data-schwab`:

    CONFIRMED (from live investigation 2026-04-01):
    - opal-data-schwab has an explicit DENY on ALL writes at the bucket level -- affects
      everyone including EC2. The bucket policy protects the authoritative ingestion path.
    - As a result, the converter (convert_schwab_rps_to_parquet.py) cannot write back
      to opal-data-schwab/02_anonymized/ even though the design assumed it could.
    - Current workaround: Schwab RPS CSVs were staged to opal-data-bd/uploads/schwab/
      and converter was patched to read from there instead.
    - silver/RPS/ (in opal-data-bd) IS writable -- 534 partitions built there successfully.
    - The gold scripts (02/03) now read from silver/RPS/ for injection logic.

    PROBLEM: The workaround works but the routing is fragile -- it patches around the
    bucket policy rather than designing the right structure. For ongoing Schwab ingestion
    (daily RPS feed) and future cross-validation workflows, the routing must be coherent.
  </background>

  <requirements>

    <requirement id="1">
      AUDIT: Read the current opal-data-schwab bucket policy.
      ```bash
      aws s3api get-bucket-policy --bucket opal-data-schwab --output text | python3 -m json.tool
      ```
      Document:
      - What prefixes are write-protected and why
      - What principals are allowed/denied for each prefix
      - Whether there is a legitimate reason to keep writes locked on 01_raw/ (authoritative ingestion)
      - Whether 02_anonymized/ or any other prefix could be made writable for EC2
    </requirement>

    <requirement id="2">
      AUDIT: Map the current end-to-end Schwab → BD gold routing.
      Trace the actual data flow as it exists today:
      - Who writes to opal-data-schwab/01_raw/ (what Lambda or ingestion process)
      - What convert_schwab_rps_to_parquet.py does and where it writes output
      - How silver/RPS/ in opal-data-bd is populated
      - How gold scripts 02/03 read from silver/RPS/ for injection

      Read the relevant scripts:
      - data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py
      - Any existing ingestion Lambda or SSM runbook for Schwab data

      Document the current flow as a step-by-step data lineage diagram in your report.
    </requirement>

    <requirement id="3">
      DESIGN: Propose a streamlined routing structure. The design must satisfy:

      a) Authoritative ingestion path (01_raw/) remains write-protected from EC2 and
         Lambda processing jobs -- only the designated ingestion mechanism can write there.

      b) A clean, writable "processing" prefix exists where EC2 gold jobs can:
         - Write intermediate converter output (parquet)
         - Read for gold cross-validation and injection

      c) No staging workarounds. The converter should write directly to the correct
         destination without patching or indirection through a foreign bucket
         (opal-data-bd/uploads/schwab/ is a workaround, not a design).

      d) The Schwab bucket structure should mirror the BD bucket structure where applicable:
         - bronze/ = raw ingest (write-protected, ingestion only)
         - silver/ = converted/normalized parquet (EC2 writable)
         - gold/ = cross-validated or enriched (EC2 writable, same as BD gold)

      Concrete proposal: which prefixes to add/modify on opal-data-schwab, what IAM
      principals get write access to which prefixes, and whether any changes to
      opal-data-bd/uploads/schwab/ are needed (deprecate? repurpose?).
    </requirement>

    <requirement id="4">
      DESIGN: For the ongoing daily Schwab ingestion pipeline (future AE task order):
      - The RPS files arrive daily. Where should they land (bucket/prefix)?
      - Who triggers ingestion -- existing Lambda, new Lambda, or manual SSM?
      - How does the gold pipeline know new RPS data is available?
        (S3 event trigger? EventBridge schedule? Manual flag?)
      Include a brief recommendation. This does NOT need to be fully designed --
      just enough for AE and CTO to evaluate the approach.
    </requirement>

    <requirement id="5">
      Produce a design document at:
      docs/architecture/ADHC_HISTRY_schwab_bucket_design.md

      Structure:
      ## Current State
      [Data lineage + bucket policy summary]

      ## Problems
      [Specific friction points with evidence]

      ## Proposed Design
      [New bucket structure, prefix map, IAM principal assignments]

      ## Migration Steps for AE
      [Ordered list of bucket policy changes + any bucket creation needed]

      ## Daily Ingestion Recommendation
      [Brief routing proposal for ongoing RPS feed]
    </requirement>

    <requirement id="6">
      Message COO (2.0.0_SA_COO) when the design document is written, with a
      2-3 sentence summary of the proposed change and any constraints you found
      (e.g. if 01_raw/ write protection is tied to compliance or Schwab agreement,
      flag that -- AE should not remove it without understanding why it exists).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-data-schwab bucket policy documented -- all deny/allow statements mapped.</criterion>
    <criterion id="2">Current data lineage documented -- Schwab CSV to gold cross-validation, end-to-end.</criterion>
    <criterion id="3">Proposed design specifies concrete prefix map + IAM principal assignments (no vague "use proper permissions").</criterion>
    <criterion id="4">Migration steps are AE-actionable -- specific aws s3api or Terraform changes.</criterion>
    <criterion id="5">Design document written to docs/architecture/ADHC_HISTRY_schwab_bucket_design.md.</criterion>
    <criterion id="6">COO messaged with summary.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DO NOT modify any bucket policies or IAM roles. Investigation and design only.</constraint>
    <constraint>DO NOT upload or move any Schwab files. Read-only audit of existing structure.</constraint>
    <constraint>If 01_raw/ write protection exists for a compliance or data-integrity reason, preserve it in the proposed design -- do not recommend removing it without flagging the reason.</constraint>
    <constraint>The design must keep silver/RPS/ in opal-data-bd as the interface for gold scripts -- those scripts are already wired and working. The question is how upstream routing gets cleaner, not rewiring gold.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_HISTRY.002" status="complete">
      DS Phase 2 injection scripts committed (2666dc1f). silver/RPS/ → gold interface is established.
      DT audits the upstream routing without changing the gold interface.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">docs/architecture/ADHC_HISTRY_schwab_bucket_design.md</deliverable>
    <deliverable type="message">COO summary message with proposed design and any compliance flags</deliverable>
  </deliverables>
</task_order>
