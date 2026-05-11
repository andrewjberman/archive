<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.PORTAL-VERIFY</id>
    <project>ADVI_INFNNA</project>
    <title>Portal visual verify — Joe Brandenburg present, IWM normalizes, NMNC/NNA reconciliation</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~30 min visual sweep + RAVC</estimated_effort>
  </metadata>

  <references>
    <ref type="incident">INFNNA.001 — Andrew flagged portal Q2 2026 firm NNA = -$1.36M while NMNC = $19.7M (incongruous). Root cause: Joe Brandenburg (rep_id=6) missing from bronze + canonical_nna stale under old IWM-aggregated attribution.</ref>
    <ref type="upstream_TOs">INFNNA.SILVER + INFNNA.GOLD must complete before this visual verify runs (rebuilt platinum/firm/leaderboard.json + nmec_nmnc_nna.json + header_metrics.json).</ref>
    <ref type="prior_ground_truth">Andrew's accounts_v2 cross-tab: rep_id=3 IWM 13 accounts $254K, rep_id=6 Joe 67 accounts $16M, rep_id=11 Patrick 152 accounts $20.4M, rep_id=12 Peter 617 accounts $160.9M. Total ~$197M (pre-current-snapshot); current canonical $203.2M.</ref>
  </references>

  <context>
    Once gold cascade rebuilds platinum artifacts with corrected attribution, the portal
    must show:
      - Leaderboard with all 4 advisors including Joe Brandenburg (non-zero NNA)
      - IWM (Inflection Wealth Management general bucket) normalized to small share
        (~13 accounts, ~$254K AUA, ~0% of NNA)
      - Q2 2026 firm NNA reconciled with Q2 NMNC (NMNC ≈ NNA-from-new-clients)

    This is the final visual gate. If anything looks off, RAVC with specifics so DS
    can investigate residual issues.
  </context>

  <scope>
    <step>
      Wait for COO signal that INFNNA.GOLD complete + new platinum artifacts live.
      COO will explicitly trigger this TO; do not start ahead of signal.
    </step>
    <step>
      Load /advisor-intelligence portal as Andrew, select Inflection. Visit each panel:
        - Assets Overview (firm-level NMNC + NNA tiles + stacked bars)
        - Distribution tab (per-advisor breakdowns)
        - Advisor drill (each of 4 advisors)
    </step>
    <step>
      CHECK A — Leaderboard / per-advisor view:
        - Confirm all 4 advisors visible: Inflection Wealth Management, Joe Brandenburg, Patrick Scanlan, Peter Lee
        - Joe Brandenburg row shows non-zero AUA (~$16M) AND non-zero NNA (Q2 + YTD + 1Y windows)
        - IWM row shows small AUA (~$254K) AND small / zero NNA
        - Peter Lee no longer dominates 89% of NMNC
    </step>
    <step>
      CHECK B — Firm-level NMNC / NNA reconciliation:
        - Q2 2026 NMNC tile value (post-rebuild)
        - Q2 2026 firm NNA tile value (post-rebuild)
        - Confirm NMNC ≈ NNA inflows from new accounts (within 10%)
        - Confirm Q2 firm NNA is no longer -$1.36M (should be reasonable positive or modestly negative, depending on actual flows)
    </step>
    <step>
      CHECK C — No regressions on adjacent panels:
        - Asset Mix tab still renders
        - Top Holdings still renders
        - Distribution tab still renders
        - 49F (other firm) — confirm no impact on 49F panels (gate isInflectionFirm)
    </step>
    <step>
      Capture screenshots + result JSON. Append "Final Verification post-INFNNA" section
      to org/tier3_junior/0.4.2_RD_AdvisorIntelligence/inflec_ground_truth.md with the
      new ground truth: Total AUA, per-advisor AUA + accounts + NNA breakdown, dates
      verified.
    </step>
    <step>
      RAVC to COO: PASS/FAIL per check + new ground truth values + commit hash + screenshots.
    </step>
  </scope>

  <acceptance_criteria>
    <criterion id="AC1">All 4 advisors visible in leaderboard.</criterion>
    <criterion id="AC2">Joe Brandenburg's AUA + NNA non-zero across windows.</criterion>
    <criterion id="AC3">IWM AUA ≤ $300K AND IWM NNA close to zero.</criterion>
    <criterion id="AC4">Q2 firm NNA reconciles with Q2 NMNC (NMNC-from-new ≈ NNA-from-new, within 10%).</criterion>
    <criterion id="AC5">No regressions on Asset Mix, Top Holdings, Distribution panels.</criterion>
    <criterion id="AC6">49F firm — zero impact (isInflectionFirm gate confirmed).</criterion>
    <criterion id="AC7">inflec_ground_truth.md updated with post-fix canonical values.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>INFNNA.GOLD must complete + COO trigger.</upstream>
    <downstream>None — final gate.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>pending INFNNA.GOLD completion</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD until COO triggers post INFNNA.GOLD RAVC. Then execute immediately.</message>
  </go_signal>
</task_order>
