<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-23-valfin-009-inf-d-02-config</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <re_routed_from>0.4.0_DS_ClientPlatform (base; pre-LD-0027 spawn)</re_routed_from>
    <re_routed_at>2026-05-24T02:25Z UTC (implicit -- DS~D picked up on intake per spawn-baked-directive)</re_routed_at>
    <date>2026-05-23</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_VALFIN</project_code>
    <!-- CLOSURE 2026-05-24T02:25Z UTC (2.0.0_SA_COO base). DS~D RAVC2-ACCEPTED.
         Commit 940321a37 + session log session_valfin_009_inf_d_02_comp_validate_config_fix.md.
         All 5 ACs PASS: comp-validate INF_D_02 --artifact /tmp/pl_book.json exits 0
         pre + post commit (PASS Count 199 >= 100 at clients); intent preserved
         (count_min type + threshold unchanged); only INF_D_02 block touched (no
         scope-creep, 14 ins / 3 del all within INF_D_02 yaml block); session log
         + Compiler Tools section landed; this RAVC2-ACCEPT closes.
         
         Selection reasoning: peter_lee/book.json (workhorse ~199 clients / ~627
         accounts / ~$165M AUA) over inflection_wealth_management/book.json (small
         specific book, 6 clients, insufficient for count_min=100 gate). Tighter
         regression detection.
         
         CC CVO ratified per DS~D RAVC2-Request body cite (filename:
         20260524T022753Z_0.4.0_DS_ClientPlatform~D_-RAVC2-Request_-_ADVI_VALFIN.009.md). -->

    <priority>P3 -- comp-validate is producing EXIT 1 on INF_D_02 due to stale config (not a script defect). Unblocks clean comp-validate runs across INF gold scripts; not gating any active critical path.</priority>
    <sla>~30 min wall (config-edit, no script touch).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-23T07:35Z. Surfaced by DS Base in
         ADVI_VALFIN.001 Phase-3 RAVC2 (5365d96f2) as out-of-scope per AC5; DS
         routed for separate config-correction TO. -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1)</prd>
    <validation_brief>docs/briefs/advi-valfin-001-inflection-books-tab-validation-20260523.md (5365d96f2) -- the pre-existing comp-validate findings section</validation_brief>
    <comp_validate_config>data/orion/scripts/gold/gold_validate_config.yaml lines 105-116 (INF_D_02 block)</comp_validate_config>
    <comp_validate_protocol>docs/architecture/COMP_VALIDATE_PROTOCOL.md</comp_validate_protocol>
  </references>

  <objective>
    Fix the stale `primary_artifact` reference in `gold_validate_config.yaml` for INF_D_02 so `comp-validate INF_D_02` exits 0 against the script's actual output shape. Current config points at `platinum/advisors/inflection_wealth_management/advisor_client_detail.json` (a path INF_D_02 does not write); script writes per-household `platinum/clients/{hh_id}/detail.json` + per-advisor `platinum/advisors/{advisor_key}/book.json`. End-state: comp-validate INF_D_02 clean exit + check semantic matches what INF_D_02 actually produces.
  </objective>

  <context>
    DS Base's ADVI_VALFIN.001 Phase-3 RAVC2 (5365d96f2) flagged: "INF_D_02 comp-validate: config references `platinum/advisors/inflection_wealth_management/advisor_client_detail.json` with `clients` count_min=100. This file doesn't exist -- INF_D_02 writes individual `platinum/clients/{hh_id}/detail.json` per household (no firm-level aggregate). Config needs update to reference correct per-household path or a valid aggregate artifact. EXIT 1 on comp-validate for INF_D_02."

    Root cause hypothesis: the config block was authored against an earlier INF_D_02 emit shape (pre-some-refactor) that has since changed. The check intent ("INF_D_02 produces a substantive household population") is still valid, but the artifact-path and count-semantic need to match the current emit shape.

    DS owns the deepest understanding of what INF_D_02 actually writes + which check shape best preserves the intent. This TO authorizes DS to make the call -- propose the new check shape + ship.
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- Diagnose what INF_D_02 actually emits at firm-aggregate vs per-household level. Run:
        - `aws s3 ls s3://opal-data-inf/platinum/advisors/{any-advisor-key}/` to confirm book.json + any aggregate.
        - `aws s3 ls s3://opal-data-inf/platinum/clients/` to count per-household detail.json files.
        - Identify the right check semantic: either (i) count_min on per-household detail.json files (use a glob / list_objects check pattern) OR (ii) point at a different INF_D_02 output that has a `clients` array OR (iii) replace the check with a more apt one matching the current emit shape.

      DELIVERABLE B -- Edit `data/orion/scripts/gold/gold_validate_config.yaml` INF_D_02 block (lines ~105-116):
        - Update `primary_artifact` to a path INF_D_02 actually writes (or remove the field if check is path-agnostic).
        - Update the `clients` count_min check to match the new artifact shape OR replace with an equivalent semantic check.
        - Preserve the check intent ("INF_D_02 producing substantive household population") so a future schema-drift can still trip the gate.

      DELIVERABLE C -- Verify the fix:
        - Run `comp-validate INF_D_02` -- exits 0; the new check resolves correctly against the live artifact(s).
        - Negative test: temporarily break the artifact emit (or mock a scenario) -- verify the check would have caught the regression. (Document in session log; do NOT actually break production data.)

      DELIVERABLE D -- Commit + push via .tools/safe-commit.sh + session log + RAVC2 to COO with comp-validate output.
    </in_scope>
    <out_of_scope>
      - The INF_D_00 geo_drill / geo_aua comp-validate ERROR -- separate TO (ADVI_VALFIN.010 banked, scope-owner pending CTO triage since this surface was an INFGRO concern + INFGRO closed per LD-0014).
      - Any INF_D_02 script logic change -- this is a CONFIG fix, not a code fix.
      - Adding new comp-validate checks for other scripts -- scope-creep guard; touch only the INF_D_02 block.
      - The fee-billing gap (INF_C_08) -- separate biz question pending Andrew.
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform (DS pod-4 base; this is DS-only).
    No cross-lane coordination needed -- gold_validate_config.yaml is in DS pod-4's owned-paths lane.
    CC CVO on the RAVC2 -- they may want to add the corrected check to their /spot-check pattern reference.
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_D_02</run>
        <expect>WRITES list reveals all artifacts INF_D_02 emits -- enumerate the candidate primary_artifact paths.</expect>
        <if_mismatch>STOP. If comp-pipescript can't enumerate, fall back to grep-on-script for `put_object` / `to_parquet` / `to_json` calls.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-validate INF_D_02 (against the proposed config edit, locally)</run>
        <expect>Exit 0. The new check resolves cleanly against the live artifact.</expect>
        <if_mismatch>STOP. Iterate the config until comp-validate is clean.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0 (yaml passes whatever the gate runs; if yaml-only-gate not configured, skip with reasoning in session log).</expect>
        <if_mismatch>STOP. Investigate gate failure before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-validate INF_D_02 (post-push, re-run from clean checkout)</run>
        <expect>Exit 0 confirmed.</expect>
        <if_mismatch>STOP. Drift between local + pushed state; diagnose.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">comp-validate INF_D_02 exits 0 against the corrected config.</ac>
    <ac id="AC2">The corrected check preserves the original intent: a meaningful substantive-population gate on INF_D_02's output (would catch a future schema-drift or scope-filter regression).</ac>
    <ac id="AC3">Only the INF_D_02 block in gold_validate_config.yaml is modified -- no scope-creep into other script blocks.</ac>
    <ac id="AC4">Session log includes Compiler Tools section reproducing every &lt;run&gt; with observed output + pass/fail vs. &lt;expect&gt;.</ac>
    <ac id="AC5">RAVC2 to COO + CC CVO with the comp-validate output evidencing AC1.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Editing the INF_D_02 script itself (script logic is correct per VALFIN.001 closure; this is a CONFIG defect).
    - Removing the check entirely without replacing it (the intent -- gate on substantive population -- is load-bearing).
    - Adding checks for other scripts (scope-creep guard).
    - Acceptance flex on AC1 (the comp-validate exit-0 check is the empirical gate; without it the fix is unconfirmed).
  </not_authorized>
</task_order>
