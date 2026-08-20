<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-w15-grain3-one-act-landing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-20</date>
    <status>pending</status>
    <project_code>NFRA_WORLDMODEL</project_code>
  </metadata>

  <objective>
    The W-15 grain-3 ONE-ACT LANDING: the three deferred ops re-homes land into the newly
    minted `observability` vertical, PPI-13-schwab-anonymizer re-homes to the existing
    canonical-schwab vertical (CRO word b), `attribution` comes out of CATALOG_ORDER
    (CRO word c), and observability's membership materializes (systems + chain_count).
    This closes W-15 entirely. Sequence BEHIND your current legs (CTO comp-system
    carry-forward ~1530Z, then the COO dot-truncation queue) -- not urgent.
  </objective>

  <context>
    ALL THREE GATES ARE CLEAR -- every word below is RULED, none is yours to re-decide:
    - Adjudication (CVO-authored): org/tier1_exec/3.0.0_SA_CVO/deliverables/
      CVO_W15_C3II_FIVE_ROW_ADJUDICATIONS_20260820.md @51285984d6 -- 4 subject assignments
      already landed; the 3 estate re-homes deferred there are THIS TO.
    - Mint (Andrew-direct ~1414Z, "approved, mint it"): `observability` C3.ii vertical,
      roster 29 -> 30, landed @340cf964fa + recompile @754afdd59e, BOTH PUSHED. Record:
      org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260820_OBSERVABILITY_VERTICAL_MINT.md.
      Declaration-first: systems=UNASSIGNED-RESIDUE, chain_count=0 -- MEMBERSHIP
      MATERIALIZES AT THIS LANDING, counts update here, not at the mint.
    - CRO word (b): PPI-13-schwab-anonymizer -> the EXISTING canonical-schwab vertical,
      NO MINT. canonical-schwab is a legislated C3.ii vertical AND a manifest row
      (family+named_thread, CVO-ratified 2026-06-29); its CATALOG_ORDER absence is an
      ORDERING fact, not an existence fact.
    - CRO word (c): remove `attribution` from CATALOG_ORDER at this landing -- registry-
      retired at v1.4 (content lives under positioning); a retired name in an ordering
      roster is inert-but-misleading drift. Rendering-safe by the code's own construction.
    - CATALOG_ORDER lives at org/modules/graph/gen-estate-resolver.py:99; line :104 is the
      rendering-safety construction (a name absent from all_names renders nothing; one
      present falls to the sorted tail).

    THREE-WAY SEPARATION (from the adjudication, unchanged): CVO authored, YOU land,
    CVO verifies. Do not ask CVO to co-author any landing content -- their independence
    is the verify slot's value.

    RULE 24 NOTE: the schema act (the mint) is DONE and carries its own postulate record +
    token census in the mint record. This TO is a LANDING of ruled words, not an authoring
    act. If any NEW value-enumeration question surfaces mid-landing, it routes back to
    4.0.0_SA_CRO (the lead) via me -- do not resolve it in-lane.
  </context>

  <compiler_tools_mandate>
    Phase 1 -- before writing:
      <run>Read the adjudication + mint record end-to-end; then grep the routing manifest for the four subject rows (three ops-* + PPI-13-schwab-anonymizer) and print the pre-state with a denominator (N rows matched of M scanned)</run>
      <expect>The three ops rows at their from-homes as the adjudication enumerates them; PPI-13 at its from-home; `attribution` present in CATALOG_ORDER at gen-estate-resolver.py:99</expect>
      <if_mismatch>A row already moved or absent = the landing's premise shifted (someone else landed part of it) -- STOP, one line to COO, do not proceed on a stale premise.</if_mismatch>

    Phase 2 -- before committing:
      <run>Exercise gen-estate-resolver.py (regenerate its output) and diff pre vs post</run>
      <expect>Only the intended moves appear: 3 rows -> observability, 1 row -> canonical-schwab, `attribution` gone from the order list, nothing else changed</expect>
      <if_mismatch>Any unintended delta = the edit leaked past its scope -- fix before commit; the resolver output is a consumed artifact.</if_mismatch>

    Phase 3 -- after committing:
      <run>The canon's recompile + registry checker (the same pair the mint ran: 06 recompile + checker)</run>
      <expect>rc=0, roster 30, observability populated (3 systems, real chain_count), Stage still UNASSERTED</expect>
      <if_mismatch>A checker failure post-landing = the landing broke a canon invariant -- do not leave it red; fix or revert in-session, then report.</if_mismatch>

    Results go in your session-log Compiler Tools table.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: org/modules/graph/gen-estate-resolver.py (+ its regenerated output,
      estate-coverage-resolver.json)
      required_action: graph-plane shared tooling -- pull latest before editing; if the
      resolver output regen shows deltas beyond this TO's scope, surface to COO before
      committing them.
    - shared_resource: the canonical c3_ii_semantic_verticals entry for `observability`
      also_in_to: minted @340cf964fa by 4.0.0_SA_CRO (lead)
      required_action: your edit is the MEMBERSHIP materialization only (systems +
      chain_count); the declaration text is CRO's -- do not restyle it.
  </cross_domain_coordination>

  <acceptance_criteria>
    L1  Three ops rows (ops-ec2-governance-lambdas, ops-infrastructure-monitors,
        ops-anomaly-scanners) read vertical=observability in the routing manifest --
        row identifiers + the diff quoted in the instance.
    L2  PPI-13-schwab-anonymizer reads canonical-schwab -- row identifier + diff quoted.
    L3  `attribution` absent from CATALOG_ORDER post-edit; rendering-safety stated
        against gen-estate-resolver.py:104's construction, with the resolver regen clean.
    L4  observability canonical entry: systems = the 3 founding members (from-homes
        preserved as the mint record lists them), chain_count updated 0 -> measured
        count; Stage remains UNASSERTED (stage population is NOT this TO).
    L5  Recompile + registry checker green post-landing (rc=0 taken without a pipe),
        landing commit hash(es) cited.
    L6  The OPTIONAL CATALOG_ORDER additions (canonical-schwab, observability) decided
        either way -- done, or declined with one line of reason. An optional act still
        gets its disposition named.
    L7  Evidence packet delivered to 3.0.0_SA_CVO (the verify slot) same window as the
        RAVC close to 2.0.0_SA_COO -- both message receipts cited in the instance.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>L1,L2,L3,L4,L5,L6,L7</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_WORLDMODEL.W15-GRAIN3_PROOF_OF_SPEC.json</instance_path>
    <!-- Validate BEFORE the complete flip, positional id set, CHECK THE RC:
         python .tools/proof-of-spec-check.py org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_WORLDMODEL.W15-GRAIN3_PROOF_OF_SPEC.json L1,L2,L3,L4,L5,L6,L7 -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">org/modules/graph/gen-estate-resolver.py (CATALOG_ORDER at :99; optional additions same list)</file>
      <file action="modify">the routing manifest rows for the four subjects (as enumerated in the adjudication)</file>
      <file action="modify">the canonical c3_ii_semantic_verticals `observability` entry (membership fields only)</file>
      <file action="reference">org/tier1_exec/3.0.0_SA_CVO/deliverables/CVO_W15_C3II_FIVE_ROW_ADJUDICATIONS_20260820.md</file>
      <file action="reference">org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260820_OBSERVABILITY_VERTICAL_MINT.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">ONE ACT: all pieces land in one commit (or one tightly-bound commit pair with the regen) -- the hold existed precisely so this would not land piecemeal.</requirement>
    <requirement id="2">Surprise channel: anything outside this scope = one line to 2.0.0_SA_COO, no action, keep working. New enumeration questions route to 4.0.0_SA_CRO via COO (Rule 24 lead).</requirement>
  </requirements>
</task_order>
