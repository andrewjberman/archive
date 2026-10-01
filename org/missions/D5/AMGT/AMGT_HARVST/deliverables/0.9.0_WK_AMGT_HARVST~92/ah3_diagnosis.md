# ah-3 diagnosis -- why 91% of ft body fetches came back locked (0.9.0_WK_AMGT_HARVST~92)

Subject: run record `.runtime/opal-data-harvest/runs/20261001T123436Z-ft-a76fabb550.json` (ASML, 12:34-15:01Z, 416 body
fetches, 61 stored). Sources of the two root causes: commit 146e2c4c0e (session) and fe204a851f (tier); both merged @a78b06d3e6.

## Signatures in the record (416 fetch outcomes, printed denominator)

| outcome | issues | n |
|---|---|---|
| rejected | publisher_did_not_unlock_body + short_or_partial_body + missing_metadata + invalid_publication_date + company_not_mentioned | 322 |
| stored | none | 61 |
| rejected | company_not_mentioned only | 27 |
| rejected | company_not_mentioned + short_or_partial_body | 6 |

The 322-row signature IS the barrier page: no title, no date, no body, no company mention. The share is 322 of 416 = 77%
of fetches carrying `publisher_did_not_unlock_body` (the 91% in the order counts the 324-of-357 REJECTED, a different
denominator). It is an access problem, not relevance.

## Root cause 1 -- a dead session (a real defect, fixed)

Saved pages show `isUserLoggedIn` true for the first ~150 fetches and false for the remaining ~266: the login died
mid-job and the job kept fetching barriers. In fetch order (record dict order; the ~150 boundary is the saved-page
observation in 146e2c4c0e):

| stretch | fetches | locked (did_not_unlock) | stored |
|---|---|---|---|
| logged in (first 150) | 150 | 76 (51%) | 48 |
| logged out (remaining 266) | 266 | 246 (92%) | 13 |

The profile jar's `FTSession_s` was dead and `TabSession.seed` never replaced a cookie whose name the jar already held,
so the bundle's live cookie never reached the page. Request mode is the in-tab `fetch()` of `/content/<uuid>` with the
page's own cookie jar (status 200 in `request_attempts` for every row -- the barrier is served as a 200 page, never an
error status). Fix: `publishers.ft_page_state()` classifies barrier + `isUserLoggedIn` false as AuthExpired (the worker
renews once, or stops under `--no-sign-in`); `tab_transport.logged_in()` + `seed` replace FTSession/FTSession_s only when
the loaded page reads logged out. A free page with no body (a live blog) is no longer counted as an unlock failure.

## Root cause 2 -- the Premium tier the account does not hold (a COVERAGE LIMIT, not an unlock)

After fix 1 a live ASML run held a logged-in session and 10 of 43 body fetches were still the barrier. All 10 were
listing teasers carrying ft's `o-labels--premium` label (35 of 35 on the earlier logged-in barrier stretch). A logged-in
session on this account cannot read FT Premium content; no request mode changes that. This is NOT an unlock: those
articles stay unreachable. The fix (`contracts.json` `skip_premium_labelled`, `financial_times()`) skips them BEFORE the
body fetch and notes each as skipped (why `premium_tier`). Fewer wasted fetches, same coverage -- the locked share falls
because the fetches are not made, and the premium articles are a stated gap in ft coverage.

## What was not the cause

- credentials mode / a cross-origin redirect to accounts.ft.com: not observed; every attempt is status 200 on
  www.ft.com with the barrier in the body.
- a barrier served to `fetch()` but not to a navigated page: not distinguishable in the 200-with-barrier rows alone and
  not needed once the logged-out stretch is explained by a dead cookie.

## Plants

`lib/opal_data_harvest/test_ah3_ft_unlock.py` (12 plants); collector suite 480 passed, 1 skipped (base 468).
`ah3_run_after_fix1_partial.json` is the in-flight record of the post-fix-1 ASML run (43 fetches) that exposed cause 2.
