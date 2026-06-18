<to_id>ADVI_NNAATTR.TO-2</to_id>
<project>ADVI_NNAATTR</project>
<title>TO-2 -- DE/RD frontend repoint to the all-roles advisor_nna_canonical (F-1b/F-1c) + drop the INFMVP.F5 architect-override + F-3 Inflection fee-split</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>0.4.2_RD_AdvisorIntelligence (chart-VISUAL repoint sub-leg: snapshot donut + continuous + Lifetime Activity -- STAGED for RD after the DECK_CLAUDE Andrew-direct work; coordinate window vocab/labels)</consult>
<issued_by>2.0.0_SA_COO (ADVI_NNAATTR decomposition; TO-2 was gated only on DE-online -- now MET; /drive cycle 2026-06-18)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<!-- GO 2026-06-18 (COO /drive): DE 0.4.0 live + flagged parallel capacity (P2-1 waits on AE P2-2). TO-2's only gate was DE-online (met); F-1a landed (the all-roles number exists). DE-leg GO now; RD chart-leg staged behind the deck. Build now, VERIFY on the served artifact post-nightly. -->

<priority>HIGH -- the NNA fix's FRONTEND leg. TO-1 (DS) produces the all-roles advisor_nna_canonical, but the silent financial-display defect (same advisor reads $4.14M vs $6.95M by route -- Travis) is NOT user-visible-fixed until the FE SURFACES read the canonical number. Plus the Continuous chart's 60%-flow-loss bug (sampled nna_adv) closes here.</priority>

<gate>DE-online: MET. The all-roles advisor_nna_canonical field EXISTS (TO-1 deployed F-1a). BUILD now; VERIFY on the SERVED artifact post-nightly (D_00f's F-2 series-tie fix validates on tonight's nightly -> fresh tomorrow-AM). Build-then-verify-on-served, same pattern as TO-1.</gate>

<scope>
F-1b/F-1c (DE data-wiring -- this GO): repoint the ADVI page NNA surfaces -- Distribution, Continuous chart, profile, snapshot donut, Lifetime Activity -- to READ advisor_nna_canonical:
- windows (totals): QTD/YTD/MAX/1Y/3Y/q_current/q1/q2/q3, each with fee_paying/no_fee split (F-4 tie-out). Hero/total displays read windows.
- series (bucket-summed per-period): the Continuous chart area/tooltips read series. CRITICAL: this repoint ALSO FIXES the 60%-flow-loss bug -- the continuous chart currently reads the SAMPLED nna_adv/nna_geo; repointing to the bucket-summed series stops the sampling (sum-within-period, correct flows).
- Align window vocab/labels across surfaces (the spine defect was mismatched/unlabeled window vocabularies -- one identical number per window x fee_view everywhere).
DROP the ADVI_INFMVP.F5 architect-only override: the override path is SUPERSEDED by the canonical field -- REMOVE it (grep-confirm removed, not bypassed).
F-3: Inflection fee-split (the inf NNA fee-paying/no-fee split rendering).
RD sub-leg (STAGED for RD, after the deck): the chart-VISUAL repoint (hero totals -> windows; area/tooltips -> series; Lifetime Activity -> matching window). Coordinate labels with the DE wiring. RD GO when its deck slot frees.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check on the NNA-rendering components (Distribution / Continuous / profile / snapshot donut / Lifetime Activity) -- vs the advisor_nna_canonical field shape (windows + series)</run>
      <expect>The components' current NNA field reads enumerated; the canonical windows/series shape present in the served contract. MISSING = a runtime-undefined repoint target.</expect>
      <if_mismatch>STOP. If a surface reads a field not in advisor_nna_canonical, the repoint target is wrong -- confirm the canonical field shape with DS (TO-1 producer) before wiring.</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions (if the repoint introduces new react-query keys for the canonical field)</run>
      <expect>No key collision; the canonical-field query key is distinct or correctly shared.</expect>
      <if_mismatch>Resolve the collision before wiring (the W3 OFC-class discipline).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>VERIFY on the SERVED advisor_nna_canonical artifact (post-nightly): cross-route identity -- the same advisor reads the SAME per-advisor number on every surface (the $4.14M-vs-$6.95M divergence GONE in the FE); the Continuous chart reads series not the sampled nna_adv</run>
      <expect>Cross-route identity holds on the served number; the 60%-flow-loss is gone (series, not sampled); the INFMVP.F5 override path removed. Verify on the SERVED artifact, NEVER self-report.</expect>
      <if_mismatch>If a surface still diverges or the continuous still samples, the repoint missed a read-site -- enumerate + fix. A served-artifact mismatch is the close-blocker.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
READS advisor_nna_canonical (DS/D_00f produces it; the SERVED artifact validates on tonight's nightly -> verify tomorrow-AM). DE data-wiring (this GO) + RD chart-visual (staged sub-leg). GATE-OF-RECORD = the NFRA_GCONTR NNA value-limb (CVO: 49F House recognized-canonical, Unassigned bounded-transient) -- the FE read + the emit must satisfy it (advisory v1 flags the current divergence by design). Coordinate the window vocab/labels DE<->RD so the chart-visual matches the data-wiring.
</cross_domain_coordination>

<acceptance_criteria>
1. The ADVI NNA surfaces (Distribution, Continuous, profile, snapshot donut, Lifetime Activity) READ advisor_nna_canonical (windows for totals, series for the continuous chart).
2. CROSS-ROUTE IDENTITY in the FE: same advisor = same per-advisor number on every surface (the silent $4.14M-vs-$6.95M divergence gone), verified on the SERVED artifact post-nightly.
3. Continuous chart 60%-flow-loss FIXED: reads the bucket-summed series, not the sampled nna_adv/nna_geo.
4. ADVI_INFMVP.F5 architect-only override REMOVED (grep-confirm removed, not bypassed).
5. F-3 Inflection fee-split rendered.
6. Window vocab/labels aligned across surfaces (one number per window x fee_view).
7. Session-log Compiler Tools reproduces each <run>. RAVC2 to COO (CC CTO + CVO). RD chart-visual sub-leg RAVC2's separately when its slot fires.
</acceptance_criteria>

<dependencies>
  <dependency project="ADVI_NNAATTR" task="TO-1" note="F-1a produces the all-roles advisor_nna_canonical field (deployed; served verify post-nightly)" status="complete"/>
  <dependency artifact="served advisor_nna_canonical (post tonight's nightly = fresh)" status="pending-nightly"/>
</dependencies>

<references>
  <ref type="to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_NNAATTR.TO-1... (the producer; the canonical field + buckets)</ref>
  <ref type="brief">docs/briefs/advi-infmvp-f5-canonical-advisor-nna-phase0-20260528.md (the canonical windows/series field + the RD repoint detail, line 88)</ref>
</references>

<lane_note>
DE data-wiring PRIMARY (F-1b/F-1c + drop-INFMVP.F5 + F-3) -- now-unblocked (F-1a landed, DE online), your parallel slot while P2-1 waits on AE's P2-2. RD chart-VISUAL sub-leg STAGED (after the DECK_CLAUDE deck work) -- I GO RD's leg when its slot frees + coordinate labels. BUILD now; the cross-route-identity VERIFY is on the SERVED artifact post-nightly (tomorrow-AM, when D_00f's fix is fresh). RAVC2 to COO (CC CTO+CVO).
</lane_note>
