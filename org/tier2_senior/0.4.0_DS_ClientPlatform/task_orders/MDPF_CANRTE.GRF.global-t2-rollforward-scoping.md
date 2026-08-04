<task_order>
<to_id>MDPF_CANRTE.GRF.global-t2-rollforward-scoping</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P1 (ANDREW-DIRECT ~1715Z at the CTO terminal -- verbatim record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260804_1715Z_GLOBAL_ROLLFORWARD_DESIGN.md; folded into the CANRTE frame per CTO's dispatch ask 172343Z)</priority>

<title>Global T+2 roll-forward SCOPING (design-only): cottonwood's last real value carried as a MARKED INTERIM on lagged Global dates, overwritten on real-value arrival -- one time period for everyone</title>

<context>
ANDREW'S RULING (read the verbatim record first -- the phrasing is the ruling): BD/cottonwood is
effectively T+2 against T+1 for 49f+inflection, so the GLOBAL scope rolls forward cottonwood's
last real value as a MARKED INTERIM on the lagged dates, overwritten by the real value when it
arrives -- everyone stays in one time period. Surfaces: Global aum-metrics.json +
account-distribution.json + aggregate-aua-timeseries.json.

TWO LAW INTERACTIONS, ALREADY DISPOSITIONED IN THE RECORD (carry them, do not re-litigate):
(1) no-LOCF remains the PER-FIRM law untouched -- the Global fold gets a DECLARED, MARKED carry,
same family as the existing carry-window machinery; (2) the 1646Z frontier-clamp edict [a]
STANDS as the immediate fix -- the roll-forward is the DURABLE layer that makes the clamp
naturally non-binding, and is NOT read as replacing it absent Andrew's word.

SEAT WALL (Andrew's own naming, record it in your artifact): 0.5.0_AE_OpalETL implements the
cloud side and ANDREW BRINGS THEM IN HIMSELF -- your scoping document HANDS OFF to that seat;
NOBODY (you, me, CTO) dispatches 0.5.0_AE on this. Your deliverable must be readable by that
seat cold.

AMENDED 1738Z (CTO source-grounded simplification, his 173824Z -- dim_mdpf_aggregate_aua_
timeseries.py:1940-2030 + :1749-1775 read this hour): THE CARRY MACHINERY ALREADY EXISTS for
aggregate-aua-timeseries -- the Global fold already (a) carries cottonwood's last measured value
within the roster-derived gate_policy window (cottonwood 3 TD); (b) labels every carried point
carried_at_declared_cadence(as_of=...) with as_of_by_partner -- Andrew's marked-interim semantic
VERBATIM; (c) overwrites naturally on rebuild when real data arrives; (d) DE's new clamp reads
carried points as PRESENT, so the frontier self-advances with zero further FE work. Today
clamped to 07-30 only because the freeze EXCEEDED the declared window and the bounded carry
correctly refused -- the fix for a frozen pipeline is the PIPELINE (unfrozen today), never a
wider window. Record note (fold into your artifact): DE's clamp and the fold carry were built
as two halves of ONE mechanism without either seat knowing it -- the inversion Andrew intuited
is the two halves meeting.
</context>

<scope>
DESIGN-ONLY scoping document (zero code, zero serve contact -- the CANRTE walls apply).
NARROWED per the 1738Z amendment -- NO new carry engine, NO window widening, and
aggregate-aua-timeseries needs NO design (the mechanism is live; cite it):
1. EXTEND THE SAME CARRY BASIS (existing window + carried_at_declared_cadence labels + natural
   overwrite) to the TWO derived artifacts: Global aum-metrics.json -- the real design work is
   PER-MODEL carry in by_model, and the composition gate MUST HOLD under carried legs (state
   how); and Global account-distribution.json -- account-COUNT carry semantics.
2. THE STEADY-STATE CONTRACT, stated: cot at T+2 inside its 3-TD declared window = always
   carried on the T+1 tail = Global frontier at T+1 every day, PROVIDED THE DAILY CHAIN RUNS --
   name the NEVER#4 schedule work as the real dependency, routed to CTO, not absorbed here.
3. THE LAG DECLARATIONS AS W-1 BINDING ROWS: per-firm effective-lag declared in
   route_bindings.yaml (landed @8058f5523 -- fold as the L3 Global-fold contract row family).
   A lag is a DECLARED property, never re-inferred at run time.
4. FRONTIER-CLAMP INTERACTION: one paragraph -- the clamp already reads carried points as
   PRESENT (mechanism live), so with the derived artifacts carrying, it becomes naturally
   non-binding; it is NOT removed by this design absent Andrew's word.
5. HANDOFF SECTION for 0.5.0_AE: the (much smaller) implementation surface named per artifact,
   inputs, acceptance shape incl. the marked-interim round-trip (interim served -> real arrives
   -> overwrite verified) -- written cold-readable.
6. Sequencing at your seat is YOURS: interleave with W-2 + tonight's ~02Z clock.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before design">
    <step>
      <run>read the Andrew-direct record verbatim + re-read your Phase-A SS on the Global fold; comp-pipescript io on the Global fold producer --pipeline mdpf (current manifest)</run>
      <expect>The ruling's exact words grounded; the fold's current inputs/outputs captured as the design baseline.</expect>
      <if_mismatch>Surface any conflict between the ruling's surface list and the live fold outputs BEFORE designing -- do not adjudicate it.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before submitting">
    <step>
      <run>self-audit: marking mechanism artifact-carried + reader-distinguishable; overwrite semantics idempotent; lag rows declared-not-inferred; clamp interaction stated; 0.5.0_AE handoff cold-readable; every claim file:line @ commit or labeled INFERRED</run>
      <expect>All six scope items present; the two law dispositions carried verbatim, not re-litigated.</expect>
      <if_mismatch>STOP and fix -- a scoping doc that re-opens a dispositioned law costs a sovereign round-trip.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after submitting">
    <step>
      <run>deliver to me + CTO (program triangle); the 0.5.0_AE handoff waits for ANDREW'S bring-in -- you hand the document over only when that seat arrives asking, citing his word</run>
      <expect>CTO + I can review without a follow-up ask; the seat wall holds (no dispatch to 0.5.0_AE from anyone in the fabric).</expect>
      <if_mismatch>REWORK per CTO redline.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Folds into YOUR OWN W-1 (lag rows) -- self-coordinate, same seat. The three Global surfaces are
live served artifacts: this TO touches NONE of them (design-only; implementation is 0.5.0_AE's
on Andrew's bring-in, and any serve-touching lands under the W-5-class gates when its time
comes). The frontier-clamp FE work is DE's under the 1646Z edict -- your design cites it,
never modifies it.
</cross_domain_coordination>

<acceptance_criteria>
1. Scoping document delivered with all six scope items; marking mechanism artifact-carried and
   reader-distinguishable; overwrite semantics with idempotency stated.
2. Lag declarations specified as W-1 binding rows (declared, never inferred).
3. Both law dispositions carried verbatim; the 0.5.0_AE seat wall recorded in the artifact.
4. Zero code, zero serve contact.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">ANDREW-DIRECT ~1715Z verbatim record (CTO deliverables path above) + CTO dispatch ask 172343Z</ref>
  <ref type="frame">MDPF_CANRTE plan @c68f238e5 (W-1 binding config = the lag rows' home); Phase-A design @ab2d2f167 (Global fold)</ref>
  <ref type="edict">Andrew 1646Z item [a] frontier clamp (STANDS -- the immediate fix this design makes naturally non-binding)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
