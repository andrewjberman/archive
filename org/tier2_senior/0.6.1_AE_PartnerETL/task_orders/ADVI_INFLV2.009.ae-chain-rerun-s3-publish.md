# Task Order: ADVI_INFLV2.009 — AE 0.6.1: Chain Re-Run + S3 Publish (Post-INFLV2.005)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-009</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — gates INFLV2.010 (RD smoke + Andrew sign-off)</priority>
  </metadata>

  <objective>
    After DS ships the INFLV2.005 Revenue Ops insight script, execute a full gold chain
    rerun on the Inflection runner to publish updated platinum artifacts including the
    new InflectionInsightsPanel artifact key. Same SSM dispatch pattern as INFGRD.003.

    Note: This is a DIFFERENT rerun from INFGRD.003. INFGRD.003 produces $200M correct-scope
    data. INFLV2.009 runs AFTER INFLV2.005 to add the insights panel artifact on top of
    that baseline. If INFGRD.003 platinum is already live and correct, INFLV2.009 may
    only need to run the new script rather than a full chain — DS RAVC on INFLV2.005 will
    specify whether full rerun or incremental script-only dispatch is needed.
  </objective>

  <scope>
    <task id="1" label="Gate check">
      Confirm INFLV2.005 commit is on origin/CLOUD before dispatching:
        git fetch origin && git log origin/CLOUD --oneline -5
      Also confirm INFGRD.003 platinum is live ($~200M, 3 leaderboard entries).
    </task>

    <task id="2" label="Dispatch per DS RAVC spec">
      DS INFLV2.005 RAVC will specify:
        A) Full gold chain rerun (if new script is standalone gold script)
        B) Incremental: run only the new insights script + publisher step (if D_04 extension)

      Execute whichever pattern DS specifies. Same runner: i-0ed5afded2ebd4ed4.
    </task>

    <task id="3" label="Platinum artifact verification">
      After chain/script completes:
        - Confirm new InflectionInsightsPanel artifact is present at confirmed S3 key
        - Confirm existing artifacts unchanged (header_metrics, leaderboard, timeseries)
        - Confirm header_metrics.total.aua still in $140M–$250M range (not regressed)
    </task>

    <task id="4" label="CloudFront invalidation">
      Invalidate CF for:
        - /platinum/firm/* (if any firm artifact changed)
        - New insights artifact path specifically
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      InflectionInsightsPanel artifact present at S3 key specified by DS INFLV2.005 RAVC.
    </criterion>
    <criterion id="2">
      header_metrics.total.aua still in $140M–$250M range post-rerun.
    </criterion>
    <criterion id="3">
      CF invalidation complete.
    </criterion>
    <criterion id="4">
      RAVC to 2.0.0_SA_COO + 0.4.2_RD_AdvisorIntelligence with artifact S3 key confirmed.
      Subject: RAVC — ADVI_INFLV2.009 COMPLETE | insights artifact live | CF invalidated
      This is the go-signal for RD INFLV2.010.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gate: INFLV2.005 COMPLETE (DS RAVC with commit hash + artifact key spec).</constraint>
    <constraint>Do NOT signal COO until artifact is confirmed present at S3 key.
    Partial or failed runs are not acceptable RAVC triggers.</constraint>
    <constraint>Record in EC2_MANIFEST.json per EC2 deployment protocol if new
    SSM deployment record is required.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFLV2.005"
                status="open"
                note="Insights script commit on CLOUD + RAVC with artifact key spec."/>
  </dependencies>

  <deliverables>
    <deliverable type="ssm">Gold chain (or incremental) dispatch on i-0ed5afded2ebd4ed4.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO + 0.4.2_RD_AdvisorIntelligence.
    Go-signal for INFLV2.010.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §6 (phase decomposition)</ref>
    <ref type="runner">i-0ed5afded2ebd4ed4 — Inflection gold runner</ref>
    <ref type="prior">ADVI_INFGRD.003 TO — same dispatch pattern</ref>
  </references>
</task_order>
```
