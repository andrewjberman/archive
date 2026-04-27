<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-B.ae-orion-selector-spec</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status><!-- Gate: Andrew A1 — W0.3 pairing session must be scheduled + completed first. -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-B</wave>
    <supersedes>W2.6.ae-orion-signin-walkthrough.md (scope updated — web-form model, Slack removed)</supersedes>
    <gates_on>Andrew A1 (W0.3 pairing session)</gates_on>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-B (cc170c00)</prd_ref>

  <objective>
    Capture confirmed Orion CSS selectors and export navigation path via live pairing session
    with Andrew. Output: written spec at deliverables/advi_inflec_orion_selector_spec.md.
    This spec is the hard gate for TO-C (orion_export.ts) and TO-D (unit tests).
  </objective>

  <scope>
    Conduct W0.3 pairing session with Andrew (screen-share or walkthrough).
    Capture and document:
    1. Login URL (https://login.orionadvisor.com/ — confirm actual URL used)
    2. Username field CSS selector
    3. Password field CSS selector
    4. Submit button selector
    5. Post-submit state detection: does Orion prompt OTP, or proceed to export directly?
    6. OTP input field CSS selector (if 2FA triggered)
    7. OTP submit button CSS selector
    8. Post-OTP (or post-login) export page URL pattern
    9. Export template navigation for each: TRN, AUM, SlickGrid
       — how to reach each template and trigger download

    ALSO during pairing:
    - Test the inf-otp-relay Function URL (from TO-A) on Andrew's phone.
      GET {Function_URL} must render HTML form on mobile. Confirm and document.
    - Document exact OTP SMS format Orion sends (digit count, any prefix text).

    Deliverable: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/advi_inflec_orion_selector_spec.md
    Include Andrew confirmation in spec frontmatter before closing.
  </scope>

  <acceptance_criteria>
    1. Selector spec document at deliverables/advi_inflec_orion_selector_spec.md with:
       login URL, username selector, password selector, submit selector, post-submit state
       detection (OTP vs no-OTP), OTP input selector, OTP submit selector, post-OTP export
       page URL pattern, TRN/AUM/SlickGrid navigation path.
    2. Lambda Function URL confirmed rendering on Andrew's phone during pairing. Noted in spec.
    3. OTP SMS format documented (digit count, expected pattern).
    4. Andrew confirms spec accuracy before TO-C starts. Approval noted in spec frontmatter.
    5. Session log with pairing notes.
    6. RAVC4 to 2.0.0_SA_COO with spec path + Andrew approval confirmation.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT reference Slack in the selector spec — Slack was eliminated by W3.B pivot.</rule>
    <rule>Do NOT start TO-C or TO-D without Andrew's explicit spec confirmation in frontmatter.</rule>
  </do_not>
</task_order>
