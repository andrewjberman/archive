<task_order>
<id>MDPF_3FIRMS.3F-P3a</id>
<title>Cottonwood page DEV render + rendered screenshots for Andrew — the SLICE of 3F-P3 that opens on G8-green (NOT all-WS-G)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-P (Platinum) — SCOPED SLICE of 3F-P3, dependency-gated on G8-green</workstream>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-23T00:50Z</issued_at>
<status>staged</status>
<priority>ANDREW-DIRECT (goal function restated). Verbatim below. Opens on G8-green; DE is idle-reserved for it.</priority>

<authorization>
Andrew-direct at the CTO terminal ~00:4xZ, VERBATIM (custody CTO's): "what i want to know is where is
the frontend Cottonwood page for MDPF" ... "The entire point of _3FIRMS was to get to that point."
-> CTO ruling 004927Z (the Cottonwood slice of 3F-P3 opens on G8-green) -> COO wiring.
</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-P row 3F-P3; §2.4 FE state (the closed-series-literal defect)</ref>
  <ref type="predecessor">3F-P1 (@39ea5916e) — the consumption locus table + the closed-literal finding; 3F-G8 — the artifacts this renders</ref>
  <ref type="skill">/frontend-dev — the render-read-check-color-law loop (a grep cannot see blankness or contrast)</ref>
</references>

<gate priority="READ FIRST — this is a SLICE, not all of P3">
⚠ **THIS OPENS ON G8-GREEN, NOT the all-legs WS-G barrier — a deliberate CTO narrowing, same logic as G8's own gate.** It consumes ONLY 3F-G8's staged output (the Cottonwood account-distribution + aum-metrics pair), which exists tomorrow morning once DS builds G8 on the B5 (~03:30Z) gate. The all-WS-G gate exists to protect FE builds from UNVERIFIED gold SHAPES; the shape THIS slice consumes is the G8-built one, so it is safe to render against it early.
⛔ **THE REST OF 3F-P3 STAYS WS-G-GATED as written** — cross-firm parity, Global rendering, and P4/P5 do NOT open here. This slice is Cottonwood-only, DEV-only, screenshots-only.
</gate>

<scope>
**Andrew wants to SEE the Cottonwood page. The deliverable is RENDERED SCREENSHOTS WITH REAL NUMBERS, to him.**

1. **Build the Cottonwood rendering path on portal DEV** against the staged G8 artifacts (`json/mdpf/cottonwood/{account-distribution,aum-metrics}.json`). Dropdown -> charts working for the `cottonwood` firm selection.
2. **Fix the closed-series-literal defect AT LEAST for the Cottonwood path** (§2.4): the trend chart's series list is a **closed literal**, so a model absent from the literal renders BLANK while legend + donut draw — every guard was built for a VALUE being absent, none for a SERIES being absent. Make the series list **data-driven** for Cottonwood so its models render. (Generalizing to all firms is 3F-P3 proper, WS-G-gated — here, at least Cottonwood renders.)
3. **Colour collision fixed IF CHEAP** (two Cottonwood models collapsing to the same colour) — deterministic per-model colours. If not cheap, note it and defer to 3F-P3.
4. **DELIVER RENDERED SCREENSHOTS WITH REAL NUMBERS to Andrew via the /frontend-dev loop** — per firm view (Cottonwood), showing populated trends + distribution, the numbers legible.

⛔⛔ **NOTHING SERVED. NO PORTAL PROMOTE. DEV ONLY.** The portal main tree stays on DEV (portal rule 19). This is a render-and-screenshot deliverable, not a deploy. The one flip (WS-F) and any PROD promote are separate, gated, and NOT here.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step>
      <run>comp-transform schema-check ModelPortfolios --feature cottonwood</run>
      <expect>The Cottonwood cohort's rendered fields enumerated; MISSING = runtime undefined, itemize.</expect>
      <if_mismatch>A MISSING field on a SEV1 surface is a latent runtime undefined — fix before rendering.</if_mismatch>
    </step>
    <step>
      <run>comp-transform ternary-audit ModelPortfolios</run>
      <expect>The series-literal + firm-branch sites enumerated — the fix list for the closed-literal defect.</expect>
      <if_mismatch>The audit output IS the fix list; encode it, do not eyeball the component.</if_mismatch>
    </step>
    <step>
      <run>comp-surface-check (BY HAND — it cannot block)</run>
      <expect>Read it yourself. ModelPortfolios is SEV1 (CRITICAL on model_portfolios.headline + .benchmark).</expect>
      <if_mismatch>Silence is not a pass; an unblocked commit is not a clearance. Read the output.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before screenshot">
    <step>
      <run>bunx tsc -b (portal DEV)</run>
      <expect>Zero TypeScript errors on the Cottonwood path.</expect>
      <if_mismatch>STOP; a type error on the rendered path is a defect Andrew would see.</if_mismatch>
    </step>
    <step>
      <run>/frontend-dev render loop: headless render of the Cottonwood MDPF view, READ the screenshot</run>
      <expect>Trends POPULATED (not blank), distribution drawn, numbers legible, silver-canvas color law honored (no light text / ghost buttons outside a dark Panel).</expect>
      <if_mismatch>A grep cannot see blankness or contrast — the RENDERED screenshot is the acceptance instrument. A blank trend chart with a drawn legend is the exact §2.4 defect; it must be fixed, not screenshotted as-is.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>comp-transform schema-check ModelPortfolios (re-run)</run>
      <expect>No new MISSING introduced; DEV tree still compiles.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>FE render on DEV against already-staged G8 artifacts. No data written, no pipeline
  run, no deploy. Screenshots are the output.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="json/mdpf/cottonwood/*.json (G8 staged output)" shared_with="0.4.0_DS (3F-G8)">
    You consume G8's staged artifacts. Do NOT start until DS confirms G8 core is staged (G8-green). MCP DS
    for the staged artifact paths + confirmation.
  </resource>
  <resource path="portal DEV ModelPortfolios.tsx" shared_with="future 3F-P3 (WS-G-gated)">
    Your Cottonwood-path series-literal fix is a subset of P3's full data-driven-series fix. Note what you
    changed so P3 generalizes it rather than re-doing it.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_3FIRMS.3F-G8" status="staged" blocking="true">
    G8 core artifacts must be staged (G8-green). G8 gates on B5 (~03:30Z). Start when DS confirms staged.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Cottonwood firm selection renders on portal DEV: dropdown -> charts working against staged G8 artifacts.
2. The closed-series-literal defect fixed at least for the Cottonwood path — its models render, not blank.
3. Colour collision fixed if cheap, else noted + deferred to 3F-P3.
4. **RENDERED SCREENSHOTS WITH REAL NUMBERS delivered to Andrew** (via /frontend-dev), trends populated,
   numbers legible, silver-canvas color law honored — the screenshot is the acceptance instrument.
5. Zero served, zero promote, DEV only; portal main tree on DEV.
6. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; screenshots to Andrew. Escalate if the G8 artifact shape does not support the
render (that is a G8 defect, not a P3a one), or if the closed-literal fix cannot be scoped to Cottonwood
alone without touching the WS-G-gated cross-firm path.
</escalation>
</task_order>
