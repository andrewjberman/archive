# verify-channel — ADVI_INFPRM.W2 cross-tenant SECURITY verify (firmId-fallback)

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | **Deploy:** partners-api-v1.16.2 (commits 15d500737/e7f16a12b/8c4a80b11)
**Surface:** infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
**Why HIGH-priority:** the one place the Inflection-scoping effort could turn a UX bug into a cross-firm DATA LEAK (flagged in my 2h scan).

## Verdict: PASS — no cross-tenant bypass. Code-confirmed (not self-report).

The W2 fix adds `if not firm_id: firm_id = user_firm_id` in BOTH ?firmId gate blocks (advisor-intelligence L1696-97 + books L1795-96). Independently read the authz ordering:
- **firm_id resolution:** L1685/1790 firm_id=query ?firmId=; if absent -> L1697/1796 firm_id=user_firm_id.
- **user_firm_id source:** L1626 `auth_context.get('firmId')` = API-GW-authorizer/JWT context — NOT client-spoofable.
- **is_authorized gates the RESOLVED firm_id AFTER the fallback:** L1703/1801 `if not is_authorized(firm_id, allowed_firms): return 401`. is_authorized (L271-285) = firm_id in allowed_firms (or 'ALL'); allowed_firms from auth_context (L1622, JWT).

Security properties (all hold):
1. Fallback resolves ONLY to the user's own JWT firm -> always in allowed_firms -> can NEVER expand access beyond own firm. (T1/T3: omitted-firmId scopes to own firm.)
2. Explicit cross-firm ?firmId= is non-empty -> fallback does NOT fire -> is_authorized gates it -> 401. (T5: inflection user ?firmId=demo -> 401. Code-confirmed: 'demo' not in inflection's allowed_firms.)
3. SAME is_authorized gate for both paths (explicit + fallback) — the fallback changes only the DEFAULT (empty->401 becomes own-firm->200), never the authz check. Regression-safe: explicit-firmId callers (internal selector, 49F/demo) unaffected (T2/T4).

AE's live-invoke T1-T5 are independently corroborated by the code logic. comp-iam no-gap, 0-diff (per AE).

## Honest limit
Rendered-pixel (Peter's Books surface actually loading) = Andrew/CTO visual smoke (headless down). This certifies the backend authz logic, not the rendered FE. W1(RD~C)+W2(AE) together = Peter's full Books surface.

RAVC2 PASS to AE; CC CTO/COO.
— 3.0.0_SA_CVO
