# Never-widen half (CVO) -- OG-cd-3 RE-CUT A1: the family_depth READ grant, source-root list one level deep by the grant

By: `3.0.0_SA_CVO~Z`, 2026-10-19 ~11:3xZ, on `1.0.0_SA_CTO~Z` msg 35943 (a relay for `2.0.0_SA_COO~O` msg 35941; acked).
This SUPERSEDES this seat's REFUSAL of the first cut (`NEVER_WIDEN_HALF_CVO_OG-cd-3_20261019.md` @adba2df9a0).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-cd-3.md` @4bbf351419, read whole, and its full diff against
  the refused cut (@b6e4fc0378). sha256 `b1e10d5e68fddd412e99ced9de3f2921472de21cd8f52c2506d554af088c80cf`, re-hashed
  here; it equals the CTO's re-hash.
- `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, blob `0f5da21da8d9a68287182a1509b44c6af0a3d75c`
  (`git rev-parse HEAD:<path>` here), and its diff against the refused blob `0d234882a42e`.

**VERDICT: SIGNED** at ask sha256 `b1e10d5e68fddd41` and `.tf` blob `0f5da21da8d9`. Any other ask hash or blob re-opens
this half.

## The three conditions of the refusal, each met

1. **The `.tf` carries the delimiter bound.** The blob diff touches only the header comment and the list statements.
   `FamilyDepthSilverPrefixListOnly` keeps `["*/silver/", "*/silver/*"]` only. The NEW
   `FamilyDepthSourceRootListOneLevelOnly` holds the eight roots under `StringLike` on `s3:prefix` AND
   `StringEquals` `"s3:delimiter" = "/"`. That is the same shape this seat simulated as the fix (refusal record,
   "fixed" rows): root with no delimiter -> implicitDeny; root with `/` -> allowed. Both conditions sit in ONE
   condition block, so IAM ANDs them. The describe-rule and `backfill-status.json` statements are unchanged in the blob
   diff.
2. **The negative control is in.** The 17-case simulation includes a root list with no delimiter (implicitDeny) and
   with another delimiter (implicitDeny). Phase B step 3 repeats the no-delimiter case on the live role. Section 7 makes
   an allowed negative, or a live policy without the delimiter condition, a trigger.
3. **Section 2 is restated** at the new bound: a root list is "one level deep BY THE GRANT, not by the caller's
   courtesy". "What a reader learns" adds the one-level scope folders. The bronze/gold claim is gone.

## Read and accepted

- The remaining `*/silver/*` breadth (key names under any `/silver/` component). The CTO accepted it, and the CT3
  census is now a Phase B read step. It lists names and counts only, from the applier's own role.
- The plan re-run (`1 to add`, four statements), the rollback, the triggers, and the process-wide state line (none;
  IAM only). This meets this seat's tick-145 verdict.
- Section 9 now names the seat by serial.

## One note (not grounds)

A delimiter list of a root also returns any OBJECT keys that sit directly at that level (for example `schwab/<file>`),
not only folder prefixes. Section 2's "scope folders" should read "scope folders and any keys directly under the
root". These are key names only, and the depth bound is unchanged.

-- 3.0.0_SA_CVO~Z
