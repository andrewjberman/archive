# DSGN_IRPTV1 -- window 2 of the admin + Dev walk, 2026-09-26: K6, the export-B BEFORE read

**Walker:** 2.0.0_SA_COO~D. **Packet:** v7 blob 3edebd85 (both halves at HEAD; ledger irpt-uiwalk-principal-w2-20260926,
operator 2.0.0_SA_COO~P). **Principal:** irpt-uiwalk-1790435397@opal.test, created 15:10:02Z, deleted 15:26:02Z (P 101281).
**Login:** 15:14:06Z. **Post-delete reload:** landed on /login at 15:28:55Z (1 of 1).

## K6

- Target: a single-account 49financial client. The directory search returns relationships only; the account count shows only
  after a selection. Four selections were made on the Holdings tab (each a page `POST /selections`, K3, retained):
  ANTHONY DALE REID (3 accounts), HOPE SMITH ****4033 (2 accounts, "2 without account details" -- no narrowing offered),
  JASON JONES ****9978 (1 account), KAY SMITH ****5910 (2 accounts). A guard in the script opened Performance only for a
  1-account selection.
- JASON JONES ****9978 (49financial, 1 account): Performance opened ONCE at ~15:22Z; exactly 1
  `GET /api/scoped/investor-reporting/performance/sel_750b3096b55a093c3c08589ba7e05a1b75fca1abf144442409f28fa16d5f6868` fired.
- **The answer is NOT in the browser record.** The GET had not answered within the script's 15 s wait, and the next probe's
  page load cancelled the browser side; the HAR holds no entry for it. No second GET was made (K6 admits ONE). The answer
  (status, ok, state, reason, section count; REPORT#/RETENTION# rows if a 200 retained) is read server-side by 2.0.0_SA_COO~P
  from the IRPT log and irpt-requests (asked 101262-thread, 15:25Z).
- Lesson for the next K6-style read: wait on the response itself, not a fixed timer.

## HAR and audit

`prod-uiwalk-w2-20260926.har` (this folder, gitignored at .gitignore:353 -- read in place; sha256
`8db22a19c954604d78590a97eb2f51f5828a524deecf489111d908ed2dd0de52`), written scrubbed in-stream by owner3.mjs, leak checks clean.

| class (denominator 469) | count |
|---|---|
| GET / HEAD / OPTIONS | 444 |
| POST /auth/refresh | 11 |
| POST /auth/login | 1 |
| POST directory/resolve | 9 |
| POST selections (K3) | 4 |
| outside the admitted classes | 0 |
| `/auth/admin/` | 0 |

The browser-side write guard kept 100 `POST .../prod/analytics/ingest` telemetry calls off the network.

The pause (Andrew-direct via CTO 101279, 15:27Z) arrived after K6 had fired; only the safety closure (reload, HAR close) ran
under it.
