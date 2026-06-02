<task_order>
<metadata>
  <to_id>MDPF_SCOPED.OPS1</to_id>
  <project>MDPF_SCOPED</project>
  <title>AE: unstick MDPF daily chain (stalled since 2026-05-29), fix auto-stop vs eclipse-wait timer conflict, add a staleness/heartbeat alarm, verify N clean weekday runs — closure gate</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>1.0.0_SA_CTO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCH-READY (AE offline at authoring — fabric wound down; action on next AE session or post-spawn)</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — closure gate for MDPF_SCOPED (Andrew-direct 2026-06-02: "assess MDPF is good to go on daily scheduling ... if scheduled adequately and organized in pattern, then we can close that, need AEs to go through it and review"). FE + data are Andrew-confirmed good; daily-scheduling health is the last open gate.</priority>
  <references>
    <ref type="runbook">data/mdpf/scripts/RUNBOOK_AE_mdpf_daily_chain.md</ref>
    <ref type="dispatch">infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh (Stage 0.5 eclipse wait, lines 195-241; MDPF_ECLIPSE_WAIT_SECS default 1800)</ref>
    <ref type="terraform">infra/aws/terraform/mdpf-pipeline/{eventbridge,alarms,ec2,lambdas}.tf</ref>
    <ref type="runner_instance">i-02448edb624a7a7cf (t3.medium, mdpf-daily-runner)</ref>
  </references>
</metadata>

<scope>
**Andrew wants MDPF_SCOPED closed once daily scheduling is adequate + organized + AE-reviewed. The architecture IS well-built, but the live pipeline is currently STALLED. This TO is the fix + verification that gates closure.**

## CTO assessment findings (read-only AWS evidence, 2026-06-02 ~13:15Z)

**The schedule architecture is good:** EventBridge rule `mdpf-daily-refresh-trigger` `cron(0 15 ? * MON-FRI *)` is ENABLED and FIRING reliably (TriggeredRules = 1/day Thu/Fri/Mon). DLQ + 3 CloudWatch alarms (DLQ-depth, chain-failed, stage5-ownts-failed) wired to the ops SNS topic. 5-stage idempotent DAG with a runbook. No complaint with the design.

**But the live pipeline has produced no fresh data since Friday 2026-05-29.** Root cause (fully resolved):

1. **The 2026-06-01 (Mon) scheduled run STALLED and was killed mid-wait.**
   - `s3://opal-data-mdpf/telemetry/mdpf-daily-runner/status.json`: run_id `mdpf_daily_20260601_150025`, run_date `2026-06-01`, **status "running"**, frozen at `updated_at 2026-06-01T15:01:23Z`, only 1/10 steps done (STAGE0-BRONZE), last_output `"Stage 0.5 wait-for-eclipse-gold sentinel"`.
   - Runner instance `i-02448edb624a7a7cf`: launched `2026-06-01T15:00:08Z`, **stopped `2026-06-01 15:16:18 GMT "User initiated"`** — i.e. ~16 min in, WHILE inside the Stage 0.5 eclipse wait.

2. **TIMER CONFLICT (proximate cause):** the Stage 0.5 eclipse-gold wait is bounded at **1800s (30m)** and is non-fatal (on timeout it proceeds; WS-C roll-forward absorbs a missing eclipse vintage). That design is correct in isolation — BUT an **auto-stop fires on the runner at ~15-16 min**, SHORTER than the 30m wait. So precisely when the eclipse sentinel is absent (when the full 30m wait is exercised), the auto-stop guillotines the instance before the non-fatal-proceed can run Stages 1-5. The chain can never complete on any day the eclipse sentinel is late/absent. (Phase note references an MDPF-runner auto-stop that AE previously root-caused/fixed for a backfill — this is the same auto-stop, now in conflict with the eclipse wait.)

