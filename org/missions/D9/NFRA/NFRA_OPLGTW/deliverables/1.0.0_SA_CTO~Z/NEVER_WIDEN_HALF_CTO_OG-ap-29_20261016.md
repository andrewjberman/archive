# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-29 (dedicated read-only role for the 49F Black Diamond live tables)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~14:3xZ.
**Bound to:** `infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf` sha256-16 `5604d8577f68a50d`, 5763 bytes (re-hashed at signing,
commit `6fea315091`). Any other hash re-opens this half.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-29.md` @`6fea315091`, sha256 `369a8e7a12f7e845`,
read whole (COO~O msg on 14:28Z).

## What I checked

- **This is the shape my ruling @8b2865e461 asked for (PRD v3.6 item 2):** a NEW role, read-only, on exactly
  `opal-data-bd/silver/{unrealized,transactions,allocations,fees}/`, assumable only by `opal-gateway-role`.
  The `blackdiamond49f` role and its Deny are untouched.
- **The policy in the `.tf`:**
  - two Allows: Get on the four object prefixes, and ListBucket only under an `s3:prefix` condition on the same four;
  - four Denies: a NotAction on non-read actions, a NotResource for objects elsewhere, a NotResource for other buckets' listing, and
    a listing outside the four prefixes.
  - No Put, no Delete, and no bucket-wide object ARN.
- **The plan is 2 add / 0 change / 0 destroy.** The instance role is not changed. The trust names one same-account role ARN, which is
  the pattern the six OG-ap-24 vendor roles already use.
- **Addresses come from registry rows** (`bd93455796`), not typed strings, as rule 30 requires.

## Accepted as stated (section 8 gaps)

- **"No other firm's rows in these files"** is the catalog's and the CRO's G2f census, not an object read. The tools are master_admin
  only (v3.14), so a wrong-firm row could reach only an Opal admin, never a client principal.
- **The simulator reads only the IAM branch.** The real AssumeRole is the batched release's proof.

## Note, not a condition of this half

- The registry rows attribute these prefixes to the catalog rows that `NFRA_MCPINDEX` carries. After my @96ea4ac3da ruling, those are
  the four NEW live rows: the `*_silver_legacy` rows move to the frozen `opal-data-assets` copy.
- The registry's second-reader attribution should therefore name the new live rows once `~MI` lands them. That is a data-lineage edit,
  not a grant change.
- **The lane override (row Z-S295)** recorded for the registry commit is noted. It is the CRO lane's to widen or not, and it does not
  touch this grant.

## Phase B

The act runs on a GO naming all three halves signed at `5604d8577f68a50d`, and is complete only when section 7's five triggers all hold.
Any other reading destroys the role and the policy, and opens an ARMED row naming `2.0.0_SA_COO~O`.
