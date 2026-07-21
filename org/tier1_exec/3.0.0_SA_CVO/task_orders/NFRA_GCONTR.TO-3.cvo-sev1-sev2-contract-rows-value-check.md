<to_id>NFRA_GCONTR.TO-3</to_id>
<project>NFRA_GCONTR</project>
<title>Author the SEV1+SEV2 graph_contracts rows (SEV1 first) + the period_defs value-check assertion</title>
<assigned_to>3.0.0_SA_CVO</assigned_to>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff 125904Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>cancelled-suspended</status>
<suspension_note>CANCELLED-as-suspended by 2.0.0_SA_COO~A registry-hygiene sweep 2026-07-21, per NFRA_GCONTR SUSPENDED-INDEFINITE (Andrew-direct sovereign 2026-07-20 ~14:35 ET; verbatim in the project suspend_directive). The SEV1+SEV2 row authoring + period_defs value-check are DROPPED-as-suspended -- CVO does not author, nothing re-surfaces to Andrew.</suspension_note>
<priority>HIGH — parallel-once-table-exists. GO gated on TO-2 (the table must exist to write rows). CVO is live + standing by ("I'll ack + author when you GO the TO"). SEV1 row ratification is further gated on Andrew sign-off (§9 tiered ratified_by).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GCONTR_PRD.md (v0.2) — §3 schema, §4 BMKAUD replay (the worked acceptance), §6 producer lineage, §7 TO-3, §9 RESOLVED policy</ref>
  <ref type="seed">docs/briefs/period-contracts-seed-benchmark-20260615.md (DS~A, 48635a865) — the fully-worked benchmark contract (canonical_writer, period_defs, forbidden_writers)</ref>
  <ref type="scope-ceiling">comp-surface-check list (re-verified by COO 2026-06-16, 0 drift): SEV1 = model_portfolios.headline, model_portfolios.benchmark, advisor_intelligence; SEV2 = model_portfolios.peers, model_portfolios.aum. This IS the v1 scope ceiling (§9) — author exactly this set, stop there.</ref>
  <ref type="value-check-origin">WS-2 benchmark-truth-audit (CVO-owned) — the period_defs check is the codified WS-2 logic (§9 value_check homing).</ref>
</references>

<scope>
Author the contract rows as enforced invariants (one census, written once — vs re-audited by hand every touch) + own the value-check assertion they encode. Rows are written into the `globgrph.graph_contracts` table TO-2 stands up; each row edit is an attributable Nessie commit (`ratified_at` pins it).

**1. SEV1 rows FIRST (§9 scope order):**
   - `model_portfolios.benchmark` (the SEED — fully worked in the brief): canonical_writer = `yang-pipeline-lambda-role`; canonical_producer = yang-benchmarks-etf-returns + its DAG branch; source_of_truth = the upstream canonical benchmark input; artifact_keys = [`json/benchmarks/model_portfolio_benchmarks.json`]; period_defs."1M" = trailing-1-calendar-month (the SEMANTIC contract); forbidden_writers includes `smartx-model-monthly-pull` (the actual override) + the EC2 dual-writer; ratified_by = **[Andrew]** (SEV1 tier, §9).
   - `model_portfolios.headline`
   - `advisor_intelligence` / NNA (advisor_nna_canonical)
**2. THEN SEV2 rows (complete the v1 ceiling):** `model_portfolios.peers`, `model_portfolios.aum` — ratified_by = **[CTO, COO]** (SEV2 tier, §9).
**3. The period_defs value-check assertion (CVO-owned, §9):** the assertion that runs a served column against its `period_defs` — a `1M` that is NOT trailing-1-calendar-month = violation, INDEPENDENT of who wrote it (the value limb, PRD §3.3). This is the codified WS-2 benchmark-truth-audit. You own both the rows AND this assertion.

