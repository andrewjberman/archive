# OPAL_ANALYST.W0 — Model Portfolios first-run atom_decomp (method + vertical validation)

<task_order>
<id>OPAL_ANALYST.W0</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>3.0.0_SA_CVO~Z</issued_to>
<date>2026-08-11</date>
<status>pending</status>
<priority>P1</priority>
<!-- THIS TO DOCUMENTS AND BINDS A RUN THAT IS ALREADY IN FLIGHT. IT DOES NOT GATE IT.
     Andrew ordered this run at CVO~Z directly and by name; holding it for a TO would have been
     gate-manufacture on a sovereign instruction (CLAUDE.md no-inferred-gates). Start word sent
     20260811T163757Z; run observed at runs/portal-page-portfolios/20260811T1640Z/. The TO's job
     is to mint the proof-of-spec criterion ids (PRD §9.8) -- fill the instance from the work you
     will already have done. If a criterion below is genuinely wrong for the run you are
     executing, SAY SO and I will amend the TO; do not bend the run to a criterion I minted
     without seeing your rectangle. -->

<references>
  <ref type="charter">org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/ANDREW_DIRECT_20260811_OPAL_ANALYST_ATOMDECOMP_PROGRAM.md — Andrew-direct ~1020Z, VERBATIM: *"for the first run only on 'Model Portfolios' i want CVO~Z to run atom_decomp on that so that we validate every little thing"*</ref>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 (v1.3 @f57c2a1642) — §9.0, §9.2 W0, §9.3 semantics delegation, §9.4 certification exception, §9.4.1 DRY-is-not-done</ref>
  <ref type="ruling">MSTR~Z 20260811T163158Z — Rule 14(e) author/certifier collision resolved: CTO~Z signs this run's certification, W0 only</ref>
  <ref type="method">projects/ATOM_DECOMP/skill/atomic-decomposition/SKILL.md Rules 1-14</ref>
  <ref type="prior-art">org/tier0_utility/0.0.3_BG_BBGTerminal/refs/census/ARTIFACT_CENSUS_MP.yaml @0c1dae3da (16 items) · the 16 published specimen sheets, manifest @bad98cbb6</ref>
</references>

<scope>
`/portfolios` — the Model Portfolios vertical, at page grain. Run home
`workflows/atom_decomposition/runs/portal-page-portfolios/<stamp>/`.

**THIS RUN CARRIES TWO OBJECTS, and the second is the reason Andrew put it first:**
1. **The MP vertical** — every little thing validated, in his words.
2. **THE METHOD ITSELF.** 0.5.0_AE_OpalETL~Z runs atom_decomp **fifteen more times** after you,
   across the rest of the Portal. Every method defect you surface here is one they do not hit
   blind. **A method read is a first-class deliverable of W0, not a courtesy** — where the method
   was awkward, ambiguous, or silent on a real question a Portal page raises.

**You author; 1.0.0_SA_CTO~Z certifies — W0 ONLY** (§9.4). **Plant the coherence-violating mutant;
do not tell me where it is.** If I miss it the pass is void, which is the entire point of it.
Steady state from W1 reverts to the method's normal shape: 0.5.0 authors, CVO~Z certifies.
</scope>

<requirements>
  <requirement id="1">**Full Rule-14 run:** rectangle from the declared schema, cells born UNMEASURED; **domain bar stated BEFORE measurement**; status-missioned fan-out merged only through the validator; **iterate UNTIL DRY (consecutive zero-change rounds, never a count target)**; certification per requirement 3; no unmeasured cell cited as fact.</requirement>
  <requirement id="2">**Rule 3 separation** — declared / deployed / invoked / artifact-producing / SERVING kept distinct per artifact. PRD §9.1.2 records that the whole page denominator is DESIRED-class (source-only); this run is the first to convert any of it to measured.</requirement>
  <requirement id="3">**`certification.json` signed by 1.0.0_SA_CTO~Z**, with the planted mutant, the coherence verdict NAMING ITS DISCRIMINATOR, mechanical constraint checks, and targeted re-derivation on action-blocking cells. **DRY is not done (§9.4.1): 0 of 3 precedent runs in this estate were ever certified** — this run is where that stops. Ping me at rectangle-final and I will certify same-turn; I am not letting the certifier be the bottleneck on a critical path I own.</requirement>
  <requirement id="4">**Semantics, on your delegated authority** (§9.3, Andrew: *"CVO~Z validates and provides the relevant semantics that I would have done, I think it's fairly obvious what they'd be"*) — the 6-question block per artifact (Q1 canonical name / Q2 business meaning / Q3 vintage semantics / Q4 Analyst serve-deny / Q5 disposition / Q6 notes), carrying your signature and date. **Andrew's own recorded verbatim semantics, where they exist, outrank a delegated one and are marked as his.** The 16 MP specimen sheets are live and re-emittable to the same URLs (0.5.0 owns the generator); the notation cycle has been blocked at Andrew since 08-10 ~2210Z and your pass is what unblocks it.</requirement>
  <requirement id="5">**Census as INPUT, never as evidence a run happened** (§9.0). `ARTIFACT_CENSUS_MP.yaml` (16 items = 7 rendered + 9 unrendered) is good material that lowers your cost. Where run and census disagree, the run wins and the disagreement is NAMED.</requirement>
  <requirement id="6">**`run.json`** validates against `ssot_establishment.schema.json#/$defs/run_manifest`, carrying the per-cycle hole census and the method vintage.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for searches; `comp-estate` for the MDPF/platinum backend feeding the page.</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`; `comp-routes behaviors` for serving-path claims.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8,C9,C10   # POSITIONAL (argv[2]) -- NOT a --expected-criteria flag; the flag form exits 2 into help text carrying no "INVALID" string`</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **1.0.0_SA_CTO~Z** — certifier for this run (W0 only) + PRD owner. Method findings route to me and I fold them into the PRD before W1's runs begin.
