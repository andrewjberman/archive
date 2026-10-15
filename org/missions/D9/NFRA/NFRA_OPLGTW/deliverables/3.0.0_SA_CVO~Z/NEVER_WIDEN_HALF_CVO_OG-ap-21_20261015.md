# Never-widen half (CVO) -- OG-ap-21: the person reader, two role moves, and harvest_get_published_analysis

By: `3.0.0_SA_CVO~Z`, 2026-10-15 ~23:0xZ, on `0.7.0_AE_CloudOps~Z` msg 34602 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-21.md` @1dd5ca7e14 (sha256 `862a1de9a7c6...`), read whole.
**Pinned to:** release `d577e0e7297b3ecba183023d8374855a93f148a7` on live base `c4c106aea1`.

## What I read before signing (~23:0xZ)

- **The diff:** `git diff --stat c4c106aea1 d577e0e729` reads 20 files, +1426 -28. EC2_MANIFEST `deployed_commit`
  c4c106aea1 is the base.
- **The invoke grant** (`harvest_published_invoke_iam.tf` at the release, `:36-49`): `lambda:InvokeFunction` on ONE ARN,
  `function:opal-amgt-scoped-api`, on `aws_iam_role.int_reader`. That role's only assumer is `opal-gateway-role` (read
  at OG-hv-2).
- **The news move** (`news_read_internal_iam.tf`, `:26-39`): `dynamodb:Query` and `dynamodb:GetItem` on the three news
  tables and `opal-keyword-intelligence/index/date-index`, on `int_reader`. That is the same width as the instance-role
  policy it replaces.
- **Credential path, the Z-S107 check:**
  - `news_typed.py:79` reads DynamoDB through `internal_role.dynamodb_client()`, the role this grant moves to.
  - `news_typed.py:95` refuses (`InternalRoleUnavailable`) rather than falling back.
  - `harvest_published.py:59-79` invokes through `internal_role.lambda_client`, and the grant names that role.
- **The invoke's payload is fixed in code** (`harvest_published.py:132`): `{"rawPath": route, "httpMethod": "GET",
  "headers": {"x-firm-id": "opal"}}`, on the route `/api/scoped/amgt/security/<key>/<section>`. The section is checked
  before any invoke.

## SIGNED: what is newly reachable

1. **A NEW grant:** the internal reader may invoke `opal-amgt-scoped-api`, which no role holds today. IAM cannot bound
   an invoke's payload. The boundary is the code: one fixed GET route, a checked section, and the Opal-only admission
   first. I accept that knowingly. It is the published research layer, Opal's own work, not client data.
2. **A MOVE:** the news reads move from the instance role to the internal reader at identical width. Both stand until
   the served read, then the instance-role policy is destroyed by name. That ordering means the reads never have a
   window with no grant.
3. **One READ tool,** `harvest_get_published_analysis`, Opal principals only. Every refusal happens before any invoke.
4. **The person reader (C-PERSON), read-only here.**
   - STOP and NARROW always apply.
   - WIDEN admits an Opal principal to a SERVED tool past the identity-scope floor, and never past the Opal gate, C2,
     the tier gate or a data grant.
   - Deny beats allow, and a failure fails closed.
   - The record is written by MC Portal's one writer, by Andrew only.
5. **The base guard on the tier line is kept** (A3). Live behaviour at the entitlement chokepoint is unchanged, and
   Z-W67-S1 ships under its own halves.

**Both branches:**
- Refused: 0 invokes and 0 DynamoDB calls, audited.
- Admitted: one GET invoke, or one Query or GetItem, under the internal reader. The answer is projected to 50 KB in the
  envelope.

**Rollback:** redeploy c4c106aea1; destroy the two new policies by name (both have prior state absence); if needed,
re-create `gw_news_read` from `news_read_iam.tf`, which this release keeps.

## Conditions

1. **The served read runs through the public endpoint** (`mcp.opalinvest.dev`) against the live ALB's 60 s idle
   timeout. It covers the new tool's admitted answer, its non-Opal refusal with 0 invokes, and one news tool now on the
   internal reader. A failing tool is pulled alone, with an ARMED row naming `2.0.0_SA_COO~O`.
2. **`gw_news_read` is destroyed only after a news tool has answered through the internal reader** in that served read.
   If the news answer fails, the old policy stays and the release is read as not met for the move.
3. **Carried, not grounds:** the person reader's WIDEN branch is still unexercised. It needs an Andrew-written record,
   and it is graded when MC Portal F2 first writes one.

-- 3.0.0_SA_CVO~Z
