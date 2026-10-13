# NEVER-WIDEN ASK -- OG-hv-1 -- the gateway's harvest read tools (for the release order `NFRA_OPLGTW.TO-OG-hv-2`)

From `0.9.0_WK_NFRA_OPLGTW~64` (round 37, R4, PRD v2.7/v2.8 FWD-21). Code is committed on `wk-NFRA_OPLGTW-64` at
`4e26a29872` (LOCAL). Nothing is released, deployed or granted by this cell.

## 1. The diff, by file (all under `infra/aws/ec2/opal-gateway/`)

| file | change |
|---|---|
| `app/harvest_read.py` | NEW. `BUCKET`, `SERVED_PREFIXES` (24), the admission, `harvest_list`, `harvest_read`, the 4 MB read cap, one audit record per call |
| `app/tools.py` | two `@mcp.tool()` registrations beside `list_shared_folder`, each through `_run` (tier, entitlement guard, audit); one import |
| `app/destructive_ops.py` | `harvest_list`, `harvest_read` added to `SAFE_TOOLS` |
| `app/data_entitlement.py` | the same two added to `NATIVE_TOOLS` (class `legacy`; NOT `DATA_GRANT_TOOLS`) |
| `tests/test_og_hv1.py` | NEW, `test_oghv1_ac01 .. ac05` |
| `tests/test_entitlement_admin.py`, `tests/test_data_entitlement_family.py` | counts re-pinned: tools 63 -> 65, non-data 54 -> 56 |

No `.env` key changes. No `ENABLED_INTEGRATIONS` change. No Terraform in this cell.

## 2. The two new tools

Class: READ. `SAFE` in `destructive_ops`, `legacy` in `data_entitlement`, so `classify()` does not fail closed and
`tool_unclassified` is not returned.

- `harvest_list(prefix, start_after="")`: ONE `list_objects_v2` page (MaxKeys 1000, Delimiter `/`): keys, sizes,
  LastModified (UTC), common prefixes, `truncated`, `next_start_after`.
- `harvest_read(key)`: one object, capped at 4 MB ON THE READ. `.json` / `.json.gz` parsed; `.parquet` returned as at most
  1000 rows (`truncated` says so); anything else UTF-8 text (`errors="replace"`).

Refusals, all `{error, code, guard_denied: true}`, evaluated in this order BEFORE any S3 call:
1. `principal_required`: no validated principal in the request.
2. `harvest_opal_only`: the principal's email fails `tools._is_opal_user` (domain `opalinvest.com`, no `#ext#`).
3. `harvest_prefix_not_served`: the prefix (and `start_after`) or key is not under one of the 24 prefixes, or contains `..`.
Then, after the read: `harvest_over_cap` (object over 4 MB; decompressed `.gz` also capped). A non-Opal principal is refused
on every prefix, `packs/` and `wsj/harvest/` included (`test_oghv1_ac02`, 8 refusals, 0 S3 calls).

## 3. The widening, stated plainly

- **The gateway's reach grows** from the catalog's one bucket (`opal-data-portal-v2`) to `s3://opal-data-harvest`, the 24
  top-level prefixes of list v4 (`7e0da2dfee`), raw included, **for Opal principals only**. Admission is by identity, not by a
  per-person grant record (PRD v2.7).
- **`opal-gateway-role`'s own S3 read on `opal-data-harvest` is itself a widening of that role** (PRD v2.8). Today the role is
  implicitDeny on that bucket (measured by the issuer, 2026-10-13 ~20:4xZ); after the grant it can read 24 prefixes of it. This
  is named as a widening of the role, separate from the tools' reach.
- **The research-only arm** (PRD v2.8): an asset manager stays refused every Schwab and Black Diamond tool unless Andrew
  admits it to v2.2's connected set. `test_oghv1_ac05` shows the same unprofiled, standard-tier Opal principal that reads
  `packs/` refused all 5 `schwab_*` tools and `blackdiamond_list_fees` (`entitlement_denied`, OG-bd-2's code).
- The audit carries the tool, the key or prefix, the verdict and the bytes -- never object content.

## 4. The IAM grant it needs (the release order's apply, not this cell)

- Policy name `gateway-global-harvest-read-policy` (`opal_naming.name("gateway", "global", "harvest-read", "policy")`, run
  here: `gateway-global-harvest-read-policy`), attached to `opal-gateway-role`.
- `s3:GetObject` on the 24 prefix ARNs (`arn:aws:s3:::opal-data-harvest/<prefix>*`, one per entry of `SERVED_PREFIXES`);
  `s3:ListBucket` on `arn:aws:s3:::opal-data-harvest` conditioned on `s3:prefix` matching those 24 prefixes.
- Expected plan: **1 add, 0 change, 0 destroy**. Encryption is SSE-S3 (no KMS statement); no bucket policy exists.
- **Count of tools: 63 -> 65.**

## 5. Both branches of a call

- **Refused:** a non-Opal principal, an unserved prefix, a `..` key, or no principal. The tool returns the coded refusal and
  makes no S3 call (recorded in `test_oghv1_ac02`, `ac03`).
- **Admitted:** an Opal principal on a served prefix. One `list_objects_v2` page, or one `get_object` read capped at 4 MB, then
  a parsed JSON / Parquet-rows / text answer (`test_oghv1_ac03`, `ac04` through the served MCP surface).

## 6. The rollback

Redeploy the prior release ref (the tools vanish with the code; 65 -> 63). Destroy the one policy
`gateway-global-harvest-read-policy` (the role returns to implicitDeny on the harvest bucket). Nothing else was written.

## 7. Open items the signer should know

- `Z-W64-S1` (BLOCKING): no source names the asset-manager principals; the census marks every row `"unknown"`. The release can
  be signed on the tools; the driven FWD-21 call needs a named principal.
- `Z-W64-S2`: `app/audit.py` has no args allowlist entry for these tools, so the audit's `args` is omitted and the key/prefix
  rides in `detail`; `tools._run` also needs a delegated Graph token for the caller (`NeedsLogin` otherwise).
