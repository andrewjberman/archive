<to_id>NFRA_GLOBGRPH.TO-F1</to_id>
<project>NFRA_GLOBGRPH</project>
<title>TO-F1 — Kuzu query-surface provenance: _build_manifest.json in all 3 loaders + comp-kuzu provenance header + 26h age-warn + commit-distance staleness + UNKNOWN-VINTAGE path + F4 loader hygiene</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 232252Z + v0.4.1 delta 233040Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete</status>
<priority>P1 — ungated; lands first, closes the frozen-vintage class (CVO verdict be17d49eb)</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GLOBGRPH_PRD.md §2b (v0.4 5208e0193 + v0.4.1 a4b22465c) — rulings F1 + F4; AC10(a)</ref>
  <ref type="verdict">org/tier1_exec/3.0.0_SA_CVO/logs/2026-06-11/kuzu_nessie_mechanics_verdict.md (be17d49eb)</ref>
</references>

<scope>
1. **Manifests (F1):** each loader — `infra/aws/globgrph/kuzu_load.py`, `kuzu_nessie_load.py`, `kuzu_stitch_load.py` — writes `_build_manifest.json` beside its DB on every successful build: `source_kind` (tarball|nessie|stitch), exact source vintage (tarball S3 key / **Nessie ref + snapshot-id PIN** / stitch file path+mtime), `built_at` UTC, node + edge counts.
2. **Provenance header:** every `comp-kuzu` invocation (`kuzu_cli.py`) prints a header from the manifest: which DB, built-when, from-what-source, counts. Age > threshold (default 26h = missed-nightly signal; configurable) ⇒ WARN.
3. **Commit-distance staleness (v0.4.1):** for Nessie-sourced DBs, compare the manifest snapshot-id pin against the newest warehouse `metadata.json` at query time (cheap S3 list — same mechanism `kuzu_nessie_load` already uses); print `BEHIND Nessie HEAD by N commits` when trailing. (Auto-refresh is TO-F2 scope — here it only NAMES the staleness.)
4. **UNKNOWN-VINTAGE:** absent manifest ⇒ loud `UNKNOWN VINTAGE` warning, never silence.
5. **F4 loader hygiene:** `kuzu_nessie_load.py` defaults `--force` (or refuses if the DB exists) — merge-without-delete structurally cannot drop phantoms (verdict leg 4).
6. **F5 doctrine echo (no code):** read-your-own-writes verification goes to served-artifact / live AWS, NEVER the graph (`feedback_verify_against_served_artifact_not_partial_proxy`). The graph is the traversal surface where minutes-stale-and-labeled is acceptable. Do not treat graph freshness as a verification substitute anywhere in this work.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read infra/aws/globgrph/kuzu_cli.py + kuzu_load.py + kuzu_nessie_load.py + kuzu_stitch_load.py; grep -rn "comp-kuzu\|kuzu_cli" org/modules/graph/graph-call-manifest.yaml .tools/ org/modules/</run>
      <expect>Complete caller inventory — every invocation path that reaches kuzu_cli.py (direct .tools/comp-kuzu wrapper, manifest entries, any module import). Header must land on EVERY path.</expect>
      <if_mismatch>STOP. A caller path that bypasses the header silently re-opens the unlabeled-vintage class. Surface unexpected callers to COO before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-kuzu smoke query against all 3 current DBs (kuzu_db, kuzu_nessie_db, kuzu_stitch_db)</run>
      <expect>Each prints the provenance header with the correct per-DB vintage; Nessie-sourced DB shows snapshot-id pin + commit-distance line; a manifest-less DB (use a scratch copy) prints loud UNKNOWN VINTAGE.</expect>
      <if_mismatch>STOP. Do not commit until all 3 surfaces + the UNKNOWN-VINTAGE path demonstrate.</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh on every touched .py</run>
      <expect>py_compile + ds-precommit-check + ruff (0.15.11, py39) all exit 0.</expect>
      <if_mismatch>Fix before commit; gate is universal for .py edits (CLAUDE.md Rule 14).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Update org/modules/graph/graph-call-manifest.yaml + org/modules/graph/comp-tools.yaml comp-kuzu entries to document the provenance/freshness contract</run>
      <expect>Manifest freshness field for comp-kuzu cites the header + 26h warn + BEHIND-by-N semantics; comp-tools.yaml row matches.</expect>
      <if_mismatch>Doc lag = the contract is invisible to the fabric; complete before RAVC2.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **AE~B Item-2b delete-propagation P1 fix (CVO-routed direct, no TO file):** SAME-SESSION PAIRING IS LOAD-BEARING (PRD v0.4.1 flags it in-PRD as the hard dependency for trusting freshness). Coordinate before touching `infra/aws/globgrph/` shared files — AE~B's fix targets the incremental updater / 2b path; TO-F1 targets loaders + CLI. Low file overlap but same directory; MCP each other before commit if both in flight.
- NFRA_GRAPHS.D4 + NFRA_GLOBGRPH.P2-STITCH-CORE: both COMPLETE/SATISFIED (f754164b4) — no live overlap; pending CTO deep-cert + CVO AC7 cert are read-only vs this TO.
</cross_domain_coordination>

<acceptance_criteria>
- AC10(a) verbatim: every comp-kuzu invocation prints the provenance header (DB, built-when, source vintage incl. Nessie snapshot-id pin, counts), WARNs past the age threshold, and for Nessie-sourced DBs reports `BEHIND Nessie HEAD by N commits` when the pin trails the warehouse; a manifest-less DB yields a loud UNKNOWN-VINTAGE warning — demonstrated on all three current DBs.
- kuzu_nessie_load.py --force-default (or refuse-if-exists) demonstrated.
- Session log includes Compiler Tools section reproducing every `<run>` from `<compiler_tools_mandate>` with observed output and explicit pass/fail vs `<expect>`. Missing rows = REWORK.
- RAVC2 evidence to COO: commit hash(es) + the 3-DB smoke output + manifest/comp-tools doc diff.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Platform tooling only (graph loaders + CLI); no silver/bronze converters, no S3 data-prefix writes.</no_reprocess_needed></data_reprocess_scope>
