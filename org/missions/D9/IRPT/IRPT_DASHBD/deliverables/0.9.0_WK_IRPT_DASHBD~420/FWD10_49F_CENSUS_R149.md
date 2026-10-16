# FWD-10 for 49 Financial, round 149 (DB-c-29) -- TEST READ, not a serve, not a production run

Counts only, from FWD10_49F_CENSUS_R149.json. No identifier or value is written here.

## 1. Where the data starts
- Both gold tables start in mid 2024 and end on the same final day; the census finds one partition per trading day across that span.
- Each published series starts on its own first recorded day. No series starts before the table start; about 59 percent start after it.
- A person needs the account's own start day. The page states it today: "Returns from <date>." is printed for every 49 Financial account, because every document carries history_scope PARTIAL_HISTORY.
- The page prints "This account's history starts on <date>; the window was shortened" only when a window reaches back before that day. It names no cause, as DB-c-24 requires.

## 2. Which trading days were not reported
- Gold census: zero absent trading days in either table across the full span. The statement a 49 Financial person could be given is "no trading day is missing from the source history".
- No published document carries both unreported_trading_days and its basis. The page therefore prints no "not reported by the source" sentence for any 49 Financial account.
- The page cannot tell "none missing" from "not measured": the sentence is absent in both cases. Nothing on the page says the check was made.
- Day-quality sentences are printed for almost every account (6,945 of the documents). Their NOT_MEASURABLE words say "the history has a gap here", which a reader may take for an unreported day. They describe a partition that holds no measurable return, not a day the source did not report.

## 3. How current the data is
- The as-of day is the same day the gold tables end on for nearly every document; three documents carry an earlier as-of day.
- The page prints "Data through <as_of>" on the Performance panel, so a person can read the date off the page.
- No series is behind the gold layer except the three older documents.

## What looks wrong or unexplained
- Every document carries numeric income entries; the round-148 Cottonwood publish carried none. The page reads them without coercion (0 coerced).
- No document carries income_claim, and no document carries the unreported-days pair. The 49 Financial publish does not carry the shape the Cottonwood publish carries.
- Under the series prefix there are about 4,300 objects that are neither series nor manifest documents. Their kind was not established: the read is bounded to series objects.
- history_scope is PARTIAL_HISTORY for every document, including the documents whose first day equals the table start. The scope flag does not separate them, and "Returns from" is printed for all of them.
- performanceView prints day-quality words but not the history_scope words in coverageWords.ts. The partial-history statement reaches the page only as "Returns from".
- Consistency check that holds: the return_basis NOT_MEASURABLE total equals the day_quality NOT_MEASURABLE total plus the FLOW_UNRECONCILED total, as the coverage words imply.
