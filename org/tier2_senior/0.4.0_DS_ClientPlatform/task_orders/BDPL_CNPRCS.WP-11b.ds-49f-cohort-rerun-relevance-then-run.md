<task_order>
<metadata>
  <to_id>BDPL_CNPRCS.WP-11b</to_id>
  <project>BDPL_CNPRCS</project>
  <title>DS: VERIFY-RELEVANCE-FIRST then (if still valid) run the stranded 49F cohort re-run for the WP-11 scoped-price-override AUA delta (~$24.3M) — else recommend close the phantom in_progress</title>
  <assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED (Andrew-direct 2026-06-02 — "verify + re-run"). DS off sanctioned-hold. INVESTIGATE-FIRST: BDPL_CNPRCS is status=MERGED (into ADVI_ROLLUP, 2026-04-15) + WP-11 stranded since 2026-04-15 — verify still-valid BEFORE re-running (likely-superseded by the MDPF Schwab-re-derive + canonical_prices churn since April).</status>
  <dispatch_held>false</dispatch_held>
  <priority>MEDIUM — capacity-fill of DS's free lane (Andrew-directed); NOT on any Inflection critical path. Clears a phantom in_progress either way (run-or-close).</priority>
  <references>
    <ref type="parent_to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/BDPL_CNPRCS.WP-11.ds-scoped-price-overrides.md (DS/~D code complete 864b6d7a; scoped overrides injected + canonical_prices spot-checks PASS; awaiting the 49F cohort re-run)</ref>
    <ref type="merged_into">BDPL_CNPRCS status=merged -> ADVI_ROLLUP (Waves 0+2, 2026-04-15)</ref>
  </references>
</metadata>

<scope>
Your own queue-hygiene flag (this session): BDPL_CNPRCS.WP-11 has been stranded in_progress since 2026-04-15 — DS/~D code complete (864b6d7a), scoped price-overrides injected, canonical_prices spot-checks PASS, but it's been "awaiting 49F cohort re-run for AUA delta (~$24.3M) + comp-blast Phase 3 + a gold_validate_config.yaml entry for canonical_prices" ever since. Andrew directed: verify + re-run.

## STEP 1 — VERIFY RELEVANCE (do this FIRST, before any re-run)
BDPL_CNPRCS is MERGED (into ADVI_ROLLUP 2026-04-15) and this has sat 6+ weeks. The 49F cohort + canonical_prices + AUA basis have churned heavily since (MDPF Schwab re-derive, canonical-prices/scoped-overrides work, the whole v0.9 MDPF basis). DETERMINE:
- Is the WP-11 scoped-price-override 49F-cohort-re-run + its ~$24.3M AUA delta STILL a live, wanted, un-superseded computation? Or has the canonical_prices / 49F-cohort / scoped-override landscape moved such that this re-run is stale/moot/already-effectively-done by later work?
- Check: is the scoped-override injection (864b6d7a) still in the live canonical_prices path, or superseded? Does the $24.3M delta still apply to the current 49F cohort, or has the basis changed?

## STEP 2 — BRANCH on the verify
- **If STILL VALID:** run the 49F cohort re-run + comp-blast Phase 3 (blast-radius) + add the gold_validate_config.yaml canonical_prices entry. Standard DS gold cycle (Rule 13) + ds-commit-gate (Rule 14) + comp-pipescript postdeps + SERVED-verify (not just partition — your discipline). RAVC2 the delta to COO+CTO+CVO.
- **If SUPERSEDED/MOOT:** do NOT re-run. Document WHY (what later work absorbed/superseded it) + recommend closing WP-11 (and the phantom in_progress). RAVC2 the close-recommendation to COO.

Either branch CLEARS the phantom in_progress — that's the goal. Don't blindly re-run a possibly-stale April computation; verify-first protects against re-introducing a superseded number.
</scope>

<acceptance>
- [ ] AC — STEP-1 relevance determination documented (still-valid vs superseded, with evidence: is the scoped-override + $24.3M delta still live on the current 49F-cohort/canonical_prices basis?). Then EITHER (still-valid) re-run + comp-blast + gold_validate_config entry + served-verify + RAVC2 the delta, OR (superseded) close-recommendation documented + RAVC2'd. Phantom in_progress cleared either way. To COO (+ CTO/CVO if a re-run lands a data change).
</acceptance>

<notes>
Capacity-fill of DS's free lane per Andrew-direct 2026-06-02 (DS's Inflection data-leg is certified-complete; this is the stranded-TO follow-up DS itself flagged). VERIFY-FIRST is mandatory given the merged-project + 6-week-stale state — Andrew said "verify + re-run," and the verify is the gate (a stale re-run could re-introduce a superseded $24.3M number into a churned basis). If still-valid, it's a clean DS gold re-run; if superseded, a clean close. The other stranded TO (ADVI_STAUDT.COHORT-A, awaiting DE footnote) is DE-gated, separate — COO drives that downstream leg.
</notes>
</task_order>
