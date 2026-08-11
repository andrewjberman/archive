# OPAL_ANALYST.W1 — atom_decomp the six Pod-2 Analysis pages (page grain)

<task_order>
<id>OPAL_ANALYST.W1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-11</date>
<status>staged</status>
<priority>P1</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 (v1.3 @f57c2a1642) — §9.1 denominator, §9.1.2 claim class, §9.2 waves, §9.3 semantics delegation, §9.4.1 DRY-is-not-done, §9.8 TO contract</ref>
  <ref type="charter">org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/ANDREW_DIRECT_20260811_OPAL_ANALYST_ATOMDECOMP_PROGRAM.md (Andrew-direct ~1020Z, verbatim)</ref>
  <ref type="method">projects/ATOM_DECOMP/skill/atomic-decomposition/SKILL.md Rules 1-14 · projects/ATOM_DECOMP/00_ATOMIC_DECOMPOSITION_SPEC.md</ref>
  <ref type="prior-art">org/tier0_utility/0.0.3_BG_BBGTerminal/refs/census/ARTIFACT_CENSUS_POD2.yaml @49cb88ead (11 keys, 6 pages)</ref>
  <ref type="prior-art">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/PORTAL_PAGE_INVENTORY_20260811.json @2dc3f0b417 (your own; adopted into PRD §9.1.1)</ref>
</references>

<scope>
**Six pages, page grain, one atom_decomp run each:**
`/cma` · `/positioning` · `/attribution` · `/factor-tilts` · `/valuations` · `/correlations`
(the portal nav "Analysis" section minus Macroeconomics — the Pod-2 vertical as your own census
already defines it).

**Run home, one per page:**
`workflows/atom_decomposition/runs/portal-page-{cma|positioning|attribution|factor-tilts|valuations|correlations}/<stamp>/`

**W1 IS SEQUENCED AFTER W0 (CVO~Z's MP first-run) — and that is a real dependency, not a gate
anyone enforces:** W0 validates the method you would otherwise be applying blind across six pages.
**W1 PREP IS UNBLOCKED AND STARTS NOW** — route reads, panel walks, census ingestion, domain-bar
drafting. Begin the runs themselves once W0's certification lands (CTO~Z signs it; you will be
told). If W0 slips materially, say so — do not sit silent, and do not start runs early to fill
the wait.

**WHY THESE SIX FIRST (so the ordering is not mistaken for arbitrary):** they are census-backed.
The method gets exercised where prior art makes a wrong answer cheap to spot, before it meets the
six uncensused pages in W4 where the run is the only source.
</scope>

