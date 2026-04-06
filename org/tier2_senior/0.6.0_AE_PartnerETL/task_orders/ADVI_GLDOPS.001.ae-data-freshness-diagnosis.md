# ADVI_GLDOPS.001 — AE: Data Freshness Diagnosis

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-03-gldops-001-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-03</date>
    <status>complete</status>
    <!-- Completed 2026-04-06. AE delivered diagnosis via MCP: EC2 running but idle since 04-02, pending marker exists, 4 days missed (Apr 3-6), silver missing since 04-02. Scripts 05+12 uploaded to S3. -->
    <priority>P0</priority>
    <project_code>ADVI_GLDOPS</project_code>
  </metadata>

  <objective>
    Diagnose the current state of bd-gold-layer-runner and determine why April 1+
    data is missing from the portal. The daily gold incremental has not run since
    the full rebuild (PID 39671) started. Report findings so DS can code the fix
    and we can trigger a catch-up incremental.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_GLDOPS_PRD.md</ref>
  </references>

  <context>
    The bd-gold-layer-runner EC2 (i-01003b035d2988dfb) was running a full rebuild
    (PID 39671). The daily gold trigger Lambda (bd-gold-trigger) sees "running"
    instance and writes a pending marker to S3 instead of starting a new run.
    The EC2 runner's pending marker check is disabled (lines 88-115 of
    infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh). The gold scripts runner
    (data/black_diamond/scripts/gold/run_gold_layer.sh) HAS an active pending check
    at lines 256-274, but only runs after the current gold run completes.

    You uploaded scripts 02+03 (91d2342f phantom fix) to S3 on 04-02 11:36 ET.
    Those are already on the EC2 for the next run.
  </context>

  <deliverables>
    Run these checks and report findings to COO via send_message:

    1. **EC2 instance state**: Is bd-gold-layer-runner running or stopped?
       ```
       aws ec2 describe-instances --instance-ids i-01003b035d2988dfb \
         --query 'Reservations[0].Instances[0].State.Name' --output text
       ```

    2. **If running**: Is PID 39671 still alive? Check via SSM:
       ```
       aws ssm send-command --instance-ids i-01003b035d2988dfb \
         --document-name AWS-RunShellScript \
         --parameters 'commands=["ps aux | grep -E \"run_gold|python3\" | grep -v grep; echo EXIT:$?"]' \
         --output text
       ```

    3. **Latest gold data date**: Check the most recent data in gold/:
       ```
       aws s3 ls s3://opal-data-bd/gold/client_performance/ --recursive | sort | tail -5
       ```

    4. **Pending marker**: Does trigger-pending.json exist?
       ```
       aws s3 cp s3://opal-data-bd/gold/trigger-pending.json - 2>/dev/null || echo "NO MARKER"
       ```

    5. **Silver pipeline April 2**: Did the silver pipeline produce April 2 data?
       ```
       aws s3 ls s3://opal-data-bd/silver/prices/ | grep "2026-04-02"
       ```

    6. **Gold run logs**: Check latest gold run logs:
       ```
       aws s3 ls s3://opal-data-bd/logs/gold-layer/ | sort | tail -5
       ```

    Report: instance state, PID status, latest gold date, pending marker status,
    silver April 2 status, latest log timestamps. COO will use this to authorize
    the manual incremental trigger.
  </deliverables>

  <dependencies>
    None -- this is the first task in the chain.
  </dependencies>
</task_order>
