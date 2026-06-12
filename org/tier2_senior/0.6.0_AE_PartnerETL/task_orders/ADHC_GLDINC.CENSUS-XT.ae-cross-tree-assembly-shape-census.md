<to_id>ADHC_GLDINC.CENSUS-XT</to_id>
<project>ADHC_GLDINC</project>
<title>CENSUS-XT — Cross-tree assembly-shape census: inf + cot gold trees + bd C_*/D_* completeness pass (CLASS-N / CLASS-I / SINGLE-SOURCE, line-cited, zero runs)</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<issued_by>2.0.0_SA_COO (CTO arch-ruling queue item 230400Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>staged</status>
<priority>Low — no gate on GLDINC cutovers; fits any capacity window</priority>

<references>
  <ref type="ruling">CTO 20260611T230400Z — A_01-nondeterminism class adjudication: true discriminator = parallel-load ASSEMBLY SHAPE (completion-order append = CLASS-N; index-slot = CLASS-I), not the keep='last' grep</ref>
  <ref type="method">Your own bd census (self-corrected, 2026-06-11) — same method, extended cross-tree</ref>
</references>

<scope>
Code-read census — ZERO runs, line-cited classification — of every parallel-load assembly site in:
1. `data/inf/scripts/gold/*.py` (full tree)
2. `data/cot/scripts/gold/*.py` (full tree)
3. `data/black_diamond/scripts/gold/C_*.py` + `D_*.py` (completeness pass — A_*/B_*/E_* already adjudicated)

For each: CLASS-N (completion-order append feeding order-sensitive dedup — the real A_01/A_04 defect), CLASS-I (index-slot deterministic), or SINGLE-SOURCE (no parallel assembly). Output = one table per tree: script, line citation(s), class, one-line reasoning.

**Fix routing (do NOT fix in this TO):** any CLASS-N found routes per-tree per firm-separation (CLAUDE.md Rule 13 — cot fixes deploy ONLY to opal-data-cot, never mirrored from bd; cross-firm refs are commit- and IAM-blocked). Census report → CTO (adjudication) + COO (decomposition of fixes, never-widen treatment per movement).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before read">
    <step>
      <run>grep -rln "as_completed\|ThreadPoolExecutor\|ProcessPoolExecutor\|imap_unordered" data/inf/scripts/gold/ data/cot/scripts/gold/ data/black_diamond/scripts/gold/C_*.py data/black_diamond/scripts/gold/D_*.py</run>
      <expect>Candidate file list for the census — every parallel-assembly site enumerated before classification.</expect>
      <if_mismatch>Empty trees or unexpected paths: verify tree locations (post-NFRA_DTAFLP renames) before proceeding; do not classify from a partial enumeration.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="census">
    <step>
      <run>Per candidate: read the assembly site; classify CLASS-N / CLASS-I / SINGLE-SOURCE with line citations</run>
      <expect>Every candidate classified; CLASS-N requires BOTH completion-order append AND order-sensitive downstream dedup (keep='last'/'first' or equivalent) — cite both lines.</expect>
      <if_mismatch>Ambiguous shape = classify UNRESOLVED with the specific ambiguity; CTO adjudicates. Do not force-fit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after census">
    <step>
      <run>Deliver census tables to CTO + COO via MCP; commit the census doc to docs/briefs/</run>
      <expect>3 tables (inf / cot / bd-C-D), every row line-cited; CLASS-N count called out in the MCP subject.</expect>
      <if_mismatch>n/a — delivery step.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- Read-only census — no code changes, no S3 artifacts, no overlap with live TOs. GLDINC cutover accumulation (shadow nights) is unaffected.
</cross_domain_coordination>

<acceptance_criteria>
- Census doc committed (docs/briefs/) with 3 line-cited tables covering 100% of the Phase-1 candidate enumeration; zero script runs (cost discipline — shadow harness stays the runtime detector).
- MCP delivery to CTO + COO with CLASS-N count in subject.
- Session log Compiler Tools section reproduces the Phase-1 grep + per-tree candidate counts + classification tallies. Missing = REWORK.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Read-only census; no code or data changes.</no_reprocess_needed></data_reprocess_scope>
