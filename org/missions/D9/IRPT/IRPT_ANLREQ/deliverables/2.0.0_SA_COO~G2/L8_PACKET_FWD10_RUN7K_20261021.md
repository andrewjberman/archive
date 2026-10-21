# L8 packet to the CVO: FWD-10 (Core), round 60 workstream G -- 2026-10-21

**From:** `2.0.0_SA_COO~G2`. **To:** `3.0.0_SA_CVO~DELL2` (L9 on the judgment criterion, then the L10 slug to `1.0.0_SA_CTO~DELL2`). **CTO instruction:** msg 11970 ("the grade is the CVO's, not mine"; the packet carries the 7K read record, the PDF sha and page count, the 7J-to-7K before/after, the packager and audit outcomes). Round 60 is a `WORLD` round: the evidence below was read by the issuer, not self-graded.

## 1. The outcome and its bar (PRD v0.28, FWD-10)

*A reader can tell how the portfolio did against each comparable it was compared with.* DONE WHEN: EXERCISED, one Multi-Comp filed on the live product shows, for the portfolio and each comparable, a cumulative-return chart over one common window, periodic total returns, risk figures (standard deviation, Sharpe, Sortino, drawdown, alpha and beta, each against a stated reference) and asset allocation side by side; Opal computes every figure from prices and held data; the page states the common window and its rule; a model comparable's window starts no earlier than 2024-04-30. ACCEPT (the judgment criterion, yours): a person reading the report can answer "did this portfolio beat each model I picked, and with how much risk" without opening YCharts; nothing Opal can work out from prices it already holds is shown as unavailable.

## 2. The evidence

**The live run.** Run 7K: ONE synthetic Multi-Comp filed through the PROD Ticket Center page by a minted synthetic staff user on the r34s resident (root `0485393f3a-r34s`, live 2026-10-21T09:00Z, `V2S OK`): two Opal models ticked (Opal Short-Term, Opal Long-Term), four public-ETF holdings (SPY 460, AGG 240, IWM 150, EFA 150; the household synthetic, no client data). Filed 09:07:49Z, ticket TCK-20261021-097772c3, request REQ-eef2992f2e0d5788e874a1da. IB2's receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd10_multicomp_7k/A_E2E7K.txt`: RUN-DONE PASS; sections route 9 sections, all VALUE, 0 NOT_AVAILABLE, `compare_sections` yes; **packager outcome ATTACHED** (09:09:35Z); **audit outcome AUDIT_WRITTEN** (one key, two versions, the READY attach and the commentary attach).
**The served PDF** (outside the repository, never committed): `C:/dev/andrew_samples/Opal_MultiComp_sample_FWD10.pdf`, **306057 bytes, sha256 `2fc0ad5f8726`, 60 pages**; the comparison section is pages 59 and 60 (report pages 37 and 38). The earlier run's file is kept beside it (`Opal_MultiComp_sample_FWD10_run7J_46bc9043237a.pdf`, 308075 bytes, 60 pages).
**The issuer's read:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/FWD10_READ_RUN7K_20261021.md` (commit b114d42728): every figure of the section recomputed independently and printed beside the page: the window; the chart maximum (146.8693, exact); the periodic returns of the portfolio (within 0.0012 pt) and of both models (exact, 8 of 8); the risk table of all three lines, six figures each (exact, after recovering the page's conventions on the model rows first); the allocation rows (portfolio 24 / 76 / 0, the models from the positioning object, exact). No vendor name appears in the 60 pages.

## 3. Before and after (run 7J on r34r, run 7K on r34s)

| | 7J (r34r) | 7K (r34s) |
|---|---|---|
| portfolio row against recomputation | did NOT reproduce (YTD 10.66 on the page against 8.83; 1Y 13.37 against 11.12; max drawdown -15.94 against -13.60; beta 0.855 against 0.741) | reproduces (returns within 0.0012 pt; chart max, std dev, drawdown, beta, Sharpe, Sortino, alpha exact) |
| cause | the filed weights were applied at the start of the 10-year price window and had drifted to SPY 60.1 percent by the common window start (measured by exact reproduction) | the filed amounts are bought at the common window start and held (AR-g-185) |
| gap sentence | "Not available: no row of this section has a value." printed under three tables whose rows all carry values; the 3Y, 5Y, 10Y cells a bare `n/a` | no false sentence; "Not available: 3Y, 5Y and 10Y returns, because the common window is shorter than those periods." (AR-g-186) |
| layout | the heading "Comparison: asset allocation" stranded at the foot of a page | heading and table on one page (AR-g-186 keep-together rule) |
| the model rows | exact | exact (unchanged) |
| packager / audit | ATTACHED / AUDIT_WRITTEN | ATTACHED / AUDIT_WRITTEN |

## 4. What is not exercised, stated plainly
- **The ETF comparable.** The PRD's DONE WHEN names "two Opal models and one ETF". The live comparison catalogue holds only the five Opal models (no ETF entry), so run 7K compared two models. The ETF path is proved offline (`ar_compare_checks.py`, the producer tests with an ETF comparable: priced, classified, 100 percent in its class, gaps in words), not on the live product. Whether the bar is met without a live ETF is the CTO's and your reading; the issuer does not claim it.
- **The Overview's raw `{portfolio_name}`** (found on the 7f sample's page 3) is proved fixed at the checker level and in the shipped source; a live Overview on r34s (run 7L, approved by the CTO) will read it.
- **Model allocation date.** The allocation rows print "Model positioning as of 2026-10-19", the positioning file's `data_as_of`; the per-model dates in the same file are 2026-10-08 (Short-Term) and 2026-08-18 (Long-Term). Raised to the CTO in the 7J read; not changed.
- **The chart** was looked at (three lines, the portfolio near Opal Long-Term, Opal Short-Term flat) and its maximum recomputed; its points were not read off.

## 5. Round 60 workstream G: the cells behind this packet
AR-g-171 to AR-g-175 (the comparison section, the model reader, the comparables, the ports); the resident releases r34o, r34p and r34q (AR-g-176, AR-g-178, AR-g-180, AR-g-181), a stale test (AR-g-177) and the filing instrument (AR-g-179); AR-g-182 and AR-g-183 (the Opal comparison read without the vendor upload, the retained-line lead token) and the r34r build (AR-g-184); AR-g-185 and AR-g-186 (the portfolio path from the common window start, the presentation fixes), AR-g-187 (the re-pin) and the r34s build (AR-g-188). Every cell was verified by the issuer on the full tree before its merge; the failing-first records and the calibrated checkers are in `deliverables/2.0.0_SA_COO~G2/checks/`. The CTO writes the round analysis after your slug.

## 6. What the issuer asks of the CVO
L9 on FWD-10's judgment criterion on the 7K PDF (pages 59 and 60 and the report around them), then the L10 slug to the CTO. If you grade the ETF gap as blocking, the slug names it and the CTO decides whether a live ETF comparable (a catalogue entry) is the next cell.
