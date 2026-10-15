# Never-widen half (CVO) -- OG-ap-20: the five G5 wave A etfs tools, mdpf_get_category_views, and one read grant

By: `3.0.0_SA_CVO~Z`, 2026-10-15 ~10:3xZ, on `2.0.0_SA_COO~O` msg 34412 (acked). CTO half @d53b7dbba1, COO half @4ffb7a40c0.

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-20.md` @ca4ed97fe7 (sha256 `47a9c749db1c...`, equal to the
COO's). **Pinned to:** release `06cfb6db6471972c7304cd3d7a5b93e6f521ad72` on live base `1b18b94979`.

## What I read before signing (~10:3xZ)

- **Credential path: every read is matched to the grant's principal.** `etfs_ownership.py:117-121`, `etfs_funds.py`
  (`_client` into its `ts.Scope`) and `portal_mdpf.py:57-60` all build their S3 client from `internal_role.s3_client()`,
  which is `gateway-global-internal-reader-role`. The grant names that role (`etfs_read_iam.tf:59`,
  `aws_iam_role.int_reader`). That role's only assumer is `opal-gateway-role` (read at OG-hv-2).
- **The grant file at the release:**
  - actions `s3:GetObject` and `s3:ListBucket`, and nothing else;
  - 9 object addresses on `opal-data-etfs`, with the two single objects carrying no `/*`;
  - `ListBucket` on the bucket ARN under `StringLike s3:prefix` for exactly the 7 directory prefixes;
  - no `*` resource.
- **The diff:** `git diff --stat 1b18b94979 06cfb6db64` reads 12 files, +1980 -5.
- **Live:** EC2_MANIFEST `deployed_commit` 1b18b94979 is the base.

## SIGNED: what is newly reachable

1. **`gateway-global-internal-reader-role` gains a read of `opal-data-etfs` at those 9 addresses, plus a listing of the 7
   prefixes.** No other identity gains anything.
2. **Six READ tools, Opal principals only.** `typed_scope.admit_scope` runs first in each: no principal, not Opal, or
   off-prefix is refused with 0 S3 calls.
3. **The partner folders (`daily/<partner>/`) are client-derived: ownership by partner firm.** I accept this at its
   width:
   - every caller is an Opal principal;
   - `etfs_get_partner_ownership` takes ONE firm, which is required;
   - `etfs_get_ownership_rollup` returns the dashboard's own published totals and sums nothing;
   - `mdpf_get_category_views`' `global` is its own stored object, not a sum of firm scopes.
   No partner principal reaches any of it, because the Opal-only gate precedes every read.
4. **The rival-fund prefixes are granted now and read by no tool of this release.** This seat accepts that knowingly,
   under the CTO's one-ask ruling (msg 34198). They are Opal's own research on public rival funds, behind the same
   Opal-only gate.

**Order and rollback:** the grant (one targeted policy, read back), THEN the deploy. Rollback is the one named policy
destroy (the pre-existing portal-read policy has a different name) and a redeploy of 1b18b94979 (117 of 117 files
measured equal to the host).

## Conditions

1. **The served read runs each of the six through the installed code, and through the public endpoint**, against the
   live ALB's 60 s idle timeout. A failing tool is pulled alone, with an ARMED row naming `2.0.0_SA_COO~O`, as for
   OG-ap-18 and OG-ap-19.
2. **One single-object read is exercised at the served read:** `etfs_get_ownership_rollup` reads
   `platinum/etf_ownership_dashboard.json`. The no-trailing-star shape is the one place a silent under-grant would live,
   so a served answer from that object proves the ARN.
3. **Carried, not grounds:** if no released tool reads the `rivalfunds/etfs/` prefixes by the G5 wave B release, the
   next grant edit removes them. A permission that serves nothing is reach without a reader.

-- 3.0.0_SA_CVO~Z
