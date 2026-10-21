# FIDUPL probe 2 (CTO msg 9076): the Historical Prices & Positions wizard and its create call, read-only (2026-10-21)

Author 2.0.0_SA_COO~P1, 2026-10-21 ~12:25Z. Names, shapes and counts only: no account number, G number, group name, client name, cookie or token.

## Boundary and session

- ONE agent-driven sign-in at 12:07:46Z on the warmed agent profile (four public pages browsed 12:03:36-12:07:14Z: slow scrolling, mouse wander, no form): `outcome=SIGNED_IN` (password, code, authorize all true; no 403). Logged out 12:20Z, statuses `204,400`. The session count in the trailing hour was two others (11:05Z one-shot, 11:20Z backfill).
- The walk reached the page `.../app/tools/portfolio-exports/historical` (frame `/ssc/importexport/appcontent/historical/index-v26.9.1.S1.html`) and, for the Group question, the Custom wizard's page of **step 4 (Create File)**. **No Run Export, Save and Exit, Next on step 4 or Verify was pressed.** The browser blocked every non-GET to the import-export service (`BLOCKED writes: []`: none attempted). Form state only: the calendar date was set to 16-October-2026 once; the Custom wizard held one placeholder export name and file name and ONE existing first-name Group (selected by index, never named here); both tabs were closed unsaved.
- The create call was NOT captured on the wire; it was read from the page's own JavaScript (`/ssc/importexport/appcontent/common/bundle-v26.9.1.S1.js` and `.../historical/bundle-v26.9.1.S1.js`, public app code), which is the stricter boundary.

## What the Historical Prices & Positions page offers

- **Date:** one date from a calendar; the page text reads "Dates displayed in calendar (120 dates prior to current date)"; the code sets the minimum to today minus 120 days and the maximum to yesterday (the default is yesterday).
- **Export Format:** Standard Format A, Standard Format B, Custom (values `'1'`, `'2'`, `'3'`).
- **Export Data Using:** Account Number or Custom Name (indicator `'AN'` / `'CN'`).
- **Export Type:** Positions & Balances, Prices (Format A; Format B has a positions-and-prices or prices choice). With Custom, the saved custom profile decides which of positions and prices are allowed.
- **Buttons:** "Cancel without making changes", "Run Export". Success shows a confirmation modal (the file is produced asynchronously; where it appears, by the Export Status list, is inferred and not measured).

## The create call (read from the page code)

`POST /ssc/importexport/<prodContString>/export/v1/historicalExport.json` (the sibling calls on this login use `wc/channel`), JSON body, keys:

| key | value |
|---|---|
| `profileId`, `profileName` | empty for Standard A and B; the chosen saved custom profile's id and name for Custom |
| `exportFormat` | `'1'` Standard A, `'2'` Standard B, `'3'` Custom |
| `historicalDate` | `MM/dd/yyyy` |
| `fileFormat` | `'FL'` for Standard A and B; empty for Custom |
| `fileTypes` | Standard A: `PBL` (positions and balances) and/or `PRC`; Standard B: `PRC` and/or `POS`; Custom: `POS` and/or `PRC` |
| `indicatorName` | `'AN'` or `'CN'` for Standard; empty for Custom |

Positions, balances and prices only: **no accounts, securities or transactions file exists in this wizard.** Reach: **120 calendar days** back from today (on 2026-10-21: 2026-06-23 to 2026-10-20).

`GET .../export/v1/profileList.json` answers 200 with **3 saved custom export profiles** (keys `profileId`, `profileName`, `profileDesc`, `prices`, `positions`): a Custom historical export can reuse one of them to get the custom layouts. `GET .../firmCustomProfiles.json` stays at 0.

## The one-off Group export (CTO msg 9013/9022) cannot be made without saving a profile

The Custom wizard's step 4 (Create File) offers only "Create Files On Demand" (run later from Saved Exports) and "Create Files Automatically" (an Export Status download); both are SAVED export profiles, and the only buttons are Cancel without saving, Save and Exit, Previous and Next (to Verify). There is no run-once path that leaves no profile. The Group filter therefore reads as a property of a profile: it needs a profile to exist. That is a vendor-configuration act under Andrew's name (CTO ruling 9003 item 3); this walk stopped on the page of step 4 and created nothing.

## Not measured (what a live historical export would show)

How the request's output is named and where it appears (the Export Status list for the REQUEST day, or for the historical date), the layouts of `PBL` against the custom `position.txt`/`prices.txt`, any per-day limit, and whether `Custom` accepts the daily's saved profile. ONE historical request from the box session (a real read, outside the standing export, e.g. historicalDate 10/15/2026 with the daily's saved Custom profile for positions and prices) would measure all four; it needs the CTO's word.
