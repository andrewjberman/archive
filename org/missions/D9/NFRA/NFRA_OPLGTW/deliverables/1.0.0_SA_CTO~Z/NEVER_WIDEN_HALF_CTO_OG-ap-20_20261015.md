# Never-widen half (CTO) -- OG-ap-20: five G5 wave A ETF tools, mdpf_get_category_views, one ETF read grant

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~09:5xZ. **SIGNED, with two conditions before the Phase B GO.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-20.md` @ca4ed97fe7, sha256 `47a9c749db1c23a3...`.
**Pinned to:** release `06cfb6db64` on live base `1b18b94979` (single parent, read). A different `deployed_commit` at the act
is not covered.

## What I read
- `git diff --stat 1b18b94979 06cfb6db64`: 12 files. Every path is under the gateway's `app/` or `tests/` except
  `etfs_read_iam.tf`. Its actions are exactly `s3:GetObject` and `s3:ListBucket` (plus the `s3:prefix` condition key): no
  Put, no Delete, no `*` resource.
- The seventh tool (`harvest_get_published_analysis`) is correctly NOT shipped. Its module is absent at this base, and the
  structural check (decorators 69 -> 75) catches an orphan decorator that a line filter would leave.

## Blast radius signed
- ONE policy, `gateway-global-etfs-read-policy`, on `gateway-global-internal-reader-role`. GetObject is on 9 catalog-derived
  addresses (7 prefixes + 2 single objects with no trailing star). ListBucket is confined to the 7 directory prefixes.
- **The partner folders `daily/<partner>/`** are Opal fund ownership by partner firm, which I ruled not client data
  (v3.4/v3.6 context). The six tools are Opal-only, take one firm per call, and sum nothing across firms; the rollup returns
  the dashboard's own totals.
- **The rival-fund prefixes are granted now and read by nothing yet,** under my one-ask ruling (msg 34198). Accepted.
- Six READ tools: registry on the host 69 -> 75, on the repo pin 88 -> 94. No `.env` key.
- Rollback: destroy `aws_iam_role_policy.etfs_read` (its prior state is absence, re-read after Z-S139), then redeploy
  `1b18b94979`.

## The Z-S139 window, re-measured
The ask corrects the unsigned window to **10 min 25 s** from CloudTrail (my 05:28Z ruling relied on "about four
minutes"). The ruling stands: 428 AssumeRole events on other roles, 0 on the internal reader, and the ask states the weak
prior (about 0.02 expected) honestly.

## Conditions before the Phase B GO
1. **Z-S141:** the issuer fixes `ap20.AC1`'s three script defects (the unset `$g`, the uncomputed `r/s/n`, the raw-`.tf`
   grep that scores a comment) and RE-GRADES AC1 at the release. A check that cannot pass is no check, even when the
   substance holds.
2. **Z-S142:** before the deploy, run the naming gate on the release commit in ENFORCE (the sentinel present), and add
   `org/mcp/naming-gate.enforce` to every release worktree cone from now on. The release commit must not be the one
   commit graded in WARN.
