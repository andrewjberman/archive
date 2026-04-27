# Task Order: ADVI_INFGRD.003 — AE 0.6.1: Silver Rebuild + Full Chain Re-Run

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-infgrd-003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — final chain run before RD validation + Inflection production sign-off</priority>
  </metadata>

  <objective>
    After DS commits the ADVI_INFGRD.002 silver-layer firm filter, execute a full silver
    rebuild (non-incremental) followed by a full gold chain re-run on the Inflection runner.
    Existing silver parquets carry contaminated data (9 advisors, $429M). The rebuild
    applies the new advisor_firm filter from scratch across all historical data.
    Expected result: ~4 Inflection-only advisors, ~$191M total AUA in platinum artifacts.
  </objective>

  <scope>
    <task id="1" label="Gate check">
      Confirm ADVI_INFGRD.002 commit is on CLOUD origin before proceeding:
        git fetch origin && git log origin/CLOUD --oneline -5
      Confirm the commit hash from DS RAVC matches HEAD or is in history.
      Also confirm DS~A F1-F3 D_04 timeseries patch is live (parallel track, same runner).
    </task>

    <task id="2" label="Silver rebuild (non-incremental)">
      Dispatch SSM command to the Inflection runner (i-0ed5afded2ebd4ed4) to run
      convert_orion_to_silver.py with --upload flag (non-incremental full rebuild).

      The silver rebuild will:
        - Pull latest bronze CSVs from s3://opal-data-inf/bronze/orion/
        - Apply the new advisor_firm filter (ADVI_INFGRD.002)
        - Upload filtered silver parquets to s3://opal-data-inf/silver/

      Confirm Guard C diagnostic output in SSM logs — should show firm breakdown table
      with ONLY inflection_wealth_management advisors post-filter.
      Confirm Guard B does NOT fire (AUA in $50M–$400M range).
    </task>

    <task id="3" label="Full gold chain re-run">
      After silver rebuild confirms success:
        - Dispatch full Inflection gold chain (I_00 through I_09 + publisher)
        - Use same SSM dispatch pattern as ADVI_INFLEC W4.13 / SCOPEFIX-1 chain re-run
        - Expected runtime: 2-4 hours

      Monitor chain progress via SSM logs. Do NOT signal COO until all scripts confirm exit 0.
    </task>

    <task id="4" label="Platinum artifact verification">
      After chain completes:
        aws s3 cp s3://opal-data-inf/platinum/firm/header_metrics.json /tmp/infgrd-hm.json
        cat /tmp/infgrd-hm.json | python -c "import json,sys; d=json.load(sys.stdin); print(d['total']['aua'])"

        aws s3 cp s3://opal-data-inf/platinum/firm/leaderboard.json /tmp/infgrd-lb.json
        cat /tmp/infgrd-lb.json | python -c "import json,sys; d=json.load(sys.stdin); print(len(d['advisors']))"

      Expected: total_aua ~$191M (within 30% tolerance: $140M–$250M), advisor count ~4.
      Also confirm s3://opal-data-inf/platinum/advisors/ contains ONLY Inflection employee
      subdirs (no keil_financial_partners/, no jeremy_keil/ if not Inflection).

      Run comp-validate if applicable for the Inflection pipeline config.
    </task>

    <task id="5" label="CloudFront invalidation">
      Trigger CF invalidation for all affected platinum paths:
        - /platinum/firm/* (header_metrics, leaderboard, partner_analytics, timeseries)
        - /platinum/advisors/* (per-advisor directories)
      Same pattern as prior CF invalidations on opal-data-inf distribution.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Silver rebuild completes exit 0. Guard C prints firm breakdown showing only
      inflection_wealth_management. Guard B does NOT fire.
    </criterion>
    <criterion id="2">
      Full gold chain (I_00–I_09 + publisher) completes exit 0 on all scripts.
    </criterion>
    <criterion id="3">
      platinum/firm/header_metrics.json total_aua is in range $140M–$250M (target ~$191M).
    </criterion>
    <criterion id="4">
      platinum/firm/leaderboard.json advisor count matches Andrew's confirmed Inflection
      employee count (~4, exact number from .001 + Andrew confirm).
    </criterion>
    <criterion id="5">
      platinum/advisors/ directory contains ONLY Inflection employee subdirs. No Keil entries.
    </criterion>
    <criterion id="6">
      RAVC sent to 2.0.0_SA_COO + 0.4.0_DS_ClientPlatform + 0.4.2_RD_AdvisorIntelligence with:
        - Silver rebuild exit 0 confirmation
        - Gold chain exit 0 confirmation
        - Actual total_aua value from header_metrics.json
        - Actual advisor count from leaderboard.json
        - CF invalidation complete
      Subject: RAVC — ADVI_INFGRD.003 COMPLETE | $[X]M AUA | [N] advisors | CF invalidated
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Full non-incremental silver rebuild required. Incremental rebuild will NOT
    apply the new filter to pre-existing contaminated parquets.</constraint>
    <constraint>Do NOT signal COO until all scripts exit 0 AND platinum AUA is in range.
    If chain fails mid-run, triage and report with failed script name + exit code.</constraint>
    <constraint>If Guard B fires during silver rebuild (AUA out of bounds), STOP and escalate
    to COO + DS. Do not continue the gold chain on bad data.</constraint>
    <constraint>Record the deploy in EC2_MANIFEST.json per EC2 deployment protocol if
    a new SSM deployment record is required.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFGRD.002"
                status="open"
                note="Silver filter commit must be on origin/CLOUD before silver rebuild.
                Verify commit hash from DS RAVC matches origin before dispatching SSM."/>
  </dependencies>

  <deliverables>
    <deliverable type="ssm">Silver rebuild SSM dispatch + gold chain SSM dispatch on
    Inflection runner i-0ed5afded2ebd4ed4.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO + 0.4.0_DS_ClientPlatform +
    0.4.2_RD_AdvisorIntelligence with full verification payload (AUA, advisor count,
    CF invalidation). This is the go-signal for RD .004.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md §5.2 — Backfill Strategy</ref>
    <ref type="prior_chain">ADVI_INFLEC W4.13 — gold chain dispatch pattern (same runner)</ref>
    <ref type="gate">ADVI_INFGRD.002 DS commit RAVC</ref>
    <ref type="runner">i-0ed5afded2ebd4ed4 — Inflection gold runner</ref>
  </references>
</task_order>
```
