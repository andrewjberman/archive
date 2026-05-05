<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-006</id>
    <project>ADVI_INFLEC</project>
    <title>INF_I_D00c geo_drill key emit — cumulative_chart geo_drill absent (YELLOW cell)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A (primary)</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- COMPLETE 2026-05-05. DS~A Phase 0+1: 2dd28fe9f + 927809851. AE 0.6.1 Phase 2: SSM 0bbbd1f8 inf-gold-layer-runner 15:22:41Z. geo_drill present: True, len=1, ETag c3744910317ee02317ef519ecc51d529. AC1-4 PASS. YELLOW->GREEN upgrade confirmed. DS~A to update matrix cell. -->
    <priority>low</priority>
    <estimated_effort>0.5d (single key addition to INF_I_D00c; chain re-run ~15min)</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v3 — YELLOW: cumulative_chart.json geo_drill key absent; FE optional-chains so no crash</ref>
    <ref type="script">data/orion/scripts/gold/INF_I_D00c.cumulative_chart.py — CATALOG entry added `87f794863`; script produces cumulative_chart.json</ref>
    <ref type="compiler_evidence">comp-pipescript io INF_I_D00c — not resolving in graph (script exists on filesystem; not fully indexed)</ref>
    <ref type="fe_pattern">portal/src/api/endpoints/advisor-intelligence.ts getCumulativeChart — consumes cumulative_chart.json; FE optional-chains geo_drill key</ref>
  </references>

  <context>
    INF_I_D00c.cumulative_chart.py produces platinum/firm/cumulative_chart.json. The audit matrix
    v3 rates the geo_drill key as YELLOW — the key is absent from the emitted artifact, but the
    FE optional-chains so there's no crash. This is a real data gap (geo-drillable view is not
    populated for Inflection) but it doesn't block the primary cumulative chart display.

    Fix: add geo_drill key to INF_I_D00c output, sourced from the same geographic breakdown
    data that PartnerAnalytics already uses (views.geo from partner_analytics_*.json or the
    canonical geo donut source).

    This is a YELLOW → GREEN upgrade, not a RED fix. Low priority relative to AUDIT-002/003.
  </context>

  <phase id="0" when="before any write — confirm geo_drill source">
    <step>
      <run>comp-pipescript io INF_I_D00c (or read script directly) — identify current WRITES and what reads are in place</run>
      <expect>Script writes cumulative_chart.json; reads cumulative AUA + chart data; does NOT include geo_drill</expect>
      <if_mismatch>If geo_drill already in script but not in artifact — execution/chain issue, not code issue</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json /tmp/pa.json; python3 -c "import json; d=json.load(open('/tmp/pa.json')); print([k for k in d.keys()])"; echo "---"; python3 -c "import json; d=json.load(open('/tmp/pa.json')); geo=d.get('views',{}).get('geo',{}); print(list(geo.keys())[:5])"</run>
      <expect>partner_analytics.json has views.geo with geographic breakdown data compatible with geo_drill shape expected by FE</expect>
      <if_mismatch>If geo source structure differs from geo_drill expected shape — document shape delta and adapt accordingly</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="before committing fix">
    <step>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_I_D00c.cumulative_chart.py</run>
      <expect>Exit 0 — py_compile + AST + ruff all pass</expect>
      <if_mismatch>Fix all errors before committing</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp data/orion/scripts/gold/INF_I_D00c.cumulative_chart.py s3://opal-data-inf/code/gold/ &amp;&amp; comp-pipescript deployed INF_I_D00c</run>
      <expect>MATCH</expect>
      <if_mismatch>Re-upload</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="after AE chain re-run (targeted: INF_I_D00c only)">
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/cumulative_chart.json /tmp/cc.json; python3 -c "import json; d=json.load(open('/tmp/cc.json')); print('geo_drill present:', 'geo_drill' in d); print('geo_drill len:', len(d.get('geo_drill',{})))"</run>
      <expect>geo_drill present: True; geo_drill len &gt; 0</expect>
      <if_mismatch>If present but empty: geo source data gap; flag as RED-(c) and escalate to COO with evidence</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>AE 0.6.1: targeted re-run of INF_I_D00c only (if chain supports targeted dispatch); otherwise --from INF_I_D00c. DS~A provides MATCH before GO.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">cumulative_chart.json geo_drill key present and non-empty post-chain</criterion>
    <criterion id="AC2">comp-pipescript deployed MATCH on INF_I_D00c before AE dispatch</criterion>
    <criterion id="AC3">Session log Compiler Tools section reproduces each &lt;run&gt; + observed result + PASS/FAIL vs &lt;expect&gt;</criterion>
    <criterion id="AC4">RAVC3 to COO with commit hash + AC1-3 status. YELLOW → GREEN upgrade confirmed in AUDIT matrix (DS~A amends matrix cell or COO does in next GT-recon).</criterion>
  </acceptance_criteria>
</task_order>
