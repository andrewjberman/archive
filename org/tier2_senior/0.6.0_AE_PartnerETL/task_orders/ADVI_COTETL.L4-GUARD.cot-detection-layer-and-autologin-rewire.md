<task_order>
<id>ADVI_COTETL.L4-GUARD</id>
<title>cot re-freeze guard: detection layer (keepalive + freshness-probe + cot-cookie-alerts SNS) + rewire cot 02:00 off the MFA-failing session-fetch to the canonical firm-parameterized auto-login</title>
<issued_to>0.6.0_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P0 — #1 documented fabric priority (cot silent re-freeze)</priority>
<project>ADVI_COTETL</project>

<context>
cot's served AUA froze SILENTLY for 9 days (06-09 -> data_as_of stuck) once already. Root of the recurrence risk: cot's 02:00 refresh still runs the OLD MFA-failing `data/cot/scripts/bronze/cot_bd_session_fetch.py`, which fails with NO alarm -> cot silently re-freezes in ~1d. CVO is firing the stopgap (re-fire the cot completing-run on a77d58e45 to write a live blackdiamond/cot/session) IN PARALLEL with this TO; this TO is the DURABLE fix so the stopgap never has to be repeated and a future freeze ALARMS instead of going silent.

Architecture already on the ground (grounded, not assumed):
- Canonical auto-login = `infra/aws/terraform/bd-49f-auto-login/` — Playwright full sign-in + OTP + device-trust, already FIRM-PARAMETERIZED (commits a1a49d27b firm-derive relay-default `blackdiamond/${BD_FIRM_ID}/otp-relay`; a69875e97 firm-param debug-shot key `ec2/bd-${firm}-auto-login/debug`). a77d58e45 = the COMPLETE sign-in + Kimi-classify hardening ("one script, hardens cot+49F"). This is the target cot must rewire TO.
- OLD path to retire from cot's 02:00 trigger: `data/cot/scripts/bronze/cot_bd_session_fetch.py` (writes the BD session secret that `cot_bronze_ingest.py` reads from Secrets Manager).
- cot box: i-0643a5bee8a8feabf (t3.large, 37bad0246). NOTE per CVO: it was slated for 0.7.0 overnight STOP — coordinate start-on-demand with CVO/0.7.0 before any live run.

CTO (1.0.0_SA_CTO) ARCH-GATES all design questions — route the detection-layer shape (probe cadence, alarm thresholds, SNS topic/sub design) + the rewire cutover plan to CTO before deploy. This is the L4 leg of ADVI_COTETL AUAFIX (AE freeze-alert + comp-freshness oracle, folds F-1) plus the auto-login rewire.
PRD: docs/architecture/ADVI_COTETL_AUAFIX_PRD.md.
</context>

<scope>
PART A — DETECTION LAYER (firm-twin of the 49F pattern; so a cot session staleness ALARMS, never silent again):
  1. Freshness-probe on the cot session/cookie state (the blackdiamond/cot|${BD_FIRM_ID}/session secret + the served cot AUA data_as_of) that emits a CloudWatch metric/alarm when the session is stale OR cot served AUA stops advancing past its expected cadence.
  2. cot-cookie-alerts SNS topic (firm-param twin of 49F's), wired so a cot session/freeze failure publishes to opal-critical-surface-alerts (the COO SQS rider) — i.e. the failure reaches the COO /drive loop, not a silent void.
  3. Keepalive as designed with CTO (so the device-trust cookie does not lapse between nightly runs).

PART B — REWIRE cot's 02:00 trigger off `cot_bd_session_fetch.py` to the canonical firm-parameterized auto-login (bd-49f-auto-login, firm=cot/${BD_FIRM_ID}), so the 02:00 refresh uses the WORKING auto-login + device-trust path. Verify the rewired trigger writes a live, mintable cot session that cot_bronze_ingest.py consumes successfully.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service cot</run>
      <expect>Current cot runner/role boto3 surface enumerated; identify whether SNS:Publish to a cot-cookie-alerts topic + Secrets Manager write to the canonical cot session path are already granted.</expect>
      <if_mismatch>STOP. Note the missing grant; it must be added in iam.tf as part of this TO (Part A SNS publish + canonical session write).</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io cot_bd_session_fetch</run>
      <expect>READS/WRITES of the OLD session-fetch enumerated incl the Secrets Manager session secret cot_bronze_ingest.py depends on — confirm the canonical auto-login writes the SAME consumable shape before rewiring.</expect>
      <if_mismatch>STOP. If the canonical auto-login output shape differs from what cot_bronze_ingest.py reads, surface to CTO (arch-gate) before cutover — a shape mismatch silently breaks bronze.</if_mismatch>
    </step>
    <step>
      <run>comp-freshness chain cot</run>
      <expect>Baseline cot chain freshness captured (session secret + served AUA data_as_of) so the detection-layer thresholds key off real cadence, not guessed values.</expect>
      <if_mismatch>Record the baseline regardless; if cot is currently frozen, that IS the signal the probe must catch.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-iam gaps</run>
      <expect>Zero new permission gaps after the iam.tf change (SNS:Publish to cot-cookie-alerts + canonical session write for the cot role).</expect>
      <if_mismatch>STOP. Do not safe-apply until comp-iam gaps is clean.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-freshness chain cot</run>
      <expect>After the rewired trigger runs (coordinated start-on-demand), the cot session secret + served AUA advance — freshness PASS, not frozen.</expect>
      <if_mismatch>Surface to COO + CTO. The rewire did not unfreeze cot; do not close the TO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
  1. DETECTION proven LIVE: deliberately stale/missing cot session is detected and an alert lands on opal-critical-surface-alerts (verify the COO SQS rider or the alarm transitions to ALARM) — the "silent freeze can never recur" gate. EXERCISE it, do not just configure it.
  2. REWIRE proven: cot's 02:00 trigger no longer invokes cot_bd_session_fetch.py; it invokes the canonical firm-parameterized auto-login; a coordinated run writes a live cot session that cot_bronze_ingest.py mints successfully (cite S3/Secrets path + mtime + a 200/mint evidence line).
  3. Terraform-only deploy (safe-apply), iam.tf 0-gap, tag + push --follow-tags; EC2 code via S3->pull (never inline/on-VM). Coordinate the cot box (i-0643a5bee8a8feabf) start-on-demand with CVO/0.7.0.
  4. CTO arch-gate sign-off on the detection-layer design + rewire cutover BEFORE deploy.
  5. Session log Compiler Tools section reproduces every &lt;run&gt; above with observed output + pass/fail vs &lt;expect&gt;. Missing rows = REWORK.
</acceptance_criteria>

<cross_domain_coordination>
  - CVO (3.0.0_SA_CVO): firing the parallel stopgap (re-fire cot completing-run on a77d58e45). Coordinate so your rewire does not race CVO's session write; CVO also owns cot box start-on-demand coordination.
  - 0.7.0_AE_CloudOps: owns the cot box (i-0643a5bee8a8feabf) overnight STOP schedule — coordinate start-on-demand.
  - opal-critical-surface-alerts SNS (now multi-consumer): Part A adds a cot publisher; confirm it does not collide with existing 49F/egress publishers.
  - CTO arch-gate on all design questions.
</cross_domain_coordination>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md</ref>
  <ref type="canonical-autologin">infra/aws/terraform/bd-49f-auto-login/</ref>
  <ref type="old-script-to-retire">data/cot/scripts/bronze/cot_bd_session_fetch.py</ref>
  <ref type="completing-run-commit">a77d58e45</ref>
</references>
</task_order>
