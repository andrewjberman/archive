# AMGT_CORPUS round 37 CRPS-am-2 leg v -- TSM's Model tab after the re-derive

## The walk (two slots from MSTR~Z on the laptop's Y-6 hold; ARM/DISARMED relayed both times)

- **Slot 1 (13:43-13:48Z): read nothing.** My start command chained `git rev-parse ... origin/DEV` before `bun run dev:live`. The
  rev-parse failed (exit 128), so the server never started; the walk took 0 screenshots. DISARMED 13:48:01Z.
- **Slot 2 (13:53-13:57Z):** the server was verified 200 first. Walk `tmp/ui-walk/20261005T135401Z`: 15 screenshots, 0 guard aborts,
  0 API issues, DISARMED 13:57:00Z (login refused). **But every tab shot, Model included (`012`, `013`), is covered by the news
  timeline's "October 3rd, 2026" day popup** that the walk opened at step 005 and did not close. The sheet is not readable in this
  walk. This is a walk-instrument finding for the /ui-walk owner, not a page defect of am-3 or am-2.

## The seam read instead (the real served payload through the real page builder)

- **Served:** the DEPLOYED `opal-amgt-scoped-api` (`2rFeF57l`) `/thesis` for TSM_US_Equity, invoked through RESAPP's capture
  helper. 400 fiscal figures, 200 of them money (unit MILLIONS / ABSOLUTE / PER SHARE, not a share count). 200 of 200 carry a
  currency: TWD, the reporting currency.
- **Built:** that payload through the REAL `portal/src/pages/SecurityAnalysis/modelSheet.ts` at portal DEV `2e7c5cdb` (the
  page's own builder; `ModelTab.tsx` prints `row.currency` beside the unit words, round-37 am-3, CTO-reviewed). **13 of 13 money
  rows name a currency**, e.g. EPS / DPS / EBITDA / EBITDA (adjusted) -> TWD; 0 rows are left with the "currency not stated" mark.
  At round 37's cut, the same 13 rows exposed 1 (am-3 fixture, TSM before am-2).
- **For the CVO (am-1 AC3, the judgment):** every TSM money row reads TWD, including per-share EPS and DPS. TSM is a US-listed ADR
  whose filings are in TWD, so these are reporting-currency values per ordinary share. That is the producer's rule; whether it is
  the right side for each field is the open AC3 judgment, as is row Z-W1-S34 (HISTORICAL_MARKET_CAP).
