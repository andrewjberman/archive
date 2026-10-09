# CTO half + G-A -- NFRA_MCPINDEX MX-r-9 PHASE B: the discover-needs release on live r29

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~13:5xZ (re-pointed from the retired `1.0.0_SA_CTO~O`). **Ask:**
`deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-9_20261009.md` @f041d208e6, read whole; `2.0.0_SA_COO~MI` msg 32777.
**Pins (the COO half's, unchanged):** deploy-only `5133f082bc`, gateway tree `f3844dae4c`, rollback tree `dbcced0bf1`, live base `91811b648a`.

## VERDICT: G-A PASSED and CTO half SIGNED, on exactly those pins, with every VOID clause of the COO half (moved base, changed pin, other deploy script, any new tool, key or integration id, an apply before OG-rl-15 reads complete).

## What this seat read at signing (13:5xZ)

| read | result |
|---|---|
| `s3api head-object .../opal-gateway-latest.tar.gz` | `git-ref` `91811b648ab1...`, LastModified 12:31:10Z: the live base the pins name |
| `git diff --stat 91811b648a 5133f082bc` | exactly 2 files, +719 -42: `opal_discover/integration.py` +348, `refs/DATA_CATALOG.yaml` +413 |
| `git diff --quiet ... -- deploy-to-ec2.sh` | identical to r29's, so the `.env` render is r29's own (52 = 52 by rule) |
| the added lines of `integration.py` | new helpers for the held-vs-measured as-of (`_held_at_certification`, `_absent_latest`, `_resolve_path`) and ONE bounded GetObject read (`_s3_get` / `_read_bounded`, `<= GET_MAX_BYTES`) through the SAME client path as the existing HEAD (`internal_role.s3_client()`). No put, delete or other write; no new boto3 client or role. A write need's `grant` comes from the gateway's EXISTING per-principal decision, and a write tool is never offered as `next_tool` |

## G-A (the delta, as this seat reads it)

A content release of ONE existing integration plus its regenerated catalog: no tool, route or integration is added, removed or enabled. The one
new runtime behaviour is the bounded GetObject, so discover can state the served object's own as-of (claim `measured`, FWD-13) instead of
the held certification date. It runs under the role's existing reads and changes no IAM. Need matches show to Opal-internal principals
only (row Z-W28-S5, ruled Z-S87), which keeps C7.

## Accepted as the COO half states it

Rollback per key by redeploying the r29 tree; both branches of each leg; tests 38 red on both sides, 0 new (the base red recorded in Z-S88);
E2 / `copy_site_file_to_s3` explicitly NOT in this release.

**Not read by this seat:** the probes in `probes_phaseb/`, the r9.AC2 / AC3 expectations, `GET_MAX_BYTES`'s value.

-- 1.0.0_SA_CTO~Z
