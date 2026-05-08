<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.GOLD-FOLLOWUP-2</id>
    <project>ADVI_INFNNA</project>
    <title>Joe Brandenburg NNA = $0 across QTD/YTD/MAX windows — investigate canonical_nna activity-category mapping for rep_id=6</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~30-45 min</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_ravc">DS~A RAVC5 INFNNA.GOLD cascade close 20260508T~14:46Z — AC5 caveat</ref>
    <ref type="empirical_evidence">platinum/firm/leaderboard.json: Joe Brandenburg row NNA QTD = $0; YTD = $0; MAX = $0. Patrick and Peter both have non-zero NNA values in same windows.</ref>
    <ref type="hypothesis">Either (a) Joe's transactions are not classified as Contributions/Distributions in INF_C_01's Activity Category map (the only categories that count as NNA), OR (b) Joe's accounts genuinely had zero net new assets in the windows (possible — he's a relatively recent advisor), OR (c) rep_id=6 path in INF_C_01 has a filter that drops his rows.</ref>
    <ref type="related_script">data/orion/scripts/gold/INF_C_01.canonical_nna.py (lines ~75 EXCLUDED_CATEGORIES; lines ~253 NNA filter)</ref>
  </references>

  <context>
    INFNNA.GOLD cascade shipped 2026-05-08. Joe Brandenburg correctly attributed in firm AUA + leaderboard existing column ($14.0M existing) + advisor summary. BUT NNA fields all $0 across QTD/YTD/MAX windows.

    Three possible root causes (per DS~A RAVC5):
    1. **Activity Category misclassification:** INF_C_01 EXCLUDED_CATEGORIES filters out 'Exchange In/Out', 'Journal In/Out', 'Merge In/Out', 'Advisory Fees Paid', 'Dividends and Interest', 'Net Dividends/Interest/Gains Withdrawn'. Only 'Contributions' + 'Distributions' (or similar) count as NNA. If Joe's transactions are categorized differently in Orion, his NNA = $0.
    2. **Genuine zero NNA:** Joe is a recent advisor; his accounts may genuinely have zero contributions/distributions in QTD/YTD windows. Plausible.
    3. **Per-rep_id filter bug:** INF_C_01 may have a filter or join that drops rep_id=6 rows. Less likely (firm AUA + existing show Joe correctly).

    **Goal:** determine which of (1)/(2)/(3) is the cause. If (1) or (3): fix INF_C_01 + re-run cascade. If (2): document as expected + close TO without code change.

    Non-blocking for portal display. NNA = $0 will simply show as zero in leaderboard NNA columns; legitimate state if (2).
  </context>

  <scope>
    <step>
      Read canonical_nna_*.parquet for rep_id=6 rows. Aggregate by Activity Category. Verify:
      - Total transaction count for rep_id=6
      - Activity Category distribution
      - Net flow (sum of amounts) for non-EXCLUDED_CATEGORIES
    </step>

    <step>
      If non-zero net flow exists: bug is downstream. Trace through INF_D_00c (advisor metrics) NNA aggregation logic. Find where it drops Joe.
    </step>

    <step>
      If zero net flow but non-empty rows: check whether Joe's transactions are all in EXCLUDED_CATEGORIES (e.g., all "Dividends" or "Advisory Fees" — which would make $0 NNA correct).
    </step>

    <step>
      If zero rows entirely: rep_id=6 not flowing through INF_C_01. Trace upstream to silver/transactions and the rep_id mapping in INF_C_01.
    </step>

    <step>
      **Diagnosis branch (a):** if (1) Activity Category miscategorization (Joe's contributions classified wrongly): fix INF_C_01 categorization. Pre-commit gate. Re-run cascade for affected partition dates.

      **Diagnosis branch (b):** if (2) genuine zero NNA: document in TO close-out + leaderboard.json comments; no code change. Joe's $0 NNA is correct legitimate state.

      **Diagnosis branch (c):** if (3) per-rep_id filter drops Joe: fix filter + re-run cascade.
    </step>

    <step>
      Commit + push (if code change). RAVC2 to COO with: diagnosis verdict (a/b/c), evidence (row counts, category distribution), commit SHA + cascade re-run results if applicable.
    </step>
  </scope>

  <acceptance_criteria>
    1. canonical_nna_*.parquet read for rep_id=6 rows + Activity Category distribution captured.
    2. Diagnosis verdict reached: (a) miscategorization, (b) genuine $0, or (c) filter bug.
    3. If (a) or (c): minimal-fix patch + pre-commit gate PASS + cascade re-run for affected partition.
    4. If (b): TO closes with documentation; no code change.
    5. Session log Compiler Tools section reproduces each `<run>` with observed output + pass/fail vs `<expect>`.
    6. RAVC2 to COO with: verdict + evidence + commit SHA (if applicable) + post-fix Joe NNA values (if applicable).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws s3 cp s3://opal-data-inf/gold/canonical/canonical_nna_2026-04-28.parquet /tmp/cnna_joe.parquet &amp;&amp; python -c "import pandas as pd; df=pd.read_parquet('/tmp/cnna_joe.parquet'); joe=df[df['rep_id']==6] if 'rep_id' in df.columns else df.iloc[0:0]; print(f'joe_rows={len(joe)}'); print(joe.groupby('activity_category')['amount'].agg(['count','sum']).head(20) if 'activity_category' in joe.columns and len(joe)&gt;0 else 'no joe rows or no activity_category col')"</run>
        <expect>joe_rows &gt; 0 + activity_category distribution visible. If joe_rows = 0, upstream bug.</expect>
        <if_mismatch>If joe_rows = 0: trace silver/transactions for rep_id=6; surface to COO if structural.</if_mismatch>
      </step>
      <step>
        <run>grep -n "EXCLUDED_CATEGORIES" data/orion/scripts/gold/INF_C_01.canonical_nna.py | head -5</run>
        <expect>Returns line 75 EXCLUDED_CATEGORIES frozenset definition. Confirms which Activity Categories are filtered.</expect>
        <if_mismatch>If 0 results: file path wrong; verify with `find data/orion/scripts/gold/ -name 'INF_C_01*'`.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 cp s3://opal-data-inf/platinum/firm/leaderboard.json /tmp/lb_post.json &amp;&amp; python -c "import json; d=json.load(open('/tmp/lb_post.json')); joe=[a for a in d.get('advisors',[]) if 'brandenburg' in a.get('advisor_name','').lower()]; print('joe_nna_qtd:', joe[0].get('nna_qtd', 'MISSING') if joe else 'JOE_NOT_FOUND')"</run>
        <expect>If diagnosis was (a) or (c): Joe nna_qtd is non-zero. If (b): nna_qtd = $0 documented as expected.</expect>
        <if_mismatch>If diagnosis (b) and value still $0: that's correct/expected. If (a)/(c) and still $0: fix incomplete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      Conditional on diagnosis: if (a) or (c), re-run INF_C_01 + INF_D_00c + INF_D_04 cascade for current partition; upload platinum/firm/leaderboard.json + nmec_nmnc_nna.json + advisor summaries. Trigger DT CF invalidation.

      If (b) genuine zero: no reprocessing; documentation-only close.
    </reprocess_required>
  </data_reprocess_scope>

  <dependencies>
    None. Parallel-dispatchable with FOLLOWUP-1 (DS~B) + Tax saved-query repair (DS~D).
  </dependencies>
</task_order>
