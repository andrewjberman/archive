# DSGN_IRPTV1 -- what is queued on the one portal slot, and what is parked, with owner and condition (2.0.0_SA_COO~D2, 2026-10-11 ~12:5xZ)

Every portal-editing cell of this project runs in series on one worktree pair (`C:/dev/wk-dsgn-irptv1-49`), so its candidates stay one linear
history onto DEV. This file is the carrier for cells that are ruled but not yet issued; an issued cell lives in its order.

## Issued, in slot order

| cell | order | state |
|---|---|---|
| IV-e-98 | `task-orders/DSGN_IRPTV1.TO-IV-e-98.wire-folder-regeneration.md` (round 18) | RUNNING, worker ~54, base portal 73806e29 |
| IV-e-97 | `task-orders/DSGN_IRPTV1.TO-IV-e-97.tooling-hygiene.md` (round 17) | issued, not started; runs after IV-e-98 |

## Ruled, NOT yet issued -- owner 2.0.0_SA_COO~D2; un-parks when the slot is free, in this order

1. **IV-e-101 (id reserved): an Opal report is drawn with the vendor's wording.** Row IRPT_YCDGEN-D2-W14-S1 (related: IRPT_YCDGEN-W4-S8, the
   adapter sets no provider). The page that opens a retained report prints "Vendor attribution:" per section and "Extraction validation"
   under Technical details on an OPAL_ENGINE report (`OwnedRequestHistory.tsx:151-167, 407`; `NativeSections.tsx:105, 186-190`, as the
   journey read cites them; a code read at portal dbeb6764ea, nothing rendered). Source: 2.0.0_SA_COO~G2 msg 4935, on 1.0.0_SA_CTO~DELL2's
   ruling msg 4924 ("Hop 12's two new rows ... to 2.0.0_SA_COO~D2 as page cells"). Product change; candidate to the CTO.
2. **IV-e-102 (id reserved): after a Prospect Generate the report may have nowhere to open from.** Row IRPT_YCDGEN-D2-W14-S2, INFERRED from a
   portal comment, not measured: "Your analysis requests" mounts only when the header holds a client (`AnalysisTab.tsx:397-409`). The cell
   MEASURES it first (rendered, with no client in the header), then fixes it if true. Same source and ruling.
3. **IV-e-103 (id reserved): the 130% weight.** Row DSGN_IRPTV1-D2-W53-S7: on a synthetic two-account fixture the unpicked Holdings view
   prints a 130.0% weight over a 500,000 base while the card total reads 1,000,000 (seen by this seat in the screenshot
   `deliverables/0.9.0_WK_DSGN_IRPTV1~53/holdings-face.driver-client.png`). Is it the fixture or the page's weight base? A read first.
   1.0.0_SA_CTO~DELL2 msg 4888: "a row with an owner before that walk".
4. **The contract-exact history reader (ruling (A)).** 1.0.0_SA_CTO~DELL2 msg 4818: a named cell, cut ONLY after irpt-status release 5 has
   been live again and read through the page. Un-parks on that, not on the slot.

## Parked on another seat

- **The portal PROD push of the history reader (portal 8ed372cb, now inside DEV).** Andrew's word (client-facing page). The census
  (`deliverables/0.9.0_WK_DSGN_IRPTV1~56/READER_CENSUS.json`) says it is the only reader that refuses release 5 at PROD.
- **The two fixtures the readers refuse** (directory-browse, analysis-input-upload): 2.0.0_SA_COO~P2 corrects them (CTO msg 4864); the smoke
  map then takes the two routes, in whichever cell is on the slot.
- **The custody readers** (read needs `report.accounts`; persist has no reader): no page calls them yet; they wait (CTO msg 4859).
- **FWD-1's Performance hop:** IRPT_BCKEND row S252 (CTO msgs 4705, 4730).

## Update ~13:1xZ

- IV-e-101 and IV-e-102 are ISSUED (round 21) and run in a second worktree pair, ahead of IV-e-98, by 1.0.0_SA_CTO~DELL2's msg 4958. They
  are no longer parked; their orders are the carrier.
- **New, ruled-by-fact, not issued -- IV-e-104 (id reserved), owner 2.0.0_SA_COO~D2:** 2.0.0_SA_COO~P2 corrected the two producer fixtures
  and made four response schemas declare `unprojected_grant` (@d8fb17b6d5, msg 4959; not re-read by this seat). So (a) the smoke map takes
  `directory-browse` and `analysis-input-upload` and their two excuses fall away (three remain), and (b) the five ids that waited on those
  schemas (fe-s-13 content-pins x3, producer-fixtures RESPONSE ENVELOPE, IVE17-AC3) are re-run and should pass. Test and fixture files;
  the build hash is measured before and after. Un-parks when a portal worktree is free. P2 asked to be told if either fixture still fails
  a reader.
