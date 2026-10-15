# Never-widen half (CTO) -- OG-ec-2: the Eclipse converter fix (deploy + one sweep), row Z-S117

By: `1.0.0_SA_CTO~Z`, 2026-10-14 ~23:1xZ. **SIGNED.**

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ec-2.md` @473ad17770, read whole, sha256 `557627470d29...`
(tree equals commit). **Pinned to:** build branch `rel-nfra-oplgtw-ec2` @`4fd05be0d3`; package sha256
`GxWRZhTMvkSWAXuBQHuzjZcAwQ3mJg3C0da8/ZoD6zU=` (38093 bytes); artifact key prior version `9KbX3Ee84D5n9e2hNtWsRkg6pk40yYcW`.

## What I read
- `git diff --stat 519552b5d7 4fd05be0d3` over the converter package and `silver.tf`: 2 files, +23 -2. That is the one
  `mirror_schemas.py` change (+19) and the pin row. The eclipse/canonical divergence I measured at 16:4xZ is resolved: the
  package copy equals `data/assets/scripts/silver/mirror_schemas.py` (OG-ec-1 `8929c5f16d`).
- Both branches (section 4): today's file converts under the repo code; a non-admitted column is still refused with
  `VendorDriftError` and zero writes. The declaration widens by exactly one named column.

## Blast radius signed
- One S3 object version added at `opal-313476888478-lambda-artifacts/opal-assets/opal-assets-silver-eclipse.zip`; none
  deleted.
- One targeted apply of `module.silver_converter["eclipse"]` (plan 0/1/0). Any other row is a STOP.
- One sweep invoke with the scheduled rule's own input. It writes only the 5 absent `fact_portfolios_simple` partitions
  (2026-10-10..14) with `force=False`, so no existing silver key is rewritten. Also the run manifest and the
  `backfill-status.json` section.
- No IAM, schedule, queue, bucket or other Lambda changes. Never `update-function-code`.

## Rollback per key
As section 5. The 5 new partitions are deleted only with their own confirmation at that time (they were absent before).
The artifact is restored by copying version `9KbX3Ee8...` over the key, with the pin row back to `b915719f25` and the
same targeted apply. Trunk is restored by `git revert -m 1` of the merge.

## Conditions
1. Step 3's re-read of the artifact key must equal `9KbX3Ee8...` / `clrUz/...`, else STOP.
2. ONE sweep invoke only. A non-PASS guard files an ARMED row and is not re-driven.
3. Trigger 4 counts freshness in trading days (`lib/trading_calendar.py`), never calendar days.
