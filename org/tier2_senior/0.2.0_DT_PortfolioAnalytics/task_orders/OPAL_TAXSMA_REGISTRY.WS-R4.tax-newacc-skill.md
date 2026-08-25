<task_order>
<to_id>OPAL_TAXSMA_REGISTRY.WS-R4</to_id>
<title>/tax-newacc SKILL — resolve+confirm (exact) -> enroll (idempotent) -> ad-hoc tax-pt2 run; MCP-gateway operable by Alyssa via her scoped IAM</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<date>2026-07-17</date>
<!-- PARKED 2026-07-20 by 0.2.0_DT per CTO sequence call 201850Z: MDPF_REVAMP is sole focus. Resume-trigger = MDPF parity+swap complete OR Andrew word. Clean-park, not started, nothing stranded. Resume owner = OPAL_TAXSMA then-owner (likely 0.5.0~A delegate); flag CTO to route. -->
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_TAXSMA_REGISTRY, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>P2 (Andrew-direct via CTO). The operator surface. Depends on WS-R1 (registry), WS-R2 (resolver), WS-R5 (Alyssa's grant to invoke+enroll).</priority>

<authority>
Andrew-direct 2026-07-17 (verbatim vision, brief §1). PRD §3, §5 WS-R4. Alyssa runs /tax-newacc {schwab_account_number} through the MCP connection with her scoped IAM.</authority>

<gate>
EXACT-number resolution (via WS-R2) with a HUMAN CONFIRM step before enroll — the skill SHOWS the resolved (schwab_acct -> internalId, client_name) and requires confirmation; FAIL-LOUD on absent-or-!=1, NO fuzzy fallback (§2 non-negotiable). Enroll is IDEMPOTENT (re-running for an already-enrolled account is a no-op, not a duplicate). The ad-hoc run uses the SAME producer + pull_date partitioning (D5).
</gate>

<scope>
The /tax-newacc {schwab_acct} skill, three steps:
(1) RESOLVE + CONFIRM: WS-R2 exact-number resolve -> present (schwab_acct -> internalId, client_name) for confirmation -> fail-loud on absent-or-!=1.
(2) ENROLL: idempotent append to the registry (WS-R1's ETag-conditional RMW) with enrolled_at/enrolled_by(=Alyssa)/status=active.
(3) AD-HOC RUN: invoke the tax-pt2 producer for THAT account now -> bronze->silver->gold on the spot (immediate report), not waiting for tomorrow's ETL.
MCP-gateway operable: the skill runs under Alyssa's scoped IAM (WS-R5) via the gateway (the assume-role boundary is the security control). DE consult if any FE surfaces.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="end-to-end exercise">
    <step>
      <run>Run /tax-newacc for a NEW account end-to-end (resolve->confirm->enroll->ad-hoc run) under Alyssa's scoped role; verify the registry gained the entry (idempotent on re-run) + the ad-hoc gold landed</run>
      <expect>Exact-resolved+confirmed, idempotent enroll, ad-hoc report on the spot; a fuzzy/absent input FAILS LOUD (no enroll, no run).</expect>
      <if_mismatch>STOP. A skill that enrolls on a fuzzy match or duplicates on re-run violates §2/idempotency.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Depends on WS-R1 (registry), WS-R2 (resolver), WS-R5 (Alyssa's invoke+enroll grant — the skill cannot act until that grant is applied+verified). Runs THROUGH the MCP gateway under Alyssa's scoped role. No alert leg.
</cross_domain_coordination>

<acceptance_criteria>
1. /tax-newacc: resolve(exact)+confirm -> idempotent enroll -> ad-hoc tax-pt2 run, all under Alyssa's scoped IAM via the gateway.
2. Fuzzy/absent/>1 input FAILS LOUD (no enroll, no run) — exercised.
3. Idempotent: re-running for an enrolled account is a no-op (no duplicate).
4. Exercised end-to-end (a new account -> registry entry + ad-hoc gold) once WS-R5 grant is live.
5. Session log reproduces the exercise + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md (§3, §5 WS-R4)</ref>
</references>
</task_order>
