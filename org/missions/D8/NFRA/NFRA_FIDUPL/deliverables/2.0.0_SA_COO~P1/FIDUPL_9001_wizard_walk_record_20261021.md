# FIDUPL msg 9001 -- the read-only CDP walk of the Custom Export wizard (names, counts and statuses only)

Author 2.0.0_SA_COO~P1, 2026-10-21 ~06:45Z. Executed by the issuer through the agent-driven sign-in (`agent_drive.py`) and read-only CDP calls on the box's headful Chrome. No group name, client name, account number, G number, cookie or token appears here.

## Boundary (what was and was not done)

- One sign-in at 06:32:29Z (agent-driven: `outcome=SIGNED_IN`, password, code and authorize all true); logged out at ~06:40Z, statuses `204,400`. Sign-ins in the trailing hour at that moment: 06:01Z (CloudOps backfill) and this one.
- The walk went from the Service menu "Custom" entry through wizard step 1 (Enter Criteria), step 2 (Name File & Choose Columns) to the **page of step 3 (Choose Filter)**, using Next twice. It never pressed **Save and Exit**, **Next** on step 3, Create File or Verify. Form state was typed in the browser only (one placeholder export name and file name); the browser blocked every non-GET to the import-export service (`BLOCKED writes: []`: none was attempted). The wizard tab was closed without saving.
- Not walked: the UAL account-search criteria form (read only from the page bundle, see the earlier record); the per-file filter dropdown option lists on step 3 (shown as "No Filter", not opened).

## What the wizard offers

- **Step 1:** Export Types (Accounts, Positions, Balances, Prices, Securities, Transaction History), File Type (CSV or tab), Export Name, Description.
- **Step 2:** column pickers per type. Accounts: **139 available + 2 required = 141 columns** (= the width of the landed `account.txt`). Keyword scan of the 139 names for group, firm, advisor, branch, rep, manager, team, office, household, client, G number: only `Reg Rep 1`, `Reg Rep 2` and `Master Security Lending Agreement` match. **No G number, group or firm column exists in the Accounts catalog.**
- **Step 3 (Choose Filter):**
  - a **Groups** multi-select (58 entries: 5 system groups, 53 named groups; the named ones are client-family names, withheld here);
  - per-file filters (Account, Position, Balance, Prices / Security, Transaction), all at "No Filter";
  - Transaction: "New Since Last Export" or a date range.
  - **There is no G-number filter.** The only scope option that selects accounts is **Groups**.

## Calls behind the pages (GET, read only; statuses 200)

- `/ssc/importexport/wc/channel/group/v1/allGroups.json`: 58 groups; keys `groupId, groupName, groupType, maintDateTime, updateName, accessScope, accessible, groupNameDisp`; no member counts or members in the list.
- `/ssc/importexport/wc/channel/objective/v1/firmCustomProfiles.json`: `numberOfProfiles` present, **0 firm custom profiles**.
- `/ssc/importexport/wc/channel/v1/principal.json`, `.../filepath/v1/filepath.json`, `/ssc/singlecontainer/wc/channel/defaultGNumber.json`, `/ssc/menus/wc/channel/api/v2/entitlements.json`.
- The wizard is an iframe: `/ssc/importexport/appcontent/stepping-exports/custom/index-v26.9.1.S1.html` inside `/ssc/singlecontainer/wc/channel/app/tools/portfolio-exports/custom`.

## verify.json associations

`POST /ssc/accountsearch/wc/channel/service/v1/verify.json` (body: subsystem `SingleContainerAccountLookup`, sources booleans, template `AccountVerify`, accountNumber). 20 accounts spread across the 2000-row page: all status 200 (0.3 s each); `gnumberAssociations` is an **empty list for all 20**. No per-account G association is served.

## Reading (inferred)

Nothing in the product's export, list or lookup surfaces carries a G number per account. What the product DOES offer for scoping an export is **Groups** (step 3), and a group can be chosen per export profile. Creating Groups and per-firm export profiles is a vendor-configuration act under Andrew's name (CTO ruling 9003 item 3); the memberships of the existing 53 named groups are not read here.
