<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w6.4-otp-dashboard</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Optional polish: build a dashboard or small web relay form for Andrew to submit OTP from mobile without using the AWS CLI. PRD §6.3 options: (a) CLI one-liner (already implemented in W2.5), (b) iOS Shortcut posting to S3, (c) tiny password-protected web form. Implement per Andrew's Q11 preference (OPEN). If Andrew selects CLI-only, this TO is a no-op — close it.
  </objective>

  <context>PRD §6.4. Purely a UX polish TO. Blocked on W6.3 (core flow working) + Andrew Q11 answer. If Andrew's preference is CLI + iOS Shortcut, AE writes the Shortcut `x-callback-url` spec + S3 pre-signed URL generation, rather than a web form. If web form: minimal, password-protected, serves via HTTPS (CloudFront or Lambda URL).</context>

  <compiler_tools_mandate>
    (N/A — optional TO; implementation varies by Q11 answer.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on Andrew Q11 answer. If no answer by W6.3 completion, close as 'deferred pending Q11'."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. If Q11 = CLI only: close this TO as deferred. No action.
    2. If Q11 = iOS Shortcut: Shortcut YAML spec documented + pre-signed URL generation script written.
    3. If Q11 = web form: form deployed, password-protected, Andrew can submit OTP from mobile.
    4. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="create">(depends on Q11 answer)</file></files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on Andrew Q11 answer.</requirement>
    <requirement id="2">Optional — if Andrew is happy with CLI, close immediately.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with Q11 resolution + implementation if applicable.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT build if Andrew says CLI is sufficient.</rule></do_not>
</task_order>
