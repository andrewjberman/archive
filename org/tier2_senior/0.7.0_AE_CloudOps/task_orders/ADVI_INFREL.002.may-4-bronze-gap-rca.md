<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.002</id>
    <project>ADVI_INFREL</project>
    <title>May 4 Inflection bronze gap RCA + remediation (parallel; non-blocking)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Authored sprint mode 2026-05-05T~21:15Z post PRD ADVI_INFREL v0.1 ship; flipped staged→pending 20260506T133122Z by COO session 59 post-D4 dispatch. Parallel non-blocking — does NOT gate on TO-1. AE 0.7 LEAD. -->
    <priority>high</priority>
    <estimated_effort>~0.25d investigation + ~0.25d remediation if root-cause is fixable</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.2 + §6 TO-2</ref>
    <ref type="evidence_baseline">`bronze/orion-api-v2/2026-05-04/` is MISSING despite cron `opal-inf-bronze-runner-cron` enabled (12:43 UTC); 2026-05-04 is Monday (weekday), warrants investigation</ref>
    <ref type="weekend_baseline">2026-05-02 (Sat) + 2026-05-03 (Sun) plausibly Orion API unavailable (no investigation done); weekend gaps not in scope of this TO unless RCA shows runner-side cause</ref>
  </references>

  <context>
    Cron `opal-inf-bronze-runner-cron` runs daily 12:43 UTC and dispatches SSM command to inf-bronze-runner EC2 to run orchestrator.py (multi-dim daily pull). For 2026-05-04 (Monday), bronze partition is missing.

    Three competing root-cause classifications:
    - **(a) Lambda cron didn't fire** — EventBridge rule misconfigured, OR Lambda errored before SSM dispatch.
    - **(b) Lambda fired but SSM didn't dispatch** — IAM gap, instance state (stopped), or SSM agent unhealthy.
    - **(c) SSM dispatched but orchestrator.py failed mid-run** — Orion API outage, JWT expiry, instance resource gap, or script bug.

    Cross-reference TO-1: if TO-1 RCA shows orchestrator chain doesn't flag completion correctly (`_BRONZE_COMPLETE.json` not written), May 4 bronze MAY have actually succeeded but failed to flag. Empirical: check `aws s3 ls s3://opal-data-inf/bronze/orion-api-v2/2026-05-04/` for ANY data including non-sentinel files. If empty, runner truly didn't write.
  </context>

  <phase id="0" when="Phase 0 RCA — investigation only">
    <step>
      <run>CloudWatch logs `opal-inf-bronze-runner-cron` Lambda — 2026-05-04 invocation. Did it fire? StartTime + EndTime + ExitCode + LogStream contents.</run>
      <expect>Empirical answer to class (a). If no invocation logged: EventBridge rule misconfigured. If invocation errored: error message.</expect>
      <if_mismatch>If CloudWatch retention &lt;30d and 2026-05-04 logs are gone: surface gap to me; consider extending retention.</if_mismatch>
    </step>
    <step>
      <run>EC2 `inf-bronze-runner` SSM command history 2026-05-04 — did command run? `aws ssm list-command-invocations --instance-id <runner> --start-time-after 2026-05-04T00:00:00Z --start-time-before 2026-05-05T00:00:00Z`. Get exit code + output.</run>
      <expect>Empirical answer to class (b)/(c). If no SSM dispatch: class (b). If SSM ran with non-zero exit: class (c) + failure details.</expect>
      <if_mismatch>If SSM history is purged: surface; SSM history retention may need investigation.</if_mismatch>
    </step>
    <step>
      <run>If class (c) (SSM dispatched but failed): identify failure mode. Cross-reference Orion API status 2026-05-04 (Andrew vendor confirm if needed) + JWT freshness at 12:43 UTC + instance resource state (`describe-instance-status` 2026-05-04 for `inf-bronze-runner`).</run>
      <expect>Failure mode classified — Orion outage / JWT expiry / instance resource / script bug</expect>
      <if_mismatch>If failure mode unknown after investigation: escalate to me + CTO; may require ADVI_INFREL_V2 expansion or sentinel-mechanism overhaul.</if_mismatch>
    </step>
    <step>
      <run>RAVC3 Phase 0: classify root cause + remediation scope. Document in TO file `<phase_0_findings>`. Cross-reference TO-1 if shared root cause.</run>
      <expect>Root cause locked + remediation path clear</expect>
      <if_mismatch>If multi-class: scope remediation to address ALL classes</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="Phase 1 remediation — gates on Phase 0 RAVC3">
    <step>
      <run>If class (a) — EventBridge rule fix + CW alarm on rule-not-firing.</run>
      <expect>Rule fixed; alarm on `Opal/InflectionBronze/CronNotFired` for missed invocations</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md</if_mismatch>
    </step>
    <step>
      <run>If class (b) — IAM/SSM agent/instance state fix + CW alarm on SSM dispatch failure.</run>
      <expect>SSM dispatch path healthy + observability via `Opal/InflectionBronze/SSMDispatchFailure`</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md</if_mismatch>
    </step>
    <step>
      <run>If class (c) — depends on failure mode. If Orion outage → document as expected + add CW alarm only. If JWT/script/resource → fix.</run>
      <expect>Remediation matches failure mode</expect>
      <if_mismatch>If failure mode is Orion outage with no fix possible: ship CW alarm only + document operational runbook</if_mismatch>
    </step>
    <step>
      <run>Backfill 2026-05-04 partition (manual SSM dispatch acceptable if RCA shows recoverable).</run>
      <expect>`bronze/orion-api-v2/2026-05-04/` populated with all expected dim files post-backfill; silver chain (post TO-1 fix) propagates within 6h</expect>
      <if_mismatch>If backfill not possible (Orion data not retroactively available): document gap permanence; do NOT delete or modify other partitions.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="Phase 2 ship — gates on Phase 1 remediation">
    <step>
      <run>If TF/Lambda changes: comp-iam gaps + safe-commit.sh + terraform apply 0-diff + tag bump per LAMBDA_DEPLOYMENT_PROTOCOL.md</run>
      <expect>Clean ship per protocol</expect>
      <if_mismatch>Per protocol</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="Phase 3 empirical — 7-day observation">
    <step>
      <run>7-day observation: NO consecutive weekday gap on `bronze/orion-api-v2/`. Daily partitions land + sentinel writes (post TO-1).</run>
      <expect>AC1-AC4 satisfied</expect>
      <if_mismatch>If a gap recurs: re-investigate same TO; do NOT close.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Parallel-able with TO-1.** No direct dependency; can run concurrent. Cross-reference findings.</coord>
    <coord>**AE 0.7 lead** per PRD §6 (CloudOps owns runner + cron debugging primary surface). AE 0.6.1 may consult on Inflection-specific orchestrator.py code.</coord>
    <coord>**Backfill scope** — 2026-05-04 only (single weekday). Weekend 2026-05-02/03 NOT in scope unless RCA reveals runner-side cause not Orion outage.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing fix">comp-iam service opal-inf-bronze-runner-cron + comp-iam service inf-bronze-runner + comp-routes trace opal-inf-bronze-runner-cron</phase>
    <phase id="2" when="before commit">comp-iam gaps + safe-commit.sh</phase>
    <phase id="3" when="after deploy">7-day observation; CW Metric/Alarm verify</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">RCA classification documented in TO `<phase_0_findings>` + CTO PRD v0.2 §5 absorption.</criterion>
    <criterion id="AC2">If runner-bug class: fix shipped + CW alarm authored.</criterion>
    <criterion id="AC3">If Orion-outage class: documented as expected + alerting authored.</criterion>
    <criterion id="AC4">2026-05-04 partition backfilled (if recoverable); silver propagation post TO-1 fix.</criterion>
    <criterion id="AC5">7-day observation no consecutive weekday gap.</criterion>
    <criterion id="AC6">RAVC5 close: commit hash + apply 0-diff (if TF) + tag bump + 7-day empirical + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — pending COO dispatch GO post Andrew acceptance</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged` until Andrew acceptance OR COO dispatch decision. AE 0.7 lead per PRD §6. Parallel-able with TO-1.</message>
  </go_signal>

  <phase_0_findings>
    <root_cause_class>b-variant — instance state race condition (manual stop colliding with automated cron)</root_cause_class>
    <classification_date>2026-05-06</classification_date>
    <classified_by>0.7.0_AE_CloudOps</classified_by>

    <finding id="1_cloudtrail">
      CloudTrail confirms: Andrew_Berman issued StopInstances on i-083ad9ae297f88e9f at 2026-05-04T12:41:14 UTC — exactly 2min 31sec before cron fired at 12:43:45 UTC. Instance was in `stopping` state when Lambda invoked.
    </finding>

    <finding id="2_lambda_behavior">
      inf-bronze-trigger Lambda (lambda_function.py line 72-85): stopping-state handler calls start_instances (always fails during stopping — IncorrectInstanceState), swallows exception with "Start failed while stopping (expected)", returns statusCode=200. EventBridge sees successful invocation; no automatic retry triggered. Mode marker was written but SSM was never dispatched.
    </finding>

    <finding id="3_s3_empty">
      aws s3 ls s3://opal-data-inf/bronze/orion-api-v2/2026-05-04/ returned empty (exit 1) — zero files written. Rules out "data written but sentinel missing" variant. Runner truly did not execute.
    </finding>

    <finding id="4_retry_stream">
      Second Lambda invocation stream (12:47:31Z) shows only INIT_START and no subsequent events — retry either failed at Lambda init or was pre-empted. Did not recover the missed start.
    </finding>

    <finding id="5_cron_discrepancy">
      Note: Lambda manifest and docstring say cron(30 12 * * ? *) = 12:30 UTC. Empirical CW data shows consistent 12:43:XX UTC firing across May 1-6. Actual deployed cron rule fires at 12:43 UTC, not 12:30. Low-priority discrepancy; manifest/doc stale — not the cause of May 4 gap but worth correcting.
    </finding>

    <fix_scope>
      (1) inf-bronze-trigger Lambda: stopping-state handler must poll until stopped (max 120s, 10s interval) then call start_instances. On timeout, raise exception so EventBridge retries. Return 200 only on confirmed start or already-running.
      (2) CW metric Opal/InflectionBronze/TriggerMissedStart — emit on stopping-race-condition detect; alarm on any occurrence.
      (3) Backfill 2026-05-04: manual SSM dispatch if Orion API retains historical data. Need confirmation Orion supports date-parameterized pulls for prior dates.
      (4) Minor: align cron expression in manifest + Lambda docstring with actual 12:43 UTC deployed rule.
    </fix_scope>

    <backfill_assessment>
      Recoverable IF Orion API supports historical date pulls. AE 0.6.1 consult needed on orchestrator.py --date flag existence. If Orion returns current-day-only data, May 4 gap is permanent and requires documentation only.
    </backfill_assessment>
  </phase_0_findings>
</task_order>
