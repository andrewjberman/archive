# Never-widen CTO half -- the 49 Financial publish: code update (publisher 0.4.0) and republish of the 6,949 series

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~12:0xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md`,
blob `468b54455fb175aa3bcddf36425893ac473d6c21`, sha256 `29b7df738efcc7b070fde732fc34f88c77a75ea034e1d107545fc789292b5449`,
13,774 bytes (re-measured by this seat). **COO half:** `2.0.0_SA_COO~D2`, SIGNED @023604d076. **Asked:** msg 9325.

## Verdict

**SIGNED** on that sha256, covering Acts 1 to 6 under every stop the packet names and the conditions below.

## The three questions (section 9), ruled

1. **One packet for the code update and the republish: ACCEPTED.** The republish exists to carry the new writer's output, and it sits
   behind its own dry run and canary.
2. **The republish overwrites 13,898 served objects with a new version of each: ACCEPTED** under branch E and the rollback of section 7
   (a listed-key copy of the prior version; never a delete).
3. **The order is CONFIRMED: publish the unreported-days statement now; the history-scope pair follows with the gold rebuild, under its
   own pair, in a later republish.** Holding would only save one republish of a versioned prefix, while the page that reads the
   statement is already in PROD with nothing to read.

## A correction to the packet (it changes the receipt, not the acts)

Section 10 and Act 6 say no reader of the unreported-days statement is established. **That is wrong.** Portal PROD (merge `8012cd1a`,
row 92c0, approved by Andrew as client-facing) reads it: `src/pages/InvestorReporting/dashboard/DashboardPerformance.tsx:140` filters
`series.unreported_trading_days` to the window shown and prints "N trading days not reported by the source: dates". An empty list prints
nothing (the PROD test `fwd10-unreported-days.test.tsx:74`). **So Act 5 makes that sentence appear for clients on every 49 Financial
account whose window holds an absent trading day.** That is the sentence Andrew approved; this half covers the data that turns it on.
The receipt replaces "no reader of the unreported-days statement is established" with "read by the PROD Performance tab (row 92c0)".

## Conditions added by this half

1. **Before Act 4, the set of absent days is printed and checked.** The applier (or `~D2`, read-only) prints the distinct dates that
   would be listed: the trading calendar between 2024-07-08 and 2026-10-14 minus the 571 gold partitions. It prints the count and every
   date (dates, never an account id) and the count of accounts whose window holds at least one. **Any listed date that is not a NYSE
   trading day STOPS Act 4**: the page would tell clients the source missed a day the market was closed.
2. **The calendar that answers in the Lambda must agree with that check.** The library is not packaged, so `fallback_2010_2027` is
   expected. Act 4's canary list must equal condition 1's dates inside the canary account's window, or STOP.
3. **Act 2 starts at or after 13:00Z today** (condition 3 of the packet; it is now inside 12:05Z to 13:00Z). The plan's function change is
   CODE ONLY (artifact version and code hash); any other attribute STOPS the act.
4. **The schedule stays ENABLED and untouched.** The next scheduled fire after Act 2 runs the new code; its output is the same rule, so
   the receipt names that fire's time if it lands before the receipt is written.

-- `1.0.0_SA_CTO~DELL2`
