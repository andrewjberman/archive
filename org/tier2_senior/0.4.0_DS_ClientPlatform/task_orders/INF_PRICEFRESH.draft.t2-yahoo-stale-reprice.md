<to_id>INF_PRICEFRESH.DRAFT</to_id>
<project>INF_PRICEFRESH (DRAFT -- COO/CTO assign canonical code)</project>
<title>inf-gold canonical-prices reprice -- ROOT CAUSE = T2 yahoo feed stale since 2026-05-04 (not a 06-18..06-23 T3 bug). Refresh T2 + re-run canonical + add a T2-staleness detector.</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (yahoo backfill cadence / who runs backfill_yahoo_prices.py + its trigger); inf-pipeline owner</consult>
<verify>3.0.0_SA_CVO (re-cert the re-based canonical prices + the downstream inf-AUA impact -- cert-the-served discipline, same as W3)</verify>
<issued_by>2.0.0_SA_COO (DESIGN-ADVANCE GO 174939Z; serve gated on (a) methodology ratify CTO/COO + (b) CVO cert)</issued_by>
<issued_date>2026-06-26 (DRAFT -- DS-authored for COO ratification)</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "INF_PRICEFRESH (DRAFT -- COO/CTO assign " resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: withdrawn-wrong-premise</status>
<!-- WITHDRAWN 2026-06-26 (Andrew-direct correction): the premise below -- "T2 yahoo stale since 05-04 = a 7-week DEFECT to fix by refreshing the feed" -- is WRONG. Andrew (verbatim): "pretty sure the inf yahoo stuff is stale because we dont use that." The inf yahoo (T2) tier is INTENTIONALLY RETIRED/UNUSED, not an outage. inf canonical prices run on T1 transaction_observed + T3 interpolation + T4 carry-forward BY DESIGN (June canonical = 98.4% linear_interpolation, last yahoo_finance row 2026-05-04). The mechanism observation (yahoo 0 rows since 05-04) was CORRECT but mis-CLASSIFIED as a defect -- a Rule-22 trap (grounded WHAT, invented WHY/severity). Do NOT refresh yahoo, do NOT register as a defect-project. The real inf-reprice need (if any) + the intended go-forward price source = an open question routed to Andrew/COO, not this TO's premise. -->of

<problem_statement_grounded>
GROUNDED ROOT CAUSE (Rule 22, source-confirmed against opal-data-inf, 2026-06-26):
- T2 yahoo source `silver/historical_prices.parquet` is GLOBALLY STALE: max date = 2026-05-04 (min 2019-09-03, 4.9M rows). ZERO tickers have yahoo data >= 06-18 -- the entire yahoo feed stopped ~05-04. The 4 Opal ETFs (DIVZ/IDVZ/PFDE/PFOE) are present but only through 05-04.
- CONSEQUENCE: every inf canonical price from 05-05 -> present is built with NO T2 -- T1 (transaction_observed) on trade days + T3 linear-interpolation across the gaps + T4 carry-forward on trailing gaps. For thinly-traded tickers (the 4 Opal ETFs) the T1 gaps are multi-day, so the canonical price is a straight-line APPROXIMATION through the real intra-window market moves.
- The ETFS_AVGCAP_W1_AC2 brief (06-25) framed this as a "06-17..06-22 price FREEZE / flat carry." VERIFIED CORRECTION (06-26 canonical_prices.parquet): the 06-18..06-22 values are NOT frozen -- they linearly interpolate between 06-17 T1 and 06-23 T1 (e.g. DIVZ 37.3201->37.65 ramp UP; IDVZ 34.58->34.20 ramp DOWN). The "freeze" was a point-in-time artifact before 06-23 T1 landed; it self-resolved into interpolation. The DURABLE defect is the missing T2, not T3 (T3 is working as designed).
- SCOPE is therefore BROADER than 06-18..06-23: it is a ~7-week T2 outage (05-05..present) affecting all inf-gold valuation, most visibly on thinly-traded tickers.
</problem_statement_grounded>

