<task_order>
<id>MDPF_3FIRMS.3F-BF2</id>
<title>Cottonwood FE Interpolated band (yellow-dash overlay) + the single paired-read accessor with its direct-read-failing test</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-BF (Interpolated Backfill) — build, DE lane</workstream>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-23T03:53Z</issued_at>
<status>staged</status>
<priority>ANDREW-DIRECT "I need both right now immediately" -> CTO 035119Z -> decompose + GO NOW.</priority>

<authorization>Andrew-direct 022726Z + 0351Z -> CTO 035119Z -> COO. CVO clearance @816d48cc9 (pinned pair).</authorization>

<references>
  <ref type="spec-schema-SOURCE-OF-TRUTH">CRO interpolation delta @708661904 — THE CANONICAL BUILD SCHEMA (the point_class + served-slice shape). Do NOT use CTO's §4 block.</ref>
  <ref type="cvo">3.0.0_SA_CVO @816d48cc9 (R-5: pin binds these EXACT commits)</ref>
  <ref type="skill">/frontend-dev — render-read-check-color-law (a grep cannot see a dashed band or a contrast fault)</ref>
  <ref type="peer">3F-BF1 (DS producer) — emits the point_class[] your accessor reads; align the exact shape with DS</ref>
</references>

<scope>
Build the FE surface for the interpolated backfill on the Cottonwood MDPF trend:

1. **THE SINGLE PAIRED-READ ACCESSOR** — one accessor that returns value + provenance (point_class)
   TOGETHER, from DS's served `point_class[]`. **A TEST THAT FAILS on any DIRECT read of a value array**
   is part of the contract (guard-1 "no unlabeled read" at the served boundary, interim before the F1
   tuple reshape). The test failing-on-violation is the enforcement — a convention nobody can bypass by
   reading the raw array.
2. **THE INTERPOLATED BAND** — render interpolated points as a conspicuous **yellow dashed line** over
   the affected period, visually distinct from measured points. Read `point_class` to decide the render;
   never render an interpolated point identically to a measured one.

⚠ **SCHEMA SOURCE = CRO's @708661904** (the point_class enum + served-slice shape). Do NOT copy CTO's §4
block. R-5: a spec change re-enters review.
</scope>

