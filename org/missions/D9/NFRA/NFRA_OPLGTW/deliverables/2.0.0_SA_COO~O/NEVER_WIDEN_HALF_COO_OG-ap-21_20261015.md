# Never-widen half (COO) -- OG-ap-21, the person reader, the news move, the invoke grant and `harvest_get_published_analysis`

By: `2.0.0_SA_COO~O` (issuer), 2026-10-15 ~23:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-21.md` (sha256 862a1de9a7c6, committed `1dd5ca7e14`, AE msg 34601),
release `d577e0e7297b3ecba183023d8374855a93f148a7` on `rel-nfra-oplgtw-p21`, base = live `c4c106aea1cc47d15f81397208226bd9b292c9dc` (NFRA_MCPINDEX MX-r-14).

## SIGNED at `d577e0e729`, on conditions C1-C6

What this seat read at signing, in the release tree `C:/tmp/og-rel-p21` (not from the ask's prose):
- **The release is parent-of-base exact:** `git rev-parse HEAD` = the full release_sha; `HEAD~1` = `c4c106aea1`. `git diff --stat HEAD~1 HEAD` names 20 files (the ask's table), 1426 insertions, 28 deletions. `tests/test_og_bd2.py` is not in the diff (0 lines).
- **Structural oracle:** `@mcp.tool` decorators in `app/tools.py` at the release = 76 (base 75, one new tool); rival tokens (`etfs_rivals`, `_rv1`, `_rv2`, `etfs_get_peer_group`) in the diff = 0. The two OG-rv-3 commits did not ride.
- **The base guard survives (A3):** `app/data_entitlement.py` lines 730 and 751 both read `if (not access.restricted and ...)`: dispatch path and list path. Live behaviour at the tier chokepoint is unchanged. Row Z-W67-S1 stays open and is not ruled here.
- **The test divergence is accepted:** `test_ogcp1_ac02` carries two assertions expecting `entitlement_denied` (lines 166 and 175), each with a comment citing Z-W67-S1. A3 said "one"; the second is the same fact, and AE proved it in the run. I read it as within A3, not a new ruling.
- **Who gains:** `gateway-global-internal-reader-role` gains TWO policies. (a) `int_reader_news_read`: `dynamodb:Query` and `dynamodb:GetItem` on the three news tables plus `date-index`, four ARNs, no Scan, no write, no wildcard, width equal to the instance role's existing news statement. (b) `gw_harvest_published_invoke`: `lambda:InvokeFunction` on ONE function ARN, `opal-amgt-scoped-api`, one statement. (b) is a NEW GRANT that no role holds today (Z-S149); it is stated as one, and the code (`internal_role.lambda_client`) already assumes that identity.
- **Who loses:** nobody at this release. The instance role's news statement stands through Phase B step 4 and is destroyed by name only after the served read (step 5).
- **The person reader only narrows or admits an Opal principal past `identity_scope`; it overrides no other gate** (Opal-only, C2, tier, data grants), fails closed, and is written only by C18 (Andrew-only).
- **Both branches:** refused arms (`principal_required`, `harvest_opal_only`, `harvest_prefix_not_served`, `harvest_bad_argument`, `harvest_published_unavailable`) fire BEFORE any invoke or DynamoDB call, zero reads; admitted = one invoke or one Query/GetItem through the internal reader, answer projected to 50 KB.
- **Rollback (two independent legs):** redeploy the base `c4c106aea1`; destroy `aws_iam_role_policy.int_reader_news_read` and `aws_iam_role_policy.gw_harvest_published_invoke` through `safe-apply` targeted (prior state absence for both). `news_read_iam.tf` is not deleted, so a destroyed `gw_news_read` re-creates from code.
- **The naming gate:** the release branch runs the pre-clause gate (md5 `7be9e4ed`); graded on trunk in ENFORCE the diff exits 0 (two policy names CONFORMANT, one RAISE-EXISTING that mints nothing). Accepted as the ask states it (section 9).

**C1 -- the ask stays at its bytes through the GO** (sha256 `862a1de9a7c6`).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other gateway release is in flight (per-tree denominator printed). No `HALT_OVERRIDE`.

**C3 -- if the live base moves, this half does NOT carry.** Another release landing first means a re-cut and a re-sign. (MX-r-14 is the base; OG-ap-23 and OG-ap-24 wait behind this one: one gateway release at a time.)

**C4 -- the grants first, read back from IAM with `get-role-policy` for BOTH policies, then the deploy.** Ledger `nfra-oplgtw-gateway-release-p21` opened (entry AND sentinel) before the apply. On any trigger failing: redeploy the base, destroy the two policies, file an ARMED row naming this seat.

**C5 -- the served read** shows `harvest_get_published_analysis` answering an Opal stand-in principal with the envelope and refusing a non-Opal one with ZERO invokes, plus `registry_before` 75 to 76 on the host's own registry and `AMGT_SCOPED_API_FUNCTION` in the `.env` key names.

**C6 -- `gw_news_read` is destroyed by name only after C5 passes**, never before and never by a plan that touches anything else; the destroy plan reads `0 to add, 0 to change, 1 to destroy`.

No `apply` in any form before the three halves are signed at `release_sha` and the GO names them (Z-S139 standing rule).

## Not covered

- The ruled behaviour of Z-W67-S1 (a profiled master_admin ALLOWED): its own release, its own halves.
- MP-pd-3 (`app/admin_people_access.py`) and any other NFRA_MCPORTAL content.
- The code batch (`OG-ap-23`), the six vendor roles (`OG-ap-24`), and any other gateway change.

-- 2.0.0_SA_COO~O
