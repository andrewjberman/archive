# Task Order: MDPF_COTMDL TO-1 -- verify Portfolio Strategy field populated for real Cottonwood accounts

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mdpf-cotmdl-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>COMPLETE (NEGATIVE) 2026-07-07 -- CTO ran this verification directly as due diligence (Andrew-direct "check immediately", CTO 193310Z). RESULT: Cottonwood runs NO model-portfolio program in Black Diamond -- silver/transactions portfolio_strategy_id 0/10,236 non-null (0%); portfolio_strategy_name 100% populated but 1 distinct value 'No Strategy' for ALL rows; realized/unrealized carry no strategy cols. CUSIP-fallback (Opal ETFs DIVZ/IDVZ/PFDE/PFOE) viable but marginal (12 accounts / 39 holdings). => MDPF_COTMDL is effectively a NO-OP for a real 49F/Inflection-style model view. MDPF build decomposition (TO-2 tagging / TO-3 aggregator / TO-4 frontend) is HELD pending Andrew's park-vs-minimal-12-account ruling (CTO surfacing to Andrew). CTO updated org/projects/MDPF_COTMDL.json phase+blocking (committed). Never dispatched to DS -- CTO pre-empted with the check.</dispatch_state>
    <gate_note>Gates: none. Closed by CTO-direct execution (negative finding); no DS dispatch needed. Build TOs held for Andrew ruling.</gate_note>
  </metadata>

  <objective>Verify that `portfolio_strategy_id`/`portfolio_strategy_name` (BD's "Portfolio Strategy" dimension, present in the transactions/realized/unrealized query templates already flowing daily) are actually POPULATED (not null/generic) for real Cottonwood accounts in opal-data-cot silver tables -- not just schema-present. This is the starting gate for the whole MDPF_COTMDL build (Cohort 3).</objective>

  <requirements>
    <requirement id="1">Read cot silver transactions (or realized/unrealized, whichever is fastest to check) and confirm portfolio_strategy_id/portfolio_strategy_name columns exist and carry real, non-null, non-generic values for a sample of real Cottonwood accounts.</requirement>
    <requirement id="2">Report the distribution -- how many distinct strategies, what fraction of accounts have a real assignment vs null (null = non-model, expected residual per PRD SS4 error-cases).</requirement>
    <requirement id="3">Confirm qt1 holdings (pending live dump per D2 SS7) status -- if still not confirmed, note it as a residual open item for TO-2, not a blocker for this verification.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>Concrete answer: Portfolio Strategy field is populated-and-usable, or is NOT (in which case the PRD's whole cheap-verification premise needs CTO re-scoping before TO-2 proceeds).</criterion>
    <criterion>Distribution reported (strategy count, model vs non-model account split).</criterion>
  </acceptance_criteria>

  <cross_domain_coordination>
    <item>Gates MDPF_COTMDL.TO-2 (cot-side model-tagging gold script) -- notify COO on completion so TO-2 can be authored+GO'd.</item>
  </cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MDPF_COTMDL_PRD.md SS4 (commit 7e321a3ec)</ref>
    <ref type="project">org/projects/MDPF_COTMDL.json</ref>
  </references>
</task_order>
```
