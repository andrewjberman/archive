# ETFS_RIVALS round 17 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~11:2xZ)

One cell, RIV-nc-1, on the ruling of 1.0.0_SA_CTO~Z msg 30817 term 2. Issuance 7a27742b3a; build 74a0f21f39; close
8a012b0f38; merge 1cbee3e716 on site-Z CLOUD (LOCAL). Nothing of rounds 15 to 17 is deployed or served.

## Mechanical criterion

nc-1.AC1 PASS 0 failures, re-run by the issuer on the branch (it re-runs pc-1.AC1, pc-1.AC2 and md-1.AC2: all PASS);
proof instance VALID. Package suite on merged CLOUD 07ff6ebe34: 851 passed, 2 skipped, 0 failed.

## The real run, re-run and looked at

Day 2026-10-06, live inputs, local writes only, code root CLOUD 07ff6ebe34: record
`round17/real_run_2026-10-06.after_nc1.json`. In a browser (localhost stand-in for the gateway's routes), every
fund-security whose chart object carries `"currency": null` was opened: 97 of 97 show no `<svg>` and the sentence
"No price history is stored for this holding yet." (round 16's measurement script counted 96 on its run; this run's
objects hold 97, the difference not examined). A dollar holding (IDVZ Petrobras) still draws, reads "Price in USD" and
does not carry the sentence. Screenshot `round17/r17_realrun_modal_no_currency.png`.

## Found on this run: row ETFS_RIVALS-Z-S56 (BLOCKING, INERT)

A dialog's static trade list says "No trades in the last 365 days" for a fund-security whose chart object holds trade
markers inside those 365 days. Parsed from the run's index.html: 618 frames say it, and 542 of those have one or more
markers in the object; 77 more list fewer trades than the object has markers. (The parse counts 702 frames against the
run's own 695.) The list is built from the trades in the page context, not from the year's trades. The Lambda deploy
does not go out with it open. Repair shape, the issuer's to rule inside cell RIV-md-1's surface: the static line stops
naming a window it does not cover, and the script lists the object's markers in words when the chart object loads.

## Judgment criteria owed at L9

RIV-nc-1 J1, RIV-pc-1 J1, RIV-pd-2 J1, RIV-md-1 J1, RIV-co-1 J1 -- on this run's artifacts.

## What waits, and on whom

- 2.0.0_SA_COO~RV: one repair cell for S56 (round 18); the backfill's security list with formerly-held keys (ruling
  30817 term 1) at the backfill run; the COO never-widen half for the Lambda deploy.
- 3.0.0_SA_CVO~RV: the grades and the slug. 1.0.0_SA_CTO~Z: the gateway release ask (msg 30755) and the CTO halves.
- 0.0.0_AB_MSTR~Z on Andrew's word: the push of site-Z CLOUD.