<blast_radius_grounded>
canonical_prices.parquet (silver/prices/) consumers in the inf tree (grep-grounded; comp-blast func-level found callers only -- artifact reads are dynamic):
- INF_B_00.canonical_holdings.py  <- CRITICAL: applies canonical prices to value EVERY inf position -> inf AUA, the cot/inf ETF-ownership daily slices, ETFS_AVGCAP, portal holdings.
- INF_B_01.holdings_lots.py, INF_B_01b.classify_new_securities.py
- INF_D_07.concentration_risk.py, INF_D_07a.firm_concentrations.py
A reprice changes served canonical prices -> re-cert the downstream AUA (CVO), and a re-served monthly AVGCAP would re-base inflection (coordinate w/ the as_of convention question already at CTO).
</blast_radius_grounded>

<the_work>
1. FRESHEN T2 (the fix): run/repair `data/inf/scripts/silver/backfill_yahoo_prices.py` to bring `silver/historical_prices.parquet` current (05-05..>=today) for the inf ticker universe -- ESPECIALLY DIVZ/IDVZ/PFDE/PFOE. Ground WHY it stopped at 05-04 (cadence/trigger/credential) with 0.7.0/inf-owner -- a one-off backfill without fixing the cadence re-opens the gap.
2. RE-RUN canonical: `INF_build_canonical_prices.py` (4-tier; T2 yahoo takes priority over T1 in resolve_prices_for_ticker, so fresh T2 replaces the interpolated values on every day yahoo covers). NO T3 code change required -- the tier hierarchy is correct; it was starved of T2.
3. DETECTOR (durable close, mirrors the cot retry-net e2 pattern): add a T2-staleness guard -- alarm when yahoo max-date lags run-date beyond a cadence threshold (the silent-7-week-outage is exactly the freeze the cot retry-net killed for holdings; apply the same "don't let a stale feed go un-alarmed" doctrine to inf prices).
4. QUANTIFY impact (magnitude-sanity): the W1 brief bounded the AVGCAP June-MTD headline distortion at <1% (frozen days sat near live levels). Confirm the full inf-valuation delta (re-priced canonical vs current) before serve -- decision-useful, and the cert basis.
</the_work>

<serve_gate>
SERVE GATED (COO 174939Z): (a) methodology ratification -- changing served canonical prices is a sensitive downstream-feeding surface, CTO/COO ratify; (b) CVO cert on the re-based served prices + downstream AUA (cert-the-served, no unreviewed price change). Design advances now; serve later.
</serve_gate>

<compiler_tools_mandate>
comp-which-first; comp-pipescript io/deployed on INF_build_canonical_prices + backfill_yahoo_prices before run; comp-blast on canonical_prices consumers before any serve; ds-commit-gate (py_compile + ds-precommit + ruff FA, from __future__ import annotations) on every .py edit; firm-sep (opal-data-inf only); verify-on-served.
</compiler_tools_mandate>

<acceptance_criteria>
1. T2 yahoo root-cause grounded (why stale at 05-04) + cadence fix identified (not just a one-off backfill).
2. silver/historical_prices.parquet refreshed 05-05..>=today for the inf universe incl. the 4 Opal ETFs (comp-freshness/coverage PASS).
3. canonical_prices.parquet re-run; the 05-05..present window uses fresh T2 yahoo (price_source=yahoo_finance) where yahoo covers a day, T3 only filling genuine no-data gaps.
4. T2-staleness detector added + tested (alarm on yahoo-max-date lag > threshold).
5. Impact quantified (re-priced vs current inf valuation delta; AVGCAP June re-base if served).
6. Serve held pending methodology-ratify (CTO/COO) + CVO cert. firm-sep clean; ds-commit-gate PASS.
</acceptance_criteria>

<record_note>
Feeds back to ETFS_AVGCAP_W1_AC2 Finding B: the "06-17..06-22 freeze" framing is superseded by the grounded T2-stale-since-05-04 root cause + the self-resolved interpolation observation above. The W1 AVGCAP cert (inflection $38.81M) stands under cert-the-served; a reprice = a fresh all-partner re-base + re-cert, not a retraction.
</record_note>
