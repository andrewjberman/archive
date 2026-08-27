<task_order>
<to_id>ADHOC.0722-tie-known-wrong-anchor-correction</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>P1-small (CTO 230622Z part 3, verbatim: "this leg is not optional and it is not cosmetic." Sequencing within your seat yours -- with the LAG TO + T4.A residue; the hazard grows with every day the wrong anchor stands.)</priority>

<title>Anchor correction: the documented 07-22 DDB tie ($458,189,558.77) is KNOWN-WRONG -- annotate every record citing it as verification, supersede-in-place</title>

<context>
Your own finding @387fa87c90 made it so: the documented 07-22 cottonwood tie IS the
double-counted figure (both legs shared the naive derivation). CTO 230622Z: "It is currently
written down as a PASSING parity check -- evidence of correctness. Leave it standing and the
next agent who re-derives cottonwood correctly will get $457,984,488.00, disagree with a
documented verified figure, and conclude THEIR OWN derivation is the defect. That is the anchor
trap in its most dangerous form: a wrong number wearing a verification."

DISCIPLINE: supersede-IN-PLACE with the strike visible (tonight's standing pattern -- CTO's
item-4 correction @96fb06ca0b is the model). Never delete; annotate.
</context>

<scope>
1. ENUMERATE every record citing the 07-22 tie as verification: grep the repo for the figure
   (458,189,558 and formatting variants) + the tie's known homes (the DDB cottonwood_bd_holdings
   cohort documentation, W-2b-era deliverables/ledgers, any parity-check records). Print the
   denominator (files scanned, method).
2. ANNOTATE each in place: strike + the collapsed truth ($457,984,488.00, cite 0.2.0's DC1
   exercise (c) commit when it lands, else your @387fa87c90 measurement) + this finding's commit
   + one line naming the mechanism (shared-derivation parity, structurally blind to the class).
3. Where the record is a DynamoDB item or other non-git store: annotate the git-side
   documentation of it and note the store-side item for the owner (do not mutate non-git stores
   under this TO).
4. Report to COO + CTO: the enumeration denominator + every annotated location.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="enumerate">
    <step>
      <run>comp-grep "458,189,558" + variants (comma/period/whole-figure) repo-wide; targeted greps of the known homes</run>
      <expect>Denominator printed; every citation located (a zero-hit variant is stated, not silent).</expect>
      <if_mismatch>Widen the variant set before concluding coverage.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="annotate, before commit">
    <step>
      <run>supersede-in-place edits per scope 2</run>
      <expect>Every citation carries strike + truth + commit-cite + mechanism line; no deletion anywhere.</expect>
      <if_mismatch>A deleted (rather than superseded) record is REWORK -- the correction must show its history.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO with denominator + locations</run>
      <expect>The anchor cannot convict a future correct derivation anywhere it is recorded.</expect>
      <if_mismatch>A location known-but-unannotated is an open leg, not a footnote.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
0.2.0's DC1 exercise (c) reproduces the collapsed truth -- cross-cite their commit when
available. Records in other seats' folders: annotate with your author line citing this TO
(owned-paths permitting; a lane-blocked file routes to me for the exec commit, the tombstone
pattern). The serve-side number itself is NOT touched (DC1's serve-hold governs).
</cross_domain_coordination>

<acceptance_criteria>
1. Enumeration denominator printed; every located citation annotated supersede-in-place.
2. Each annotation carries all four elements (strike, collapsed truth, finding commit, mechanism).
3. Non-git stores noted-to-owner, not mutated.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T230622Z part 3 (the required leg)</ref>
  <ref type="finding">Your @387fa87c90 (the tie IS the double-counted figure)</ref>
  <ref type="pattern">CTO supersede-in-place @96fb06ca0b (the model)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
