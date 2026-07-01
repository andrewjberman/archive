# TASK ORDER — NFRA_COMPRAIL.TO-5 (the close TO)

<issued_to>0.8.0_AE_CloudComp~E</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>
<!-- DELIVERED 2026-07-01: comp-rail-audit 3b87a05a1 (pushed). Telemetry 89% rail-found; broad-grep FP/TP scoped to governed repo-grep = 4% on 27 thin/dryrun events -> HOLD recommendation (data-insufficient for a fabric-wide hard-deny; nudge already works, 769 comp-grep adoptions). RAVC'd COO~B + CVO~B + CTO. COMPRAIL close finalizes on COO+CVO disposition of the HOLD (their gate). Coverage-gap classes -> COMPLEARN. -->

<priority>MEDIUM — Andrew-direct close-out drive (2026-07-01). COMPRAIL core is LIVE + enforcing fabric-wide (TO-2/3/4 complete, Andrew GO 06-22). TO-5 is the LAST tier + the close TO. NOT gate-lift-gated; sequence behind your COMPLEARN close + the active wave. You own the rail-log via COMPLEARN's tool_activity, so you're the natural owner.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPRAIL (the FIRES verb) is LIVE + enforcing: tier-1 raw-aws-inspection + tier-2a infra/.tf-grep DENY w/ `# rail-checked:` override; native Grep/Glob NUDGE. PRD: `docs/architecture/NFRA_COMPRAIL_PRD.md`. The ONE remaining tier = the STAGED broad-repo-grep tier (friction-sensitive, enables only after a proven-coverage FP pass). TO-5 does the post-enforce telemetry + the coverage-audit that GATES that enablement. This is the COMPRAIL close TO.

## Objective
(1) Post-enforce TELEMETRY + coverage-audit over `org/mcp/comp-which-rail.log` (the enforce-window data): are agents finding the rail (route-vs-run rates, repeat-override intents = coverage gaps)? (2) The broad-repo-grep tier FP-pass EVIDENCE -> a GO/NO-GO recommendation to COO~B+CVO~B (the enablement is a DELIBERATE COO+CVO call, NOT auto -- friction-sensitive). Landing (1)+(2) closes COMPRAIL.

## Scope — TO-5
1. **Telemetry/coverage-audit:** analyze the rail-log enforce-window: route vs on-rails-run distribution; repeat `# rail-checked:` overrides for the SAME intent (each = a coverage-gap signal -> a tool to build, ties to COMPLEARN's routing-miss candidates -- reuse your P2 corpus). Emit a coverage report.
2. **Broad-grep-tier FP-pass:** run the FP/TP evaluation on a broad-repo-grep DENY (would it deny legitimate broad searches?). Quantify the friction. Recommend GO (enable) / HOLD (coverage insufficient) / NO-GO to COO~B + CVO~B -- do NOT enable it yourself; the settings-matcher change is COO+CVO-gated (friction-sensitive, fabric-wide).
3. **Close evidence:** the telemetry report + the FP-pass + the recommendation = the COMPRAIL close artifacts.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read org/mcp/comp-which-rail.log (the enforce-window) + reuse your COMPLEARN P2 rail-log corpus (1957 rail rows)</run>
      <expect>Route/run/override distribution computable; repeat-override intents identifiable (the coverage-gap signal). Rail-log is the live enforce-window data.</expect>
      <if_mismatch>STOP. If the rail-log isn't capturing enforce events, that itself is a telemetry gap -> flag COO~B.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>the broad-grep FP/TP evaluation on a representative intent set</run>
      <expect>FP rate quantified; a defensible GO/HOLD/NO-GO recommendation with the friction tradeoff. NO settings change made (COO+CVO-gated).</expect>
      <if_mismatch>If coverage is insufficient for a clean FP pass, recommend HOLD + name the gaps to build (feeds COMPLEARN). That's a valid close (the tier stays staged-by-design).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 2.0.0_SA_COO~B + 3.0.0_SA_CVO~B: the broad-grep-tier enablement is OUR gated call (friction-sensitive, fabric-wide) -- you recommend, we decide. Do NOT wire the settings matcher yourself.
- NFRA_COMPLEARN (yours, CLOSED): the repeat-override coverage gaps ARE routing-miss/build-new candidates -- reuse the corpus + the value-scorer.
- 1.0.0_SA_CTO: CC on the coverage-audit + the tier recommendation.
</cross_domain_coordination>

<acceptance_criteria>
1. Post-enforce telemetry/coverage report over the live rail-log (route/run/override rates + repeat-override coverage gaps).
2. Broad-grep-tier FP/TP pass + a GO/HOLD/NO-GO recommendation to COO~B+CVO~B (no self-enablement).
3. Session log Compiler Tools section reproduces every run. RAVC COO~B + CC CVO~B + CTO -- this + the COO+CVO disposition on the broad-grep tier closes COMPRAIL (the core rail is already live+enforcing; TO-5 closes the last tier's disposition).
</acceptance_criteria>

## Note
COMPRAIL's core value (comp-which-first, enforcing) is already delivered + Andrew-GO'd live. TO-5 disposes the last (friction-sensitive) tier honestly -- a HOLD recommendation (tier stays staged-by-design, gaps fed to COMPLEARN) is a valid close, NOT a failure. The point is a GROUNDED disposition, not force-enabling a friction gate mid-session.
