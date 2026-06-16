<to_id>NFRA_GCONTR.TO-4</to_id>
<project>NFRA_GCONTR</project>
<title>pipescript --contract / --flipped surface over graph_contracts (false-clean: uncontracted = LOUD-unreviewed)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff 125904Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>MEDIUM — the surface, last in the build order. GO gated on TO-3 (rows must exist to read). DS owns the pipescript CLI (owned-paths grant 0096b5cbb) so this is same-tool, DS-lane (no cross-tool owner-review).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GCONTR_PRD.md (v0.2) — §3 schema, §5 tool surface (the --contract/--flipped spec), §7 TO-4, §8 acceptance 3+4</ref>
  <ref type="tool-owner">NFRA_PIPESCRIPT (CLOSED 2026-06-15, ead69f1e5) — pipescript CLI canonical; DS owns pipescript_cli.py per owned-paths grant 0096b5cbb. This TO extends that CLI.</ref>
  <ref type="false-clean-doctrine">The reachability/false-clean discipline from NFRA_PIPESCRIPT P3.2 (loud-unreviewed surfacing) — applied here to the VALUE layer: an uncontracted surface is never silently "fine".</ref>
</references>

<scope>
Add the value-layer read surface to pipescript, reading the new `globgrph.graph_contracts` table (TO-2 creates, TO-3 populates). Two flags:

**1. `pipescript --contract <thread>`:** read graph_contracts for the thread/surface and display the DECLARED contract — canonical_writer, period_defs, ratified_by, ratified_at — alongside any OBSERVED writer drift (a writer on the WRITES edges not equal to canonical_writer / present in forbidden_writers). This is the "what does the contract say + does reality match" view.

**2. `pipescript --flipped --since <snapshot>`:** for each window/period flip since the snapshot, TAG it:
   - **SANCTIONED** — the flip was accompanied by a ratified graph_contracts edit in the same window.
   - **UNSANCTIONED** — a flip with NO ratified contract edit (exit 2 in the CLI surface — this is the CLI's own non-advisory signal; distinct from comp-surface-check's v1-advisory gate).
   - **uncontracted = LOUD-unreviewed** — the surface has NO contract row at all -> surfaced LOUD as `unreviewed`, NEVER silently clean (the false-clean discipline on the value layer; PRD §8 AC4).

**Constraint:** do NOT regress the existing pipescript named-thread traversal (the gate-b 25-thread census). --contract/--flipped are ADDITIVE.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>pipescript --list (and a sample pipescript &lt;name&gt; on an existing named thread)</run>
      <expect>The existing 25 named-thread traversal works as the baseline (the gate-b set). Record it as the pre-change reference so --contract/--flipped additions can be proven non-regressive.</expect>
      <if_mismatch>If the baseline traversal is already broken, STOP and surface to COO before adding new flags onto a broken base.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh pipescript_cli.py (py_compile + ds-precommit-check + ruff py39, pin 0.15.11)</run>
      <expect>Exit 0 — the new flags pass the universal edit gate.</expect>
      <if_mismatch>Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>pipescript --gate-b (the 25-thread golden-fixture traversal regression)</run>
      <expect>25/25 still pass — the existing traversal is NON-REGRESSED by the --contract/--flipped additions.</expect>
      <if_mismatch>STOP. A gate-b regression means the new flags perturbed the shared traversal — fix before RAVC.</if_mismatch>
    </step>
    <step>
      <run>pipescript --contract model_portfolios.benchmark + pipescript --flipped --since &lt;a known BMKAUD-window snapshot&gt;</run>
      <expect>--contract returns the declared canonical_writer (yang-pipeline) / period_defs (1M=trailing) / ratified_by + observed drift; --flipped tags the BMKAUD window UNSANCTIONED (or uncontracted-LOUD if TO-3's benchmark row isn't authored yet). An uncontracted SEV1 surface reads LOUD `unreviewed`.</expect>
      <if_mismatch>If --contract returns nothing for a contracted surface, the table read is broken. If --flipped silently clean on an uncontracted surface, the false-clean discipline is violated — fix.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-3 (CVO) dependency — HARD:** --contract/--flipped READ the graph_contracts rows CVO authors. GO gated on TO-3 rows existing (at least the SEV1 benchmark row, for a meaningful Phase-3 demo). Until rows exist, every surface reads uncontracted-LOUD — which is itself a valid (and the default) state to render.
- **TO-2 (AE) dependency:** the table must exist (TO-2) — transitively satisfied via TO-3.
- **pipescript CLI is DS-owned** (owned-paths 0096b5cbb) — same-tool lane, no cross-tool owner-review needed (per the RV-0033/0034 convention: same-tool DS-inclusive lane granted at decomposition time). Commit directly.
</cross_domain_coordination>

<acceptance_criteria>
- `pipescript --contract model_portfolios.benchmark` returns the declared canonical_writer / period_defs / ratified_by + any observed writer drift (PRD §8 AC3).
- `pipescript --flipped --since <snap>` tags each flip SANCTIONED / UNSANCTIONED / uncontracted-LOUD (PRD §8 AC3).
- An uncontracted SEV1 surface reads LOUD `unreviewed`, never silently "fine" (PRD §8 AC4 — false-clean discipline on the value layer).
- gate-b 25/25 non-regressed (existing named-thread traversal intact).
- Session log Compiler Tools section reproduces every `<run>` above with observed output + explicit pass/fail vs `<expect>`. Missing rows = REWORK.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Read-only CLI surface over the graph_contracts table; no data path, silver/bronze script, or served artifact is touched.</no_reprocess_needed></data_reprocess_scope>
