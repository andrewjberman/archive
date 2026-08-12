# NFRA_TOOLCHECK.P4-AD1 — atom_decomp the comp-* VERDICT tools (instruments program, run 1)

<task_order>
<id>NFRA_TOOLCHECK.P4-AD1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~Z</issued_to>
<date>2026-08-11</date>
<status>complete</status>
<!-- COMPLETE 2026-08-11 ~2030Z by 0.8.0_AE_CloudComp~Z. Run comp-verdict-tools__20260811T1931Z
     CERTIFIED PASS @2c0946081a (CVO~Z; mutant caught by necessary inequality; all exercises
     reproduced). Proof-of-spec validated rc=0 VALID (positional form, rc-checked) BEFORE this flip.
     Closure @90dc1930b8. C1-C8 all PASS with evidence in the instance. -->
<priority>P1</priority>
<!-- SEQUENCING: begins at W1-COMPLETE (OPAL_ANALYST pages 5-6 certifying now). Read-in starts
     immediately; the first measurement waits for my release word. Andrew's authorization chain:
     GO ~1740Z -> gated + comp-tooling-confined ~1817Z -> integration RATIFIED ~1905Z
     (@7ea4fdbd38). This TO runs INSIDE NFRA_TOOLCHECK P4's registered scope -- deliberately NOT a
     new project/PRD (Build Ladder rung 2; the estate already registered this program). -->

<references>
  <ref type="authority">org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260811_INSTRUMENTS_DECOMP_PROGRAM_GO.md (verbatims + gate discharge + sequencing)</ref>
  <ref type="boundary">the ratified FABRIC_ONTOLOGY_INTEGRATION doc @7ea4fdbd38 — COMP TOOLING ONLY; the supervision/broker cluster needs Andrew's word and is OUT of this TO</ref>
  <ref type="method">projects/ATOM_DECOMP/skill/atomic-decomposition/SKILL.md Rules 1-14 · ssot_establishment.schema.json @22ce467d37 (relations/structural_changes/notes)</ref>
  <ref type="method-law">docs/architecture/OPAL_ANALYST_PRD.md §9.8.1 classes A-L + K/K.1/K.2 — READ BEFORE FIRST MEASUREMENT; these were paid for today</ref>
  <ref type="worked-examples">workflows/atom_decomposition/runs/portal-page-portfolios/20260811T1640Z/ (incl. certification.attempt1.VOID.json — read the failure too) · runs/portal-page-cma/ (both runs; the supersession)</ref>
  <ref type="prior-findings">CLAUDE.md's own documented instrument defects (comp-validate NO_CONFIG; to-check default-view blindness; comp-find line-vs-node grain) — PRIOR CLAIMS TO VERIFY, not facts to inherit</ref>
</references>

<scope>
**ONE atom_decomp run. Subject: `comp-verdict-tools`. Run home:
`workflows/atom_decomposition/runs/comp-verdict-tools/<stamp>/`.**

**Entities — the three comp-* VERDICT instruments** (tools whose OUTPUT is a verdict another seat
acts on): `comp-validate` · `proof-of-spec-check.py` · `comp-find` (its DENOMINATOR/BAND verdict
surface, not its search function). Each entity is one instrument.

**You declare the axis fresh** (Rule 24: one intent, one grain, stated in `axis_declaration.json`
with the domain bar BEFORE any measurement). Guidance, not prescription: the field set that made the
Portal runs work was artifact-shaped; an instrument-shaped set will differ — what the tool CLAIMS to
answer, its verdict vocabulary, its false-verdict modes (can it say PASS when the truth is FAIL —
and can it say anything when it could not measure?), its documented-vs-exercised blind spots, who
ACTS on its output, disposition. **The known CLAUDE.md defect claims are PRIOR CLAIMS your run
verifies or refutes at source — inheriting them unverified is the census-as-evidence class (§9.0).**

**BOUNDARY, hard:** comp tooling only. If decomposing a verdict tool leads you to a broker/
supervision/liveness surface, that edge is a NAMED BOUNDARY per Rule 7 — recorded, not crossed.
</scope>

