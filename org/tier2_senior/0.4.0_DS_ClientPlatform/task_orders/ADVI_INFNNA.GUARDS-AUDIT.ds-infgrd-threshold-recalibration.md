<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.GUARDS-AUDIT</id>
    <project>ADVI_INFNNA</project>
    <title>Recalibrate INFGRD Guard B AUA thresholds across all silver builders ($203M is now canonical)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>medium</priority>
    <estimated_effort>~1h audit + threshold updates + commit</estimated_effort>
  </metadata>

  <references>
    <ref type="incident">INFNNA full-backfill 2026-05-07 — accounts_v2 silver Guard B fired at $476.9M ([$50M, $400M] bounds). Root cause: missing rep_id filter (let through all custodian-matched accounts). Filter applied today; canonical now 848 accounts / $203.2M.</ref>
    <ref type="canonical_baseline">accounts_v2 INFLECTION_REP_IDS-filtered: 848 rows / $203.2M (2026-05-07 snapshot, all 4 advisors including Joe Brandenburg)</ref>
    <ref type="prior_baselines">Pre-Joe baselines: ~$197M (3 reps including IWM but missing Joe). Pre-attribution-fix: stale IWM-aggregated.</ref>
    <ref type="apply_aua_guard">data/orion/scripts/silver/convert_orion_api_to_silver.py — apply_aua_guard() helper. Search for invocations across all dim builders.</ref>
  </references>

  <context>
    INFGRD Guard B is a sanity check that fires when filtered AUA falls outside expected
    bounds. Bounds were calibrated to ~$197M baseline (pre-Joe). Now that Joe is
    correctly attributed, baseline is $203.2M — within prior bounds. But the bounds need
    updating so future drift detects above current canonical, not above stale baseline.

    Also: other dim builders may have their own Guard B thresholds. They all need
    re-calibration to the new canonical baseline.
  </context>

  <scope>
    <step>
      grep across silver builders for `apply_aua_guard\|GUARD_B\|filtered AUA outside\|sanity bounds` to enumerate all guard invocations.
    </step>
    <step>
      For each guard invocation, document:
        - Dim name
        - Current bounds [low, high]
        - Field guarded (current_value, ending_mv, etc.)
        - Expected canonical AUA today (post-filter)
    </step>
    <step>
      Update bounds. Recommended tightening:
        low = $150M (allow some downside vs $203M)
        high = $300M (allow ~50% upside before alert)
      Adjust per-dim if specific dim has narrower expected scope (e.g. accounts_v2 is firm-wide; specific subset dims may differ).
    </step>
    <step>
      Pre-commit gate: .tools/ds-commit-gate.sh on edited builder file(s) — exit 0.
    </step>
    <step>
      Commit via safe-commit.sh:
        --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;"
        -m "fix(ADVI_INFNNA.GUARDS-AUDIT): recalibrate INFGRD Guard B thresholds — $203M canonical post-Joe-attribution-fix"
        -- data/orion/scripts/silver/convert_orion_api_to_silver.py [other builders if changed]
    </step>
    <step>git push origin CLOUD + S3 upload + comp-pipescript deployed MATCH.</step>
    <step>
      Re-run a silver build (e.g., accounts_v2 today) — confirm Guard B passes within new bounds.
    </step>
    <step>
      RAVC: per-dim guard table (before/after thresholds) + test build pass.
    </step>
  </scope>

  <acceptance_criteria>
    <criterion id="AC1">All Guard B invocations across silver builders enumerated with current + new thresholds.</criterion>
    <criterion id="AC2">New thresholds are sized to $203M canonical with reasonable margin (low ≥ $150M, high ≤ $350M for firm-wide AUA dims).</criterion>
    <criterion id="AC3">Test silver builds pass without Guard B failure under new thresholds.</criterion>
    <criterion id="AC4">Commit + push + S3 upload + comp-pipescript MATCH.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None.</upstream>
    <downstream>INFNNA.SILVER cleanup may surface Guard B failures otherwise.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Lower priority than INFNNA.SILVER + INFNNA.GOLD; can ship in parallel.</message>
  </go_signal>
</task_order>
