<task_order>
  <metadata>
    <id>ADVI_49EXEC.005</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- RAVC4-closed 2026-04-24 by 2.0.0_SA_COO. Evidence: commit 8cc69bab (CLOUD). RE-BASELINE: TO draft targeted D_00c; actual platinum leaderboard writer is D_04.client_portal_summary.py line ~2398 per comp-pipescript io. Rotation added to D_04 (correct producer): s3.copy_object src=platinum/firm/leaderboard.json dst=platinum/firm/leaderboard.prior_week.json with NoSuchKey/exception handled as WARN (first run safe). py_compile + ds-commit-gate PASS. S3 MATCH ETag b9e5e567e046219deab959b8886e5708. comp-platinum reverse leaderboards.prior_week = empty (case [a] new artifact no prior consumers). Phase 3 post-nightly verification: DS reports aws s3 ls evidence tomorrow AM confirming platinum/firm/leaderboard.prior_week.json emits after tonight's 23:00Z nightly. CTO RAVC accepted MCP 20260424. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (gates leaderboard_rank_delta + cohort_drift slot triggers in TO 1)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §4.4 + §7 TO 5</ref>
  </references>

  <objective>
    Add 1-line snapshot rotation at the end of the nightly leaderboard build script (D_00c.advisor_leaderboard.py per recent RA-P3 work):

    BEFORE writing the new `platinum/leaderboards/{firm}.json`, copy the existing version to `platinum/leaderboards/{firm}.prior_week.json`. Sequencing critical — the renamed copy is the OLD value, then overwrite with new.

    Implementation choice (PRD §4.4): Option A (snapshot rotation, 1 line). Option B (timeseries store) deferred to v1.5+.

    Output: 1-2 line addition to the leaderboard build script + S3 upload of the modified script.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00c.advisor_leaderboard.py (or the leaderboard-emitting script per comp-pipescript)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/code/gold/D_00c.advisor_leaderboard.py — script update</write>
      <write_after_first_run>s3://opal-data-bd/platinum/leaderboards/{firm}.prior_week.json — rotation begins after first nightly post-deploy</write_after_first_run>
    </s3_writes>
  </scope>

  <wire_contract>
    `platinum/leaderboards/{firm}.prior_week.json` exists 7+ days into rollout (rolling weekly snapshot). TO 1 templates consume this for leaderboard_rank_delta + cohort_drift trigger comparisons.
  </wire_contract>

  <acceptance_criteria>
    1. Rotation logic added BEFORE leaderboard write (sequencing verified — old copy first, then overwrite).
    2. py_compile clean.
    3. S3 upload to `code/gold/` with documented etag.
    4. After first nightly post-deploy: `aws s3 ls s3://opal-data-bd/platinum/leaderboards/` shows both `{firm}.json` AND `{firm}.prior_week.json`.
    5. Spot-check: `{firm}.prior_week.json` mtime should be the previous run's mtime (one nightly behind).
    6. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE to COO + CTO with: commit hash, S3 etag, post-nightly verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00c</run>
        <expect>WRITES list includes `gold/artifacts/employee_leaderboard.json` (per RA-P3 graph). Confirm leaderboard write site is in this script. If actual leaderboard file is elsewhere (D_00b? a separate script?), re-baseline.</expect>
        <if_mismatch>Locate actual leaderboard producer.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse leaderboards.prior_week</run>
        <expect>Empty (new artifact; no consumers yet).</expect>
        <if_mismatch>If consumers exist, schema must match prior contract.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_00c.advisor_leaderboard.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after first nightly post-deploy">
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/leaderboards/ | grep prior_week</run>
        <expect>{firm}.prior_week.json exists with mtime = previous run.</expect>
        <if_mismatch>Sequencing bug — rotation may have written current value to prior_week.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Single-writer on `platinum/leaderboards/{firm}.{prior_week.}json`. No other TO touches.
    - Output consumed by TO 1 (DS templates) + future v1.5 features.
    - Coordinate with ~B if RA-P3 D_00c file still has open edits — likely safe (RA-P3 commit `e53f0afa` shipped + S3-uploaded already).
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    TO 5 close → TO 1 templates consume the prior_week snapshot for rank_delta + cohort_drift triggers.
  </next>
</task_order>