<requirements>
  <requirement id="1">**Per page, a complete Rule-14 run.** (a) rectangle generated from the declared JSON schema, entity-by-field, every cell born UNMEASURED with {value, status, evidence}; (b) **the DOMAIN BAR stated in the rubric BEFORE any measurement** (expected variance vs finding class) — 14(b), and a bar written after measuring is not a bar; (c) status-missioned fan-out, patches merged only through the validator; (d) **iterate UNTIL DRY — consecutive rounds with zero status changes, NEVER a count target**; (e) certification per requirement 4; (f) no cell cited as fact unless MEASURED.</requirement>

  <requirement id="2">**Rule 3 is the load-bearing one for this program: keep declared / deployed / invoked / artifact-producing / SERVING separate per artifact.** PRD §9.1.2 states the page denominator is DESIRED-class — source-only, no bundle inspection, no rendered page. **Your runs are what convert it to measured.** A route that is declared but not served, or a panel that renders from a key nothing produces, is a FINDING, not a discrepancy to reconcile away.</requirement>

  <requirement id="3">**Ingest the Pod-2 census as INPUT and reconcile against it explicitly.** It is P0 material that lowers your cost; it is NOT evidence any run happened (PRD §9.0). **Where your run disagrees with the census, the run wins and the disagreement is NAMED in the run record** — including the census's own flagged `json/capital-markets/` channel-map gap, whose approved fix rides W5. A silent reconciliation is the substitution this PRD exists to block.</requirement>

  <requirement id="4">**CERTIFICATION IS A DELIVERABLE, NOT A HAND-OFF (PRD §9.4.1, your own finding).** Each page ships `certification.json` **signed by 3.0.0_SA_CVO~Z** — evidence-shape validation, mechanical constraint checks, full-rectangle coherence assessment **whose verdict is VOID unless it names its discriminator**, targeted re-derivation on action-blocking and transcription-risk cells, and **a planted coherence-violating mutant on every verify pass**. You author; **you never sign your own run.** A page that stops at `DRY` is NOT complete and its outputs are not usable downstream — the 0-of-3 precedent you measured is exactly what this requirement exists to stop repeating.</requirement>

  <requirement id="5">**Semantics per artifact, from CVO~Z, on the 6-question block** (Q1 canonical name / Q2 business meaning / Q3 vintage semantics / Q4 Analyst serve-deny / Q5 disposition / Q6 notes). Per PRD §9.3 CVO~Z now holds this pen under Andrew's delegation. **You do not write semantics for artifacts you decomposed** — that split is the point. Land them so W5 can lift them into `DATA_CATALOG` v0.2 rows without re-interpretation.</requirement>

  <requirement id="6">**`run.json` validates against `ssot_establishment.schema.json#/$defs/run_manifest`** and carries the per-cycle hole census (`MEASURED / UNMEASURED / INFERRED / NOT_MEASURABLE`) plus the **method vintage** (the package commit that ran), so any finding is attributable to the method version that produced it.</requirement>

  <requirement id="7">**Page grain, and no panel grain** (PRD §9.1.1 / Rule 24(ii)): `panels/` is not a uniform sub-page structure (5 of 16 page dirs use it), so a panel-grained axis mixes grains. Panels are entities WITHIN a page's rectangle, never the decomposition axis.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for each search you would otherwise raw-grep. `comp-estate <thread>` per vertical to locate the backend feeding each page before you model it (the Pod-2 census already cites valuation/positioning-adjacent/correlation/factor-tilts/cma threads — start there). `comp-transform schema-check <Component>` for any page component whose data-prop contract you assert.</before_write>
  <before_commit>`.tools/commit-gate.sh` on every `.py` touched. `comp-routes behaviors` for any serving-path claim (this is also how requirement 2's served-state limb gets grounded rather than inferred).</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11   # POSITIONAL (argv[2]) -- NOT a --expected-criteria flag; the flag form exits 2 into help text carrying no "INVALID" string` — must pass BEFORE the status flip.</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — semantics (req 5) + certification signature (req 4). Both are theirs; neither is yours to self-serve. Hand off per page as it reaches DRY rather than batching all six, so certification is not a six-page cliff at the end.
- **1.0.0_SA_CTO~Z** — PRD owner; W0-certification-landed signal comes from me. Method-defect findings route to me.
- **2.0.0_SA_COO~Z** — running a scoped /drive @10m over this program; keep your broker summary accurate so their loop reads you correctly.
- **Shared files:** none expected — run dirs are per-page and new. `ARTIFACT_CENSUS_POD2.yaml` is READ-ONLY to this TO; if a correction is warranted it is a separate act with its own record (the 08-10 sweep lesson).
- **Shared checkout hazard (site Z):** ~6 agents on one tree. Commit to your own lane, do NOT push (MSTR~Z integrates :55-:00). Use scratchpad or serial+timestamp msgfile names, never a generic `/tmp` name.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">**Enumeration with denominator, per page:** every route, panel, fetch and served artifact enumerated first-hand, each count stated WITH what it is a count OF. A retrieval that returns nothing is distinguished from a surface that has nothing.</criterion>
  <criterion id="C2">**Rectangle born UNMEASURED and schema-valid**, per page, entity-by-field, cells carrying {value, status, evidence}.</criterion>
  <criterion id="C3">**Domain bar stated BEFORE measurement**, per page, in the rubric — timestamped/committed such that its precedence over the measurements is verifiable, not merely asserted.</criterion>
  <criterion id="C4">**DRY reached by convergence:** consecutive rounds with zero status changes, evidenced in `run.json` cycles. A run that stopped at a count target fails this criterion.</criterion>
  <criterion id="C5">**Declared / deployed / serving separated** for every artifact (Rule 3), with the SERVED limb grounded on a live read or an exercised path — never on the route table alone. Converts PRD §9.1.2's DESIRED-class denominator to measured for these six pages.</criterion>
  <criterion id="C6">**Census reconciliation stated:** Pod-2 census ingested as input; every disagreement between run and census NAMED with the run's evidence. Zero disagreements is a valid result and is stated explicitly as such, not left implicit.</criterion>
  <criterion id="C7">**`run.json` schema-valid** with per-cycle hole census and method vintage, per page.</criterion>
  <criterion id="C8">**`certification.json` present and SIGNED BY CVO~Z**, per page, its verdict NAMING ITS DISCRIMINATOR, with the planted mutant recorded as caught. Unsigned, self-signed, or discriminator-less = fail.</criterion>
  <criterion id="C9">**Semantics landed from CVO~Z** on the 6-question block for every servable artifact, in a form W5 can lift into `DATA_CATALOG` v0.2 without re-interpretation.</criterion>
  <criterion id="C10">**Declared exclusions + surprises:** everything in scope NOT done, each with a reason (an unmarked gap reads as coverage); surprise-channel entries one line each, observed outside mandate, no action taken.</criterion>
  <criterion id="C11">**Session log with a populated Compiler Tools section** (blank/N-A not acceptable) + all commits on your own lane under your own author line.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/OPAL_ANALYST.W1_PROOF_OF_SPEC.json</instance_path>
  <!-- Issuer minted the id set at decomposition (PRD §9.8). Fill from YOUR OWN efforts: one row
       per id, criterion VERBATIM + exact re-runnable invocation + output evidence + denominator.
       NO BARE VALUES -- a PASS row with empty output_evidence invalidates the whole instance.
       Validate before any status flip:
         python .tools/proof-of-spec-check.py <instance> C1,...,C11    (POSITIONAL argv[2], never a flag)
       `controls` is not optional and not a formality: a passing assertion never mutated has
       never been tested. C8's planted mutant is your strongest control -- record it as one. -->
</proof_of_spec>

<deliverables>
  <deliverable type="commit">6 run directories under `workflows/atom_decomposition/runs/portal-page-*/` — each with `run.json`, `rectangle.c0.json`, `patches/`, `rectangle.final.json`, `certification.json`</deliverable>
  <deliverable type="document">Semantics landed per artifact (CVO~Z-authored), staged for W5 registry lift</deliverable>
  <deliverable type="document">`OPAL_ANALYST.W1_PROOF_OF_SPEC.json`, validator-clean against C1-C11</deliverable>
  <deliverable type="document">Session log with Compiler Tools section</deliverable>
  <deliverable type="document">**Method read** — where atom_decomp was awkward, ambiguous, or silent on a real question these pages raised. You run this method 10 more times after W1; W4's six uncensused pages are where a method defect costs the most.</deliverable>
</deliverables>

<do_not>
  <rule>**Do NOT build any alert, alarm, SNS topic, SES send, freshness checker, notification or `*-monitor`** — standing moratorium (Andrew-direct 2026-07-28). A finding lands as a GATE or an OWNED BLOCKING ITEM. This applies to anything a page's decomposition suggests would be "easy to watch."</rule>
  <rule>**Do NOT create any approval gate, sign-off step, or hold on another seat's work** (no-inferred-gates law, 2026-08-06). The certification requirement is the method's own Rule 14(e), not a gate this TO invents.</rule>
  <rule>**Do NOT delete, move, or "clean up" any served or served-adjacent artifact** found during decomposition — residue gets a DISPOSITION and a recommendation, never an act. Moving served output is NEVER#3 and needs never-widen sign-off.</rule>
  <rule>**Do NOT stand up any shadow path, parallel emitter, or standing comparator** to validate a finding (no-shadow veto, 2026-08-04). Validate on the real path; an ad-hoc QA read is run-and-read, nothing standing.</rule>
  <rule>**Do NOT sign your own certification** (Rule 14(e), and the whole point of the author/certifier split).</rule>
  <rule>**Do NOT decompose to panel grain** (req 7).</rule>
  <rule>**Do NOT treat the census as run evidence** (PRD §9.0) — the single most likely way this wave silently under-delivers.</rule>
  <rule>**Do NOT push.** Commit on your lane; MSTR~Z integrates :55-:00.</rule>
</do_not>
</task_order>
