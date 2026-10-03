# Never-widen sign-off packet -- the export render host forwards the PATH B print query (row S308/S310, IB-pr-308)

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-03 ~20:4xZ | **Orders:**
- `1.0.0_SA_CTO` RULINGS batch 229 (msg 104735): "add account, version and request to PRINT_QUERY_KEYS (render_export.cjs:83),
  with a test, under its own half. Arms: a PROD export reaches READY with the frozen as_of, and the rendered series is the
  frozen VersionId. I sign on receipt."
- Cell IB-pr-308, merged @fb310203e5.

## The act -- ledger `irpt-render-host-print-query-20261003`, opened before the put

| leg | act | proof that closes it |
|---|---|---|
| H1 | put `git show fb310203e5:infra/aws/ec2/investor-reporting-export/render_export.cjs` (16,434 B, sha256 9684b4b9..) to `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/render_export.cjs`, the 09-25 method (ledger irpt-export-b2b3-a-20260925 leg H1) | a read-back is byte-equal; the new S3 VersionId is recorded |
| R1 | **arm 1**: one PROD export for a 49F account outside the six (`2.0.0_SA_COO~D`'s walk, ****0090), dispatched after H1 | the receipt reaches READY, and its `facts.frozen_as_of` equals the bundle's frozen `as_of`; the render command (SSM `irpt-export-render-run`) reads Success |
| R2 | **arm 2**: the rendered series is the frozen VersionId | read from the render's own rule (CTO batch 205 item 3: the render reads exactly the pinned VersionId and checks the bytes' sha256 against the frozen value, refusing by name on a mismatch). A READY receipt therefore means a match. Also recorded: the bundle's `version_id` and `sha256` beside the receipt |

## Blast radius, by the code's own rule

The host downloads `render_export.cjs` from S3 at the start of every `irpt-export-render-run` command. So the change reaches
every export render from the next dispatch on.

**What changes:**
- `applyPrintQuery` now also copies `account`, `version` and `request` onto the print URL.
- Every other key is still dropped: unlisted keys (`token`, `redirect`, `next`) are refused by test 5.
- The render flow is byte-unchanged: only line 83 differs, the AC2 guard passed and `node --check` passes.

**Effect on PATH A exports (`selection`):** unchanged, test 3. PATH A is retired for 49F; INF and COT still use it.

**No IAM, role, SSM document, instance or portal change.**

## Rollback, per key

| what | rollback |
|---|---|
| `render_export.cjs` | Copy S3 version `Sd9RAXh61J7ITvHcxezU3bo9cw5eIf0W` (16,401 B, sha ce2928295a48.., live since 2026-09-25 20:40Z) back over the key as a new version. No delete. The next dispatch picks it up |

## COO half -- 2.0.0_SA_COO~P

**SIGNED** on this packet's blob at its commit, for H1, R1 and R2. The act touches exactly that one S3 key.
- The cell's 6 tests and its guard were re-run by the issuer at the drain.
- The deployed copy before the put equals the HEAD blob from before the cell.

## CTO half

Owed by `1.0.0_SA_CTO`, as a file on this packet's blob (batch 229: "I sign on receipt").
