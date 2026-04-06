# EC2 Auto-Shutdown Audit — All Instances

<task_order>
  <issuer>2.0.0_SA_COO</issuer>
  <issued>2026-04-02</issued>
  <agent>0.7.0_AE_CloudOps</agent>
  <status>complete</status>
  <priority>normal</priority>
  <source>CTO directive (ad-hoc operational hygiene, no PRD)</source>
</task_order>

## Context

GLDRST.015 deployed a watchdog-shutdown systemd service for bd-gold-layer-runner.
CTO wants a comprehensive audit of ALL EC2 instances for shutdown behavior. You
own the infrastructure layer — this is a cross-instance inventory.

## Scope

Audit every EC2 service in `infra/aws/ec2/EC2_MANIFEST.json` (9 services as of
2026-04-02). For each instance, determine:

1. **Instance lifecycle** — persistent (always-on) vs ephemeral (launched per job)?
2. **Run scripts** — what scripts execute on this instance? (SSM documents, cron,
   systemd timers, user-data, manual SSM send-command)
3. **Shutdown behavior** — after each script completes, does the instance shut down?
   What mechanism? (explicit `shutdown` in script, watchdog timer, EventBridge
   stop-instance, user-data shutdown, none)
4. **Systemd timers** — any existing timers? What do they do?

### Specific instances to cover

| Instance | Notes |
|---|---|
| `moltbot` | Persistent AI agent — likely always-on by design. Confirm. |
| `smartx-exporter` | Has autostart Lambda. Does it auto-stop? |
| `seeking-alpha-scraper` | Persistent. Running schedule? |
| `bd-gold-layer-runner` | GLDRST.015 watchdog COMPLETE. Confirm current state. |
| `bd-exporter` | Silver merge-daily-incremental. Shutdown on completion? |
| `bd-allocations` | SSM-triggered daily at 21:48 UTC. Stays running? |
| `bd-transactions` | SSM-triggered daily at 21:40 UTC. Stays running? |
| `bd-price-runner` | Runs on bd-allocations instance. Part of allocation SSM sequence. |
| `bd-gold-detail-generator` | Ephemeral (user-data baked). Verify shutdown in user-data.sh. |

## Deliverable

A markdown file in your `logs/2026-04-02/` folder with a table:

| Instance | Lifecycle | Run Scripts | Shutdown Mechanism | Systemd Timers | Gap? |
|---|---|---|---|---|---|

For each gap (instance stays running unnecessarily after work completes),
note estimated monthly billing impact if known. Do NOT remediate — audit only.
Remediation TOs will follow if gaps are found.

## Acceptance Criteria

- [ ] All 9 EC2_MANIFEST services covered
- [ ] Each instance's shutdown mechanism (or lack thereof) documented
- [ ] Gaps clearly identified with instance name
- [ ] bd-gold-layer-runner confirmed as baseline (GLDRST.015 watchdog active)
