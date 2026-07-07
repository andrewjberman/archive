# Task Order: MDPF_COTMDL TO-1 -- verify Portfolio Strategy field populated for real Cottonwood accounts

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mdpf-cotmdl-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-07-07</date>
    <status>staged</status>
    <dispatch_state>STAGED, sequenced BEHIND ADVI_COTETL.AUAFIX-L6 -- 0.4.0_DS_ClientPlatform is currently the owner of the urgent live ~$3M served-AUA correctness fix (reopened this session, in flight). This TO is fast/read-only per CTO's own framing but is NOT more urgent than a live served-number bug -- do not stack. GO the moment L6 lands (or if DS reports L6 needs external input and has spare cycles, their call to interleave). PRD docs/architecture/MDPF_COTMDL_PRD.md (commit 7e321a3ec) SS4, TO-1 of 4 sequenced.</dispatch_state>
    <gate_note>Gates: none technically (read-only against already-landed data) -- but sequenced behind L6 for owner-focus reasons, not a hard dependency.</gate_note>
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
