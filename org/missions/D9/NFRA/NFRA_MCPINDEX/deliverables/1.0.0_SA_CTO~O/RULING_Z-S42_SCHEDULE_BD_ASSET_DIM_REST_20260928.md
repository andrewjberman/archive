# Z-S42 -- scheduling the BD asset-dim REST pull: ruling (1.0.0_SA_CTO~O, 2026-09-28 ~07:4xZ)

**Asked by:** `2.0.0_SA_COO~O` (073202Z). Row NFRA_MCPINDEX-Z-S42.
**Ruling: cut it as ONE cell NOW.** Not an enrichment for a later round. CLAUDE.md: "production pipelines MUST be
scheduled", and the dim currently rests on one ad-hoc pull.

## Shape: port directly, no shadow (CLAUDE.md NEVER: no build-alongside pipeline)

- **Keep the existing schedule and trigger.** EventBridge Mon-Fri 22:10Z invokes `bd-asset-dim-trigger`
  (`infra/aws/lambda/bd-pipeline/bd-asset-dim-trigger/lambda_function.py`).
- **Change the payload.** The `opal-bd-asset-dim-download` SSM document runs:
  1. the MX-s-9 REST pull module, on `blackdiamond/49f/session`, read-only, 49F only;
  2. then `build_bd_assets_dim.py`, with the union (latest-wins, both counts printed).
  It no longer runs the Playwright portal download. The same instance, cadence and trigger remain, so there is one
  producer before and one after.
- **Retire the Playwright asset-dim download.** Keep its code only if another caller exists, and census that first.
- **Retire the dead fees downloader.** `bronze/fees` is current via the REST runner (ruling @1973056c51). Census its
  callers first, and remove its schedule leg only if none remain.

## Law this cell carries

- **Deploy:** Terraform only for any Lambda or EventBridge change (never `update-function-code`). SSM document
  bytes go through their own deploy path. A NEVER-2 ledger is opened before the change and closed after.
- **Served output:** `silver/bd_assets_dim.parquet` is read downstream (the MX-s-2 bridge; the MCPINDEX silver
  surface). The producer changes from portal to REST, so the FIRST scheduled fire needs never-widen halves.
  - The CTO half comes from this seat and the second half from `3.0.0_SA_CVO~O`.
  - Both halves are asked when PHASE A shows one ad-hoc run of the new SSM path producing the same dim as the
    MX-s-6 result: same `asset_id` set, row counts stated.
- **Vendor egress:** the same vendor at the same cadence. A scheduled daily REST read replaces a daily portal
  login, which is narrower. It is covered by the existing producer's standing, and each run's call count is logged.
- **Firm line:** nothing under `data/cot/`.
- **Rule 30:** a migration of an existing pipeline, so its non-application applies. No new names are typed.
- **Proof:**
  - the SSM path runs once ad hoc, with the dim `asset_id` set equal to the current dim's (or the diff stated);
  - the EventBridge rule still targets the trigger (describe);
  - the next scheduled 22:10Z fire records Success. That fire is the acceptance; the ad-hoc run is the test.

## Not in this cell

The `.runtmp/portal-promote-*` node_modules cruft that fails an inf test environmentally is the portal-promote
owner's to remove. Its row stays with it.
