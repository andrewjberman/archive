<task_order>
  <metadata>
    <id>ADVI_INFDRF.001</id>
    <slug>dsa-inf-d04-geo-reconciliation-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-15 -- Andrew-flagged URGENT. Defects A/B/D proceed immediately. Defect C (client_count canonicalization) is gated on the CTO ruling (see cross_domain_coordination) -- author the A/B/D fix now; hold the C rewrite for the ruling.</dispatch_unblock_condition>
    <project_code>ADVI_INFDRF</project_code>
    <priority>P1 -- Andrew-flagged URGENT. Inflection live-portal Segment Analytics shows reconciliation slippage (state count != sum of city counts; histogram plotted != total). DS~A is the BE root-cause author and the designated owner.</priority>
    <sla>Fast -- Andrew wants it quick. ~3-5h for A/B/D + the chain run; C follows the CTO ruling.</sla>
  </metadata>

  <references>
    <diagnosis>DS~A BE root-cause diagnosis 2026-05-15 (Andrew-flagged URGENT co-investigation with DE 0.4) -- evidence-backed via S3 object-versions + INF_D_04 code trace; the DS~A session log carries the full evidence. This TO is scoped directly from that diagnosis -- DS~A authored it; do not re-derive.</diagnosis>
    <directive>Andrew direct 2026-05-15 -- flagged the Inflection live-portal data drift URGENT; DS~A + DE 0.4 co-investigated.</directive>
    <sibling>ADVI_INFDRF.002 (AE 0.6.1) -- the 06:00 cron holdings under-build (the root cause of the "WA 685->744" symptom). RD 0.4.2 shipped sibling FE fixes the same day (GEO L1 median 1ac05055, account-grain count 79a512bd, GEO city->Books route 92365e05). DE 0.4 owns the FE surface->field-grain map -- coordinate.</sibling>
  </references>

  <context>
    INF_D_04 client_portal_summary.py (_build_geo_view + _compute_histogram_block) carries 4 distinct count-reconciliation defects that surface as visible slippage between the Segment Analytics snapshot / radial / header. DS~A confirmed INF_D_04 code is UNCHANGED since 2026-05-14 -- these are pre-existing latent defects exposed by the drift investigation, not a regression. (The "WA 685 -> 744" symptom is a separate root cause -- a defective 06:00 holdings build corrected by the 17:57Z full chain; 744 is CORRECT. That is ADVI_INFDRF.002, not this TO.)
  </context>

  <objective>
    INF_D_04 emits internally-consistent Segment Analytics counts: the state total equals the sum of its city breakdown; the histogram reports an explicit excluded-count so plotted + excluded == total; client_count has a single canonical source; radial_12m's partial decomposition is explicitly labeled.
  </objective>

  <scope>
    <item>DEFECT A (immediate) -- null-city accounts are dropped from the city breakdown, so the state count (744 WA) != the sum of city counts (515). Fix _build_geo_view so null-city / unmapped-city accounts are retained (an explicit Unknown / Unmapped city bucket, or otherwise carried so state == sum(city)). REAL BUG.</item>
    <item>DEFECT B (immediate) -- the histogram 1K floor filters accounts but emits no excluded count, so the plotted total (770) != the firm total (865). Add an explicit excluded-count reconciliation field to _compute_histogram_block output so plotted + excluded == total. Per CLAUDE.md Rule 17 the gold tier is where business-logic filtering belongs -- this is gold; the fix is to make the filter's exclusion COUNTED + emitted, not to remove the filter.</item>
    <item>DEFECT D (immediate) -- radial_12m is a partial decomposition presented unlabeled. Add an explicit label / partial-flag so the FE renders it as a partial decomposition, not a full one.</item>
    <item>DEFECT C (GATED on the CTO ruling) -- client_count has a dual source of truth: 321 (geo view, holdings-merge household nunique) vs 307 (accounts_dim, the dedicated client dimension; radial_12m clients also sum to 307). DS~A's read: 307 is canonical, geo's 321 is a side-effect of the holdings merge. Do NOT rewrite the geo household derivation until the CTO rules which is canonical. Once ruled: converge client_count to the single canonical source across the geo view + radial + header.</item>
    <item>SCOPE -- this is an INF_D_04 gold-emitter fix. The 06:00 cron holdings under-build is ADVI_INFDRF.002 (AE). The FE surface->field-grain map is DE 0.4's -- coordinate but do not own it here.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Defect A fixed -- INF_D_04 geo view: state count == sum of its city counts (null/unmapped-city accounts retained, not dropped).</ac>
    <ac id="AC2">Defect B fixed -- the histogram block emits an explicit excluded-count; plotted + excluded == firm total.</ac>
    <ac id="AC3">Defect D fixed -- radial_12m carries an explicit partial-decomposition label/flag.</ac>
    <ac id="AC4">Defect C -- on the CTO ruling: client_count converged to the single canonical source across geo view + radial + header. If the ruling is still pending at TO-completion, AC4 may RAVC2 as "A/B/D shipped, C held for the CTO ruling" -- a valid partial-complete state.</ac>
    <ac id="AC5">comp-pipescript io on INF_D_04 (COLUMN GAPS); ds-commit-gate.sh on the .py before commit; from __future__ import annotations first import (Rule 15); no emoji. The fix materialized via a gold chain re-run; smoke-test + validate the reconciled counts against the materialized client_portal_summary artifact and carry the evidence in the RAVC2 (Andrew /loop directive).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1: comp-pipescript io on INF_D_04.client_portal_summary.py. Phase 2: ds-commit-gate.sh before commit; comp-pipescript deployed before the chain run. Phase 3: verify the reconciled counts on the materialized artifact (state == sum-city; plotted + excluded == total).</compiler_tools_mandate>

  <cross_domain_coordination>
    DEFECT C -- CTO RULING REQUIRED. The canonical firm client_count question (307 accounts_dim vs 321 geo-derived) is routed to the CTO by COO; it may escalate to Andrew (product: the definition of "a client"). Defects A/B/D do NOT wait on it -- ship them; hold only the C rewrite. COO relays the ruling.
    CHAIN RUN -- this TO materializes via a gold chain re-run. Coordinate the chain run with COO -- there is a pending INFGRO firm_return_pct_twr fix + ADVI_BIWNDW.002 1Y/3Y window-emit that also need an INF chain run; avoid redundant cycles. Surface to COO before the chain run.
    DE 0.4 owns the FE surface->field-grain map (the sibling FE side); RD 0.4.2 already shipped FE fixes (1ac05055 / 79a512bd / 92365e05). Coordinate so the BE reconciliation + the FE rendering agree.
    ADVI_INFDRF.002 (AE 0.6.1) fixes the 06:00 cron holdings under-build -- the root cause of the "WA 685->744" symptom. Independent of this TO; both feed the same project.
  </cross_domain_coordination>

  <deliverables>
    <item>INF_D_04 fixed (defects A/B/D; C on the CTO ruling); gold chain re-run; reconciled counts verified on the materialized artifact.</item>
    <item>Session log + RAVC2 to COO + CC CTO + CC DE 0.4.</item>
  </deliverables>

  <ravc>0.4.0_DS_ClientPlatform (DS~A) RAVC2 to COO + CC CTO + CC DE 0.4 on AC1-5.</ravc>

  <notes>
    Andrew-flagged URGENT -- move fast. DS~A authored the diagnosis; this TO is scoped from it -- do not re-derive. Defects A/B/D are immediate; defect C waits only on the CTO ruling. Per CLAUDE.md Rule 17 the histogram filter (defect B) stays -- the fix is to COUNT + emit the exclusion, not remove the business filter; null-city retention (defect A) is shape-preservation, not field-slimming. No emoji; Rule 15 future-import. Smoke-test the reconciled counts on the materialized artifact per Andrew's /loop directive.
  </notes>
</task_order>