3. **UPSTREAM eclipse/Inflection gold is itself stale since 5/29.** `s3://opal-data-inf/gold/eclipse/2026-06-01/_meta/gold_complete.json` is ABSENT; eclipse gold's latest date is `2026-05-29`. So even a clean MDPF run today only gets a roll-forward (1-day-stale inflection), not fresh 6/1 inflection data. The Inflection/eclipse pipeline not producing 6/1 is a separate upstream gap to confirm/coordinate.

4. **MONITORING GAP:** all 3 alarms read OK throughout this stall, because a HUNG/killed run never emits `ChainFailed=1` and `treat_missing_data=notBreaching`. The alarms catch hard failures + DLQ, but NOT a no-complete / staleness. A run that starts, hangs, and gets stopped is invisible. There is no freshness/heartbeat alarm.

## Deliverables (Terraform-only for infra per CLAUDE.md Rule 7; S3-artifact model per Rule 12)

1. **Immediate unstick** — re-dispatch the daily chain for the missing date(s) (6/1, and 6/2 after today's 15:00Z fire if it also stalls). Verify clean completion to runbook acceptance: `aggregate_aua/{d}.json` reconciliation.overall=PASS, `aggregate_aua_timeseries.json` as_of_last advances, 4 OWNTS ticker artifacts fresh. Clear the frozen status.json.

2. **Resolve the auto-stop vs eclipse-wait timer conflict** (root fix). Options for AE judgment — pick and justify:
   (a) move the auto-stop to fire only AFTER chain completion (event-driven stop, not a fixed ~15m timer), or
   (b) shorten `MDPF_ECLIPSE_WAIT_SECS` to comfortably less than the auto-stop window, or
   (c) raise/disable the auto-stop window for the runner during the chain.
   Whichever — the instance must never be stopped while the chain is mid-run. Document the chosen timing relationship in the runbook.

3. **Add a STALENESS / heartbeat alarm** — close the monitoring gap. A daily-chain run that fires but does not COMPLETE (or `aggregate_aua_timeseries.json` as_of_last older than the last expected trading day by > N days) must alarm to the ops SNS topic. The current failure alarms cannot catch a hang. (e.g. emit a `ChainCompleted=1` heartbeat on clean finish + alarm on missing heartbeat after the scheduled window; or an S3-object-freshness alarm on the timeseries rollup.)

4. **Upstream eclipse staleness** — confirm whether the Inflection/eclipse gold pipeline is supposed to produce daily 6/1+ partitions; if yes, root-cause its 5/29 staleness (or route to the INF/eclipse owner). MDPF's roll-forward masks this; surface it so it isn't silently 1-day-stale forever.

## Acceptance (the closure gate)

- [ ] AC1 — Chain re-dispatched; `aggregate_aua_timeseries.json` as_of_last == latest expected trading day; partitions present for every recent weekday; reconciliation.overall=PASS; 4 OWNTS tickers fresh.
- [ ] AC2 — Timer conflict fixed; instance demonstrably not stopped mid-run; chosen timing documented in runbook.
- [ ] AC3 — Staleness/heartbeat alarm deployed via Terraform, tested to fire on a no-complete, routes ops SNS.
- [ ] AC4 — **≥ 2 consecutive scheduled weekday runs complete clean end-to-end with fresh data** (the real proof it's "scheduled adequately"). No manual dispatch in those runs.
- [ ] AC5 — Eclipse upstream staleness characterized (fixed or formally accepted as roll-forward-by-design with the gap documented).
- [ ] AC6 — `comp-validate` / runbook acceptance green; RAVC2 evidence package to ws CTO + COO for the closure decision.

**Closure of MDPF_SCOPED is gated on AC1-AC6.** Until then the project stays REOPENED/active.
</scope>

<notes>
FE + data layer are Andrew-confirmed good (recharts v3 stacked-order fix caebae0d + Model Portfolios FE cascade, Andrew-confirmed; D1/D2/D3 from the 2026-05-29 reopen resolved). This TO is purely the daily-scheduling-health gate. CTO authored it as a FIX-class item under /ws-charter autonomous authority off an Andrew-direct assessment request; dispatch-ready, action when AE is live.
</notes>
</task_order>
