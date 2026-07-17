<task_order>
<to_id>NFRA_KUZUSPLIT.P0-P1</to_id>
<title>Graph-refresh split — P0 instrument the real morning cost, then P1 split into comp-kuzu-full (MSTR-startup, force full) / comp-kuzu-inc (workers, incremental-OR-serve-labeled-stale, NEVER full)</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<!-- STAFFING RESOLVED (Andrew-direct 2026-07-17 ~20:2xZ via COO): builder lane = 0.8.0~D (new lane, shared
     with NFRA_COMPSIMILAR — same platform domain; base stays Andrew-reserved per LD-0305). MSTR spawn requested. -->
<date>2026-07-17</date>
<status>staged</status>
<priority>P2 (Andrew batch 2026-07-17). GATE CLEARED: Andrew RATIFIED — GO fires on ~D registration.</priority>

<authority>
Andrew-direct verbatim: "full derive as a function of 0.0.0_AB_MSTR startup, but for the remainder of the
session, all agents should just be using incremental update pre comp tool queries... comp-kuzu-full and
comp-kuzu-inc." PRD @ docs/architecture/NFRA_KUZUSPLIT_PRD.md; brief @ docs/briefs/GRAPH_REFRESH_AUDIT_AND_KUZU_SPLIT_20260717.md; LD-0307.
</authority>

<gate>
ANDREW RATIFIED 2026-07-17 ~20:2xZ (via COO AskUserQuestion): O-1 = YES, comp-kuzu-inc = incremental-OR-
serve-labeled-stale, NEVER full (a worker on a large delta serves the complete prior-vintage DB labeled-stale
+ LOUD log; never a 6min mid-task rebuild — the §4 hard gate, now LAW for this build). O-2/O-3/O-4 proceed
per PRD rec (P0-instrument-first; new project not reopen-GLOBGRPH; P4 distribute DEFERRED to the two-machine
wave). GATE CLEARED. COO fires GO on ~D registration (MSTR spawn requested). CTO arch-gates the code as platform owner.
</gate>

<scope>
DON'T-REBUILD-WHAT-EXISTS (D-002 guard): the symmetric local incremental refresh ALREADY EXISTS
(kuzu_incremental_refresh.py, default-on, 92x faster). The gap is SCHEDULING + SURFACING, not existence.
  - P0 INSTRUMENT (gates sizing, Rule 22): name the exact operator "10min" habit being replaced; MEASURE real
    per-box morning cost + fallback rate; confirm the shared-canonical warm benefits peers. No fix sized before this.
  - P1 SPLIT: comp-kuzu-full = force full kuzu_nessie_load unconditionally (MSTR startup); comp-kuzu-inc =
    incremental-or-serve-labeled-stale, NEVER full; bare comp-kuzu unchanged (back-compat). kuzu_cli.py gains a
    mode flag; two thin wrappers set it. AC-P1: -inc on a FORCED large delta serves labeled-stale + logs LOUD +
    does NOT full-rebuild (exercised). P2 (MSTR-startup idempotent hook) + P3 (docs, ships WITH P1) are follow-on
    staged TOs; P4 (distribute) optional per O-4.
</scope>

<compiler_tools_mandate>
  <phase id="0" when="P0 instrument (before any code)">
    <step>
      <run>Measure: time kuzu_nessie_load (full) vs kuzu_incremental_refresh (inc) on a live box morning; capture the nightly-2a large-delta fallback event + its per-box cost</run>
      <expect>Real numbers (not the PRD's ~6min estimate): full cost, inc cost, fallback rate/day. This is the sizing basis; a config-read is NOT a measurement (Rule 22a — exercise the path).</expect>
      <if_mismatch>STOP. If the habit being replaced isn't the assumed one, re-scope with CTO before P1.</if_mismatch>
    </step>
  </phase>
  <phase id="1" when="before commit (P1)">
    <step>
      <run>comp-manifest-check (registration invariant) after adding the two .tools/comp-kuzu-{full,inc} executables</run>
      <expect>Both new executables REGISTERED (tools_index + comp-tools.yaml + graph-call-manifest.yaml) — the invariant blocks a commit leaving them unregistered.</expect>
      <if_mismatch>STOP. Register both before commit; an unregistered comp-tool is an incomplete ship.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
NFRA_COMPSIMILAR (same platform lane): its resource_summaries Kuzu projection must ride THIS refresh model —
build the -inc/-full split first (or co-design) so there is ONE refresh path. MSTR-lane doc edits
(CLAUDE.md comp-* row + XXX.md Step-1b startup hook + MEMORY.md line) ship IN THE SAME WAVE as the code so the
map never leads reality (Art. VI: MSTR governs the docs, does not edit the code; CTO arch-gates; 0.8.0 builds).
alert-suspension: N/A — no alert leg.
</cross_domain_coordination>

<acceptance_criteria>
1. P0: real measured morning cost + fallback rate committed as the sizing basis (exercised, not estimated).
2. P1: comp-kuzu-full forces full; comp-kuzu-inc on a forced large delta SERVES LABELED-STALE + logs LOUD +
   does NOT full-rebuild — exercised with a forced large delta (the §4 hard gate; the whole point).
3. Both executables registered (comp-manifest-check green); docs ship same-wave.
4. Session log reproduces each mandate run + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/NFRA_KUZUSPLIT_PRD.md</ref>
  <ref type="brief">docs/briefs/GRAPH_REFRESH_AUDIT_AND_KUZU_SPLIT_20260717.md</ref>
  <ref type="ledger">org/tier0/ledger/LD-0307.md</ref>
</references>
</task_order>
