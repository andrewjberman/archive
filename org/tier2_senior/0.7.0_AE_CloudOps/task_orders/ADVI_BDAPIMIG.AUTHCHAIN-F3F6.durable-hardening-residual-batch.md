<to_id>ADVI_BDAPIMIG.AUTHCHAIN-F3F6</to_id>
<project>ADVI_BDAPIMIG</project>
<title>bd-49f auth-chain durable-hardening RESIDUAL batch (F3-F6): OTP config-vs-transient fail-fast, native-IP bot-block classifier+alarm, direct-rc=1 alarm, device-trust silent-degrade alarm -- F1+F2 landed separately</title>
<assigned_to>0.7.0_AE_CloudOps (box-owner; owns the ALARM findings F4-alarm/F5/F6) + 0.6.0_AE_PartnerETL (bd_49f_auto_login.js author; owns the .js findings F3/F4-classifier)</assigned_to>
<consult>0.6.2_AE_PartnerETL (auditor -- f7dc5c871; F5/F6 alarm-absence grounding); 1.0.0_SA_CTO (arch-gate auth-chain + any new alarm); 2.0.0_SA_COO (logged this as a durable follow-on)</consult>
<issued_by>self-filed 0.7.0_AE_CloudOps~A 2026-07-02, per COO "F3-F6 = FOLLOW-UP batch ... log as a durable follow-on, non-urgent"</issued_by>
<issued_date>2026-07-02</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_BDAPIMIG, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active-queued (NON-URGENT durable follow-on; the two HIGH gaps F1+F2 are handled separately -- 0.6.0 authors, 0.7.0 deploys+on-box-exercises, folded into the box-rollout)</status>

