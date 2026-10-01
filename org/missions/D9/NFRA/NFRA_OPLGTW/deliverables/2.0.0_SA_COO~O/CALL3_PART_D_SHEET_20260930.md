# Call 3 -- Part D, about 3 minutes (NFRA_OPLGTW)

**For:** Andrew, after G-ACCT step 5. **Driven by:** `2.0.0_SA_COO~O`. **Scope confirmed by:** `1.0.0_SA_CTO~O` msg
27304: call 3 is Part D only. G-D, the controlled walkthrough, stays parked on Opal IT's test user (OG-g-1).

## Why Part D changed shape

The dashboard page load was already done on 2026-09-28. It showed that your sign-in header carries `sub` but no `oid`
or `tid` (`NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/round3/E1_G-HDR_READ.md`). OG-t-2 keys the gateway's tiers on
Entra `<tid>/<oid>` pairs, so the values come from the Entra admin center instead (row NFRA_OPLGTW-Z-S20). These are
the same three people as today's email rosters, so nobody's access widens.

## Your steps

1. Open `https://entra.microsoft.com`. On **Overview**, copy the **Tenant ID**.
2. Go to **Users**, open `andrew@opalinvest.com`, and copy its **Object ID**. This is the master admin.
3. Do the same for `alyssa@opalinvest.com` and `opalbloomberg@opalinvest.com`. These are the two write-capable
   principals.
4. Paste the four GUIDs into this terminal, each with its label. Nothing else is needed: no password and no secret.

## What the COO does with them

- It writes the values to `%LOCALAPPDATA%\opal\og-principals\part_d_20260930.json`, outside every repository.
- It commits `PART_D_RECORD_20260930.md` beside this sheet. The record holds the source, the UTC read time and the
  file's sha256, never a value.
- It hands OG-t-2 PHASE A its values in the hand-off message. PHASE A pre-reads the blast radius (old tier vs new tier
  for every principal) and uploads nothing. The release itself waits on both never-widen halves.
