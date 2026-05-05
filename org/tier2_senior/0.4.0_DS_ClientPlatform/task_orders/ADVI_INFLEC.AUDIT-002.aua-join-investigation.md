<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-002</id>
    <project>ADVI_INFLEC</project>
    <title>AUA-join upstream investigation — activity_scan / cash_drag / concentration_risk (3 RED cells)</title>
    <issued_to>0.4.0_DS_ClientPlatform~D (primary) + 0.5.0_AE_OpalETL (cross-ref if chain re-run needed)</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- COMPLETE 2026-05-05: 4-step pricing fix executed by DS~D. activity_scan/cash_drag/concentration_risk all GREEN. DS~D RAVC5 7c936826a. Root cause: canonical_prices.parquet stale since 2026-04-22; rebuilt through 2026-05-05. -->
    <priority>high</priority>
    <estimated_effort>0.5d diagnosis; 0.5-1d fix if single root cause</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">ADVI_INFLEC.md (Phase 2)</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v3 — 3 RED cells: activity_scan AUA=0, cash_drag AUA=0, concentration_risk EMPTY []</ref>
    <ref type="ae_lambda_emit">docs/architecture/_drafts/INFLEC_AUDIT_AE_LAMBDA_EMIT.md — empirical AE 0.5 sampling: 307 rows activity_scan ALL AUA=0; 295 rows cash_drag ALL AUA=0/cash_pct=0; concentration_risk 2B=[]</ref>
    <ref type="compiler_evidence">comp-pipescript io INF_D_05 → reads gold/dimensions/accounts_dimension_latest.parquet; comp-pipescript io INF_D_06 → same read; comp-pipescript io INF_D_07 → reads silver/accounts_dim/latest.parquet</ref>
    <ref type="cto_ruling">CTO RAVC3 2026-05-05: bundle into single TO; if single root cause → 1 fix lands 3 cells GREEN; if divergent → split 002a/002b</ref>
  </references>

  <context>
    AE 0.5 Lambda emit audit found three INFLEC-only platinum artifacts with zero/empty AUA:
    - platinum/firm/activity_scan.json: 307 rows, ALL AUA=0 (INF_D_05 source)
    - platinum/firm/cash_drag.json: 295 rows, ALL AUA=0, ALL cash_pct=0 (INF_D_06 source)
    - platinum/firm/concentration_risk.json: 2 bytes = [] EMPTY (INF_D_07 source)

    Compiler graph shows INF_D_05 and INF_D_06 both read gold/dimensions/accounts_dimension_latest.parquet
    as their sole input. INF_D_07 reads silver/accounts_dim/latest.parquet (different source).

    CTO hypothesis: cross-cutting AUA-join gap — these scripts may source AUA from an artifact
    that doesn't contain valid AUA data for Inflection, OR the join key between accounts and
    the AUA dimension is failing silently.

    Single-root-cause ruling: if confirmed, one fix resolves all 3 cells. If divergent, split
    into AUDIT-002a (INF_D_05/06) + AUDIT-002b (INF_D_07) as separate sub-TOs.
  </context>

  <phase id="0" when="before any read or write — discovery">
    <step>
      <run>comp-pipescript io INF_D_05</run>
      <expect>READS: gold/dimensions/accounts_dimension_latest.parquet — confirm single read source</expect>
      <if_mismatch>Update TO scope with actual read sources before proceeding</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_06</run>
      <expect>READS: gold/dimensions/accounts_dimension_latest.parquet — same source as INF_D_05</expect>
      <if_mismatch>If read sources differ between D_05/D_06, document both and trace independently</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_07</run>
      <expect>READS: silver/accounts_dim/latest.parquet — different source from D_05/D_06</expect>
      <if_mismatch>If same source as D_05/D_06, single root cause more likely</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="before writing any fix">
    <step>
      <run>S3 read: aws s3 cp s3://opal-data-inf/gold/dimensions/accounts_dimension_latest.parquet /tmp/accounts_dim.parquet; python3 -c "import pandas as pd; df=pd.read_parquet('/tmp/accounts_dim.parquet'); print(df.columns.tolist()); print(df.dtypes); print(df[['aua','fee_earning_aua','market_value']].head(5) if 'aua' in df.columns else 'NO AUA FIELD'); print(len(df))"</run>
      <expect>Parquet loads; AUA-related column present (aua, market_value, or fee_earning_aua); values non-zero for at least some rows</expect>
      <if_mismatch>If AUA column absent → root cause is INF_D_05/06 reading wrong artifact (no AUA field); fix = point scripts to canonical holdings. If column present but all zero → AUA computation upstream gap; trace INF_D_00c or B_00 canonical holdings feed to accounts_dimension_latest</if_mismatch>
    </step>
    <step>
      <run>Read data/orion/scripts/gold/INF_D_05.activity_scan.py — identify the AUA field name being read from accounts_dimension_latest.parquet and the join/merge key used</run>
      <expect>Explicit column name dereference visible; join key is advisor_key or rep_id or account_id</expect>
      <if_mismatch>If field name mismatch vs actual parquet columns → fix is rename/alias in script</if_mismatch>
    </step>
    <step>
      <run>Same read for INF_D_06.cash_drag.py and INF_D_07.concentration_risk.py — document AUA field name and join key per script</run>
      <expect>If same field name as D_05 → same fix applies to all three. If D_07 diverges → split scope.</expect>
      <if_mismatch>Document divergence and author separate AUDIT-002b scope for D_07</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_05 (re-run after diagnosis to confirm no COLUMN GAPS missed)</run>
      <expect>COLUMN GAPS section: either empty (all columns present in load list) or lists the missing AUA column explicitly</expect>
      <if_mismatch>If COLUMN GAPS lists AUA column → confirms the fix needed; add to load list</if_mismatch>
    </step>
    <step>
      <run>Verdict: single-root-cause YES or NO? Document in session log under ## Root Cause Verdict</run>
      <expect>One of: A) Wrong artifact sourced (no AUA field) | B) Column name mismatch | C) Join key failure | D) Expected zero (by design — Inflection has no fee AUA in that dimension)</expect>
      <if_mismatch>N/A — this step produces the verdict, not validates it</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before committing any fix code">
    <step>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_05.activity_scan.py data/orion/scripts/gold/INF_D_06.cash_drag.py data/orion/scripts/gold/INF_D_07.concentration_risk.py</run>
      <expect>Exit 0 — py_compile + AST undefined-name scanner + ruff all pass</expect>
      <if_mismatch>Fix all errors before committing. Zero tolerance on import errors or undefined names.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed INF_D_05</run>
      <expect>MATCH — runner has your fixed code</expect>
      <if_mismatch>Upload to S3 before AE dispatch</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after chain re-run (AE dispatches chain from INF_D_05 forward)">
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/activity_scan.json /tmp/activity_scan.json; python3 -c "import json; d=json.load(open('/tmp/activity_scan.json')); rows=[r for r in d if r.get('aua',0)!=0]; print(f'{len(rows)}/{len(d)} rows have non-zero AUA')"</run>
      <expect>At least some rows with non-zero AUA (count &gt; 0); zero-row result still RED</expect>
      <if_mismatch>Root cause not fully resolved — escalate to COO with updated trace before closing</if_mismatch>
    </step>
    <step>
      <run>Same spot-check for cash_drag.json (cash_pct non-zero rows) and concentration_risk.json (len &gt; 0)</run>
      <expect>cash_drag: non-zero cash_pct rows present; concentration_risk: array length &gt; 0</expect>
      <if_mismatch>Partial fix — document which scripts still need attention and escalate</if_mismatch>
    </step>
  </phase>

  <bifurcation_protocol>
    If Phase 1 verdict = divergent (D_07 different root cause from D_05/D_06):
    - Author AUDIT-002a scoped to INF_D_05/06 fix (single commit)
    - Author AUDIT-002b scoped to INF_D_07 fix (separate commit)
    - Close this TO (AUDIT-002) as "split per bifurcation protocol" in the status comment
    - MCP COO immediately with split decision and rationale
  </bifurcation_protocol>

  <cross_domain_coordination>
    <coord>AE 0.5: if fix requires chain re-run from INF_D_05 forward, AE 0.5 dispatches on inf-gold-layer-runner. DS~D provides: S3-uploaded fixed scripts + comp-pipescript deployed MATCH confirmation + MCP GO to AE 0.5.</coord>
    <coord>DS~A: do NOT touch INF_D_05/06/07 — AUDIT-002 scope is DS~D's. DS~A is on AUDIT-005/006.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Root cause verdict documented in session log under ## Root Cause Verdict with evidence (S3 parquet inspection output, script read line citations, column name comparison)</criterion>
    <criterion id="AC2">If fix shipped: comp-pipescript deployed MATCH on all 3 scripts before signaling AE</criterion>
    <criterion id="AC3">If fix shipped: post-chain spot-check shows at least some non-zero AUA in activity_scan.json AND non-zero cash_pct in cash_drag.json AND non-empty array in concentration_risk.json</criterion>
    <criterion id="AC4">Session log Compiler Tools section reproduces each &lt;run&gt; + observed result + PASS/FAIL vs &lt;expect&gt;</criterion>
    <criterion id="AC5">RAVC3 to COO with commit hash(es) + AC1-4 status. If bifurcation: include split rationale and new sub-TO IDs.</criterion>
  </acceptance_criteria>
</task_order>
