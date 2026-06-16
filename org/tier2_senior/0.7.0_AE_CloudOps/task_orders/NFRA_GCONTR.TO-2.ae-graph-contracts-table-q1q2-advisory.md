<to_id>NFRA_GCONTR.TO-2</to_id>
<project>NFRA_GCONTR</project>
<title>Stand up globgrph.graph_contracts (Nessie main) + Q1/Q2 diff engine + wire Q2 into comp-surface-check (ADVISORY mode)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff 125904Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>HIGH — the long pole. TO-3 (CVO rows) is parallel-once-table-exists; TO-4 (DS surface) reads the rows. This TO unblocks the chain. GO gated on 0.7.0_AE_CloudOps being spawned (globgrph lane owner currently offline — surfaced to MSTR/Andrew).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GCONTR_PRD.md (v0.2) — §3 RATIFIED schema, §4 BMKAUD replay, §5 tool surface, §7 TO-2, §9 RESOLVED policy</ref>
  <ref type="seed">docs/briefs/period-contracts-seed-benchmark-20260615.md (DS~A, 48635a865) — the graph_contracts DDL + worked benchmark contract</ref>
  <ref type="schema-ratify">PRD §3 (CTO-ratified v0.1): versioning is via Nessie commits (NO `version` column — the commit graph IS the version history; `ratified_at` pins the authorizing commit); ADD `active BOOLEAN DEFAULT true` (audit-preserving retire, mirrors suppression_v1.yaml `active`).</ref>
</references>

<scope>
Stand up the value-layer never-widen machinery: the contract table + the two-query diff engine + the advisory comp-surface-check wiring. THREE limbs, one declaration (PRD §3).

**1. Create `globgrph.graph_contracts` on Nessie main** (Iceberg, co-located beside graph_nodes_*/graph_edges_*), per the RATIFIED §3 schema EXACTLY — incl. CTO amendments: NO `version` column (Nessie commit graph = version history; `ratified_at` pins the authorizing commit) + ADD `active BOOLEAN DEFAULT true`. Deploy via **Terraform / `.tools/safe-apply.sh`** per the globgrph deploy path — NEVER bare `terraform apply` (Rule 18 / safe-apply HALTGT checkpoint). The table starts EMPTY; CVO (TO-3) authors the rows.

**2. Q1 (structure — the graph diff):** snapshot-diff `graph_edges` -> the WRITES edges into a contracted artifact (a `comp-aws diff` extension or globgrph diff sub-command). `+smartx -> json/benchmarks` is a structural delta. Read-only.

**3. Q2 (policy — the contract JOIN):** JOIN the Q1 delta against `graph_contracts` -> a writer NOT in `canonical_writer` (or present in `forbidden_writers`) with NO accompanying ratified contract edit (same window) = **UNSANCTIONED**. A SANCTIONED change = the contract was edited + ratified in the same window (the recorded never-widen sign-off).

