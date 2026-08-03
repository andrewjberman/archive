# Derivation-depth assessment (CTO authorization 233628Z; bounded to the 48 pairs)

**archetype:** VALIDATE
**Author:** 0.4.0_DS_ClientPlatform -- 2026-08-03 ~23:50Z. READ-ONLY (versioned GETs only).
**Method:** per artifact, every exposure-window version (07-28..07-31Z) value-diffed against
the post-recovery (>=08-01) version on COMMON paths only (axis growth excluded); date/period-
keyed entries compared SAME-DATE across versions, so a restated historical value is evidence
the window version carried different (shell-era) values. Machine output: depth_assess_out.json.

## THE VERDICT: FLOWED -- the near-empty snapshots reached SERVED VALUES, not just selection

**Unambiguous shell signatures (not explainable as daily drift):**

1. **partner_analytics_{annual,monthly,quarterly} -- the ADV (advisor) + CLA views
   collapsed to degenerate values during the window.** Historical-period donut totals
   rendered as THE CURRENT FIRM TOTAL: `.views.adv.y1/y2/y3.donut.total = 463,649,292.59`
   during the window, restated after recovery to their real values (y1 -> 436,654,607.00;
   y2/y3 -> 0; m2 -> 218,525,272.68; m3 -> 168,717.70). Mechanism fit: the ADV dimension
   derives from the allocations enrichment (Rep Code / advisor attribution -- the very
   columns the 1-3-row snapshots lack), so attribution degenerated to one bucket carrying
   the whole firm. CLA anomalies of the same class:
   `.views.cla.current.geo.segments[0].nmnc.inflows = 371,657,251.14` during the window
   vs 5,289,440.48 restated (~70x).
   Scale: ~4,000-4,700 common-path values restated per version in each of the three
   (denominators 12,523 / 33,865-33,944 / 22,402-22,481).

2. **The same degenerate total propagated into headline surfaces**: dashboard
   (employee_leaderboard architect.aua, clients_tab.tax.taxable), header_metrics
   (by_architect[0].aua, total.aua), leaderboard (1Y summary + entries),
   clients-tab-slim (headline.total_aua, tax.taxable) all carried 463,649,292.59-class
   values during the window. CAVEAT: for these, "total AUA" legitimately tracks the firm
   total daily; the DISCRIMINATING evidence is the partner-analytics historical-period
   degeneracy above, plus leaderboard per-client anomalies (e.g. small_account_aua
   -169,031.64 -> -119,031.64, a $50,000.00 exact-step restatement).

3. **NNA/flow surfaces carried restated history**: cumulative_chart same-date entries
   (e.g. date=2026-07-24 TX nna) shifted ~$11,030.33 uniformly; timeseries_chart
   growth_decomposition period=2026-07 market: 22,036,641.41 -> 25,612,231.77;
   header_metrics nna_qtd 4,931,297.59 -> 4,806,133.96.

## Two-cause honesty (do NOT read raw counts as impact)

The raw restated-value counts (e.g. client_directory 352/669) conflate (a) ordinary daily
movement in current-period values between the window write and the 08-01 recovery write,
and (b) shell-induced values. Counts OVERSTATE shell impact; the SIGNATURES in section 1
are the shell-attributable core (historical periods must not move day-to-day; degenerate
equality with the current total is not drift). Per-path exhaustive attribution beyond the
signatures was not performed -- marked UNKNOWN rather than estimated.

## UNKNOWNs (with reasons)

- Pre-07-19 serve history: permanently unreconstructable (no surviving versions) -- the
  June episode's SERVE impact stays unknown even though its artifact-level double-count
  is measured (0.2.0's census). Stated per CTO instruction, not smoothed.
- client_directory per-household aua diffs (~0.7%) are within daily-drift range --
  shell-flow NOT established for that artifact (its allocations dependency is metadata
  enrichment); verdict UNKNOWN-leaning-drift.
- Exact per-artifact dollar impact at each of the 48 pairs: the restated deltas above are
  measured per shown path; a full per-pair dollar ledger would require path-level
  classification of every restated value (available in depth_assess_out.json for anyone
  who needs it; not summarized further to avoid drift-vs-shell conflation).

## One-line for the package

Within surviving evidence, the four exposure-day publishes did not merely SELECT
near-empty snapshots -- they SERVED shell-degenerate values on partner-facing surfaces,
most visibly as historical advisor-view totals equal to the current firm total, corrected
at the 08-01 recovery publish.
