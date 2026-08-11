# OPAL_ANALYST.EXP1 — /market fallback VISIBILITY (Andrew-expedited)

<task_order>
<id>OPAL_ANALYST.EXP1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.1.0_DE_MarketIntelligence~Z</issued_to>
<date>2026-08-11</date>
<status>pending</status>
<priority>P1 — Andrew-expedited</priority>

<references>
  <ref type="ruling">Andrew ~2210Z @d1baa0b631, "recs approved" — EXPEDITE THE VISIBILITY HALF ONLY. Rationale verbatim: *"a silent wrong number on the default page is the one defect class that reaches clients."*</ref>
  <ref type="spec">org/tier1_exec/1.0.0_SA_CTO/deliverables/MARKET_FALLBACK_VISIBILITY_EXPEDITE_SPEC_20260811.md — A/B/C/D, source-grounded at DEV HEAD. THE SPEC GOVERNS; this TO adds the contract around it.</ref>
  <ref type="finding">W3a `/market` certified run (0.5.0 author, CVO~Z certifier) — R1, grounded independently by three seats</ref>
</references>

<scope>
`portal/src/api/endpoints/market.ts` `getAllReturns` + the `/market` footer render path, on **DEV**.

**THE DEFECT (armed, not fired):** the fallback leg is silent by every surface a person would check —
it synthesises `generated_at: new Date()` (`:239`) so the payload self-reports as current, the six
footers bind manifest `data_pkl` rather than the artifact, and the primary's fallback target has been
unwritten since 2026-04-15 (118 days). Primary is healthy today; exposure is conditional on a primary
failure. **`/market` is the default landing surface** (`/` redirects there and the catch-all sends
every unmatched path there).

**FOUR CHANGES, spec A–D, nothing more:** (A) the fallback response carries a tier marker so the
payload stops claiming to be primary; (B) **`generated_at` STOPS LYING** — carry the artifact's own
date (`firstItemDataAsOf`, already read at `:238`) or omit it, never `new Date()`; (C) the surface
renders the degraded state and the ARTIFACT's date in the footer path the page ALREADY has; (D) the
`:219` warn stays unguarded and carries the artifact date.
</scope>

<requirements>
  <requirement id="1">**(B) is the load-bearing change** — a synthesised freshness stamp on stale data IS the defect, not a symptom. If time forces a subset, B ships first.</requirement>
  <requirement id="2">**No accessor redesign.** The primary/fallback architecture, the 118-day target's restore-vs-retire disposition, and footer-to-artifact binding AS A GENERAL FIX are explicitly OUT — they ride the remediation queue as design calls.</requirement>
  <requirement id="3">**`comp-transform schema-check` on any component whose data props change**, per the DE compiler minimums, before commit.</requirement>
  <requirement id="4">Portal tree stays on **DEV**; standard promotion path only.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-transform schema-check <Component>` for the footer/render surface; `comp-transform fields` if props change shape.</before_write>
  <before_commit>portal lint/typecheck per the repo's own gate.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
  <criterion id="C1">**RENDERED VERIFICATION, not a source read** — the degraded state is EXERCISED (force the fallback path locally) and OBSERVED in a screenshot per the `/frontend-dev` discipline, with the artifact's date visible in the render. *A degraded-state UI claim verified from source is the config-read-for-a-behaviour-claim class (Rule 22a) — and closing an invisible-degradation finding on a source read would be that class at its most embarrassing.*</criterion>
  <criterion id="C2">**`generated_at` no longer synthesised on the fallback leg** — shown by the exercised response, not by the diff alone.</criterion>
  <criterion id="C3">**Healthy path UNCHANGED** — primary-path render and payload identical to pre-change (the negative control: a visibility change that alters the healthy surface has changed more than it was authorized to).</criterion>
  <criterion id="C4">Silver-canvas colour law honored on any new visual state (the standing portal defect class); session log with Compiler Tools section.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4</expected_criteria>
  <instance_path>org/tier3_junior/0.1.0_DE_MarketIntelligence/deliverables/OPAL_ANALYST.EXP1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">The A–D change on DEV</deliverable>
  <deliverable type="document">The rendered evidence (degraded + healthy), proof-of-spec instance, session log</deliverable>
</deliverables>

<do_not>
  <rule>⛔ **THIS IS NOT AN ALARM AUTHORIZATION. The moratorium is untouched.** Existing UI and existing logs ONLY. No alert, alarm, SNS, SES, monitor, freshness checker, or notification machinery — any of that needs Andrew's SEPARATE word (his bound, in his ruling).</rule>
  <rule>⛔ **No direct PROD act.** DEV branch, standard promotion.</rule>
  <rule>No accessor redesign; no touching the 118-day-stale target; no general footer-binding fix.</rule>
  <rule>Do not push (lane commit; MSTR~Z integrates).</rule>
</do_not>
</task_order>
