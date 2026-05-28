<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-23-valfin-010-inf-c-09-placeholder-filter</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <re_routed_from>0.4.0_DS_ClientPlatform (base)</re_routed_from>
    <re_routed_at>2026-05-23T19:15Z UTC</re_routed_at>
    <re_routed_reason>MSTR v1.5 cycle-2 BOTTLENECK-RESPONSE INTENSIFICATION fired on DS Base 2026-05-23T19:10Z (CY-0044). DS Base STALE 135+ min after dispatch (last commit 87ae43cf8 16:30Z UTC; broker summary stale "Waiting on COO" predates the .010 + .011 + .009 dispatches). Compacted-context-stuck pattern hypothesis. CTO chose toolkit option (c) DS~C re-routing via COO lane-routing-hub authority (a TIER0_LAW + b RD-micro-charter both out-of-scope for gold-script lane per CLAUDE.md Rule 13). COO option (i): direct re-dispatch via this <issued_to> field edit. Original TO content + ACs + compiler mandate UNCHANGED -- only the recipient lane changes.</re_routed_reason>
    <date>2026-05-23</date>
    <status>in_progress</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_VALFIN</project_code>
    <priority>P1 -- CVO LD-0018 F1 finding: placeholder-zero partitions pollute the fee_status_audit; 61% of accounts get wrong `first_known_fee_status_date=2023-05-25` instead of 2026-04-01. One-line filter fix; corrects a real data-correctness defect in the audit output.</priority>
    <sla>~1-2h wall (one-line edit + re-run + comp-validate + RAVC2).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-23T15:14Z UTC. CVO LD-0018 verify-
         channel verdict YELLOW (commit 5cdd5fa7e); F1 P1 finding routed to DS per
         verifier-not-fixer doctrine. Brief partial resolution of DS's original
         Routing Ask #3 (the fee_status_audit half; the fee_rate_history half is
         a separate Orion Advisory Fees ETL gap, not in this TO scope). -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1)</prd>
    <cvo_verdict>org/tier1_exec/3.0.0_SA_CVO/logs/2026-05-23/cvo_loop_1530Z_LD0018_fee_imputation_verdict.md (commit 5cdd5fa7e)</cvo_verdict>
    <source_file>data/orion/scripts/gold/INF_C_09.py (lines 138-144 -- the placeholder-filter site)</source_file>
    <audit_artifact>s3://opal-data-inf/gold/views/fee_status_audit.parquet</audit_artifact>
    <originating_ask>DS Phase-2 RAVC2 (commit c02c9c1ed) Routing Ask #3 -- "INF_C_08 fee billing gap" (partial resolution; this TO addresses the fee_status_audit defect; fee-RATE history gap is separate scope).</originating_ask>
  </references>

  <objective>
    Fix the placeholder-zero filter at INF_C_09.py:138-144 so the `fee_status_audit.parquet` correctly reflects each account's `first_known_fee_status_date`. Current defect: 61% of accounts get the wrong `2023-05-25` (the placeholder-zero partition date) instead of the correct `2026-04-01` (the actual first-known fee-status date). End-state: re-run produces a clean audit; comp-validate INF_C_09 stays exit 0; no other audit columns disturbed.
  </objective>

  <context>
    CVO LD-0018 verify-channel verdict YELLOW identified two distinct mechanisms behind DS's original fee-billing-gap surface:

    (1) **fee-RATE history (INF_C_08 input):** `gold/dimensions/fee_rate_history.parquet` is a 3,566-byte zero-row stub written by DEPRECATED `INF_A_02.fee_rate_history.py`. INF_C_08 correctly zero-stubs `fee_efficiency_score=0.0` + `fee_data_available=False` for all 168 advisors because of this. This is the REAL gap DS surfaced -- needs separate TO when the Orion Advisory Fees feed lands. NOT IN THIS TO SCOPE.

    (2) **fee-STATUS audit (INF_C_09 output):** `gold/views/fee_status_audit.parquet` exists, fresh, scaled, dispatched daily. F1 finding: placeholder-zero partitions written by an earlier ingestion bootstrap pollute the audit -- specifically the 2023-05-25 partition is a placeholder, and 61% of accounts get this date as their `first_known_fee_status_date` instead of the correct 2026-04-01 (actual first-known date). One-line filter fix at INF_C_09.py:138-144 per CVO verdict §F1. THIS IS THE TO SCOPE.

    F2 finding (zero downstream consumers; orphaned publisher) is OUT of this TO scope -- architectural decision routes to CTO separately (wire consumer / park publisher / Phase-2-staged decision).
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- INF_C_09.py one-line filter fix.
        - Per CVO verdict §F1: filter out the 2023-05-25 placeholder-zero partition at the source-data load step (lines 138-144). Specific filter shape per CVO's verdict file.
        - No other INF_C_09 logic touched; scope-creep guard.

      DELIVERABLE B -- Re-run + verify.
        - Safe-deploy cycle per CLAUDE.md Rule 13.
        - Re-run INF_C_09 against current data.
        - Sentinel verify: 5-10 sample accounts that previously had `first_known_fee_status_date=2023-05-25` now show `2026-04-01` (or whatever the correct empirical date is per CVO verdict).
        - Sentinel verify: 5-10 accounts that were correct (had `2026-04-01` originally) STILL show that date (no regression).
        - Coverage check: 61% wrong → 0% wrong post-fix.

      DELIVERABLE C -- comp-validate INF_C_09.
        - Exit 0 against the corrected output.
        - If comp-validate gate doesn't exist for INF_C_09 (the gold_validate_config gap class), document in session log; the .009 sibling TO is handling INF_D_02 config; pattern may apply here too.

      DELIVERABLE D -- RAVC2 to COO + CC CVO.
        - All evidence (commit + sentinel verify table + comp-validate output).
        - Closes the F1 portion of LD-0018 verdict.
    </in_scope>
    <out_of_scope>
      - F2 architectural decision (wire consumer vs park publisher vs Phase-2-staged) -- routed to CTO.
      - The fee-RATE history gap (Orion Advisory Fees feed not loaded) -- separate future TO.
      - Other INF_C_09 logic changes beyond the line-138-144 filter -- scope-creep guard.
      - INF_C_08 changes -- it's correctly behaving per spec given the zero-row fee_rate_history input.
      - INF_A_02 changes (deprecated; deletion is a separate cleanup TO if pursued).
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform.
    No cross-lane coord needed -- INF_C_09 is in DS pod-4's owned-paths lane.
    CC CVO on RAVC2 (they raised the finding; will validate the F1 portion of LD-0018 closes).
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_C_09</run>
        <expect>READS includes the placeholder-source path being filtered; WRITES includes gold/views/fee_status_audit.parquet. No COLUMN GAPS.</expect>
        <if_mismatch>STOP. If a COLUMN GAP surfaces, the filter logic may need a downstream re-derive.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_09.py</run>
        <expect>Exit 0. py_compile + AST + ruff all PASS.</expect>
        <if_mismatch>STOP. Investigate gate failure before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/safe-deploy.sh (per CLAUDE.md Rule 13)</run>
        <expect>Push -> S3 upload -> comp-pipescript deployed INF_C_09 MATCH -> SSM dispatch INF_C_09.</expect>
        <if_mismatch>STOP. Investigate deployed-vs-committed drift.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/gold/views/fee_status_audit.parquet /tmp/fs_audit.parquet + parquet inspect 5-10 sample accounts</run>
        <expect>Previously-wrong accounts now show the correct date (2026-04-01 or per CVO verdict); previously-correct accounts unchanged.</expect>
        <if_mismatch>STOP. Filter may have over- or under-filtered; investigate before declaring AC1 PASS.</if_mismatch>
      </step>
      <step>
        <run>comp-validate INF_C_09 (if config exists)</run>
        <expect>Exit 0 OR config-doesn't-exist documented with reasoning in session log.</expect>
        <if_mismatch>Address per the validate config OR escalate to COO if a real defect surfaces.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">INF_C_09.py:138-144 one-line filter fix lands; no other logic touched.</ac>
    <ac id="AC2">Re-run + sentinel verify: 5-10 previously-wrong accounts now correct; 5-10 previously-correct accounts unchanged (no regression).</ac>
    <ac id="AC3">Coverage check: post-fix audit shows 0% accounts with the wrong placeholder-zero date (down from 61%).</ac>
    <ac id="AC4">comp-validate INF_C_09 exits 0 OR config-doesn't-exist documented with reasoning.</ac>
    <ac id="AC5">safe-deploy cycle clean: comp-pipescript deployed INF_C_09 MATCH on origin/CLOUD.</ac>
    <ac id="AC6">Session log Compiler Tools section reproduces every &lt;run&gt; with observed output + pass/fail vs. &lt;expect&gt;.</ac>
    <ac id="AC7">RAVC2 to COO + CC CVO with all evidence; closes F1 portion of LD-0018 verdict.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Editing INF_C_09 beyond the line-138-144 filter (scope-creep guard).
    - Touching INF_C_08 (correct per spec; F1 is INF_C_09 only).
    - Touching INF_A_02 (deprecated; deletion is a separate cleanup TO if pursued).
    - Touching fee_rate_history.parquet writes (separate Orion Advisory Fees feed scope).
    - Acceptance flex on AC2/AC3 (sentinel verify + coverage check are the empirical gates).
  </not_authorized>
</task_order>
