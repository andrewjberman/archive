<to_id>ADVI_COTETL.AUAFIX-L4</to_id>
<project>ADVI_COTETL</project>
<title>cot AUA freeze/staleness ALERT: register cot AUA in comp-freshness (close the no-oracle gap) + wire a staleness alarm that FOLDS the F-1 egress fix -- verify egress DELIVERS</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX PRD decomposition, 2026-06-18; CTO PRD ef04a08cc)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>cancelled -- Andrew-direct 2026-07-07 ("if this rides solely on sms alert programming then fuck it, mark all as done or canceled"). Ground-truthed before closing: opal-critical-surface-alerts is dead on BOTH subscribed channels, not just SMS -- the SMS number (+17862617679) is SNS-sandbox/unverified (same root cause as the partner-etl-ops-alerts P1 today), AND the SQS subscriber (opal-critical-surface-alerts-coo) has ZERO Lambda event-source-mappings, same zero-consumer pattern as the P1 fix. The comp-freshness oracle-registration half of this TO's scope appears independently closed (cot IS registered in comp-freshness as of 2026-07-07, verified live) -- likely landed via other freshness-rollout work, not this TO. The staleness-alarm-wiring half was never built and is not being built. Not reopening without a fresh Andrew/COO directive.</status>
<priority>HIGH -- the "never-silent-again" hardening. RIDES F-1 (already #1 on AE's post-TO-D3 queue): F-1 (opal-critical-surface-alerts SES-migrate/sub-confirm) IS L4's egress leg -- same fix, now also a cot-AUA-freshness dependency. The comp-freshness oracle registration + the staleness alarm are the additional L4 work. Sequenced behind TO-D3 alongside F-1.</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md (ef04a08cc) -- §4 the silent-freeze gap, §5 L4, §7 AC4</ref>
  <ref type="f1-consolidation">F-1 (opal-critical-surface-alerts egress fix) already bumped to #1 on AE's queue (COO drive cycle-9, 194450Z) -- triple-justified: SEV1 critical-surface alert + graph freeze-backstop (CVO G-1) + this cot-AUA-freshness L4. One egress fix, three payoffs.</ref>
  <ref type="delivery-not-publish">memory/reference_sns_confirmed_sub_not_equal_delivers -- verify NumberOfNotificationsDelivered>0, NOT publish-accepted/sub-confirmed. SMS-in-sandbox + SSE-KMS-without-service-key both silently fail delivery; the PRD's "doubly silent" failure mode.</ref>
  <ref type="no-oracle">PRD §4(a): comp-freshness chain --list shows NO cot AUA entry today (CTO-verified) -- nothing watched it for 9 days.</ref>
</references>

<scope>
Make a multi-day cot AUA freeze LOUD (it was silent for 9 days -- two blind spots: no oracle + broken egress):
1. **Register cot AUA in comp-freshness** (close the no-oracle gap): add the cot AUA gold/platinum chain + served artifact to comp-freshness so there IS a freshness signal (today `comp-freshness chain --list` has no cot entry).
2. **Wire a staleness alarm** on cot AUA data_as_of: a multi-day stall (e.g. data_as_of not advancing past N days) fires an alert.
3. **The alert egress = the F-1 fix** (SES-migrate/sub-confirm opal-critical-surface-alerts). VERIFY egress DELIVERS: NumberOfNotificationsDelivered>0 on a synthetic freeze -- NOT publish-accepted, NOT sub-confirmed (the doubly-silent failure mode; SMS-sandbox + SSE-KMS-without-service-key both silently drop).
4. Acceptance test: a SYNTHETIC freeze (simulate cot AUA stalling) fires a DELIVERED alert.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before wiring">
    <step>
      <run>comp-freshness chain --list (confirm cot AUA absent today) + comp-iam service (confirm the alarm/SNS publish perms) for the freshness-alarm principal</run>
      <expect>cot AUA confirmed absent from the oracle (the gap); the principal that will publish the staleness alarm has SNS publish to opal-critical-surface-alerts (post-F-1-fix).</expect>
    </step>
  </phase>
  <phase id="2" when="after wiring, the synthetic-freeze acceptance test">
    <step>
      <run>Synthetic cot-AUA-freeze -> the staleness alarm fires -> confirm DELIVERY via NumberOfNotificationsDelivered>0 (CloudWatch SNS metric), NOT publish-accepted</run>
      <expect>The synthetic freeze produces a DELIVERED alert (Delivered>0). If Delivered=0 while publish succeeded -> egress still broken (F-1 not fully fixed) -> the alert is still silent. AC4 requires DELIVERED.</expect>
      <if_mismatch>Delivered=0 = the doubly-silent failure persists. Do NOT mark L4 done on publish-accepted. Re-check the F-1 egress (SES sub-confirm / KMS service-key grant).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **F-1 is the shared egress (THREE consumers now):** opal-critical-surface-alerts serves (a) the SEV1 critical-surface alert, (b) the graph freeze-backstop (CVO G-1 / COMPRAIL mandatory-rail freshness), (c) this cot-AUA-freshness L4. The F-1 fix (already #1 on AE) restores all three. L4's alarm is a NEW publisher to that topic -- verify it after F-1 lands.
- **Sequenced behind TO-D3** alongside F-1 (AE's queue: TO-D3 -> F-1=L4-egress -> COTETL L1/L5 -> P2-2). The oracle-registration + alarm-wiring are the L4-specific work beyond F-1's egress fix.
- **L5 (CVO) re-verifies** this alert as part of the closeout + the standing freshness-guard cert.
- **Independent of L1/L2** (it's the hardening leg) but the synthetic-freeze test is cleanest once the chain is live (post-L1).
</cross_domain_coordination>

<acceptance_criteria>
- AC4 (PRD): a multi-day cot-AUA freeze fires a DELIVERED alert (egress delivery-verified via NumberOfNotificationsDelivered>0, NOT publish-accepted); cot AUA has a LIVE freshness oracle (registered in comp-freshness, was absent).
- The synthetic-freeze acceptance test produced a delivered alert (Delivered>0).
- F-1 egress consolidation confirmed (the same fix serves all 3 consumers).
- Session log Compiler Tools section reproduces every `<run>` with the delivery metric + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Freshness oracle registration + a staleness alarm + the egress fix. No served artifact, pipeline, or producer data touched -- monitoring/alerting infra.</no_reprocess_needed></data_reprocess_scope>
