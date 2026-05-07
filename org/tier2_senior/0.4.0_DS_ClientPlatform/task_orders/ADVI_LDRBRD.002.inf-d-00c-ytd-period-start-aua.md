<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_LDRBRD.002</id>
    <project>ADVI_INFLEC</project>
    <title>INF_D_00c — YTD period_start_aua semantic fix (Bug B from LDRBRD.001)</title>
    <issued_to_phase0>0.4.0_DS_ClientPlatform~C</issued_to_phase0><!-- semantic ratify -->
    <issued_to_phase1>0.4.0_DS_ClientPlatform~D</issued_to_phase1><!-- implementation -->
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status>
    <priority>normal</priority>
    <estimated_effort>~0.5h DS~C (semantic ratify + test assertion); ~1h DS~D (implement + gate + run)</estimated_effort>
  </metadata>

  <references>
    <ref type="predecessor">ADVI_LDRBRD.001 — Bug B deferred from LDRBRD.001 session log (DS~D 2026-05-06): "Bug B: YTD period_start_aua None — DS~C semantic ratify needed. Separate follow-on TO."</ref>
    <ref type="gold_script">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py — _aua_at_start() + compute_leaderboard_entries()</ref>
    <ref type="evidence">LDRBRD.001 session log: YTD peter_lee period_start_aua=0.0 (Bug A2 fallback), YTD YTD windows returning psa=0.0 default rather than correct Jan 1 AUA value. The Bug A2 fix in commit 6e49f2694 applied psa_map.get(advisor_key, 0.0) default, which masks None but may not compute the correct value.</ref>
  </references>

  <context>
    LDRBRD.001 fixed Bug A (MAX window_start fallback), Bug C (lifecycle_aua wiring), and Bug A2
    (None → 0.0 default for pre-onboarding advisors). Bug B (YTD period_start_aua) was deferred
    because the correct semantic requires DS~C input.

    The question: for the YTD window (period_start = 2026-01-01), what should period_start_aua be?

    Options:
    A. Nearest-partition fallback: find the holdings partition closest to 2026-01-01 (same pattern
       as Bug A MAX fallback). Emit that AUA with a WARN if no exact match. This is consistent
       with Bug A treatment.
    B. Hard-zero: if no partition exists for Jan 1, emit 0.0 (current behavior post-Bug A2 fix).
       Semantically: "we don't know starting AUA, so we show 0." Safe but misleading.
    C. Onboarding-based: for advisors who joined after Jan 1, use their first known AUA as
       period_start_aua for YTD. Reflects "AUA at start of this advisor's year."

    DS~C ratifies Option A, B, or C (or a variant). DS~D implements.
  </context>

  <phase id="0" owner="0.4.0_DS_ClientPlatform~C" when="semantic ratify">
    <step>
      Review INF_D_00c.portal_leaderboard.py: read _aua_at_start() and compute_leaderboard_entries()
      to understand the current YTD window_start lookup path.
    </step>
    <step>
      Check available holdings partitions near 2026-01-01 in S3:
        aws s3 ls s3://opal-data-inf/silver/api_dims/assets/ | grep "2026-01" | head -10
        aws s3 ls s3://opal-data-inf/silver/api_dims/assets/ | head -5
      (Understand if a Jan 1 partition or near-Jan partition exists.)
    </step>
    <step>
      Choose the correct semantic option (A, B, or C above). Document rationale.
      Send RAVC2 to COO with: chosen option + brief rationale + any implementation notes for DS~D.
    </step>
  </phase>

  <phase id="1" owner="0.4.0_DS_ClientPlatform~D" when="after DS~C RAVC2 ratification arrives">
    <step>
      Implement per DS~C ratification in INF_D_00c.portal_leaderboard.py.
      Most likely: extend _aua_at_start() fallback logic to cover YTD window case
      (nearest partition to period_start date, with WARN on mismatch > 30 days).
    </step>
    <step>Pre-commit gate: .tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py — exit 0.</step>
    <step>Commit via safe-commit.sh with --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;"</step>
    <step>S3 upload: aws s3 cp data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py s3://opal-data-inf/code/gold/INF_D_00c.portal_leaderboard.py</step>
    <step>Dispatch chain run via AE 0.7 or SSM (same pattern as LDRBRD.001 D5 run f9dacdd0).</step>
    <step>Verify: employee_leaderboard.json YTD period_start_aua non-zero for advisors with holdings before Jan 1.</step>
    <step>RAVC3 to COO: commit + S3 + chain run evidence + YTD period_start_aua values observed.</step>
  </phase>

  <acceptance_criteria>
    <criterion id="AC1">YTD period_start_aua non-null and non-zero for advisors with pre-YTD-start holdings (e.g., peter_lee, patrick_scanlan).</criterion>
    <criterion id="AC2">YTD period_start_aua = 0.0 only for advisors whose first holding post-dates 2026-01-01 (pre-onboarding; semantically correct).</criterion>
    <criterion id="AC3">WARN emitted in gold log if nearest-partition fallback used (if Option A chosen).</criterion>
    <criterion id="AC4">Pre-commit gate exit 0. Commit + S3 upload confirmed. Chain run produces leaderboard.json at PROD prefix.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>20260506T~1800Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. DS~C: Phase 0 semantic ratify now. DS~D: read the TO and begin code review of _aua_at_start(); Phase 1 implementation awaits DS~C RAVC2.</message>
  </go_signal>
</task_order>
