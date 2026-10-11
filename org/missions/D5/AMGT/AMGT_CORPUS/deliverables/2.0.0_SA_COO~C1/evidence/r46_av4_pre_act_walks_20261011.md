# AMGT_CORPUS round 46 -- CRPS-av-4 leg p: the pre-act page walks (the baseline for the CTO half's condition 2)

**Issuer:** `2.0.0_SA_COO~C1` (dell1), 2026-10-11. The walker's output stays local under `tmp/ui-walk/<stamp>/` (gitignored: page content and
screenshots are never committed). This record names what was walked, on what, and when, so the post-act walks have a stated baseline.

| label | portal tree | built from | walked | output dir | shots | walker |
|---|---|---|---|---|---|---|
| prod-pre | `C:/tmp/portal-r46-prod` (detached) | `origin/PROD` `37aa1247` | 13:21Z-13:26Z | `tmp/ui-walk/20261011T132124Z` | 86 | armed 13:21Z, disarmed 13:26:31Z, login after: 401 REFUSED |
| dev-pre | `C:/tmp/portal-r46-dev` (detached) | `origin/DEV` `f00c7b8e` (carries av-2 `599e51fb`) | 13:54Z-13:59Z | `tmp/ui-walk/20261011T135427Z` | 86 | armed 13:54Z, disarmed 13:59:03Z, login after: 401 REFUSED |

Names (one per team-sheet class, as the CTO half asked): TSM US (master_absent), SAN FP (own_new), ROG SW (own_model); every tab and expansion the
walker takes per name. Method: `checks/round46/av4_page_walk.sh <label> <tree>` starts `bun run dev:live --port 5174` from the named tree, then
`walk.mjs --route /security-analysis --security ...`. Live function at the walks: `opal-amgt-scoped-api` `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=`
(09:26:42Z), serving /11 with no `row_classes` key (`r46_av4_legp_pre_snapshot_20261011.json`).

**What "PROD unchanged in pixels" is read as here.** The PROD-built page is the portal tree at `origin/PROD`, which does not carry av-2. After the
redeploy the same three names are walked on the same tree and `checks/round46/av4_pixel_compare.py` pairs the shots by step and compares them pixel for
pixel. Live data can move between the two reads (a Bloomberg refresh, an as-of stamp): any DIFFERENT pair is read for what changed before it is called
a PROD change, and a pair whose differing box is a data figure unrelated to `team_sheet` is named as such, not hidden.
