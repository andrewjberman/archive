<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.JOE-TXN-BACKFILL</id>
    <project>ADVI_INFNNA</project>
    <title>Historical transactions bronze re-pull with corrected INFLECTION_REP_IDS="3,6,11,12" filter — populate Joe Brandenburg's true NNA values</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~30-60 min wall-clock</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_ravc">DS~C FOLLOWUP-2 RAVC2 `148bb2097` 2026-05-08T~16:00Z — diagnosis (c): historical bronze NEVER had rep_id=6 because pre-INFNNA.001 puller filter excluded Joe</ref>
    <ref type="puller_fix">DS~A `e2edbe321` 2026-05-08 — pull_inflection_transactions_v2.py:71 INFLECTION_REP_IDS = "3,6,11,12" (was "3,11,12"). Live; correctly pulls Joe go-forward.</ref>
    <ref type="empirical_evidence">silver/transactions/ FULL SCAN across 1504 partitions = 0 rep_id=6 rows. Pre-INFNNA.001 puller filter `@RepIDs="3,11,12"` excluded Joe from ALL historical Orion pulls. 2026-05-07 transactions.csv shows rep_ids = [11, 12] only.</ref>
    <ref type="proven_pattern">DS~A perf backfill `b6w6bucc3` 2026-05-08T~16:17Z — same 64-worker `local_silver_backfill.py` pattern; 50min wall / 1987 OK / 97.4% — 10x speedup over sequential</ref>
  </references>

  <context>
    Joe Brandenburg (rep_id=6) was excluded from all historical Orion transaction pulls before INFNNA.001 fix `e2edbe321` shipped today. As a result:
    - silver/transactions/ has 0 rep_id=6 rows across 1504 partitions
    - canonical_nna has 0 rep_id=6 rows (since INF_C_01 reads silver/transactions)
    - leaderboard.json shows Joe NNA = $0 across QTD/YTD/MAX windows — **artifactual, not actual**
    - Joe's TRUE NNA values are unknown until historical bronze is re-pulled with corrected filter

    **Goal:** re-pull historical transactions bronze with corrected `INFLECTION_REP_IDS="3,6,11,12"` filter. Re-build silver/transactions/. Re-run INF_C_01 → INF_D_00c → INF_D_04 cascade. Trigger DT CF invalidation. Joe's leaderboard NNA columns populate with real values.

    **Pattern:** identical to today's perf backfill — same `local_silver_backfill.py` driver, 64 workers, same skip-existing semantics. Add `transactions` dim to DIMS config (or repurpose existing entry); fire across historical date range.

    **Expected outcome:** Joe's QTD/YTD/MAX NNA columns transition from $0 to real values (could be material — Joe's accounts have ~$14M existing; some material contribution/distribution flow over the historical window is plausible).

    **Side effect — silver re-write:** existing silver/transactions/ partitions will be OVERWRITTEN with the corrected-filter data (which now includes Joe's rows in addition to Patrick + Peter). This is the desired idempotent state.
  </context>

  <scope>
    <step>
      Verify current puller code: `pull_inflection_transactions_v2.py:71` should have `INFLECTION_REP_IDS = "3,6,11,12"` (post-`e2edbe321`). Cross-check before firing.
    </step>

    <step>
      Determine date range:
      - Lower bound: same as perf backfill (2020-03-11) OR Joe's account-active start (whichever is later — Joe likely doesn't predate firm onboarding). Use conservative lower bound 2020-03-11 to match perf coverage.
      - Upper bound: 2026-05-07 (T-1; 2026-05-08 transactions land tomorrow per cron)
    </step>

    <step>
      Add `transactions` dim to `local_silver_backfill.py` DIMS config (or modify existing entry):
      - script: `pull_inflection_transactions_v2.py --start-date {date} --end-date {date} --upload-bronze`
      - bronze_key: `bronze/orion-api/{date}/transactions.csv`
      - silver_key: `silver/transactions/{date}.parquet`
      - silver builder: `convert_transactions_to_silver.py` (or whichever canonical path)
      - skip-existing: **OFF** (we want to OVERWRITE existing silver — current data is missing rep_id=6)
      - --no-require-bronze: ON (this is bronze pull + silver build chained)
      - timeout: 240s/pull (matches perf pattern)
    </step>

    <step>
      Pre-commit gate on the driver edit: `.tools/ds-commit-gate.sh .runtmp/local_silver_backfill.py`
    </step>

    <step>
      Fire run:
      ```
      python .runtmp/local_silver_backfill.py \
        --from 2020-03-11 --to 2026-05-07 \
        --dims transactions \
        --workers 64 \
        --no-require-bronze \
        --no-skip-existing
      ```
      Expected wall-clock: 30-60min (transactions dim is heavier per-call than perf — payload includes all account transactions per snapshot, can be MB-scale per date).
    </step>

    <step>
      Re-run cascade for affected date range (or just current date if Lambda chain handles incrementals):
      - `INF_C_01.canonical_nna.py --start-date 2020-03-11 --end-date 2026-05-07 --upload`
      - `INF_D_00c.advisor_metrics.py` (cascade trigger)
      - `INF_D_04.build_dashboard.py` (cascade trigger)

      Or: trigger inf-silver-chain Lambda via S3 event + let aggregator fire.

      DS~A choice on cascade dispatch path; whatever's fastest to ship platinum updates.
    </step>

    <step>
      Verify Joe NNA values post-cascade:
      ```
      aws s3 cp s3://opal-data-inf/platinum/firm/leaderboard.json /tmp/lb_post.json
      python -c "import json; d=json.load(open('/tmp/lb_post.json')); joe=[a for a in d.get('advisors',[]) if 'brandenburg' in a.get('advisor_name','').lower()]; print('joe_nna_qtd:', joe[0].get('nna_qtd', 'MISSING'), 'ytd:', joe[0].get('nna_ytd'), 'max:', joe[0].get('nna_max'))"
      ```
      Expected: at least one of QTD/YTD/MAX shifts from $0 to non-zero.
    </step>

    <step>
      Trigger DT 0.4 CF invalidation on `/api/scoped/advisor-intelligence/platinum/firm/leaderboard.json` + `/nmec_nmnc_nna.json` + `/advisors/joe_brandenburg/summary.json` (single wildcard `/platinum/*` works per DT's earlier optimization).

      RAVC2 to COO with: backfill stats + Joe's pre/post NNA values + DT invalidation ID.
    </step>
  </scope>

  <acceptance_criteria>
    1. Puller pre-flight verified: `pull_inflection_transactions_v2.py:71` has corrected `"3,6,11,12"` filter.
    2. local_silver_backfill.py driver updated with transactions dim entry; pre-commit gate PASS.
    3. Bronze + silver re-pull completes; ≥95% OK rate (matches perf backfill outcome at same scale).
    4. silver/transactions/ partitions now contain rep_id=6 rows (verify via parquet read on a sample date).
    5. Cascade re-run completes; canonical_nna_*.parquet has rep_id=6 entries (verify via parquet read).
    6. leaderboard.json post-cascade: Joe Brandenburg row shows non-zero NNA in at least one of QTD/YTD/MAX (or documented zero-flow with empirical evidence).
    7. DT CF invalidation triggered; ID captured.
    8. Session log Compiler Tools section reproduces each `<run>` with observed output + pass/fail.
    9. RAVC2 to COO with: wall-clock, OK/fail counts, frontier dates, Joe pre/post NNA values, DT invalidation ID.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n "INFLECTION_REP_IDS" data/orion/manual_api/pull_inflection_transactions_v2.py | head -3</run>
        <expect>Line 71 shows `INFLECTION_REP_IDS = "3,6,11,12"` (post-`e2edbe321`).</expect>
        <if_mismatch>If still old "3,11,12": stop. e2edbe321 didn't propagate; surface to COO.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/silver/transactions/2026-05-07.parquet /tmp/txn_pre.parquet 2>&amp;1 &amp;&amp; python -c "import pandas as pd; df=pd.read_parquet('/tmp/txn_pre.parquet'); print('rep_id_6_rows:', (df['rep_id']==6).sum() if 'rep_id' in df else 'no rep_id col'); print('unique rep_ids:', df['rep_id'].unique() if 'rep_id' in df else 'n/a')"</run>
        <expect>rep_id_6_rows = 0 (confirms pre-fix gap). unique rep_ids likely [11, 12].</expect>
        <if_mismatch>If rep_id_6_rows &gt; 0: bronze already has Joe; backfill may be unnecessary. Verify before firing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 cp s3://opal-data-inf/silver/transactions/2026-05-07.parquet /tmp/txn_post.parquet &amp;&amp; python -c "import pandas as pd; df=pd.read_parquet('/tmp/txn_post.parquet'); print('rep_id_6_rows:', (df['rep_id']==6).sum())"</run>
        <expect>rep_id_6_rows &gt; 0 (Joe rows now present in silver post-backfill).</expect>
        <if_mismatch>If still 0: backfill didn't propagate; debug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      MAJOR: silver/transactions/ for ~2050 historical dates will be OVERWRITTEN with corrected-filter data. This is the desired idempotent state.

      Cascade re-run for affected dates: INF_C_01 → INF_D_00c → INF_D_04 → DT CF invalidation.

      Net effect: leaderboard.json + nmec_nmnc_nna.json + per-advisor summary.json all re-emitted with Joe's true NNA flow data. Production data correctness improvement.
    </reprocess_required>
  </data_reprocess_scope>

  <dependencies>
    None blocking. Mirrors perf backfill pattern (just shipped clean). Parallel-dispatchable with any other in-flight work.
  </dependencies>
</task_order>