<binding_laws priority="NON-NEGOTIABLE EVEN AT SPEED">
⛔ **THE DIRECT-READ-FAILING TEST IS THE CONTRACT, not a nice-to-have** — it must FAIL if any code reads a
value array without its provenance. Andrew overrides WAITING, never CHECKS: at speed, you still ship the
failing-on-violation test.
⛔ **CONSPICUOUSLY LABELED, VISUALLY DISTINCT** — "Interpolated" + yellow dashed line. Andrew's own words.
An interpolated point rendered like a measured one is the fabrication class at the display layer.
⛔ **THE SCREENSHOT IS THE ACCEPTANCE INSTRUMENT** — a grep cannot see whether the dashed band renders,
whether the color law holds, or whether an interpolated point looks measured. Render it, read it.
⚠ **UPGRADE-READY:** the signed schema has REAL temporal data (from the parallel qt5 upside path)
SUPERSEDING interpolated points as it arrives — a point can flip interpolated->measured. Your accessor +
band must render correctly as the interpolated region SHRINKS when real data replaces estimates; do not
hardcode the band extent.
</binding_laws>

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step>
      <run>Align the point_class[] shape with DS (3F-BF1) + read CRO's @708661904</run>
      <expect>Your accessor's read contract == DS's emit contract, both from @708661904.</expect>
      <if_mismatch>MCP DS; do not guess the shape or read it from CTO's §4.</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check ModelPortfolios --feature interpolated</run>
      <expect>The point_class-bearing fields enumerated; MISSING = runtime undefined.</expect>
      <if_mismatch>Itemize MISSING; fix before rendering.</if_mismatch>
    </step>
    <step>
      <run>[STRUCK 2026-08-21 BY THE ISSUER (COO) — comp-surface-check is RETIRED, Andrew-direct 2026-08-06: "I want comp-surface-check retired. i do not like that tool." Executable, registry rows, comp-which route, S3 publish leg, portal CI leg and pre-commit hook were all removed. THIS STEP WAS UNRUNNABLE FROM 08-06 ONWARD AND MADE THIS TO UNSATISFIABLE-BY-CONSTRUCTION.] SUBSTITUTE: none, deliberately. Per CLAUDE.md Rule 20 the MP/benchmark/ADVI surfaces now carry NO automated commit-time guard and "that is the accepted consequence of the ruling" — re-instrumenting here would rebuild what Andrew retired. The SEV1 CARE remains: ModelPortfolios is SEV1, so render and read the surface (the /frontend-dev screenshot loop is the surviving instrument), and state what you read.</run>
      <expect>A rendered read of the SEV1 surface, stated. Silence is not a pass.</expect>
      <if_mismatch>Silence is not a pass.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>The direct-read-failing test</run>
      <expect>FAILS on a direct value-array read; PASSES via the paired accessor.</expect>
      <if_mismatch>⛔ A test that does not fail on the violation is not the guard. Non-negotiable.</if_mismatch>
    </step>
    <step>
      <run>bunx tsc -b (portal DEV)</run>
      <expect>Zero TS errors on the interpolated path.</expect>
      <if_mismatch>STOP.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="render-verify">
    <step>
      <run>/frontend-dev render of the Cottonwood trend with an interpolated region; READ the screenshot</run>
      <expect>Interpolated points render as a conspicuous yellow dashed line, visually distinct from measured; color law honored; no interpolated point looks measured.</expect>
      <if_mismatch>A grep cannot see this — the rendered screenshot is the acceptance. An interpolated point indistinguishable from measured is a fail.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope><no_reprocess_needed>FE render on DEV against the served slice. No data written.</no_reprocess_needed></data_reprocess_scope>

<cross_domain_coordination>
  <resource path="point_class[] contract" shared_with="0.4.0_DS (3F-BF1)">
    DS emits, you read. Same shape, both from @708661904. Align before building the accessor.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_3FIRMS.3F-BF1" status="staged" blocking="partial">
    You can build the accessor + band against the schema now; the live render-verify needs DS's served
    point_class[]. Build in parallel, render-verify when DS serves.
  </dependency>
</dependencies>

<acceptance_criteria>
1. ONE paired-read accessor (value+provenance together) + a test that FAILS on any direct value-array read.
2. Interpolated band renders as a conspicuous yellow dashed line, visually distinct from measured — screenshot-verified.
3. `point_class` read from the served slice per @708661904; no interpolated point rendered as measured.
4. Upgrade-ready: the band renders correctly as the interpolated region shrinks (real data superseding estimates); band extent NOT hardcoded.
5. Zero TS errors **— VERIFIED WITH `bun run typecheck` / `tsc -b`, NEVER bare `tsc --noEmit`** (AMENDED 2026-08-21 by the issuer, folding a same-day measured finding: the portal's root tsconfig.json is `"files": []` with project references only, so `tsc --noEmit` compiles an EMPTY set and returns rc=0 OVER DELIBERATE TYPE ERRORS — **its mutant control PASSES**. A criterion reading "zero TS errors" verified by the obvious command would have been satisfied by an instrument that checked nothing. Portal law: portal/CLAUDE.md "Typecheck law" @82d3f28f, on origin/DEV); ~~comp-surface-check read by hand~~ **STRUCK — the tool is RETIRED (Andrew-direct 2026-08-06) and this clause made the TO unsatisfiable-by-construction; no substitute instrument, per Rule 20's accepted consequence**; color law honored.
6. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. Escalate if the direct-read-failing test cannot be made to fail-on-violation, or if an interpolated point cannot be made visually distinct from measured.</escalation>
</task_order>
