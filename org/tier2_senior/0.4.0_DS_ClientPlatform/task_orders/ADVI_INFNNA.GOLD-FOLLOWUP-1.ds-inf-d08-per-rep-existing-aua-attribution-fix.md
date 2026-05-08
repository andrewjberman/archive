<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.GOLD-FOLLOWUP-1</id>
    <project>ADVI_INFNNA</project>
    <title>INF_D_08 per-rep_id existing_aua + existing_count attribution bug — Joe + IWM rows show $0 / count=0 despite firm totals correct</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status>
    <completed_date>2026-05-08</completed_date>
    <evidence>commit 5a2d87027 — INF_D_08 existing_aua switched to accounts_v2 silver; ETag 2cbb4e836558cb23c69ff117dde3c053; all 4 advisors non-zero; RAVC2 delivered 20260508T160848Z.</evidence>
    <priority>medium</priority>
    <estimated_effort>~30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_ravc">DS~A RAVC5 INFNNA.GOLD cascade close 20260508T~14:46Z — AC3 caveat</ref>
    <ref type="empirical_evidence">platinum/firm/nmec_nmnc_nna.json (1511B / ETag d3578a5a1e8dd0a43721dd8c9252b292 / 14:42:51Z): Joe + IWM advisors[].existing_count=0, existing_aua=$0; firm totals correct ($203.2M / 305 HH; firm existing_aua=$36M)</ref>
    <ref type="affected_script">data/orion/scripts/gold/INF_D_08.* (NMEC/NMNC/NNA derivation)</ref>
  </references>

  <context>
    INFNNA.GOLD cascade shipped 2026-05-08 (DS~A `2ac4f26c1`). Joe Brandenburg + IWM correctly attributed in canonical_nna + leaderboard ($16.2M Joe / 21 clients). However, per-advisor rollup in `nmec_nmnc_nna.json` shows `existing_aua` and `existing_count` both = $0 / 0 for Joe AND IWM — but Patrick + Peter rows DO get values.

    **Firm-level totals are correct** ($203.2M total AUA / 305 HH / firm existing_aua=$36M). The bug is in the per-rep_id rollup split: probably a `groupby(rep_id).agg(...)` that's keying on something other than canonical rep_id (e.g., advisor_name vs rep_id mismatch), OR a join that drops Joe + IWM via filter.

    Hypothesis: INF_D_08 has a per-advisor projection that uses rep_id=6 in some places and a different identifier (advisor_key, advisor_name) in others; one path matches all 4 advisors, the other matches only Patrick + Peter. Investigate via spot-check + diff.

    **Non-blocking for portal:** leaderboard.json + per-advisor summary.json are the primary portal consumers; both correct. nmec_nmnc_nna.json is consumed by [check downstream — likely AUM-by-advisor cards on dashboard].
  </context>

  <scope>
    <step>
      Read INF_D_08 source: identify the function that produces `advisors[]` array in nmec_nmnc_nna.json. Trace existing_aua + existing_count derivation.
    </step>

    <step>
      Spot-check input data: read canonical_nna_*.parquet for rep_id=6 (Joe) — confirm rows present with non-zero existing_aua values. If absent: bug is upstream in INF_D_08's input projection. If present: bug is in INF_D_08's per-advisor rollup logic.
    </step>

    <step>
      Diff Patrick (rep_id=11 or 12) row construction vs Joe (rep_id=6) row construction in code. Identify the divergent path (groupby key mismatch, filter that drops Joe, advisor_name vs rep_id confusion, etc).
    </step>

    <step>
      Apply minimal fix. Likely shape:
      - If groupby on advisor_name: switch to rep_id (canonical key per AUDIT-003 + INFNNA.001 pattern)
      - If filter that excludes Joe/IWM: extend to include rep_ids {6, IWM-mapped}
      - If join that drops rows: add fallback or fix join condition

      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_08.*.py`
    </step>

    <step>
      Re-run INF_D_08 against current canonical_nna data. Verify output:
      - All 4 advisors have non-zero existing_count
      - Sum of advisors[].existing_aua matches firm existing_aua = $36M (within tolerance)
      - Joe row: existing_count > 0; existing_aua > $0 (likely ~$14M based on leaderboard existing column)
      - IWM row: existing_count > 0; existing_aua > $0 (likely ~$1.7M)
    </step>

    <step>
      Upload corrected nmec_nmnc_nna.json to platinum prefix. Capture ETag.

      Trigger DT 0.4 CF invalidation on `/api/scoped/advisor-intelligence/platinum/firm/nmec_nmnc_nna.json` (single-file invalidation, low cost).
    </step>

    <step>
      Commit + push. RAVC2 to COO with: SHA, ETag, before/after row spot-check (Joe/Patrick/Peter/IWM).
    </step>
  </scope>

  <acceptance_criteria>
    1. INF_D_08 source identified + minimal-fix patch landed.
    2. Pre-commit gate (`.tools/ds-commit-gate.sh`) PASS.
    3. nmec_nmnc_nna.json regenerated with all 4 advisors[].existing_count > 0 + existing_aua > 0.
    4. Sum of advisors[].existing_aua matches firm existing_aua ~$36M (within 1% tolerance).
    5. Joe row: existing_aua approximately matches leaderboard's "Existing" column ($14.0M).
    6. ETag captured; CF invalidation routed to DT.
    7. Session log Compiler Tools section reproduces each `<run>` with observed output + pass/fail.
    8. RAVC2 with: commit SHA, ETag, before/after spot-check table for all 4 advisors.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_D_08</run>
        <expect>READS includes canonical_nna; WRITES includes nmec_nmnc_nna.json. No COLUMN GAPS on rep_id field.</expect>
        <if_mismatch>If rep_id missing from READS column list: that's the bug — fix the load list. If WRITES doesn't include nmec_nmnc_nna.json: script identification wrong; surface to COO.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/gold/canonical/canonical_nna_2026-04-28.parquet /tmp/cnna_test.parquet 2>&amp;1 && python -c "import pandas as pd; df=pd.read_parquet('/tmp/cnna_test.parquet'); print('rep_id_6_rows:', (df['rep_id']==6).sum() if 'rep_id' in df else 'rep_id_NOT_in_columns'); print('cols:', df.columns.tolist()[:20])"</run>
        <expect>rep_id_6 rows &gt; 0 (Joe present in canonical_nna). Confirms input data has Joe; bug is downstream in INF_D_08.</expect>
        <if_mismatch>If rep_id_6 = 0 OR rep_id not in columns: bug is upstream (INF_C_01 / silver) NOT INF_D_08; surface to COO before patching.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 cp s3://opal-data-inf/platinum/firm/nmec_nmnc_nna.json /tmp/nmec_post.json &amp;&amp; python -c "import json; d=json.load(open('/tmp/nmec_post.json')); [print(a['advisor_name'], 'count=', a.get('existing_count', 'MISSING'), 'aua=$', f\"{a.get('existing_aua', 0):,.0f}\") for a in d.get('advisors', [])]"</run>
        <expect>All 4 advisors print non-zero existing_count + non-zero existing_aua. Joe row ~$14M.</expect>
        <if_mismatch>If still $0 for Joe: fix incomplete. If existing_count is non-zero but existing_aua is $0 (or vice versa): partial fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      Phase 3 step: re-run INF_D_08 against current canonical_nna; upload corrected platinum/firm/nmec_nmnc_nna.json. Single-file scope; downstream invalidation via DT.
    </reprocess_required>
  </data_reprocess_scope>

  <dependencies>
    None. canonical_nna is current (DS~A `2ac4f26c1` 2026-05-08). Parallel-dispatchable with FOLLOWUP-2 (DS~C) + Tax saved-query repair (DS~D) + perf backfill.
  </dependencies>
</task_order>
