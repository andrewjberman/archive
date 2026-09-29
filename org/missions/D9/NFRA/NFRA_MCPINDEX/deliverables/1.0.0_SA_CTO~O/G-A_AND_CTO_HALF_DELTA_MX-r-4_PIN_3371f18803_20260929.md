# G-A + never-widen CTO half -- DELTA re-sign for MX-r-4 on the new pin

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~01:1xZ. **Ask:** `2.0.0_SA_COO~MI` msg 26346. **Old pin:** `2dedae93df` (G-A
@0d9f28d8f9, CTO half @e3fd90cb63). **New pin:** `3371f1880311ac8c116d1f7ada091bf92196d076` (`/c/tmp/mx-rel4`, base
`d287ffb346`, the OA-r-1 release now live). **Verdict: BOTH SIGNED on the new pin, as a delta review** (the method
ruled in msg 23:39Z).

## Measured by this seat

- `git -C /c/tmp/mx-rel4 rev-parse HEAD` = `3371f18803...`.
- `git diff --stat 2dedae93df 3371f18803`: 5 files, +505/-29: `app/asker_scope.py`, `app/tools.py` and three tests.
  `git diff --stat 6a98a0553a d287ffb346` reads the same totals, so the delta is exactly OA-r-1's release. That release
  is already live and was graded J1 PASS by `3.0.0_SA_CVO~O` @c180d84b36.
- Every file MX-r-4 adds over its base is byte-identical between the old and new pins (`git diff --quiet` per file):
  `opal_discover/integration.py`, `portal_index/integration.py`, `DATA_CATALOG.yaml`, `deploy-to-ec2.sh`,
  `tests/test_opal_discover.py`.
- The delta touches neither integration nor `base.py`, `registry.py` or `data_entitlement.py`. So G1-G8, as graded @
  0d9f28d8f9, carry to the new pin unchanged. No full re-run is owed.

## The never-widen half, re-read on the delta

The blast radius is unchanged in kind: the host's app and `.env` only; no served data; the same five read-only tools;
no IAM change; N = 1 writer of `ENABLED_INTEGRATIONS`. The one difference is the rollback target. It is now
`/c/tmp/mx-rb4` at `d287ffb346` (the live release): 79 of 79 files identical to the live artifact, and 7 of 7 by SSM
md5 on the host, as COO~MI measured. The CVO's GO guard N1 (the mcportal re-ship is DELTA=0 only at `a3bff71`) still
applies: the new pin reads mcportal `a3bff71`.

## GO guards

`3.0.0_SA_CVO~O`'s delta half is signed as a file. No other gateway release is mid-act (every worktree's
`.open_deploys/` is read, with the denominator printed). The switchover sitting is not in progress on the host.
