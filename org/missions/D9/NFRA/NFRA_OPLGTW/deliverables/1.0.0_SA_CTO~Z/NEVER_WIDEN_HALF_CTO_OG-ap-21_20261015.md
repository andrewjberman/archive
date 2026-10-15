# Never-widen half (CTO) -- OG-ap-21: the person reader, two role moves, `harvest_get_published_analysis`

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~23:0xZ. **SIGNED.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-21.md` @1dd5ca7e14, read whole (201 lines), sha256
`862a1de9a7c6...`. **Pinned to:** release `d577e0e7297b3ecba183023d8374855a93f148a7` on live base
`c4c106aea1cc47d15f81397208226bd9b292c9dc`. **If `deployed_commit` at the act is not `c4c106aea1`, this half does not cover the act.**

## What I read (~23:0xZ)

- `git rev-list --parents -n1 <release>`: a single parent, `c4c106aea1`, which equals the live `deployed_commit` in
  `EC2_MANIFEST.json` at HEAD.
- `git diff --stat <base> <release>`: **20 files, +1426 -28**. Every path is under `infra/aws/ec2/opal-gateway/`,
  `infra/aws/terraform/opal-gateway/` or `org/standards/NFRA_OPLGTW_CONTRACT.json`. No other path.
- **The Terraform diff, line by line.**
  - The invoke policy is `lambda:InvokeFunction` on the one ARN `function:opal-amgt-scoped-api`.
  - The news policy is `dynamodb:Query` and `dynamodb:GetItem` on the three news tables and the one `date-index`.
  - Neither has a wildcard action or a wildcard resource.

## Blast radius signed

Sections 1 to 7 of the ask as written:
- **The code release:** registry 75 -> 76, pins 94 -> 95 and 85 -> 86, plus one `.env` key.
- **The two new policies on `gateway-global-internal-reader-role`:**
  - **(a) the news MOVE,** at identical width. The old `gw_news_read` is destroyed by name only AFTER the served read,
    so the news reads never lose their grant.
  - **(b) a NEW GRANT** of `lambda:InvokeFunction` on one function that no role holds today (Z-S149). This is a real
    widening and I sign it as one. The tool's code already assumes that identity, and without the grant it answers
    `harvest_published_unavailable`. Every refusal arm fires before any invoke, and a non-Opal principal cannot cause
    one.
- **The 17 importers of `internal_role.py` and `access_state.py`:** additive only, as measured in section 3(c).

**Rollback:** section 6 as written. Redeploy `c4c106aea1`, destroy the two new policies by target (prior state:
absent), and re-create `gw_news_read` from the `news_read_iam.tf` that the release keeps.

## Both branches

Section 5 adopted. **Refused:** zero invokes and zero DynamoDB calls, audited. **Admitted:** one invoke or one
Query/GetItem through the internal reader, enveloped at 50 KB.

## The two BLOCKING rows (bfb1fc8b11) -- ruled

- **Z-S153: KEEP the base guard (A3 confirmed).** Taking cp-1 `theirs` would revert a live guard by merge. The release
  keeps live behaviour at the entitlement chokepoint, and `test_ogcp1_ac02`'s two assertions expect
  `entitlement_denied`, citing Z-W67-S1. Both readings deny the tool; only the gate order differs.
  - **Z-W67-S1 stays OPEN**, as its own cell with its own halves, AFTER the Friday finish. It is not on the critical
    path, and nothing here decides it.
- **Z-S154: drop `tests/test_admin_people_access.py` from this cut (A3 confirmed).** `app/admin_people_access.py` is
  MP-pd-3's, so NFRA_MCPORTAL ships module and test together in its own release.

## Conditions

1. The deploy tree's HEAD equals `d577e0e729` in full, and its parent equals the live `deployed_commit`. No
   `HALT_OVERRIDE`.
2. The order of acts is section 4, with step 5 (destroy `gw_news_read`) strictly after the served read.
3. The two new policies are read back from IAM before the deploy, and the destroy is read back after.
