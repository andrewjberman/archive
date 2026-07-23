<task_order>
<to_id>NFRA_MSBEFF.R4R6</to_id>
<title>TRIGGERS + HYGIENE — (R4) bind the unrun record/deploy tools to the moments their answer matters; (R6) reconcile the ~46 phantom tool names still cited in docs/HUD after retirement</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<!-- RE-TARGETED 2026-07-23 from base 0.8.0 to the ~B tilde lane (Andrew spawned 4 build tildes to
     parallelize the R-series). The batch-GO to base covered R1R3->R5->R2->R4R6 serially; R4R6 now
     moves to a dedicated lane so base keeps only R5 + owns the shared registration surface. The
     batch-GO assignment of R4R6 to base is SUPERSEDED. -->
<date>2026-07-23</date>
<status>pending</status>
<priority>R4 = P2 (widest behavioral gap by stakes) · R6 = P3 (cheap hygiene, same batch)</priority>

<authority>
Andrew-direct 2026-07-23 (verbatim in NFRA_MSBEFF.R1R3 authority block). No standard-change gate:
R4 is trigger wiring under TRIGGER_LAYER doctrine (docs/doctrine/TRIGGER_LAYER.md, ~Z-owned); R6 is
record reconciliation. ~Z holds the doctrine; 0.8.0 builds.
</authority>

<evidence_base>
R4 — the trigger gap, measured (CASE_STUDY_1_MDPF_ARC.md): comp-state ran ZERO times in the entire
telemetry era while MDPF RF-15's registry drift sat undetected (comp-state is the BM25 drift linter
built for exactly that) · dump_enriched_templates.py "exists, gate-clean, never run" across FOUR
MONTHS of an empty vendor column (RF-14) · agent-verbatim: "No tool detected the deploy gap
automatically pre-run. Today's PROD bd-gold-trigger fired against 4 stale S3 scripts." The doctrine
line: an instrument that is available but never fires is halfway to no instrument.
R6 — Phase-0 measurement: the compiler log references 129 distinct comp-* names; only 83 exist. ~46
phantoms, including RETIRED-but-still-cited tools: coverage-map (39 refs), learns-backlog (22),
tool-hud (18), tool-universe, debris-ext, surface. Record-vs-reality drift inside the instrument layer.
</evidence_base>

<scope>
R4 — TRIGGER WIRING (move tools from "available" to "fires at a moment of work"):
  A. comp-state on a PROJECT-CLOSEOUT / SUPERSESSION trigger — when a project JSON flips status or a
     REGISTRY row moves, the drift sweep fires automatically and its output goes to the closing agent.
  B. comp-pipescript deployed on a DEPLOY-COMPLETION trigger — a deploy that lands without the
     deployed-check having run surfaces LOUD (the bd-gold-trigger-vs-4-stale-scripts class).
  Design rule (TRIGGER_LAYER): the trigger's output must land as an OWNED item or a gate result, never
  a log line nobody reads. Prefer the existing hook surface; do not invent a new scheduler.
  SCOPE FLOOR: two triggers, exercised. Do NOT fan out to every tool — an over-triggered estate trains
  agents to skim, which is the BL-1 death in a new costume.

R6 — PHANTOM-NAME RECONCILIATION:
  C. Sweep docs/ + the HUD + prompts + skills for references to retired/nonexistent comp-* names;
     each hit either repoints to the live successor or is deleted with the retirement cited.
  D. Add a RETIRED-ALIAS check to comp-manifest-check: a doc/HUD reference to a name that is neither
     registered nor a declared alias FAILS the completeness gate (this is the same registration
     invariant as R1R3 condition (a), pointed at the docs surface).
  Note: the phantom list from Phase 0 is a STARTING POINT, not the denominator — derive the live set
  yourself from the registry vs the reference surfaces, and print it.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>R4: enumerate the existing hook/trigger surfaces (PostToolUse/PreToolUse, the closeout path, deploy path) — reuse, do not invent. R6: derive the live phantom set (registry vs docs/HUD/prompts references).</run>
    <expect>Both denominators printed: N trigger surfaces available; M references scanned / K phantoms found.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>R4 MUTANT: stage a project-close with an INJECTED registry drift — the trigger must fire and surface it. Stage a deploy with a stale script — the deployed-check must surface LOUD. R6 MUTANT: add a reference to a fake retired name; the alias check must FAIL the gate.</run>
    <expect>All three mutants on the record. A trigger that has never been observed firing has not been built.</expect>
    <!-- ISOLATION MANDATE (added 2026-07-23 by 1.0.0_SA_CTO~Z after the shared-worktree incident — MY
         dispatch gap: the R4 closeout-trigger mutant stages a project-JSON status flip + a REGISTRY row
         move, which live IN THE SHARED MAIN TREE, and the deploy mutant touches deploy state; running
         these in the shared tree churns CLOUD<->scratch and STRANDS other agents' commits, the
         portal-main-stays-on-DEV class). MANDATE: run EVERY R4/R6 mutant fixture in an ISOLATED worktree
         (`git worktree add ../ajb-r4-mutant <scratch-branch>`), NEVER by switching the shared main tree
         off CLOUD. The shared tree stays on CLOUD at all times. No rebase, no force; do not delete a
         scratch branch that anchors a preservation tag. This is a GENERAL rule for any mutant that
         manipulates real tree/branch/close-path state — the fixture isolates, the shared tree never
         moves. -->
    <step><run>ISOLATION: run the above mutant fixtures ONLY in an isolated `git worktree add` — NEVER by switching the shared main tree off CLOUD (the closeout mutant touches the project-JSON/REGISTRY close path in the shared tree; the deploy mutant touches deploy state).</run>
    <expect>Evidence that mutants ran in an isolated worktree; the shared main tree remained on CLOUD throughout (state it explicitly).</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Report the live trigger firings (or their absence) over the first real closeout/deploy after landing.</run>
    <expect>An observed real firing, or an explicit statement that none has occurred yet with the watch left armed.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
R4's closeout trigger touches the project-closure path (org/projects/*.json + REGISTRY.md) used by all
execs — additive observation only, must never block or alter a closure. R6's alias check shares
comp-manifest-check with R1R3's registration invariant — land them coherently (one gate, two checks).
No main-fabric coupling.
</cross_domain_coordination>

<acceptance_criteria>
1. Two triggers live (closeout->comp-state, deploy->pipescript-deployed), each mutant-proven firing.
2. Trigger output lands as an owned/gate result per TRIGGER_LAYER, not a log line (state where it lands).
3. Phantom set derived live with denominator printed; every hit repointed or deleted-with-citation.
4. Retired-alias check live in comp-manifest-check, mutant-proven (fake retired name FAILS).
5. No blocking side effects on the closure or deploy paths (state how verified).
6. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z. Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
