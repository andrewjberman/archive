# Task Order: ADVI_COTPPLADVFIX TO-2 -- enable the advisor-drill Books tab for cot + verify single-advisor render

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-advi-cotppladvfix-to2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <completed>2026-07-08</completed>
    <reconcile_note>Status-reconciled 2026-07-20 by 2.0.0_SA_COO (Andrew-direct backlog review). Books tab / advisor-drill config-nav SHIPPED LIVE on portal PROD -- portal-v2.1.133 (@27f543ade, CI run 28954979551 SUCCESS, present-as-is Option A). TO-1's served advisor entity landed first so the gate was met.</reconcile_note>
    <dispatch_state>STAGED, GATED on TO-1's SERVED advisor entity. TO-1 (DS A_01 injection) must land AND be nightly-served (exactly one cottonwood_capital_advisors/ book on opal-data-cot) before this can render anything but an empty stub. GO fires when DS notifies COO the served entity has landed (expected earliest: tonight's 02:00 UTC nightly after DS deploys TO-1). DE (0.4.0_DE_ClientPlatform) is not yet respawned -- COO will respawn the DE lane at GO time, not now (no actionable work until TO-1's entity exists; respawning now would just idle it, LD-0158). PRD docs/architecture/ADVI_COTPPLADVFIX_PRD.md. TO-2 of 3.</dispatch_state>
    <gate_note>Gates: HARD dependency on TO-1's served advisor entity (needs the data, not a stub). Portal main tree stays on DEV.</gate_note>
  </metadata>

  <objective>Surface the now-populated advisor-drill Books tab for Cottonwood: flip the cottonwood/layout.ts flags that gate the Books nesting, and verify the SHARED AdvisorIntelligence BooksTab renders a single-advisor firm cleanly (one advisor card "Cottonwood Capital Advisors" -> all clients nested -> account drill) with zero 49F/inflection regression.</objective>

  <requirements>
    <requirement id="1">In portal/src/pages/AdvisorIntelligence/_partners/cottonwood/layout.ts, flip the MINIMAL set required for the Books nesting to mount: tabs.books.enabled false->true, advisorDrill.enabled false->true (L63), advisors.enabled false->true (L72), distribution cohorts.adv 'disabled'->'enabled' (L56). Confirm each is actually required (comp-transform schema-check) -- flip only what the Books nesting needs, update the stale "hidden for v1" comments (L13-15, L133).</requirement>
    <requirement id="2">Q1 RECONCILIATION (COO-decided -- SUPERSEDE): ADVI_COTMVP is COMPLETE and shipped OUTCOME-B with Books DISABLED (books.enabled=false, "Advisors/Books hidden for v1" L133) and the advisor-drill deferred as REVISIT-LATER. There is NO conflicting enabled firm-level-only Books view to replace -- you are materializing the deferred Option B on a currently-disabled surface. Do NOT reopen COTMVP.</requirement>
    <requirement id="3">Verify the shared BooksTab handles N=1 advisor: a single advisor card, all clients nested, account drill -- NOT a broken/empty leaderboard or a divide-by-N glitch. Numbers reconcile to the firm headline (no advisor-vs-firm double-count).</requirement>
    <requirement id="4">Multi-tenant safety: the shared BooksTab / advisor-drill components serve 49F + inflection too. Their Books tabs MUST be unchanged -- confirm no cross-tenant regression.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">comp-transform schema-check BooksTab (+ the AdvisorIntelligence advisor-drill components) -- confirm the data-prop type contract the single-advisor served artifact satisfies (MISSING = runtime undefined).</phase>
    <phase name="before_commit">confirm 49F + inflection tenants' Books tabs are unaffected by the shared-component path (no cross-tenant regression); comp-transform ternary-audit if any cohort/mode branch is touched.</phase>
    <phase name="after_commit">comp-routes trace / behaviors on the platinum firm-dashboard + advisor-summary fetch path for cottonwood scope (4xx/HTML-masking check); browser-repro as a cottonwood-scoped user.</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>HARD-gated on ADVI_COTPPLADVFIX.TO-1 (DS) served advisor entity -- do not start render verification against a stub.</item>
    <item>Shares cottonwood/layout.ts + the shared BooksTab with 49F + inflection tenants (multi-tenant component) -- TO-2 must not regress their Books tabs.</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>A cottonwood-scoped user sees the Books tab with "Cottonwood Capital Advisors" -> all clients nested -> account drill; numbers reconcile to the firm headline (screenshot/browser-repro evidence).</criterion>
    <criterion>49F + inflection Books tabs unchanged (repro/screenshot evidence of no regression).</criterion>
    <criterion>Portal main tree remained on DEV throughout.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/ADVI_COTPPLADVFIX_PRD.md S4.2 / S4.3 / S6 TO-2 (commit 11f6bd3c2)</ref>
    <ref type="project">org/projects/ADVI_COTPPLADVFIX.json</ref>
  </references>
</task_order>
```
