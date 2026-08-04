<task_order>
<to_id>MDPF_CANRTE.W1.route-bindings-config</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>complete</status>
<priority>P1 (Phase-C wave 1; joint plan acceptance on record -- CTO 165917Z + COO 165942Z, gate-3 closed per CTO 170636Z; Andrew "Proceed" at the COO terminal 1706Z accelerates seating from the morning wave to NOW)</priority>

<title>MDPF_CANRTE W-1: route_bindings.yaml lands (pure-add, zero behavior) -- the Phase-A binding table as declared config</title>

<context>
GOVERNING DOCUMENT: your own Phase-B plan @c68f238e5 SS2 (W-1) -- this TO adds nothing to its
design and narrows nothing; on any perceived conflict the plan wins and you surface it. Inputs:
Phase-A design @ab2d2f167, CTO fork rulings (F-1/F-2/F-3 + canonized SS2.1 contract + ratified
grammar), TIGHT SCOPE @86f52bdfb.
</context>

<scope>
Exactly the plan's W-1: data/mdpf/config/route_bindings.yaml -- per-firm model/custody/non-model
source rows (49f custody = the Andrew-canonical DDB cohort VERBATIM per F-1/C-1), the L1 row
present ONLY with its declared vendor-grain reason (cottonwood; 49f/inflection ABSENT as the
reference shape), model-key sets, launch seams/depths, carry windows (roster-derived), and the
CARRY-IMPORT declaration as a binding row (plan SS6 step 4, KEEP-as-declared ruled). Sibling
pattern of partner_roster.json; deliberately NOT a roster extension. PLUS the read-only tie-out
validator: every binding row == the module constant it replaces, cited to live module constants
(dim:66-131 class), run once at land. Pure-add: NOTHING consumes the file yet; zero behavior
change anywhere.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>re-cite each binding row's source constant at CURRENT HEAD (your @e0d657799 citations re-resolved -- the tree moved today)</run>
      <expect>Every row traces to a live constant file:line @ current commit; any drift since Phase A named before encoding.</expect>
      <if_mismatch>STOP on any constant that moved semantically; a binding table encoding stale constants is born wrong.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>the tie-out validator against the landed yaml (pipe-free rc; print the denominator: rows checked)</run>
      <expect>Every row ties to its live constant; denominator == the full binding-row count, zero skips.</expect>
      <if_mismatch>STOP. Fix the row or the citation -- never land a partially-tied table.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO: commit + validator output verbatim; confirm zero consumers (grep for the filename estate-wide, expect only the validator + this TO family)</run>
      <expect>Pure-add proven, not asserted -- the rollback claim (delete the file) is only true while nothing consumes it.</expect>
      <if_mismatch>An unexpected consumer = W-2 started early somewhere -- surface before closing.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Zero shared files with live streams (new config file + a validator). W-2 (sibling TO, same seat)
consumes this file -- self-sequence W-1 first. The ETFS-CANON wall stands: the 49f custody row
carries the sovereign ruling VERBATIM; a future ETFS ruling flips one row, zero route change.
</cross_domain_coordination>

<acceptance_criteria>
1. route_bindings.yaml landed with every plan-named row family present; C-1 verbatim in the 49f
   custody row; L1 rows carry declared reasons or are absent.
2. Tie-out validator output in the log: full denominator, every row tied to a live constant.
3. Zero-consumer proof at close (the pure-add invariant).
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="plan">@c68f238e5 SS2 (governing) + SS9</ref>
  <ref type="rulings">MDPF_CANRTE_FORK_RULINGS_20260804.md (F-1/C-1, F-2 L1 discipline)</ref>
  <ref type="acceptance">CTO 165917Z + COO 165942Z + gate-record 170636Z; Andrew "Proceed" 1706Z (seating acceleration)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
