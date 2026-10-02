# IRPT_DASHBD FWD-1 -- the real run: a signed-in page reads a covered account's served series through the live route

Seat `2.0.0_SA_COO~D` (workstream F, FAST lease `IRPT_DASHBD~D`). 2026-10-02 06:26Z-06:28Z. Asked by `2.0.0_SA_COO~P` 104079 (the
read route live 05:52Z; this fetch closes its ledger `irpt-dashbd-reporting-read-apply-20261002` leg A1). CTO round-1 analysis
ADDENDUM 1 A2: FWD-1's real run is workstream F's signed-in fetch of the platinum series already served, its as-of shown with it.
No client name, account number or figure beyond the face's own return and dates is written here.

## How it ran

- The UI walker, signed in, on the local DEV build at `localhost:5174` (portal DEV `39b7a0fc`, plan item 5), against the REAL backend:
  walk `tmp/ui-walk/20261002T062634Z` (local, never committed). Walker armed and disarmed by itself (disarmed 06:28:38Z, a login with
  the walk password refused 401); `0.0.0_AB_MSTR` cleared the arm (104091) and was told DISARMED.
- One 49 Financial client with two accounts (the search text from `2.0.0_SA_COO~P` 104083, held in the gitignored inbox). The walk
  selected each account in the Performance tab's picker.

## What the route answered (the walk's own network log)

| request | answers |
|---|---|
| `GET /api/scoped/investor-reporting/reporting/<account>/manifest` | 2, both HTTP 200 (one per account) |
| `GET /api/scoped/investor-reporting/reporting/<account>/series` | 1, HTTP 200 (the covered account only) |

No fixture on any hop: the page's own fetch, the deployed route, the published platinum objects.

## What the page showed (screenshots read)

- **The covered account** (the thread account, shot 006): the dashboard figure INSTEAD of the tab's own -- "Total return, before
  advisory fees", YTD 6.10%, "January 2nd, 2026 to September 28th, 2026 -- 185 trading days measured", **"Data through September
  28th, 2026"** on the face beside the number (A2), two coverage sentences served by the file (one large-flow day; a partial history),
  the chart and its brush; the tab's own period presets hidden (one period chooser on the page).
- **The other account** (shot 007): its manifest read answered, no series read, and the tab's own figure stayed (its presets,
  its own report request) -- the switch reads the manifest's presence per account.

## Not measured, and why

- The time from the first byte to the painted chart and the requests after a date change (plan section 4): the default walk does
  not press the dashboard's presets or time the paint. A window change makes no request BY CONSTRUCTION (`DashboardPerformance`
  computes every window in the browser from the series it holds; it has no fetch), but that was NOT measured here; the fixture-plane
  run measured only that returning to an account re-reads nothing. A walker step for both numbers is the next instrument.
- The account picker's per-account suffix read "YTD pending" for both accounts at screenshot time (IRPT_BCKEND's figure, not the
  dashboard's): parked in `STATUS~D.md` (owner 1.0.0_SA_CTO).

## Addendum 08:13Z-08:15Z -- the two numbers plan section 4 asks for, measured (walker `--dashboard-window`)

The same client and the local DEV build at portal `8df9e3d3`, against the real backend: walk `tmp/ui-walk/20261002T081313Z`
(local, never committed; `dashboard-window.json` beside its `findings.json`). Disarmed 08:15:26Z, login with the walk password
REFUSED; `0.0.0_AB_MSTR` told before and after. The step starts its clock at the Performance tab's own press (the picker has no
"All accounts" entry, so the tab opens on the covered account), times every other account from its select, then returns.

| what | measured |
|---|---|
| covered account, tab press -> painted chart (a drawn area in the dashboard chart) | **5,288 ms** |
| of which `GET .../manifest` | sent at 639 ms, answered in 2,858 ms, HTTP 200 |
| of which `GET .../series` (sent when the manifest answered) | sent at 3,498 ms, answered in 1,698 ms, HTTP 200, **17,665 bytes transferred** |
| requests after each of the five window presses (1M, 3M, YTD, 1Y, Since inception), 1.5 s each | **0, 0, 0, 0, 0** (measured days 21, 64, 185, 251, 558) |
| the other account (no series served) | manifest 951 ms, no series read, the tab's own body at 2,800 ms |
| back to the covered account | 0 reads, chart painted in 85 ms |

So a window change is answered in the browser with no request (C-SERVE), measured and not only by construction. Opening the
account takes about 5.3 s, more than half of it the manifest route's own time; the page reads the series only after the
manifest says it exists, so the two reads run one after the other. The two date fields were not typed (the presets go through
the same selection path).

ITEM 1a UN-PARKS ON THIS WALK: the account picker's suffix read "YTD 3.62%" (IRPT_BCKEND's period figure, shot 007) on the
same page as the dashboard, whose YTD for this account read 6.10% at 06:26Z (data through September 28th, 2026). An account
is now served by both sources and the two figures disagree on one page. Asked of 1.0.0_SA_CTO (a design call).
