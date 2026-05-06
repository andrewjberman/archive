<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-003</id>
    <project>ADVI_INFLEC</project>
    <title>joe_brandenburg top_holdings.json — rep_id resolution + INF_I_D02b catalog add</title>
    <issued_to>0.4.0_DS_ClientPlatform~B (rep_id resolution + script fix) + 0.6.1_AE_PartnerETL (catalog add + chain re-run)</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- DS~B GOed via MCP 20260505T123459Z. COMPLETE: commits dffb2bf22 (INF_I_D02b naming fix + S3 upload) + e257875ec (INF_D_04 sibling fix); joe_brandenbrug top_holdings.json QA emitted qa/advisors/joe_brandenbrug/ 20260505T174425Z; DS~B RAVC5 20260505T173651Z + RAVC6 naming correction 20260505T174441Z. Residual: AE 0.6.1 PROD promotion + silver/api_dims/assets/ rep_id=6 gap (INFINGE Phase 1 scope). -->
    <priority>high</priority>
    <estimated_effort>1d (0.5d DS~B rep_id + script fix; 0.5d AE catalog add + chain)</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v3 — RED: joe_brandenburg/top_holdings.json MISSING</ref>
    <ref type="dsb_gap_dump">docs/architecture/_drafts/INFLEC_AUDIT_DSB_IWM_GAPS.md — Gap 6: silver/api_dims/assets/ only has rep_ids 3/11/12; INF_I_D02b.top_holdings.py ADVISOR_KEY_BY_REP_ID hardcoded 3/11/12</ref>
    <ref type="compiler_evidence">comp-pipescript io INF_I_D02b — script exists at data/orion/scripts/gold/INF_I_D02b.top_holdings.py; not currently in compiler graph (not indexed in comp-pipescript)</ref>
    <ref type="script_path">data/orion/scripts/gold/INF_I_D02b.top_holdings.py</ref>
  </references>

  <context>
    INF_I_D02b.top_holdings.py produces platinum/advisors/{advisor}/top_holdings.json for each
    Inflection advisor. The script has ADVISOR_KEY_BY_REP_ID hardcoded to map rep_ids {3: 'inflection_wealth_management',
    11: 'peter_lee', 12: 'patrick_scanlan'}. joe_brandenburg is missing — his Orion rep_id is unknown.

    silver/api_dims/assets/ (from HISTBF backfill) only has subdirectories for rep_id=3/11/12.
    joe_brandon is listed as a 4th Inflection advisor (per S7SUMFIX: 4 advisor summary.json files exist)
    but has no rep_id entry in the assets silver data.

    Two-step fix: DS~B identifies the rep_id → updates INF_I_D02b → AE adds to dispatch catalog.
  </context>

  <phase id="1" when="before writing any fix">
    <step>
      <run>DS~B: aws s3 ls s3://opal-data-inf/bronze/orion-api/ --recursive | grep -E "representatives|accounts_v2" | sort | tail -20</run>
      <expect>Most recent bronze date folder visible; representatives/ or accounts_v2/ files present</expect>
      <if_mismatch>If bronze data absent for joe_brandon — check silver/representatives/ or platinum/advisors/joe_brandenburg/summary.json for advisor_id field</if_mismatch>
    </step>
    <step>
      <run>DS~B: aws s3 cp s3://opal-data-inf/platinum/advisors/joe_brandenburg/summary.json /tmp/joe_summary.json; python3 -c "import json; d=json.load(open('/tmp/joe_summary.json')); print(d.get('advisor_id'), d.get('rep_id'), d.get('metadata',{}))"</run>
      <expect>advisor_id field present; if rep_id in summary — use it directly</expect>
      <if_mismatch>If rep_id absent from summary: probe bronze/orion-api/{latest_date}/representatives/ CSV for name matching joe_brandon/joe_brandenburg</if_mismatch>
    </step>
    <step>
      <run>DS~B: once rep_id confirmed — read data/orion/scripts/gold/INF_I_D02b.top_holdings.py and locate ADVISOR_KEY_BY_REP_ID dict</run>
      <expect>Dict has exactly 3 entries currently (rep_ids 3/11/12); add joe_brandenburg's rep_id → 'joe_brandenburg'</expect>
      <if_mismatch>If dict structure differs — adapt accordingly; mapping must produce an advisor_key that matches the platinum/advisors/ path key</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before committing">
    <step>
      <run>DS~B: .tools/ds-commit-gate.sh data/orion/scripts/gold/INF_I_D02b.top_holdings.py</run>
      <expect>Exit 0 — py_compile + AST scanner + ruff all pass</expect>
      <if_mismatch>Fix all errors. Script must have `from __future__ import annotations` as first import.</if_mismatch>
    </step>
    <step>
      <run>DS~B: aws s3 cp data/orion/scripts/gold/INF_I_D02b.top_holdings.py s3://opal-data-inf/code/gold/ &amp;&amp; comp-pipescript deployed INF_I_D02b</run>
      <expect>MATCH — runner has updated script with joe_brandenburg mapping</expect>
      <if_mismatch>Re-upload until MATCH</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after DS~B RAVC3 confirms rep_id + MATCH — AE 0.6.1 step">
    <step>
      <run>AE 0.6.1: verify INF_I_D02b is in the orion-gold-dispatch.sh catalog (or equivalent chain registration). If absent, add it.</run>
      <expect>INF_I_D02b appears in the dispatch catalog before the top_holdings emit step; re-run produces s3://opal-data-inf/platinum/advisors/joe_brandenburg/top_holdings.json</expect>
      <if_mismatch>Add catalog entry per existing INF_I_D02a or INF_I_D02 pattern; Terraform/infra change NOT required — catalog-only addition</if_mismatch>
    </step>
    <step>
      <run>AE 0.6.1: dispatch chain from INF_I_D02b (or targeted re-run of INF_I_D02b only if catalog supports it) on inf-gold-layer-runner</run>
      <expect>platinum/advisors/joe_brandenburg/top_holdings.json exists with ETag newer than dispatch timestamp and len(top_holdings) &gt; 0</expect>
      <if_mismatch>If zero rows: rep_id mapping produced wrong key — loop back to DS~B for re-verification</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>AE 0.6.1: gated on DS~B RAVC3 confirming rep_id identification + INF_I_D02b S3 MATCH. DS~B sends MCP GO to AE 0.6.1 directly once MATCH confirmed.</coord>
    <coord>DS~A: do NOT touch INF_I_D02b — AUDIT-003 scope is DS~B.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">DS~B session log documents joe_brandenbrug rep_id source (S3 path or summary.json field) + evidence (jq output or aws s3 ls line)</criterion>
    <criterion id="AC2">comp-pipescript deployed INF_I_D02b → MATCH before DS~B signals AE</criterion>
    <criterion id="AC3">platinum/advisors/joe_brandenburg/top_holdings.json exists post-chain with ETag newer than AE dispatch + at least 1 holding row</criterion>
    <criterion id="AC4">Session log Compiler Tools section reproduces each &lt;run&gt; + observed result + PASS/FAIL vs &lt;expect&gt;</criterion>
    <criterion id="AC5">RAVC3 from DS~B to COO + RAVC3 from AE 0.6.1 to COO each with commit hash + AC status</criterion>
  </acceptance_criteria>
</task_order>
