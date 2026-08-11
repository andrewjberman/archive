# DRAFT — for Andrew's review before anything leaves the building
# Explanation for the Inflection team: the advisor-dashboard asset figures

**Status: INTERNAL DRAFT. Not sent. Andrew edits/approves/sends.**
*(Written client-facing: no internal tool names, no agent serials, no repo paths. The numbers
are as of August 11, 2026 and will drift slightly day to day.)*

---

## What you asked about

Some advisor dashboard figures — most visibly the "non-fee-earning assets" number on an
advisor's profile — did not match the numbers in billing review. For one advisor the dashboard
showed roughly **$696K** of non-fee-earning assets while the billing-report view of the same
accounts showed roughly **$128K**. We ran this fully to ground. Here is exactly what those
numbers are, why they differed, and what we are changing.

## The short answer

**Both numbers come from the same Orion data, and neither valuation was wrong. The smaller
number came from a billing report that only "sees" accounts opened more than three years ago.**

The billing extract we were using asks Orion an *activity-report* question over a rolling
three-year window. Orion answers that question honestly — but for any account opened within
the last three years, the activity engine returns a blank rather than a value. Our pipeline
then treated "blank" as "$0," so every account opened since roughly August 2023 silently
dropped out of the billing-report sums.

This is not an Orion data problem, and it is not an account problem. We verified directly with
Orion that the affected accounts are active, reconciled, and in balance, with correct current
values — the account values were always right in the portfolio system. The gap was purely in
the *window* of one report extract, compounded by our side reading "no answer" as "zero."

## How we proved it (so you don't have to take our word for it)

- Across the whole book, every account the billing report valued matched its live current
  value **to the cent** — 485 of 485 accounts, on the same day.
- Every account the report showed as $0 while holding real assets — all 312 of them — was
  opened **after** August 2023 (i.e., inside the three-year window). Every populated account
  was opened before. Zero exceptions in either direction.
- The clincher: as the rolling window moves forward each day, accounts "graduate" into it on
  their three-year anniversary. We watched 27 accounts cross that line over the last four
  months — they began reporting values within a day or two of **exactly** their
  account-opening date plus three years.

## What it means for the numbers

- The dashboard's **$696K** figure for that advisor is the correct one: it is the sum of
  live current values across his non-fee-earning accounts. The $128K figure was the same sum
  with nine of his twelve accounts (about $568K, mostly recently-opened accounts) blanked out
  by the report window.
- The same window effect ran the **other way at firm level, and it is the bigger story**: the
  billing extract's *fee-earning* asset total read about **$137.2M**, when the live
  current-value figure across the same fee-earning accounts is about **$196.7M**. In other
  words, roughly **$59.6M of billed client assets** — essentially the accounts your firm has
  opened in the last three years — were invisible to that report. Growth was the thing the
  window hid.

## What we are changing

1. The billing extract is being re-based so account coverage no longer depends on account age
   (and where a raw current value exists in Orion, we use it directly).
2. "No data" and "zero dollars" are being made distinct in our pipeline so a blank can never
   silently read as $0 again.
3. Nothing was changed retroactively; no served number was rewritten as part of this
   investigation, and billing itself (fees charged) was never affected — this was a
   reporting-window issue, not a billing issue.

Happy to walk through any account-level detail with your team.

---
*Prepared by Opal Capital — internal draft v1, 2026-08-11.*
