# Part Y arms for the NEXT Analysis window -- the four carried report arms, plus the S206 discriminator

Author `2.0.0_SA_COO~Y`, 2026-09-29 ~15:3xZ. Successor to `W22_PART_Y_ARMS_20260929.md` (@ac0eade564).
The window number is `2.0.0_SA_COO~P`'s to assign (W23 is taken by ~D's directory-search window, ledger
`irpt-ui-walk-principal-w23-20260929`, so W24 at this writing). **Written ahead of the ask so that no packet
waits on this lane:** ~P can cut whenever an Analysis slot opens.

**Precondition:** the resident st4 root and the generate pin as ~P re-reads them at create. If any pin differs at
create, the window does not open. Nothing here needs new code -- every arm runs on tooling already served and already
exercised in W22.

**Tools:** `live_chain.py` @78c8ce05a6 with `WALK_PW_RETAINED=1`; `case_trace.py` @f86dc994b9; `job_watch.py`;
`resident_journal.py` (SSM, read-only). One login, one K4 and at most one K5 per body. No retry. A challenged vendor
mutation is never replayed.

## Why this window is not a repeat of W22

W22 spent five submissions and produced ONE report. Three bodies died `RESOLVE_RETRY_EXHAUSTED` and a fourth died
`SESSION_REFRESH_ALREADY_USED`, leaving four report arms unexercised. Rows `IRPT_BCKEND-S206` (@befabb9a7b) and
`IRPT_BCKEND-S207` (@827cbc166f) measured why, and both point at the same thing: **a second resolve in flight**.
Across W22's denominator of 5, every body that resolved READY was the first after an idle gap, and every body dispatched
while another resolve was live exhausted after four `PROVIDER_READ_UNAVAILABLE` receives -- including the identical CSV
that had resolved in 1 s fourteen seconds earlier.

So this window changes exactly one thing about how the bodies are driven, and adds a deliberate arm that settles
whether that change is the right one.

## A. The four carried arms, SERIALIZED (bodies 1-4)

**Serialization rule, the one change from W22:** body `N+1`'s K4 is not POSTed until body `N`'s `NORMALIZATION#` row
reads a terminal state (`NORMALIZED` / `NEEDS_CORRECTION` / `FAILED` / `REFUSED`) by consistent Query, plus a 20 s
floor. `live_chain.py` already blocks on that row, so serialization is achieved by running the four bodies
sequentially in one shell, not by any code change.

| # | body | firm | K4 arm | the arm it closes |
|---|---|---|---|---|
| 1 | Multi-Comp `opal_short_term`,`opal_intermediate_term` (CSV) | cottonwood | W15 CSV | W21 Y2 / W22 Y2 -- both models printed, or `COMPARISON_NOT_PRINTED` |
| 2 | Target Weight, notional 1000 (XLSX) | cottonwood | `aapl-vnq-target-weight.xlsx`, `WALK_REFERENCE_NOTIONAL=1000` | W22 Y3 -- the REPORT. The vendor half is already proven (W22 echoed `AAPL 600.0` / `VNQ 400.0` Dollars, `upload_record_id 780748`, `model_portfolio_id 2367113`); only the PDF and certification are owed |
| 3 | Overview (CSV) | 49financial | W15 CSV | W21 Y6 / W22 Y4 -- the FIRST certified 49financial report |
| 4 | Overview (CSV) | inflection | W15 CSV | W21 Y5 / W22 Y5 -- a certified Inflection report |

Bodies 3 and 4 go through the foreign-firm name check (the CRO's standing condition 3). In W22 that check ran and
passed on the cottonwood PDF only, because neither foreign-firm body ever reached K5.

## B. The S206 discriminator (bodies 5-6), run LAST

After body 4 is terminal, **two Comparison bodies on `opal_long_term`, cottonwood, dispatched SIMULTANEOUSLY.** The
shape is the one W22 already proved works solo (W22 Y1 -> READY -> `RPT-2e21b52e..`), so the only variable is
concurrency.

- **Both exhaust `RESOLVE_RETRY_EXHAUSTED`** -> S206 CONFIRMED. `PROVIDER_READ_UNAVAILABLE` is a concurrency refusal,
  its `REPLACE_FILE` remedy is wrong for that code, and the serialization rule in section A is the correct operating
  discipline until the resident's provider read is made safe under concurrency.
- **Both resolve READY** -> S206 REFUTED, and W22's three exhaustions want another explanation. Say so plainly and
  re-open the row.
- **One of each** -> single-flight confirmed at a finer grain than S206 claims; record which one won and its ordering.

This costs two submissions and is the cheapest way to turn S206 from a correlation over 5 bodies into a deliberate
mechanism with the organic case as its negative arm. It is a READ: it deploys nothing and writes only rows the
principal owns.

**Cap asked: 6 submissions** (4 serialized arms + the 2-body discriminator). W22's cap was 5.

## C. How every terminal state is read (from S207)

**The resident journals NO line for a job ATTENTION.** Over W22's 14:08-14:34Z span the journal carried 79 lines, every
one `IRPT_RESIDENT_POLL`, while `REQ-51f1413b..` moved to ATTENTION `SESSION_REFRESH_ALREADY_USED`; the code existed
only in `irpt-jobs`. So, per body:

1. the `NORMALIZATION#<upload_id>` row in `irpt-requests`, consistent Query -- `state`, `reason`, `findings`,
   `dispatched_at`, `resolved_at`;
2. the `irpt-jobs` row by `tenant` + `job` -- `state`, `job_detail.code`, `outbox_state`, the `intent_*` claims with
   their `claimed_at` and fence;
3. `case_trace.py <firm> <REQ>` on every body that reaches a report;
4. the `IRPT_RESIDENT_RESOLVE` lines by SSM for the window span, as corroboration, **never as the oracle**.

A named terminal state, READY or an ATTENTION with its code, is a pass. A hang past the cap is not.

## D. What ~Y needs from ~P's packet

The walk principal (K1, credoff and delete at the cap), the window's time bounds, and both halves -- as W22's packet
(`1f3bf0914f` @6550c62cdf). Plus **the cap raised to 6** for section B, or a one-line refusal of section B, in which
case the window runs sections A and C alone and S206 stays a correlation.

The DLQ message count is read before and after, as always; any growth over the pre-existing 1 is a BLOCKING row.
