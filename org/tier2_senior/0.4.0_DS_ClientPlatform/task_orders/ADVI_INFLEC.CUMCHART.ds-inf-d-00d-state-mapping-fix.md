<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.CUMCHART</id>
    <project>ADVI_INFLEC</project>
    <title>INF_D_00d.cumulative_chart.py state-mapping fix — refactor to use household_dim.state_code (mirrors INF_D_04)</title>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~30-45 min refactor + commit + S3 + verify</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnosis">RD diagnosis 20260507T185240Z — Inflection Continuous Segment Analytics broken — INF_D_00d publisher uses wrong state-mapping source</ref>
    <ref type="user_report">Andrew: "the continuous view is deprecated and not using the same data as snapshot, none of the GEO stacked blocks and wrong AUA number."</ref>
    <ref type="andrew_routing">Andrew direct 2026-05-07T~18:58Z: "i have routed this note from RD to DS~D for implementation"</ref>
    <ref type="target_file">data/orion/scripts/gold/INF_D_00d.cumulative_chart.py</ref>
    <ref type="reference_pattern">data/orion/scripts/gold/INF_D_04.client_portal_summary.py lines 1690-1716 (_build_geo_view) — known-working state-mapping pattern</ref>
  </references>

  <context>
    The Inflection portal's DistributionTab CONTINUOUS view (vs Snapshot view) renders broken:
      - geo.categories = ['Other', 'Other'] (literal duplicate, no real states)
      - geo.data only carries {date, Other: <value>}
      - last-row total = $189.2M (94.8% of canonical $199.6M)
      - adv.categories = only 3 of 4 advisors
      - nna_geo same broken state

    Root cause (RD diagnosis): INF_D_00d.cumulative_chart.py lines 199-208 joins state via
    `silver/api_dims/accounts_v2.state` field — but that field is empty for Inflection accounts.
    Every household falls into 'Other' fallback.

    The WORKING snapshot publisher (INF_D_04.client_portal_summary.py lines 1690-1716) uses
    `household_dim.state_code` with an `accounts_dim` fallback path. Same pattern needs to
    apply in INF_D_00d for consistent state-by-state stacks.

    Secondary bugs in INF_D_00d to fix while there:
      1. Duplicate 'Other' in categories (lines 223-225) — when 'Other' is already in top_states
         AND in pivot.columns, it gets appended twice.
      2. Missing 4th advisor in adv.categories — investigate (TOP_N_ADVISORS=9 cutoff?
         name-normalization mismatch? row-filter dropping one?).
      3. nna_geo (lines 354-372) has same broken state-mapping — applies same fix.
  </context>

  <scope>
    <step>
      Read INF_D_04.client_portal_summary.py lines 1690-1716 (`_build_geo_view`) to capture
      the canonical state-mapping pattern:
        Path 1: hd[['household_id', 'state_code']] (when household_dim has household_id directly)
        Path 2 (fallback): accounts_dim merge (account_id → household_id)
    </step>
    <step>
      Read INF_D_00d.cumulative_chart.py current state — specifically:
        Lines 199-208: build_geo_view state-mapping from accounts_v2.state
        Lines 223-225: top_states + pivot.columns dedup logic
        Lines 354-372: build_nna_geo_view state-mapping (same broken pattern)
        adv aggregation logic (find missing-4th-advisor cause)
    </step>
    <step>
      Refactor 3 functions to use the household_dim.state_code path:
        - build_geo_view (lines 199-208 → mirror INF_D_04 pattern)
        - build_geo_drill_view (likely same pattern)
        - build_nna_geo_view (lines 354-372 → mirror INF_D_04 pattern)
      Drop accounts_v2.state source entirely.
    </step>
    <step>
      Fix duplicate-'Other' dedup (lines 223-225). Use set semantics or explicit not-in
      check before append.
    </step>
    <step>
      Audit missing-4th-advisor: verify INFLECTION_REP_IDS (or whatever the script uses)
      includes all 4 = {3, 6, 11, 12}. If filter is correct, verify advisor_assignments
      has all 4 reps. If row-filter, identify which advisor is being dropped + why.
    </step>
    <step>
      Pre-commit gate: .tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00d.cumulative_chart.py — exit 0.
    </step>
    <step>
      Commit via .tools/safe-commit.sh:
        --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;"
        -m "fix(ADVI_INFLEC.CUMCHART): INF_D_00d state-mapping uses household_dim.state_code (mirrors INF_D_04). Drops accounts_v2.state. Dedup Other. Audit 4th advisor."
        -- data/orion/scripts/gold/INF_D_00d.cumulative_chart.py
    </step>
    <step>
      git push origin CLOUD.
    </step>
    <step>
      S3 upload (per CLAUDE.md rule 13 — DS owns gold-script S3 upload):
        aws s3 cp data/orion/scripts/gold/INF_D_00d.cumulative_chart.py \
          s3://opal-data-inf/code/gold/INF_D_00d.cumulative_chart.py
      Verify comp-pipescript deployed INF_D_00d MATCH.
    </step>
    <step>
      Empirical run: dispatch via inf-gold-qa-runner SSM with OUTPUT_PREFIX=qa/ to test
      against current bronze + silver. Verify cumulative_chart.json output:
        - geo.categories includes real states (e.g., WA, MT, CA, IN, MN per snapshot)
        - geo.data rows carry per-state AUA
        - adv.categories has all 4 advisors
        - last-row total ≈ $199.6M (canonical)
    </step>
    <step>
      Per Andrew direct routing — do NOT wait for INFNNA.GOLD cascade to re-run. Standalone
      gold dispatch for INF_D_00d only is fine. PROD push: signal AE 0.7 to bd-gold-trigger
      OR manual SSM dispatch on inf-gold-layer-runner with OUTPUT_PREFIX=platinum/
      (production prefix) once QA passes.
    </step>
    <step>
      Post-PROD-publish: CDN invalidation for platinum/firm/cumulative_chart.json?firm=inf
      (CF distribution EVTSA9VEHNZVH). Coordinate with AE 0.7 if you need invalidation
      permissions, OR call inf-portal-publisher Lambda which handles CF invalidation
      (catch-warn until IAM permission lands; standalone aws cli works in interim).
    </step>
    <step>
      RAVC to COO: commit hash + S3 ETag + comp-pipescript MATCH + sample QA JSON output
      (geo.categories list, adv.categories list, last-row total).
      Tag RD for post-publish visual verification.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript deployed INF_D_00d.cumulative_chart.py — MATCH required</tool>
    <tool>comp-validate INF_D_00d --artifact (post-publish) — exit 0 ALL-PASS</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">build_geo_view + build_geo_drill_view + build_nna_geo_view all use household_dim.state_code (with accounts_dim fallback) — accounts_v2.state dropped entirely.</criterion>
    <criterion id="AC2">Duplicate-'Other' dedup fixed (set-based or explicit not-in check).</criterion>
    <criterion id="AC3">All 4 advisors present in adv.categories (rep_ids 3, 6, 11, 12).</criterion>
    <criterion id="AC4">QA empirical run produces cumulative_chart.json with real states (WA/MT/CA/IN/MN per snapshot reference) + last-row total ≈ $199.6M.</criterion>
    <criterion id="AC5">PROD publish + CDN invalidation complete.</criterion>
    <criterion id="AC6">RD visual verify confirms continuous view matches snapshot view's segment list.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent fix on current bronze + silver state.</upstream>
    <downstream>RD post-publish visual verify (AC6).</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:58Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Andrew direct routing to DS~D. Standalone fix; do not wait for INFNNA.GOLD cascade. ~30-45 min total.</message>
  </go_signal>
</task_order>