<priority>
NON-URGENT. F1+F2 (the 2 HIGH source-grounded gaps = today's incident residual) are being landed NOW on a separate track. F3-F6 are the LOWER-tier residual from 0.6.2's durable-auth audit -- real hardening, no active fire. CRITICAL SEQUENCING CAVEAT (0.6.2/COO): F5 (+F6) are ALARM findings that must GROUND-THE-ALARM-ABSENCE FIRST -- F5 is flagged HYPOTHESIS in the audit (do NOT add a "direct rc=1 alarm" until it's confirmed no existing alarm already covers the rc=1 terminal; Rule-22a: a hypothesis cannot authorize a fix). F7 (cookie-freshness) is likely MOOT -- verify-then-drop.
</priority>

<context>
Source: 0.6.2_AE_PartnerETL durable-auth re-mint chain robustness audit, commit f7dc5c871 (docs .../bd-49f-auto-login-durable-hardening-audit-20260702.md). Each finding Rule-22a-tagged source-grounded vs hypothesis. F1+F2 greenlit + in-flight; F3-F6 batched here as the durable follow-on.
</context>

<scope>
F3 -- OTP config-vs-transient fail-fast (.js, 0.6.0 lane): distinguish a CONFIG error (bad adapter/mailbox/app-reg -> permanent, fail-fast LOUD, no retry-storm) from a TRANSIENT OTP-fetch miss (retry). Today a config error burns all retry attempts silently. Source-grounded.
F4 -- native-IP bot-block classifier + alarm (.js classifier = 0.6.0 lane; alarm = 0.7.0 lane): detect the BD bot-block/challenge page (native-datacenter-IP egress path -- the residential proxy is the guard, but if it drops, BD blocks) as a DISTINCT state + alarm it (vs a generic UNKNOWN loop -> MAX_STEPS). Source-grounded.
F5 -- direct rc=1 alarm (0.7.0 lane -- CloudWatch) -- HYPOTHESIS, GROUND FIRST: the audit hypothesizes a login rc=1 terminal has no direct alarm. BEFORE building: confirm no existing alarm (authtoken-absence / keepalive-absence / silver-stale-{5}) already covers the rc=1-terminal freshness gap. If covered -> CLOSE as no-op. If a genuine gap -> add a direct rc=1 SNS alarm off the session-fetch SSM failure / a rc=1 metric. Rule-22a: the hypothesis cannot authorize the alarm until the absence is ground-confirmed.
F6 -- device-trust silent-degrade alarm (0.7.0 lane) -- GROUND FIRST: if device-trust stops being set (BD stops honoring the remember-device cookie), logins still succeed but MFA fires every run -> slow OTP-exhaustion risk. Alarm on a device-trust-absent streak. Confirm the current device-trust capture (bd_device_registration in the session bundle) is observable enough to alarm on before building.
F7 -- cookie-freshness (LIKELY MOOT): verify the existing silver-stale + authtoken-absence alarms already cover cookie-freshness; if so, DROP with a one-line note. Do not build.
</scope>

<acceptance_criteria>
1. F3 (0.6.0): config-vs-transient OTP branch -> config error fails fast LOUD, transient retries. CTO arch-gate (auth-chain), 0.7.0 deploys.
2. F4: bot-block classified as a distinct state (0.6.0) + alarmed (0.7.0).
3. F5: alarm-absence GROUND-CONFIRMED first -> either CLOSE no-op (existing coverage) or add the direct rc=1 alarm (safe-apply, ledgered).
4. F6: device-trust-degrade observability ground-confirmed -> alarm on the absent-streak.
5. F7: verified moot -> dropped with a note, OR (if a real gap) folded in.
6. Each new alarm rides safe-apply; each .js change rides CTO arch-gate + 0.7.0 deploy + on-box exercise-confirm. RAVC COO + CTO + 0.6.2.
</acceptance_criteria>

<references>
  <ref type="audit">0.6.2 durable-auth audit, commit f7dc5c871 (docs/.../bd-49f-auto-login-durable-hardening-audit-20260702.md)</ref>
  <ref type="code">infra/aws/ec2/bd-49f-auto-login/bd_49f_auto_login.js ; infra/aws/terraform/bd-pipeline/ (alarms)</ref>
  <ref type="related">F1+F2 (the 2 HIGH) landed separately -- 0.6.0 authors, 0.7.0 deploys+on-box-exercises</ref>
  <ref type="rule">CLAUDE.md Rule-22 (hypothesis cannot authorize a fix -- binds F5/F6 ground-first)</ref>
</references>

<lane_note>
Split-lane: alarm findings (F5/F6, F4-alarm) = 0.7.0 (CloudWatch/TF); .js findings (F3, F4-classifier) = 0.6.0 (build-lead). NON-URGENT durable follow-on. F5/F6 GROUND-THE-ALARM-ABSENCE before building (hypothesis-gated). F7 verify-then-drop. Coordinate at pick-up; do NOT batch-build the alarms without confirming the absence each covers.
</lane_note>

<grounding_verdict who="0.7.0_AE_CloudOps~A" date="2026-07-06" rule="22a (alarm-absence ground-confirmed before build)">
GROUNDED the F5/F6 alarm-absence against live CloudWatch (describe-alarms bd-49f*) + the emit-source (comp-grep put_metric_data across infra/aws/). Live bd-49f alarm inventory (7): authtoken-absence (AuthTokenOK SampleCount<1 / 3h x3), keepalive-absence (KeepaliveOK SampleCount<1 / 1h x2), silver-stale-{allocations,fees,realized,transactions,unrealized} (TradingDayLag>2 / Firm=49f,Table=X). Metric-emit topology (source-confirmed): AuthTokenOK + per-table TradingDayLag are emitted by bd-49f-freshness-probe (EventBridge 1h, 401-specific, None=transient=no-emit); KeepaliveOK by bd-49f-keepalive (15m, 401/403->0+SNS). These are INDEPENDENT PROBE Lambdas -- NOT the login script's exit code.

F5 (direct login rc=1 alarm) = CLOSE NO-OP. The rc=1-terminal FRESHNESS gap IS covered downstream: a sustained login failure -> stale cookie -> keepalive-absence / KeepaliveOK=0 (cookie-death) AND -> stale data -> silver-stale-{5} (ultimate backstop). A direct per-run rc=1 alarm would only reduce detection LATENCY, not close a coverage gap; paging on a self-healing transient rc=1 contradicts the retired-authtoken-dead philosophy (07-02, bd-v2.44.0: don't page transients the re-auth chain self-heals). Rule-22a satisfied: absence-of-coverage REFUTED.
  REFRAME (higher-value, surfaced by the 07-06 incident): today's txn freeze was NOT a login rc=1 (login rc=0, cookie minted 00:02Z) -- it was a SILENT runner sentinel-emit AccessDenied (bd-49f-runner-role missing s3:PutObject on bronze/*), caught only by manual grounding + would surface only via the slow (holiday-extended) silver-stale backstop. The genuinely valuable alarm is a RUNNER-RUN / SENTINEL-EMIT-FAILURE alarm (fires when a session-complete run does NOT produce bronze/{date}/_BRONZE_COMPLETE.json within N hours), NOT a login rc=1 alarm. Candidate hardening AFTER base's +PutObject-on-bronze/* IAM cure lands (so the alarm doesn't fire on the currently-known gap). Route: alarm-half = 0.7.0 lane; needs the emit/marker + CTO arch-gate.

F6 (device-trust silent-degrade alarm) = DEFER (observability-emit-first). Device-trust IS captured (bd_49f_auto_login.js:540-541 bd_device_registration + bd_device_cookie_name into the session bundle) but is NOT emitted as any CloudWatch metric (no put_metric_data for device-trust anywhere in infra/aws/). => nothing to alarm on yet. F6 is therefore NOT a pure-alarm task: it needs a DeviceTrustOK emit added first (probe/runner reads bd_device_registration presence -> BD/49F/Auth DeviceTrustOK 1/0), THEN the absent-streak alarm is 0.7.0's. Emit-half = probe/runner lane (0.6.0) + CTO arch-gate. Non-urgent: device-trust GREEN through the 07-04 holiday (box i-0fa1846f self-minted WITH device-trust 07-06 00:02Z) + consequence (MFA-every-run -> OTP-exhaust -> cookie death) is covered downstream by keepalive/silver-stale as a slow backstop.

DISPOSITION: F5 closable no-op (evidence above); F6 re-scoped to emit-first (blocker named). RAVC COO+CTO+0.6.2 to run when the F3-F6 batch is actively worked (non-urgent; not raised now -- 07-06 P0 durable-serve is the active fire). The 07-06-surfaced runner/sentinel-emit-failure alarm is the item worth prioritizing when the batch reopens.
</grounding_verdict>
