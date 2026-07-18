<task_order>
<to_id>OPAL_TAXSMA_REGISTRY.WS-R2</to_id>
<title>RESOLVER — exact Schwab-account-number -> BD internalId, CONTINGENT ladder (xref -> sanctioned exact-number query -> account-api), EXACT + fail-loud, NO fuzzy</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<date>2026-07-17</date>
<status>pending</status>
<priority>P2 (Andrew-direct via CTO). The correctness spine — WS-R1 seed + WS-R4 skill both call this resolver. Carries the load-bearing egress-feasibility finding (D2/D3).</priority>

<authority>
Andrew-direct 2026-07-17, NON-NEGOTIABLE (verbatim): "this needs to all be done based on account number from Alyssa's docs not fuzzy matching or some bullshit." PRD §2, §4 D2/D3, §5 WS-R2.
</authority>

<gate>
THE NON-NEGOTIABLE (§2): EXACT account-number match only. FAIL LOUD if the exact number is absent or resolves to !=1 account. NO fuzzy name / last-4 / surname fallback at ANY tier. A last-4 match is NOT an exact match — do NOT ship one as "exact."
D3 EGRESS (CONTINGENT, hard-gate): tier-1 (xref) + tier-2 (sanctioned exact-number query) stay WITHIN the standing 49F-reporting word. tier-3 (account-api/* full-number) is a NEW egress surface -> HOLD for Andrew's explicit egress-word EXTENSION. No account-api live call without it. Availability is not authorization.
</gate>

<scope>
Build a shared resolver module (the WS-R1 seed + WS-R4 skill both import it). Input = Alyssa's exact Schwab account number. Resolution LADDER, each tier EXACT + fail-loud:
1. xref fast-path (ZERO calls): dim_account_xref maps schwab_account_id -> bd_external_id; internalId = int(bd_external_id[3:]). Exact by the existing mapping (Chiles 0027265115 -> 22596361 confirmed).
2. sanctioned exact-number QUERY (preferred egress): FIRST DELIVERABLE — establish whether the sanctioned portfolioreporting surface supports a query-BY-exact-accountNumber that returns ONLY the matching account (exact by construction). NOTE: AccountDetailSearch returns a MASKED (last-4) number — that is NOT sufficient; tier-2 must be an exact-number query, not the masked search. If tier-2 works -> use it, no egress extension.
3. account-api/* full-number (fallback ONLY if tier-2 infeasible): the unmasked full number -> a true exact match, but a NEW egress path -> D3 hold.
Resolve once, persist the result to the registry (so the xref/roster carries it thereafter).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="tier-2 feasibility (the gating finding)">
    <step>
      <run>Determine (DRY where possible, ONE live exercise on the sanctioned surface if needed) whether portfolioreporting supports an exact-accountNumber query returning ONLY the exact match</run>
      <expect>A definite yes/no. If YES: tier-2 is the path, no D3 extension. If NO: tier-3 (account-api) is required -> route the D3 egress-extension ask to CTO (who surfaces to Andrew) BEFORE any account-api call.</expect>
      <if_mismatch>STOP + route to CTO. Do NOT default to account-api without the finding + (if needed) Andrew's extended word.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Feeds WS-R1 (seed resolution) + WS-R4 (skill enrollment). The tier-2/tier-3 finding gates whether CTO must surface an egress extension to Andrew. bd data only (bd<->cot separation stands).
</cross_domain_coordination>

<acceptance_criteria>
1. Resolver module: EXACT match, FAIL-LOUD on absent-or-!=1, NO fuzzy fallback (tested: a last-4-only candidate is REJECTED, not accepted).
2. The tier-2 endpoint-feasibility finding landed to CTO (does the sanctioned surface do an exact-number query?) — determines D3.
3. If tier-3 needed: the D3 egress-extension ask routed to CTO, NO account-api live call before Andrew's extended word.
4. Resolves + persists the seed set; xref fast-path verified (Chiles exact).
5. Session log reproduces the ladder + the tier-2 finding + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md (§2, §4 D2/D3, §5 WS-R2)</ref>
  <ref type="egress-rule">CLAUDE.md vendor-egress NEVER-rule; memory/feedback_availability_is_not_authorization_vendor_egress.md</ref>
</references>
</task_order>
