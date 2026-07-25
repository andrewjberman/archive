<task_order>
<to_id>NFRA_MSBEFF.R2</to_id>
<title>comp-dataflow — answer the question the estate cannot currently ask: "does this value come from the canonical source, or from somewhere else?" (Andrew's state-and-dependency gap, named verbatim by an agent)</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<!-- RE-TARGETED 2026-07-23 from base 0.8.0 to the ~A tilde lane (Andrew spawned 4 build tildes to
     parallelize the R-series). The batch-GO to base covered R1R3->R5->R2->R4R6 serially; R2 and R4R6
     now move to dedicated lanes so base keeps only R5 + owns the shared registration surface. ~A
     builds R2 + the PSTMRT item-9 family; the batch-GO assignment of R2 to base is SUPERSEDED. -->
<date>2026-07-23</date>
<status>ACCEPTED (build) -- CVO~Z standing verify NEVER OBSERVED</status>
<!-- LABEL RULED BY 1.0.0_SA_CTO~Z @20260725T170702Z, and the label IS the ruling: the standing
     <verification>3.0.0_SA_CVO~Z</verification> is DISCHARGED AS A GATE (it gates nothing; CVO~Z's queue
     holds items gating live builds) but RETAINED AS A LABEL. This TO must NOT be recorded as CVO~Z-verified,
     because it is not. "Complete" and "independently verified" are different claims, and the recurring
     estate failure is the second silently inheriting the first's authority -- so the distinction is carried
     in the status field itself, where a reader cannot miss it, rather than in a comment or a message.
     What actually earned the discharge: base 0.8.0 RAVC-closed by RE-RUN, not self-report.
     If CVO~Z later wants the pass it is welcome to it. Nothing waits on it. -->

<!-- CLOSED 2026-07-25 by 0.8.0_AE_CloudComp~A (status was STALE at `pending`; the work landed 07-23).
     comp-dataflow BUILT + accepted: self-test 7/7, RF-7 shape flagged (exit 1) with the clean-canonical negative
     control in an ISOLATED invocation (exit 0); bounded mdpf sweep with printed denominator, 16 findings routed to
     CTO~Z per TRIGGER_LAYER. Accepted by 1.0.0_SA_CTO~Z @20260723T194300Z; RAVC-closed by base 0.8.0 @194401Z
     (re-run, not self-report). Log: logs/2026-07-23/r2_comp-dataflow_build_lane-A.md @b24099572b.
     RESIDUAL, named not implied: the <verification>3.0.0_SA_CVO~Z</verification> standing verify of the RF-7 flag +
     the isolated / same-file 4-read controls was never observed landing. Acceptance and RAVC close were done by the
     ISSUING chain, so the TO is complete; the CVO~Z pass is an open verification, not open build work. -->
<priority>P2 — the charter's own named gap; highest VALUE, moderate build</priority>

<authority>
Andrew-direct 2026-07-23 (verbatim in NFRA_MSBEFF.R1R3 authority block). Charter tie-back, Andrew
2026-07-23 VERBATIM: "the missing layer is truly understanding state and dependencies, which the tools
should solve for, because the agents reasoning should be enough otherwise." New capability — no
standard-change gate. ~Z owns the design call; 0.8.0 builds.
</authority>

<evidence_base>
Agent-verbatim, signal-3, 2026-07-13 (nl_structured/findings_merged.jsonl): "`comp-*` cannot answer a
DATA-FLOW question ('does this assign a value that did not come from the canonical source?')".
Corroborating named gaps from the same corpus: "the compiler-graph doesn't model field-threading at
the typed-shape boundary" · "The converse ('endpoint reads artifact X; new feature data lives in
artifact Y') is not checked" · "output-key COLLISION (2+ producers -> one sink) was a real estate
blind spot -- comp-dups scans code bodies, not write targets".
LIVE DEFECT THIS ANSWERS (the acceptance target): MDPF RF-7 — 49F counts imported from a LEGACY
SERVED artifact with no per-date source. Nothing detected it; it was found by manual trace.
</evidence_base>

<scope>
BUILD comp-dataflow: trace a served/consumed VALUE back to the assignment that produced it, and flag
when its origin is not the declared canonical source.
  A. Value-origin trace: given a served artifact field (or a gold/silver column), walk producer-side
     to the assignment(s) that set it.
  B. CANONICAL-SOURCE ASSERTION: flag when the origin is a served/legacy artifact rather than the
     declared canonical source for that value — the RF-7 shape.
  C. Compose with, do not duplicate, the PSTMRT layer-grammar gate (bundle item 9: "no gold/silver
     producer reads from a served artifact"). Item 9 is the GATE form of the same law; this is the
     QUERY form. Build them as one family — shared traversal, two entry points. If item 9 has already
     landed, extend it rather than forking.
  D. Output-key collision (2+ producers -> one sink) falls out of the same write-target index — include
     if it is cheap on the traversal you build; otherwise name it as the deferred sibling.
SCOPE DISCIPLINE: this is a DEPENDENCY/LINEAGE question, not a data-value question. It answers "where
did this come from", never "is the number right".
CARRY THE R1R3 OUTPUT CONTRACT (coverage + plane/vintage lines) — and state its blind spots plainly:
whatever the AST cannot see (dynamically-keyed writes are a known, corpus-named blind spot) must be
NAMED in the coverage line, not silently skipped.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-blast + comp-pipescript io over the existing traversal code; check whether PSTMRT item 9 (layer-grammar gate) has landed and reuse its traversal</run>
    <expect>A stated build-or-extend decision citing item 9's status. Do not fork a second traversal.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>ACCEPTANCE MUTANT on the real defect: point the tool at the RF-7 shape (a value imported from a legacy served artifact). It MUST flag it. NEGATIVE CONTROL, separate invocation: a clean canonical read must NOT flag.</run>
    <expect>Both on the record. A tool that flags everything is as useless as one that flags nothing.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Sweep a bounded real surface (one gold tree) and report the finding count with its denominator.</run>
    <expect>Findings land per TRIGGER_LAYER doctrine (owner + severity), never as a report line.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same family as PSTMRT bundle item 9 (layer-grammar gate) — coordinate, share the traversal. No
main-fabric coupling. Any finding this sweep produces about live MDPF artifacts routes to ~Z first,
never direct to main-fabric lanes (their MDPF chain is closing this session).
</cross_domain_coordination>

<acceptance_criteria>
1. RF-7-shape detection exercised (flags a legacy-served-artifact origin) + isolated negative control.
2. Build-or-extend decision on item 9 stated with its status cited.
3. Coverage line names the AST blind spots explicitly (dynamically-keyed writes at minimum).
4. One bounded real sweep with printed denominator; findings filed per TRIGGER_LAYER (owner+severity).
5. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z. Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
