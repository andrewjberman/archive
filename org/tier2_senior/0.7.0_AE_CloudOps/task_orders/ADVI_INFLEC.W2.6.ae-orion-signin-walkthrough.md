<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.6-orion-walkthrough</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: OTP selectors confirmed via inspector tool (commit b1e19d51a, 29f52f95c). -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Pair with Andrew to step through the Orion export sign-in flow. Capture: login URL, field names/selectors, OTP page layout, post-login navigation to export page, Slickgrid export selector, TRN/AUM/accounts export triggers. Output: a written Playwright selector spec AE uses to author `orion_export.ts` (W2.7). Blocked on W0.3 (Andrew schedules this pairing session).
  </objective>

  <context>PRD §5.2 + §6.3. Andrew described Orion login as: standard username/password → SMS OTP → post-login dashboard → Slickgrid export page. Specific selectors unknown until Andrew screens-share or walks AE through. This is a human pairing session output; AE captures everything in a structured doc.</context>

  <compiler_tools_mandate>
    (N/A — pairing session + doc output. No compiler runs needed.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W0.3 (Andrew schedules pairing). When Andrew signals W0.3 ready, this TO is immediately actionable."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Written selector spec at `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/advi_inflec_orion_selector_spec.md`.
    2. Spec includes: login URL, username field selector, password field selector, OTP input field selector, "submit OTP" button selector, post-login export page URL/navigation path, TRN export trigger selector, AUM export trigger, accounts_dim export trigger.
    3. Timing notes: how long Orion waits before OTP expires, page load times.
    4. Andrew confirms spec is accurate before W2.7 starts.
    5. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/advi_inflec_orion_selector_spec.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Hard block on W0.3. Do not attempt to guess selectors from Orion docs.</requirement>
    <requirement id="2">Andrew must confirm spec accuracy before W2.7.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Orion selector spec.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT guess selectors. Pair with Andrew.</rule>
  </do_not>
</task_order>
