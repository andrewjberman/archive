<task_order>
  <metadata>
    <id>YALP_MDSRC.C6</id>
    <slug>ae-ycharts-credential-refresh-from-har</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <!-- ROUTING 2026-05-21 (COO): C6 originally issued to base 0.7.0_AE_CloudOps; base went NOT-REGISTERED so COO reassigned to ~A (2450c41ea); Andrew then directed the ~A session to RE-REGISTER as base 0.7.0_AE_CloudOps (PID 31396 — the same agent throughout). issued_to restored to 0.7.0_AE_CloudOps, now the live base lane. Lane-agnostic TO (HAR extract + Secrets Manager write); no work lost in the base->~A->base routing. -->
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — Andrew-direct (2026-05-21, relayed via CTO). Refresh the YCharts interim credential: a colleague is letting us use his YCharts signin (more stable than the prior Alyssa account). A fresh HAR capture exists; C6 extracts the cookie bundle and refreshes the Secrets Manager secret the C1 pipeline reads. CREDENTIAL-PREP ONLY — the YCharts execution freeze still holds (see context); nothing runs against YCharts.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct. A stable interim YCharts session means that when Andrew lifts the execution freeze, the C1 integration starts from a non-degraded session (the prior account was single-session-eviction-prone).</priority>
    <sla>~0.5 effort-day — a bounded credential-refresh op.</sla>
  </metadata>

  <references>
    <har>C:\Users\AndrewBerman\Downloads\ycharts.com(mchm).har — the fresh colleague-signin YCharts HAR. PATH HAS PARENS — quote it in every command. Read it IN PLACE from Downloads; it stays OUT of the repo tree.</har>
    <c1>YALP_MDSRC.C1 — the YCharts credential pipeline. C6 refreshes the same interim secret C1 reads. Confirm the exact secret name + the cookie-bundle JSON shape against the C1 design before writing.</c1>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED) §3 — third-party credentials live ONLY in Secrets Manager; never in git, logs, or messages.</standard>
  </references>

  <context>
    The C1 capture pipeline reads an interim YCharts cookie bundle from an AWS Secrets Manager secret (ycharts/credentials, per the C1 design — AE confirms exact name). The prior bundle was an Alyssa-account session, single-session-eviction-prone. Andrew has arranged a colleague's YCharts signin as a more stable interim credential and captured a fresh HAR. C6 is the manual refresh of that secret from the new HAR — the same operation C1's capture Lambda automates, done once by hand.

    FREEZE STILL HOLDS. Andrew has NOT lifted the YCharts execution freeze (BUILD/STAGE-YES, RUN-NO). C6 is credential-PREP — refreshing a stored secret — NOT a YCharts process run. C1's capture Lambda stays deployed-dormant (EventBridge schedule DISABLED, no invoke). C6 makes NO live YCharts call. The dedicated-seat plan is unchanged — the colleague signin is explicitly interim; the dedicated seat remains the end state.
  </context>

  <scope>
    <in_scope>
      - Read the HAR in place from the quoted Downloads path. Extract the YCharts cookie bundle — the session cookies + aws-waf-token per the C1 / A3-P2 auth-session model.
      - Confirm the target Secrets Manager secret name + the bundle JSON shape against the C1 design (this is a REFRESH of the existing interim secret, not a new secret).
      - Write the refreshed bundle to that Secrets Manager secret (aws secretsmanager put-secret-value / update).
      - Structural validation (NON-EXECUTING — no live YCharts call): confirm the written bundle has the expected cookie names + non-expired expiry timestamps + the aws-waf-token, matching the C1-expected shape.
    </in_scope>
    <out_of_scope>
      - Any live YCharts call — no probe, no capture-Lambda invoke, no session test. The freeze holds.
      - Enabling C1's EventBridge schedule or invoking the capture Lambda — it stays dormant.
      - Re-architecting C1 — C6 is a credential refresh only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>C6 is a credential-refresh op — no gold script, portal component, route, IAM-policy, or schema change. No comp-* graph tool applies. The audit check is the structural validation below.</note>
    <phase id="1" when="after writing the secret">
      <step>
        <run>aws secretsmanager get-secret-value on the refreshed secret; structurally inspect the bundle — cookie NAMES + expiry timestamps + aws-waf-token presence (names/expiry/shape ONLY — never echo cookie VALUES).</run>
        <expect>Bundle present, JSON shape matches the C1-expected contract, expected cookie names present, expiry timestamps in the future, aws-waf-token present. NO live YCharts call made.</expect>
        <if_mismatch>If the bundle is malformed, missing a cookie, or already expired — do not RAVC2; report the structural gap (which field, NOT its value) and re-extract from the HAR.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - HARD SECURITY CONSTRAINTS (Third-Party Data Standard §3 — non-negotiable):
      * The cookie bundle goes ONLY to Secrets Manager. NEVER commit it to git, NEVER echo cookie values in logs, session logs, commit messages, or agent-to-agent messages. RAVC2 reports the refresh structurally (cookie names/expiry present) — never a value.
      * The HAR file stays OUT of the repo — do not copy it into the workspace tree, do not git-add it. Read in place from the Downloads path. (`*.har` is already in .gitignore, line 270 — belt-and-suspenders confirmed; the operative rule is still: don't add it.)
      * The Downloads path has parentheses — quote it in every command.
    - No silver/bronze/gold or S3-data changes — auto-rule 4 N/A.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — the YCharts cookie bundle extracted from the colleague-signin HAR and written to the C1 Secrets Manager secret; the prior (Alyssa) bundle replaced.
    - AC2 — Phase-1 structural validation passes: bundle shape matches the C1 contract, expected cookie names + future expiry + aws-waf-token present — confirmed WITHOUT any live YCharts call.
    - AC3 — zero credential leakage: no cookie value in any commit, log, or message; the HAR not added to the repo. C1's capture Lambda confirmed still dormant (EventBridge DISABLED, not invoked).
    - AC4 — session log Compiler Tools section reproduces the Phase-1 structural check (names/shape only); RAVC2 to COO + CC CTO reporting the refresh structurally.
  </acceptance_criteria>
</task_order>
