<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-pyfield-column-denominator</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>4.0.0_SA_CRO</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>NFRA_PYFIELD</project_code>
  </metadata>

  <objective>
    Establish the COLUMN DENOMINATOR for the Python gold/silver subscript population, so that an
    acceptance bar for the `PyFieldRecognizer` build can be STATED. Q2 measured that no column
    denominator exists: 24.3% flow-local reach is a true statement about SUBSCRIPTS and a meaningless
    one about COLUMNS, because much of the unresolved mass (`r['...']`, `row['...']`, `obj['Key']`)
    was never a column. This TO produces the denominator. It does NOT produce the extractor.
  </objective>

  <context>
    PRD: `docs/architecture/NFRA_PYFIELD_PRD.md` @004588f9cb (v1.0, AUTHORIZED). Read §2.4, §6 TO-0,
    §7 Q2/Q4, and Appendix A before starting. Project JSON: `org/projects/NFRA_PYFIELD.json`.

    AUTHORIZATION, Andrew-direct 2026-08-07 at the 1.0.0_SA_CTO~D terminal, VERBATIM:
    *"Yeah i want the python data tracing"* — with the consumer (*"it will be comp-pipescript"*) and
    the use case (*"when we do migrations it will be essential to be able to track field dependencies
    in pipelines"*). CTO~D's prior DEFER recommendation is SUPERSEDED and recorded as overturned.

    >> SEQUENCING IS LOAD-BEARING AND IT IS NOT THE OBVIOUS ONE (CTO~D architecture ruling, carried
    here verbatim in substance): TO-0 IS THE COLUMN DENOMINATOR, NOT THE EXTRACTOR. Building the
    extractor first ships a mechanism nobody can score. AUTHORIZATION DOES NOT MEAN START AT THE BUILD.

    ⚠ THIS IS A MEASUREMENT DEPENDENCY, NOT AN APPROVAL STEP. Nothing in this TO requires any seat's
    signature, GO, sign-off or co-sign, and no other workstream is held pending your output. What is
    true is narrower and purely factual: TO-1's acceptance criteria are UNSTATEABLE until a denominator
    exists. You are not gating anyone (Andrew-direct 2026-08-06: no gates on any work unless he asks).

    WHY THE THIRD STRATUM EXISTS — the sensitivity test that motivates this whole TO. The "column
    floor" moves 5.5x with the marker set, measured at the CTO~D seat against your own probe:

      MINIMAL (`value_counts`,`nunique`,`fillna` — no dict has these)   228 hits   5.2%
      MID     (approximately your set)                                  735 hits  16.7%
      WIDE    (any method not on `dict`)                              1,247 hits  28.3%

    Your Result-2 SHAPE survives — usage-side genuinely IS evidence of column-ness. The NUMBER attached
    to it does not: 1,016 is not "the" floor, it is THAT MARKER SET's floor. The ~507 sites between
    MINIMAL and MID are exactly where the hand-chosen set does its unverified work, which is why they
    are a named stratum below rather than folded into a general sample. (Your denominator of 4,406
    name-based subscripts reproduced EXACTLY at the CTO~D seat by an independently written probe —
    two probes agreeing on the population is what makes the spread attributable to the marker set
    rather than to the corpus. That agreement is why this TO can proceed on your strata counts.)
  </context>

  <compiler_tools_mandate>
    Phase 1 — before classifying anything:
      <run>comp-which "how do I find python subscript call sites in gold scripts"</run>
      <expect>Routes to a rich tool, or RUNS the on-rails search primitive with dependency context.
      Never dead-ends.</expect>
      <if_mismatch>If comp-which routes nowhere for this intent, that is a COVERAGE GAP, not an excuse
      to reach for raw grep — record it and report it to COO in the session log.</if_mismatch>

      <run>comp-find "\[['\"]" data/inf/scripts/gold data/assets/scripts/gold</run>
      <expect>Graded content hits with band labels (HEAD|DEF|SURFACED|CONFIG|TEST|DOC|COLD) and
      dependency context. Use `--all` when you need the full population rather than page 1 —
      A PAGINATED COUNT IS A PAGE SIZE WEARING A TOTAL'S CLOTHES, and this TO's entire output is a
      denominator.</expect>
      <if_mismatch>If a stratum count from comp-find disagrees with the PRD's figures (596 / ~507 /
      2,596), do NOT silently adopt either — report both with their retrieval commands and say which
      you used. A denominator that changed without explanation is the finding, not a nuisance.</if_mismatch>

      ⚠ USE `comp-find`, NOT `comp-grep`/`comp-glob`. Base-CTO ruling 2026-08-07 (1.0.0_SA_CTO,
      responding to this TO's authoring): comp-find EXISTS, is registered on all 7 canonical surfaces,
      carries a 25-test mutation-checked battery @c2b6e828d, and passed an independent non-author field
      trial — so a TO naming it is EXECUTABLE TODAY regardless of the Rule-21 law text, and the CTO owns
      closing that gap. Verified at the COO seat before issuing: `comp-find --help` runs and self-
      describes as "replaces comp-grep" / "replaces comp-glob". Scored on OUTPUT, not rc.

      <run>comp-estate --definitions</run>
      <expect>Prints the RATIFIED term registry (SYSTEM_DEFINITIONS).</expect>
      <if_mismatch>If `column`, `field`, or `subscript` already carry ratified definitions that conflict
      with the vocabulary you are about to use, adopt the ratified term — do NOT re-coin beside it
      (BUILD LADDER rung 2, granularity amendment, Andrew-direct 2026-08-07).</if_mismatch>

    Phase 2 — before committing:
      <run>comp-which "what consumes the NFRA_PYFIELD column denominator"</run>
      <expect>Orientation only. No production code is produced by this TO, so no blast radius changes.</expect>

    Phase 3 — after committing:
      Record every command run, its output disposition, and WHICH search primitive was live at your
      seat, in the session log Compiler Tools table. A TO with no compiler check logged is NOT accepted
      as complete (`org/standards/TO_COMPILER_GATE.md`).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Reasoned, not assumed: this TO writes NO production code, modifies NO gold/silver script, no
    Lambda, no portal component, no IAM, and no S3 key. Its only output artifact lives in the CRO home.
    `comp-blast` was NOT run because it takes a function or artifact and this TO changes neither —
    a vacuous call would produce a clean-looking result that asserts nothing. The PRD is REFERENCED,
    not modified. TO-1 (0.8.0_AE_CloudComp) consumes this TO's OUTPUT VALUE, not any file it writes,
    so there is no last-write-owner to sequence. -->
  </cross_domain_coordination>

  <acceptance_criteria>

    1. A PUBLISHED COLUMN DENOMINATOR carrying, in one place: the numerator, the denominator, the
       sampling rule, the confidence interval, and a MEASUREMENT VINTAGE (ISO date).
       ⛔ FORBIDDEN SHORTCUT, NAMED SO IT CANNOT BE TAKEN BY ACCIDENT: "N columns found" is NOT
       acceptable. "N from M subscripts, K unresolved/undecidable, sampled by <rule>, measured
       <date>" is. A numerator without a denominator reproduces EXACTLY the defect this project
       found in D1's own declarations — in a producer where nobody has a prior to check against.

    2. THE CLASSIFICATION CARRIES THREE STATES, NOT TWO: `column` / `not-column` / `undecidable-at-
       this-site`. The third state is MANDATORY and it is not a formality — a base that the call site
       genuinely does not disambiguate must land in it, never be forced into one of the first two.
       ⛔ A run reporting ZERO undecidable sites is a FINDING AGAINST THE CLASSIFICATION, not a clean
       result: the population is known to be genuinely mixed, so zero ambiguity means the ambiguity
       was absorbed silently and the denominator inherited the forcing.

    3. STRATA COVERED, with per-stratum counts reported SEPARATELY (a pooled figure hides which
       stratum carries the uncertainty):
         (a) the 596 usage-only hits — FULL census, all 596 classified
         (b) the ~507 sites between the MINIMAL and MID marker sets — FULL census
         (c) the 2,596 neither-axis hits — SYSTEMATIC sample, n >= 200
       Each stratum's column-rate is reported with its own interval.

    4. SAMPLING IS SYSTEMATIC AND RE-DERIVABLE. First-per-file alphabetical (the way CVO~C sampled the
       portal loci), or an explicit every-Nth rule with N stated.
       ⛔ FORBIDDEN SHORTCUT: a hand-picked sample MEASURES THE AUTHOR, not the corpus. The
       per-site classifications must be recorded INDIVIDUALLY (site locus + verdict + one-line reason)
       so a second party can re-derive the ratio without re-doing the judgement. A summary table alone
       does not satisfy this — the easiest way to pass a summary-only criterion is to classify a
       handful and extrapolate, which is the defect.

    5. THE PUBLISHED FIGURE STATES ITS CORPUS AND IS NOT PRESENTED AS AN ESTATE FIGURE.
       Per PRD Appendix A: `data/inf/scripts/gold` + `data/assets/scripts/gold` are re-derived;
       `bd`, `cot`, `mdpf` and the assets monolith are UNSWEPT; the `etfs`+`find` figures are carried
       on your own word and NOT re-derived at any other seat. Whatever you sweep, name what you did
       NOT sweep in the same sentence as the number.

    6. Session log with a Compiler Tools section (mandatory) and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier1_exec/4.0.0_SA_CRO/deliverables/NFRA_PYFIELD_COLUMN_DENOMINATOR_20260807.md</file>
      <file action="create">org/tier1_exec/4.0.0_SA_CRO/logs/{session log}</file>
      <file action="reference">docs/architecture/NFRA_PYFIELD_PRD.md</file>
      <file action="reference">data/inf/scripts/gold/**.py</file>
      <file action="reference">data/assets/scripts/gold/**.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Classify strata (a) and (b) in full and stratum (c) by systematic sample, into
    the three-state vocabulary of criterion 2.</requirement>
    <requirement id="2">Record each classified site individually: locus, verdict, one-line reason.</requirement>
    <requirement id="3">Publish per-stratum rates with intervals, then the pooled denominator with its
    sampling rule and vintage.</requirement>
    <requirement id="4">State the corpus bounds — swept and UNSWEPT — beside the figure.</requirement>
    <requirement id="5">If the probe you used for the original spike is still scratchpad-only and
    uncommitted, commit it under this TO so the measurement is reproducible. You flagged it yourself as
    needing re-derivation before anything rests on it; something now rests on it.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">The column-denominator deliverable named in scope.</deliverable>
    <deliverable type="commit">The classification record + the probe (requirement 5).</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT build the extractor, the recognizer, or any production code. Zero production code in
    this TO. That is TO-1 and it has a different receiver.</rule>
    <rule>DO NOT lift or reuse `_DF_METHODS` as the marker set. It is hand-drawn and incident-driven —
    71 names against a real universe of 240, missing 170 (70.8%), carrying one entry that can never
    fire, and not version-pinned. If you need a marker set for stratification, DERIVE it from the
    installed pandas API and say which version you derived against.</rule>
    <rule>DO NOT hand-pick the sample. See acceptance criterion 4.</rule>
    <rule>DO NOT report a numerator without its denominator, and DO NOT present any figure here as an
    estate-wide figure.</rule>
    <rule>DO NOT call any external vendor API. No per-use word has been given and availability is not
    authorization.</rule>
    <rule>DO NOT build any alert, alarm, SNS topic, SES send, freshness checker or monitor. Standing
    moratorium.</rule>
    <rule>DO NOT treat this TO as authority to hold, gate, or block another seat's work. It blocks
    nothing by approval; it supplies a value TO-1's bar needs.</rule>
  </do_not>
</task_order>
