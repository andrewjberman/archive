# DSGN_IRPTV1 -- window 4 of the admin + Dev walk, 2026-09-26: K7 (the page read) and K8 (the first export)

**Walker:** 2.0.0_SA_COO~D. **Packet:** v10 blob 32c85e40 (CTO half stands 101403/101406; CRO half @bc1481a8be); ledger
irpt-ui-walk-principal-w4-20260926 (operator 2.0.0_SA_COO~P). **Principal:** irpt-uiwalk-1790446664@opal.test, created 18:17:54Z.
**Login:** 18:19:56Z. **Post-delete reload:** landed on /login at 18:25:50Z (1 of 1).

## K7 -- the page read K8 would export

- JASON JONES ****9978 (49financial, 1 account, $852,918.93) selected on Holdings (one `POST /selections`, K3, retained).
- Performance opened once: ONE `GET /api/scoped/investor-reporting/performance/sel_750b3096...?start=2026-01-01&end=2026-09-26&selected_tenant=49financial`.
- Answer in 5.5 s: HTTP 200, `ok: false`, state `UNAVAILABLE`, `public_reason_code: OBJECT_NOT_COVERED`; no report id; no report rendered.
- v10 passes K7 only when a report renders, so **K7 did not pass and K8 did NOT run** (no export POST left the browser). No retry: the
  packet admits one read plus one reload on a gateway cutoff, and this was not a cutoff. CTO 101422: "Correct stop".

## What the refusal was (corrected)

- First reading (this seat, 101419): the page's YTD preset ends on the browser's calendar date (2026-09-26), past the data's as-of date.
  The CTO ACCEPTED the fix as a round-6 item (101422): every period preset ends on the data's as-of date (IV-e-34 amendment 1 @6178d55e99).
- **Correction (CTO 101428):** the K7 refusal itself was the backend REOPEN authorization check (P-REOPEN-01): a second viewer of an
  account and window with a retained report is refused, and the refusal is mislabelled OBJECT_NOT_COVERED. The old build's logs show the
  same denial, so it is not a regression of export B's D1. 2.0.0_SA_COO~P builds the fix under a never-widen half. The preset fix
  still stands on its own merits.

## HAR and audit

`prod-uiwalk-w4-20260926.har` (this folder, gitignored at .gitignore:353 -- read in place; sha256
`e217c72eb90a08b9d6d33a6bcee7c6598ea1515e33eac982f6dc0d72518c85b0`), written scrubbed in-stream by owner4.mjs (its guard admits exactly ONE
POST /export; none was sent). Leak checks clean.

| class (denominator 113) | count |
|---|---|
| GET / HEAD / OPTIONS | 107 (the ONE K7 performance GET among them) |
| POST /auth/refresh | 3 |
| POST /auth/login | 1 |
| POST directory/resolve | 1 |
| POST selections (K3) | 1 |
| POST export (K8) | 0 |
| outside the admitted classes | 0 |

The write guard kept 37 `POST .../prod/analytics/ingest` telemetry calls off the network.
