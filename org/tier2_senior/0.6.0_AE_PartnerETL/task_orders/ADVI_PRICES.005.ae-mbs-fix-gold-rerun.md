# Task Order: ADVI_PRICES.005 — 05e Gap Diagnostic on Existing Data

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-05e-diagnostic</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <!-- Completed 2026-03-27. AE ran silver rebuild + 05e validation. Gap reduced from 3.72% to 0.169%. See logs/2026-03-27/advi_prices_005_mbs_fix_silver_rebuild.md -->
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    Run the new 05e_decompose_aua_gap.py diagnostic against EXISTING gold and silver
    artifacts to quantify the AUA gap decomposition. 05e is read-only — no data rebuild
    needed. It will show the $107M MBS root cause and gross over/under breakdown.
  </objective>

  <requirements>
    <requirement id="1">
      Wait for DT to push e494e2be (enhanced 05e with gross breakdown) to origin.
      Then sync gold scripts to S3:
        aws s3 sync data/black_diamond/scripts/gold/ s3://opal-data-bd/code/gold/ --delete
      Only the new 05e file matters. Stash uncommitted GLDRST P3 changes first if present.
    </requirement>

    <requirement id="2">
      On EC2, pull updated scripts and run:
        cd /home/ubuntu/gold-layer/scripts
        aws s3 sync s3://opal-data-bd/code/gold/ .
        python 05e_decompose_aua_gap.py

      Record full output: aggregate gap %, per-tier breakdown, gross overvaluation,
      gross undervaluation, worst offenders by position.
    </requirement>

    <requirement id="3">
      Report results to COO and DS:

      send_message(from="0.6.0_AE_PartnerETL", to="2.0.0_SA_COO",
        subject="PRICES.005 -- 05e gap decomposition results",
        body="05e output: {full results}")

      send_message(from="0.6.0_AE_PartnerETL", to="0.4.0_DS_ClientPlatform",
        subject="05e gap decomposition on existing data",
        body="05e output: {full results}")
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">05e runs successfully against existing artifacts</criterion>
    <criterion id="2">Gap decomposition output shows MBS contribution</criterion>
    <criterion id="3">COO and DS notified with full output</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>NO silver rebuild. NO gold rerun. 05e is read-only.</constraint>
    <constraint>Stash uncommitted GLDRST P3 changes before any S3 sync.</constraint>
    <constraint>Execute autonomously. Do NOT wait for human input.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="push-e494e2be" status="pending">
      Enhanced 05e commit needs to be on origin before S3 sync
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="artifact">05e gap decomposition output</deliverable>
    <deliverable type="message">Results sent to COO and DS</deliverable>
  </deliverables>
</task_order>
