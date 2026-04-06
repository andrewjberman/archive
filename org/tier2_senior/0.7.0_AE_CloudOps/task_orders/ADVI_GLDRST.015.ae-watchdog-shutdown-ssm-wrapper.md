<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-02-gldrst-015-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-02</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Implement a watchdog shutdown safety net and an SSM nohup wrapper for
    the bd-gold-layer-runner EC2 instance. This prevents idle instances
    from running indefinitely when SSM kills the gold rebuild process tree
    after its 7200s timeout.
  </objective>

  <context>
    When gold rebuilds are triggered via SSM send-command, the `tee` pipe
    pattern in `run_gold_layer.sh` (line 62: `exec > >(tee /tmp/gold_runner.log) 2>&1`)
    ties the process tree to the SSM agent. SSM has a 7200s executionTimeout.
    Full rebuilds take longer. When the timeout hits, SSM kills the entire
    process group, preventing `run_gold_layer.sh` from reaching its
    `shutdown -h now`. The instance is left running idle (observed: 15+ hours
    on 2026-04-02).

    The automated path (Lambda `bd-gold-trigger` -> EC2 start -> systemd
    `run-gold-layer.sh`) is unaffected. But manual SSM runs by AE are common
    during development, debugging, and recovery.

    PRD: docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md (Work Stream A)
  </context>

  <scope>
    <files>
      <file action="create">infra/aws/ec2/bd-gold-layer-runner/watchdog-shutdown.sh</file>
      <file action="create">infra/aws/ec2/bd-gold-layer-runner/watchdog-shutdown.service</file>
      <file action="create">infra/aws/ec2/bd-gold-layer-runner/watchdog-shutdown.timer</file>
      <file action="create">data/black_diamond/scripts/gold/ssm-run-gold.sh</file>
      <file action="modify">infra/aws/ec2/bd-gold-layer-runner/setup-instance.sh</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create a watchdog shutdown script (`watchdog-shutdown.sh`) that checks:
      - No `run_gold_layer.sh` or `python3` process is running
      - Instance has been up for > 30 minutes (`uptime -s` comparison)
      - No `/tmp/GOLD_KEEP_ALIVE` marker file exists
      If all three conditions met: `shutdown -h now`
      Log each check cycle to `/var/log/watchdog-shutdown.log` (plain ASCII, no emojis).
    </requirement>

    <requirement id="2">
      Create a systemd timer (`watchdog-shutdown.timer`) that runs the watchdog
      every 5 minutes. The corresponding service unit (`watchdog-shutdown.service`)
      calls the watchdog script. Enable the timer in `setup-instance.sh`.
    </requirement>

    <requirement id="3">
      Create `ssm-run-gold.sh` wrapper script:
      ```bash
      #!/bin/bash
      nohup ./run_gold_layer.sh "$@" > /tmp/gold_runner.log 2>&1 &
      echo "PID: $!"
      echo "Log: /tmp/gold_runner.log"
      echo "Instance will self-stop on completion."
      ```
      This detaches from SSM immediately, making the timeout irrelevant.
    </requirement>

    <requirement id="4">
      Upload all new/modified files to S3 via the standard EC2 deployment path
      (`safe-ec2-deploy.sh`). Verify the watchdog timer is active on the gold
      runner instance after deploy.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">watchdog-shutdown.timer active on bd-gold-layer-runner</criterion>
    <criterion id="2">watchdog successfully shuts down idle instance in test (start instance, wait 30+ min with no gold process, confirm shutdown)</criterion>
    <criterion id="3">ssm-run-gold.sh detaches correctly -- SSM command returns immediately with PID</criterion>
    <criterion id="4">GOLD_KEEP_ALIVE marker prevents shutdown when present</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify run_gold_layer.sh itself -- the watchdog is a safety net, not a replacement for the existing shutdown logic</constraint>
    <constraint>All logging must use plain ASCII (no emojis) per CLAUDE.md Rule 13</constraint>
    <constraint>Deploy via safe-ec2-deploy.sh per EC2 deployment protocol</constraint>
  </constraints>

  <dependencies>
    None -- this is independent of the S3 restructure TOs.
  </dependencies>

  <deliverables>
    <deliverable type="commit">watchdog-shutdown.sh + systemd units + ssm-run-gold.sh</deliverable>
    <deliverable type="deploy">Watchdog timer active on bd-gold-layer-runner via safe-ec2-deploy.sh</deliverable>
    <deliverable type="log">Session log with test evidence</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md</ref>
    <ref type="source">infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh</ref>
  </references>
</task_order>