<requirements>
  <requirement id="1">Full Rule-14 run under the §9.8.1 regime: axis + domain bar committed BEFORE measurement; cells born UNMEASURED; every merge through ssot_validate; DRY by convergence under DIFFERENT lenses (binding C); evidence as {instrument, locator, vintage} triples — never prose (the declined-relaxation rule).</requirement>
  <requirement id="2">**Verdict tools are exercised, never only read** (Rule 22a): every false-verdict-mode claim carries a run that PRODUCED the false verdict (e.g. comp-validate on a script with no config; proof-of-spec-check's flag-form rc=2 vocabulary hazard; comp-find's line-vs-node grain on a measured corpus). A blind spot asserted from documentation is INFERRED, not MEASURED.</requirement>
  <requirement id="3">**K/K.1/K.2 regime in full:** consumable derives from dry (never final); verifier packet = c0 + pre-dry patches + final + run.json + constraints + seal; plant sealed at plant time in MUTANT_SEALED.md, coordinates never in-object; CVO~Z certifies with the reconstruction attestation.</requirement>
  <requirement id="4">**METHOD READ, C10-grade, fresh-eyes:** you are the first author onboarding to this method after its hardening — where the §9.8.1 bindings were ambiguous, silent, or wrong FOR AN INSTRUMENT SUBJECT (they were written on a page subject) is a first-class deliverable. "It worked fine" passes only as a measured verdict naming what you probed.</requirement>
  <requirement id="5">**Findings land as findings** — no fixes to the tools in this TO, no deletion, no retirement recommendation without Rule-9's full ladder, and NOTHING notification-shaped (moratorium). Surprise channel: one line to me, no action, keep working.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>Read-ins per references. `comp-which` for searches; the tools under test are ALSO your instruments — when you must use one to study another, say so in the cell's evidence (an instrument measuring itself is a named limitation, not a disqualification).</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`; all rc values captured as the next statement (binding I).</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8   # POSITIONAL argv[2]; CHECK THE RC — the help banner contains both verdict words</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — certifier (normal shape: you author, they certify) + the instance registers. Hand off at DRY; do not batch behind other work.
- **1.0.0_SA_CTO~Z** — program owner; release word for first measurement; method findings route to me.
- **0.5.0_AE_OpalETL~Z** — owns the W1 emitter (`w1_emit.py` pattern); reuse their conforming-emitter approach rather than re-deriving it (Build Ladder rung 2). Ask them, not me, for its mechanics.
- **Shared checkout:** commit to your own lane, never push (MSTR~Z integrates); scratchpad or serial+timestamp msgfiles.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bar committed verifiably BEFORE first measurement (timestamp precedence checkable).</criterion>
  <criterion id="C2">Rectangle schema-valid, cells born UNMEASURED, evidence triples throughout; denominators printed with every count.</criterion>
  <criterion id="C3">Every false-verdict-mode claim EXERCISED — the run that produced the false verdict cited per cell; prior CLAUDE.md defect claims each verified/refuted at source, disagreements NAMED.</criterion>
  <criterion id="C4">DRY by convergence under at least two distinct lenses, evidenced in run.json cycles.</criterion>
  <criterion id="C5">`certification.json` signed by CVO~Z with the K.2 reconstruction attestation; planted mutant caught or the attempt VOIDed and retained (attempts accumulate).</criterion>
  <criterion id="C6">Consumable `rectangle.final.certified.json` derived from dry per binding K; K.1 packet composition used and stated in the handoff.</criterion>
  <criterion id="C7">METHOD READ delivered at the C10 bar (fresh-eyes, instrument-subject deltas named).</criterion>
  <criterion id="C8">Session log with populated Compiler Tools section; declared exclusions + surprises per the standing schema.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TOOLCHECK.P4-AD1_PROOF_OF_SPEC.json</instance_path>
  <!-- Issuer-minted per the 08-11 canonization. Fill from your own efforts; validate BEFORE the
       complete flip. C3 is the criterion this TO exists for: an instrument's false-verdict mode,
       exercised, is the whole reason Andrew ordered instruments decomposed. -->
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package at `runs/comp-verdict-tools/<stamp>/` — full K/K.1/K.2 artifact set</deliverable>
  <deliverable type="document">METHOD READ (C7)</deliverable>
  <deliverable type="document">`NFRA_TOOLCHECK.P4-AD1_PROOF_OF_SPEC.json`, validator-clean</deliverable>
  <deliverable type="document">Session log</deliverable>
</deliverables>

<do_not>
  <rule>**Do NOT cross the ratified boundary** — supervision/broker/liveness surfaces are named boundaries, never entities. Andrew's word widens it; nothing else does.</rule>
  <rule>**Do NOT build monitors/alerts/notifications** (moratorium) — a finding lands as a finding.</rule>
  <rule>**Do NOT fix, delete, or retire any tool in this TO** (Rule 9; findings-only).</rule>
  <rule>**Do NOT inherit CLAUDE.md's defect claims as facts** — verify at source or mark INFERRED.</rule>
  <rule>**Do NOT start measurement before my release word** (W1-complete trigger). Read-in now.</rule>
  <rule>**Do NOT push.**</rule>
</do_not>
</task_order>
