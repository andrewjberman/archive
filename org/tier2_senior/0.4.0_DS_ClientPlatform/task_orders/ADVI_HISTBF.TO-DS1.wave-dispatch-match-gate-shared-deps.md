<task_order>
  <metadata>
    <id>ADVI_HISTBF.TO-DS1</id>
    <project>ADVI_HISTBF</project>
    <title>Wave Dispatch MATCH Gate — Shared Deps Assertion (RULING 4)</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P1 — process gate; blocks Wave C dispatch authorization</priority>
    <estimated_effort>0.5h (script + checklist update)</estimated_effort>
    <gates_on>ADVI_HISTBF.003 Wave B RAVC4 (COO will issue Wave C dispatch only after this TO is complete)</gates_on>
  </metadata>

  <context>
    RULING 4 issued by COO 2026-05-01 following Wave B v1 failure (20260430T223214Z):

    INCIDENT: Wave B v1 dispatch failed at startup — pull scripts failed with
    ModuleNotFoundError because rate_limiter.py and jwt_freshness.py were missing from
    S3 on the EC2 runner. Wave A MATCH gate was asserted on 4 pull scripts
    (pull_inflection_accounts_v2.py, pull_inflection_household.py,
    pull_inflection_household_rep_mapping.py, pull_inflection_billing.py) but NOT on
    shared deps. DS uploaded both files manually (~13:03Z); AE 0.6.1 updated
    dispatch_histbf_backfill_v2.sh to include them in the EC2 sync block.

    ROOT CAUSE: No structural requirement to assert shared deps existence in MATCH gate.
    The 4-script MATCH gate was DS~B's scope — shared deps were authored by DS BASE and
    not included in the MATCH gate procedure.

    AE 0.6.1 raised "DS RULING 4 COO TO pending" in RAVC4 20260501T174900Z.

    RELATED: AE 0.6.1 already updated dispatch_histbf_backfill_v2.sh to sync
    rate_limiter.py + jwt_freshness.py in the EC2 pre-run block. This TO adds the
    upstream MATCH gate assertion so the issue is caught before dispatch, not at runtime.
  </context>

  <objective>
    Update DS wave dispatch procedure so that any future HISTBF wave dispatch MATCH gate
    explicitly asserts that shared deps are present and current in S3 before DS sends
    MATCH RAVC to COO.

    Two deliverables:
    (1) Add S3 existence check for shared deps to the wave dispatch checklist / pre-dispatch
        script. At minimum an aws s3 ls assertion for:
        - s3://opal-data-inf/code/orion/rate_limiter.py
        - s3://opal-data-inf/code/orion/jwt_freshness.py
        (and any future shared dep added to the dispatch sync block)
    (2) Update the MATCH gate assertion comment/docstring in
        dispatch_histbf_backfill_v2.sh (or successor) to explicitly list shared deps as
        required assertions alongside per-dim pull scripts. If AE 0.6.1 already updated
        the sync block, DS annotates the assertion section to reference both pull scripts
        AND shared deps.
  </objective>

  <acceptance_criteria>
    1. Pre-dispatch assertion exists (aws s3 ls or equivalent) for rate_limiter.py and
       jwt_freshness.py at their canonical S3 paths; exits non-zero (blocks dispatch) if
       either is missing
    2. MATCH gate docstring/comment in dispatch script updated to list shared deps
       alongside per-dim scripts as required assertions
    3. Change committed on CLOUD with DS author serial; RAVC4 to COO confirms commit hash
    4. No changes to script logic outside assertion block (scope-contained fix)
  </acceptance_criteria>

  <notes>
    This is a process-hardening TO. Scope is narrow: assertion check + comment update only.
    Do NOT refactor the dispatch script or modify run logic.
    AE 0.6.1 owns the EC2 sync block — do not modify dispatch_histbf_backfill_v2.sh
    beyond the assertion section without AE coordination.
    COO will not authorize Wave C dispatch until this TO RAVC4 is received.
  </notes>
</task_order>
