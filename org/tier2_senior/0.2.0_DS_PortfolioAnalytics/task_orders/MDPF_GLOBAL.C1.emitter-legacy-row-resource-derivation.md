<task_order>
<to_id>MDPF_GLOBAL.C1.emitter-legacy-row-resource-derivation</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>complete</status>
<status_note>Flipped pending->complete 2026-08-04T1545Z by assignee (stale-line reconciliation, evidence-cited): spec COMPLETE @03ab006764 (droppable branch EMPTY, parity 12/12 exact, :992 fail-loud spec, s2 verdict made sound); close-out ACCEPTED @f8d294e39b (CTO retirement-becomes-a-fix line folded).</status_note>
<priority>P1 (T5.B precondition C1, the DERIVATION leg -- CTO ruling 221736Z: RE-SOURCE IS THE DEFAULT AND THE PRESUMPTION. This is the last live dependency on the runner chain; your derivation determines the implementation AE base executes.)</priority>

<title>C1 derivation: can opal-assets-daily-emitter's non-re-sourced legacy rows re-derive from the canonical revamp lineage? RE-SOURCE presumed; droppable needs value-level proof</title>

<context>
~F's T5.A verdict @b877dbc0f5: the runner chain retires whole on {C1, C2}. C1's mechanism
(source-confirmed): opal-assets-daily-emitter's DAILY path base-reads the runner's
aggregate_aua/{date}.json partition (lambda_function.py:1513-1518 @440d16e018; deployed 07-28
config confirmed) because its non-re-sourced LEGACY ROWS have no other source. The emitter also
carries the :992 _latest_key silent-aging hazard (silently re-serves the last partition forever
if the producer dies -- today it IS aging, the runner has not run since 07-31).

CTO RULING (221736Z, binding): RE-SOURCE IS THE DEFAULT AND THE PRESUMPTION. Your derivation
runs on that footing: the deliverable is the re-source SPEC (how each legacy row re-derives
from the canonical revamp lineage: source table(s), transformation, parity expectation). The
DROPPABLE branch exists but carries an AFFIRMATIVE proof burden: a VALUE-LEVEL before/after
diff on the emitter's OUTPUT showing no served value moves -- never a reader count ("droppable
is a CONTENT claim"). Only if the derivation shows rows IRREPRODUCIBLE from canonical lineage
AND the value-level diff is clean does the droppable ask go to CTO with that diff.

BINDING REGARDLESS OF BRANCH (CTO verbatim class): the :992 silent-aging hazard closes WITH C1
-- "a reader that silently re-serves the last key forever when its producer stops is a
fail-toward-fine defect in its own right; it must not survive the re-source as 'well, it works
now.'" Your spec must state the fail-loud behavior the AE implementation carries.
</context>

<scope>
1. Enumerate the emitter's non-re-sourced legacy rows precisely (which rows, which fields, at
   :1513-1518's read) -- denominator printed.
2. Per row: derive whether it re-derives from the canonical lineage (opal-data-assets silver ->
   revamp gold). Output = the RE-SOURCE SPEC: source, transformation, expected parity, cited
   file:line @ commit per claim. UNKNOWN stays loud.
3. Parity pre-check in scratch: for a sample of dates, re-derived values vs the emitter's
   current output -- quantify agreement (this is the spec's evidence, and it also pre-builds
   the value-level diff should any row land in the droppable branch).
4. The :992 rider: specify the fail-loud replacement behavior (per-stage observable, per the
   CANON-PROVEN per-stage law) for the AE implementation.
5. Deliverable: derivation note + spec in your deliverables folder; report to COO + CTO + AE
   base (AE implements on your spec; CTO rules on any droppable ask with your diff).
6. READ-ONLY on production; scratch derivations only. The emitter Lambda itself is AE's to
   change, not yours.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before derivation">
    <step>
      <run>Read lambda_function.py:1500-1530 + :985-1000 at pinned commit; comp-estate mdpf for the lineage context</run>
      <expect>The base-read + _latest_key mechanisms confirmed at vintage; canonical lineage tables identified.</expect>
      <if_mismatch>STOP. A moved mechanism re-grounds before deriving.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io --pipeline mdpf on the canonical revamp scripts feeding the candidate source tables (hand-derive where the assets tree is still tool-blind, say so)</run>
      <expect>Candidate re-source tables' producers/columns enumerated.</expect>
      <if_mismatch>Tool gaps noted to the coverage build; hand-derivation labeled.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="derivation + parity pre-check">
    <step>
      <run>scratch re-derivation on sample dates; value-level compare vs current emitter output</run>
      <expect>Per-row verdict: RE-DERIVES (with parity quantified) or IRREPRODUCIBLE (with the mechanism why); no row left unclassified.</expect>
      <if_mismatch>An unclassified row is UNKNOWN-loud, never silently presumed either branch.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO + 0.7.0_AE_CloudOps: spec path + commit + per-row verdicts + the :992 fail-loud spec + any droppable ask WITH its value-level diff</run>
      <expect>AE base can implement from the spec alone; CTO has what a droppable ruling needs, if asked.</expect>
      <if_mismatch>A spec AE cannot implement from is REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
AE base owns the implementation leg (emitter Lambda change + :992 fix + deploy) on your spec --
they are mid-T2.C; your report gives them a ready work item for their next window, sequenced
with CTO. The runner chain stays LIVE until T5.B (your derivation must not assume it dead --
the 07-31 partition is the current base input). Sequencing at your seat: C2 first (small,
gate-granted), this second; both fit around tonight's cycle read and the AE asks.
</cross_domain_coordination>

<acceptance_criteria>
1. Legacy-row denominator printed; every row classified {RE-DERIVES + parity quantified /
   IRREPRODUCIBLE + mechanism / UNKNOWN-loud} with file:line @ commit cites.
2. Re-source spec implementable by AE without further derivation; :992 fail-loud behavior
   specified per-stage-observable.
3. Any droppable ask carries the VALUE-LEVEL before/after diff (CTO's affirmative burden),
   never a reader count.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T221736Z item (a) -- re-source default + droppable proof burden + :992 rider</ref>
  <ref type="kill-list">~F T5.A @b877dbc0f5 rows 1-2 (C1 holds the whole verdict at CONDITIONAL)</ref>
  <ref type="mechanism">lambda_function.py:1513-1518 + :992 @440d16e018 (deployed 07-28 config confirmed)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
