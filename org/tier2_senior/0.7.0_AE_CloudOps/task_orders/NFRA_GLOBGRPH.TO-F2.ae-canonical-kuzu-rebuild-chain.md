<to_id>NFRA_GLOBGRPH.TO-F2</to_id>
<project>NFRA_GLOBGRPH</project>
<title>TO-F2 — Canonical Kuzu surface: one Nessie-rebuilt kuzu_db as comp-kuzu default + rebuild-on-HEAD-advance auto-refresh + build mutex / atomic-swap concurrency</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 232252Z + v0.4.1 delta 233040Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>staged</status>
<priority>P1.5-follow — GATED on Item-2a stability (CTO declares; do NOT start on TO-F1 completion alone)</priority>

<gate>
Item-2a (hybrid freshness nightly chain, PRD §2a) declared STABLE by CTO. Additionally per PRD F5 caveat: AE~B's Item-2b delete-propagation P1 fix is the hard dependency for TRUSTING auto-refresh freshness — confirm it has landed before flipping auto-refresh on as default behavior.
</gate>

<references>
  <ref type="prd">docs/architecture/NFRA_GLOBGRPH_PRD.md §2b (v0.4 5208e0193 + v0.4.1 a4b22465c) — ruling F2 + v0.4.1 multi-agent concurrency reqs; AC10(b)+(c)</ref>
  <ref type="dependency">NFRA_GLOBGRPH.TO-F1 (manifests + pin + commit-distance check are the substrate this TO's auto-refresh triggers on)</ref>
</references>

<scope>
1. **Canonical surface:** collapse the three-vintage interim to ONE canonical rebuild chain — Nessie (post-nightly-2a + accumulated-2b) → single canonical `kuzu_db`. `comp-kuzu` default points ONLY there. Scratch/alternate DBs (`kuzu_ac7.db`, per-cert scratch) remain addressable via explicit `--db` flag only — never default.
2. **Rebuild trigger = HEAD-advance, not cron (v0.4.1):** when TO-F1's pin-vs-HEAD check detects BEHIND, the canonical surface auto-refreshes — so agent A's re-query after agent B's cloud change reads post-change state once 2b has committed it. Writer side needs nothing: agents never write the graph; CloudTrail→2b→Nessie event-sources every change regardless of author; Nessie serializes commits.
3. **Concurrent-rebuild safety (v0.4.1):** rebuilds run under a build MUTEX (workspace mkdir-mutex pattern, cf. safe-commit.sh commit-mutex v2) + build-to-tempdir-and-atomic-rename SWAP. Readers never see a half-built DB; a lost mutex race waits or reuses the fresh winner's result. Without this, the Windows half-wipe MERGE-union corruption (kuzu_nessie_load.py docstring: 1,967 nodes from an 1,180-row table) becomes routine with N agents on one working tree.
4. **F5 doctrine echo (no code):** auto-refresh does NOT make the graph a verification surface — read-your-own-writes verification stays on served-artifact / live AWS. Graph = traversal only.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-kuzu provenance header on all current DBs (TO-F1 must be live); re-grep callers as in TO-F1 Phase 1 for any new invocation paths since</run>
      <expect>TO-F1 contract demonstrably in place (headers + pin + BEHIND reporting); caller inventory unchanged or delta understood.</expect>
      <if_mismatch>STOP. TO-F2 builds on the F1 substrate; surface gaps to COO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Concurrency demonstration: N>=3 concurrent comp-kuzu invocations that each trigger refresh on a deliberately-stale canonical DB</run>
      <expect>No corrupt/half-built DB at any point; exactly one rebuild wins; losers wait or reuse; node/edge counts match the single-rebuild oracle. (= AC10(c))</expect>
      <if_mismatch>STOP. Do not commit a default-surface flip with unproven concurrency safety.</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh on every touched .py</run>
      <expect>All checks exit 0.</expect>
      <if_mismatch>Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Real query against the post-flip default surface; update graph-call-manifest.yaml + comp-tools.yaml (default DB + auto-refresh semantics)</run>
      <expect>Default surface serves canonical Nessie-rebuilt DB, at-worst one-nightly-old or 2b-fresh (= AC10(b)); docs match.</expect>
      <if_mismatch>Surface to COO; consider reverting the default repoint until resolved.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **AE~B Item-2b delete-propagation fix:** gate-condition AND shared-directory coordination (see TO-F1 block).
- **Any agent using `comp-kuzu` mid-flip:** the default-DB repoint changes what every fabric agent's query answers. Announce the flip via MCP to CTO+COO before committing it; CTO certs the contract change.
</cross_domain_coordination>

<acceptance_criteria>
- AC10(b): post-F2, comp-kuzu default surface serves the canonical Nessie-rebuilt DB and answers with at-worst one-nightly-old (or 2b-fresh) data on a real query, auto-refreshing on HEAD-advance.
- AC10(c): N concurrent comp-kuzu invocations triggering refresh produce no corrupt/half-built DB (mutex + atomic swap demonstrated; readers always see a complete DB).
- Scratch DBs unreachable except via explicit --db.
- Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. Missing rows = REWORK.
- RAVC2 evidence to COO+CTO: commit hash(es) + concurrency-demo transcript + post-flip query output.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Platform tooling only; no silver/bronze converters, no S3 data-prefix writes.</no_reprocess_needed></data_reprocess_scope>