- **0.5.0_AE_OpalETL~Z** — holds W1 (staged) and owns the MP specimen-sheet generator. **W1's runs wait on your certification landing**; their prep is unblocked and running. If W0 will slip materially, tell me — six pages of prep are sitting behind it.
- **2.0.0_SA_COO~Z** — scoped /drive @10m over this program; keep your broker summary accurate.
- **Shared checkout (site Z):** commit to your own lane, do NOT push (MSTR~Z integrates :55-:00); scratchpad or serial+timestamp msgfile names, never a generic `/tmp` name.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">**Enumeration with denominator** — every route, panel, fetch and served artifact on `/portfolios` enumerated first-hand, each count stated WITH what it is a count OF.</criterion>
  <criterion id="C2">**Rectangle born UNMEASURED and schema-valid**, entity-by-field, cells carrying {value, status, evidence}.</criterion>
  <criterion id="C3">**Domain bar stated BEFORE measurement**, verifiably so (committed/timestamped ahead of the measurements), not asserted after.</criterion>
  <criterion id="C4">**DRY reached by convergence** — consecutive zero-status-change rounds evidenced in `run.json` cycles, never a count target.</criterion>
  <criterion id="C5">**Declared / deployed / serving separated** per artifact, the SERVED limb grounded on a live read or exercised path.</criterion>
  <criterion id="C6">**Census reconciliation stated** — MP census ingested as input, every run-vs-census disagreement NAMED with the run's evidence (zero disagreements is valid and is stated explicitly).</criterion>
  <criterion id="C7">**`run.json` schema-valid** with per-cycle hole census + method vintage.</criterion>
  <criterion id="C8">**`certification.json` signed by 1.0.0_SA_CTO~Z**, verdict NAMING ITS DISCRIMINATOR, planted mutant recorded and its detection recorded. A pass in which the mutant was not caught is VOID and is reported as void.</criterion>
  <criterion id="C9">**Semantics landed** on the 6-question block for every servable MP artifact, signed and dated by CVO~Z, in a form W5 can lift into `DATA_CATALOG` v0.2 without re-interpretation.</criterion>
  <criterion id="C10">**METHOD READ delivered** — a named, specific account of where atom_decomp was awkward, ambiguous, or silent on a real question `/portfolios` raised, plus any recommended amendment. **"The method worked fine" is an acceptable finding ONLY if stated as a measured verdict with what you probed** — a blank method read fails this criterion, because 15 runs are about to be executed on the strength of it.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9,C10</expected_criteria>
  <instance_path>org/tier1_exec/3.0.0_SA_CVO/deliverables/OPAL_ANALYST.W0_PROOF_OF_SPEC.json</instance_path>
  <!-- Minted at decomposition by the issuer (PRD §9.8); fill from your own efforts, one row per
       id, criterion VERBATIM + re-runnable invocation + output evidence + denominator. No bare
       values. Validate before any status flip. You built the coverage layer this validator runs
       -- C8's mutant is the strongest control in the set; record it as one. -->
</proof_of_spec>

<deliverables>
  <deliverable type="commit">`workflows/atom_decomposition/runs/portal-page-portfolios/<stamp>/` — `run.json`, `rectangle.c0.json`, `patches/`, `rectangle.final.json`, `certification.json`</deliverable>
  <deliverable type="document">MP semantics, 6-question block per artifact, signed + dated</deliverable>
  <deliverable type="document">**Method read** (C10) — routes to CTO~Z, folded into the PRD before W1 runs begin</deliverable>
  <deliverable type="document">`OPAL_ANALYST.W0_PROOF_OF_SPEC.json`, validator-clean against C1-C10</deliverable>
  <deliverable type="document">Session log with Compiler Tools section</deliverable>
</deliverables>

<do_not>
  <rule>**Do NOT build any alert, alarm, SNS topic, SES send, freshness checker or `*-monitor`** (standing moratorium).</rule>
  <rule>**Do NOT create approval gates or holds on other seats** (no-inferred-gates law).</rule>
  <rule>**Do NOT delete or relocate any served or served-adjacent artifact** — residue gets a disposition, never an act (NEVER#3).</rule>
  <rule>**Do NOT stand up a shadow path or standing comparator** to validate a finding (no-shadow veto).</rule>
  <rule>**Do NOT sign your own certification** — CTO~Z signs this one (§9.4), and this exception is W0-scoped.</rule>
  <rule>**Do NOT reveal the mutant's location** before certification.</rule>
  <rule>**Do NOT push.**</rule>
</do_not>
</task_order>
