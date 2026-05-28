<task_order>
  <metadata>
    <id>ADVI_INFDEMO.002</id>
    <slug>rd-fee-summary-costbasis-cosmetics-estimates</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-28</date>
    <status>complete</status><!-- F6+F8+F9 shipped portal DEV b5487690 (prior session). tsc clean. RAVC2 sent 2026-05-28. -->
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P0 — IWM demo TODAY (Andrew direct, batch 2). Early-PM demo, ~2-3h runway.</priority>
    <sla>Fast — F6 cosmetic, F8 one-line default, F9 small calc. Bundle one portal DEV cycle.</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md Batch 2 (F6/F8/F9 here; F7 = DS investigation, separate)</ref>
    <ref type="andrew_direct">Andrew 2026-05-28 ~1045 PT, image set 2: recolor+retitle Unrealized/Realized; client tax-status bar missing (DS); Advisor Split default 100%; Advisor Revenue (Estimated) by Window toggle.</ref>
    <ref type="cto_grounding">file/lines CTO-verified via explore this session; CLIENT LIST header pattern = text-[10px] text-white/40 uppercase tracking-widest mb-2.5</ref>
  </references>

  <context>
    Batch 2 of the IWM demo-prep cleanup. Portal DEV only (Rule 19). VISUAL-CONFIRM in bun run dev required (demo). F6 touches a SHARED component (TaxCostBasisPanel renders at advisor L2 + client L3 + account L4) — confirm it reads well at all levels. F8/F9 are client-level (FeeSummaryPanel, L3 only).
  </context>

  <objective>
    Three frontend fixes: (F6) recolor + retitle the UNREALIZED/REALIZED cards; (F8) default Advisor Split to 100%; (F9) render Advisor Revenue (Estimated) computed from the Window toggle. (F7 — client-level tax-status bar — is a DS investigation; you may get a follow-up to wire the l3Tax adapter if DS finds the data is present.)
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/panels/TaxCostBasisPanel.tsx (F6: title :152, card grid :145-195, colors via chartColors.ts TAX_COLORS)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/tabs/FeeSummaryPanel.tsx (F8: Advisor Split :399-401; F9: Advisor Revenue :403-405; inputs: feePayingAua :314, Total Firm Revenue :398, rfsWindow/effectiveWindow toggle :167-193)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/panels/ClientListPanel.tsx (:285 — CLIENT LIST header pattern to mirror)</file>
      <file action="readonly_reference">portal/src/.../chartColors.ts (TAX_COLORS + existing blue/orange palette tokens)</file>
    </files>
  </scope>

  <fix id="F6" priority="P0-cosmetic">
    <what>UNREALIZED/REALIZED cards: (a) recolor UNREALIZED green→BLUE, REALIZED yellow→ORANGE; (b) move the titles outside the container mirroring CLIENT LIST.</what>
    <recolor>Currently UNREALIZED = TAX_COLORS.taxFree (#10b981 emerald) + bg-emerald-500/10 + border-emerald-500/20; REALIZED = TAX_COLORS.taxDeferred (#f59e0b amber) + bg-amber-500/10 + border-amber-500/20. Change UNREALIZED→blue, REALIZED→orange (dot + bg/10 + border/20). Use palette-consistent blue + orange tokens (the existing Equity-blue + Alternatives/Cash-orange from the asset-mix donut, or blue-500/orange-500) — your pick for visual consistency. Do NOT reuse the tax-status taxFree/taxDeferred tokens (those stay green/yellow on the tax-status bar — F6 is only the Unrealized/Realized cards).</recolor>
    <retitle>Move the title (currently :152 inside the card: text-[10px] text-white/50 uppercase tracking-wide, beside the dot) OUTSIDE/above the card container, styled to MATCH CLIENT LIST exactly: text-[10px] text-white/40 uppercase tracking-widest mb-2.5, as a sibling above the container block. Container below holds COST BASIS / GAIN-LOSS / accts. Dot placement your visual call (CLIENT LIST has no dot; blue/orange can read from the card accent).</retitle>
    <ac>UNREALIZED blue + REALIZED orange; both titles outside the container in CLIENT LIST header style; content unchanged; visual-confirm reads well at advisor AND client level (shared component).</ac>
  </fix>

  <fix id="F8" priority="P0">
    <what>Advisor Split defaults to 100% (FeeSummaryPanel :399-401) instead of "—".</what>
    <do>When advisorSplitPct is null / no team_attribution present, default Advisor Split to 100.0%. Rationale (Andrew): IWM is single-advisor — no multi-advisor multi-account splits like 49F, so the advisor owns 100%. Also default the Accounts Summary SPLIT (BPS) column to the full bps (no split) rather than "—". If real team_attribution IS later emitted (DS), it takes precedence over the 100% default — guard the default so it only fills the absence.</do>
    <ac>Advisor Split shows 100.0% for IWM; SPLIT (BPS) shows full bps; a real multi-advisor split (if emitted) still wins.</ac>
  </fix>

  <fix id="F9" priority="P0">
    <what>Advisor Revenue renders an estimate labeled "Advisor Revenue (Estimated)" (FeeSummaryPanel :403-405) instead of "—".</what>
    <do>Compute client-side: advisorSplitPct (F8 = 100%) × the windowed Total Firm Revenue already shown at :398 (window_revenue?.[effectiveWindow]?.firm_revenue_usd ?? annual_implied_revenue). It must track the Window: toggle (QTD/YTD/MAX) — i.e. read effectiveWindow like Total Firm Revenue does — and reflect the current fee-paying-AUA snapshot. With split=100%, it equals the windowed firm revenue; keep it consistent with the Total Firm Revenue row so they never diverge. Change the row LABEL to "Advisor Revenue (Estimated)".</do>
    <why-estimated>It's off the current-snapshot fee-paying AUA, not day-by-day account values (that's the future DS TO, F10). The parenthetical sets the expectation — keep it.</why-estimated>
    <ac>Advisor Revenue (Estimated) renders a real number, tracks the Window toggle, == split × windowed firm revenue, label includes "(Estimated)".</ac>
  </fix>

  <phase id="verify" when="after write">
    <step><run>bun run dev :5173 — confirm F6 (blue/orange cards, titles outside, reads well advisor+client), F8 (100% split), F9 (estimated revenue tracks QTD/YTD/MAX toggle).</run><expect>All ACs visually confirmed in the running app.</expect></step>
    <step><run>bun build x + schema-check; confirm no 49F regression (F6 shared component — 49F Cost Basis cards also restyle; that's acceptable/desired for consistency, but verify no break).</run><expect>Clean.</expect></step>
  </phase>

  <acceptance>Commit portal DEV (NOT PROD — Rule 19). RAVC2 to COO + CC CTO. Hold origin push consistent with the .001 demo-gate posture unless told otherwise. Flag CTO immediately if F6 reads badly at any level or F9's window-math is ambiguous.</acceptance>

  <notes>F7 (client tax-status bar) is a DS investigation — if DS finds the L3 tax data is present (adapter gap not data miss), you'll get a follow-up to wire AdvisorBookClientDetail.tsx l3Tax (:126-146). Don't start F7 until DS reports. F10 (day-by-day revenue) is a future DS TO, not this TO.</notes>
</task_order>
