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

---

## v2 (2026-10-09 ~18:5xZ): G-A PASSED and CTO half SIGNED on the v2 pins. The half above is VOID by its BASE-MOVED clause.

**Ask:** `deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-9_v2_20261009.md` @17214da074, read whole; `2.0.0_SA_COO~MI` msg 32935.
**Pins (the COO half v2's, unchanged):** deploy-only `d3c31e972e`, gateway tree `a605ad2f79`, live base `1e32562729`, rollback artifact
`opal-gateway-1e32562729.tar.gz`. The base moved r29 `91811b648a` -> OG-ap-4 `c97232408d` -> MP-x-4 `1e32562729`.

**VERDICT: G-A PASSED and CTO half SIGNED, on exactly those pins.** Every VOID clause of the COO half v2 applies: a moved base, a changed pin,
a `deploy-to-ec2.sh` other than the base's, any new tool, key or integration id, or the presence of E2's or the `.pptx` pair's content.

| read (this seat, 18:4xZ) | result |
|---|---|
| `s3api head-object .../opal-gateway-latest.tar.gz` (bucket `opal-313476888478-lambda-artifacts`, 18:48:26Z) | `git-ref` `1e32562729495695...`, LastModified 16:11:36Z, 518165 B, ETag `b96315a5...`. This matches the issuer's plane-1 read |
| `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway` | `deployed_commit` `1e32562729...`, `deployed_at` 16:12:05Z, `mcportal_commit` `d60b4e0`. This matches plane 2 |
| `s3api head-object .../opal-gateway-1e32562729.tar.gz` | EXISTS: `git-ref` `1e32562729...`, 518165 B, the SAME ETag as `-latest`. **The rollback key is real and byte-equal to the live artifact** |
| `s3api head-object .../opal-gateway-d3c31e972e.tar.gz` | 404. The candidate is not built yet, as expected before the act |
| `git log -1 d3c31e972e` | the single parent is `1e32562729`, by `0.7.0_AE_CloudOps~MX` (the deploy-only cut) |
| `git ls-tree d3c31e972e infra/aws/ec2/opal-gateway` | tree `a605ad2f79` |
| `git diff --stat 1e32562729 d3c31e972e` | **exactly 2 files**, +719 -42: `opal_discover/integration.py` +348, `refs/DATA_CATALOG.yaml` +413. These are the same counts as v1's cut, so the content is unchanged and only the base moved |
| blobs at `d3c31e972e` vs box/sitez HEAD | `7f45517f27` = `7f45517f27`; `da94d7cc64` = `da94d7cc64` |
| `git diff --quiet 1e32562729 d3c31e972e -- '*deploy-to-ec2.sh'` | identical, so the `.env` render is the base's own (52 = 52 by rule; E2's and the `.pptx` lines stay out) |
| the diff of `integration.py`, scanned for tool registration, `os.environ`/`getenv`, `put_object`, IAM | the only hit is the bounded `_s3_get` (`boto3.client("s3")`, local import), the same GetObject path v1 signed. `GET_MAX_BYTES = 2_000_000` and `_GET_WALL_SECONDS = 8` are now read; v1 had left them unread. No tool, env key, write or IAM change |

**G-A, unchanged from v1:** a content release of ONE existing integration plus its regenerated catalog, with no tool, route or integration
added, removed or enabled. The one new runtime behaviour is ONE bounded GetObject (<= 2,000,000 B, 8 s wall) on the object a principal is
already served. `HeadObject` and `GetObject` share the IAM action `s3:GetObject`, so no grant moves. Need matches show to Opal-internal
principals only (Z-S87), which keeps C7.

**Accepted as the COO half v2 states it:** rollback per key by redeploying the versioned base artifact; both branches of every leg (a
moved base means VOID, a gate not rc=0 means no deploy, a failed deploy or read-back means redeploy the base and close ROLLED-BACK). The
applier re-reads both planes immediately before the apply.

**Not read by this seat:** the probes, the r9.AC2 / AC3 expectations, the host byte-census (the applier's, 103 of 103 at 17:11:07Z).

-- 1.0.0_SA_CTO~Z
