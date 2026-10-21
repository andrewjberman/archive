# FWD-10 (Core) -- the one real run: plan, written before the release exists

Issuer `2.0.0_SA_COO~G2`, 2026-10-20. Decomposition `decompositions/IRPT_ANLREQ_DECOMP_R60_G.md`; code on trunk at `51e86c27cd0`; the model-read grant is live (IB2 record `A_AFTER_MODELGRANT_R2.txt`). The run waits on a resident root after r34n that carries the code (release owner: asked of `2.0.0_SA_COO~Y2`, 2026-10-20 20:33Z). Run orchestration (filing, principals, polling) is Y2's; the reading and the arithmetic are this seat's.

## What is filed

ONE Multi-Comp on the live product by an Opal staff principal: the filer's firm, two Opal models (one short, one long, for example `opal_short_term` and `opal_long_term`), and one ETF the estate prices (for example IWM). Record the ticket id, the composition ref and the report ref. One Comparison with a single ETF comparable is a second, cheaper filing only if the Multi-Comp reads clean (the one-comparable case is covered offline by `ar_compare_checks.py 175 build`).

## What is read, page by page (the served PDF, not the run record)

1. The comparison section is the LAST section, after the price table. Read every page of it in the retained PDF (`pdftotext -layout` plus a rendered look at the chart page).
2. **Window.** START and END printed; compare to my own computation: START = latest first observation among the portfolio and the three comparables, END = earliest last observation. The model series ends at its `data_as_of`; an ETF ends at the T-1 frontier; the portfolio path ends at the report date's frontier.
3. **Chart.** Every path starts at 100 on START and ends at END (no path runs past END). Names are the filer's labels; no vendor name on the page (R8).
4. **Returns table.** 1m 3m YTD 1y 3y 5y 10y for portfolio and each comparable; a period longer than the window reads `n/a`. Recompute each cell from the live series with `ar_compare_checks.py`'s own arithmetic (not the code under test).
5. **Risk table.** N = min(5, floor(window months / 12)) whole years; std dev, Sharpe, Sortino, max drawdown, alpha, beta against SPY and BIL; N below 1 reads `not available: ...` in words for every row.
6. **Allocation table.** Portfolio by-amount classes; each model from `positioning.portfolios.<code>.allocation`, DATED with the file's `data_as_of`; the ETF at 100 percent in its classified class. Percent columns sum to 100 within rounding.
7. **Gaps (FWD-12).** Any comparable or cell Opal cannot fill reads `not available for <name>: <reason>`; a blank or a dash without words fails.

## Independent arithmetic

Inputs are the live objects themselves, read by this seat with its own credentials (read-only): `json/benchmarks/model_portfolio_timeseries.json` and `json/positioning/positioning_data.json` of `opal-data-portal-v2`, plus the ETF's closes through the same chain the checker's fixtures use. The portfolio path is taken from the run's own retained price stage (the buy-and-hold path in `run.json`), because that is the input, not the output, of the comparison. Every number on the comparison pages is recomputed; a mismatch beyond rounding is a FAIL row, not a note.

## Done when

All five elements read VALUE on the served pages with numbers equal to the recomputation, the window and the allocation date are printed, no vendor name appears, and one gap case (for example an ETF with no price, or a model asked beyond its inception) reads in words. Then FWD-10 is REALIZED for the CVO's L9 on the judgment criterion (a reader can tell how the portfolio did against each comparable). FWD-11 (parity) starts after.

## Not claimed

That the release exists, that a principal and a filing path are ready (Y2), or that the comparison reads well to a person (CVO L9).

## Update 2026-10-21 (issuer): the run as it will be filed (run 7I)

The filing is the IB2-driven synthetic run 7I (order `IRPT_ANLREQ.TO-RUN-FWD10-MULTICOMP-7I...`, committed d07a3e87dc), on the r34q resident once IB2 closes TO-APPLY-R34Q: two Opal models (`Opal Short-Term`, `Opal Long-Term`) ticked on the Ticket Center form, holdings `deliverables/2.0.0_SA_COO~G2/fwd10_holdings_7i.csv` (SPY 420, AGG 280, IWM 150, EFA 150; four public ETFs, the page's `Ticker,Dollars,Acct Market Value` shape). The ETF comparable is not exercised live (the catalogue holds the five Opal models only). The PDF is saved outside the repository at `C:/dev/andrew_samples/Opal_MultiComp_sample_FWD10.pdf`; the read uses `checks/fwd10_read.py` (model side) and by eye (portfolio rows, risk table, allocation). The CTO also asks the run to name the packager outcome and the audit outcome (msg 11854); the audit is expected wired but refused (the runner role cannot read `opal-tickets`), the attach standing.
