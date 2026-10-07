# BD morning run vs evening run -- the shape, confirmed before anything is switched off

`NFRA_MCPINDEX.TO-MX-a-1` | `0.7.0_AE_CloudOps~MI` | measured 2026-10-06 20:05-20:45Z | read-only, no call to Black Diamond
Figures and citations: `BD_RUN_SHAPE_COMPARISON.json` beside this file.

## Your three questions

**Is the morning run a REST API?** Yes. It is a clean four-call REST flow against Black Diamond's
DataMining API at `https://bd3.bdreporting.com` -- get a token, post a saved query, poll until it is
done, download the spreadsheet. No browser, no portal login, no Playwright anywhere in it. It signs in
with a saved session cookie out of Secrets Manager that a keepalive refreshes every 15 minutes.

**What fields and data come back?** Four tables, and they are wide. Transactions 71 columns, 5,144 rows
on the day I read. Allocations 92 columns, 34,505 rows. Unrealized 15 columns, 500,000 rows.
Realized 13 columns, 8,530 rows. Full column lists are in the JSON. These are not thin extracts --
transactions alone carries the advisor split percentages, the fee and tax fields, client city/state/zip,
the account and relationship identifiers and the asset identifiers.

**Does BD stamp its own as-of anywhere?** Yes, and this was the thing worth finding. Every
spreadsheet BD sends has a **second worksheet called `Timestamps`** that BD writes itself, carrying
`Created (Eastern)` -- BD's own generation time -- plus the template name and the exact window BD
actually ran. Example from the transactions file: `Created (Eastern) = 10/3/2026 8:02:14 PM`, which
matches our own landing record to within two seconds. On top of that, transactions and allocations each
carry an `As of Date` **column** that BD fills in. So the provenance is genuinely BD-side, not ours.
Two caveats, both measured: the pipeline reads BD's `End Date` from that sheet to date the file and
keeps `As of Date` as a column, but **`Created (Eastern)` is thrown away** and never reaches silver;
and the code never looks at HTTP response headers at all, so if BD stamps anything there we cannot see it.

## The evening run

**It does not touch Black Diamond.** I read the live served version of both SSM documents (version 3 of
3, the one actually running, not the repo file). The only two things either one downloads are a Python
script and a library folder out of our own S3 bucket. The Playwright portal download was taken out when
BD added MFA in June; the documents say so in their own comments. So the evening run is not a second
source of data. It is a second program that re-reads what the morning run already landed.

**And it is not even the same program.** This is the part the earlier picture had wrong. The evening run
uses a copy of the merge script frozen on **2026-06-29**; the morning run uses a copy updated
**2026-10-01**. 43KB against 60KB, 695 lines different. Both write to the same silver tables.

**What it actually does, day to day.** On roughly two days in three it finds nothing to do and exits --
the morning path got there about 22 hours earlier. Its only real work is on the days the morning path
deliberately holds back, which measured as 11 of the 34 days from 3 September to today, almost all
Mondays and Tuesdays. On those days BD has not posted transactions yet, the morning run correctly
refuses to advance, and the evening run is the only thing that merges same-day.

## Is the evening run richer? No -- it is the same or thinner

I compared a partition the morning wrote against one the evening wrote, same table, column by column.

- **Realized: identical.** Same 15 columns, same order.
- **Transactions: the evening output is MISSING a column the morning output has** -- `cusip`, 73 columns
  against 74. Its own log says why: `bd_assets_dim unavailable; skipping cusip join`.

**Nothing exists in the evening output that is absent from the morning output.** The only difference runs
the other way. On every axis -- source, table coverage, schema width, code vintage, completeness
checking -- the morning run is in better condition.

## Verdict: yes, the evening run can go -- but not today, and not first

It is extraneous as a *source* and as a *schema*. It is not yet redundant as a *scheduler*: it is still
the only thing merging Monday and Tuesday data on the same day. Switch it off now and Monday/Tuesday
silver arrives about two days late.

The fix for that is already built and sitting on a branch -- `MX-s-18`, which teaches the morning runner
to decide completeness itself so it covers Mondays and Tuesdays too. It has **not** been applied, and it
is blocked on one small IAM grant: the runner's role is currently allowed to *write* its completion
marker but not to *read it back*, which is the one thing `MX-s-18` needs. That decision sits with the COO.

**Order of operations:** land `MX-s-18` (after the IAM grant) -> watch one real Monday and one real
Tuesday fill in on their own -> only then disable the two evening schedules -> wait a week -> retire the
Lambdas and the SSM documents. Disabling a schedule is reversible; deleting a document is not.

**One thing not to touch:** there are **three** separate EC2 boxes here, not one. A third document,
`opal-bd-asset-dim-download`, is live on its own box and must keep running. Decommissioning the two
evening documents cannot strand it -- but only because it is a different machine, which is worth knowing
before anyone terminates anything.

## Separately, found while looking: the morning run has its own gap

Two of its four tables -- **allocations and unrealized -- have landed only once a week since 10 July**,
always a Friday snapshot picked up on the Sunday run. Twelve consecutive weekly gaps. The cause is
measured, not guessed: the run fires at 00:00Z, which is 8pm the previous evening in New York, and it
asks BD for a snapshot only about four hours old. BD returns an empty export and the pipeline correctly
refuses it. Only the weekend run, which asks for the Friday, gets a snapshot old enough to be complete.
This is nothing to do with the evening run and switching the evening run off neither causes nor fixes it.
It is filed on the surprise channel for the COO to own.
