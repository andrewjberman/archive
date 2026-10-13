# Black Diamond's own help text on how external cash flows are timed in a daily return -- the read (2.0.0_SA_COO~D2, 2026-10-13 ~12:3xZ-12:5xZ)

**Ordered by:** Andrew-direct card 5 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_122xZ_ANSWERS_TO_NINE_DELL2_CARDS.md`, call `dell2-20261012T205030Z-e41e`): the question is
answered by an agent reading Black Diamond's own method help with the stored signed-in session; nothing is sent; no client data. Relayed by 1.0.0_SA_CTO~DELL2 msg 6907.

## The answer, in Black Diamond's own words (claim: MEASURED, read from the vendor's help center at the times above)

**Source A -- "Performance Calculations"** (`https://learn.bdreporting.com/article/97-calculations-performance-calculations`, page title "Performance Calculations - Black Diamond"):

- "Black Diamond calculates daily performance returns, adjusted for cash flows. The **default** performance return calculation is as follows: **Beginning of Day Additions, End of Day Withdrawals**"
- "Most scenarios with a positive Net Additions will utilize the following calculation: (EMV - BMV - Net Additions) / (BMV + Net Additions)"
- "If there is no Net Additions or a negative Net Additions, we will utilize the following calculation: (EMV - BMV - Net Additions) / BMV"
- "Option to use a different calculation methodology, upon request: **All End of Day Cash Flows**"

**Source B -- "Time-Weighted Rate of Return"** (`https://learn.bdreporting.com/article/99-calculations-time-weighted-rate-of-return`):

- "For a given performance period, TWRR is calculated by linking a group of holding period returns. Black Diamond treats a holding period as equal to one day. The Beginning Market Value for each day
  incorporates any external flows from the previous business day."
- "The HPR formula is dependent on the Net Additions for the day": negative Net Additions `(Ending Market Value - Beginning Market Value - Net Additions) / Beginning Market Value`; positive Net
  Additions `(Ending Market Value - Beginning Market Value - Net Additions) / (Beginning Market Value + Net Additions)` (the same two formulas as Source A).

**What the two pages say together.** The default is asymmetric: a positive flow (an addition) is weighted as if it arrived at the START of its day (it enters the denominator with the beginning value); a negative
flow (a withdrawal) is treated as arriving at the END of its day (the denominator is the beginning value alone). The vendor offers one alternative on request, all flows at end of day.

## What the pages do NOT say (not established)

- **Which of the two conventions the 49 Financial firm's Black Diamond account actually uses.** The page states the default and an on-request alternative; the firm's own setting is not on the help pages.
  A reader cannot settle the tie-out from this text alone; the firm's setting would have to be read from the firm or asked of the vendor (not done, and nothing was sent).
- How the "previous business day" sentence in Source B reconciles with the "Beginning of Day Additions" default in Source A (the pages do not reconcile them; this record does not either).
- Any statement about weekends, holidays or flows on a non-business day (not searched for; the patterns used were about start, beginning, end, close and open of day or period, flow timing and assumptions).
- Quotations above are the page text with the figure dash and bold marks shown as plain "-" and `**`; read the page for exact typography.

## Method and what was read (GET only; nothing written, nothing sent)

- Credential: the stored 49F session, Secrets Manager `blackdiamond/49f/session` (a cookie jar of 7 cookies, `captured_at` 2026-09-28; it still authorised the requests 15 days later). Read in-process by
  `bd_flow_timing/bd_help_read.py` (this folder; the repo path derived, not typed). **No cookie value was printed, written or kept**; only cookies whose domain is `.bdreporting.com` were sent, and only to
  `*.bdreporting.com` hosts. The existing daily pull's Terraform names the same secret; this box's AWS profile was permitted to read it, and no IAM was changed.
- Pages read, in order: `https://bd3.bdreporting.com/` (the app root: status 200, title "Black Diamond", used only to find where help lives; only the domain names and three configuration key names found in its HTML were printed; no page text or client content was printed or kept; the app's
  own configuration names `docs.bdreporting.com` and `learn.bdreporting.com`); `https://docs.bdreporting.com/` (status 200, title **"Vault"**: that host is Black Diamond's client document vault, NOT help. Only its title was
  printed; nothing from it was read, listed or kept, and it was not fetched again); `https://learn.bdreporting.com/` and two searches on it (time-weighted return cash flow; performance calculation methodology), which are the
  help center's own pages; then five help articles: 97, 99, 1062 (Performance Returns Overview), 1782 (Transaction Editing: Changing External Flow Effects), 105 (Counterintuitive Returns). Only articles 97 and 99 carried a
  statement on flow timing; 1062, 1782 and 105 matched none of the timing patterns searched.
- Without the session both documentation hosts redirect to the vendor's sign-in page (read with no credential first, status 200 at `login.bdreporting.com/Auth/SignIn`), so the session was needed.
- Client data: none read. The help center holds vendor text only; the one client-bearing host (the Vault) was touched once, title only, as stated.

## Why this matters to IRPT_DASHBD (stated, not decided here)

The round-86 section 4 question was "the other system's written statement of its flow timing". Sources A and B are that statement. Whether they decide the tie-out is not for this seat: the CTO's round-86 rule is that no read by a
seat decides it, and the firm's own setting (above) is open.

-- 2.0.0_SA_COO~D2
