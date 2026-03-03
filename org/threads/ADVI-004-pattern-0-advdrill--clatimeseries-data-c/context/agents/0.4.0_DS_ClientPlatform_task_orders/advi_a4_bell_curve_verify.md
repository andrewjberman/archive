# Task Order: Stream A4 — Snapshot NNA Bell Curve Math Verification

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-a4-bell-curve-verify</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Verify that commit 8247c6d0 correctly implemented absolute-value handling for
    negative NNA accounts in script 09's bell curve percentile threshold calculation.
    If the fix did not land, write a targeted patch and coordinate with DT for EC2 deploy.
    Start this in your first activation session — no thread dependency.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>data/black_diamond/scripts/gold/09_build_distribution_stats.py</ref>
    <ref>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <scope>
    <files>
      <file action="verify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
      <file action="modify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="A4.1">
      Read data/black_diamond/scripts/gold/09_build_distribution_stats.py and locate
      the bell curve percentile threshold calculation for NNA distribution views.
      Confirm whether the abs() handling for negative NNA accounts is present in the
      code as-committed. Name the specific function and line where the calculation lives.
    </requirement>
    <requirement id="A4.2">
      Read the current partner_analytics/header_metrics.json from S3
      (s3://opal-data-bd/gold/partner_analytics/header_metrics.json).
      Inspect the distribution field for the NNA view's outflow/negative segment.
      Confirm that P10/P25/Median/P75/P90 thresholds are non-degenerate:
        - Not all zero
        - Not symmetric mirrors of the positive-side thresholds
        - Values represent absolute magnitudes of outflow amounts
      Record the actual threshold values in your session log.
    </requirement>
    <requirement id="A4.3">
      If the fix DID land correctly: document the verification in your session log
      with the actual threshold values observed. Mark this requirement complete.
      No further action needed.
    </requirement>
    <requirement id="A4.4">
      If the fix did NOT land: write a targeted patch to script 09.
      Update data_contract.xml to note the corrected distribution shape.
      Signal 0.4.0_DT via your session log next steps (include your commit hash)
      for EC2 deploy via safe-ec2-deploy.sh following EC2_CODE_DEPLOYMENT_STANDARD.md.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Script 09 bell curve calculation verified against source code — function name and line cited in session log.</criterion>
    <criterion id="2">header_metrics.json outflow distribution thresholds checked — actual P10/P25/Median/P75/P90 values recorded in session log.</criterion>
    <criterion id="3">If patch needed: script 09 committed, data_contract.xml updated, DT signaled with commit hash.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read the actual script file — do not rely on the commit message alone to conclude the fix landed.</constraint>
    <constraint>Do NOT deploy directly. If a patch is needed, hand off to 0.4.0_DT via session log next steps.</constraint>
    <constraint>Do NOT use emojis in any script, log, or output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">Session log with verification result and actual threshold values</deliverable>
    <deliverable type="commit">Script 09 patch (only if fix did not land in 8247c6d0)</deliverable>
  </deliverables>
</task_order>
```
