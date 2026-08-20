<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-cot-supervised-portfolio-group</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (gold/dim legs, Rule 13) + 0.6.2_AE_PartnerETL (bronze fetch leg G1)</issued_to>
    <date>2026-08-20</date>
    <status>pending -- 0.2.0_DS GO'd 2026-08-20T1724Z (COO msg 63320, writes authorized, G2-first sequencing); 0.6.2_AE GO fires on its own registration</status>
    <project_code>COT_SUPERVISED (Andrew-sanctioned fix, CTO-designed 63310; cot = Cottonwood, COMPLETELY separate firm pipeline from bd -- Rule 13 separation binds)</project_code>
  </metadata>

  <objective>
    ANDREW-SANCTIONED (his word at the CTO terminal ~1632Z, VERBATIM: "Yeah we need to fix
    the cottonwood issue, there should be a way to do this retroactively through some kind
    of filter, also it appears that cottonwood uses the 'portfolio_group' key to split
    advisors, i need CTO to investigate these."): land the Cottonwood supervised/unsupervised
    retroactive filter + the portfolio_group advisor-book split, per CTO's completed
    investigation @1d196ac3ba (CTO_COT_SUPERVISED_FIELD_TRACE_20260820.md -- READ FIRST;
    the design below is CTO's, gate is CTO's, nothing here is yours to re-design).
  </objective>

  <context>
    GROUNDED FINDINGS (CTO trace, both legs): the cot book's supervised split is CLEAN AT
    ACCOUNT LEVEL (0/102 mixed in the HAR account drill; unsupervised = dedicated held-away
    accounts) -- so the retroactive filter is a DIMENSION JOIN on AccountID over existing
    history, NO re-pull of history. The pipeline gap is ONE LINE: A_00.accounts_dimension
    DECLARES portfolio_group and :599's `available` filter SILENTLY DROPS it (the
    transactions extract never carries it; served dim read live: 23 cols, no
    portfolio_group) -- the declared-vs-delivered class.

    EGRESS BASIS, named: the G1 pull is Cottonwood Black Diamond DataMining -- under the
    STANDING cot-BD egress lift (Cottonwood BD ONLY, not bd/49f). No fresh egress word needed.

    ⚠ GRAIN PIN (COO-injected, standing law): cot BD fact_holdings is RELATIONSHIP-grain
    (row = Relationship x Account x Asset) -- NAIVE SUMS DOUBLE-COUNT. Every AUM tie-out in
    this TO collapses grain first (collapse_relationship_grain()) or its numbers are wrong
    by construction.

    THE HAR ORACLE (2026-08-19, from Andrew's own session): supervised firm $458,351,400 /
    named-books $455,532,550 (= Manav's $455M exactly) / unsupervised $30.4M (the delta he
    asked about). Books: Rubottom $290M / Shipley $135M / Bass $45M / No-Group $18.8M.
    The $18.8M No-Portfolio-Group line to Manav's side is AT ANDREW'S DISCRETION -- noted,
    not an act in this TO.

    NAMED CAVEAT (rides every deliverable, stated not silent): the dimension join applies
    TODAY'S flags to history -- acceptable for dashboard AUM by design decision (CTO),
    never presented as historical point-in-time supervision state.
  </context>

  <compiler_tools_mandate>
    Phase 1: read the CTO trace end-to-end; comp-pipescript io A_00 --pipeline cot (COLUMN
    GAPS before touching the dim); enumerate :599's current drop set with a denominator.
    Phase 2: commit-gate (auto); the tie-out battery BEFORE commit -- grain-collapsed sums
    vs the HAR oracle row-for-row; a mutant (un-collapsed sum) must FAIL the tie-out.
    Phase 3: comp-pipescript deployed per script touched (Rule 13 DS deploy incl. s3 cp);
    comp-validate per gold artifact; served-dim re-read showing portfolio_group present.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: the cot tree (data/cot/... per PIPELINE_MAP)
      required_action: cot is a COMPLETELY separate firm pipeline from bd -- never mirror or
      sync (gate + IAM enforced). Any bd/49F pattern (e.g. the BD-style aum toggle in G5,
      the sleeves precedent) is cited as PATTERN REFERENCE ONLY -- no shared code, no shared
      keys (CTO 63314). 0.6.2 owns the bronze fetch; DS owns silver/gold per Rule 13;
      coordinate the A_00 landing seam by MCP before either commits. STAFFING NOTE: DS~B
      (0.4.0) is explicitly NOT this TO's seat -- it holds the FRI named-reader control the
      single-green compression leans on (MSTR 63313 + CTO 63314 concur).
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is CTO's six-leg design (a)-(f); G1-G6 map to
    (a)-(f) one-to-one, G7 is the proof contract -- exhaustive over the sanctioned design,
    nothing outside it in scope.)
    G1 [0.6.2, design leg a]: ONE account-attributes DataMining pull at Account level
        {AccountID, Account Supervised, Account Billable, Position Only, Portfolio Group}
        landed bronze-raw (Rule 17a: byte-faithful) and consumed into A_00.
    G2 [DS, leg d]: A_00's :599 available-filter gains a LOUD PRINT for dropped declared
        columns (the silent-drop fixed as a class, not just for these fields); served dim
        re-read shows portfolio_group + supervised flags present (was 23 cols without).
    G3 [DS, leg b]: the retroactive supervised filter = dim join on AccountID over existing
        history; ACCEPTANCE = grain-collapsed tie-out vs the HAR oracle on 2026-08-19:
        $458,351,400 / $455,532,550 / $30.4M, and the four book totals. The un-collapsed
        mutant fails.
    G4 [0.6.2 + DS, leg c] -- SCOPE PINNED 2026-08-20 ~1740Z (COO, on 0.6.2's fork 63338):
        {Holding Supervised + Account Supervised} BOTH added to the daily holdings template
        (BD templateId 226355, in-place update per the AUAFIX-DATEMODE precedent). This
        TO's original one-column line was a PARAPHRASE of CTO's trace section 2, which
        names two columns -- the ruled design source governs over the paraphrase (the
        W15-L4 precedent, same day). Mechanism concurs: with both columns the daily
        invariant (a holdings row whose flag disagrees with its account's = a loud
        finding) is SELF-CONTAINED in each day's extract, and account_supervised gains a
        daily refresh path the one-shot G1 pull cannot provide. The Portfolio-Group
        template rider (same staleness class, surfaced by 0.6.2) is CTO's design fork,
        routed separately -- NOT granted here; if CTO's word lands before the template
        touch fires it folds in, else it rides a second touch.
    G5 [DS, leg e]: gold emits BOTH aum_supervised and aum_all (the BD-style toggle) +
        the portfolio_group book split.
    G6 [DS, leg f]: the today's-flags-to-history caveat stated in the served artifact's
        meta/notes -- verifiable by reading the artifact, not the TO.
    G7: proof instance VALID rc=0 positional G1-G7; CTO arch-gate acceptance cited.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>G1,G2,G3,G4,G5,G6,G7</expected_criteria>
    <instance_path_grammar>org/tier2_senior/{assignee_folder}/deliverables/COT_SUPERVISED_PROOF_OF_SPEC_{seat}_{YYYYMMDD}.json</instance_path_grammar>
    <group id="bronze-G1-G4" status="NOT_YET_MINTED" instance_path="org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/COT_SUPERVISED_PROOF_OF_SPEC_062_20260820.json"/>
    <group id="gold-G2-G6" status="NOT_YET_MINTED" instance_path="org/tier2_senior/0.2.0_DS_PortfolioAnalytics/deliverables/COT_SUPERVISED_PROOF_OF_SPEC_020_20260820.json"/>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Not deadline-bearing; normal cadence. Surprise channel: one line to 2.0.0_SA_COO. New enumeration questions (any axis/value minting) route through CTO per Rule 24.</requirement>
    <requirement id="2">RAVC close to COO, cc 1.0.0_SA_CTO (arch gate). The Manav book-hygiene line stays at Andrew's discretion -- no outbound act from either seat.</requirement>
  </requirements>
</task_order>