**§9 HARD CONSTRAINTS:**
- TIERED ratified_by: SEV1 edits (benchmark/headline/advisor_intelligence) require **Andrew** sign-off recorded in `ratified_by`; SEV2 (peers/aum) = **CTO+COO**. The surface's SEV tier (critical-surfaces.yaml) drives WHO must sign. Do NOT self-ratify a SEV1 row — surface to Andrew (via COO) for the SEV1 sign-off; record the authorizing Nessie commit in `ratified_at`.
- SCOPE CEILING = exactly the SEV1+SEV2 set above. Do NOT author rows for non-critical artifacts in v1.
- The benchmark row + TO-2's Q2 wiring together = the BMKAUD-catch end-to-end (joint acceptance with TO-2).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before authoring">
    <step>
      <run>comp-surface-check list</run>
      <expect>SEV1 = {model_portfolios.headline, model_portfolios.benchmark, advisor_intelligence}; SEV2 = {model_portfolios.peers, model_portfolios.aum}. Exactly 5, 0 drift vs PRD §6. This is the authoritative scope ceiling.</expect>
      <if_mismatch>If the set drifted since 2026-06-16, STOP and surface to COO+CTO — the §9 scope ceiling was decided against this exact set; a change re-opens the scope decision.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit (each row)">
    <step>
      <run>schema-conformance check: each row validates against the RATIFIED §3 graph_contracts schema (all required columns; period_defs MAP well-formed; ratified_by tier matches the surface SEV; active=true)</run>
      <expect>Every row conforms; SEV1 rows carry ratified_by=[Andrew] (with the authorizing commit), SEV2 rows ratified_by=[CTO,COO]. No malformed period_defs.</expect>
      <if_mismatch>STOP. A SEV1 row missing Andrew sign-off must NOT be committed as ratified — hold for the sign-off. Fix any schema non-conformance first.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after authoring (acceptance)">
    <step>
      <run>BMKAUD replay (PRD §4): synthetic SmartX write-path into the benchmark artifact with NO ratified contract edit -> comp-surface-check Q1+Q2 (advisory in v1); AND a non-trailing 1M served value -> the period_defs value-check</run>
      <expect>Q1+Q2 mark UNSANCTIONED (advisory WARN in v1 — TO-2 ships advisory); value-check flags the non-trailing 1M as a violation. End-to-end BMKAUD-catch demonstrated — days before an eyeball catch.</expect>
      <if_mismatch>If the replay is NOT caught: the benchmark row (canonical_writer/forbidden_writers/period_defs) is mis-authored, or the value-check assertion is wrong — fix before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-2 (AE) dependency — HARD:** the `globgrph.graph_contracts` table must EXIST before you author rows (parallel-once-table-exists). Converge with AE on the exact schema field USAGE (canonical_writer / forbidden_writers / ratified_by / period_defs) so your rows and AE's Q2 JOIN agree. Schema is RATIFIED (§3) — converge on usage, not re-design.
- **TO-2 joint acceptance:** your benchmark row + AE's Q2 comp-surface-check wiring TOGETHER produce the BMKAUD-catch. Coordinate the Phase-3 replay so it exercises both.
- **Andrew SEV1 sign-off:** SEV1 rows (benchmark/headline/advisor_intelligence) need Andrew in ratified_by — route the sign-off request through COO; do not block on it for the SEV2 rows (CTO+COO can ratify those in parallel).
- **TO-4 (DS) downstream:** DS's pipescript --contract/--flipped READS your rows — your row schema/content is DS's input. No action needed from you, but keep rows schema-conformant.
</cross_domain_coordination>

<acceptance_criteria>
- All SEV1 rows (benchmark, headline, advisor_intelligence/NNA) then SEV2 rows (peers, aum) authored + CVO-attested + Nessie-committed (each edit attributable); the v1 SEV1+SEV2 scope ceiling complete, nothing beyond it.
- SEV1 rows carry ratified_by=[Andrew] with the authorizing Nessie commit in ratified_at; SEV2 rows ratified_by=[CTO,COO]. (Tiered §9.)
- The period_defs value-check assertion is encoded (CVO-owned) and fires on a non-trailing 1M.
- BMKAUD replay (§4) caught end-to-end (with TO-2's Q2) — advisory in v1.
- An uncontracted SEV1 surface reads LOUD `unreviewed` (the false-clean discipline holds on the value layer — never silently "fine").
- Session log Compiler Tools section reproduces every `<run>` above with observed output + explicit pass/fail vs `<expect>`. Missing rows = REWORK.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Contract rows + a value-check assertion are governance metadata on the value layer; they do not change any served artifact, silver/bronze script, or producer. No served-output movement. (The contracts CONSTRAIN future writes; they do not rewrite past data.)</no_reprocess_needed></data_reprocess_scope>
