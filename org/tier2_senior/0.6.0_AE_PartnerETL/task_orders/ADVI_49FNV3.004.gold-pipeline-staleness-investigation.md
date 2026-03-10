<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
  </metadata>

  <objective>
    Investigate why opal-data-bd/gold/timeseries_chart.json has a last data date of 2026-03-02
    despite the bronze/silver/gold pipeline being configured to run daily. The publisher Lambda
    (bd-portal-publisher) was last triggered on 2026-03-06. Determine why 8 days of data are
    missing, whether the pipeline is failing silently, and fix the root cause so the gold layer
    stays current.
  </objective>

  <scope>
    <files>
      <file action="investigate">opal-data-bd/gold/pipeline-complete.json (trigger file)</file>
      <file action="investigate">opal-data-bd/gold/timeseries_chart.json (last data date 2026-03-02)</file>
      <file action="investigate">EC2 bd-gold-layer-runner logs and cron schedule</file>
      <file action="investigate">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Determine the last successful run of the bronze/silver/gold pipeline on
      EC2 (bd-gold-layer-runner). Check CloudWatch logs, S3 timestamps on gold/ parquet files,
      and the pipeline-complete.json trigger file timestamp.</requirement>
    <requirement id="2">Determine why the pipeline has not produced data past 2026-03-02. Possible
      causes: cron not running, bronze feed stale (Schwab/BD data not arriving), silver transform
      failing, gold scripts failing, pipeline-complete.json not being written.</requirement>
    <requirement id="3">Check if the bronze feed (raw Schwab/BD data) has been arriving daily.
      If the upstream data feed stopped, identify when and why.</requirement>
    <requirement id="4">Check if the gold pipeline ran but failed after 2026-03-02. Look for
      error logs, partial outputs, or the pipeline hanging.</requirement>
    <requirement id="5">Once root cause is identified, fix or escalate. If it's a cron/scheduling
      issue, fix the cron. If it's a data feed issue, document and escalate to Andrew. If it's a
      script failure, identify the failing script and fix it.</requirement>
    <requirement id="6">After fix, verify the pipeline runs successfully and
      timeseries_chart.json gets a current last data date.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Root cause documented: what broke, when it broke, why it was silent.</criterion>
    <criterion id="2">Pipeline running daily again with current data dates.</criterion>
    <criterion id="3">Session log with full investigation trail and fix applied.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify the bd-portal-publisher Lambda logic — this is an infrastructure
      and scheduling investigation, not a code change to the publisher.</constraint>
    <constraint>Follow EC2 deployment protocol if any script changes are needed on EC2.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="document">Session log with root cause analysis and fix verification.</deliverable>
  </deliverables>
</task_order>