**4. Wire Q2 into `comp-surface-check` in ADVISORY MODE (§9 ramp — HARD CONSTRAINT):** a SEV1 contracted-surface commit runs Q1+Q2, and an UNSANCTIONED result **WARNS (advisory) — it MUST NOT exit 2** in this TO. This mirrors the comp-manifest-check D6 advisory ramp. The hard-block flip (exit 2 + audited SURFACE_ACK override) is a LATER one-line CTO ramp-flip gated on low-FP evidence once the SEV1 contracts are authored + tuned. **Do NOT ship hard-block on day 1** — that is explicitly out of scope and would create day-1 false-positive friction before TO-3's contracts exist. The existing comp-surface-check file-gate behavior must be NON-REGRESSED (Q1/Q2 are additive).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write/deploy">
    <step>
      <run>comp-kuzu "CALL show_tables() RETURN *" (or the Nessie/Iceberg table-list on globgrph main)</run>
      <expect>graph_nodes_* + graph_edges_* present; graph_contracts is NET-NEW (no existing table of that name) — confirms no collision beside the existing warehouse tables (PRD §6).</expect>
      <if_mismatch>STOP. If graph_contracts already exists, surface to COO+CTO before any CREATE (would indicate a prior partial stand-up; reconcile first).</if_mismatch>
    </step>
    <step>
      <run>comp-iam service [the diff/Q1-Q2 lambda or the comp-surface-check runtime principal]</run>
      <expect>The principal that runs Q1 (graph_edges snapshot read) + Q2 (graph_contracts read) has the needed Nessie/Iceberg read perms. Enumerate any missing perm BEFORE deploy.</expect>
      <if_mismatch>STOP. Add the missing perm to iam.tf first; then comp-iam gaps at Phase 2.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit/deploy">
    <step>
      <run>comp-iam gaps (only if iam.tf changed) + terraform plan via .tools/safe-apply.sh (0-diff after the table-create apply)</run>
      <expect>0 new IAM gaps; safe-apply plan = the table-create only, 0 unrelated drift; HALTGT checkpoint clears.</expect>
      <if_mismatch>STOP. Resolve gaps / unexpected plan diff before apply. NEVER bare terraform apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>comp-surface-check selfcheck — synthetic BMKAUD T1 replay: a fake `+smartx -> json/benchmarks` WRITES edge with NO ratified graph_contracts edit, run against a SEV1 contracted surface</run>
      <expect>Q1 surfaces the +smartx delta; Q2 marks it UNSANCTIONED and WARNS (advisory) — exit 0, NOT exit 2 (advisory ramp). The existing file-gate path still behaves identically (non-regressed).</expect>
      <if_mismatch>If Q2 exits 2: the advisory ramp is mis-wired — fix to warn-only before RAVC. If Q2 does NOT flag the synthetic UNSANCTIONED: the JOIN is broken — fix. If the existing file-gate regressed: revert the wiring.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **graph_contracts table (THE shared foundation):** created here, WRITTEN by CVO (TO-3 rows), READ by DS (TO-4 pipescript --contract/--flipped). Before finalizing the Q2 JOIN column semantics, MCP CVO (TO-3) to converge on the exact schema field usage (canonical_writer / forbidden_writers / ratified_by / period_defs) so CVO's rows and your JOIN agree. The table schema is RATIFIED (§3) — converge on USAGE, do not re-design the schema.
- **comp-surface-check (shared tool):** you ADD Q1+Q2 (advisory). The existing SEV1 file-gate (the D8 critical-surface gate) MUST be non-regressed — it runs on every safe-commit. Coordinate any structural change to comp-surface-check with CTO (tool owner of the surface-check gate).
- **TO-3 dependency:** TO-3's benchmark row + this TO's Q2 wiring together = the BMKAUD-catch end-to-end (joint acceptance). TO-3 cannot author rows until this table exists.
</cross_domain_coordination>

<acceptance_criteria>
- `globgrph.graph_contracts` exists on Nessie main with the RATIFIED §3 schema (incl. `active BOOLEAN`, no `version` column); a contract row edit is an attributable Nessie commit.
- Q1 returns the WRITES-edge snapshot-diff into contracted artifacts; Q2 performs the contract JOIN and classifies SANCTIONED / UNSANCTIONED.
- Q2 is wired into comp-surface-check in ADVISORY mode — synthetic BMKAUD-replay UNSANCTIONED WARNS (exit 0), does NOT hard-block (exit 2). Hard-block flip is explicitly deferred to a later CTO ramp.
- comp-surface-check existing file-gate behavior is NON-REGRESSED.
- Session log Compiler Tools section reproduces every `<run>` above with observed output + explicit pass/fail vs `<expect>`. Missing rows = REWORK.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>New governance table + read-only diff queries (Q1/Q2) + an advisory (warn-only) gate wiring. No silver/bronze script change; no served-output movement; no consumer reads changed data paths. The table starts empty and is populated by TO-3.</no_reprocess_needed></data_reprocess_scope>
