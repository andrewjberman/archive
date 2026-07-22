<task_order>
<id>MDPF_3FIRMS.3F-S4</id>
<title>Cross-firm silver schema parity — canonical shape per data class + column-level contract per gold consumer</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-S (Silver)</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:29Z</issued_at>
<status>complete</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-S row 3F-S4; §3.1 canonical per-firm shape; §3.2 layer contracts</ref>
</references>

<scope>
Andrew's §0 words drive this TO: *"it is important that as we fork off for firms in this process that we
are doing our best to be canonical in data shape and architecture."*

(a) **Document the CANONICAL silver shape per DATA CLASS** — holdings / assets / positions — across all
    three firms. The `_s2` schema-2 pattern is the reference.
(b) **Column-level contract per GOLD CONSUMER**: for every column a gold script reads, map it to a
    source column or a NAMED derivation.
(c) **Name every divergence with a disposition** (canonicalize / accept-with-reason / defer).

⚠ **AUTO-RULE 7 — EMPIRICAL PARQUET INSPECTION, NEVER DOCSTRINGS.** Read the actual parquet schemas.
A docstring is a claim about a file; the file is the fact. This is the declared-vs-applied class that
produced three separate incidents on 2026-07-22 alone.

⚠ **ZERO UNMAPPED READS is the bar.** A gold script reading a column that maps to nothing is either a
latent KeyError or a silent null — both reach a served number.

⚠ §3.1 already ANSWERS the architectural question you raised: **silver IS the canonical source for the
firm total** (`fact_rps_s2` for 49F, `fact_assets` for Inflection, **`fact_holdings` for Cottonwood**).
The runner reads silver for totals and gold `dim_model_portfolio` for the Cottonwood model
decomposition. What was missing is the GRANT (3F-S3), not an artifact. **Do not design a new gold
artifact to carry firm totals.**

⛔ **CORRECTION @2026-07-22T21:00Z — THIS TO ORIGINALLY SAID `fact_holdings_s2` FOR COTTONWOOD. THAT WAS
WRONG, AND IT WAS MY ERROR: I transcribed it from PRD §1.2 without checking, which is the exact
declared-vs-applied failure this TO's auto-rule 7 exists to prevent.** Your own S2 measurement disproved
it and 3F-S3's joint determination (@`517bcb235`, three independent limbs) settled it:
- **`fact_holdings` (16,762 x 24) = the real holdings table, CANONICAL for the COT AUA total.**
- **`fact_holdings_s2` (5 x 7) = the BD vendor TIMESTAMPS sheet**, landed as section 2 by the
  never-drop-a-sheet law (`mirror_schemas.py TIMESTAMPS_SECTION @61365878d`); 4,565 B vs 388,478 B on
  `date=2026-07-20`.
- **The live builder reads `fact_holdings` and is CORRECT AS-IS.** No read-path change.

>> **THIS IS THE SUBJECT OF YOUR OWN TO, DEMONSTRATED ON THE TO ITSELF: `_s{N}` IS NOT A SCHEMA
CONTRACT.** Schwab's `fact_rps_s2` IS the real balances table (7,086 x 39); Cottonwood's `_s2` is
metadata. **The suffix means "section N of the vendor workbook," which is a per-vendor accident of
layout, not a tier or a schema version.** Everyone — the PRD, me, and by pattern-match anyone reading
Schwab first — read it as a contract. **Make that explicit in the contract document; it is the single
most valuable thing this TO can leave behind.** <<
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io on every gold script consuming the six MDPF-feeding silver tables</run>
      <expect>Full READS list per script; COLUMN GAPS empty.</expect>
      <if_mismatch>Non-empty COLUMN GAPS is a direct finding for this TO — itemize. ⚠ KNOWN GAP: `io` misses cross-bucket served imports in helper functions; supplement with source reads.</if_mismatch>
    </step>
    <step>
      <run>Empirical parquet schema inspection per table (actual files, not docstrings)</run>
      <expect>Column name + dtype per table, at a stated partition vintage.</expect>
      <if_mismatch>A schema claim without a partition vintage is not a citation. State which partition you read.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Build the consumer->source column map; identify unmapped reads</run>
      <expect>Every gold-consumer column maps to a source column or a NAMED derivation. Unmapped set = EMPTY.</expect>
      <if_mismatch>Each unmapped read is itemized with the consuming file:line @ commit-ish and routed to its owner. Do not silently drop it.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on any shared silver table before proposing a canonicalization</run>
      <expect>Blast radius enumerated; cross-domain consumers named.</expect>
      <if_mismatch>Any node in 2+ blast radii is CROSS-DOMAIN — MCP the other owner before committing.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run comp-pipescript io across the consumer set</run>
      <expect>No new COLUMN GAPS introduced.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Documentation + contract only. **If a canonicalization requires a silver
  converter change, that is a SEPARATE TO with its own reprocess scope** — a schema change to a silver
  table is Rule-17-sensitive and rewrites historical partitions. Do not fold one into this TO.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="all six silver fact tables" shared_with="0.6.2_AE_PartnerETL~A (B-legs, S1) + 0.7.0_AE_CloudOps (S3)">
    Overlaps every bronze/silver TO. Your contract is the reference the others verify against —
    circulate before committing.
  </resource>
  <resource path="fact_holdings vs fact_holdings_s2" shared_with="3F-S3">
    The canonical determination is made in S3 with 0.7.0. Consume that decision; do not duplicate it.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_3FIRMS.3F-S2" status="staged" blocking="false">
    S2's census surfaces the tables; running S2 first is efficient but not required.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Contract document committed: canonical silver shape per data class across all three firms.
2. **Every gold-consumer column maps to a source column or a named derivation — ZERO unmapped reads**
   (or each itemized with owner + file:line @ commit-ish).
3. Divergences named with an explicit disposition.
4. All schema evidence is EMPIRICAL parquet inspection at a stated partition vintage — never docstrings.
5. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. Escalate any unmapped read on a served-number path immediately.</escalation>
</task_order>
