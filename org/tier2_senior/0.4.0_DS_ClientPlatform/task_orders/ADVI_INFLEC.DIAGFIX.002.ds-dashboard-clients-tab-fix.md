<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.002</id>
    <project>ADVI_INFLEC</project>
    <title>Fix dashboard.json split flag + clients_tab.json schema — Books tab crash blocker</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure: 650332e58 (dashboard split flag + clients_tab headline schema + S3 key path platinum/firm/clients_tab.json); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>critical</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §C4</ref>
    <ref type="target_script">data/orion/scripts/gold/INF_D_04.client_portal_summary.py</ref>
    <ref type="crash_root">ClientsTab.tsx line 288-291: dash.clients_tab.headline on undefined → TypeError</ref>
    <ref type="portal_contract">dashboard.json needs: split=true + clients_tab embedded OR separate clients_tab.json with headline object</ref>
  </references>

  <context>
    Books tab crashes with "Unable to Load Books" (ErrorBoundary catch). Root cause:
    - dashboard.json is a 273-byte stub: {firm_id, firm_name, generated_at, data_as_of, headline, ytd}
    - No `split` flag → getPlatinumFirmDashboard() returns stub directly
    - ClientsTab.tsx reads `dash.clients_tab.headline` → TypeError on undefined

    INF_D_04.client_portal_summary.py (line 638ff) builds the dashboard dict and writes
    dashboard.json. It needs to:
    1. Add 'split': True to the dashboard dict (or equivalent signal)
    2. The portal then loads clients_tab.json separately — but clients_tab.json has wrong schema
       Current: {generated_at, data_as_of, firm_id, total_aua, client_count, clients[]}
       Required: {headline: {aua, client_count, account_count, ...}, snapshot: {...}, distribution: {...}}

    TWO sub-tasks:
    A. Add split=True to dashboard.json output in INF_D_04
    B. Find + fix the clients_tab.json generating script to produce the correct schema

    After fix: re-run INF_D_04 + relevant clients_tab script on EC2 → verify platinum/firm/ on S3.
  </context>

  <scope>
    TASK A — Add `split` flag to dashboard.json:
    In INF_D_04.client_portal_summary.py build_dashboard(), in the dashboard dict construction:
    Add: 'split': True

    This tells the portal to load individual files (leaderboard.json, clients_tab.json,
    fee_efficiency.json) rather than expecting them embedded.

    Verify by reading the current dashboard dict construction at approx line 638-660
    and inserting 'split': True.

    TASK B — Fix clients_tab.json schema:
    1. Find which gold script generates clients_tab.json:
       Grep data/orion/scripts/gold/ for "clients_tab" to locate the generator.
       Likely INF_D_04 or INF_I_D00.portal_aggregates.py.

    2. The portal expects clients_tab.json with this top-level shape:
       {
         "headline": {
           "aua": <float>,            // total firm AUA (use aum_snapshot managed_value.sum())
           "client_count": <int>,
           "account_count": <int>,
           "fee_earning_aua": <float>,
           "data_as_of": <str>
         },
         "snapshot": { ... },         // optional metadata
         "distribution": { ... }      // optional distribution data
       }
       At minimum, headline.aua and headline.client_count must be non-null.

    3. Fix the generator to produce this shape. headline.aua should come from
       aum_snapshot managed_value.sum() (same source as header_metrics.total.aua).

    TASK C — Pre-commit gate:
    .tools/ds-commit-gate.sh on all modified Python files.

    TASK D — Re-run on EC2:
    After S3 upload: dispatch INF_D_04 re-run on EC2 via orion-gold-dispatch.sh or SSM.
    Verify: platinum/firm/dashboard.json has 'split': true.
    Verify: platinum/firm/clients_tab.json has headline.aua populated.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_D_04</run>
        <expect>WRITES includes platinum/firm/dashboard.json. READS includes silver/aum_snapshot.
        Verify no new COLUMN GAPS introduced by this fix.</expect>
        <if_mismatch>Document any PORTAL CONSUMERS of dashboard.json in session log.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "clients_tab" data/orion/scripts/gold/ | head -20</run>
        <expect>Identify which script writes clients_tab.json (the generator).</expect>
        <if_mismatch>If not found in gold/, check data/orion/scripts/silver/ and bronze/.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh &lt;modified_files&gt;</run>
        <expect>Exit 0. py_compile + AST + ruff all pass.</expect>
        <if_mismatch>STOP. Fix gate failures before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload and EC2 re-run">
      <step>
        <run>aws s3 cp s3://opal-data-inf/platinum/firm/dashboard.json /tmp/dashboard.json &amp;&amp; python3 -c "import json; d=json.load(open('/tmp/dashboard.json')); print('split=', d.get('split'), 'headline.aua=', d.get('headline',{}).get('total_aua'))"</run>
        <expect>split= True, headline.aua is non-null and ~$182.6M.</expect>
        <if_mismatch>Script did not regenerate correctly — check EC2 run logs.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/platinum/firm/clients_tab.json /tmp/clients_tab.json &amp;&amp; python3 -c "import json; d=json.load(open('/tmp/clients_tab.json')); h=d.get('headline',{}); print('headline.aua=', h.get('aua'), 'client_count=', h.get('client_count'))"</run>
        <expect>headline.aua is non-null (~$182.6M). client_count is a positive integer.</expect>
        <if_mismatch>clients_tab schema fix did not take effect.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      platinum/firm/dashboard.json has 'split': true (or 'split': True in JSON = true).
      Evidence: aws s3 cp + python parse in session log.
    </criterion>
    <criterion id="2">
      platinum/firm/clients_tab.json has headline.aua populated (~$182.6M) and
      headline.client_count is a positive integer. Evidence: aws s3 cp + python parse in session log.
    </criterion>
    <criterion id="3">
      .tools/ds-commit-gate.sh exits 0 on all modified files. Evidence: gate output.
    </criterion>
    <criterion id="4">
      S3 uploaded + comp-pipescript deployed MATCH for all modified scripts.
      Evidence: deploy check in session log.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO: commit hash(es), S3 deploy MATCH, dashboard.json snippet,
      clients_tab.json headline snippet.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="independent"/>
    Parallelizable with DIAGFIX.001 (AE investigation) and DIAGFIX.003/004/005.
    Does NOT need scope bug investigation to fix — crash fix is schema/flag only.
  </dependencies>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFLEC.DIAGFIX.002): INF_D_04 dashboard split flag + clients_tab headline schema" \
      -- &lt;modified_files&gt;
  </commit_identity>

  <notes>
    The Books tab crash (TypeError on dash.clients_tab.headline) will be fully resolved
    once split=true AND clients_tab.json has a valid headline object. DE is also authoring
    a defensive null-check (DIAGFIX.005) as belt-and-suspenders — both should ship.
    headline.aua in clients_tab should use aum_snapshot managed_value.sum() (=$182.6M exact),
    NOT holdings market_value (=$89.6M scope bug value).
  </notes>
</task_order>
